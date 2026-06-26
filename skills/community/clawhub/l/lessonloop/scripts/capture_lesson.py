#!/usr/bin/env python3
import argparse
from datetime import datetime
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description='Append a compact lesson to daily memory')
    p.add_argument('--workspace', default='/Users/steven/.openclaw/workspace')
    p.add_argument('--date', help='YYYY-MM-DD; defaults to local date')
    p.add_argument('--lesson', required=True)
    args = p.parse_args()

    workspace = Path(args.workspace)
    date = args.date or datetime.now().strftime('%Y-%m-%d')
    memdir = workspace / 'memory'
    memdir.mkdir(parents=True, exist_ok=True)
    path = memdir / f'{date}.md'

    header = f'# {date}\n\n'
    line = f'- {args.lesson.strip()}\n'

    if path.exists():
        text = path.read_text(encoding='utf-8')
        if not text.endswith('\n'):
            text += '\n'
        if line not in text:
            path.write_text(text + line, encoding='utf-8')
    else:
        path.write_text(header + line, encoding='utf-8')

    print(path)


if __name__ == '__main__':
    main()
