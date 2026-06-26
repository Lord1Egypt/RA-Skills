#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
from common import now_iso, read_json, slugify, storage_root, write_json, list_pets


def create_pet(args):
    pet_id = args.pet_id or slugify(args.name)
    path = storage_root() / 'pets' / f'{pet_id}.json'
    if path.exists():
        raise SystemExit(f'Pet already exists: {pet_id}')
    data = {
        'pet_id': pet_id,
        'name': args.name,
        'nickname': args.nickname or [],
        'species': args.species,
        'breed': args.breed,
        'gender': args.gender,
        'birthday': args.birthday,
        'adoption_date': args.adoption_date,
        'neutered': args.neutered,
        'color_markings': args.color_markings,
        'personality_tags': args.personality_tags or [],
        'notes': args.notes,
        'avatar_media': args.avatar_media,
        'created_at': now_iso(),
        'updated_at': now_iso(),
    }
    write_json(path, data)
    print(json.dumps({'status': 'created', 'pet_id': pet_id, 'path': str(path), 'pet': data}, ensure_ascii=False, indent=2))


def update_pet(args):
    path = storage_root() / 'pets' / f'{args.pet_id}.json'
    data = read_json(path)
    if not data:
        raise SystemExit(f'Pet not found: {args.pet_id}')
    for field in ['name', 'species', 'breed', 'gender', 'birthday', 'adoption_date', 'color_markings', 'notes', 'avatar_media']:
        value = getattr(args, field)
        if value is not None:
            data[field] = value
    if args.nickname is not None:
        data['nickname'] = args.nickname
    if args.personality_tags is not None:
        data['personality_tags'] = args.personality_tags
    if args.neutered is not None:
        data['neutered'] = args.neutered
    data['updated_at'] = now_iso()
    write_json(path, data)
    print(json.dumps({'status': 'updated', 'pet_id': args.pet_id, 'path': str(path), 'pet': data}, ensure_ascii=False, indent=2))


def view_pet(args):
    path = storage_root() / 'pets' / f'{args.pet_id}.json'
    data = read_json(path)
    if not data:
        raise SystemExit(f'Pet not found: {args.pet_id}')
    print(json.dumps(data, ensure_ascii=False, indent=2))


def list_all(_args):
    print(json.dumps({'pets': list_pets()}, ensure_ascii=False, indent=2))


def build_parser():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='command', required=True)

    def add_common(sp):
        sp.add_argument('--name')
        sp.add_argument('--species')
        sp.add_argument('--breed')
        sp.add_argument('--gender')
        sp.add_argument('--birthday')
        sp.add_argument('--adoption-date')
        sp.add_argument('--color-markings')
        sp.add_argument('--notes')
        sp.add_argument('--avatar-media')
        sp.add_argument('--nickname', action='append')
        sp.add_argument('--personality-tags', nargs='*')

    c = sub.add_parser('create')
    c.add_argument('--pet-id')
    c.add_argument('--name', required=True)
    c.add_argument('--species', required=True)
    c.add_argument('--breed')
    c.add_argument('--gender')
    c.add_argument('--birthday')
    c.add_argument('--adoption-date')
    c.add_argument('--color-markings')
    c.add_argument('--notes')
    c.add_argument('--avatar-media')
    c.add_argument('--nickname', action='append')
    c.add_argument('--personality-tags', nargs='*')
    c.add_argument('--neutered', action='store_true')
    c.set_defaults(func=create_pet)

    u = sub.add_parser('update')
    u.add_argument('--pet-id', required=True)
    add_common(u)
    u.add_argument('--neutered', type=lambda x: x.lower() == 'true')
    u.set_defaults(func=update_pet)

    v = sub.add_parser('view')
    v.add_argument('--pet-id', required=True)
    v.set_defaults(func=view_pet)

    l = sub.add_parser('list')
    l.set_defaults(func=list_all)
    return p


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
