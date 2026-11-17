"""Deterministic insurance cash-flow calculations."""

from __future__ import annotations

import math
from collections.abc import Iterable


def normalize_value(
    raw_value: float,
    raw_unit: str,
    *,
    basic_amount: float | None = None,
    annual_premium: float | None = None,
) -> float:
    """Normalize supported insurance-table units to CNY."""
    value = float(raw_value)
    if raw_unit == "CNY":
        return value
    if raw_unit == "CNY_per_10000_basic_amount":
        if basic_amount is None:
            raise ValueError("basic_amount is required for this unit")
        return value * float(basic_amount) / 10_000
    if raw_unit in {
        "CNY_per_1000_annual_premium",
        "basic_amount_CNY_per_1000_annual_premium",
    }:
        if annual_premium is None:
            raise ValueError("annual_premium is required for this unit")
        return value * float(annual_premium) / 1_000
    raise ValueError(f"Unsupported unit: {raw_unit}")


def _npv(rate: float, events: list[dict]) -> float:
    if rate <= -1:
        return math.inf
    return sum(float(event["amount"]) / ((1 + rate) ** float(event["time_years"])) for event in events)


def calculate_xirr(events: Iterable[dict], *, tolerance: float = 1e-9, max_iterations: int = 300) -> float | None:
    """Return annual effective IRR for decimal-year events using bracketed bisection.

    Returns None when cash flows do not contain both positive and negative values
    or when a root cannot be bracketed. A bracketed solver is used instead of
    Newton iteration so sparse insurance cash flows fail predictably.
    """
    items = sorted((dict(event) for event in events), key=lambda event: float(event["time_years"]))
    amounts = [float(event["amount"]) for event in items]
    if not items or not any(value < 0 for value in amounts) or not any(value > 0 for value in amounts):
        return None

    low = -0.999999
    high = 1.0
    low_value = _npv(low, items)
    high_value = _npv(high, items)
    while low_value * high_value > 0 and high < 1_000_000:
        high *= 2
        high_value = _npv(high, items)
    if not math.isfinite(low_value) or low_value * high_value > 0:
        return None

    for _ in range(max_iterations):
        midpoint = (low + high) / 2
        value = _npv(midpoint, items)
        if abs(value) <= tolerance or abs(high - low) <= tolerance:
            return midpoint
        if low_value * value <= 0:
            high = midpoint
        else:
            low = midpoint
            low_value = value
    return (low + high) / 2


def break_even_metrics(yearly_records: Iterable[dict]) -> dict:
    """Calculate three explicitly different nominal break-even definitions."""
    cumulative_premium = 0.0
    cumulative_distribution = 0.0
    surrender_year = None
    distribution_year = None
    final_maturity = 0.0

    for record in sorted(yearly_records, key=lambda item: int(item["policy_year"])):
        cumulative_premium += float(record.get("premium", 0) or 0)
        cumulative_distribution += float(record.get("cash_distribution", 0) or 0)
        cash_value = float(record.get("cash_value", 0) or 0)
        final_maturity = float(record.get("maturity_benefit", 0) or 0)
        if surrender_year is None and cumulative_distribution + cash_value >= cumulative_premium:
            surrender_year = int(record["policy_year"])
        if distribution_year is None and cumulative_distribution >= cumulative_premium:
            distribution_year = int(record["policy_year"])

    return {
        "surrender_break_even_year": surrender_year,
        "cash_distribution_break_even_year": distribution_year,
        "maturity_nominal_break_even": cumulative_distribution + final_maturity >= cumulative_premium,
    }


def validate_dividend_events(events: Iterable[dict], *, option: str) -> None:
    """Reject dividend cash-flow representations that would double count value."""
    event_types = {event.get("event") for event in events}
    if option == "accumulate" and {"annual_dividend", "accumulated_dividend"} <= event_types:
        raise ValueError("double count: accumulated dividends already include annual dividends")
    if option == "cash" and "accumulated_dividend" in event_types:
        raise ValueError("double count: cash dividend option cannot include accumulated dividends")
