"""
strategy_engine.py — Signal generation and technical indicator logic.

Each strategy function receives a DataFrame of OHLCV bars and returns a list of Signal objects.
New strategies can be added and registered in config/settings.yaml.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd
from loguru import logger


# ── Data Models ────────────────────────────────────────────────────────────────

@dataclass
class Signal:
    symbol: str
    direction: str          # "LONG" or "SHORT"
    strategy: str
    entry_price: float
    stop_price: float
    target_price: float
    confidence: float       # 0.0 – 1.0
    quantity: int = 0       # Filled by risk_manager
    entry_reason: str = ""
    indicators: dict = field(default_factory=dict)
    market_conditions: dict = field(default_factory=dict)
    signal_id: str = field(default_factory=lambda: str(uuid.uuid4()))


# ── Indicators ─────────────────────────────────────────────────────────────────

def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, adjust=False).mean()
    avg_loss = loss.ewm(com=period - 1, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def compute_macd(series: pd.Series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def compute_atr(bars: pd.DataFrame, period: int = 14) -> pd.Series:
    high_low = bars["high"] - bars["low"]
    high_close = (bars["high"] - bars["close"].shift()).abs()
    low_close = (bars["low"] - bars["close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.ewm(com=period - 1, adjust=False).mean()


def compute_ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def compute_indicators(bars: pd.DataFrame, params: dict) -> dict:
    """Compute all indicators for a bar DataFrame."""
    close = bars["close"]
    rsi_period = params.get("rsi_period", 14)
    ema_period = params.get("ema_trend_period", 50)

    rsi = compute_rsi(close, rsi_period)
    atr = compute_atr(bars)
    ema = compute_ema(close, ema_period)

    return {
        "rsi": float(rsi.iloc[-1]),
        "atr": float(atr.iloc[-1]),
        f"ema_{ema_period}": float(ema.iloc[-1]),
        "last_close": float(close.iloc[-1]),
    }


# ── Strategies ─────────────────────────────────────────────────────────────────

def strategy_rsi_mean_reversion(symbol: str, bars: pd.DataFrame, params: dict) -> list[Signal]:
    """
    RSI Mean Reversion:
    - LONG when RSI < oversold AND price above EMA (uptrend context)
    - SHORT when RSI > overbought AND price below EMA (downtrend context)
    """
    signals = []
    if len(bars) < 55:
        return signals

    close = bars["close"]
    rsi = compute_rsi(close, params["rsi_period"])
    atr = compute_atr(bars)
    ema = compute_ema(close, params["ema_trend_period"])

    last_rsi = rsi.iloc[-1]
    last_atr = atr.iloc[-1]
    last_close = close.iloc[-1]
    last_ema = ema.iloc[-1]
    atr_mult = 2.0  # default; overridden by risk config in production

    indicators = {
        "rsi": round(last_rsi, 2),
        "atr": round(last_atr, 4),
        f"ema_{params['ema_trend_period']}": round(last_ema, 4),
    }

    # LONG signal
    if last_rsi < params["oversold"] and last_close > last_ema:
        stop = last_close - (last_atr * atr_mult)
        target = last_close + (last_atr * atr_mult * 1.5)
        confidence = round(1 - (last_rsi / params["oversold"]), 2)
        signals.append(Signal(
            symbol=symbol,
            direction="LONG",
            strategy="rsi_mean_reversion",
            entry_price=last_close,
            stop_price=stop,
            target_price=target,
            confidence=confidence,
            entry_reason=f"RSI={last_rsi:.1f} below {params['oversold']}, price above EMA{params['ema_trend_period']}",
            indicators=indicators,
        ))

    # SHORT signal
    elif last_rsi > params["overbought"] and last_close < last_ema:
        stop = last_close + (last_atr * atr_mult)
        target = last_close - (last_atr * atr_mult * 1.5)
        confidence = round((last_rsi - params["overbought"]) / (100 - params["overbought"]), 2)
        signals.append(Signal(
            symbol=symbol,
            direction="SHORT",
            strategy="rsi_mean_reversion",
            entry_price=last_close,
            stop_price=stop,
            target_price=target,
            confidence=confidence,
            entry_reason=f"RSI={last_rsi:.1f} above {params['overbought']}, price below EMA{params['ema_trend_period']}",
            indicators=indicators,
        ))

    return signals


def strategy_macd_momentum(symbol: str, bars: pd.DataFrame, params: dict) -> list[Signal]:
    """
    MACD Momentum:
    - LONG when MACD histogram crosses above 0 with min size
    - SHORT when MACD histogram crosses below 0 with min size
    """
    signals = []
    if len(bars) < 35:
        return signals

    close = bars["close"]
    _, _, hist = compute_macd(close, params["fast"], params["slow"], params["signal"])
    atr = compute_atr(bars)

    last_hist = hist.iloc[-1]
    prev_hist = hist.iloc[-2]
    last_atr = atr.iloc[-1]
    last_close = close.iloc[-1]
    atr_mult = 2.0

    indicators = {
        "macd_hist": round(last_hist, 4),
        "atr": round(last_atr, 4),
    }

    # LONG: histogram crosses above 0
    if prev_hist < 0 and last_hist >= params["min_histogram"]:
        stop = last_close - (last_atr * atr_mult)
        target = last_close + (last_atr * atr_mult * 1.5)
        confidence = min(last_hist / params["min_histogram"] / 5, 1.0)
        signals.append(Signal(
            symbol=symbol,
            direction="LONG",
            strategy="macd_momentum",
            entry_price=last_close,
            stop_price=stop,
            target_price=target,
            confidence=round(confidence, 2),
            entry_reason=f"MACD hist crossed above 0, hist={last_hist:.4f}",
            indicators=indicators,
        ))

    # SHORT: histogram crosses below 0
    elif prev_hist > 0 and last_hist <= -params["min_histogram"]:
        stop = last_close + (last_atr * atr_mult)
        target = last_close - (last_atr * atr_mult * 1.5)
        confidence = min(abs(last_hist) / params["min_histogram"] / 5, 1.0)
        signals.append(Signal(
            symbol=symbol,
            direction="SHORT",
            strategy="macd_momentum",
            entry_price=last_close,
            stop_price=stop,
            target_price=target,
            confidence=round(confidence, 2),
            entry_reason=f"MACD hist crossed below 0, hist={last_hist:.4f}",
            indicators=indicators,
        ))

    return signals


# ── Strategy Registry ──────────────────────────────────────────────────────────

STRATEGY_REGISTRY = {
    "rsi_mean_reversion": strategy_rsi_mean_reversion,
    "macd_momentum": strategy_macd_momentum,
}


# ── StrategyEngine ─────────────────────────────────────────────────────────────

class StrategyEngine:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.enabled = cfg["strategies"]["enabled"]
        self.params = cfg["strategies"]["params"]
        logger.info(f"StrategyEngine initialized with strategies: {self.enabled}")

    def generate_signals(self, bars_dict: dict) -> list[Signal]:
        """Run all enabled strategies over all symbols. Returns deduplicated signals."""
        all_signals: list[Signal] = []
        for symbol, bars in bars_dict.items():
            for strategy_name in self.enabled:
                fn = STRATEGY_REGISTRY.get(strategy_name)
                if fn is None:
                    logger.warning(f"Unknown strategy: {strategy_name}")
                    continue
                params = self.params.get(strategy_name, {})
                try:
                    signals = fn(symbol, bars, params)
                    all_signals.extend(signals)
                    if signals:
                        logger.info(
                            f"[{strategy_name}] {symbol}: {signals[0].direction} "
                            f"conf={signals[0].confidence}"
                        )
                except Exception as e:
                    logger.error(f"Strategy {strategy_name} failed on {symbol}: {e}")

        # Deduplicate: one signal per symbol
        seen = set()
        deduped = []
        for s in sorted(all_signals, key=lambda x: -x.confidence):
            if s.symbol not in seen:
                seen.add(s.symbol)
                deduped.append(s)

        return deduped

    def score_signal(self, signal: Signal) -> float:
        return signal.confidence

    def update_params(self, strategy_name: str, new_params: dict) -> None:
        """Apply improved parameters (called by performance tracker)."""
        if strategy_name in self.params:
            self.params[strategy_name].update(new_params)
            logger.info(f"Updated params for {strategy_name}: {new_params}")
