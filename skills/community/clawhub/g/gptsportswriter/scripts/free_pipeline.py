#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARSE_SCRIPT = ROOT / 'parse_free_odds.py'

SPORT_URLS = {
    'baseball_mlb': 'https://www.covers.com/sport/baseball/mlb/matchups',
    'basketball_nba': 'https://www.covers.com/sport/basketball/nba/matchups',
    'icehockey_nhl': 'https://www.covers.com/sport/hockey/nhl/matchups',
    'soccer_epl': 'https://www.covers.com/sport/soccer/england-premier-league/matchups',
}


def main():
    ap = argparse.ArgumentParser(description='Fetch public matchup page text and parse event candidates')
    ap.add_argument('--sport', required=True)
    args = ap.parse_args()

    url = SPORT_URLS.get(args.sport)
    if not url:
        print(json.dumps({'sport': args.sport, 'error': 'unsupported sport'}))
        sys.exit(1)

    try:
        import requests
    except Exception:
        print(json.dumps({'sport': args.sport, 'error': 'requests not installed'}))
        sys.exit(1)

    r = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
    html = r.text
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text('\n')
    except Exception:
        text = html

    with tempfile.NamedTemporaryFile('w+', delete=False) as f:
        f.write(text)
        tmp = f.name

    proc = subprocess.run([sys.executable, str(PARSE_SCRIPT), tmp], capture_output=True, text=True, check=True)
    parsed = json.loads(proc.stdout)
    print(json.dumps({'sport': args.sport, 'url': url, 'parsed': parsed}, indent=2))


if __name__ == '__main__':
    main()
