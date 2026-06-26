#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path


def daterange(days):
    today = datetime.now().date()
    for i in range(days):
        yield (today - timedelta(days=i)).isoformat()


def main():
    p = argparse.ArgumentParser(description='Summarize LessonLoop activity')
    p.add_argument('--workspace', default='/Users/steven/.openclaw/workspace')
    p.add_argument('--days', type=int, default=7)
    args = p.parse_args()

    logdir = Path(args.workspace) / 'memory' / 'lessonloop'
    entries = []
    for d in daterange(args.days):
        path = logdir / f'{d}.jsonl'
        if not path.exists():
            continue
        for line in path.read_text(encoding='utf-8').splitlines():
            line=line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except Exception:
                pass

    lesson_types = Counter(e.get('lessonType', 'unknown') for e in entries)
    storage = Counter(e.get('storage', 'unknown') for e in entries)
    sources = Counter(e.get('source', 'unknown') for e in entries)

    print('LessonLoop Report')
    print(f'days: {args.days}')
    print(f'totalEvents: {len(entries)}')
    print('lessonTypes: ' + ', '.join(f'{k}={v}' for k,v in sorted(lesson_types.items())) if lesson_types else 'lessonTypes: none')
    print('storage: ' + ', '.join(f'{k}={v}' for k,v in sorted(storage.items())) if storage else 'storage: none')
    print('sources: ' + ', '.join(f'{k}={v}' for k,v in sorted(sources.items())) if sources else 'sources: none')
    if entries:
        print('latest: ' + entries[-1].get('lesson', '')[:120])
    else:
        print('latest: none')


if __name__ == '__main__':
    main()
