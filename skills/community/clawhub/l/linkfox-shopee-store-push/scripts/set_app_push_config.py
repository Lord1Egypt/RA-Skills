#!/usr/bin/env python3
"""
Shopee Store — set_app_push_config

官方: https://open.shopee.com/documents/v2/v2.push.set_app_push_config?module=105&type=1

入参说明见 references/apis/set-app-push-config.md。
"""

from __future__ import annotations

import json
import sys

from _push_api_runner import run_push_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: set_app_push_config.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_push_api("set_app_push_config", params, "set_app_push_config.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
