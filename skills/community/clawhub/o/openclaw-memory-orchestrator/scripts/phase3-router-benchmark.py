#!/usr/bin/env python3
from __future__ import annotations

import json
import importlib.util
from pathlib import Path
import os

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
REPORT = ROOT / 'memory' / 'reports' / 'phase3-router-benchmark-2026-03-28.md'


def loadmod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    router = loadmod('phase3_query_router', ROOT / 'scripts' / 'phase3-query-router.py')
    recovery = loadmod('phase3_miss_recovery', ROOT / 'scripts' / 'phase3-miss-recovery.py')
    queries = ['偏好 · Session bootstrap', 'Auto-generated daily memory', '2026-03-25 SSL', '不存在的查詢測試']
    rows = []
    routed = 0
    recovered = 0
    missed = 0

    for q in queries:
        cls = router.classify_query(q)
        rec = recovery.recover(q)
        if rec['stage'] != 'none':
            routed += 1
        if rec['stage'] == 'thin':
            recovered += 1
        if rec['stage'] == 'none':
            missed += 1
        rows.append({
            'query': q,
            'class': cls['class'],
            'route': cls['route'],
            'confidence': cls['confidence'],
            'stage': rec['stage'],
            'hits': rec['hits'],
        })

    total = len(queries)
    routed_rate = round(routed / total * 100, 2) if total else 0.0
    lines = [
        '# Phase3 Router Benchmark · 2026-03-28',
        '',
        f'- total_queries: {total}',
        f'- routed_hits: {routed}',
        f'- recovered_hits: {recovered}',
        f'- misses: {missed}',
        f'- routed_rate_pct: {routed_rate}',
        '',
        '## Results',
    ]
    for r in rows:
        lines.append(
            f"- {r['query']}: class={r['class']} route={r['route']} conf={r['confidence']} stage={r['stage']} hits={r['hits']}"
        )

    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({
        'report': str(REPORT),
        'total_queries': total,
        'routed_hits': routed,
        'recovered_hits': recovered,
        'misses': missed,
        'routed_rate_pct': routed_rate,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
