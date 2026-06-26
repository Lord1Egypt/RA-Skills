"""Evidence-driven synthesis for Order 03."""

from __future__ import annotations

from dataclasses import replace
from datetime import date
from typing import Any

from intelligence_desk_brief.contracts import (
    CreateBriefRequest,
    CreateBriefResponse,
    DeliveryStatus,
    UserFocus,
)
from intelligence_desk_brief.memory import MemoryContext, resolve_workspace_id
from intelligence_desk_brief.exposure_mapping import build_exposure_outputs
from intelligence_desk_brief.readthroughs import build_driver_readthroughs
from intelligence_desk_brief.scenario_engine import build_scenarios
from intelligence_desk_brief.signal_noise import build_signal_vs_noise
from intelligence_desk_brief.source_taxonomy import TEMPLATE_FACTORS, classify_evidence, lane_weight, source_quality_value


def _portfolio_scope(request: CreateBriefRequest) -> str:
    if request.holdings:
        return ", ".join(request.holdings)
    if request.watchlist:
        return ", ".join(request.watchlist)
    return "Theme-only desk view"


def _brief_objective(request: CreateBriefRequest) -> str:
    if request.brief_type.value == "daily":
        return "Daily review of what changed, why it matters, and what to monitor next."
    if request.brief_type.value == "earnings_reaction":
        return "Assess immediate portfolio implications from the latest earnings-related developments."
    return "On-demand risk brief that prioritizes the most relevant public-market changes."


def _factor_lens(evidence: list[dict[str, Any]]) -> list[str]:
    lens: list[str] = []
    for factor in TEMPLATE_FACTORS:
        if any(item["factor"] == factor for item in evidence):
            lens.append(factor)
    return lens


def build_brief(
    request: CreateBriefRequest,
    normalized_evidence: list[dict[str, Any]],
    memory_context: MemoryContext,
    *,
    as_of_date: date,
    delivery_status: DeliveryStatus,
) -> CreateBriefResponse:
    evidence_items = [item for item in normalized_evidence if item["item_type"] == "evidence"]
    retrieval_notices = [item for item in normalized_evidence if item["item_type"] != "evidence"]
    classified_evidence = classify_evidence(evidence_items, request)
    factor_lens = _factor_lens(classified_evidence)

    user_focus = UserFocus(
        portfolio_or_watchlist=_portfolio_scope(request),
        interested_industries=request.themes,
        brief_objective=_brief_objective(request),
        factor_lens=factor_lens,
        comparison_baseline=_comparison_baseline(request, memory_context),
        scenario_questions=request.scenario_questions,
    )

    current_exposure_map, dominant_factors = build_exposure_outputs(request, classified_evidence)
    key_drivers_and_readthroughs = build_driver_readthroughs(request, classified_evidence)
    scenario_analysis = build_scenarios(request, classified_evidence)
    signal_vs_noise = build_signal_vs_noise(classified_evidence, scenario_analysis)
    risk_map_changes = _build_risk_map_changes(
        classified_evidence,
        dominant_factors,
        key_drivers_and_readthroughs,
        memory_context,
    )
    watchpoints = _build_watchpoints(classified_evidence, memory_context)
    evidence_and_sources = _build_evidence_and_sources(classified_evidence)
    audit_trail = _build_audit_trail(
        classified_evidence,
        dominant_factors,
        risk_map_changes,
        key_drivers_and_readthroughs,
        scenario_analysis,
        watchpoints,
    )

    uncertainty_notes = [
        (
            "Live Apify retrieval is active, but this remains a bounded MVP evidence set."
            if any(item["provider"] == "apify" for item in classified_evidence)
            else "The Order 1 brief uses fixture-backed evidence, so the change map is representative rather than live."
        ),
        "Primary company materials outrank commentary and curated analysis when the brief forms the risk map.",
        "Broad X commentary is visible for awareness, but unsupported narrative spread is explicitly downgraded.",
    ]
    if memory_context.first_run:
        uncertainty_notes.append(
            "No prior brief context was recalled for this portfolio yet, so the change section uses a first-run baseline."
        )
    if memory_context.warning:
        uncertainty_notes.append(memory_context.warning)
    uncertainty_notes.extend(
        notice["fact"] for notice in retrieval_notices
    )

    summary = _build_summary(
        request,
        current_exposure_map,
        key_drivers_and_readthroughs,
        risk_map_changes,
        memory_context,
    )

    workspace_id = resolve_workspace_id(request)
    brief = CreateBriefResponse(
        brief_id=_build_brief_id(request, as_of_date),
        date=as_of_date.isoformat(),
        workspace_id=workspace_id,
        profile_id=request.profile_id,
        profile_name=request.profile_name,
        summary=summary,
        user_focus=user_focus,
        current_exposure_map=current_exposure_map,
        dominant_factors=dominant_factors,
        risk_map_changes=risk_map_changes,
        key_drivers_and_readthroughs=key_drivers_and_readthroughs,
        scenario_analysis=scenario_analysis,
        signal_vs_noise=signal_vs_noise,
        watchpoints=watchpoints,
        evidence_and_sources=evidence_and_sources,
        audit_trail=audit_trail,
        uncertainty_notes=uncertainty_notes,
        delivery_status=delivery_status,
        delivery_metadata=None,
    )
    return replace(brief)


