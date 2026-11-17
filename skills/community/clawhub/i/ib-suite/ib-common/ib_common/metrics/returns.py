# skills/ib-common/ib_common/metrics/returns.py
"""Return-based performance ratios computed from a period-return series.

All functions accept a sequence of periodic (e.g. daily) simple returns and
annualize with `periods` (252 trading days by default). Zero-variance or
degenerate inputs return 0.0 rather than raising, so callers can treat the
result as a plain fact.
"""
from __future__ import annotations
from collections.abc import Sequence
import numpy as np


def sharpe(returns: Sequence[float], rf: float = 0.0, periods: int = 252) -> float:
    """Annualized Sharpe ratio; 0.0 when volatility is zero."""
    r = np.asarray(returns, dtype=float)
    excess = r - rf / periods
    sd = excess.std(ddof=1) if r.size > 1 else 0.0
    if sd == 0:
        return 0.0
    return float(np.sqrt(periods) * excess.mean() / sd)


def sortino(returns: Sequence[float], rf: float = 0.0, periods: int = 252) -> float:
    """Annualized Sortino ratio using downside deviation; 0.0 if no downside."""
    r = np.asarray(returns, dtype=float)
    excess = r - rf / periods
    downside = excess[excess < 0]
    dd = downside.std(ddof=1) if downside.size > 1 else 0.0
    if dd == 0:
        return 0.0
    return float(np.sqrt(periods) * excess.mean() / dd)


def calmar(returns: Sequence[float], periods: int = 252) -> float:
    """Annualized return divided by absolute max drawdown of the equity curve."""
    r = np.asarray(returns, dtype=float)
    if r.size == 0:
        return 0.0
    equity = np.cumprod(1 + r)
    running_max = np.maximum.accumulate(equity)
    drawdown = equity / running_max - 1.0
    max_dd = drawdown.min()
    if max_dd == 0:
        return 0.0
    ann_return = equity[-1] ** (periods / r.size) - 1.0
    return float(ann_return / abs(max_dd))
