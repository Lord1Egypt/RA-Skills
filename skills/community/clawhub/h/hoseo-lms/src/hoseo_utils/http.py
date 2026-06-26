import urllib.request
import urllib.parse
import http.cookiejar

from hoseo_utils.constants import USER_AGENT


def install_cookie_opener():
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    urllib.request.install_opener(opener)
    return opener


def http_get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(req).read().decode("utf-8")


def http_post(url: str, data: dict) -> str:
    payload = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(req).read().decode("utf-8")

