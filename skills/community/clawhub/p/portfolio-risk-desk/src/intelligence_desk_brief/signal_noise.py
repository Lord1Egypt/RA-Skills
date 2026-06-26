"""Signal-versus-noise classification for Order 03."""

from __future__ import annotations

from typing import Any

from intelligence_desk_brief.source_taxonomy import lane_weight, source_quality_value


def build_signal_vs_noise(
    evidence: list[dict[str, Any]],
    scenarios: list[Any],
) -> list[dict[str, Any]]:
    del scenarios
    items = [item for item in evidence if item["item_type"] == "evidence"]
    ordered = sorted(
        items,
        key=lambda item: (_bucket_priority(_bucket_for(item)), _classification_rank(item)),
        reverse=True,
    )

    return [
        {
            "bucket": _bucket_for(item),
            "title": item["source"]["title"],
            "reason": _reason_for(item),
        }
        for item in ordered
    ]


def _classification_rank(item: dict[str, Any]) -> int:
    score = int(item["ranking"]["score"])
    score += lane_weight(item) * 6
    score += source_quality_value(item["source_quality"]) * 4
    if item["corroboration_status"] == "corroborated":
        score += 8
    if item["corroboration_status"] == "conflicting":
        score -= 5
    return score


def _bucket_for(item: dict[str, Any]) -> str:
    if item["corroboration_status"] == "conflicting":
        return "conflicting"
    if item.get("low_quality") or item["category"] == "market_chatter":
        return "noise"
    if item["source_lane"] == "x_commentary" and (
        item["source_quality"] == "low"
        or item["signal_strength"] == "low"
        or item["corroboration_status"] != "corroborated"
    ):
        return "noise"

    score = _classification_rank(item)
    if (
        score >= 70
        and item["source_quality"] == "high"
        and item["source_lane"] != "x_commentary"
    ):
        return "high_signal"
    if score >= 38:
        return "monitor"
    return "noise"


def _reason_for(item: dict[str, Any]) -> str:
    base = item["why_it_matters"]
    if item["source_lane"] == "x_commentary" and item["corroboration_status"] != "corroborated":
        return f"{base} This remains uncorroborated X commentary."
    if item["source_lane"] in {"hedge_fund_primary", "curated_analysis"}:
        return f"{base} Treat this as thesis-shaping analysis rather than a substitute for primary-source fact."
    if item["source_lane"] == "policy":
        return f"{base} Even unresolved policy evidence stays visible because it could materially change the risk map."
    if item["source_lane"] == "competitor":
        return f"{base} Competitor evidence matters because it can alter read-throughs across multiple holdings."
    if item["corroboration_status"] == "conflicting":
        return f"{base} The current evidence set points in different directions, so the tension stays visible."
    return base


def _bucket_priority(bucket: str) -> int:
    return {
        "high_signal": 4,
        "monitor": 3,
        "conflicting": 2,
        "noise": 1,
    }.get(bucket, 0)
