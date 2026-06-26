#!/usr/bin/env python3
"""Print a one-shot ticker for a symbol."""
from __future__ import annotations

import argparse
import sys

from _okx_client import market_api


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--instId", required=True, help="e.g. BTC-USDT, BTC-USDT-SWAP")
    args = p.parse_args()

    resp = market_api().get_ticker(instId=args.instId)
    if resp.get("code") != "0":
        print(f"OKX error: {resp.get('msg')!r}", file=sys.stderr)
        return 1

    data = resp.get("data") or []
    if not data:
        print(f"No ticker data for {args.instId}")
        return 1
    t = data[0]
    print(f"{args.instId}")
    print(f"  last : {t.get('last')}")
    print(f"  bid  : {t.get('bidPx')} ({t.get('bidSz')})")
    print(f"  ask  : {t.get('askPx')} ({t.get('askSz')})")
    print(f"  24h  : open={t.get('open24h')} high={t.get('high24h')} low={t.get('low24h')} vol={t.get('vol24h')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
