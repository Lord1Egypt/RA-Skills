"""Guardrails enforced at propose-time AND re-checked at execute-time.

Env vars:
    OKX_ALLOWED_SYMBOLS              CSV of instId values; empty means "any".
    OKX_MAX_NOTIONAL_USDT_PER_TRADE  Per-trade ceiling (USDT). Default 50.
    OKX_MAX_DAILY_NOTIONAL_USDT      Sum of executed USDT notional today.
                                     Default 200.

A breach raises GuardrailError. Propose scripts treat that as "refuse and
explain"; execute scripts treat it as "abort even if the user already said YES"
because circumstances may have changed since the proposal was created.
"""
from __future__ import annotations

import os

from _pending import today_notional_usdt


class GuardrailError(Exception):
    pass


def _allowed_symbols() -> list[str]:
    raw = os.environ.get("OKX_ALLOWED_SYMBOLS", "").strip()
    if not raw:
        return []
    return [s.strip() for s in raw.split(",") if s.strip()]


def _max_per_trade() -> float:
    return float(os.environ.get("OKX_MAX_NOTIONAL_USDT_PER_TRADE", "50"))


def _max_daily() -> float:
    return float(os.environ.get("OKX_MAX_DAILY_NOTIONAL_USDT", "200"))


def check_symbol(inst_id: str) -> None:
    allowed = _allowed_symbols()
    if allowed and inst_id not in allowed:
        raise GuardrailError(
            f"Symbol '{inst_id}' not in OKX_ALLOWED_SYMBOLS={allowed}. "
            f"Either add it or pick a different instrument."
        )


def check_notional(notional_usdt: float) -> None:
    cap = _max_per_trade()
    if notional_usdt > cap:
        raise GuardrailError(
            f"Notional ${notional_usdt:.2f} exceeds OKX_MAX_NOTIONAL_USDT_PER_TRADE=${cap:.2f}. "
            f"Reduce the trade size or raise the cap."
        )


def check_daily_room(notional_usdt: float) -> None:
    cap = _max_daily()
    used = today_notional_usdt()
    if used + notional_usdt > cap:
        raise GuardrailError(
            f"Today's executed notional is ${used:.2f}; adding ${notional_usdt:.2f} would exceed "
            f"OKX_MAX_DAILY_NOTIONAL_USDT=${cap:.2f}. Try again tomorrow or raise the cap."
        )


def check_all(inst_id: str, notional_usdt: float) -> None:
    check_symbol(inst_id)
    check_notional(notional_usdt)
    check_daily_room(notional_usdt)


def summary() -> str:
    allowed = _allowed_symbols()
    return (
        f"Guardrails: per-trade=${_max_per_trade():.2f}, daily=${_max_daily():.2f}, "
        f"used today=${today_notional_usdt():.2f}, "
        f"allowed_symbols={allowed if allowed else 'ANY'}"
    )
