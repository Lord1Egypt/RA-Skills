"""Bounded HTTP reads, cached system proxy routing and credential-safe redirects."""
import base64
from email.utils import parsedate_to_datetime
from functools import lru_cache
import os
import json
import sys
import threading
import time
import urllib.request
from urllib.parse import unquote
from urllib.request import ProxyHandler, _parse_proxy, proxy_bypass

_route_lock = threading.Lock()

def registry_revision():
    if os.name == 'nt':
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings') as key:
                return winreg.QueryInfoKey(key)[2]
        except OSError:
            pass
    return None

@lru_cache(maxsize=128)
def _route(host, settings):
    return proxy_bypass(host)

class CachedProxyHandler(ProxyHandler):
    def proxy_open(self, req, proxy, protocol):
        original = req.type
        proxy_type, user, password, hostport = _parse_proxy(proxy)
        proxy_type = proxy_type or original
        settings = (tuple(sorted(self.proxies.items())), registry_revision())
        with _route_lock:
            bypass = _route(req.host, settings) if req.host else False
        if bypass:
            return None
        if user and password:
            credentials = base64.b64encode(f'{unquote(user)}:{unquote(password)}'.encode()).decode('ascii')
            req.add_header('Proxy-authorization', 'Basic ' + credentials)
        req.set_proxy(unquote(hostport), proxy_type)
        if original == proxy_type or original == 'https':
            return None
        return self.parent.open(req, timeout=req.timeout)

class CredentialRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if any(k.lower() in {'x-api-key', 'authorization'} for k, _ in req.header_items()):
            raise urllib.error.HTTPError(req.full_url, code, 'Authenticated API redirect refused', headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def install():
    urllib.request.install_opener(urllib.request.build_opener(CachedProxyHandler(), CredentialRedirectHandler()))

def bounded_read(response, limit=20 * 1024 * 1024):
    raw = response.read(limit + 1)
    if len(raw) > limit:
        raise ValueError('响应超过 20MB 上限；请缩小查询范围')
    return raw

def retry_delay(headers, attempt, maximum=15):
    value = headers.get('Retry-After') if headers else None
    if value:
        try:
            delay = float(value)
        except ValueError:
            try:
                delay = parsedate_to_datetime(value).timestamp() - time.time()
            except (ValueError, TypeError, OverflowError):
                delay = 1.5 * (attempt + 1)
    else:
        delay = 1.5 * (attempt + 1)
    return None if delay > maximum else max(0, delay)

def read_catalog(request, timeout=15):
    """Retry the free catalog on transient transport failures, never use old prices."""
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(bounded_read(response))
        except urllib.error.HTTPError as error:
            delay=retry_delay(error.headers,attempt)
            if error.code not in (429,500,502,503,504) or attempt==2 or delay is None:
                raise
        except (urllib.error.URLError,OSError,TimeoutError):
            if attempt==2:
                raise
            delay=1+attempt
        print('[目录重试] 临时网络错误，保留当前账号和查询范围',file=sys.stderr)
        time.sleep(delay)
