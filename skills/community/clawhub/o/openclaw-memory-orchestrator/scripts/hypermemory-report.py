#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import os

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
INDEX_DIR = ROOT / 'memory' / 'index'
REPORT_PATH = ROOT / 'memory' / 'reports' / 'hypermemory-report-2026-03-28.md'


def load_json(path: Path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding='utf-8'))


def main() -> int:
    master = load_json(INDEX_DIR / 'memory-master-index.json')
    thin = load_json(INDEX_DIR / 'thin-index.json')
    delta = load_json(INDEX_DIR / 'delta-summaries.json')
    manifest = load_json(INDEX_DIR / 'manifest.json')

    lines = [
        '# HyperMemory-4D Report · 2026-03-28',
        '',
        '## HM4D Status',
        f"- enabled: {manifest.get('strategy', {}).get('hm4d_enabled', False)}",
        f"- total_records: {master.get('total_records', 0)}",
        f"- latest_records: {len(master.get('latest_records', []))}",
        f"- thin_index_entries: {len(thin) if isinstance(thin, list) else 0}",
        f"- delta_count: {delta.get('delta_count', 0)}",
        '',
        '## Salience Distribution',
    ]

    for key, value in (master.get('by_salience_level') or {}).items():
        lines.append(f'- {key}: {value}')

    lines.extend(['', '## Retention Distribution'])
    for key, value in (master.get('by_retention_tier') or {}).items():
        lines.append(f'- {key}: {value}')

    lines.extend(['', '## Latest Records'])
    for item in master.get('latest_records', [])[-10:]:
        lines.append(
            f"- [{item.get('type')}] {item.get('title')} | salience={item.get('salience_level')} | tier={item.get('retention_tier')} | delta_from={item.get('delta_from')}"
        )

    lines.extend(['', '## Output Files'])
    for rel in [
        'memory/index/memory-master-index.json',
        'memory/index/thin-index.json',
        'memory/index/delta-summaries.json',
    ]:
        path = ROOT / rel
        lines.append(f'- {rel} ({path.stat().st_size if path.exists() else 0} bytes)')

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({
        'report': str(REPORT_PATH),
        'total_records': master.get('total_records', 0),
        'thin_index_entries': len(thin) if isinstance(thin, list) else 0,
        'delta_count': delta.get('delta_count', 0),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
