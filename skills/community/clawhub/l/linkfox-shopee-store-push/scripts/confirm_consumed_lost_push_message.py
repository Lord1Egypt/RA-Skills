#!/usr/bin/env python3
"""
Shopee Store — confirm_consumed_lost_push_message

官方: https://open.shopee.com/documents/v2/v2.push.confirm_consumed_lost_push_message?module=105&type=1

入参说明见 references/apis/confirm-consumed-lost-push-message.md。
"""

from __future__ import annotations

import json
import sys

from _push_api_runner import run_push_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: confirm_consumed_lost_push_message.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_push_api("confirm_consumed_lost_push_message", params, "confirm_consumed_lost_push_message.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
