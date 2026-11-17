"""Diagnostic module 4: trade review (activity + execution cost).

v1 focuses on the most robust, always-available fact from executions:
commission drag in basis points of traded notional. Win-rate and holding
period need round-trip pairing and are deferred to a later iteration.
"""
from __future__ import annotations
from ib_common.schema import Execution
from .findings import Finding, grade

DIM = "trade_review"


def summarize(executions: list[Execution]) -> dict:
    """Aggregate trade counts, notional by side, and commission drag (bps)."""
    buy_notional = sum(e.quantity * e.price for e in executions if e.side.upper().startswith("B"))
    sell_notional = sum(e.quantity * e.price for e in executions if e.side.upper().startswith("S"))
    total_notional = buy_notional + sell_notional
    total_commission = sum(e.commission for e in executions)
    commission_bps = (total_commission / total_notional * 1e4) if total_notional else 0.0
    return {
        "n_trades": len(executions),
        "buy_notional": buy_notional,
        "sell_notional": sell_notional,
        "total_commission": total_commission,
        "commission_bps": commission_bps,
    }


def analyze(executions: list[Execution], thresholds: dict) -> list[Finding]:
    """Return trade-review findings: commission drag on traded notional."""
    if not executions:
        return []
    s = summarize(executions)
    p = grade(s["commission_bps"],
              thresholds["commission_bps_warn"], thresholds["commission_bps_crit"])
    return [Finding(
        priority=p, dimension=DIM,
        finding=f"Commissions cost {s['commission_bps']:.1f} bps of traded notional",
        evidence=s,
        impact="high per-trade cost erodes returns, especially on small tickets",
        suggestion="review order sizing and whether trade frequency is justified",
        trigger_condition=f"commission drag >= {thresholds['commission_bps_warn']} bps",
        confidence=0.9,
        data_limitations="reqExecutions only reaches ~7 days; use Flex for full history",
    )]
