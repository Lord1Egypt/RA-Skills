#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import os

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
INDEX_DIR = ROOT / 'memory' / 'index'
INPUT_PATH = INDEX_DIR / 'retrieval-view.json'
OUTPUT_PATH = INDEX_DIR / 'retrieval-view-packed.json'


def main() -> int:
    items = json.loads(INPUT_PATH.read_text(encoding='utf-8'))
    pointers = {}
    next_id = 1
    packed = []

    for item in items:
        path = item.get('p')
        if path not in pointers:
            pointers[path] = next_id
            next_id += 1
        packed.append({
            'i': item.get('i'),
            'k': item.get('k'),
            't': item.get('t'),
            's': item.get('s'),
            'r': item.get('r'),
            'p': pointers[path],
        })

    payload = {
        'dict': {str(v): k for k, v in pointers.items()},
        'items': packed,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')

    before_bytes = INPUT_PATH.stat().st_size
    after_bytes = OUTPUT_PATH.stat().st_size
    reduction = before_bytes - after_bytes
    reduction_pct = round((reduction / before_bytes) * 100, 2) if before_bytes else 0.0

    print(json.dumps({
        'entries': len(packed),
        'pointer_dict_size': len(pointers),
        'before_bytes': before_bytes,
        'after_bytes': after_bytes,
        'reduction_bytes': reduction,
        'reduction_pct': reduction_pct,
        'output': str(OUTPUT_PATH),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
