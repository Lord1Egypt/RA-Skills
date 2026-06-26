#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
FNS = BASE / 'fns.py'


def run_fns(args):
    cmd = ['python3', str(FNS)] + args
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr or p.stdout)
        raise SystemExit(p.returncode)
    return p.stdout


def parse_json_output(text):
    return json.loads(text)


def cmd_read(args):
    out = run_fns(['get', '--path', args.path, '--content-only'])
    data = {
        'ok': True,
        'action': 'read_note',
        'path': args.path,
        'content': out,
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_search(args):
    cmd = ['search', '--keyword', args.keyword, '--page-size', str(args.page_size)]
    if args.search_content:
        cmd.append('--search-content')
        cmd += ['--search-mode', 'content']
    out = run_fns(cmd)
    raw = parse_json_output(out)
    payload = raw.get('data', {}) if isinstance(raw, dict) else {}
    items = payload.get('list', []) if isinstance(payload, dict) else []
    simplified = [
        {
            'path': item.get('path'),
            'updatedAt': item.get('updatedAt'),
            'size': item.get('size'),
        }
        for item in items
    ]
    print(json.dumps({
        'ok': True,
        'action': 'search_notes',
        'keyword': args.keyword,
        'count': len(simplified),
        'results': simplified,
    }, ensure_ascii=False, indent=2))


def cmd_write(args):
    out = run_fns(['put', '--path', args.path, '--content', args.content])
    raw = parse_json_output(out)
    note = raw.get('data', {}) if isinstance(raw, dict) else {}
    print(json.dumps({
        'ok': True,
        'action': 'write_note',
        'path': note.get('path', args.path),
        'version': note.get('version'),
        'updatedAt': note.get('updatedAt'),
    }, ensure_ascii=False, indent=2))


def cmd_append(args):
    out = run_fns(['append', '--path', args.path, '--content', args.content])
    raw = parse_json_output(out)
    note = raw.get('data', {}) if isinstance(raw, dict) else {}
    print(json.dumps({
        'ok': True,
        'action': 'append_note',
        'path': note.get('path', args.path),
        'version': note.get('version'),
        'updatedAt': note.get('updatedAt'),
    }, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(description='High-level actions for ObsidianFNS')
    sub = p.add_subparsers(dest='command', required=True)

    read = sub.add_parser('read-note')
    read.add_argument('--path', required=True)
    read.set_defaults(func=cmd_read)

    search = sub.add_parser('search-notes')
    search.add_argument('--keyword', required=True)
    search.add_argument('--page-size', type=int, default=10)
    search.add_argument('--search-content', action='store_true')
    search.set_defaults(func=cmd_search)

    write = sub.add_parser('write-note')
    write.add_argument('--path', required=True)
    write.add_argument('--content', required=True)
    write.set_defaults(func=cmd_write)

    append = sub.add_parser('append-note')
    append.add_argument('--path', required=True)
    append.add_argument('--content', required=True)
    append.set_defaults(func=cmd_append)

    args = p.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
