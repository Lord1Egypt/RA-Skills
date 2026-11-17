# skills/ib-portfolio-analyst/ib_analyst/account_health.py
"""Diagnostic module 1: account health (cash buffer + gross leverage).

Facts only: computes cash ratio and gross leverage from the snapshot and
grades them against configurable cutoffs. Wording/urgency come from the
Finding priority, not from prose here.
"""
from __future__ import annotations
from ib_common.schema import Snapshot
from .findings import Finding, Priority, grade

DIM = "account_health"


def analyze(snapshot: Snapshot, thresholds: dict) -> list[Finding]:
    """Return account-health findings: cash-ratio and leverage checks."""
    acct = snapshot.account
    nlv = acct.net_liquidation or 1.0
    gross = sum(abs(p.base_value) for p in snapshot.positions)   # base ccy, FX-converted
    cash_ratio = acct.total_cash / nlv
    leverage = gross / nlv

    findings: list[Finding] = []

    cash_p = grade(cash_ratio,
                   thresholds["cash_ratio_warn"], thresholds["cash_ratio_crit"],
                   higher_is_worse=False)
    findings.append(Finding(
        priority=cash_p, dimension=DIM,
        finding=f"Cash is {cash_ratio:.1%} of net liquidation",
        evidence={"cash_ratio": round(cash_ratio, 4),
                  "total_cash": acct.total_cash, "net_liquidation": nlv},
        impact="thin cash reduces ability to meet margin moves without forced selling",
        suggestion="review whether the cash buffer matches your margin volatility tolerance",
        trigger_condition=f"cash ratio <= {thresholds['cash_ratio_warn']:.0%}",
        confidence=0.95,
        data_limitations=f"values as of snapshot {acct.ts.isoformat()}",
    ))

    lev_p = grade(leverage, thresholds["leverage_warn"], thresholds["leverage_crit"])
    findings.append(Finding(
        priority=lev_p, dimension=DIM,
        finding=f"Gross leverage is {leverage:.2f}x net liquidation",
        evidence={"gross_exposure": gross, "net_liquidation": nlv,
                  "leverage": round(leverage, 3)},
        impact="higher leverage amplifies both drawdowns and margin sensitivity",
        suggestion="assess whether exposure is intentional and within your risk budget",
        trigger_condition=f"gross leverage >= {thresholds['leverage_warn']}x",
        confidence=0.95,
        data_limitations="market values use last-synced prices",
    ))
    return findings
