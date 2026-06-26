#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import os

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
INDEX_DIR = ROOT / 'memory' / 'index'
REPORT_PATH = ROOT / 'memory' / 'reports' / 'phase2-route-simulator-2026-03-28.md'

QUERIES = [
    'Auto-generated daily memory',
    'Session bootstrap',
    'Durable Memory Addendum',
    '偏好 · Session bootstrap',
    '專案狀態 · Auto-generated daily memory',
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def search_titles(items, query, key):
    q = query.lower()
    return [item for item in items if q in (item.get(key) or '').lower()]


def main() -> int:
    hot = load_json(INDEX_DIR / 'retrieval-view-hot.json').get('items', [])
    packed = load_json(INDEX_DIR / 'retrieval-view-packed.json').get('items', [])

    rows = []
    fast_hits = 0
    fallback_hits = 0
    misses = 0

    for query in QUERIES:
        hot_hits = search_titles(hot, query, 't')
        packed_hits = search_titles(packed, query, 't')
        if hot_hits:
            route = 'fast_path'
            fast_hits += 1
        elif packed_hits:
            route = 'fallback_path'
            fallback_hits += 1
        else:
            route = 'miss'
            misses += 1
        rows.append({
            'query': query,
            'route': route,
            'hot_hits': len(hot_hits),
            'packed_hits': len(packed_hits),
        })

    total = len(QUERIES)
    fast_rate = round((fast_hits / total) * 100, 2) if total else 0.0
    fallback_rate = round((fallback_hits / total) * 100, 2) if total else 0.0
    miss_rate = round((misses / total) * 100, 2) if total else 0.0

    lines = [
        '# Phase2 Route Simulator · 2026-03-28',
        '',
        f'- total_queries: {total}',
        f'- fast_hits: {fast_hits}',
        f'- fallback_hits: {fallback_hits}',
        f'- misses: {misses}',
        f'- fast_rate_pct: {fast_rate}',
        f'- fallback_rate_pct: {fallback_rate}',
        f'- miss_rate_pct: {miss_rate}',
        '',
        '## Routing Results',
    ]
    for row in rows:
        lines.append(f"- {row['query']}: route={row['route']} hot={row['hot_hits']} packed={row['packed_hits']}")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({
        'report': str(REPORT_PATH),
        'total_queries': total,
        'fast_hits': fast_hits,
        'fallback_hits': fallback_hits,
        'misses': misses,
        'fast_rate_pct': fast_rate,
        'fallback_rate_pct': fallback_rate,
        'miss_rate_pct': miss_rate,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
