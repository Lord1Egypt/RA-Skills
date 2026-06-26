#!/usr/bin/env python3
"""Fetch daily OHLCV candles, optionally with RSI/SMA overlays.

Output mirrors okx_get_candles.py for consistency across the two skills.
"""
from __future__ import annotations

import argparse
import sys

from _ibkr_client import connect, smart_stock


def _sma(values: list[float], window: int) -> float | None:
    if len(values) < window:
        return None
    return sum(values[-window:]) / window


def _rsi(values: list[float], period: int = 14) -> float | None:
    if len(values) < period + 1:
        return None
    gains: list[float] = []
    losses: list[float] = []
    for i in range(1, len(values)):
        delta = values[i] - values[i - 1]
        gains.append(max(delta, 0.0))
        losses.append(max(-delta, 0.0))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - 100.0 / (1.0 + rs)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--symbol", required=True)
    p.add_argument("--exchange", default=None)
    p.add_argument("--currency", default=None)
    p.add_argument("--duration", default="6 M",
                   help='IBKR duration string. e.g. "30 D", "6 M", "1 Y", "2 Y"')
    p.add_argument("--bar", default="1 day",
                   help='IBKR bar size. "1 day", "1 hour", "5 mins", etc.')
    p.add_argument("--what-to-show", default="TRADES",
                   help='"TRADES" (default) or "MIDPOINT" for FX/options')
    p.add_argument("--indicators", action="store_true")
    args = p.parse_args()

    ib = connect()
    try:
        contract = smart_stock(args.symbol, args.exchange, args.currency)
        qualified = ib.qualifyContracts(contract)
        if not qualified:
            print(f"Could not qualify contract for {args.symbol}", file=sys.stderr)
            return 1

        bars = ib.reqHistoricalData(
            qualified[0],
            endDateTime="",
            durationStr=args.duration,
            barSizeSetting=args.bar,
            whatToShow=args.what_to_show,
            useRTH=True,
            formatDate=1,
        )
        if not bars:
            print(f"No bars returned for {args.symbol}", file=sys.stderr)
            return 1

        print(f"{args.symbol} {args.bar}  ({len(bars)} bars)")
        print(f"{'date':<22} {'open':>12} {'high':>12} {'low':>12} {'close':>12} {'volume':>14}")
        for b in bars[-5:]:
            print(f"{str(b.date):<22} {b.open:>12.2f} {b.high:>12.2f} {b.low:>12.2f} {b.close:>12.2f} {b.volume:>14}")

        if args.indicators:
            closes = [b.close for b in bars]
            sma20 = _sma(closes, 20)
            sma50 = _sma(closes, 50)
            rsi14 = _rsi(closes, 14)
            print()
            print("Indicators on close:")
            print(f"  last close : {closes[-1]:.2f}")
            print(f"  SMA(20)    : {sma20:.2f}" if sma20 is not None else "  SMA(20)    : n/a")
            print(f"  SMA(50)    : {sma50:.2f}" if sma50 is not None else "  SMA(50)    : n/a")
            print(f"  RSI(14)    : {rsi14:.2f}" if rsi14 is not None else "  RSI(14)    : n/a")
            if rsi14 is not None:
                if rsi14 < 30:
                    print("  signal     : RSI oversold (<30) — consider buy")
                elif rsi14 > 70:
                    print("  signal     : RSI overbought (>70) — consider sell")
                else:
                    print("  signal     : neutral")
    finally:
        ib.disconnect()
    return 0


if __name__ == "__main__":
    sys.exit(main())
