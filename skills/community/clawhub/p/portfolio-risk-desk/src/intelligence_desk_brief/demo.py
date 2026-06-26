"""Canonical demo runner for Portfolio Risk Desk."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import date
from typing import Any

from intelligence_desk_brief.config import AppConfig
from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.fixtures import load_demo_request_payload, load_mock_evidence
from intelligence_desk_brief.orchestrator import PortfolioRiskDesk
from intelligence_desk_brief.providers.base import RetrievalAdapter

CANONICAL_DEMO_PROMPT = (
    "Create my daily Portfolio Risk Desk for NVDA, AMD, TSM, ASML, focus on AI infrastructure "
    "and semiconductors, and tell me what changed since yesterday plus what happens if rates move higher."
)


@dataclass(frozen=True)
class DemoRunResult:
    prompt: str
    mode: str
    markdown: str
    payload: dict[str, Any]
    operator_notes: list[str]


class _DemoProviderFailureAdapter(RetrievalAdapter):
    def collect(self, request: CreateBriefRequest) -> list[dict[str, Any]]:
        del request
        payload = deepcopy(load_mock_evidence())
        return [
            payload[1],
            payload[4],
            {
                "id": "retrieval-notice-primary",
                "item_type": "retrieval_notice",
                "category": "retrieval_status",
                "source_title": "Primary retrieval degraded during demo",
                "url": "https://openclaw.local/provider-degraded",
                "published_at": "2026-03-25T12:00:00+00:00",
                "fact": "Primary web retrieval partially failed, so the brief continued with bounded evidence.",
                "interpretation": "The demo should still show portfolio reasoning instead of failing outright.",
                "confidence_level": "low",
                "signal_strength": "low",
                "retrieval_status": "failed",
                "provider": "apify",
                "source_type": "primary_web",
                "raw_reference": {"demo": True},
            },
        ]


def run_demo(mode: str = "happy") -> DemoRunResult:
    request_payload = load_demo_request_payload()
    request_payload["delivery_target"] = "notion"
    request = CreateBriefRequest.from_dict(request_payload)

    config = AppConfig(notion_parent_page_id="demo-parent-page")
    retrieval_adapter: RetrievalAdapter | None = None
    operator_notes: list[str] = []

    if mode == "provider_failure":
        retrieval_adapter = _DemoProviderFailureAdapter()
        operator_notes.append(
            "Primary retrieval was intentionally degraded. The brief should still prove portfolio thinking, scenario confidence, and evidence traceability."
        )
    elif mode == "delivery_failure":
        config = AppConfig()
        operator_notes.append(
            "Delivery was intentionally left unavailable. The brief should still render inline with useful analysis and clear failure status."
        )
    else:
        operator_notes.append(
            "Canonical happy-path demo: prompt -> evidence -> exposure map -> memory-aware change section -> notion handoff."
        )

    runtime = PortfolioRiskDesk(config, retrieval_adapter=retrieval_adapter)
    brief, markdown = runtime.create_brief(request, as_of_date=date(2026, 3, 25))

    if brief.delivery_status.value == "failed":
        operator_notes.append("Delivery failed cleanly and the brief still returned a useful inline artifact.")
    if brief.uncertainty_notes:
        operator_notes.append("Uncertainty notes remained visible, preserving a judge-friendly story under partial failure.")

    return DemoRunResult(
        prompt=CANONICAL_DEMO_PROMPT,
        mode=mode,
        markdown=markdown,
        payload=brief.to_dict(),
        operator_notes=operator_notes,
    )
