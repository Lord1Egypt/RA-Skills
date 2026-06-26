#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path
import os
from typing import Dict, List, Any

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
JSONL_PATH = ROOT / 'memory' / 'index' / 'memory-records.jsonl'
OUTPUT_PATH = ROOT / 'memory' / 'index' / 'delta-summaries.json'


def load_records() -> List[Dict[str, Any]]:
    if not JSONL_PATH.exists():
        return []
    items: List[Dict[str, Any]] = []
    with JSONL_PATH.open('r', encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def normalize_summary(text: str) -> List[str]:
    return [line.strip() for line in (text or '').splitlines() if line.strip()]


def build_deltas(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for item in records:
        key = item.get('source_path') or item.get('id')
        grouped.setdefault(key, []).append(item)

    deltas: List[Dict[str, Any]] = []
    for source_path, group in grouped.items():
        if len(group) < 2:
            continue
        group = sorted(group, key=lambda x: x.get('timestamp', ''))
        base = group[0]
        base_lines = normalize_summary(base.get('summary', ''))
        for current in group[1:]:
            current_lines = normalize_summary(current.get('summary', ''))
            diff = list(difflib.unified_diff(base_lines, current_lines, lineterm=''))
            if not diff:
                continue
            delta_lines = [line for line in diff if line.startswith('+ ') or line.startswith('- ')]
            deltas.append({
                'source_path': source_path,
                'base_id': base.get('id'),
                'current_id': current.get('id'),
                'delta_from': current.get('delta_from') or base.get('id'),
                'change_count': len(diff),
                'delta_preview': diff[:20],
            })
    return {
        'generated_from': str(JSONL_PATH),
        'delta_count': len(deltas),
        'deltas': deltas,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Build HM4D delta summaries')
    parser.add_argument('--output', default=str(OUTPUT_PATH))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    records = load_records()
    payload = build_deltas(records)
    output = Path(args.output)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({
        'records': len(records),
        'delta_count': payload['delta_count'],
        'output': str(output),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
