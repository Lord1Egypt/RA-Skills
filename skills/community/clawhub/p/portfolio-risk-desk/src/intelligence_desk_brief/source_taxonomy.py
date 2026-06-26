"""Source-lane classification and weighting for synthesis."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from intelligence_desk_brief.contracts import CreateBriefRequest

TEMPLATE_FACTORS = [
    "AI capex and infrastructure sensitivity",
    "Semiconductor demand and inventory cycle exposure",
    "Rates and multiple compression sensitivity",
    "China, regulation, or policy exposure",
    "Supply-chain concentration or foundry dependence",
    "Earnings revision sensitivity",
]

SOURCE_LANE_WEIGHTS = {
    "earnings_primary": 4,
    "company_primary": 4,
    "hedge_fund_primary": 3,
    "policy": 3,
    "competitor": 3,
    "macro": 2,
    "curated_analysis": 2,
    "other": 1,
    "x_commentary": 0,
}

SOURCE_QUALITY_VALUES = {"high": 3, "medium": 2, "low": 1}
POSITIVE_CHANGE_LABELS = {"strengthened", "improving", "improved", "positive", "upside"}
NEGATIVE_CHANGE_LABELS = {"weakened", "deteriorated", "negative", "downside", "pressure"}


def classify_evidence(
    items: list[dict[str, Any]],
    request: CreateBriefRequest,
) -> list[dict[str, Any]]:
    """Attach lane-aware synthesis metadata to ranked evidence."""

    factor_counts = Counter(item["factor"] for item in items if item["item_type"] == "evidence")
    factor_lane_sets: dict[str, set[str]] = defaultdict(set)
    factor_direction_sets: dict[str, set[str]] = defaultdict(set)

    provisional: list[dict[str, Any]] = []
    for item in items:
        if item["item_type"] != "evidence":
            provisional.append(dict(item))
            continue

        source_lane = infer_source_lane(item)
        factor_lane_sets[item["factor"]].add(source_lane)
        factor_direction_sets[item["factor"]].add(_direction_for_change(item.get("change_label", "")))

        enriched = dict(item)
        enriched["source_lane"] = source_lane
        provisional.append(enriched)

    classified: list[dict[str, Any]] = []
    for item in provisional:
        if item["item_type"] != "evidence":
            classified.append(item)
            continue

        source_lane = item["source_lane"]
        enriched = dict(item)
        enriched["source_quality"] = infer_source_quality(enriched)
        enriched["entity_type"] = infer_entity_type(enriched, request)
        enriched["corroboration_status"] = infer_corroboration_status(
            enriched,
            factor_counts,
            factor_lane_sets,
            factor_direction_sets,
        )
        enriched["lane_weight"] = SOURCE_LANE_WEIGHTS.get(source_lane, 1)
        classified.append(enriched)
    return classified


def infer_source_lane(item: dict[str, Any]) -> str:
    source_type = str(item.get("source_type") or item.get("source", {}).get("type") or "").lower()
    category = str(item.get("category") or "").lower()
    text = _text_blob(item)
    url = str(item.get("source", {}).get("url") or item.get("url") or "").lower()

    if item.get("is_x_signal") or source_type.startswith("x") or category == "x_signals":
        return "x_commentary"

    if "policy" in category or "policy" in source_type or _has_any(text + " " + url, ["whitehouse.gov", "commerce.gov", "treasury.gov", "ustr.gov", "europa.eu", "policy", "tariff", "export control", "regulation", "sanction", "antitrust"]):
        return "policy"

    if category == "macro" or _has_any(text, ["fed", "yield", "rates", "macro", "inflation", "treasury", "cpi"]):
        return "macro"

    if _has_any(source_type + " " + category, ["earnings", "filing", "investor_relations"]) or _has_any(
        text + " " + url,
        ["earnings", "guidance", "10-q", "10-k", "8-k", "sec.gov", "investor relations", "shareholder letter"],
    ):
        if _has_any(text + " " + url, ["earnings", "guidance", "10-q", "10-k", "8-k"]):
            return "earnings_primary"
        return "company_primary"

    if category == "investor_analysis" or _has_any(
        source_type + " " + category + " " + text,
        ["analysis", "research note", "curated", "publisher", "barron's", "wsj", "ft.com", "bloomberg", "reuters breakingviews"],
    ):
        return "curated_analysis"

    if _has_any(source_type + " " + category, ["hedge_fund_primary", "hedge_fund_analysis"]) or _has_any(
        text + " " + url,
        ["13f", "shareholder letter", "investor letter", "hedge fund", "activist", "pershing square", "elliott", "coatue", "viking", "third point"],
    ):
        return "hedge_fund_primary"

    if category in {"peer", "competitor", "supply_chain"} or "peer" in category or _has_any(
        text,
        ["competitor", "peer", "rival", "supplier", "customer", "inventory digestion", "pricing", "capacity", "foundry", "lithography"],
    ):
        return "competitor"

    return "other"


def infer_source_quality(item: dict[str, Any]) -> str:
    if item.get("low_quality"):
        return "low"

    source_lane = item.get("source_lane", "other")
    raw_reference = item.get("raw_reference")
    author = raw_reference.get("author", {}) if isinstance(raw_reference, dict) and isinstance(raw_reference.get("author"), dict) else {}
    url = str(item.get("source", {}).get("url") or item.get("url") or "").lower()

    if source_lane in {"earnings_primary", "company_primary", "hedge_fund_primary"}:
        return "high"
    if source_lane == "policy":
        return "high" if url.endswith(".gov") or ".gov/" in url or "europa.eu" in url else "medium"
    if source_lane == "competitor":
        return "high" if item.get("confidence_level") == "high" else "medium"
    if source_lane == "macro":
        return "medium"
    if source_lane == "curated_analysis":
        return "medium"
    if source_lane == "x_commentary":
        if item.get("source_type") == "x_official" or author.get("verified") or author.get("is_blue_verified"):
            return "medium"
        return "low"
    return "medium" if item.get("confidence_level") in {"medium", "high"} else "low"


def infer_entity_type(item: dict[str, Any], request: CreateBriefRequest) -> str:
    source_lane = item.get("source_lane", "other")
    text = _text_blob(item)

    if source_lane == "policy":
        return "policymaker"
    if source_lane in {"hedge_fund_primary", "curated_analysis"}:
        return "investor"
    if source_lane == "x_commentary":
        return "commentator"
    if source_lane == "competitor":
        if _has_any(text, ["supplier", "foundry", "equipment", "lithography", "capacity"]):
            return "supplier"
        if _has_any(text, ["customer", "buyer", "hyperscaler", "order"]):
            return "customer"
        return "competitor"

    tracked = {symbol.upper() for symbol in request.holdings + request.watchlist}
    affected = {name.upper() for name in item.get("affected_names", [])}
    if tracked & affected:
        return "holding"
    return "other"


def infer_corroboration_status(
    item: dict[str, Any],
    factor_counts: Counter[str],
    factor_lane_sets: dict[str, set[str]],
    factor_direction_sets: dict[str, set[str]],
) -> str:
    factor = item["factor"]
    directions = factor_direction_sets.get(factor, {"neutral"})
    if "positive" in directions and "negative" in directions:
        return "conflicting"

    if factor_counts.get(factor, 0) > 1 and len(factor_lane_sets.get(factor, set())) > 1:
        return "corroborated"

    if factor_counts.get(factor, 0) > 1 and item.get("source_quality") == "high":
        return "corroborated"

    return "single_source"


def source_quality_value(label: str) -> int:
    return SOURCE_QUALITY_VALUES.get(label, 1)


def lane_weight(item: dict[str, Any]) -> int:
    return int(item.get("lane_weight") or SOURCE_LANE_WEIGHTS.get(item.get("source_lane", "other"), 1))


def _direction_for_change(label: str) -> str:
    lowered = label.strip().lower()
    if lowered in POSITIVE_CHANGE_LABELS:
        return "positive"
    if lowered in NEGATIVE_CHANGE_LABELS:
        return "negative"
    return "neutral"


def _text_blob(item: dict[str, Any]) -> str:
    parts = [
        item.get("source_title"),
        item.get("source", {}).get("title") if isinstance(item.get("source"), dict) else "",
        item.get("source_type"),
        item.get("category"),
        item.get("fact"),
        item.get("interpretation"),
        item.get("why_it_matters"),
        item.get("watchpoint"),
    ]
    return " ".join(str(part).lower() for part in parts if part)


def _has_any(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return any(needle in lowered for needle in needles)
