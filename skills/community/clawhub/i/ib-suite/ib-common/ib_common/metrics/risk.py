# skills/ib-common/ib_common/metrics/risk.py
"""Risk measures: drawdown, historical VaR/CVaR, and concentration (HHI).

VaR and CVaR are reported as positive loss magnitudes at the given
confidence level using the historical (non-parametric) method.
"""
from __future__ import annotations
from collections.abc import Sequence
import numpy as np


def max_drawdown(equity: Sequence[float]) -> float:
    """Largest peak-to-trough decline of an equity curve, as a negative fraction."""
    e = np.asarray(equity, dtype=float)
    if e.size == 0:
        return 0.0
    running_max = np.maximum.accumulate(e)
    drawdown = e / running_max - 1.0
    return float(drawdown.min())


def hist_var(returns: Sequence[float], level: float = 0.95) -> float:
    """Historical Value-at-Risk at `level`, returned as a positive loss."""
    r = np.asarray(returns, dtype=float)
    if r.size == 0:
        return 0.0
    q = np.quantile(r, 1 - level)      # left-tail quantile of returns
    return float(max(0.0, -q))


def hist_cvar(returns: Sequence[float], level: float = 0.95) -> float:
    """Historical Conditional VaR (expected shortfall), positive loss."""
    r = np.asarray(returns, dtype=float)
    if r.size == 0:
        return 0.0
    threshold = np.quantile(r, 1 - level)
    tail = r[r <= threshold]
    if tail.size == 0:
        return float(max(0.0, -threshold))
    return float(max(0.0, -tail.mean()))


def hhi(weights: Sequence[float]) -> float:
    """Herfindahl-Hirschman concentration index of |weights|, normalized to sum=1."""
    w = np.abs(np.asarray(weights, dtype=float))
    total = w.sum()
    if total == 0:
        return 0.0
    w = w / total
    return float(np.sum(w ** 2))
