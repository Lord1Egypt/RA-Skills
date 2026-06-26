#!/usr/bin/env python3
"""List open positions (relevant for swap/futures/margin)."""
from __future__ import annotations

import argparse
import sys

from _okx_client import account_api


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--instType", default=None, help="MARGIN|SWAP|FUTURES|OPTION")
    args = p.parse_args()

    kwargs: dict = {}
    if args.instType:
        kwargs["instType"] = args.instType
    resp = account_api().get_positions(**kwargs)
    if resp.get("code") != "0":
        print(f"OKX error: {resp.get('msg')!r}", file=sys.stderr)
        return 1
    rows = resp.get("data") or []
    if not rows:
        print("No open positions.")
        return 0
    print(f"Open positions ({len(rows)}):")
    print(f"{'instId':<18} {'posSide':<6} {'pos':>14} {'avgPx':>14} {'upl':>14} {'lever':>6}")
    for p in rows:
        print(
            f"{p.get('instId',''):<18} {p.get('posSide',''):<6} "
            f"{p.get('pos',''):>14} {p.get('avgPx',''):>14} {p.get('upl',''):>14} {p.get('lever',''):>6}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
