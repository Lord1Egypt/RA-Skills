#!/usr/bin/env python3
import json
import subprocess
import sys
import requests
import shutil


def run(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=15)
        return out.strip()
    except Exception as e:
        return f'ERROR: {e}'


def fetch_rdap(domain):
    try:
        r = requests.get(f'https://rdap.org/domain/{domain}', timeout=15, headers={'User-Agent': 'OpenClaw-osint-investigator/1.0'})
        if r.status_code == 200:
            data = r.json()
            return {
                'ldhName': data.get('ldhName'),
                'handle': data.get('handle'),
                'status': data.get('status'),
            }
        return {'error': f'rdap returned {r.status_code}'}
    except Exception as e:
        return {'error': str(e)}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'usage: check_domain.py <domain>'}))
        return
    domain = sys.argv[1].strip()
    whois_out = 'WHOIS command not available'
    if shutil.which('whois'):
        whois_out = run(['bash', '-lc', f'whois {domain} | sed -n "1,80p"'])
    result = {
        'domain': domain,
        'whois': whois_out,
        'rdap': fetch_rdap(domain),
        'dns_a': run(['bash', '-lc', f'dig +short {domain} A']),
        'dns_mx': run(['bash', '-lc', f'dig +short {domain} MX']),
        'dns_txt': run(['bash', '-lc', f'dig +short {domain} TXT']),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
