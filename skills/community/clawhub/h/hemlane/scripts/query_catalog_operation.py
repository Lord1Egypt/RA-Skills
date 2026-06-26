#!/usr/bin/env python3
"""Replay read-oriented Hemlane GraphQL operations from operation-catalog.json.

Uses HAR-derived query text + sample variables, then merges caller-provided
variables. Auth comes from a captured auth JSON file or env vars, never from the
catalog.
"""
import argparse, copy, json, os, sys
from pathlib import Path
from urllib import request, error

ENDPOINT = os.environ.get('HEMLANE_GRAPHQL_ENDPOINT', 'https://api.hemlane.com/graphql')
CATALOG = Path(__file__).parent.parent / 'references' / 'operation-catalog.json'
KEEP_HEADERS = {'authorization','x-csrf-token','content-type','origin','referer','user-agent','cookie','accept','apollographql-client-name','apollographql-client-version'}
SENSITIVE = {'cookie','authorization','x-csrf-token'}
WRITE_KEYWORDS = ('create','update','delete','submit','logview','mutation','comment','send','revert')


def load_catalog():
    data = json.loads(CATALOG.read_text())
    return data if isinstance(data, list) else data.get('operations', [])


def find_operation(name):
    for op in load_catalog():
        if op.get('operationName') == name or op.get('name') == name:
            return op
    raise SystemExit(f'Operation not found: {name}')


def is_read_op(op):
    kind = str(op.get('kind') or '').lower()
    name = str(op.get('operationName') or op.get('name') or '').lower()
    query = str(op.get('queryExcerpt') or op.get('query') or '').lower()
    if kind and kind != 'query':
        return False
    return not any(k in name or k in query[:80] for k in WRITE_KEYWORDS)


def load_headers(path):
    headers = {}
    if path:
        data = json.loads(Path(path).read_text())
        headers = data.get('headers', data) if isinstance(data, dict) else {}
    env_map = {
        'HEMLANE_COOKIE': 'Cookie',
        'HEMLANE_CSRF_TOKEN': 'x-csrf-token',
        'HEMLANE_AUTHORIZATION': 'Authorization',
        'HEMLANE_USER_AGENT': 'User-Agent',
        'HEMLANE_REFERER': 'Referer',
        'HEMLANE_ORIGIN': 'Origin',
    }
    for env, header in env_map.items():
        if os.environ.get(env):
            headers[header] = os.environ[env]
    out = {}
    for k, v in (headers or {}).items():
        lk = k.lower()
        if lk in KEEP_HEADERS or lk.startswith('x-'):
            out[k] = str(v)
    out.setdefault('Content-Type', 'application/json')
    out.setdefault('Accept', 'application/json')
    out.setdefault('Origin', 'https://www.hemlane.com')
    return out


def deep_update(a, b):
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            deep_update(a[k], v)
        else:
            a[k] = v
    return a


def gql(headers, operation_name, query, variables):
    payload = {'operationName': operation_name, 'query': query, 'variables': variables}
    req = request.Request(ENDPOINT, data=json.dumps(payload).encode(), headers=headers, method='POST')
    try:
        with request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode('utf-8', 'replace')
    except error.HTTPError as e:
        body = e.read().decode('utf-8', 'replace')
        raise SystemExit(f'HTTP {e.code}: {body[:2000]}')
    data = json.loads(body)
    if data.get('errors'):
        raise SystemExit(json.dumps({'errors': data['errors']}, indent=2))
    return data


def main():
    ap = argparse.ArgumentParser(description='Replay a read-only Hemlane catalog GraphQL operation.')
    ap.add_argument('--operation-name', required=True)
    ap.add_argument('--auth-file')
    ap.add_argument('--variables-json', default='{}')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--output')
    args = ap.parse_args()

    op = find_operation(args.operation_name)
    if not is_read_op(op):
        raise SystemExit(f'Refusing non-read operation via generic catalog replay: {args.operation_name}')
    query = op.get('queryExcerpt') or op.get('query')
    if not query:
        raise SystemExit(f'No query text in catalog for {args.operation_name}')
    variables = copy.deepcopy(op.get('sampleVariables') or {})
    overrides = json.loads(args.variables_json or '{}')
    if not isinstance(overrides, dict):
        raise SystemExit('--variables-json must be a JSON object')
    deep_update(variables, overrides)
    headers = load_headers(args.auth_file)
    if args.dry_run:
        out = {
            'endpoint': ENDPOINT,
            'operationName': args.operation_name,
            'sourceFiles': op.get('files', []),
            'variables': variables,
            'headers': {k: ('<redacted>' if k.lower() in SENSITIVE else v) for k, v in headers.items()},
        }
    else:
        out = gql(headers, args.operation_name, query, variables)
    text = json.dumps(out, indent=2)
    if args.output:
        Path(args.output).write_text(text + '\n')
    print(text)


if __name__ == '__main__':
    main()
