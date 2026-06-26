#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from common import now_iso, load_pet, make_record_id, write_record


def add_record(args):
    load_pet(args.pet_id)
    created_at = args.created_at or now_iso()
    frontmatter = {
        'record_id': make_record_id('rec'),
        'pet_id': args.pet_id,
        'type': args.type,
        'title': args.title or '',
        'created_at': created_at,
        'tags': args.tags or [],
        'media': args.media or [],
        'extra': json.loads(args.extra) if args.extra else {},
    }
    path = write_record(frontmatter, args.body or '')
    print(json.dumps({'status': 'created', 'path': str(path), 'record': frontmatter}, ensure_ascii=False, indent=2))


def build_parser():
    p = argparse.ArgumentParser()
    p.add_argument('--pet-id', required=True)
    p.add_argument('--type', required=True, choices=['daily', 'moment', 'photo', 'feeding', 'health', 'reminder-note'])
    p.add_argument('--title')
    p.add_argument('--body')
    p.add_argument('--created-at')
    p.add_argument('--tags', nargs='*')
    p.add_argument('--media', nargs='*')
    p.add_argument('--extra', help='JSON string for structured fields')
    return p


if __name__ == '__main__':
    args = build_parser().parse_args()
    add_record(args)
