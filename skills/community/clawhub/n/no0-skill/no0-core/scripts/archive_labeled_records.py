#!/usr/bin/env python3
"""
Standalone archiver: moves labeled records from change_log.json to change_log_labeled.json.
"""
import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / 'change_log.json'
DST = BASE / 'change_log_labeled.json'


def is_pending(val):
    return val is None or val == '' or str(val).lower() == 'null'

def resolve_level(row):
    return row.get('level')

def load_json(path: Path):
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    records = load_json(SRC)
    if not records:
        print('no records')
        return

    pending = []
    labeled = []
    for row in records:
        if not isinstance(row, dict):
            continue
        if is_pending(resolve_level(row)):
            pending.append(row)
        else:
            row.setdefault('archived_record_time', datetime.now().astimezone().isoformat(timespec='seconds'))
            labeled.append(row)

    if labeled:
        existing = load_json(DST)
        seen = {str(x.get('event_id')) for x in existing if isinstance(x, dict)}
        for row in labeled:
            event_id = str(row.get('event_id'))
            if event_id and event_id not in seen:
                existing.append(row)
                seen.add(event_id)
        save_json(DST, existing)

    save_json(SRC, pending)
    print(f'archived={len(labeled)} pending={len(pending)}')


if __name__ == '__main__':
    main()
