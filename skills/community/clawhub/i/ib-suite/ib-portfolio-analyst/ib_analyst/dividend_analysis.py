"""Deterministic dividend facts: income mix, Yield on Cost, withholding drag.

All figures are historical facts from the Flex-sourced dividend records and
the current snapshot's cost basis. No forward yield, no growth forecast —
those are deferred.

Currency handling (v1): this module assumes a single reporting currency.
`income_by_symbol` aggregates gross/tax/net per symbol and keeps the row's
currency (first seen wins), and the withholding-drag ratio is computed on
pooled gross/tax totals across all rows. Grouping or FX-converting across
distinct currencies is deferred to a later iteration.
"""
from __future__ import annotations
from ib_common.schema import Dividend, Snapshot
from .findings import Finding, grade

DIM = "dividends"


def income_by_symbol(dividends: list[Dividend]) -> dict[str, dict]:
    """Aggregate gross/tax/net income per symbol (keeps native currency)."""
    agg: dict[str, dict] = {}
    for d in dividends:
        row = agg.setdefault(d.symbol, {"gross": 0.0, "tax": 0.0, "net": 0.0,
                                        "currency": d.currency})
        row["gross"] += d.gross
        row["tax"] += d.tax
        row["net"] += d.gross - d.tax
    return agg


def yield_on_cost(dividends: list[Dividend], snapshot: Snapshot) -> dict[str, float]:
    """Net dividend income / cost basis, only for currently held symbols."""
    inc = income_by_symbol(dividends)
    cost = {p.symbol: p.quantity * p.avg_cost for p in snapshot.positions}
    out: dict[str, float] = {}
    for sym, row in inc.items():
        basis = cost.get(sym)
        if basis and basis > 0:
            out[sym] = row["net"] / basis
    return out


def analyze(dividends: list[Dividend], snapshot: Snapshot, thresholds: dict) -> list[Finding]:
    """Return dividend findings: best held Yield-on-Cost + portfolio tax drag."""
    if not dividends:
        return []
    findings: list[Finding] = []

    yoc = yield_on_cost(dividends, snapshot)
    if yoc:
        sym, val = max(yoc.items(), key=lambda kv: kv[1])
        findings.append(Finding(
            priority=grade(val, thresholds["yield_on_cost_warn"],
                           thresholds["yield_on_cost_crit"], higher_is_worse=False),
            dimension=DIM,
            finding=f"{sym} yield on cost is {val:.2%}",
            evidence={"symbol": sym, "yield_on_cost": round(val, 4)},
            impact="yield on cost shows income return against what you paid, not market price",
            suggestion="compare against your income objective for this holding",
            trigger_condition=f"yield on cost <= {thresholds['yield_on_cost_warn']:.0%}",
            confidence=0.8,
            data_limitations="trailing realized dividends only; not a forward yield",
        ))

    gross = sum(d.gross for d in dividends)
    tax = sum(d.tax for d in dividends)
    drag = tax / gross if gross else 0.0
    findings.append(Finding(
        priority=grade(drag, thresholds["withholding_drag_warn"],
                       thresholds["withholding_drag_crit"]),
        dimension=DIM,
        finding=f"Withholding tax is {drag:.1%} of gross dividend income",
        evidence={"gross": round(gross, 2), "tax": round(tax, 2), "drag": round(drag, 4)},
        impact="tax withholding reduces the income you actually keep",
        suggestion="review whether treaty rates or account structure could lower withholding",
        trigger_condition=f"withholding drag >= {thresholds['withholding_drag_warn']:.0%}",
        confidence=0.85,
        data_limitations="reflects taxes recorded in Flex; reclaim/treaty effects not modeled. "
                         "v1 assumes a single reporting currency and does not group or "
                         "FX-convert across currencies",
    ))
    return findings
