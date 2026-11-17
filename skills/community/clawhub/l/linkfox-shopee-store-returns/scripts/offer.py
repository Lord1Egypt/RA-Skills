#!/usr/bin/env python3
"""
Shopee Store — offer

官方: https://open.shopee.com/documents/v2/v2.returns.offer?module=102&type=1

入参说明见 references/apis/offer.md。
"""

from __future__ import annotations

import json
import sys

from _returns_api_runner import run_returns_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: offer.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_returns_api("offer", params, "offer.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
