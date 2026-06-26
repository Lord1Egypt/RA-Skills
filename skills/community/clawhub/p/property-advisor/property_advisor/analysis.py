from __future__ import annotations

import re
from statistics import median
from typing import Any


PLACEHOLDER_IMAGE_HINTS = ("carddefault", "placeholder", "default", "no-image")


def safe_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()


def unique_strings(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        text = safe_text(item)
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def parse_price_text(price_text: str | None) -> dict[str, Any]:
    text = safe_text(price_text)
    if not text:
        return {
            "raw": price_text,
            "value": None,
            "monthly_value": None,
            "currency": None,
            "period": None,
            "rent_or_sale": None,
        }
    lowered = text.lower()
    match = re.search(r"(?P<value>\d[\d,]*(?:\.\d+)?)", text.replace(",", ""))
    value = float(match.group("value")) if match else None
    currency = None
    for token in ("A$", "AUD", "S$", "SGD", "HK$", "HKD", "AED", "USD", "NZ$", "NZD", "GBP", "£", "¥", "JPY", "RMB", "CNY", "$"):
        if token.lower() in lowered:
            currency = token
            break
    period = None
    if any(token in lowered for token in ("/wk", " per week", "weekly", "/pw", " week")) or re.search(r"(?<![a-z])pw\b", lowered):
        period = "week"
    elif any(token in lowered for token in ("/mo", " per month", "monthly", " pcm", " month")) or re.search(r"(?<![a-z])pm\b", lowered):
        period = "month"
    elif any(token in lowered for token in ("/yr", " per year", "yearly", "annual", " p.a")):
        period = "year"
    rent_or_sale = "rent"
    monthly_value = None
    if value is not None:
        if period == "week":
            monthly_value = round(value * 4.33, 2)
        elif period == "month":
            monthly_value = round(value, 2)
        elif period == "year":
            monthly_value = round(value / 12, 2)
        elif value >= 100000:
            rent_or_sale = "sale"
        else:
            monthly_value = round(value, 2)
    if value is not None and value >= 100000 and period is None:
        rent_or_sale = "sale"
        monthly_value = None
    return {
        "raw": price_text,
        "value": value,
        "monthly_value": monthly_value,
        "currency": currency,
        "period": period,
        "rent_or_sale": rent_or_sale,
    }


def extract_bedrooms(*values: str | None) -> float | None:
    combined = " ".join(safe_text(value) for value in values if safe_text(value))
    lowered = combined.lower()
    if "studio" in lowered:
        return 0.0
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:bed|bedroom|br|居室|室)", lowered)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def has_placeholder_image(images: list[str]) -> bool:
    for image in images:
        lowered = safe_text(image).lower()
        if not lowered:
            continue
        if any(token in lowered for token in PLACEHOLDER_IMAGE_HINTS):
            return True
    return False


def price_context(snapshots: list[Any]) -> dict[str, Any]:
    values = [
        snapshot.monthly_price_value
        for snapshot in snapshots
        if getattr(snapshot, "monthly_price_value", None) is not None
    ]
    if not values:
        return {"median_monthly": None, "count": 0}
    return {"median_monthly": float(median(values)), "count": len(values)}


def detect_price_risk(monthly_value: float | None, peers: dict[str, Any]) -> list[str]:
    if monthly_value is None or peers.get("median_monthly") is None:
        return []
    median_monthly = peers["median_monthly"]
    risks: list[str] = []
    if monthly_value < median_monthly * 0.7:
        risks.append(f"价格显著低于样本中位数，当前月度等效价约 {monthly_value:.0f}，疑似异常低价或短租/合租。")
    elif monthly_value > median_monthly * 1.4:
        risks.append(f"价格明显高于样本中位数，当前月度等效价约 {monthly_value:.0f}，需确认是否有面积或配套优势。")
    return risks


def join_for_markdown(items: list[str]) -> str:
    values = unique_strings(items)
    return "<br>".join(values) if values else "无"


def compact_assessment(assessment: dict[str, Any] | None) -> str | None:
    if not assessment:
        return None
    conclusion = safe_text(assessment.get("conclusion"))
    evidence = assessment.get("evidence") or []
    if conclusion and evidence:
        return f"{conclusion} ({safe_text(evidence[0])})"
    return conclusion or safe_text(evidence[0]) if evidence else None
