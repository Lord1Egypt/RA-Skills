from __future__ import annotations

import argparse
import json
from pathlib import Path

TEMPLATE = '''from __future__ import annotations

import argparse
import json
from pathlib import Path

import requests

DEFAULT_HEADERS = {
    "origin": "{origin}",
    "referer": "{referer}",
    "user-agent": "Mozilla/5.0",
}}


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").strip()


def build_session(cookie_file: str, csrf_file: str = "", authorization_file: str = "") -> requests.Session:
    s = requests.Session()
    headers = dict(DEFAULT_HEADERS)
    headers["cookie"] = read_text(cookie_file)
    if csrf_file:
        headers["x-csrf-token"] = read_text(csrf_file)
    if authorization_file:
        headers["authorization"] = read_text(authorization_file)
    s.headers.update(headers)
    return s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cookie-file", required=True)
    ap.add_argument("--csrf-file", default="")
    ap.add_argument("--authorization-file", default="")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    session = build_session(args.cookie_file, args.csrf_file, args.authorization_file)
    request_template = {request_template}

    # Replace dynamic fields before real use.
    print(json.dumps({{"request_template": request_template}}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def main() -> int:
    ap = argparse.ArgumentParser(description='Create a first-pass direct client scaffold from a captured request JSON.')
    ap.add_argument('request_json')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.request_json).read_text(encoding='utf-8'))
    req = data.get('request', data)
    headers = {h.get('name', ''): h.get('value', '') for h in req.get('headers', [])}
    origin = headers.get('origin', headers.get('Origin', 'https://example.com'))
    referer = headers.get('referer', headers.get('Referer', origin + '/'))
    request_template = {
        'method': req.get('method', 'POST'),
        'url': req.get('url', ''),
        'queryString': req.get('queryString', []),
        'postData': req.get('postData', {}),
    }
    rendered = TEMPLATE.format(
        origin=origin.replace('{', '{{').replace('}', '}}'),
        referer=referer.replace('{', '{{').replace('}', '}}'),
        request_template=json.dumps(request_template, indent=2, ensure_ascii=False),
    )
    Path(args.out).write_text(rendered, encoding='utf-8')
    print(json.dumps({'out': args.out}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
