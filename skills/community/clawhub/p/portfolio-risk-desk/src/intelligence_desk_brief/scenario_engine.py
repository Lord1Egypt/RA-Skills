"""Scenario analysis builders for Order 03."""

from __future__ import annotations

import re
from typing import Any

from intelligence_desk_brief.contracts import CreateBriefRequest, ScenarioAnalysisItem
from intelligence_desk_brief.source_taxonomy import TEMPLATE_FACTORS, lane_weight, source_quality_value

SCENARIO_KEYWORDS = {
    "Rates and multiple compression sensitivity": ["rate", "rates", "yield", "fed", "multiple", "valuation"],
    "China, regulation, or policy exposure": ["china", "policy", "regulation", "tariff", "export", "restriction", "election"],
    "Supply-chain concentration or foundry dependence": ["foundry", "supply", "capacity", "bottleneck", "lithography", "supplier"],
    "Semiconductor demand and inventory cycle exposure": ["semiconductor", "chip", "inventory", "demand", "competitor", "peer"],
    "AI capex and infrastructure sensitivity": ["ai", "capex", "infrastructure", "cloud", "hyperscaler"],
    "Earnings revision sensitivity": ["earnings", "miss", "guide", "guidance", "revision"],
}

DEFAULT_SCENARIOS = [
    "What changes if rates move higher again?",
    "What breaks or holds if a major semiconductor name misses expectations?",
]

FACTOR_FALSIFIERS = {
    "Rates and multiple compression sensitivity": [
        "Bond yields retreat and policy commentary turns more dovish.",
        "Company commentary shows demand accelerating enough to offset valuation pressure.",
    ],
    "China, regulation, or policy exposure": [
        "Formal policy changes remain narrower than feared.",
        "Management commentary indicates limited direct revenue or supply-chain disruption.",
    ],
    "Supply-chain concentration or foundry dependence": [
        "Capacity additions and lead times improve faster than expected.",
        "Customer commentary shows bottlenecks easing without delivery slippage.",
    ],
    "Semiconductor demand and inventory cycle exposure": [
        "Weakness remains isolated to one end market rather than spreading across the chain.",
        "Inventory normalization broadens without a wider pricing reset.",
    ],
    "AI capex and infrastructure sensitivity": [
        "Hyperscaler or enterprise capex commentary softens materially.",
        "Orders, backlog, or customer commentary fail to confirm the demand signal.",
    ],
    "Earnings revision sensitivity": [
        "Management guidance stabilizes and estimate cuts stop broadening.",
        "Downside commentary does not translate into follow-on revisions across peers.",
    ],
}


def build_scenarios(
    request: CreateBriefRequest,
    evidence: list[dict[str, Any]],
) -> list[ScenarioAnalysisItem]:
    scenario_questions = request.scenario_questions or DEFAULT_SCENARIOS
    built: list[ScenarioAnalysisItem] = []

    for question in scenario_questions:
        factors = _match_factors(question)
        matching_items = [
            item
            for item in evidence
            if item["item_type"] == "evidence" and item["factor"] in factors
        ]
        ordered_items = sorted(matching_items, key=_scenario_rank, reverse=True)
        supporting_items = ordered_items[:3]
        affected_names = _scenario_names(supporting_items, request)

        built.append(
            ScenarioAnalysisItem(
                scenario=_scenario_title(question),
                confidence_level=_scenario_confidence(supporting_items),
                confidence_reason=_scenario_confidence_reason(supporting_items),
                breaks_or_holds=_breaks_or_holds(question, supporting_items, factors),
                affected_names=affected_names,
                supporting_evidence_ids=[item["id"] for item in supporting_items],
                supporting_evidence=[item["source"] for item in supporting_items],
                falsifiers=_falsifiers_for(factors),
            )
        )

    return built


def _match_factors(question: str) -> list[str]:
    lowered = question.lower()
    matched = [
        factor
        for factor, keywords in SCENARIO_KEYWORDS.items()
        if any(_matches_keyword(lowered, keyword) for keyword in keywords)
    ]
    return matched or TEMPLATE_FACTORS[:2]


