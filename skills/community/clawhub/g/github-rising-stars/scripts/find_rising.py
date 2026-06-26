#!/usr/bin/env python3
"""
find_rising.py - Find fast-growing GitHub repos not yet on Trending
Usage: python3 find_rising.py [--days N] [--min-stars N] [--top N] [--lang LANG]
"""

import urllib.request
import urllib.parse
import json
import time
import argparse
from datetime import datetime, timedelta

# Spam/low-quality keywords to filter out
SPAM_KEYWORDS = [
    'hack', 'cheat', 'crack', 'free-follower', 'views-likes',
    'testnet-bot', 'trading-bot', 'multi-account', 'bypass', 'exploit',
    'keygen', 'serial', 'mod-menu', 'aimbot', 'esp-hack',
    'airdrop', 'mining', 'crypto-bot', 'pump', 'sniper',
    'followers-bot', 'views-bot', 'likes-bot',
]


def is_spam(repo):
    text = (repo['full_name'] + ' ' + (repo['description'] or '')).lower()
    return any(kw in text for kw in SPAM_KEYWORDS)


def search_github(query, sort='stars', order='desc', per_page=30):
    params = urllib.parse.urlencode({
        'q': query,
        'sort': sort,
        'order': order,
        'per_page': per_page,
    })
    url = f'https://api.github.com/search/repositories?{params}'
    req = urllib.request.Request(url, headers={
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'github-rising-stars-skill/1.0',
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read()).get('items', [])
    except Exception as e:
        print(f'  [warn] request failed: {e}')
        return []


def find_rising(days=3, min_stars=20, top=15, lang=None):
    since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    since_wide = (datetime.now() - timedelta(days=days + 2)).strftime('%Y-%m-%d')

    lang_filter = f' language:{lang}' if lang else ''

    queries = [
        f'created:>{since} stars:>{min_stars}{lang_filter}',
        f'created:>{since_wide} stars:{min_stars * 2}..500{lang_filter}',
        f'pushed:>{since} stars:{min_stars}..300 fork:false{lang_filter}',
    ]

    all_repos = {}
    for q in queries:
        items = search_github(q)
        for r in items:
            all_repos[r['id']] = r
        time.sleep(0.8)

    now = datetime.now()
    results = []
    for r in all_repos.values():
        if is_spam(r) or r.get('fork'):
            continue
        if r['stargazers_count'] < min_stars:
            continue
        created = datetime.fromisoformat(r['created_at'].replace('Z', ''))
        days_old = max((now - created).total_seconds() / 86400, 0.5)
        if days_old > days + 2.5:
            continue
        rate = r['stargazers_count'] / days_old
        results.append((rate, days_old, r))

    results.sort(key=lambda x: -x[0])
    return results[:top]


def main():
    parser = argparse.ArgumentParser(description='Find fast-growing GitHub repos before they hit Trending')
    parser.add_argument('--days',      type=int,   default=3,  help='Look back N days (default: 3)')
    parser.add_argument('--min-stars', type=int,   default=20, help='Minimum star count (default: 20)')
    parser.add_argument('--top',       type=int,   default=15, help='Number of results (default: 15)')
    parser.add_argument('--lang',      type=str,   default=None, help='Filter by language (e.g. Python, TypeScript)')
    parser.add_argument('--json',      action='store_true',     help='Output as JSON')
    args = parser.parse_args()

    results = find_rising(
        days=args.days,
        min_stars=args.min_stars,
        top=args.top,
        lang=args.lang,
    )

    if args.json:
        out = []
        for rate, days_old, r in results:
            out.append({
                'rank': len(out) + 1,
                'rate_per_day': round(rate, 1),
                'stars': r['stargazers_count'],
                'age_days': round(days_old, 1),
                'full_name': r['full_name'],
                'url': r['html_url'],
                'language': r.get('language'),
                'description': r.get('description'),
                'topics': r.get('topics', []),
            })
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    since_label = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')
    print(f'\n🔥 Fast-growing GitHub repos (created after {since_label}, ranked by stars/day)\n')
    print(f'  {"#":>2}  {"Rate":>8}  {"Stars":>6}  {"Age":>5}  {"Language":<13}  Repository')
    print('  ' + '-' * 85)

    for i, (rate, days_old, r) in enumerate(results, 1):
        age_str = f'{days_old * 24:.0f}h' if days_old < 1 else f'{days_old:.1f}d'
        lang = (r.get('language') or '-')[:12]
        desc = (r.get('description') or '')[:55]
        print(f'  {i:>2}  {rate:>6.1f}/d  {r["stargazers_count"]:>6}⭐  {age_str:>5}  {lang:<13}  {r["full_name"]}')
        if desc:
            print(f'       {"":8}  {"":6}  {"":5}  {"":13}  ↳ {desc}')

    print(f'\n  Total: {len(results)} repos shown. Run with --json for machine-readable output.\n')


if __name__ == '__main__':
    main()
