"""Host handoff adapters and helpers."""

from __future__ import annotations

from typing import Any

from intelligence_desk_brief.config import AppConfig
from intelligence_desk_brief.contracts import (
    CreateBriefRequest,
    DeliveryStatus,
    NotionWriteStatus,
    WriteBriefToNotionInput,
    WriteBriefToNotionOutput,
)
from intelligence_desk_brief.ops import log_event
from intelligence_desk_brief.providers.base import DeliveryAdapter


class OpenClawDeliveryHandoffAdapter(DeliveryAdapter):
    """Record a Notion handoff for the host to execute."""

    def __init__(self, config: AppConfig):
        self._config = config

    def write_brief(self, request: WriteBriefToNotionInput) -> WriteBriefToNotionOutput:
        metadata = {
            "handoff_version": (request.delivery_payload or {}).get("handoff_version", "unknown"),
            "workspace_id": request.workspace_id,
            "profile_id": request.profile_id,
            "profile_name": request.profile_name,
            "parent_page_id": request.parent_page_id,
            "database_id": request.database_id,
            "brief_title": request.brief_title,
            "has_markdown": bool(request.markdown),
            "delivery_payload_keys": sorted((request.delivery_payload or {}).keys()),
            "section_count": len((request.delivery_payload or {}).get("ordered_sections", [])),
            "integration_target": (request.delivery_payload or {}).get("integration_target"),
            "audit_section_count": sum(
                len(items) if isinstance(items, list) else 0
                for items in ((request.delivery_payload or {}).get("audit_bundle") or {}).values()
            ),
            "fallback_delivery_status": ((request.delivery_payload or {}).get("failure_semantics") or {}).get(
                "fallback_delivery_status"
            ),
        }
        if self._config.notion_parent_page_id or request.parent_page_id:
            log_event("delivery.handoff.accepted", workspace_id=request.workspace_id, has_markdown=bool(request.markdown))
            return WriteBriefToNotionOutput(
                notion_page_id="openclaw-handoff",
                url="https://openclaw.local/notion-handoff",
                status=NotionWriteStatus.ACCEPTED,
                delivery_metadata=metadata,
            )
        log_event("delivery.handoff.failed", workspace_id=request.workspace_id, reason="missing_parent_page")
        return WriteBriefToNotionOutput(
            notion_page_id="handoff-unavailable",
            url="https://openclaw.local/unavailable",
            status=NotionWriteStatus.FAILED,
            delivery_metadata=metadata,
        )


def resolve_delivery_status(
    request: CreateBriefRequest,
    notion_result: WriteBriefToNotionOutput | None,
) -> DeliveryStatus:
    if request.delivery_target.value == "inline":
        return DeliveryStatus.INLINE_RETURNED
    if notion_result and notion_result.status in {
        NotionWriteStatus.ACCEPTED,
        NotionWriteStatus.CREATED,
        NotionWriteStatus.UPDATED,
    }:
        return DeliveryStatus.HANDOFF_RECORDED
    return DeliveryStatus.FAILED


def write_brief_to_notion(
    request: WriteBriefToNotionInput,
    adapter: DeliveryAdapter,
) -> WriteBriefToNotionOutput:
    """Return a host-consumable Notion handoff result."""
    return adapter.write_brief(request)
