#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import os

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
INDEX_DIR = ROOT / 'memory' / 'index'
REPORT_PATH = ROOT / 'memory' / 'reports' / 'phase2b-orchestrator-2026-03-28.md'
STATE_PATH = INDEX_DIR / 'phase2b-state.json'

QUERIES = [
    'Auto-generated daily memory',
    'Session bootstrap',
    'Durable Memory Addendum',
    '偏好 · Session bootstrap',
    '專案狀態 · Auto-generated daily memory',
    '不存在的查詢測試',
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def search(items, query, key='t'):
    q = query.lower()
    return [x for x in items if q in (x.get(key) or '').lower()]


def main() -> int:
    hot = load_json(INDEX_DIR / 'retrieval-view-hot.json').get('items', [])
    packed = load_json(INDEX_DIR / 'retrieval-view-packed.json').get('items', [])

    rows = []
    fast_hits = 0
    fallback_hits = 0
    misses = 0

    for query in QUERIES:
        hot_hits = search(hot, query)
        packed_hits = search(packed, query)
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

    state = {
        'fast_path': 'retrieval-view-hot.json',
        'fallback_path': 'retrieval-view-packed.json',
        'source_of_truth': 'thin-index.json',
        'fast_hits': fast_hits,
        'fallback_hits': fallback_hits,
        'misses': misses,
        'fast_rate_pct': fast_rate,
        'fallback_rate_pct': fallback_rate,
        'miss_rate_pct': miss_rate,
        'queries': rows,
    }
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    lines = [
        '# Phase2B Orchestrator Report · 2026-03-28',
        '',
        f'- fast_path: {state["fast_path"]}',
        f'- fallback_path: {state["fallback_path"]}',
        f'- source_of_truth: {state["source_of_truth"]}',
        f'- fast_hits: {fast_hits}',
        f'- fallback_hits: {fallback_hits}',
        f'- misses: {misses}',
        f'- fast_rate_pct: {fast_rate}',
        f'- fallback_rate_pct: {fallback_rate}',
        f'- miss_rate_pct: {miss_rate}',
        '',
        '## Query Routing',
    ]
    for row in rows:
        lines.append(f"- {row['query']}: route={row['route']} hot={row['hot_hits']} packed={row['packed_hits']}")
    REPORT_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(json.dumps({
        'state': str(STATE_PATH),
        'report': str(REPORT_PATH),
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
