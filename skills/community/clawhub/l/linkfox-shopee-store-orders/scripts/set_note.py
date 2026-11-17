#!/usr/bin/env python3
"""
Shopee Store — set_note

官方: https://open.shopee.com/documents/v2/v2.order.set_note?module=94&type=1

入参说明见 references/apis/set-note.md。
"""

from __future__ import annotations

import json
import sys

from _order_api_runner import run_order_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: set_note.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_order_api("set_note", params, "set_note.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
