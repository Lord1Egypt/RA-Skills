#!/usr/bin/env python3
"""Print a one-shot quote for a stock/ETF.

Defaults to SMART exchange + USD currency (US ETFs); override per-call.
"""
from __future__ import annotations

import argparse
import sys

from _ibkr_client import connect, smart_stock


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--symbol", required=True, help="e.g. VOO, SPY, AAPL")
    p.add_argument("--exchange", default=None, help="Default SMART (or IBKR_DEFAULT_EXCHANGE)")
    p.add_argument("--currency", default=None, help="Default USD (or IBKR_DEFAULT_CURRENCY)")
    p.add_argument("--data-type", choices=["live", "delayed", "delayed-frozen", "frozen"],
                   default="delayed-frozen",
                   help="Market data type. Delayed-frozen works without paid subscriptions.")
    args = p.parse_args()

    data_type_map = {"live": 1, "frozen": 2, "delayed": 3, "delayed-frozen": 4}

    ib = connect()
    try:
        contract = smart_stock(args.symbol, args.exchange, args.currency)
        ib.reqMarketDataType(data_type_map[args.data_type])
        ticker = ib.reqMktData(contract, "", False, False)
        ib.sleep(3)

        print(f"{args.symbol} ({contract.exchange}/{contract.currency})")
        print(f"  Last  : {ticker.last}")
        print(f"  Bid   : {ticker.bid} x {ticker.bidSize}")
        print(f"  Ask   : {ticker.ask} x {ticker.askSize}")
        print(f"  Close : {ticker.close}")
        print(f"  High  : {ticker.high}")
        print(f"  Low   : {ticker.low}")
        print(f"  Vol   : {ticker.volume}")
        ib.cancelMktData(contract)
    finally:
        ib.disconnect()
    return 0


if __name__ == "__main__":
    sys.exit(main())
