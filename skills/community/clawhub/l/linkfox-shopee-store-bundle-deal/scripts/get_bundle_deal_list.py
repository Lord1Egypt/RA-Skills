#!/usr/bin/env python3
"""
Shopee Store — get_bundle_deal_list

官方: https://open.shopee.com/documents/v2/v2.bundle_deal.get_bundle_deal_list?module=110&type=1

入参说明见 references/apis/get-bundle-deal-list.md。
"""

from __future__ import annotations

import json
import sys

from _bundle_deal_api_runner import run_bundle_deal_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_bundle_deal_list.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_bundle_deal_api("get_bundle_deal_list", params, "get_bundle_deal_list.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
