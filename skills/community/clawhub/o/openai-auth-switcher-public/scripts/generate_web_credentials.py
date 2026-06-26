#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import secrets
import string

DEFAULT_USERNAME = 'admin'
ALPHABET = string.ascii_letters + string.digits


def generate_password(length: int = 18) -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))


def build_credentials(username: str = DEFAULT_USERNAME, length: int = 18) -> dict:
    return {'ok': True, 'username': username, 'password': generate_password(length)}


def main() -> int:
    parser = argparse.ArgumentParser(description='Generate default web credentials')
    parser.add_argument('--username', default=DEFAULT_USERNAME)
    parser.add_argument('--length', type=int, default=18)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    result = build_credentials(username=args.username, length=args.length)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['username']}:{result['password']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