def _build_brief_id(request: CreateBriefRequest, as_of_date: date) -> str:
    scope = request.profile_id or request.profile_name or resolve_workspace_id(request)
    normalized_scope = "".join(char.lower() if char.isalnum() else "-" for char in scope).strip("-")
    normalized_scope = normalized_scope or "workspace"
    return f"portfolio-risk-desk-{normalized_scope}-{as_of_date.isoformat()}"


def _build_summary(
    request: CreateBriefRequest,
    current_exposure_map: list[dict[str, Any]],
    drivers: list[dict[str, Any]],
    risk_map_changes: list[dict[str, Any]],
    memory_context: MemoryContext,
) -> str:
    lead_exposure = current_exposure_map[0] if current_exposure_map else None
    lead_driver = drivers[0] if drivers else None
    lead_change = risk_map_changes[0] if risk_map_changes else None
    if lead_exposure and lead_driver:
        if not memory_context.first_run and lead_change:
            return (
                f"Portfolio Risk Desk is centered on {_portfolio_scope(request)} across "
                f"{', '.join(request.themes)}. Since the last brief, {lead_change['change'].lower()}, "
                f"while the current risk map is still led by {lead_exposure['name'].lower()} and "
                f"{lead_driver['driver'].lower()} remains the main near-term driver."
            )
        return (
            f"Portfolio Risk Desk is centered on {_portfolio_scope(request)} across "
            f"{', '.join(request.themes)}. The risk map is currently led by "
            f"{lead_exposure['name'].lower()}, while the most important near-term driver is "
            f"{lead_driver['driver'].lower()} backed by {lead_driver['evidence_quality']} evidence."
        )
    return (
        f"Portfolio Risk Desk is centered on {_portfolio_scope(request)} across "
        f"{', '.join(request.themes)}. The current evidence set is still forming, so the brief "
        "leans on watchpoints and uncertainty management rather than strong directional claims."
    )


def _comparison_baseline(request: CreateBriefRequest, memory_context: MemoryContext) -> str:
    if not memory_context.first_run and memory_context.comparison_baseline:
        return memory_context.comparison_baseline
    if request.benchmark_or_comparison_lens:
        return request.benchmark_or_comparison_lens
    if memory_context.first_run:
        return "First run for this portfolio and theme set."
    return "Most recent brief comparison not configured."


def _build_risk_map_changes(
    evidence: list[dict[str, Any]],
    dominant_factors: list[dict[str, Any]],
    drivers: list[dict[str, Any]],
    memory_context: MemoryContext,
) -> list[dict[str, Any]]:
    if not memory_context.first_run:
        memory_changes = _memory_driven_changes(dominant_factors, drivers, memory_context)
        if memory_changes:
            return memory_changes

    candidates = sorted(
        [item for item in evidence if item["item_type"] == "evidence"],
        key=lambda item: (
            source_quality_value(item["source_quality"]),
            lane_weight(item),
            item["ranking"]["score"],
        ),
        reverse=True,
    )
    changes: list[dict[str, Any]] = []
    for item in candidates[:3]:
        change_prefix = {
            "earnings_primary": "Earnings evidence moved the risk map",
            "policy": "Policy evidence changed the risk map",
            "competitor": "Competitor evidence changed the read-through",
            "x_commentary": "Narrative evidence stayed provisional",
        }.get(item["source_lane"], f"{item['factor']} moved the risk map")
        changes.append(
            {
                "change": change_prefix,
                "effect": item["interpretation"],
                "evidence_id": item["id"],
                "supporting_evidence_ids": [item["id"]],
                "confidence_reason": (
                    "This change is backed by the highest-ranked evidence item currently shifting the risk map."
                ),
            }
        )
    return changes


