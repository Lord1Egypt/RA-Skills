#!/usr/bin/env python3
"""
Shopee Store — ban_user_comment

官方: https://open.shopee.com/documents/v2/v2.livestream.ban_user_comment?module=125&type=1

入参说明见 references/apis/ban-user-comment.md。
"""

from __future__ import annotations

import json
import sys

from _livestream_api_runner import run_livestream_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: ban_user_comment.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_livestream_api("ban_user_comment", params, "ban_user_comment.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
