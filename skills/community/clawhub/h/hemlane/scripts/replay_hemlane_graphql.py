#!/usr/bin/env python3
import argparse, json, os, sys
from pathlib import Path
from urllib import request, error

DEFAULT_ENDPOINT = os.environ.get('HEMLANE_GRAPHQL_ENDPOINT', 'https://api.hemlane.com/graphql')


def load_text(value: str) -> str:
    p = Path(value)
    if p.exists():
        return p.read_text()
    return value


def load_json(value: str):
    p = Path(value)
    text = p.read_text() if p.exists() else value
    return json.loads(text)


def build_headers(args):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': os.environ.get('HEMLANE_USER_AGENT', 'OpenClaw-Hemlane-Replay/1.0'),
    }
    cookie = args.cookie or os.environ.get('HEMLANE_COOKIE')
    csrf = args.csrf or os.environ.get('HEMLANE_CSRF_TOKEN')
    auth = args.authorization or os.environ.get('HEMLANE_AUTHORIZATION')
    apollo_name = os.environ.get('HEMLANE_APOLLO_CLIENT_NAME')
    apollo_version = os.environ.get('HEMLANE_APOLLO_CLIENT_VERSION')
    referer = os.environ.get('HEMLANE_REFERER')
    origin = os.environ.get('HEMLANE_ORIGIN', 'https://www.hemlane.com')

    if cookie:
        headers['Cookie'] = cookie
    if csrf:
        headers['x-csrf-token'] = csrf
    if auth:
        headers['Authorization'] = auth
    if apollo_name:
        headers['apollographql-client-name'] = apollo_name
    if apollo_version:
        headers['apollographql-client-version'] = apollo_version
    if referer:
        headers['Referer'] = referer
    if origin:
        headers['Origin'] = origin
    return headers


def redacted_headers(headers):
    out = {}
    for k, v in headers.items():
        if k.lower() in {'cookie', 'authorization', 'x-csrf-token'}:
            out[k] = '<redacted>'
        else:
            out[k] = v
    return out


def main():
    ap = argparse.ArgumentParser(description='Replay a Hemlane GraphQL request using env-based auth.')
    ap.add_argument('--query', required=True, help='GraphQL query string or path to file')
    ap.add_argument('--variables', default='{}', help='JSON string or path to variables file')
    ap.add_argument('--operation-name', help='Optional GraphQL operationName')
    ap.add_argument('--endpoint', default=DEFAULT_ENDPOINT)
    ap.add_argument('--cookie', help='Override HEMLANE_COOKIE')
    ap.add_argument('--csrf', help='Override HEMLANE_CSRF_TOKEN')
    ap.add_argument('--authorization', help='Override HEMLANE_AUTHORIZATION')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--pretty', action='store_true')
    args = ap.parse_args()

    payload = {
        'query': load_text(args.query),
        'variables': load_json(args.variables),
    }
    if args.operation_name:
        payload['operationName'] = args.operation_name

    headers = build_headers(args)

    if args.dry_run:
        print(json.dumps({
            'endpoint': args.endpoint,
            'headers': redacted_headers(headers),
            'payload': payload,
        }, indent=2))
        return

    req = request.Request(
        args.endpoint,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    try:
        with request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode('utf-8', errors='replace')
            try:
                data = json.loads(body)
                print(json.dumps(data, indent=2 if args.pretty else None))
            except Exception:
                print(body)
    except error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        sys.stderr.write(f'HTTP {e.code}\n{body}\n')
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f'{type(e).__name__}: {e}\n')
        sys.exit(1)


if __name__ == '__main__':
    main()
