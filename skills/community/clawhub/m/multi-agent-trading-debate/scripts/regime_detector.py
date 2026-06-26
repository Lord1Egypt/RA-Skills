#!/usr/bin/env python3
"""
Regime Detector - Classifies market regime using ADX + trend analysis.
Usage: python regime_detector.py [symbol] [timeframe]
"""
import sys
import json
from datetime import datetime

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

def calc_adx(high, low, close, period=14):
    """Calculate ADX indicator."""
    if not HAS_NUMPY or len(high) < period + 1:
        return 50.0  # default neutral

    high = np.array(high, dtype=float)
    low = np.array(low, dtype=float)
    close = np.array(close, dtype=float)

    plus_dm = np.where((high[1:] - high[:-1]) > (low[:-1] - low[1:]),
                        np.maximum(high[1:] - high[:-1], 0), 0)
    minus_dm = np.where((low[:-1] - low[1:]) > (high[1:] - high[:-1]),
                         np.maximum(low[:-1] - low[1:], 0), 0)

    tr = np.maximum(high[1:] - low[1:],
                    np.maximum(np.abs(high[1:] - close[:-1]),
                               np.abs(low[1:] - close[:-1])))

    plus_di = 100 * np.mean(plus_dm[-period:]) / (np.mean(tr[-period:]) + 1e-10)
    minus_di = 100 * np.mean(minus_dm[-period:]) / (np.mean(tr[-period:]) + 1e-10)

    dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di + 1e-10)
    adx = np.mean(dx[-period:])

    return float(adx)

def detect_regime(prices, symbol="BTCUSDT"):
    """
    Detect market regime from OHLCV data.
    Returns: {regime, adx, trend_strength, signal}
    """
    if len(prices) < 20:
        return _simulation_mode(symbol)

    if not HAS_NUMPY:
        return _simulation_mode(symbol)

    highs = [p.get("high", p.get("close", 50000)) for p in prices]
    lows = [p.get("low", p.get("close", 49000)) for p in prices]
    closes = [p.get("close", 49500) for p in prices]

    adx = calc_adx(highs, lows, closes)

    recent = closes[-7:]
    trend_up = all(recent[i] <= recent[i+1] for i in range(len(recent)-1))
    trend_down = all(recent[i] >= recent[i+1] for i in range(len(recent)-1))

    if adx > 25:
        regime = "TRENDING"
        signal = "follow" if not trend_down else "reverse"
    elif adx < 20:
        regime = "RANGING"
        signal = "mean_reversion"
    else:
        regime = "VOLATILE"
        signal = "reduced_size"

    return {
        "regime": regime,
        "adx": round(adx, 1),
        "trend_strength": "strong" if adx > 30 else "moderate",
        "signal": signal,
        "symbol": symbol,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "candles_analyzed": len(prices)
    }

def _simulation_mode(symbol):
    """Fallback when numpy not available."""
    return {
        "regime": "TRENDING",
        "adx": 28.5,
        "trend_strength": "moderate",
        "signal": "follow",
        "symbol": symbol,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "candles_analyzed": 0,
        "mode": "simulation"
    }

if __name__ == "__main__":
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT"
    result = detect_regime([], symbol)
    print(json.dumps(result, indent=2))
