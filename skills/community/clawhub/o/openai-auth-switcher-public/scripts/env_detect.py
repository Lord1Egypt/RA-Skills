#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from paths import detect_runtime


def main() -> int:
    parser = argparse.ArgumentParser(description='Detect OpenClaw runtime paths for the public auth-switcher skill.')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    data = detect_runtime()
    data['ok'] = bool(data.get('openclaw_root') and data.get('workspace') and data.get('agent_root'))

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0 if data['ok'] else 1

    print('OpenClaw runtime detection')
    for key, value in data.items():
        print(f'- {key}: {value}')
    return 0 if data['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
