#!/usr/bin/env python3
"""List current IBKR positions with mark and unrealised P&L."""
from __future__ import annotations

import argparse
import sys

from _ibkr_client import connect, env_summary


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--with-mark", action="store_true",
                   help="Fetch a delayed mark for each position (slower; uses market data lines)")
    args = p.parse_args()

    ib = connect()
    try:
        print(env_summary())
        positions = ib.positions()
        if not positions:
            print("No positions.")
            return 0

        marks: dict[str, float] = {}
        if args.with_mark:
            ib.reqMarketDataType(3)  # Delayed-frozen — works without subscriptions.
            tickers = []
            for pos in positions:
                t = ib.reqMktData(pos.contract, "", False, False)
                tickers.append((pos.contract, t))
            ib.sleep(3)
            for contract, t in tickers:
                last = t.last if t.last and t.last == t.last else t.close  # NaN-guard
                if last:
                    marks[contract.symbol] = float(last)
                ib.cancelMktData(contract)

        print(f"{'Symbol':<12} {'Exch':<7} {'Qty':>10} {'Avg Cost':>12} {'Mark':>10} {'Value':>14} {'UPL':>12}")
        print("-" * 84)
        total_value = 0.0
        total_cost = 0.0
        for pos in positions:
            c = pos.contract
            sym = c.localSymbol or c.symbol
            qty = float(pos.position)
            avg = float(pos.avgCost) if pos.avgCost else 0.0
            cost = qty * avg
            mark = marks.get(c.symbol)
            value = qty * mark if mark else cost
            upl = (value - cost) if mark else 0.0
            total_value += value
            total_cost += cost
            mark_str = f"{mark:>10,.2f}" if mark else f"{'—':>10}"
            upl_str = f"{upl:>+12,.2f}" if mark else f"{'—':>12}"
            print(f"{sym:<12} {(c.exchange or ''):<7} {qty:>10,.2f} {avg:>12,.2f} {mark_str} {value:>14,.2f} {upl_str}")

        print("-" * 84)
        print(f"{'Total cost':<28} {total_cost:>15,.2f}")
        if marks:
            print(f"{'Total mark':<28} {total_value:>15,.2f}")
            print(f"{'Net UPL':<28} {total_value - total_cost:>+15,.2f}")
    finally:
        ib.disconnect()
    return 0


if __name__ == "__main__":
    sys.exit(main())
