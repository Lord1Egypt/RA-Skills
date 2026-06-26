"""Single-orchestrator runtime for the packaged skill."""

from __future__ import annotations

from dataclasses import replace
from datetime import date

from intelligence_desk_brief.config import AppConfig
from intelligence_desk_brief.contracts import (
    CreateBriefRequest,
    CreateBriefResponse,
    DeliveryStatus,
    WriteBriefToNotionInput,
    WriteBriefToNotionOutput,
)
from intelligence_desk_brief.delivery import (
    OpenClawDeliveryHandoffAdapter,
    resolve_delivery_status,
    write_brief_to_notion,
)
from intelligence_desk_brief.memory import MemoryContext, build_memory_record, resolve_workspace_id
from intelligence_desk_brief.normalization import normalize_evidence
from intelligence_desk_brief.ops import configure_logging, log_event, timed_stage
from intelligence_desk_brief.providers.base import DeliveryAdapter, MemoryAdapter, RetrievalAdapter
from intelligence_desk_brief.providers.local_state import LocalFileMemoryAdapter
from intelligence_desk_brief.ranking import rank_evidence
from intelligence_desk_brief.renderer import render_markdown
from intelligence_desk_brief.retrieval import FixtureRetrievalAdapter, LiveRetrievalAdapter
from intelligence_desk_brief.synthesis import build_brief


class NullMemoryAdapter(MemoryAdapter):
    def recall_context(self, request: CreateBriefRequest) -> MemoryContext:
        del request
        return MemoryContext()

    def store_brief(self, request: CreateBriefRequest, record) -> None:
        del request, record


class PortfolioRiskDesk:
    """Coordinates analysis and host handoff generation."""

    def __init__(
        self,
        config: AppConfig,
        *,
        retrieval_adapter: RetrievalAdapter | None = None,
        memory_adapter: MemoryAdapter | None = None,
        delivery_adapter: DeliveryAdapter | None = None,
    ):
        self._config = config
        configure_logging(config.log_level)
        self._retrieval_adapter = retrieval_adapter or (
            LiveRetrievalAdapter(config) if config.enable_live_providers else FixtureRetrievalAdapter()
        )
        self._memory_adapter = memory_adapter or (
            LocalFileMemoryAdapter(config.local_state_dir)
            if config.local_state_dir
            else NullMemoryAdapter()
        )
        self._delivery_adapter = delivery_adapter or OpenClawDeliveryHandoffAdapter(config)

    def create_brief(
        self,
        request: CreateBriefRequest,
        *,
        as_of_date: date | None = None,
    ) -> tuple[CreateBriefResponse, str]:
        run_date = as_of_date or date.today()
        log_event(
            "brief.run.started",
            workspace_id=resolve_workspace_id(request),
            delivery_target=request.delivery_target.value,
            holdings=request.holdings,
            themes=request.themes,
        )
        with timed_stage("memory.recall", workspace_id=resolve_workspace_id(request)):
            memory_context = self._recall_memory_context(request)
        with timed_stage("retrieval.collect", workspace_id=resolve_workspace_id(request)):
            raw_evidence = self._retrieval_adapter.collect(request)
        with timed_stage("normalization.run", item_count=len(raw_evidence)):
            normalized_evidence = normalize_evidence(raw_evidence, request)
        with timed_stage("ranking.run", item_count=len(normalized_evidence)):
            ranked_evidence = rank_evidence(request, normalized_evidence, memory_context=memory_context)

        with timed_stage("synthesis.run", item_count=len(ranked_evidence)):
            brief = build_brief(
                request,
                ranked_evidence,
                memory_context,
                as_of_date=run_date,
                delivery_status=DeliveryStatus.INLINE_RETURNED,
            )

        notion_result = None
        markdown = render_markdown(brief)
        if request.delivery_target.value == "notion":
            log_event("delivery.handoff.requested", workspace_id=resolve_workspace_id(request))
            delivery_request = WriteBriefToNotionInput(
                brief_payload=brief.to_dict(),
                parent_page_id=self._config.notion_parent_page_id or "openclaw-parent-page",
                workspace_id=resolve_workspace_id(request),
                profile_id=request.profile_id,
                profile_name=request.profile_name,
                brief_title=f"Portfolio Risk Desk - {brief.date}",
                markdown=markdown,
                delivery_payload=_build_delivery_payload(brief, markdown),
            )
            notion_result = write_brief_to_notion(
                delivery_request,
                self._delivery_adapter,
            )

        brief = replace(
            brief,
            delivery_status=resolve_delivery_status(request, notion_result),
            delivery_metadata=notion_result.delivery_metadata if notion_result else None,
        )
        brief = self._store_memory_context(request, brief, ranked_evidence)
        markdown = render_markdown(brief)
        log_event(
            "brief.run.completed",
            brief_id=brief.brief_id,
            delivery_status=brief.delivery_status.value,
            uncertainty_count=len(brief.uncertainty_notes),
        )
        return CreateBriefResponse.from_dict(brief.to_dict()), markdown

    def write_brief_to_notion(
        self,
        request: WriteBriefToNotionInput,
    ) -> WriteBriefToNotionOutput:
        result = write_brief_to_notion(request, self._delivery_adapter)
        return WriteBriefToNotionOutput.from_dict(result.to_dict())

    def _recall_memory_context(self, request: CreateBriefRequest) -> MemoryContext:
        try:
            return self._memory_adapter.recall_context(request)
        except Exception as error:  # pragma: no cover - defensive degraded mode
            return MemoryContext(
                warning=f"Memory recall unavailable: {error}",
            )

    def _store_memory_context(
        self,
        request: CreateBriefRequest,
        brief: CreateBriefResponse,
        ranked_evidence: list[dict[str, object]],
    ) -> CreateBriefResponse:
        try:
            record = build_memory_record(request, brief, ranked_evidence)
            self._memory_adapter.store_brief(request, record)
            return brief
        except Exception as error:  # pragma: no cover - defensive degraded mode
            notes = list(brief.uncertainty_notes)
            notes.append(f"Memory store unavailable: {error}")
            return replace(brief, uncertainty_notes=notes)


