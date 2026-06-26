#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys

REQUIRED = [
    'SKILL.md', 'README.md', 'CHANGELOG.md',
    'references/pathways-overview.md',
    'references/triggers-and-routing.md',
    'references/scoring-rubrics.md',
    'resources/official-links.csv',
    'scripts/score_engine.py',
]


def check_json(path: pathlib.Path):
    with path.open('r', encoding='utf-8') as f:
        json.load(f)


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    missing = [p for p in REQUIRED if not (root / p).exists()]
    if missing:
        print('MISSING FILES:')
        for p in missing:
            print('-', p)
        return 1
    for path in (root / 'resources' / 'scorecards').glob('*.json'):
        check_json(path)
    print('SELF CHECK OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
