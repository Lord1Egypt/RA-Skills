#!/usr/bin/env python3
"""
Shopee Store — delete_show_item

官方: https://open.shopee.com/documents/v2/v2.livestream.delete_show_item?module=125&type=1

入参说明见 references/apis/delete-show-item.md。
"""

from __future__ import annotations

import json
import sys

from _livestream_api_runner import run_livestream_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: delete_show_item.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_livestream_api("delete_show_item", params, "delete_show_item.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
