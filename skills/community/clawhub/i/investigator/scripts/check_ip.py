#!/usr/bin/env python3
import json
import sys
import requests


def fetch(url):
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent': 'OpenClaw-osint-investigator/1.0'})
        return {'status_code': r.status_code, 'body': r.json() if 'json' in r.headers.get('content-type','') else r.text[:1000]}
    except Exception as e:
        return {'error': str(e)}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'usage: check_ip.py <ip>'}))
        return
    ip = sys.argv[1].strip()
    out = {
        'ip': ip,
        'ipinfo': fetch(f'https://ipinfo.io/{ip}/json'),
        'ip_api': fetch(f'http://ip-api.com/json/{ip}'),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
