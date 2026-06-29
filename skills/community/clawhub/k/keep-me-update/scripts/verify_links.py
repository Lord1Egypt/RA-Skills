#!/usr/bin/env python3
"""
KeepMeUpdate — 链接全量验证器 / Link Verifier

Usage:
  python3 verify_links.py <path-to-digest.md>

Reads a Markdown file, extracts all URLs, sends HTTP GET to each.
Exits non-zero if any non-paywalled URL fails (4xx/5xx/timeout).

Paywalled domains (Bloomberg, Reuters, FT, WSJ) get a warning but
do not block delivery — their 401/403 is expected behavior.
"""

import re
import sys
import time
import urllib.request
import urllib.error
import ssl

# Known paywalled domains — 401/403 from these is expected, not a broken link
PAYWALLED_DOMAINS = {
    'bloomberg.com', 'reuters.com', 'ft.com', 'wsj.com',
    'economist.com', 'barrons.com', 'nytimes.com',
    'extremetech.com',
}

# Slower sites that need more time
SLOW_DOMAINS = {
    'github.com', 'arxiv.org', 'lobste.rs', 'patreon.com',
}

DEFAULT_TIMEOUT = 10
SLOW_TIMEOUT = 15

def get_timeout(url: str) -> int:
    for domain in SLOW_DOMAINS:
        if domain in url:
            return SLOW_TIMEOUT
    return DEFAULT_TIMEOUT

def is_paywalled(url: str) -> bool:
    for domain in PAYWALLED_DOMAINS:
        if domain in url:
            return True
    return False

def check_url(url: str) -> dict:
    ctx = ssl.create_default_context()

    timeout = get_timeout(url)
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    })

    try:
        r = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        return {'url': url, 'status': r.status, 'ok': r.status == 200}
    except urllib.error.HTTPError as e:
        code = e.code
        if is_paywalled(url) and code in (401, 403):
            return {'url': url, 'status': code, 'ok': True,
                    'note': 'paywall (expected)'}
        return {'url': url, 'status': code, 'ok': False}
    except urllib.error.URLError as e:
        return {'url': url, 'status': None, 'ok': False, 'error': str(e.reason)}
    except Exception as e:
        return {'url': url, 'status': None, 'ok': False, 'error': str(e)}

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 verify_links.py <path-to-markdown>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath, encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    urls = set(re.findall(r'https?://[^\s\)\[\]》<>\"\']+', content))
    if not urls:
        print("No URLs found in file.")
        sys.exit(0)

    # Check for duplicate URLs (case-insensitive)
    lower_urls = [u.lower() for u in urls]
    if len(lower_urls) != len(set(lower_urls)):
        from collections import Counter
        dups = [u for u, c in Counter(lower_urls).items() if c > 1]
        print(f"\n❌ DUPLICATE URLS: {dups}")
        print("Different stories sharing the same link — fix before delivery.\n")
        sys.exit(1)

    print(f"Verifying {len(urls)} links...\n")

    broken = []
    paywalled = []
    ok_count = 0

    for url in sorted(urls):
        result = check_url(url)
        if result['ok']:
            if result.get('note'):
                print(f"⚠️  {result['status']} {url[:70]} ({result['note']})")
                paywalled.append(result)
            else:
                print(f"✅ {result['status']} {url[:70]}")
            ok_count += 1
        else:
            err = result.get('error', f"HTTP {result['status']}")
            print(f"❌ {err} {url[:70]}")
            broken.append(result)
        time.sleep(0.1)  # rate-limit

    print(f"\n--- Summary ---")
    print(f"Total: {len(urls)}  OK: {ok_count}  Broken: {len(broken)}  Paywalled: {len(paywalled)}")

    if broken:
        print(f"\n❌ {len(broken)} broken links found — MUST fix:")
        for b in broken:
            err = b.get('error', f"HTTP {b['status']}")
            print(f"  {err}: {b['url']}")
        sys.exit(1)

    print("✅ All links verified OK.")
    sys.exit(0)

if __name__ == '__main__':
    main()
