#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import os

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
INDEX_DIR = ROOT / 'memory' / 'index'
REPORT_PATH = ROOT / 'memory' / 'reports' / 'hm4d-benchmark-2026-03-28.md'


def load_json(path: Path):
    if not path.exists():
        return {} if path.suffix == '.json' else []
    return json.loads(path.read_text(encoding='utf-8'))


def run() -> dict:
    master = load_json(INDEX_DIR / 'memory-master-index.json')
    thin = load_json(INDEX_DIR / 'thin-index.json')
    delta = load_json(INDEX_DIR / 'delta-summaries.json')

    total_records = master.get('total_records', 0)
    latest_records = len(master.get('latest_records', []))
    thin_entries = len(thin) if isinstance(thin, list) else 0
    delta_count = delta.get('delta_count', 0)
    salience = master.get('by_salience_level', {})
    retention = master.get('by_retention_tier', {})

    score = 0
    checks = []

    c1 = thin_entries <= latest_records and thin_entries > 0
    checks.append(('thin_index_within_latest', c1))
    score += 1 if c1 else 0

    c2 = delta_count < total_records
    checks.append(('delta_below_total', c2))
    score += 1 if c2 else 0

    c3 = salience.get('hot', 0) >= salience.get('warm', 0)
    checks.append(('hot_not_below_warm', c3))
    score += 1 if c3 else 0

    c4 = retention.get('structured', 0) >= retention.get('compact', 0)
    checks.append(('structured_not_below_compact', c4))
    score += 1 if c4 else 0

    c5 = total_records <= 25
    checks.append(('record_budget_ok', c5))
    score += 1 if c5 else 0

    payload = {
        'total_records': total_records,
        'latest_records': latest_records,
        'thin_entries': thin_entries,
        'delta_count': delta_count,
        'salience': salience,
        'retention': retention,
        'checks': checks,
        'score': score,
        'max_score': 5,
    }
    return payload


def write_report(payload: dict) -> None:
    lines = [
        '# HM4D Benchmark · 2026-03-28',
        '',
        '## Summary',
        f"- score: {payload['score']}/{payload['max_score']}",
        f"- total_records: {payload['total_records']}",
        f"- latest_records: {payload['latest_records']}",
        f"- thin_entries: {payload['thin_entries']}",
        f"- delta_count: {payload['delta_count']}",
        '',
        '## Salience',
    ]
    for k, v in payload['salience'].items():
        lines.append(f'- {k}: {v}')
    lines.extend(['', '## Retention'])
    for k, v in payload['retention'].items():
        lines.append(f'- {k}: {v}')
    lines.extend(['', '## Checks'])
    for name, ok in payload['checks']:
        lines.append(f'- {name}: {"PASS" if ok else "FAIL"}')
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> int:
    payload = run()
    write_report(payload)
    print(json.dumps({
        'report': str(REPORT_PATH),
        'score': payload['score'],
        'max_score': payload['max_score'],
        'total_records': payload['total_records'],
        'delta_count': payload['delta_count'],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
