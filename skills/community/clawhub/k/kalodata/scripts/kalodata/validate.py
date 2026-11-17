"""Client-side validation of KaloData request parameters."""

from __future__ import annotations

import datetime
import re

REGIONS = ("US", "GB", "ID", "TH", "VN", "PH", "MY", "SG", "JP", "MX", "DE", "IT", "FR", "ES", "BR")

_RANK_FIXED = ("lastDay", "last7Day", "last30Day")
_DETAIL_FIXED = _RANK_FIXED + ("last90Day", "last180Day", "last365Day")
_CATEGORY_FIXED = ("last7Day", "last30Day", "last90Day", "last180Day", "last365Day")

# tier -> (fixed values, custom-span max days or None, yyyy-MM allowed)
TIERS = {
    "rank": (_RANK_FIXED, 31, True),
    "detail": (_DETAIL_FIXED, 365, True),
    "category": (_CATEGORY_FIXED, None, False),
    "full": (_DETAIL_FIXED, 365, True),
}

_MONTH_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
_MINMAX_RE = re.compile(r"^\d+(\.\d+)?-\d+(\.\d+)?$")
_DIGITS_RE = re.compile(r"^\d+$")


def tier_hint(tier: str) -> str:
    fixed, span, month = TIERS[tier]
    parts = ["|".join(fixed)]
    if month:
        parts.append("yyyy-MM")
    if span:
        parts.append(f"yyyy-MM-dd~yyyy-MM-dd (≤{span} days)")
    return " | ".join(parts)


def check_date_range(value: str, tier: str) -> str | None:
    """Return an error message, or None if valid for the given tier."""
    fixed, span, month_ok = TIERS[tier]
    if value in fixed:
        return None
    if month_ok and _MONTH_RE.match(value):
        return None
    if "~" in value:
        if span is None:
            return f"custom date spans are not supported here; valid: {tier_hint(tier)}"
        lo, _, hi = value.partition("~")
        try:
            a = datetime.date.fromisoformat(lo)
            b = datetime.date.fromisoformat(hi)
        except ValueError:
            return f"invalid custom span '{value}'; expected yyyy-MM-dd~yyyy-MM-dd"
        if b < a:
            return f"custom span '{value}' ends before it starts"
        days = (b - a).days + 1
        if days > span:
            return f"custom span '{value}' covers {days} days; maximum here is {span}"
        return None
    return f"invalid --range '{value}'; valid: {tier_hint(tier)}"


def check_minmax(value: str, flag: str) -> str | None:
    """`min-max` with numeric ends on both sides."""
    if _MINMAX_RE.match(value):
        return None
    return (
        f"{flag} expects \"min-max\" with numeric ends (e.g. 1000-50000; "
        f"use 0 for no lower bound, a large number for no upper bound), got '{value}'"
    )


def check_numeric_id(value: str, flag: str) -> str | None:
    if _DIGITS_RE.match(value):
        return None
    return f"{flag} must be a numeric id, got '{value}'"


def clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, v))
