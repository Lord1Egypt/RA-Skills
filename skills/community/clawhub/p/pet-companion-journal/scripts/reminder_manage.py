#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from common import load_pet, make_record_id, now_iso, read_json, storage_root, write_json


def add_reminder(args):
    load_pet(args.pet_id)
    path = storage_root() / 'reminders' / f'{args.pet_id}.json'
    data = read_json(path, {'pet_id': args.pet_id, 'reminders': []})
    reminder = {
        'reminder_id': make_record_id('rem'),
        'title': args.title,
        'reminder_type': args.reminder_type,
        'due_at': args.due_at,
        'recurrence': json.loads(args.recurrence) if args.recurrence else None,
        'status': 'active',
        'notes': args.notes,
        'created_at': now_iso(),
    }
    data['reminders'].append(reminder)
    write_json(path, data)
    print(json.dumps({'status': 'created', 'path': str(path), 'reminder': reminder}, ensure_ascii=False, indent=2))


def list_reminders(args):
    path = storage_root() / 'reminders' / f'{args.pet_id}.json'
    data = read_json(path, {'pet_id': args.pet_id, 'reminders': []})
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='command', required=True)
    a = sub.add_parser('add')
    a.add_argument('--pet-id', required=True)
    a.add_argument('--title', required=True)
    a.add_argument('--reminder-type', required=True)
    a.add_argument('--due-at', required=True)
    a.add_argument('--recurrence')
    a.add_argument('--notes')
    a.set_defaults(func=add_reminder)
    l = sub.add_parser('list')
    l.add_argument('--pet-id', required=True)
    l.set_defaults(func=list_reminders)
    args = p.parse_args()
    args.func(args)
