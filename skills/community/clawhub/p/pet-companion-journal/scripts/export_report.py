#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from collections import Counter
from common import load_pet
from record_query import iter_records, in_range


def build_report(args):
    pet = load_pet(args.pet_id)
    records = []
    for rec in iter_records():
        if rec['pet_id'] != args.pet_id:
            continue
        if args.since or args.until:
            if not in_range(rec['created_at'], args.since, args.until):
                continue
        records.append(rec)
    records.sort(key=lambda x: x['created_at'])
    counts = Counter(r['type'] for r in records)
    lines = [
        f"# {pet['name']} 的陪伴记录汇总",
        '',
        f"- 宠物：{pet['name']} ({pet.get('species','未知')}{' / ' + pet.get('breed') if pet.get('breed') else ''})",
        f"- 时间范围：{args.since or '最早'} ~ {args.until or '现在'}",
        '',
        '## 记录统计',
    ]
    for k, v in sorted(counts.items()):
        lines.append(f"- {k}: {v} 条")
    lines.extend(['', '## 时间线'])
    for rec in records:
        lines.append(f"- {rec['created_at']} | {rec['type']} | {rec.get('title') or '无标题'}")
    print('\n'.join(lines))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--pet-id', required=True)
    p.add_argument('--since')
    p.add_argument('--until')
    build_report(p.parse_args())
