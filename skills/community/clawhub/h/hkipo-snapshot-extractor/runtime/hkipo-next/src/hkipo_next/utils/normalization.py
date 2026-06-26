"""Normalization helpers shared across services."""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any


def normalize_symbol(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.isdigit():
        return text.zfill(5)
    return text


def parse_date(value: Any) -> date | None:
    if value in (None, ""):
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()

    text = str(value).strip()
    if not text:
        return None
    text = text.replace("/", "-").replace("Z", "+00:00")
    try:
        if "T" in text or "+" in text:
            return datetime.fromisoformat(text).date()
        return date.fromisoformat(text.split()[0])
    except ValueError:
        return None


def parse_optional_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return None


def parse_price_range(value: Any) -> tuple[float | None, float | None]:
    if value in (None, ""):
        return (None, None)
    matches = re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?", str(value))
    if not matches:
        return (None, None)

    numbers = [float(match.replace(",", "")) for match in matches]
    if len(numbers) == 1:
        return (numbers[0], numbers[0])
    return (numbers[0], numbers[1])


def split_sponsors(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    text = str(value).strip()
    if not text:
        return []
    parts = re.split(r"[,;/、\n]+", text)
    return [part.strip() for part in parts if part.strip()]


def value_to_repr(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value)
