#!/usr/bin/env python3
"""Small durable ledger for /deepresearch runs.

This script intentionally stays dependency-free so it can run inside OpenClaw jobs,
crons, or OMOC loops without bringing down the gateway.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path('.deepresearch')


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def slugify(text: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:64]
    if slug:
        return slug
    return hashlib.sha1(text.encode()).hexdigest()[:12]


def run_dir(slug: str | None) -> Path:
    if slug:
        return ROOT / slug
    current = ROOT / 'current'
    if current.exists():
        target = current.read_text().strip()
        if target:
            return ROOT / target
    raise SystemExit('No slug supplied and .deepresearch/current is missing. Run init first.')


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    tmp.replace(path)


def emit(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def ledger(path: Path) -> dict[str, Any]:
    return read_json(path / 'ledger.json', {
        'schema': 'deepresearch.ledger.v1',
        'question': None,
        'slug': path.name,
        'status': 'active',
        'created_at': now(),
        'updated_at': now(),
        'lanes': [],
        'sources': [],
        'claims': [],
        'notes': [],
    })


def save(path: Path, data: dict[str, Any]) -> None:
    data['updated_at'] = now()
    write_json(path / 'ledger.json', data)


def next_id(items: list[dict[str, Any]], prefix: str) -> str:
    nums = []
    for item in items:
        item_id = str(item.get('id', ''))
        if item_id.startswith(prefix):
            try:
                nums.append(int(item_id[len(prefix):]))
            except ValueError:
                pass
    return f'{prefix}{max(nums, default=0) + 1:03d}'


def cmd_init(args: argparse.Namespace) -> None:
    slug = args.slug or slugify(args.question)
    path = ROOT / slug
    data = ledger(path)
    data['question'] = args.question
    data['slug'] = slug
    if not data['lanes']:
        data['lanes'] = [
            {'id': 'L001', 'name': 'background', 'question': 'What is the necessary context?', 'status': 'open'},
            {'id': 'L002', 'name': 'evidence', 'question': 'What is the strongest evidence?', 'status': 'open'},
            {'id': 'L003', 'name': 'counterevidence', 'question': 'What contradicts or weakens the claim?', 'status': 'open'},
            {'id': 'L004', 'name': 'synthesis', 'question': 'What conclusion follows from the evidence?', 'status': 'open'},
        ]
    save(path, data)
    ROOT.mkdir(exist_ok=True)
    (ROOT / 'current').write_text(slug + '\n')
    emit({'ok': True, 'slug': slug, 'path': str(path), 'ledger': data})


def cmd_lane_add(args: argparse.Namespace) -> None:
    path = run_dir(args.slug)
    data = ledger(path)
    lane = {'id': next_id(data['lanes'], 'L'), 'name': args.name, 'question': args.question, 'status': args.status}
    data['lanes'].append(lane)
    save(path, data)
    emit({'ok': True, 'lane': lane})


def cmd_source_add(args: argparse.Namespace) -> None:
    path = run_dir(args.slug)
    data = ledger(path)
    source = {
        'id': next_id(data['sources'], 'S'),
        'title': args.title,
        'url': args.url,
        'kind': args.kind,
        'reliability': args.reliability,
        'lane': args.lane,
        'added_at': now(),
    }
    data['sources'].append(source)
    save(path, data)
    emit({'ok': True, 'source': source})


def cmd_claim_add(args: argparse.Namespace) -> None:
    path = run_dir(args.slug)
    data = ledger(path)
    claim = {
        'id': next_id(data['claims'], 'C'),
        'text': args.text,
        'sources': args.source or [],
        'status': args.status,
        'confidence': args.confidence,
        'lane': args.lane,
        'added_at': now(),
    }
    data['claims'].append(claim)
    save(path, data)
    emit({'ok': True, 'claim': claim})


def cmd_note_add(args: argparse.Namespace) -> None:
    path = run_dir(args.slug)
    data = ledger(path)
    note = {'id': next_id(data['notes'], 'N'), 'text': args.text, 'lane': args.lane, 'added_at': now()}
    data['notes'].append(note)
    save(path, data)
    emit({'ok': True, 'note': note})


def cmd_brief(args: argparse.Namespace) -> None:
    path = run_dir(args.slug)
    data = ledger(path)
    claims = data.get('claims', [])
    by_status: dict[str, int] = {}
    for claim in claims:
        by_status[claim.get('status', 'unknown')] = by_status.get(claim.get('status', 'unknown'), 0) + 1
    open_lanes = [lane for lane in data.get('lanes', []) if lane.get('status') != 'done']
    weak = [claim for claim in claims if claim.get('status') in {'weak', 'conflicting', 'unverified'}]
    emit({
        'ok': True,
        'slug': data.get('slug'),
        'path': str(path),
        'question': data.get('question'),
        'counts': {
            'lanes': len(data.get('lanes', [])),
            'open_lanes': len(open_lanes),
            'sources': len(data.get('sources', [])),
            'claims': len(claims),
            'notes': len(data.get('notes', [])),
        },
        'claims_by_status': by_status,
        'open_lanes': open_lanes,
        'claims_needing_work': weak[:10],
    })


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='deepresearch.py')
    sub = p.add_subparsers(required=True)

    init = sub.add_parser('init')
    init.add_argument('--question', required=True)
    init.add_argument('--slug')
    init.set_defaults(func=cmd_init)

    lane = sub.add_parser('lane')
    lane_sub = lane.add_subparsers(required=True)
    lane_add = lane_sub.add_parser('add')
    lane_add.add_argument('--slug')
    lane_add.add_argument('--name', required=True)
    lane_add.add_argument('--question', required=True)
    lane_add.add_argument('--status', default='open', choices=['open', 'active', 'done', 'blocked'])
    lane_add.set_defaults(func=cmd_lane_add)

    source = sub.add_parser('source')
    source_sub = source.add_subparsers(required=True)
    source_add = source_sub.add_parser('add')
    source_add.add_argument('--slug')
    source_add.add_argument('--title', required=True)
    source_add.add_argument('--url', required=True)
    source_add.add_argument('--kind', default='web', choices=['web', 'paper', 'dataset', 'docs', 'book', 'news', 'local'])
    source_add.add_argument('--reliability', default='medium', choices=['high', 'medium', 'low', 'unknown'])
    source_add.add_argument('--lane')
    source_add.set_defaults(func=cmd_source_add)

    claim = sub.add_parser('claim')
    claim_sub = claim.add_subparsers(required=True)
    claim_add = claim_sub.add_parser('add')
    claim_add.add_argument('--slug')
    claim_add.add_argument('--text', required=True)
    claim_add.add_argument('--source', action='append')
    claim_add.add_argument('--status', default='unverified', choices=['supported', 'weak', 'conflicting', 'unverified'])
    claim_add.add_argument('--confidence', default='medium', choices=['high', 'medium', 'low'])
    claim_add.add_argument('--lane')
    claim_add.set_defaults(func=cmd_claim_add)

    note = sub.add_parser('note')
    note_sub = note.add_subparsers(required=True)
    note_add = note_sub.add_parser('add')
    note_add.add_argument('--slug')
    note_add.add_argument('--text', required=True)
    note_add.add_argument('--lane')
    note_add.set_defaults(func=cmd_note_add)

    brief = sub.add_parser('brief')
    brief.add_argument('--slug')
    brief.set_defaults(func=cmd_brief)

    return p


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
