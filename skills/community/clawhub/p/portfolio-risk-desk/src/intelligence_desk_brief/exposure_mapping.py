"""Exposure mapping builders for Order 03."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.source_taxonomy import TEMPLATE_FACTORS, lane_weight, source_quality_value

EXPOSURE_TITLES = {
    "AI capex and infrastructure sensitivity": "AI infrastructure concentration",
    "Semiconductor demand and inventory cycle exposure": "Semiconductor cycle exposure",
    "Rates and multiple compression sensitivity": "Valuation sensitivity to rates",
    "China, regulation, or policy exposure": "Policy and geographic exposure",
    "Supply-chain concentration or foundry dependence": "Shared supply-chain dependency",
    "Earnings revision sensitivity": "Earnings execution sensitivity",
}


def build_exposure_outputs(
    request: CreateBriefRequest,
    evidence: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    grouped = _group_by_factor(evidence)
    scored_groups = sorted(grouped.values(), key=_group_rank, reverse=True)

    current_exposure_map = [
        _build_exposure_entry(group)
        for group in scored_groups[:3]
    ]

    if not current_exposure_map:
        current_exposure_map = [
            {
                "name": "No differentiated portfolio exposure yet",
                "names": request.holdings or request.watchlist,
                "assessment": "The current evidence set does not yet support a differentiated exposure map.",
                "confidence": "low",
                "assumptions": "Re-check with fresher primary company, policy, or competitor evidence.",
            }
        ]

    dominant_factors = [_build_dominant_factor_entry(grouped.get(factor), factor) for factor in TEMPLATE_FACTORS]
    return current_exposure_map, dominant_factors


def _group_by_factor(evidence: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for item in evidence:
        if item["item_type"] != "evidence":
            continue
        factor = item["factor"]
        bucket = grouped.setdefault(
            factor,
            {
                "factor": factor,
                "items": [],
                "names": set(),
                "source_lanes": set(),
            },
        )
        bucket["items"].append(item)
        bucket["names"].update(item.get("affected_names", []))
        bucket["source_lanes"].add(item.get("source_lane", "other"))
    return grouped


def _group_rank(group: dict[str, Any]) -> int:
    total = 0
    for item in group["items"]:
        total += max(int(item["ranking"]["score"]), 0)
        total += lane_weight(item) * 6
        total += source_quality_value(item["source_quality"]) * 4
    return total


def _build_exposure_entry(group: dict[str, Any]) -> dict[str, Any]:
    top_item = _top_item(group)
    factor = group["factor"]
    source_lanes = sorted(group["source_lanes"])
    corroboration = top_item["corroboration_status"]

    assessment = top_item["interpretation"]
    if corroboration == "corroborated" and len(group["items"]) > 1:
        assessment = (
            f"{assessment} This view is supported across {', '.join(source_lanes)} evidence "
            "rather than a single isolated item."
        )
    elif top_item["source_lane"] == "x_commentary":
        assessment = f"{assessment} This remains early narrative evidence and still needs primary-source confirmation."

    assumptions = top_item["watchpoint"]
    if top_item["source_lane"] in {"curated_analysis", "x_commentary"}:
        assumptions = "Needs confirmation from company disclosures, filings, or official commentary."

    return {
        "name": EXPOSURE_TITLES.get(factor, factor),
        "names": sorted(group["names"]),
        "assessment": assessment,
        "confidence": _group_confidence(group["items"]),
        "assumptions": assumptions,
    }


def _build_dominant_factor_entry(group: dict[str, Any] | None, factor: str) -> dict[str, Any]:
    if not group:
        return {
            "factor": factor,
            "stance": "watch",
            "impact_summary": "No direct ranked evidence in the current lookback window.",
        }

    top_item = _top_item(group)
    summary = top_item["interpretation"]
    if top_item["source_lane"] == "policy":
        summary = f"{summary} Policy-sensitive evidence is now part of the active risk map."
    elif top_item["source_lane"] == "competitor":
        summary = f"{summary} Competitor and ecosystem evidence is shaping this factor."
    elif top_item["source_lane"] in {"curated_analysis", "hedge_fund_primary"}:
        summary = f"{summary} Investor analysis is informing interpretation, but the brief still prioritizes direct evidence."

    return {
        "factor": factor,
        "stance": top_item.get("change_label", "watch"),
        "impact_summary": summary,
        "supporting_evidence_ids": [item["id"] for item in group["items"][:3]],
        "confidence_reason": _dominant_factor_confidence_reason(group["items"]),
    }


def _group_confidence(items: list[dict[str, Any]]) -> str:
    score = 0
    for item in items[:3]:
        score += source_quality_value(item["source_quality"]) * 2
        score += lane_weight(item)
        score += int(item["confidence_value"])
        if item["corroboration_status"] == "corroborated":
            score += 2
        if item["corroboration_status"] == "conflicting":
            score -= 2
    if score >= 18:
        return "high"
    if score >= 10:
        return "medium"
    return "low"


def _dominant_factor_confidence_reason(items: list[dict[str, Any]]) -> str:
    top_item = items[0]
    if top_item["corroboration_status"] == "corroborated":
        return "The factor is backed by corroborated evidence across multiple ranked items."
    if top_item["source_lane"] == "x_commentary":
        return "Confidence stays low because the factor currently leans on narrative evidence without primary confirmation."
    return (
        f"The factor is led by {top_item['source_quality']} evidence in the {top_item['source_lane']} lane, "
        "but still needs broader confirmation."
    )


def _top_item(group: dict[str, Any]) -> dict[str, Any]:
    return sorted(
        group["items"],
        key=lambda item: (
            source_quality_value(item["source_quality"]),
            lane_weight(item),
            item["ranking"]["score"],
        ),
        reverse=True,
    )[0]
