#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

ROOT = Path(os.environ.get('MEMORY_ROOT', Path.cwd() / 'memory'))
TOPICS_DIR = ROOT / 'topics'


def dump_yaml(data):
    lines = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f'{key}:')
            for item in value:
                lines.append(f'  - {item}')
        else:
            lines.append(f'{key}: {json.dumps(value, ensure_ascii=False) if isinstance(value, str) else value}')
    return '\n'.join(lines) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--slug', required=True)
    ap.add_argument('--title', required=True)
    ap.add_argument('--summary', required=True)
    args = ap.parse_args()

    TOPICS_DIR.mkdir(parents=True, exist_ok=True)
    path = TOPICS_DIR / f'{args.slug}.yaml'
    if path.exists():
        raise SystemExit(f'Topic already exists: {path}')

    blob = {
        'id': args.slug,
        'name': args.title,
        'summary': args.summary,
        'subtopics': [],
        'recent_objects': [],
        'linked_topics': [],
        'stable_preferences': [],
        'priority_rules': [],
    }
    path.write_text(dump_yaml(blob), encoding='utf-8')
    print(json.dumps({'ok': True, 'path': str(path)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