def _scenario_rank(item: dict[str, Any]) -> int:
    score = int(item["ranking"]["score"])
    score += lane_weight(item) * 6
    score += source_quality_value(item["source_quality"]) * 4
    if item["corroboration_status"] == "corroborated":
        score += 8
    if item["source_lane"] == "x_commentary" and item["corroboration_status"] != "corroborated":
        score -= 10
    return score


def _scenario_confidence(items: list[dict[str, Any]]) -> str:
    if not items:
        return "low"

    score = 0
    for item in items:
        score += source_quality_value(item["source_quality"]) * 2
        score += int(item["confidence_value"])
        score += lane_weight(item)
        if item["corroboration_status"] == "corroborated":
            score += 2
        if item["corroboration_status"] == "conflicting":
            score -= 2
        if item["source_lane"] == "x_commentary" and item["corroboration_status"] != "corroborated":
            score -= 2
    if score >= 16:
        return "high"
    if score >= 8:
        return "medium"
    return "low"


def _scenario_confidence_reason(items: list[dict[str, Any]]) -> str:
    if not items:
        return "Confidence is low because the current scenario is not backed by primary or corroborated evidence yet."
    top = items[0]
    if top["corroboration_status"] == "corroborated":
        return (
            f"Confidence is anchored by {top['source_quality']} evidence and corroboration across "
            f"{min(len(items), 3)} supporting items."
        )
    if top["source_lane"] == "x_commentary":
        return "Confidence is capped because the scenario still leans on narrative or commentary rather than primary confirmation."
    return (
        f"Confidence reflects {top['source_quality']} evidence led by the {top['source_lane']} lane, "
        "but there is still limited corroboration."
    )


def _scenario_names(items: list[dict[str, Any]], request: CreateBriefRequest) -> list[str]:
    names: list[str] = []
    for item in items:
        for name in item.get("affected_names", []):
            if name not in names:
                names.append(name)
    return names or request.holdings or request.watchlist


def _breaks_or_holds(
    question: str,
    items: list[dict[str, Any]],
    factors: list[str],
) -> list[str]:
    if not items:
        return [
            f"Evidence is still too thin to support a strong answer to '{question.rstrip('?')}'.",
            "Treat this as a watch scenario until primary company, policy, or competitor evidence improves.",
        ]

    lines = [items[0]["interpretation"]]
    if len(items) > 1:
        lines.append(items[1]["interpretation"])
    else:
        lines.append(_default_second_line(factors[0]))
    return lines


def _default_second_line(factor: str) -> str:
    if factor == "Rates and multiple compression sensitivity":
        return "Higher-for-longer rates would likely pressure the highest-duration names first."
    if factor == "China, regulation, or policy exposure":
        return "The most exposed names would be the ones with the most visible geographic or compliance dependence."
    if factor == "Supply-chain concentration or foundry dependence":
        return "Shared bottlenecks would likely spread through peers, suppliers, and dependent customers."
    if factor == "Semiconductor demand and inventory cycle exposure":
        return "Weakness would likely show up first in the more cyclical parts of the semiconductor chain."
    if factor == "AI capex and infrastructure sensitivity":
        return "The portfolio would stay most resilient where demand is still tied to durable AI build-out spending."
    return "Estimate or sentiment pressure would likely spread first to the most exposed names."


def _falsifiers_for(factors: list[str]) -> list[str]:
    for factor in factors:
        if factor in FACTOR_FALSIFIERS:
            return FACTOR_FALSIFIERS[factor]
    return [
        "Primary-source evidence fails to confirm the scenario.",
        "Subsequent company, policy, or competitor commentary points in the opposite direction.",
    ]


def _scenario_title(question: str) -> str:
    cleaned = question.strip().rstrip("?")
    for prefix in ("What changes if ", "What breaks or holds if ", "What happens if "):
        if cleaned.lower().startswith(prefix.lower()):
            return cleaned[len(prefix):].strip().capitalize()
    return cleaned


def _matches_keyword(text: str, keyword: str) -> bool:
    if " " in keyword:
        return keyword in text
    return bool(re.search(rf"\b{re.escape(keyword)}\b", text))
