#!/usr/bin/env python3
import argparse
import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path

STORE_DIR = Path.home() / '.openclaw' / 'skills' / 'ifind'
STORE_PATH = STORE_DIR / 'credentials.json'


def _ensure_dir() -> None:
    STORE_DIR.mkdir(parents=True, exist_ok=True)


def _chmod_owner_only(path: Path) -> None:
    try:
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


def status() -> int:
    env_token = os.environ.get('IFIND_REFRESH_TOKEN')
    if env_token:
        print(json.dumps({
            'status': 'ok',
            'source': 'environment',
            'path': None,
            'message': 'refresh_token is available via IFIND_REFRESH_TOKEN'
        }, ensure_ascii=False))
        return 0

    if STORE_PATH.exists():
        print(json.dumps({
            'status': 'ok',
            'source': 'file',
            'path': str(STORE_PATH),
            'message': 'refresh_token is stored locally'
        }, ensure_ascii=False))
        return 0

    print(json.dumps({
        'status': 'missing',
        'source': None,
        'path': str(STORE_PATH),
        'message': 'refresh_token is not configured'
    }, ensure_ascii=False))
    return 1


def set_token(token: str) -> int:
    token = token.strip()
    if not token:
        raise SystemExit('token is empty')
    _ensure_dir()
    payload = {
        'refresh_token': token,
        'updated_at': datetime.now(timezone.utc).isoformat()
    }
    STORE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    _chmod_owner_only(STORE_PATH)
    print(json.dumps({
        'status': 'ok',
        'path': str(STORE_PATH),
        'message': 'refresh_token stored'
    }, ensure_ascii=False))
    return 0


def remove_token() -> int:
    if STORE_PATH.exists():
        STORE_PATH.unlink()
    print(json.dumps({
        'status': 'ok',
        'path': str(STORE_PATH),
        'message': 'refresh_token removed'
    }, ensure_ascii=False))
    return 0


def load_refresh_token() -> str:
    env_token = os.environ.get('IFIND_REFRESH_TOKEN')
    if env_token:
        return env_token.strip()
    if not STORE_PATH.exists():
        raise RuntimeError(f'missing refresh_token, expected at {STORE_PATH}')
    data = json.loads(STORE_PATH.read_text(encoding='utf-8'))
    token = (data.get('refresh_token') or '').strip()
    if not token:
        raise RuntimeError(f'empty refresh_token in {STORE_PATH}')
    return token


def main() -> int:
    parser = argparse.ArgumentParser(description='Manage iFinD refresh_token storage')
    sub = parser.add_subparsers(dest='command', required=True)

    sub.add_parser('status')
    p_set = sub.add_parser('set')
    p_set.add_argument('--token', required=True)
    sub.add_parser('remove')

    args = parser.parse_args()
    if args.command == 'status':
        return status()
    if args.command == 'set':
        return set_token(args.token)
    if args.command == 'remove':
        return remove_token()
    raise SystemExit(2)


if __name__ == '__main__':
    raise SystemExit(main())
