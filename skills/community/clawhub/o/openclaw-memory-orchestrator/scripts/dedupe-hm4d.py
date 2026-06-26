#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import os
from collections import defaultdict

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
JSONL_PATH = ROOT / 'memory' / 'index' / 'memory-records.jsonl'


def load_records():
    items = []
    if not JSONL_PATH.exists():
        return items
    with JSONL_PATH.open('r', encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def dedupe(records):
    groups = defaultdict(list)
    for item in records:
        key = (
            item.get('source_path'),
            item.get('type'),
            item.get('title'),
            item.get('summary'),
        )
        groups[key].append(item)

    kept = []
    removed = []
    for _, group in groups.items():
        group = sorted(group, key=lambda x: x.get('timestamp', ''))
        keep = group[-1]
        kept.append(keep)
        if len(group) > 1:
            removed.extend(group[:-1])
    return kept, removed


def write_records(records):
    with JSONL_PATH.open('w', encoding='utf-8') as fh:
        for item in records:
            fh.write(json.dumps(item, ensure_ascii=False) + '\n')


def main() -> int:
    records = load_records()
    before = len(records)
    kept, removed = dedupe(records)
    write_records(kept)
    print(json.dumps({
        'before': before,
        'after': len(kept),
        'removed': len(removed),
        'removed_ids': [x.get('id') for x in removed[:20]],
        'jsonl_path': str(JSONL_PATH),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
