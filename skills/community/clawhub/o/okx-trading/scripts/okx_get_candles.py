#!/usr/bin/env python3
"""Fetch OHLCV candles, optionally with RSI and SMA overlays.

Output is compact so the LLM can reason over it without context bloat:
  - Last 5 candles printed verbatim
  - Then: SMA(20), SMA(50), RSI(14) on the close series if --indicators
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone

from _okx_client import market_api


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
    # Wilder smoothing
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
    p.add_argument("--instId", required=True)
    p.add_argument("--bar", default="1H", help="1m,5m,15m,1H,4H,1D,…")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--indicators", action="store_true")
    args = p.parse_args()

    resp = market_api().get_candlesticks(instId=args.instId, bar=args.bar, limit=str(args.limit))
    if resp.get("code") != "0":
        print(f"OKX error: {resp.get('msg')!r}", file=sys.stderr)
        return 1

    raw = resp.get("data") or []
    if not raw:
        print("No candle data.")
        return 1

    # OKX returns newest first — reverse for chronological order.
    # Fields: [ts, o, h, l, c, vol, volCcy, volCcyQuote, confirm]
    candles = list(reversed(raw))
    closes = [float(c[4]) for c in candles]

    print(f"{args.instId} {args.bar}  ({len(candles)} candles)")
    print(f"{'time (UTC)':<20} {'open':>12} {'high':>12} {'low':>12} {'close':>12}")
    for c in candles[-5:]:
        ts = datetime.fromtimestamp(int(c[0]) / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
        print(f"{ts:<20} {c[1]:>12} {c[2]:>12} {c[3]:>12} {c[4]:>12}")

    if args.indicators:
        sma20 = _sma(closes, 20)
        sma50 = _sma(closes, 50)
        rsi14 = _rsi(closes, 14)
        last_close = closes[-1]
        print()
        print(f"Indicators on close:")
        print(f"  last close : {last_close}")
        print(f"  SMA(20)    : {sma20:.4f}" if sma20 is not None else "  SMA(20)    : n/a")
        print(f"  SMA(50)    : {sma50:.4f}" if sma50 is not None else "  SMA(50)    : n/a")
        print(f"  RSI(14)    : {rsi14:.2f}" if rsi14 is not None else "  RSI(14)    : n/a")
        if rsi14 is not None:
            if rsi14 < 30:
                print("  signal     : RSI oversold (<30) — consider buy")
            elif rsi14 > 70:
                print("  signal     : RSI overbought (>70) — consider sell")
            else:
                print("  signal     : neutral")
    return 0


if __name__ == "__main__":
    sys.exit(main())
