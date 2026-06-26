#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import os

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
INDEX_DIR = ROOT / 'memory' / 'index'
REPORT_PATH = ROOT / 'memory' / 'reports' / 'phase2-packed-compare-2026-03-28.md'

QUERIES = [
    'Auto-generated daily memory',
    'Session bootstrap',
    'Durable Memory Addendum',
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def search_titles(items, query, key='title'):
    q = query.lower()
    hits = []
    for item in items:
        title = (item.get(key) or '').lower()
        if q in title:
            hits.append(item)
    return hits


def main() -> int:
    thin = load_json(INDEX_DIR / 'thin-index.json')
    rv = load_json(INDEX_DIR / 'retrieval-view.json')
    packed = load_json(INDEX_DIR / 'retrieval-view-packed.json')
    packed_items = packed.get('items', [])

    rows = []
    pass_count = 0
    for query in QUERIES:
        thin_hits = search_titles(thin, query, 'title')
        rv_hits = search_titles(rv, query, 't')
        packed_hits = search_titles(packed_items, query, 't')
        ok = len(thin_hits) == len(rv_hits) == len(packed_hits) and len(thin_hits) > 0
        if ok:
            pass_count += 1
        rows.append({
            'query': query,
            'thin_hits': len(thin_hits),
            'retrieval_view_hits': len(rv_hits),
            'packed_hits': len(packed_hits),
            'pass': ok,
        })

    score = f"{pass_count}/{len(QUERIES)}"
    lines = [
        '# Phase2 Packed Compare · 2026-03-28',
        '',
        f'- score: {score}',
        f'- thin_index_bytes: {(INDEX_DIR / "thin-index.json").stat().st_size}',
        f'- retrieval_view_bytes: {(INDEX_DIR / "retrieval-view.json").stat().st_size}',
        f'- packed_bytes: {(INDEX_DIR / "retrieval-view-packed.json").stat().st_size}',
        '',
        '## Query Results',
    ]
    for row in rows:
        lines.append(f"- {row['query']}: thin={row['thin_hits']} retrieval_view={row['retrieval_view_hits']} packed={row['packed_hits']} pass={row['pass']}")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({
        'report': str(REPORT_PATH),
        'score': score,
        'rows': rows,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