def create_brief(
    request: CreateBriefRequest,
    *,
    config: AppConfig | None = None,
    as_of_date: date | None = None,
) -> tuple[CreateBriefResponse, str]:
    runtime = PortfolioRiskDesk(config or AppConfig.from_env())
    return runtime.create_brief(request, as_of_date=as_of_date)


def _build_delivery_payload(brief: CreateBriefResponse, markdown: str) -> dict[str, object]:
    ordered_sections = [
        {
            "id": "user_focus",
            "title": "0) User focus",
            "content": brief.user_focus.to_dict(),
        },
        {
            "id": "current_exposure_map",
            "title": "2) Current exposure map",
            "content": brief.current_exposure_map,
        },
        {
            "id": "dominant_factors",
            "title": "Dominant factors",
            "content": brief.dominant_factors,
        },
        {
            "id": "risk_map_changes",
            "title": "3) What changed since last brief",
            "content": brief.risk_map_changes,
        },
        {
            "id": "key_drivers_and_readthroughs",
            "title": "4) Key drivers and cross-holding read-throughs",
            "content": brief.key_drivers_and_readthroughs,
        },
        {
            "id": "scenario_analysis",
            "title": "5) Scenario analysis",
            "content": [item.to_dict() for item in brief.scenario_analysis],
        },
        {
            "id": "signal_vs_noise",
            "title": "6) Signal vs noise",
            "content": brief.signal_vs_noise,
        },
        {
            "id": "watchpoints",
            "title": "7) Watchpoints",
            "content": brief.watchpoints,
        },
        {
            "id": "evidence_and_sources",
            "title": "8) Evidence and sources",
            "content": brief.evidence_and_sources,
        },
        {
            "id": "audit_trail",
            "title": "9) Audit trail",
            "content": brief.audit_trail,
        },
        {
            "id": "uncertainty_notes",
            "title": "Uncertainty notes",
            "content": brief.uncertainty_notes,
        },
    ]
    return {
        "handoff_version": "v1",
        "integration_target": "openclaw_notion_handoff",
        "delivery_mode": "handoff_only",
        "target": {
            "surface": "notion",
            "owner": "openclaw",
        },
        "page_title": f"Portfolio Risk Desk - {brief.date}",
        "metadata": {
            "brief_id": brief.brief_id,
            "date": brief.date,
            "workspace_id": brief.workspace_id,
            "profile_id": brief.profile_id,
            "profile_name": brief.profile_name,
            "delivery_status": brief.delivery_status.value,
        },
        "properties": {
            "Portfolio Risk Desk": f"Portfolio Risk Desk - {brief.date}",
            "Date": brief.date,
            "Workspace ID": brief.workspace_id,
            "Profile ID": brief.profile_id,
            "Profile Name": brief.profile_name,
            "Delivery Status": brief.delivery_status.value,
        },
        "summary_block": brief.summary,
        "markdown": markdown,
        "ordered_sections": ordered_sections,
        "source_index": brief.evidence_and_sources,
        "audit_bundle": brief.audit_trail,
        "failure_semantics": {
            "fallback_delivery_status": "failed",
            "preserve_inline_brief": True,
            "preserve_audit_bundle": True,
        },
    }
