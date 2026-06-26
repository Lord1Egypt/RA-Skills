#!/usr/bin/env python3
"""Recent filled trades from OKX (last N, default 20)."""
from __future__ import annotations

import argparse
import sys

from _okx_client import trade_api


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--instType", default="SPOT")
    p.add_argument("--limit", default="20")
    args = p.parse_args()

    resp = trade_api().get_fills_history(instType=args.instType, limit=args.limit)
    if resp.get("code") != "0":
        print(f"OKX error: {resp.get('msg')!r}", file=sys.stderr)
        return 1
    rows = resp.get("data") or []
    if not rows:
        print("No recent fills.")
        return 0
    print(f"Recent fills ({len(rows)}, instType={args.instType}):")
    print(f"{'ts':<14} {'instId':<18} {'side':<5} {'sz':>12} {'px':>14} {'fee':>12} {'feeCcy':<6}")
    for f in rows:
        print(
            f"{f.get('ts',''):<14} {f.get('instId',''):<18} {f.get('side',''):<5} "
            f"{f.get('fillSz',''):>12} {f.get('fillPx',''):>14} {f.get('fee',''):>12} {f.get('feeCcy',''):<6}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
