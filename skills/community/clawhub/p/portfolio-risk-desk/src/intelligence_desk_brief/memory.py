"""OpenClaw-facing memory helpers for Portfolio Risk Desk.

Production memory is expected to be host-managed, typically through an
OpenClaw or ClawHub Redis-backed memory plugin. These helpers define the
payload shapes the host can recall and store. Local file-backed state remains
available as a development fallback.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any

from intelligence_desk_brief.contracts import CreateBriefRequest, CreateBriefResponse

BRIEF_STATE_PREFIX = "PORTFOLIO_RISK_DESK_BRIEF_STATE:"
PROFILE_PREFIX = "PORTFOLIO_RISK_DESK_PROFILE:"
DEFAULT_WORKSPACE_ID = "guest-workspace"


@dataclass(frozen=True)
class MemoryContext:
    """Recalled context from host-managed memory."""

    available: bool = False
    first_run: bool = True
    comparison_baseline: str | None = None
    prior_summary: str | None = None
    prior_dominant_factors: list[dict[str, Any]] = field(default_factory=list)
    prior_top_drivers: list[dict[str, Any]] = field(default_factory=list)
    prior_watchpoints: list[dict[str, Any]] = field(default_factory=list)
    prior_risk_map_changes: list[dict[str, Any]] = field(default_factory=list)
    repeated_evidence_fingerprints: frozenset[str] = field(default_factory=frozenset)
    warning: str | None = None


@dataclass(frozen=True)
class MemoryRecord:
    """Minimal brief state worth storing after a run."""

    workspace_id: str
    profile_key: str
    profile_id: str | None
    profile_name: str | None
    brief_id: str
    portfolio_scope: str
    themes: list[str]
    summary: str
    dominant_factors: list[dict[str, Any]]
    top_drivers: list[dict[str, Any]]
    watchpoints: list[dict[str, Any]]
    risk_map_changes: list[dict[str, Any]]
    evidence_fingerprints: list[str]


def resolve_workspace_id(request: CreateBriefRequest) -> str:
    return request.workspace_id or DEFAULT_WORKSPACE_ID


def build_profile_key(request: CreateBriefRequest) -> str:
    payload = {
        "workspace_id": resolve_workspace_id(request),
        "profile_id": request.profile_id,
        "profile_name": request.profile_name,
        "brief_type": request.brief_type.value,
        "holdings": sorted(request.holdings),
        "watchlist": sorted(request.watchlist),
        "themes": sorted(request.themes),
        "scenario_questions": sorted(request.scenario_questions),
    }
    digest = hashlib.sha1(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return f"prdesk-{digest[:16]}"


def fingerprint_evidence(item: dict[str, Any]) -> str:
    source = item.get("source", {}) if isinstance(item.get("source"), dict) else {}
    payload = {
        "factor": item.get("factor"),
        "source_title": source.get("title") or item.get("source_title"),
        "url": source.get("url") or item.get("url"),
        "affected_names": sorted(item.get("affected_names", [])),
    }
    digest = hashlib.sha1(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return digest[:16]


def build_memory_record(
    request: CreateBriefRequest,
    brief: CreateBriefResponse,
    ranked_evidence: list[dict[str, Any]],
) -> MemoryRecord:
    return MemoryRecord(
        workspace_id=resolve_workspace_id(request),
        profile_key=build_profile_key(request),
        profile_id=request.profile_id,
        profile_name=request.profile_name,
        brief_id=brief.brief_id,
        portfolio_scope=brief.user_focus.portfolio_or_watchlist,
        themes=list(brief.user_focus.interested_industries),
        summary=brief.summary,
        dominant_factors=list(brief.dominant_factors),
        top_drivers=list(brief.key_drivers_and_readthroughs[:5]),
        watchpoints=list(brief.watchpoints[:5]),
        risk_map_changes=list(brief.risk_map_changes[:5]),
        evidence_fingerprints=[
            fingerprint_evidence(item)
            for item in ranked_evidence
            if item.get("item_type") == "evidence"
        ],
    )


def memory_context_from_record(record: MemoryRecord) -> MemoryContext:
    return MemoryContext(
        available=True,
        first_run=False,
        comparison_baseline="Most recent brief for this portfolio and theme set.",
        prior_summary=record.summary,
        prior_dominant_factors=list(record.dominant_factors),
        prior_top_drivers=list(record.top_drivers),
        prior_watchpoints=list(record.watchpoints),
        prior_risk_map_changes=list(record.risk_map_changes),
        repeated_evidence_fingerprints=frozenset(record.evidence_fingerprints),
    )


def build_memory_recall_args(request: CreateBriefRequest) -> dict[str, Any]:
    query = (
        f"Portfolio Risk Desk previous brief context for workspace {resolve_workspace_id(request)} "
        f"holdings {', '.join(request.holdings or request.watchlist)} "
        f"themes {', '.join(request.themes)} scenarios {', '.join(request.scenario_questions or [])}"
    ).strip()
    return {
        "query": query,
        "limit": 5,
        "workspace_id": resolve_workspace_id(request),
        "profile_key": build_profile_key(request),
    }


def build_memory_store_entries(
    request: CreateBriefRequest,
    brief: CreateBriefResponse,
    ranked_evidence: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    record = build_memory_record(request, brief, ranked_evidence)
    return [
        {
            "text": (
                f"{PROFILE_PREFIX}"
                f"{json.dumps({'workspace_id': record.workspace_id, 'profile_key': record.profile_key, 'profile_id': record.profile_id, 'profile_name': record.profile_name, 'portfolio_scope': record.portfolio_scope, 'themes': record.themes}, sort_keys=True)}"
            ),
            "category": "entity",
            "tags": ["portfolio-risk-desk", "profile", record.workspace_id, record.profile_key],
        },
        {
            "text": f"{BRIEF_STATE_PREFIX}{json.dumps(_record_to_state_payload(record), sort_keys=True)}",
            "category": "decision",
            "tags": ["portfolio-risk-desk", "brief-state", record.workspace_id, record.profile_key],
        },
    ]


def memory_context_from_recalled_memories(memories: list[dict[str, Any]]) -> MemoryContext:
    latest_state: dict[str, Any] | None = None
    warning: str | None = None

    for memory in memories:
        text = _extract_memory_text(memory)
        if not text:
            continue
        if text.startswith(BRIEF_STATE_PREFIX):
            payload = text.removeprefix(BRIEF_STATE_PREFIX)
            try:
                latest_state = json.loads(payload)
            except json.JSONDecodeError:
                warning = "A recalled brief-state memory could not be parsed cleanly."

    if latest_state is None:
        return MemoryContext(
            available=bool(memories),
            first_run=True,
            warning=warning,
        )

    return MemoryContext(
        available=True,
        first_run=False,
        comparison_baseline="Most recent brief for this portfolio and theme set.",
        prior_summary=str(latest_state.get("summary") or ""),
        prior_dominant_factors=_as_object_list(latest_state.get("dominant_factors")),
        prior_top_drivers=_as_object_list(latest_state.get("top_drivers")),
        prior_watchpoints=_as_object_list(latest_state.get("watchpoints")),
        prior_risk_map_changes=_as_object_list(latest_state.get("risk_map_changes")),
        repeated_evidence_fingerprints=frozenset(_as_string_list(latest_state.get("evidence_fingerprints"))),
        warning=warning,
    )


def _record_to_state_payload(record: MemoryRecord) -> dict[str, Any]:
    return {
        "workspace_id": record.workspace_id,
        "profile_key": record.profile_key,
        "profile_id": record.profile_id,
        "profile_name": record.profile_name,
        "brief_id": record.brief_id,
        "portfolio_scope": record.portfolio_scope,
        "themes": record.themes,
        "summary": record.summary,
        "dominant_factors": record.dominant_factors,
        "top_drivers": record.top_drivers,
        "watchpoints": record.watchpoints,
        "risk_map_changes": record.risk_map_changes,
        "evidence_fingerprints": record.evidence_fingerprints,
    }


def _extract_memory_text(memory: dict[str, Any]) -> str:
    if isinstance(memory.get("text"), str):
        return memory["text"]
    if isinstance(memory.get("content"), str):
        return memory["content"]
    if isinstance(memory.get("memory"), dict) and isinstance(memory["memory"].get("text"), str):
        return memory["memory"]["text"]
    return ""


def _as_object_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _as_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]
