#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime

ROOT = os.environ.get('MEMORY_ROOT', os.path.join(os.getcwd(), 'memory'))
OBJECTS_DIR = os.path.join(ROOT, 'objects')
TYPE_DIR_MAP = {
    'paper': 'papers',
    'concept': 'concepts',
    'framework': 'frameworks',
    'decision': 'decisions',
    'preference': 'preferences',
    'open-question': 'open-questions',
    'note': 'notes',
    'person': 'people',
    'project': 'projects',
}


def dump_yaml(data):
    lines = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f'{key}:')
            for item in value:
                lines.append(f'  - {item}')
        elif isinstance(value, dict):
            lines.append(f'{key}:')
            if not value:
                lines[-1] += ' {}'
            else:
                for k, v in value.items():
                    if isinstance(v, list):
                        lines.append(f'  {k}:')
                        for item in v:
                            lines.append(f'    - {item}')
                    else:
                        lines.append(f'  {k}: {v}')
        else:
            encoded = json.dumps(value, ensure_ascii=False) if isinstance(value, str) else value
            lines.append(f'{key}: {encoded}')
    return '\n'.join(lines) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--type', required=True, choices=sorted(TYPE_DIR_MAP.keys()))
    ap.add_argument('--domain', required=True)
    ap.add_argument('--slug', required=True)
    ap.add_argument('--title', required=True)
    ap.add_argument('--summary', default='TODO: add summary')
    args = ap.parse_args()

    target_dir = os.path.join(OBJECTS_DIR, TYPE_DIR_MAP[args.type])
    os.makedirs(target_dir, exist_ok=True)
    path = os.path.join(target_dir, f'{args.slug}.yaml')
    if os.path.exists(path):
        raise SystemExit(f'Object already exists: {path}')

    blob = {
        'id': f'{args.type}/{args.slug}',
        'type': args.type,
        'domain': args.domain,
        'title': args.title,
        'summary': args.summary,
        'why_it_matters': 'TODO: explain why this object should be recalled later',
        'tags': [],
        'status': 'draft',
        'confidence': 'medium',
        'last_discussed': datetime.now().date().isoformat(),
        'relations': {},
        'user_takeaways': [],
        'created_at': datetime.now().astimezone().isoformat(timespec='seconds'),
        'updated_at': datetime.now().astimezone().isoformat(timespec='seconds'),
    }
    with open(path, 'w', encoding='utf-8') as f:
        f.write(dump_yaml(blob))
    print(json.dumps({'ok': True, 'path': path}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