def _memory_driven_changes(
    dominant_factors: list[dict[str, Any]],
    drivers: list[dict[str, Any]],
    memory_context: MemoryContext,
) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    prior_factor_map = {
        item["factor"]: item
        for item in memory_context.prior_dominant_factors
        if isinstance(item, dict) and "factor" in item
    }
    current_factor_map = {item["factor"]: item for item in dominant_factors}

    for factor, item in current_factor_map.items():
        prior_item = prior_factor_map.get(factor)
        if prior_item is None and item["stance"] != "watch":
            changes.append(
                {
                    "change": f"{factor} newly entered the active risk map",
                    "effect": item["impact_summary"],
                    "evidence_id": factor,
                    "supporting_evidence_ids": list(item.get("supporting_evidence_ids", [])),
                    "confidence_reason": item.get("confidence_reason", "Confidence reason unavailable."),
                }
            )
        elif prior_item and prior_item.get("stance") != item["stance"]:
            changes.append(
                {
                    "change": f"{factor} shifted from {prior_item.get('stance', 'watch')} to {item['stance']}",
                    "effect": item["impact_summary"],
                    "evidence_id": factor,
                    "supporting_evidence_ids": list(item.get("supporting_evidence_ids", [])),
                    "confidence_reason": item.get("confidence_reason", "Confidence reason unavailable."),
                }
            )

    prior_driver_names = {
        item.get("driver")
        for item in memory_context.prior_top_drivers
        if isinstance(item, dict)
    }
    for driver in drivers:
        if driver["driver"] not in prior_driver_names:
            changes.append(
                {
                    "change": f"{driver['driver']} became a newly prominent driver",
                    "effect": driver["second_order_readthrough"],
                    "evidence_id": driver["driver"],
                    "supporting_evidence_ids": list(driver.get("supporting_evidence_ids", [])),
                    "confidence_reason": driver.get("confidence_reason", "Confidence reason unavailable."),
                }
            )
            if len(changes) >= 3:
                break

    if not changes and dominant_factors:
        top = dominant_factors[0]
        changes.append(
            {
                "change": f"{top['factor']} remained the core portfolio driver",
                "effect": top["impact_summary"],
                "evidence_id": top["factor"],
                "supporting_evidence_ids": list(top.get("supporting_evidence_ids", [])),
                "confidence_reason": top.get("confidence_reason", "Confidence reason unavailable."),
            }
        )
    return changes[:3]


def _build_watchpoints(evidence: list[dict[str, Any]], memory_context: MemoryContext) -> list[dict[str, Any]]:
    watchpoints: list[dict[str, Any]] = []
    seen_topics: set[str] = set()
    prior_topics = {
        item.get("topic")
        for item in memory_context.prior_watchpoints
        if isinstance(item, dict)
    }
    for item in sorted(evidence, key=lambda entry: entry["ranking"]["score"], reverse=True):
        if item["factor"] in seen_topics:
            continue
        seen_topics.add(item["factor"])
        watchpoints.append(
            {
                "topic": item["factor"],
                "watchpoint": _watchpoint_text(item, item["factor"] in prior_topics),
                "next_check": item["source"]["recency_note"],
                "supporting_evidence_ids": [item["id"]],
            }
        )
        if len(watchpoints) == 5:
            break
    return watchpoints


