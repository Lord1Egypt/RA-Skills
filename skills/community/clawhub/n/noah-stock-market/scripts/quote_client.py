#!/usr/bin/env python3
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urljoin

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None


WORKSPACE = Path(__file__).resolve().parents[3]
SECRETS_FILES = [
    WORKSPACE / '.secrets' / 'noah-market.env',
    Path.home() / '.openclaw' / '.secrets' / 'noah-market.env',
]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ[key.strip()] = value.strip()


for _env_file in SECRETS_FILES:
    load_env_file(_env_file)


class NoahQuoteClient:
    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None, timeout: int = 15):
        self.base_url = (base_url or os.getenv('NOAH_API_BASE_URL', 'https://securities-open-api.noahgroup.com')).rstrip('/') + '/'
        self.token = token or os.getenv('NOAH_MARKET_APIKEY', '') or os.getenv('NOAH_MARKET_TOKEN', '')
        self.timeout = timeout
        if not self.base_url:
            raise ValueError('NOAH_API_BASE_URL is missing')
        if not self.token:
            raise ValueError('未能加载 market token。')
        if requests is None:
            raise RuntimeError('requests is required')

    def _headers(self) -> Dict[str, str]:
        return {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json',
        }

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = urljoin(self.base_url, path.lstrip('/'))
        resp = requests.get(url, headers=self._headers(), params=params or {}, timeout=self.timeout)
        return self._normalize_response(resp)

    def post(self, path: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = urljoin(self.base_url, path.lstrip('/'))
        resp = requests.post(url, headers={**self._headers(), 'Content-Type': 'application/json'}, json=payload or {}, timeout=self.timeout)
        return self._normalize_response(resp)

    def _normalize_response(self, resp) -> Dict[str, Any]:
        try:
            body = resp.json()
        except Exception:
            return {
                'ok': False,
                'http_status': resp.status_code,
                'message': resp.text[:500],
                'data': None,
            }

        success = body.get('success', False)
        return {
            'ok': bool(success) and resp.ok,
            'http_status': resp.status_code,
            'code': body.get('code'),
            'message': body.get('msg', ''),
            'data': body.get('data'),
            'raw': body,
        }


if __name__ == '__main__':
    client = NoahQuoteClient()
    print(json.dumps({'base_url': client.base_url, 'token_loaded': bool(client.token)}, ensure_ascii=False))
