# skills/ib-portfolio-analyst/ib_analyst/pnl_attribution.py
"""Diagnostic module 3: P&L attribution by position.

Breaks unrealized P&L down per symbol and flags when a single name drives an
outsized share of the total. The waterfall chart shows how each name adds up
to the portfolio's unrealized result.
"""
from __future__ import annotations
import plotly.graph_objects as go
from ib_common.schema import Snapshot
from .findings import Finding, Priority

DIM = "pnl_attribution"


def attribute(snapshot: Snapshot) -> dict[str, float]:
    """Per-symbol unrealized P&L with a '_total' aggregate key."""
    out: dict[str, float] = {}
    total = 0.0
    for p in snapshot.positions:
        pnl = p.base_unrealized_pnl   # base ccy, FX-converted before summing
        out[p.symbol] = out.get(p.symbol, 0.0) + pnl
        total += pnl
    out["_total"] = total
    return out


def analyze(snapshot: Snapshot, thresholds: dict) -> list[Finding]:
    """Flag the single largest contributor to gross unrealized P&L."""
    a = attribute(snapshot)
    per_name = {k: v for k, v in a.items() if k != "_total"}
    if not per_name:
        return []

    gross = sum(abs(v) for v in per_name.values())
    if gross == 0.0:
        # ib_sync v1 lands avg_cost as a market_price placeholder, so every
        # unrealized_pnl is 0. Attributing 0% to some name would be misleading;
        # report the data gap instead.
        return [Finding(
            priority=Priority.P3, dimension=DIM,
            finding="P&L attribution unavailable: no unrealized P&L in snapshot",
            evidence={"total_unrealized": a["_total"], "n_positions": len(per_name)},
            impact="cannot tell which names drive the book without live mark-to-market",
            suggestion="sync live/delayed market prices so market_price != avg_cost",
            trigger_condition="gross unrealized P&L == 0 across all positions",
            confidence=0.99,
            data_limitations="no unrealized P&L: market_price equals avg_cost (ib_sync v1 placeholder)",
        )]

    sym, val = max(per_name.items(), key=lambda kv: abs(kv[1]))
    share = abs(val) / gross
    priority = Priority.P2 if share >= thresholds["pnl_contrib_warn"] else Priority.P3
    return [Finding(
        priority=priority, dimension=DIM,
        finding=f"{sym} accounts for {share:.0%} of gross unrealized P&L ({val:+.0f})",
        evidence={"symbol": sym, "pnl": val, "share_of_gross": round(share, 4),
                  "total_unrealized": a["_total"]},
        impact="P&L is driven by one name; reversal there swings the whole book",
        suggestion="check whether this concentration of P&L is intentional",
        trigger_condition=f"one name >= {thresholds['pnl_contrib_warn']:.0%} of gross unrealized P&L",
        confidence=0.85,
        data_limitations="unrealized only; realized P&L requires execution history",
    )]


def build_chart(snapshot: Snapshot) -> go.Figure:
    """Waterfall of per-symbol contributions to total unrealized P&L."""
    a = attribute(snapshot)
    names = [k for k in a if k != "_total"]
    values = [a[n] for n in names]
    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative"] * len(names) + ["total"],
        x=names + ["Total"],
        y=values + [a["_total"]],
    ))
    fig.update_layout(title="Unrealized P&L attribution by position")
    return fig
