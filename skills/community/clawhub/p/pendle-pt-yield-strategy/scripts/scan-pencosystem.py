#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'data'
DEFAULT_OUT = DATA / 'pencosystem.latest.json'
URL = 'https://pendle.finance/pencosystem'

ENTRY_RE = re.compile(
    r'\{"name":\d+,"iconUrl":\d+,"category":\d+,"url":\d+,"description":\d+(?:,"isOnLandingPage":\d+)?\}',
    re.S,
)


def iso_now():
    return datetime.now(timezone.utc).isoformat()


def fetch_html(url: str) -> str:
    req = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    })
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='ignore')


def parse_from_json_script(html: str):
    scripts = re.findall(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>', html, re.S)
    for raw in scripts:
        if 'protocols' not in raw or 'Contango' not in raw:
            continue
        try:
            arr = json.loads(raw)
        except Exception:
            continue
        partners = []
        for idx, item in enumerate(arr):
            if not isinstance(item, dict):
                continue
            # detect protocol records in the Nuxt payload by field shape
            if set(['name', 'iconUrl', 'category', 'url', 'description']).issubset(item.keys()):
                try:
                    name = arr[item['name']]
                    icon = arr[item['iconUrl']]
                    category = arr[item['category']]
                    url = arr[item['url']]
                    description = arr[item['description']]
                    is_landing = bool(arr[item['isOnLandingPage']]) if 'isOnLandingPage' in item and isinstance(item['isOnLandingPage'], int) else False
                    if isinstance(name, str) and isinstance(category, str) and isinstance(url, str):
                        partners.append({
                            'name': name,
                            'category': category.lower(),
                            'url': url,
                            'description': description if isinstance(description, str) else '',
                            'iconUrl': icon if isinstance(icon, str) else None,
                            'isOnLandingPage': is_landing,
                            'sourceType': 'live-nuxt-json',
                        })
                except Exception:
                    continue
        if partners:
            # de-dup by name/url
            seen = set()
            deduped = []
            for p in partners:
                key = (p['name'], p['url'])
                if key in seen:
                    continue
                seen.add(key)
                deduped.append(p)
            return deduped
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(DEFAULT_OUT))
    args = ap.parse_args()

    html = fetch_html(URL)
    partners = parse_from_json_script(html)

    result = {
        'generatedAt': iso_now(),
        'sourceUrl': URL,
        'partnerCount': len(partners),
        'partners': partners,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2))
    print(str(out))
    print(f'Parsed {len(partners)} Pencosystem partners from structured Nuxt payload')


if __name__ == '__main__':
    main()
