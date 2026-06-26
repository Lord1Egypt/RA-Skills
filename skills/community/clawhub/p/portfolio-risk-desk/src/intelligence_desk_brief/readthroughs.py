"""Driver and read-through builders for Order 03."""

from __future__ import annotations

from typing import Any

from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.source_taxonomy import lane_weight, source_quality_value


def build_driver_readthroughs(
    request: CreateBriefRequest,
    evidence: list[dict[str, Any]],
    *,
    limit: int = 5,
) -> list[dict[str, Any]]:
    del request
    candidates = [
        item
        for item in evidence
        if item["item_type"] == "evidence"
        and not item.get("low_quality")
        and (
            item["direct_relevance"]
            or item["watchlist_relevance"]
            or item["cross_name_impact"] > 1
            or item["source_lane"] in {"policy", "competitor", "curated_analysis", "hedge_fund_primary"}
        )
    ]

    ordered = sorted(candidates, key=_driver_rank, reverse=True)
    selected: list[dict[str, Any]] = []
    seen_keys: set[tuple[str, tuple[str, ...]]] = set()

    for item in ordered:
        key = (item["factor"], tuple(sorted(item.get("affected_names", []))))
        if key in seen_keys:
            continue
        seen_keys.add(key)
        selected.append(
            {
                "driver": item["factor"],
                "affected_names": item["affected_names"],
                "first_order_effect": item["fact"],
                "second_order_readthrough": _second_order_readthrough(item),
                "confidence": _driver_confidence(item),
                "confidence_reason": _driver_confidence_reason(item),
                "evidence_quality": f"{item['source_quality']} ({item['source_lane']})",
                "supporting_evidence_ids": [item["id"]],
                "ranking_score": item["ranking"]["score"],
            }
        )
        if len(selected) == limit:
            break

    return selected


def _driver_rank(item: dict[str, Any]) -> int:
    score = int(item["ranking"]["score"])
    score += lane_weight(item) * 8
    score += source_quality_value(item["source_quality"]) * 5
    if item["corroboration_status"] == "corroborated":
        score += 10
    if item["source_lane"] == "x_commentary":
        score -= 12
    return score


def _driver_confidence(item: dict[str, Any]) -> str:
    score = int(item["confidence_value"]) + source_quality_value(item["source_quality"])
    if item["corroboration_status"] == "corroborated":
        score += 2
    if item["source_lane"] == "x_commentary":
        score -= 2
    if score >= 7:
        return "high"
    if score >= 4:
        return "medium"
    return "low"


def _driver_confidence_reason(item: dict[str, Any]) -> str:
    if item["corroboration_status"] == "corroborated":
        return "This driver is corroborated by more than one relevant evidence item."
    if item["source_lane"] == "x_commentary":
        return "This driver is being tracked, but confidence is limited because it is still commentary-led."
    return (
        f"This driver is supported by {item['source_quality']} evidence in the {item['source_lane']} lane, "
        "with room for additional confirmation."
    )


def _second_order_readthrough(item: dict[str, Any]) -> str:
    base = item["interpretation"]
    names = ", ".join(item.get("affected_names", []))
    if item["source_lane"] == "competitor":
        return f"{base} Competitor and ecosystem evidence now changes the read-through for {names}."
    if item["source_lane"] == "policy":
        return f"{base} Policy-sensitive exposure can now propagate across the portfolio through geography, compliance, and demand mix."
    if item["source_lane"] in {"hedge_fund_primary", "curated_analysis"}:
        return f"{base} Investor analysis is sharpening the thesis read-through, but it does not replace primary-source confirmation."
    if item["source_lane"] == "x_commentary":
        return f"{base} The narrative is worth monitoring, but it should not lead the portfolio view without corroboration."
    return base
