#!/usr/bin/env python3
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

DEFAULT_BASE_URL = 'https://example-nightscout.herokuapp.com/'
TZ = ZoneInfo('America/Los_Angeles')


def get_base_url() -> str:
    base = (sys.argv[sys.argv.index('--url') + 1] if '--url' in sys.argv and sys.argv.index('--url') + 1 < len(sys.argv) else None) or None
    if not base:
        import os
        base = os.environ.get('NIGHTSCOUT_BASE_URL')
    if not base:
        base = DEFAULT_BASE_URL
    return base.rstrip('/') + '/'


def fetch_json(path: str):
    url = urllib.parse.urljoin(get_base_url(), path)
    req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw nightscout-local'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode('utf-8'))


def fmt_ts(ms: int | None):
    if not ms:
        return None
    return datetime.fromtimestamp(ms / 1000, TZ).strftime('%Y-%m-%d %H:%M:%S %Z')


def get_status():
    data = fetch_json('/api/v1/status.json')
    settings = data.get('settings', {})
    return {
        'success': True,
        'name': data.get('name'),
        'version': data.get('version'),
        'serverTime': data.get('serverTime'),
        'customTitle': settings.get('customTitle'),
        'units': settings.get('units'),
    }


def get_current():
    rows = fetch_json('/api/v1/entries/current.json')
    if not rows:
        return {'success': False, 'error': 'no current entries returned'}
    row = rows[0]
    return {
        'success': True,
        'sgv': row.get('sgv'),
        'units': 'mg/dL',
        'direction': row.get('direction') or row.get('trend'),
        'timestamp': fmt_ts(row.get('date')),
        'device': row.get('device'),
        'raw': row,
    }


def get_recent(count: int):
    rows = fetch_json(f'/api/v1/entries.json?count={count}')
    out = []
    for row in rows:
        out.append({
            'sgv': row.get('sgv'),
            'units': 'mg/dL',
            'direction': row.get('direction') or row.get('trend'),
            'timestamp': fmt_ts(row.get('date')),
            'device': row.get('device'),
        })
    return {'success': True, 'count': len(out), 'entries': out}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else 'current'
    try:
        if cmd == 'status':
            result = get_status()
        elif cmd == 'current':
            result = get_current()
        elif cmd == 'recent':
            count = int(argv[2]) if len(argv) > 2 else 6
            result = get_recent(count)
        else:
            result = {'success': False, 'error': 'usage: nightscout_read.py [status|current|recent <count>]'}
    except Exception as e:
        result = {'success': False, 'error': str(e)}
    print(json.dumps(result, indent=2))
    return 0 if result.get('success') else 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
