import mastodon
from mastodon import Mastodon
from bs4 import BeautifulSoup
import regex

N_CYRILLIC_SYMBOLS = 3
MESSAGE_LANG = 'ru'

m = {}

class Listener(mastodon.StreamListener):

    def on_update(self, status):
        m_text = BeautifulSoup(status.content, 'html.parser').text
        m_lang = status.language
        if m_lang is None:
            m_lang = 'unknown'
        m_user = status.account.username
        if (m_lang == MESSAGE_LANG) or (len(regex.findall(r'\p{IsCyrillic}', m_text)) >= N_CYRILLIC_SYMBOLS):
            #print(f'{m_user}', m_text[:150])
            m.status_reblog(status)


m = Mastodon(access_token="<access token>", api_base_url="https://mastodon.social/")
m.stream_public(Listener())
