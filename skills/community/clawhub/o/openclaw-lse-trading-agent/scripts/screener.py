"""FTSE 350 screener — scans tickers and ranks by composite technical score.

Fetches OHLCV data for FTSE 350 stocks, computes technical indicators,
and produces a composite score (-1.0 to +1.0) weighted across trend,
momentum, volatility, volume, and sentiment dimensions.

Usage:
    uv run scripts/screener.py                              → top 20 across all sectors
    uv run scripts/screener.py --sector Financials --top 5  → top 5 financials
    uv run scripts/screener.py --min-score 0.3              → only scores >= 0.3
"""

import argparse
import json
import sys
from typing import Any

from config import IndicatorParams, SignalWeights
from ftse350 import get_tickers
from indicators import compute_indicators, fetch_ohlcv


def _log(msg: str) -> None:
    """Print progress message to stderr."""
    print(msg, file=sys.stderr, flush=True)


def score_trend(signals: dict) -> float:
    """Score the trend component (-1.0 to +1.0).

    +1 if golden_cross or trend_up, -1 if death_cross or not trend_up, 0 otherwise.
    """
    if signals.get("golden_cross"):
        return 1.0
    if signals.get("death_cross"):
        return -1.0
    if signals.get("trend_up"):
        return 1.0
    if signals.get("trend_up") is False:
        return -1.0
    return 0.0


def score_momentum(indicators: dict, signals: dict) -> float:
    """Score the momentum component (-1.0 to +1.0).

    Averages an RSI-based score and a MACD histogram sign score.
    """
    # RSI score
    rsi = indicators.get("rsi")
    if rsi is None:
        rsi_score = 0.0
    elif rsi < 30:
        rsi_score = 1.0  # oversold bounce
    elif rsi < 50:
        rsi_score = 0.5  # rising
    elif rsi <= 70:
        rsi_score = 0.0  # neutral
    else:
        rsi_score = -1.0  # overbought

    # MACD histogram sign
    macd_data = indicators.get("macd", {})
    macd_hist = macd_data.get("histogram")
    if macd_hist is None:
        macd_score = 0.0
    elif macd_hist > 0:
        macd_score = 1.0
    elif macd_hist < 0:
        macd_score = -1.0
    else:
        macd_score = 0.0

    return (rsi_score + macd_score) / 2.0


def score_volatility(indicators: dict, signals: dict) -> float:
    """Score the volatility component (-1.0 to +1.0).

    Uses Bollinger %B. Buy the dip if trend_up and pct_b < 0.3,
    sell the rip if not trend_up and pct_b > 0.7, otherwise interpolate.
    """
    bb = indicators.get("bollinger", {})
    pct_b = bb.get("pct_b")
    trend_up = signals.get("trend_up", False)

    if pct_b is None:
        return 0.0

    if trend_up and pct_b < 0.3:
        return 1.0  # buy the dip
    if not trend_up and pct_b > 0.7:
        return -1.0  # sell the rip

    # Interpolate: map pct_b 0→+1, 0.5→0, 1→-1
    return 1.0 - 2.0 * max(0.0, min(1.0, pct_b))


def score_volume(signals: dict) -> float:
    """Score the volume component (-1.0 to +1.0).

    +1 if obv_rising AND above_vwap, -1 if both false, 0 if mixed.
    """
    obv_rising = signals.get("obv_rising")
    above_vwap = signals.get("above_vwap")

    if obv_rising is None or above_vwap is None:
        return 0.0

    if obv_rising and above_vwap:
        return 1.0
    if not obv_rising and not above_vwap:
        return -1.0
    return 0.0


def composite_score(result: dict, weights: SignalWeights | None = None) -> dict[str, float]:
    """Calculate weighted composite score from indicator results.

    Returns dict with individual component scores and the final composite.
    """
    if weights is None:
        weights = SignalWeights()

    signals = result.get("signals", {})
    indicators = result.get("indicators", {})

    trend = score_trend(signals)
    momentum = score_momentum(indicators, signals)
    volatility = score_volatility(indicators, signals)
    volume = score_volume(signals)
    sentiment = 0.0  # placeholder — filled by /lse-analyze

    score = (
        weights.trend * trend
        + weights.momentum * momentum
        + weights.volatility * volatility
        + weights.volume * volume
        + weights.sentiment * sentiment
    )

    return {
        "trend": round(trend, 4),
        "momentum": round(momentum, 4),
        "volatility": round(volatility, 4),
        "volume": round(volume, 4),
        "sentiment": round(sentiment, 4),
        "composite": round(score, 4),
    }


def scan_ticker(ticker: str, sector: str, params: IndicatorParams) -> dict[str, Any] | None:
    """Fetch data and compute score for a single ticker. Returns None on failure."""
    try:
        df = fetch_ohlcv(ticker, period="1y", interval="1d")
        result = compute_indicators(df, params)
        result["ticker"] = ticker

        scores = composite_score(result)

        return {
            "ticker": ticker,
            "sector": sector,
            "price": result.get("price"),
            "score": scores["composite"],
            "signals": {
                "trend": scores["trend"],
                "momentum": scores["momentum"],
                "volatility": scores["volatility"],
                "volume": scores["volume"],
            },
            "rsi": result.get("indicators", {}).get("rsi"),
            "macd_hist": result.get("indicators", {}).get("macd", {}).get("histogram"),
            "change_1d_pct": result.get("change_1d_pct"),
        }
    except SystemExit:
        # fetch_ohlcv calls sys.exit on empty data — catch it
        _log(f"  [skip] {ticker}: no data available")
        return None
    except Exception as e:
        _log(f"  [skip] {ticker}: {e}")
        return None


def run_screener(
    sector: str | None = None,
    top: int = 20,
    min_score: float | None = None,
) -> list[dict[str, Any]]:
    """Scan FTSE 350 tickers and return ranked results."""
    tickers = get_tickers(sector=sector)
    params = IndicatorParams()
    total = len(tickers)

    _log(f"Scanning {total} tickers" + (f" in {sector}" if sector else "") + "...")

    results: list[dict[str, Any]] = []
    for i, (ticker, sec) in enumerate(tickers.items(), 1):
        _log(f"  [{i}/{total}] {ticker}")
        entry = scan_ticker(ticker, sec, params)
        if entry is not None:
            results.append(entry)

    # Filter by min_score
    if min_score is not None:
        results = [r for r in results if r["score"] >= min_score]

    # Sort by score descending
    results.sort(key=lambda r: r["score"], reverse=True)

    # Limit to top N
    results = results[:top]

    _log(f"Done. {len(results)} stocks returned.")
    return results


def main():
    parser = argparse.ArgumentParser(description="FTSE 350 screener — rank stocks by composite technical score")
    parser.add_argument("--top", type=int, default=20, help="Number of top stocks to return (default: 20)")
    parser.add_argument("--sector", type=str, default=None, help="Filter by GICS sector (e.g., Financials)")
    parser.add_argument("--min-score", type=float, default=None, help="Minimum composite score threshold")
    args = parser.parse_args()

    results = run_screener(sector=args.sector, top=args.top, min_score=args.min_score)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
