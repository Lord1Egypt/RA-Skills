#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import os
import importlib.util

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
JSONL_PATH = ROOT / 'memory' / 'index' / 'memory-records.jsonl'
RETENTION_ENGINE = ROOT / 'scripts' / 'retention-policy.py'


def load_engine():
    spec = importlib.util.spec_from_file_location('retention_policy', RETENTION_ENGINE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'failed to load retention engine: {RETENTION_ENGINE}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_engine()
    if not JSONL_PATH.exists():
        raise SystemExit('missing memory-records.jsonl')

    lines = JSONL_PATH.read_text(encoding='utf-8').splitlines()
    updated = []
    changed = 0
    for line in lines:
        if not line.strip():
            continue
        item = json.loads(line)
        result = module.evaluate({
            'type': item.get('type', 'episodic'),
            'importance': float(item.get('importance', 0.65)),
            'source_path': item.get('source_path', ''),
            'summary': item.get('summary', ''),
            'delta_from': item.get('delta_from'),
        })
        before = (
            item.get('salience_level'),
            item.get('retention_tier'),
            item.get('delta_from'),
        )
        item['salience_level'] = result.get('salience_level')
        item['retention_tier'] = result.get('retention_tier')
        if result.get('delta_from') is not None:
            item['delta_from'] = result.get('delta_from')
        after = (
            item.get('salience_level'),
            item.get('retention_tier'),
            item.get('delta_from'),
        )
        if before != after:
            changed += 1
        updated.append(item)

    with JSONL_PATH.open('w', encoding='utf-8') as fh:
        for item in updated:
            fh.write(json.dumps(item, ensure_ascii=False) + '\n')

    print(json.dumps({
        'records': len(updated),
        'changed': changed,
        'jsonl_path': str(JSONL_PATH),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
