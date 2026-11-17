#!/usr/bin/env python3
"""
Shopee Store — list_gms_user_deleted_item

官方: https://open.shopee.com/documents/v2/v2.ads.list_gms_user_deleted_item?module=117&type=1

入参说明见 references/apis/list-gms-user-deleted-item.md。
"""

from __future__ import annotations

import json
import sys

from _ads_api_runner import run_ads_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: list_gms_user_deleted_item.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_ads_api("list_gms_user_deleted_item", params, "list_gms_user_deleted_item.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
