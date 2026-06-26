#!/usr/bin/env python3
"""
Compute technical features from OHLCV kline data.
Input (stdin JSON):
  {
    "klines": [[open_time, open, high, low, close, volume, ...], ...],   ← required
    "prices": [float, ...],   ← optional legacy fallback
    "volume": float,
    "avg_volume": float
  }
Output:
  {
    "last_price": float,
    "ema20": float,
    "ema50": float,
    "rsi14": float,
    "atr14": float,
    "macd": float,       ← MACD line (EMA12 - EMA26)
    "macd_signal": float, ← 9-period EMA of MACD
    "volume_ratio": float,
    "trend": "up"|"down"|"neutral",
    "momentum": "up"|"down"|"neutral",
    "high_volatility": bool,
    "funding_rate": float|null
  }
"""
import json
import sys


def ema(values: list, period: int) -> list:
    """Exponential moving average."""
    if not values or period <= 0:
        return []
    k = 2.0 / (period + 1)
    result = [None] * len(values)
    if len(values) < period:
        # Not enough data for a full SMA seed — use all available data as seed
        sma = sum(values) / len(values)
        result[-1] = sma
        return result
    sma = sum(values[:period]) / period
    result[period - 1] = sma
    for i in range(period, len(values)):
        result[i] = values[i] * k + result[i - 1] * (1 - k)
    return result


def rsi(closes: list, period: int = 14) -> float | None:
    """RSI for the most recent bar."""
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for i in range(-period, 0):
        diff = closes[i] - closes[i - 1]
        if diff >= 0:
            gains.append(diff)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(-diff)
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1 + rs))


def atr(highs: list, lows: list, closes: list, period: int = 14) -> float | None:
    """Average True Range for the most recent bar."""
    if len(highs) < period + 1:
        return None
    true_ranges = []
    for i in range(1, len(highs)):
        tr = max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1]))
        true_ranges.append(tr)
    if len(true_ranges) < period:
        return None
    return sum(true_ranges[-period:]) / period


def parse_klines(raw: list) -> tuple[list, list, list, list, list]:
    """Parse raw kline arrays → (opens, highs, lows, closes, volumes)."""
    opens, highs, lows, closes, volumes = [], [], [], [], []
    for k in raw:
        opens.append(float(k[1]))
        highs.append(float(k[2]))
        lows.append(float(k[3]))
        closes.append(float(k[4]))
        volumes.append(float(k[5]))
    return opens, highs, lows, closes, volumes


def main() -> int:
    payload = json.load(sys.stdin)
    klines_raw = payload.get("klines") or []
    funding_rate = payload.get("funding_rate")

    if klines_raw:
        opens, highs, lows, closes, volumes = parse_klines(klines_raw)
    else:
        # Legacy fallback
        closes = [float(x) for x in payload.get("prices", [])]
        highs = closes
        lows = closes
        volumes = []
        raw_vol = float(payload.get("volume", 0))
        avg_vol = float(payload.get("avg_volume", 1))

    if not closes:
        print(json.dumps({"error": "no price data"}))
        return 1

    last_price = closes[-1]

    # EMA series
    ema20_series = ema(closes, 20)
    ema50_series = ema(closes, 50)
    ema12_series = ema(closes, 12)
    ema26_series = ema(closes, 26)

    ema20_val = next((v for v in reversed(ema20_series) if v is not None), None)
    ema50_val = next((v for v in reversed(ema50_series) if v is not None), None)

    # MACD
    macd_line_series = []
    for e12, e26 in zip(ema12_series, ema26_series):
        if e12 is not None and e26 is not None:
            macd_line_series.append(e12 - e26)
        else:
            macd_line_series.append(None)
    macd_valid = [v for v in macd_line_series if v is not None]
    macd_val = macd_valid[-1] if macd_valid else None
    signal9 = ema(macd_valid, 9)
    macd_signal_val = next((v for v in reversed(signal9) if v is not None), None)

    # RSI
    rsi_val = rsi(closes, 14)

    # ATR
    if klines_raw:
        atr_val = atr(highs, lows, closes, 14)
    else:
        atr_val = None

    # Volume ratio
    if volumes:
        avg_vol = sum(volumes[-20:]) / min(20, len(volumes)) if volumes else 1
        raw_vol = volumes[-1]
    else:
        avg_vol = float(payload.get("avg_volume", 1)) or 1
        raw_vol = float(payload.get("volume", 0))
    volume_ratio = raw_vol / avg_vol if avg_vol else 0.0

    # High volatility: ATR > 2% of price
    high_vol = False
    if atr_val and last_price:
        high_vol = (atr_val / last_price) > 0.02

    # Trend: price vs EMAs
    if ema20_val and ema50_val:
        if last_price > ema20_val > ema50_val:
            trend = "up"
        elif last_price < ema20_val < ema50_val:
            trend = "down"
        else:
            trend = "neutral"
    elif ema20_val:
        trend = "up" if last_price > ema20_val else "down"
    else:
        trend = "neutral"

    # Momentum: RSI zones
    if rsi_val is not None:
        if rsi_val > 55:
            momentum = "up"
        elif rsi_val < 45:
            momentum = "down"
        else:
            momentum = "neutral"
    else:
        momentum = "neutral"

    result = {
        "last_price": last_price,
        "ema20": ema20_val,
        "ema50": ema50_val,
        "rsi14": rsi_val,
        "atr14": atr_val,
        "macd": macd_val,
        "macd_signal": macd_signal_val,
        "volume_ratio": volume_ratio,
        "trend": trend,
        "momentum": momentum,
        "high_volatility": high_vol,
        "funding_rate": float(funding_rate) if funding_rate is not None else None,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
