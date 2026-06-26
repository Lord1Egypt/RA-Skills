"""统一输出格式化工具"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))


def format_number(n: float | None, decimals: int = 2) -> str:
    if n is None:
        return "N/A"
    abs_n = abs(n)
    if abs_n >= 1_000_000_000_000:
        return f"${n / 1_000_000_000_000:.{decimals}f}T"
    if abs_n >= 1_000_000_000:
        return f"${n / 1_000_000_000:.{decimals}f}B"
    if abs_n >= 1_000_000:
        return f"${n / 1_000_000:.{decimals}f}M"
    if abs_n >= 1_000:
        return f"${n:,.{decimals}f}"
    return f"${n:.{decimals}f}"


def format_pct(pct: float | None) -> str:
    if pct is None:
        return "N/A"
    emoji = "🟢" if pct >= 0 else "🔴"
    return f"{emoji} {pct:+.2f}%"


def format_price(price: float | None, symbol: str = "") -> str:
    if price is None:
        return "N/A"
    if price >= 10000:
        return f"${price:,.0f}"
    if price >= 1:
        return f"${price:,.2f}"
    if price >= 0.01:
        return f"${price:.4f}"
    return f"${price:.8f}"


def now_bjt() -> str:
    return datetime.now(BJT).strftime("%Y-%m-%d %H:%M:%S")


def today_bjt() -> str:
    return datetime.now(BJT).strftime("%Y-%m-%d")


def tomorrow_bjt() -> str:
    return (datetime.now(BJT) + timedelta(days=1)).strftime("%Y-%m-%d")
