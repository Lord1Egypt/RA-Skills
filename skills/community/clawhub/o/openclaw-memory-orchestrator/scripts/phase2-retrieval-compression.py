#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import os

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
INDEX_DIR = ROOT / 'memory' / 'index'
OUT_PATH = INDEX_DIR / 'retrieval-view.json'


SAL_MAP = {'warm': 1, 'hot': 2, 'pinned': 3}
RET_MAP = {'compact': 1, 'structured': 2}
TYPE_MAP = {
    'episodic': 'e',
    'todo': 't',
    'preference': 'p',
    'entity': 'n',
    'project-state': 's',
    'decision': 'd',
    'incident': 'i',
    'semantic': 'm',
    'procedural': 'r',
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def main() -> int:
    thin = load_json(INDEX_DIR / 'thin-index.json')
    before_bytes = (INDEX_DIR / 'thin-index.json').stat().st_size

    compressed = []
    for item in thin:
        compressed.append({
            'i': item.get('id'),
            'k': TYPE_MAP.get(item.get('type'), 'u'),
            't': (item.get('title') or '')[:48],
            's': SAL_MAP.get(item.get('salience_level'), 0),
            'r': RET_MAP.get(item.get('retention_tier'), 0),
            'p': item.get('source_path'),
        })

    OUT_PATH.write_text(json.dumps(compressed, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    after_bytes = OUT_PATH.stat().st_size
    reduction = before_bytes - after_bytes
    reduction_pct = round((reduction / before_bytes) * 100, 2) if before_bytes else 0.0

    print(json.dumps({
        'entries': len(compressed),
        'before_bytes': before_bytes,
        'after_bytes': after_bytes,
        'reduction_bytes': reduction,
        'reduction_pct': reduction_pct,
        'output': str(OUT_PATH),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
