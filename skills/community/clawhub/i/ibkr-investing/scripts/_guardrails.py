"""Guardrails enforced at propose-time AND re-checked at execute-time.

Env vars:
    IBKR_ALLOWED_SYMBOLS              CSV of tickers; empty means "any".
    IBKR_MAX_NOTIONAL_USD_PER_TRADE   Per-trade ceiling (USD). Default 200.
    IBKR_MAX_DAILY_NOTIONAL_USD       Sum of executed USD notional today.
                                      Default 1000.
"""
from __future__ import annotations

import os

from _pending import today_notional_usd


class GuardrailError(Exception):
    pass


def _allowed_symbols() -> list[str]:
    raw = os.environ.get("IBKR_ALLOWED_SYMBOLS", "").strip()
    if not raw:
        return []
    return [s.strip().upper() for s in raw.split(",") if s.strip()]


def _max_per_trade() -> float:
    return float(os.environ.get("IBKR_MAX_NOTIONAL_USD_PER_TRADE", "200"))


def _max_daily() -> float:
    return float(os.environ.get("IBKR_MAX_DAILY_NOTIONAL_USD", "1000"))


def check_symbol(symbol: str) -> None:
    allowed = _allowed_symbols()
    if allowed and symbol.upper() not in allowed:
        raise GuardrailError(
            f"Symbol '{symbol}' not in IBKR_ALLOWED_SYMBOLS={allowed}. "
            f"Either add it or pick a different ticker."
        )


def check_notional(notional_usd: float) -> None:
    cap = _max_per_trade()
    if notional_usd > cap:
        raise GuardrailError(
            f"Notional ${notional_usd:.2f} exceeds IBKR_MAX_NOTIONAL_USD_PER_TRADE=${cap:.2f}. "
            f"Reduce the trade size or raise the cap."
        )


def check_daily_room(notional_usd: float) -> None:
    cap = _max_daily()
    used = today_notional_usd()
    if used + notional_usd > cap:
        raise GuardrailError(
            f"Today's executed notional is ${used:.2f}; adding ${notional_usd:.2f} would exceed "
            f"IBKR_MAX_DAILY_NOTIONAL_USD=${cap:.2f}. Try again tomorrow or raise the cap."
        )


def check_all(symbol: str, notional_usd: float) -> None:
    check_symbol(symbol)
    check_notional(notional_usd)
    check_daily_room(notional_usd)


def summary() -> str:
    allowed = _allowed_symbols()
    return (
        f"Guardrails: per-trade=${_max_per_trade():.2f}, daily=${_max_daily():.2f}, "
        f"used today=${today_notional_usd():.2f}, "
        f"allowed_symbols={allowed if allowed else 'ANY'}"
    )
