#!/usr/bin/env python3
"""List currently open (un-filled) orders."""
from __future__ import annotations

import argparse
import sys

from _okx_client import trade_api


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--instType", default=None, help="SPOT|MARGIN|SWAP|FUTURES|OPTION")
    args = p.parse_args()

    kwargs: dict = {}
    if args.instType:
        kwargs["instType"] = args.instType
    resp = trade_api().get_order_list(**kwargs)
    if resp.get("code") != "0":
        print(f"OKX error: {resp.get('msg')!r}", file=sys.stderr)
        return 1
    rows = resp.get("data") or []
    if not rows:
        print("No open orders.")
        return 0
    print(f"Open orders ({len(rows)}):")
    print(f"{'instId':<18} {'side':<5} {'ordType':<8} {'sz':>12} {'px':>12} {'state':<10} {'ordId':<22}")
    for o in rows:
        print(
            f"{o.get('instId',''):<18} {o.get('side',''):<5} {o.get('ordType',''):<8} "
            f"{o.get('sz',''):>12} {o.get('px',''):>12} {o.get('state',''):<10} {o.get('ordId',''):<22}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
