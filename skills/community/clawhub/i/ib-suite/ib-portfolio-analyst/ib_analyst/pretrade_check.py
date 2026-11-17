# skills/ib-portfolio-analyst/ib_analyst/pretrade_check.py
"""Diagnostic module 6: pre-trade risk check (v1 local simulation).

v1 estimates the post-trade single-name weight and gross leverage purely
from the local snapshot — it never contacts IB and never places an order.

v2 (deferred): replace the local estimate with a real IB WhatIf order
(`whatIfOrder`) to read the broker's exact margin impact. That requires the
order API and is intentionally out of the read-only v1 scope.
"""
from __future__ import annotations
from ib_common.schema import Snapshot
from .findings import Finding, grade

DIM = "pretrade_check"


def simulate(snapshot: Snapshot, symbol: str, side: str, quantity: float,
             price: float, thresholds: dict) -> list[Finding]:
    """Estimate post-trade concentration + leverage locally (no IB call)."""
    signed_qty = quantity if side.upper().startswith("B") else -quantity
    delta_value = signed_qty * price

    # rebuild gross exposure with the hypothetical fill (existing rows in base ccy)
    values = {p.symbol: p.base_value for p in snapshot.positions}
    values[symbol] = values.get(symbol, 0.0) + delta_value
    gross = sum(abs(v) for v in values.values()) or 1.0
    nlv = snapshot.account.net_liquidation or 1.0

    new_weight = abs(values[symbol]) / gross
    new_leverage = gross / nlv
    limit_note = "local estimate only; no IB WhatIf margin call in v1"

    findings: list[Finding] = []
    findings.append(Finding(
        priority=grade(new_weight, thresholds["single_position_weight_warn"],
                       thresholds["single_position_weight_crit"]),
        dimension=DIM,
        finding=f"After this trade {symbol} would be {new_weight:.1%} of gross exposure",
        evidence={"symbol": symbol, "post_trade_weight": round(new_weight, 4),
                  "delta_value": delta_value},
        impact="the trade shifts single-name concentration",
        suggestion="compare post-trade weight against your max single-name limit",
        trigger_condition=f"post-trade weight >= {thresholds['single_position_weight_warn']:.0%}",
        confidence=0.6,
        data_limitations=limit_note,
    ))
    findings.append(Finding(
        priority=grade(new_leverage, thresholds["leverage_warn"], thresholds["leverage_crit"]),
        dimension=DIM,
        finding=f"After this trade gross leverage would be {new_leverage:.2f}x",
        evidence={"post_trade_leverage": round(new_leverage, 3), "delta_value": delta_value},
        impact="the trade changes overall leverage and margin sensitivity",
        suggestion="verify post-trade leverage stays within your risk budget",
        trigger_condition=f"post-trade leverage >= {thresholds['leverage_warn']}x",
        confidence=0.6,
        data_limitations=limit_note,
    ))
    return findings
