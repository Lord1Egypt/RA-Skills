#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List

from paths import ensure_skill_dirs, get_profiles_dir

JsonDict = Dict[str, Any]


def _slot_dir(slot: str) -> Path:
    return get_profiles_dir() / slot


def _meta_path(slot: str) -> Path:
    return _slot_dir(slot) / 'meta.json'


def _auth_path(slot: str) -> Path:
    return _slot_dir(slot) / 'auth-profile.json'


def _load_json(path: Path) -> JsonDict:
    return json.loads(path.read_text(encoding='utf-8'))


def _save_json(path: Path, data: JsonDict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def create_slot(slot: str, display_name: str | None, email: str | None = None, expires_on: str | None = None, note: str | None = None, card_text: str | None = None) -> JsonDict:
    ensure_skill_dirs()
    slot_dir = _slot_dir(slot)
    slot_dir.mkdir(parents=True, exist_ok=False)
    meta = {
        'slot': slot,
        'display_name': (display_name or slot).strip() or slot,
        'provider': 'openai-codex',
        'account_id': None,
        'status': 'pending_auth',
        'disabled': False,
        'email': (email or '').strip(),
        'expires_on': (expires_on or '').strip(),
        'note': (note or '').strip(),
        'card_text': (card_text or '').rstrip(),
    }
    _save_json(_meta_path(slot), meta)
    return {'ok': True, 'slot': slot, 'account_id': None, 'meta': meta}


def list_slots() -> JsonDict:
    ensure_skill_dirs()
    rows: List[JsonDict] = []
    for slot_dir in sorted(get_profiles_dir().glob('*')):
        if not slot_dir.is_dir():
            continue
        row: JsonDict = {'slot': slot_dir.name}
        meta_path = slot_dir / 'meta.json'
        auth_path = slot_dir / 'auth-profile.json'
        if meta_path.exists():
            row.update(_load_json(meta_path))
        if auth_path.exists():
            auth = _load_json(auth_path)
            row.setdefault('account_id', auth.get('accountId'))
            row.setdefault('provider', auth.get('provider'))
        rows.append(row)
    return {'ok': True, 'slots': rows}


def show_slot(slot: str) -> JsonDict:
    slot_dir = _slot_dir(slot)
    if not slot_dir.exists():
        return {'ok': False, 'error': f'slot not found: {slot}'}
    result: JsonDict = {'ok': True, 'slot': slot}
    if _meta_path(slot).exists():
        result['meta'] = _load_json(_meta_path(slot))
    if _auth_path(slot).exists():
        auth = _load_json(_auth_path(slot))
        result['auth_summary'] = {
            'provider': auth.get('provider'),
            'type': auth.get('type'),
            'account_id': auth.get('accountId'),
            'expires': auth.get('expires'),
        }
    return result


def disable_slot(slot: str, disabled: bool) -> JsonDict:
    meta_path = _meta_path(slot)
    if not meta_path.exists():
        return {'ok': False, 'error': f'meta not found for slot: {slot}'}
    meta = _load_json(meta_path)
    meta['disabled'] = disabled
    _save_json(meta_path, meta)
    return {'ok': True, 'slot': slot, 'disabled': disabled}


def update_slot_meta(slot: str, display_name: str | None, email: str | None, expires_on: str | None, note: str | None, card_text: str | None) -> JsonDict:
    meta_path = _meta_path(slot)
    if not meta_path.exists():
        return {'ok': False, 'error': f'meta not found for slot: {slot}'}
    meta = _load_json(meta_path)
    if display_name is not None:
        meta['display_name'] = display_name.strip() or slot
    if email is not None:
        meta['email'] = email.strip()
    if expires_on is not None:
        meta['expires_on'] = expires_on.strip()
    if note is not None:
        meta['note'] = note.strip()
    if card_text is not None:
        meta['card_text'] = card_text.rstrip()
    _save_json(meta_path, meta)
    return {'ok': True, 'slot': slot, 'meta': meta}


def delete_slot(slot: str) -> JsonDict:
    slot_dir = _slot_dir(slot)
    if not slot_dir.exists():
        return {'ok': False, 'error': f'slot not found: {slot}'}
    shutil.rmtree(slot_dir)
    return {'ok': True, 'slot': slot, 'deleted': True}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd', required=True)
    p_create = sub.add_parser('create')
    p_create.add_argument('--slot', required=True)
    p_create.add_argument('--display-name')
    p_create.add_argument('--email')
    p_create.add_argument('--expires-on')
    p_create.add_argument('--note')
    p_create.add_argument('--card-text')
    sub.add_parser('list')
    p_show = sub.add_parser('show')
    p_show.add_argument('--slot', required=True)
    p_disable = sub.add_parser('disable')
    p_disable.add_argument('--slot', required=True)
    p_enable = sub.add_parser('enable')
    p_enable.add_argument('--slot', required=True)
    p_update = sub.add_parser('update')
    p_update.add_argument('--slot', required=True)
    p_update.add_argument('--display-name')
    p_update.add_argument('--email')
    p_update.add_argument('--expires-on')
    p_update.add_argument('--note')
    p_update.add_argument('--card-text')
    p_delete = sub.add_parser('delete')
    p_delete.add_argument('--slot', required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.cmd == 'create':
        result = create_slot(args.slot, args.display_name, args.email, args.expires_on, args.note, args.card_text)
    elif args.cmd == 'list':
        result = list_slots()
    elif args.cmd == 'show':
        result = show_slot(args.slot)
    elif args.cmd == 'disable':
        result = disable_slot(args.slot, True)
    elif args.cmd == 'enable':
        result = disable_slot(args.slot, False)
    elif args.cmd == 'update':
        result = update_slot_meta(args.slot, args.display_name, args.email, args.expires_on, args.note, args.card_text)
    elif args.cmd == 'delete':
        result = delete_slot(args.slot)
    else:
        result = {'ok': False, 'error': 'unknown command'}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get('ok') else 1


if __name__ == '__main__':
    sys.exit(main())
