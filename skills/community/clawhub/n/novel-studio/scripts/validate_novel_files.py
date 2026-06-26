#!/usr/bin/env python3
from pathlib import Path
import sys

REQUIRED_FILES = [
    '00_选题报告.md',
    '01_想法.md',
    '02_大纲.md',
]
REQUIRED_DIRS = ['characters', 'manuscript']
OPTIONAL_FILES = ['03_人物小传.md', '04_章节骨架.md']


def main():
    if len(sys.argv) < 2:
        print('Usage: validate_novel_files.py <项目目录>')
        sys.exit(1)

    root = Path(sys.argv[1]).expanduser()
    errors = []
    warnings = []

    if not root.exists():
        print(f'ERROR: project path not found: {root}')
        sys.exit(2)

    for f in REQUIRED_FILES:
        if not (root / f).exists():
            errors.append(f'Missing required file: {f}')

    for d in REQUIRED_DIRS:
        if not (root / d).is_dir():
            errors.append(f'Missing required directory: {d}/')

    for f in OPTIONAL_FILES:
        if not (root / f).exists():
            warnings.append(f'Missing optional file: {f}')

    char_count = len(list((root / 'characters').glob('*.md'))) if (root / 'characters').exists() else 0
    manu_count = len(list((root / 'manuscript').glob('*.md'))) if (root / 'manuscript').exists() else 0

    if char_count == 0:
        warnings.append('No character files found in characters/')
    if manu_count == 0:
        warnings.append('No manuscript files found in manuscript/')

    print(f'Project: {root}')
    print(f'Character files: {char_count}')
    print(f'Manuscript files: {manu_count}')

    if errors:
        print('\nErrors:')
        for e in errors:
            print(f'- {e}')
    if warnings:
        print('\nWarnings:')
        for w in warnings:
            print(f'- {w}')

    if errors:
        sys.exit(2)
    sys.exit(0)


if __name__ == '__main__':
    main()
