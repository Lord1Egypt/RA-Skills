#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from auth_file_lib import load_json_file
from paths import detect_runtime


def import_auth_file(source: str) -> dict:
    runtime = detect_runtime()
    target_path = runtime.get('auth_profiles_path')
    if not target_path:
        return {'ok': False, 'error': 'auth_profiles_path not discovered'}
    src = Path(source).expanduser().resolve()
    if not src.exists():
        return {'ok': False, 'error': f'source not found: {src}'}
    try:
        data = load_json_file(src)
    except Exception as e:
        return {'ok': False, 'error': str(e)}
    if not isinstance(data.get('profiles'), dict):
        return {'ok': False, 'error': 'invalid auth file: missing profiles object'}
    dst = Path(target_path)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {'ok': True, 'source': str(src), 'target': str(dst)}


def main() -> int:
    parser = argparse.ArgumentParser(description='Import an existing auth-profiles.json into the detected OpenClaw runtime')
    parser.add_argument('--source', required=True)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    result = import_auth_file(args.source)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result)
    return 0 if result.get('ok') else 1


if __name__ == '__main__':
    raise SystemExit(main())
