#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print('usage: extract_covers_mlb.py <html-file>', file=sys.stderr)
        sys.exit(1)

    html = Path(sys.argv[1]).read_text()
    blocks = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S | re.I)
    events = []
    for block in blocks:
        block = block.strip()
        try:
            data = json.loads(block)
        except Exception:
            continue
        if isinstance(data, dict) and data.get('@type') == 'SportsEvent':
            away = ((data.get('awayTeam') or {}).get('name') or '').strip()
            home = ((data.get('homeTeam') or {}).get('name') or '').strip()
            if away and home:
                events.append({
                    'event': f'{away} at {home}',
                    'startDate': data.get('startDate'),
                    'url': data.get('url') or ((data.get('location') or {}).get('url')),
                    'raw_name': data.get('name'),
                })
    print(json.dumps({'events': events}, indent=2))


if __name__ == '__main__':
    main()
