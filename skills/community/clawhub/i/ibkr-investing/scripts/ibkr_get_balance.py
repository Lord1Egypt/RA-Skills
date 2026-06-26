#!/usr/bin/env python3
"""Print the IBKR account summary — NAV, cash, P&L, buying power."""
from __future__ import annotations

import sys

from _ibkr_client import connect, env_summary


KEYS = {
    "NetLiquidation": "NAV",
    "TotalCashValue": "Cash",
    "StockMarketValue": "Stocks",
    "OptionMarketValue": "Options",
    "FuturesPNL": "Futures P&L",
    "UnrealizedPnL": "Unrealized P&L",
    "RealizedPnL": "Realized P&L",
    "BuyingPower": "Buying Power",
    "MaintMarginReq": "Maintenance Margin",
    "GrossPositionValue": "Gross Position Value",
    "ExcessLiquidity": "Excess Liquidity",
}


def main() -> int:
    ib = connect()
    try:
        print(env_summary())
        print(f"Account: {ib.managedAccounts()}")
        print("-" * 50)
        for av in ib.accountValues():
            if av.tag in KEYS and av.currency == "BASE":
                try:
                    val = float(av.value)
                except ValueError:
                    continue
                print(f"{KEYS[av.tag]:.<28s} {val:>15,.2f}")
    finally:
        ib.disconnect()
    return 0


if __name__ == "__main__":
    sys.exit(main())
