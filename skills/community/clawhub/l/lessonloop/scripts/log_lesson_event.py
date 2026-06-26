#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description='Append a LessonLoop event log entry')
    p.add_argument('--workspace', default='/Users/steven/.openclaw/workspace')
    p.add_argument('--date', help='YYYY-MM-DD; defaults to local date')
    p.add_argument('--lesson-type', required=True, choices=['preference', 'rule', 'mistake', 'priority'])
    p.add_argument('--storage', required=True, choices=['daily', 'candidate-long-term', 'long-term'])
    p.add_argument('--source', default='user-feedback')
    p.add_argument('--lesson', required=True)
    args = p.parse_args()

    workspace = Path(args.workspace)
    date = args.date or datetime.now().strftime('%Y-%m-%d')
    logdir = workspace / 'memory' / 'lessonloop'
    logdir.mkdir(parents=True, exist_ok=True)
    path = logdir / f'{date}.jsonl'

    entry = {
        'ts': datetime.now().isoformat(timespec='seconds'),
        'lessonType': args.lesson_type,
        'storage': args.storage,
        'source': args.source,
        'lesson': args.lesson.strip(),
    }
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    print(path)


if __name__ == '__main__':
    main()
