#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
from pathlib import Path
import os

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
INDEX_DIR = ROOT / 'memory' / 'index'
STATE_PATH = INDEX_DIR / 'phase2b-incremental-state.json'
TARGETS = [
    INDEX_DIR / 'thin-index.json',
    INDEX_DIR / 'retrieval-view.json',
    INDEX_DIR / 'retrieval-view-packed.json',
    INDEX_DIR / 'retrieval-view-hot.json',
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    current = {}
    for path in TARGETS:
        current[str(path)] = {
            'exists': path.exists(),
            'sha256': sha256(path) if path.exists() else None,
            'bytes': path.stat().st_size if path.exists() else 0,
        }

    previous = {}
    if STATE_PATH.exists():
        previous = json.loads(STATE_PATH.read_text(encoding='utf-8'))

    changed = []
    unchanged = []
    for key, value in current.items():
        if previous.get(key) != value:
            changed.append(key)
        else:
            unchanged.append(key)

    payload = {
        'changed': changed,
        'unchanged': unchanged,
        'artifacts': current,
    }
    STATE_PATH.write_text(json.dumps(current, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({
        'state': str(STATE_PATH),
        'changed_count': len(changed),
        'unchanged_count': len(unchanged),
        'changed': changed,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