def _watchpoint_text(item: dict[str, Any], was_already_active: bool) -> str:
    if item["source_lane"] == "policy":
        text = f"{item['watchpoint']} Watch for official rulemaking or management commentary before hardening the view."
        return f"{text} This remained active from the prior brief." if was_already_active else text
    if item["source_lane"] == "competitor":
        text = f"{item['watchpoint']} Check whether peers, suppliers, or customers confirm the same read-through."
        return f"{text} This remained active from the prior brief." if was_already_active else text
    if item["source_lane"] == "x_commentary":
        text = "Look for confirmation from primary company, filing, or policy sources before escalating the signal."
        return f"{text} This remained active from the prior brief." if was_already_active else text
    return f"{item['watchpoint']} This remained active from the prior brief." if was_already_active else item["watchpoint"]


def _build_evidence_and_sources(evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(evidence, key=lambda item: item["ranking"]["score"], reverse=True)
    return [
        {
            "evidence_id": item["id"],
            "source_title": item["source"]["title"],
            "url_or_publisher": item["source"]["url"],
            "timestamp_or_recency_note": item["source"]["timestamp"] or item["source"]["recency_note"],
            "why_it_mattered": f"[{item['source_lane']}] {item['why_it_matters']}",
            "fact_excerpt": item["fact"],
            "interpretation_excerpt": item["interpretation"],
        }
        for item in ordered
    ]


def _build_audit_trail(
    evidence: list[dict[str, Any]],
    dominant_factors: list[dict[str, Any]],
    risk_map_changes: list[dict[str, Any]],
    drivers: list[dict[str, Any]],
    scenarios: list[object],
    watchpoints: list[dict[str, Any]],
) -> dict[str, Any]:
    evidence_lookup = {item["id"]: item for item in evidence}
    return {
        "dominant_factors": [
            _audit_entry(
                claim_type="dominant_factor",
                claim=item["factor"],
                interpretation=item["impact_summary"],
                confidence_reason=item.get("confidence_reason"),
                supporting_evidence_ids=item.get("supporting_evidence_ids", []),
                evidence_lookup=evidence_lookup,
            )
            for item in dominant_factors
            if item.get("supporting_evidence_ids")
        ],
        "risk_map_changes": [
            _audit_entry(
                claim_type="risk_map_change",
                claim=item["change"],
                interpretation=item["effect"],
                confidence_reason=item.get("confidence_reason"),
                supporting_evidence_ids=item.get("supporting_evidence_ids", []),
                evidence_lookup=evidence_lookup,
            )
            for item in risk_map_changes
        ],
        "key_drivers": [
            _audit_entry(
                claim_type="driver",
                claim=item["driver"],
                interpretation=item["second_order_readthrough"],
                confidence_reason=item.get("confidence_reason"),
                supporting_evidence_ids=item.get("supporting_evidence_ids", []),
                evidence_lookup=evidence_lookup,
            )
            for item in drivers
        ],
        "scenarios": [
            _audit_entry(
                claim_type="scenario",
                claim=item.scenario,
                interpretation=" | ".join(item.breaks_or_holds),
                confidence_reason=item.confidence_reason,
                supporting_evidence_ids=item.supporting_evidence_ids,
                evidence_lookup=evidence_lookup,
            )
            for item in scenarios
        ],
        "watchpoints": [
            _audit_entry(
                claim_type="watchpoint",
                claim=item["topic"],
                interpretation=item["watchpoint"],
                confidence_reason="Watchpoints remain provisional until the cited evidence is refreshed or confirmed.",
                supporting_evidence_ids=item.get("supporting_evidence_ids", []),
                evidence_lookup=evidence_lookup,
            )
            for item in watchpoints
        ],
    }


def _audit_entry(
    *,
    claim_type: str,
    claim: str,
    interpretation: str,
    confidence_reason: str | None,
    supporting_evidence_ids: list[str],
    evidence_lookup: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    supporting_evidence = [
        {
            "evidence_id": evidence_id,
            "fact": evidence_lookup[evidence_id]["fact"],
            "interpretation": evidence_lookup[evidence_id]["interpretation"],
            "source_title": evidence_lookup[evidence_id]["source"]["title"],
        }
        for evidence_id in supporting_evidence_ids
        if evidence_id in evidence_lookup
    ]
    return {
        "claim_type": claim_type,
        "claim": claim,
        "interpretation": interpretation,
        "confidence_reason": confidence_reason or "Confidence reason unavailable.",
        "supporting_evidence_ids": list(supporting_evidence_ids),
        "supporting_evidence": supporting_evidence,
    }
