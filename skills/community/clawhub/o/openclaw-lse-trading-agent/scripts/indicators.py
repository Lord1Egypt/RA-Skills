"""Technical indicator calculations for LSE stocks.

Computes: RSI, MACD, Bollinger Bands, EMA 50/200, ATR, VWAP, OBV.
Outputs signal flags for golden cross, death cross, oversold, overbought, bollinger squeeze.

Usage:
    uv run scripts/indicators.py HSBA.L --period 1y
    uv run scripts/indicators.py VOD.L --period 6mo --interval 1d
"""

import argparse
import json
import sys
from datetime import datetime

import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf

from config import IndicatorParams


def fetch_ohlcv(ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """Fetch OHLCV data from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    if df.empty:
        print(json.dumps({"error": f"No data found for {ticker}"}))
        sys.exit(1)
    return df


def compute_indicators(df: pd.DataFrame, params: IndicatorParams | None = None) -> dict:
    """Compute all technical indicators and return structured results."""
    if params is None:
        params = IndicatorParams()

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    # RSI
    rsi_series = ta.rsi(close, length=params.rsi_period)
    rsi = float(rsi_series.iloc[-1]) if rsi_series is not None else None

    # MACD
    macd_df = ta.macd(close, fast=params.macd_fast, slow=params.macd_slow, signal=params.macd_signal)
    macd_line = float(macd_df.iloc[-1, 0]) if macd_df is not None else None
    macd_signal = float(macd_df.iloc[-1, 2]) if macd_df is not None else None
    macd_hist = float(macd_df.iloc[-1, 1]) if macd_df is not None else None
    macd_hist_prev = float(macd_df.iloc[-2, 1]) if macd_df is not None and len(macd_df) > 1 else None

    # Bollinger Bands
    bb = ta.bbands(close, length=params.bb_period, std=params.bb_std)
    bb_upper = float(bb.iloc[-1, 0]) if bb is not None else None
    bb_mid = float(bb.iloc[-1, 1]) if bb is not None else None
    bb_lower = float(bb.iloc[-1, 2]) if bb is not None else None
    bb_width = (bb_upper - bb_lower) / bb_mid if bb_mid and bb_mid != 0 else None

    # Bollinger %B (where price sits within bands)
    current_price = float(close.iloc[-1])
    bb_pct_b = (current_price - bb_lower) / (bb_upper - bb_lower) if bb_upper and bb_lower and bb_upper != bb_lower else None

    # EMA 50 / 200
    ema_short = ta.ema(close, length=params.ema_short)
    ema_long = ta.ema(close, length=params.ema_long)
    ema_50 = float(ema_short.iloc[-1]) if ema_short is not None else None
    ema_200 = float(ema_long.iloc[-1]) if ema_long is not None else None

    # Golden cross / death cross detection (last 5 bars)
    golden_cross = False
    death_cross = False
    if ema_short is not None and ema_long is not None and len(ema_short) > 5:
        for i in range(-5, 0):
            prev_diff = ema_short.iloc[i - 1] - ema_long.iloc[i - 1]
            curr_diff = ema_short.iloc[i] - ema_long.iloc[i]
            if prev_diff <= 0 and curr_diff > 0:
                golden_cross = True
            if prev_diff >= 0 and curr_diff < 0:
                death_cross = True

    # ATR
    atr_series = ta.atr(high, low, close, length=params.atr_period)
    atr = float(atr_series.iloc[-1]) if atr_series is not None else None
    atr_pct = (atr / current_price * 100) if atr and current_price else None

    # VWAP (cumulative for the available data)
    typical_price = (high + low + close) / 3
    cumulative_tp_vol = (typical_price * volume).cumsum()
    cumulative_vol = volume.cumsum()
    vwap_series = cumulative_tp_vol / cumulative_vol
    vwap = float(vwap_series.iloc[-1]) if not vwap_series.empty else None

    # OBV
    obv_series = ta.obv(close, volume)
    obv = float(obv_series.iloc[-1]) if obv_series is not None else None
    obv_ema_series = ta.ema(obv_series, length=params.obv_ema) if obv_series is not None else None
    obv_ema = float(obv_ema_series.iloc[-1]) if obv_ema_series is not None else None
    obv_rising = obv > obv_ema if obv is not None and obv_ema is not None else None

    # Signal flags
    oversold = rsi is not None and rsi < 30
    overbought = rsi is not None and rsi > 70
    bollinger_squeeze = bb_width is not None and bb_width < 0.04
    above_vwap = current_price > vwap if vwap else None
    trend_up = ema_50 is not None and ema_200 is not None and ema_50 > ema_200
    macd_bullish = macd_hist is not None and macd_hist > 0
    macd_turning_up = (
        macd_hist is not None
        and macd_hist_prev is not None
        and macd_hist > macd_hist_prev
    )

    # Price change stats
    pct_1d = float((close.iloc[-1] / close.iloc[-2] - 1) * 100) if len(close) > 1 else None
    pct_5d = float((close.iloc[-1] / close.iloc[-6] - 1) * 100) if len(close) > 5 else None
    pct_20d = float((close.iloc[-1] / close.iloc[-21] - 1) * 100) if len(close) > 20 else None

    return {
        "ticker": df.index.name or "unknown",
        "price": round(current_price, 2),
        "date": str(df.index[-1].date()),
        "change_1d_pct": round(pct_1d, 2) if pct_1d else None,
        "change_5d_pct": round(pct_5d, 2) if pct_5d else None,
        "change_20d_pct": round(pct_20d, 2) if pct_20d else None,
        "indicators": {
            "rsi": round(rsi, 2) if rsi else None,
            "macd": {
                "line": round(macd_line, 4) if macd_line else None,
                "signal": round(macd_signal, 4) if macd_signal else None,
                "histogram": round(macd_hist, 4) if macd_hist else None,
            },
            "bollinger": {
                "upper": round(bb_upper, 2) if bb_upper else None,
                "mid": round(bb_mid, 2) if bb_mid else None,
                "lower": round(bb_lower, 2) if bb_lower else None,
                "width": round(bb_width, 4) if bb_width else None,
                "pct_b": round(bb_pct_b, 4) if bb_pct_b else None,
            },
            "ema": {
                "ema_50": round(ema_50, 2) if ema_50 else None,
                "ema_200": round(ema_200, 2) if ema_200 else None,
            },
            "atr": round(atr, 4) if atr else None,
            "atr_pct": round(atr_pct, 2) if atr_pct else None,
            "vwap": round(vwap, 2) if vwap else None,
            "obv": round(obv, 0) if obv else None,
        },
        "signals": {
            "trend_up": trend_up,
            "golden_cross": golden_cross,
            "death_cross": death_cross,
            "oversold": oversold,
            "overbought": overbought,
            "macd_bullish": macd_bullish,
            "macd_turning_up": macd_turning_up,
            "bollinger_squeeze": bollinger_squeeze,
            "above_vwap": above_vwap,
            "obv_rising": obv_rising,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Compute technical indicators for an LSE stock")
    parser.add_argument("ticker", help="Yahoo Finance ticker (e.g., HSBA.L)")
    parser.add_argument("--period", default="1y", help="Data period (1mo, 3mo, 6mo, 1y, 2y, 5y)")
    parser.add_argument("--interval", default="1d", help="Data interval (1d, 1wk, 1mo)")
    args = parser.parse_args()

    ticker = args.ticker if "." in args.ticker else f"{args.ticker}.L"
    df = fetch_ohlcv(ticker, period=args.period, interval=args.interval)
    result = compute_indicators(df)
    result["ticker"] = ticker
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
