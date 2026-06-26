#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from datetime import datetime
from pathlib import Path
from common import parse_record, storage_root


def iter_records():
    root = storage_root() / 'records'
    for path in root.rglob('*.md'):
        yield parse_record(path)


def in_range(value, since, until):
    dt = datetime.fromisoformat(value)
    if since and dt < datetime.fromisoformat(since):
        return False
    if until and dt > datetime.fromisoformat(until):
        return False
    return True


def query(args):
    results = []
    for rec in iter_records():
        if args.pet_id and rec['pet_id'] != args.pet_id:
            continue
        if args.type and rec['type'] != args.type:
            continue
        if args.since or args.until:
            if not in_range(rec['created_at'], args.since, args.until):
                continue
        if args.keyword:
            hay = ' '.join([rec.get('title',''), rec.get('body',''), ' '.join(rec.get('tags', []))])
            if args.keyword not in hay:
                continue
        results.append(rec)
    results.sort(key=lambda x: x['created_at'], reverse=True)
    if args.limit:
        results = results[:args.limit]
    print(json.dumps({'count': len(results), 'records': results}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--pet-id')
    p.add_argument('--type')
    p.add_argument('--since')
    p.add_argument('--until')
    p.add_argument('--keyword')
    p.add_argument('--limit', type=int)
    query(p.parse_args())
