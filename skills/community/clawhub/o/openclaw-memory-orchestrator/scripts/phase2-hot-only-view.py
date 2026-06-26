#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import os

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
INDEX_DIR = ROOT / 'memory' / 'index'
INPUT_PATH = INDEX_DIR / 'retrieval-view-packed.json'
OUTPUT_PATH = INDEX_DIR / 'retrieval-view-hot.json'


def main() -> int:
    payload = json.loads(INPUT_PATH.read_text(encoding='utf-8'))
    items = payload.get('items', [])
    hot_only = [item for item in items if item.get('s', 0) >= 2]
    out = {
        'dict': payload.get('dict', {}),
        'items': hot_only,
    }
    OUTPUT_PATH.write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')

    before_bytes = INPUT_PATH.stat().st_size
    after_bytes = OUTPUT_PATH.stat().st_size
    reduction = before_bytes - after_bytes
    reduction_pct = round((reduction / before_bytes) * 100, 2) if before_bytes else 0.0

    print(json.dumps({
        'before_entries': len(items),
        'after_entries': len(hot_only),
        'before_bytes': before_bytes,
        'after_bytes': after_bytes,
        'reduction_bytes': reduction,
        'reduction_pct': reduction_pct,
        'output': str(OUTPUT_PATH),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
