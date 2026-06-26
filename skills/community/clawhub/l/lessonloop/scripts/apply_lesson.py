#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path


def append_daily_memory(workspace: Path, date: str, lesson: str):
    memdir = workspace / 'memory'
    memdir.mkdir(parents=True, exist_ok=True)
    path = memdir / f'{date}.md'
    header = f'# {date}\n\n'
    line = f'- {lesson.strip()}\n'

    if path.exists():
        text = path.read_text(encoding='utf-8')
        if not text.endswith('\n'):
            text += '\n'
        if line not in text:
            path.write_text(text + line, encoding='utf-8')
            return True, path
        return False, path

    path.write_text(header + line, encoding='utf-8')
    return True, path


def append_event_log(workspace: Path, date: str, lesson_type: str, storage: str, source: str, lesson: str):
    logdir = workspace / 'memory' / 'lessonloop'
    logdir.mkdir(parents=True, exist_ok=True)
    path = logdir / f'{date}.jsonl'
    entry = {
        'ts': datetime.now().isoformat(timespec='seconds'),
        'lessonType': lesson_type,
        'storage': storage,
        'source': source,
        'lesson': lesson.strip(),
    }
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    return path


def main():
    p = argparse.ArgumentParser(description='Apply a LessonLoop lesson to daily memory and structured logs')
    p.add_argument('--workspace', default='/Users/steven/.openclaw/workspace')
    p.add_argument('--date', help='YYYY-MM-DD; defaults to local date')
    p.add_argument('--lesson-type', required=True, choices=['preference', 'rule', 'mistake', 'priority'])
    p.add_argument('--storage', required=True, choices=['daily', 'candidate-long-term', 'long-term'])
    p.add_argument('--source', default='user-feedback')
    p.add_argument('--lesson', required=True)
    args = p.parse_args()

    workspace = Path(args.workspace)
    date = args.date or datetime.now().strftime('%Y-%m-%d')
    wrote_memory, memory_path = append_daily_memory(workspace, date, args.lesson)
    log_path = append_event_log(workspace, date, args.lesson_type, args.storage, args.source, args.lesson)

    print(json.dumps({
        'memoryPath': str(memory_path),
        'wroteMemory': wrote_memory,
        'logPath': str(log_path),
        'lessonType': args.lesson_type,
        'storage': args.storage,
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
