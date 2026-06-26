#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from datetime import datetime, timedelta, timezone
from common import read_json, storage_root

TZ = timezone(timedelta(hours=8))


def load_reminders(pet_id=None):
    root = storage_root() / 'reminders'
    files = [root / f'{pet_id}.json'] if pet_id else sorted(root.glob('*.json'))
    rows = []
    for f in files:
        data = read_json(f, {'reminders': []})
        rows.extend(data.get('reminders', []))
    return rows


def main(args):
    now = datetime.now(TZ)
    horizon = now + timedelta(days=args.days)
    due, upcoming = [], []
    for r in load_reminders(args.pet_id):
        if r.get('status') != 'active':
            continue
        due_at = datetime.fromisoformat(r['due_at'])
        if due_at <= now:
            due.append(r)
        elif due_at <= horizon:
            upcoming.append(r)
    print(json.dumps({'due': due, 'upcoming': upcoming}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--pet-id')
    p.add_argument('--days', type=int, default=7)
    main(p.parse_args())
