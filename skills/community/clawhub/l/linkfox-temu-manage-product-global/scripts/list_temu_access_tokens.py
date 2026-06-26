#!/usr/bin/env python3
"""
List locally saved Temu accessTokens (masked).

Usage:
  python list_temu_access_tokens.py
  python list_temu_access_tokens.py '{"mask": false}'
"""

import json
import sys

from _temu_token_store import list_stores

def main():
    mask = True
    if len(sys.argv) >= 2:
        try:
            params = json.loads(sys.argv[1])
            mask = params.get("mask", True)
        except json.JSONDecodeError as e:
            print(f"Invalid parameter format: {e}", file=sys.stderr)
            sys.exit(1)

    print(json.dumps(list_stores(mask=mask), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
