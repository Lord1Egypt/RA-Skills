#!/usr/bin/env python3
import json
import os
import sys
import requests
from pathlib import Path
from urllib.parse import quote


def load_api_key():
    key = os.environ.get('HIBP_API_KEY')
    if key:
        return key.strip()
    p = Path.home() / '.openclaw' / 'secrets' / 'hibp_api_key'
    if p.exists():
        return p.read_text().strip()
    return None


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'usage: check_hibp.py <email>'}))
        return
    email = sys.argv[1].strip()
    key = load_api_key()
    if not key:
        print(json.dumps({'error': 'HIBP_API_KEY not configured'}))
        return

    url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{quote(email)}?truncateResponse=false'
    headers = {
        'hibp-api-key': key,
        'user-agent': 'OpenClaw-username-email-investigator/1.0',
    }
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 404:
            print(json.dumps({'email': email, 'breach_found': False, 'breaches': []}, ensure_ascii=False, indent=2))
            return
        if r.status_code != 200:
            print(json.dumps({'email': email, 'error': f'HIBP returned {r.status_code}', 'body': r.text[:500]}, ensure_ascii=False, indent=2))
            return
        data = r.json()
        out = {
            'email': email,
            'breach_found': True,
            'breaches': [
                {
                    'name': x.get('Name'),
                    'title': x.get('Title'),
                    'domain': x.get('Domain'),
                    'breach_date': x.get('BreachDate'),
                    'pwn_count': x.get('PwnCount'),
                    'data_classes': x.get('DataClasses', []),
                }
                for x in data
            ]
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({'email': email, 'error': str(e)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
