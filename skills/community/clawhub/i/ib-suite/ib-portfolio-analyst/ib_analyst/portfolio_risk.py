"""Diagnostic module 5: portfolio risk (VaR / CVaR / max drawdown).

Builds a weight-weighted daily return series from per-symbol close-to-close
returns, then applies the historical risk metrics from ib_common. Weights
come from current market values in the snapshot.
"""
from __future__ import annotations
from collections import defaultdict
import numpy as np
from ib_common.schema import Snapshot, DailyBar
from ib_common.metrics.risk import hist_var, hist_cvar, max_drawdown
from .findings import Finding, grade

DIM = "portfolio_risk"


def _returns_by_symbol(bars: list[DailyBar]) -> dict[str, list[float]]:
    """Close-to-close simple returns per symbol, ordered by date."""
    by_sym: dict[str, list[DailyBar]] = defaultdict(list)
    for b in bars:
        by_sym[b.symbol].append(b)
    out: dict[str, list[float]] = {}
    for sym, series in by_sym.items():
        series.sort(key=lambda b: b.date)
        closes = np.array([b.close for b in series], dtype=float)
        if closes.size >= 2:
            out[sym] = list(closes[1:] / closes[:-1] - 1.0)
    return out


def portfolio_returns(snapshot: Snapshot, bars: list[DailyBar]) -> list[float]:
    """Weight per-symbol return series by market value into a portfolio series."""
    rets = _returns_by_symbol(bars)
    if not rets:
        return []
    gross = sum(abs(p.base_value) for p in snapshot.positions) or 1.0
    weights = {p.symbol: abs(p.base_value) / gross for p in snapshot.positions}
    n = min(len(v) for v in rets.values())
    port = np.zeros(n)
    for sym, series in rets.items():
        w = weights.get(sym, 0.0)
        port += w * np.array(series[-n:])
    return list(port)


def analyze(snapshot: Snapshot, bars: list[DailyBar], thresholds: dict) -> list[Finding]:
    """Return portfolio VaR(95%) and max-drawdown findings."""
    port = portfolio_returns(snapshot, bars)
    if not port:
        return []

    var95 = hist_var(port, 0.95)
    cvar95 = hist_cvar(port, 0.95)
    equity = np.cumprod([1 + r for r in port])
    mdd = abs(max_drawdown(list(equity)))

    findings: list[Finding] = []
    findings.append(Finding(
        priority=grade(var95, thresholds["var95_warn"], thresholds["var95_crit"]),
        dimension=DIM,
        finding=f"1-day 95% historical VaR is {var95:.2%} (CVaR {cvar95:.2%})",
        evidence={"metric": "var95", "var95": round(var95, 5), "cvar95": round(cvar95, 5),
                  "n_days": len(port)},
        impact="on a bad day around this loss fraction is expected to be exceeded 5% of the time",
        suggestion="check the loss size against your daily risk tolerance",
        trigger_condition=f"1-day 95% VaR >= {thresholds['var95_warn']:.0%}",
        confidence=0.7,
        data_limitations="historical VaR on a short window; not forward-looking",
    ))
    findings.append(Finding(
        priority=grade(mdd, thresholds["max_drawdown_warn"], thresholds["max_drawdown_crit"]),
        dimension=DIM,
        finding=f"Sample-window max drawdown is {mdd:.1%}",
        evidence={"metric": "max_drawdown", "max_drawdown": round(mdd, 4), "n_days": len(port)},
        impact="drawdown shows the worst peak-to-trough drop over the sample",
        suggestion="verify this is within the drawdown you can hold through",
        trigger_condition=f"max drawdown >= {thresholds['max_drawdown_warn']:.0%}",
        confidence=0.7,
        data_limitations="based on the daily bars available in the lake",
    ))
    return findings
