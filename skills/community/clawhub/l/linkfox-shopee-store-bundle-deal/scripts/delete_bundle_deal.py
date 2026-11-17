#!/usr/bin/env python3
"""
Shopee Store — delete_bundle_deal

官方: https://open.shopee.com/documents/v2/v2.bundle_deal.delete_bundle_deal?module=110&type=1

入参说明见 references/apis/delete-bundle-deal.md。
"""

from __future__ import annotations

import json
import sys

from _bundle_deal_api_runner import run_bundle_deal_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: delete_bundle_deal.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_bundle_deal_api("delete_bundle_deal", params, "delete_bundle_deal.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
