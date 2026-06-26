#!/usr/bin/env python3
"""Remote API anonymization provider adapter."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from modeio_redact.providers.base import ProviderItem, ProviderResult
from modeio_redact.workflow.map_store import normalize_mapping_entries


class RemoteApiProvider:
    """Provider wrapper over existing API anonymize callable."""

    key = "api"

    def __init__(self, anonymize_callable: Callable[..., Dict[str, Any]]):
        self._anonymize_callable = anonymize_callable

    def redact(
        self,
        content: str,
        *,
        level: str,
        input_type: str,
        sender_code: Optional[str] = None,
        recipient_code: Optional[str] = None,
    ) -> ProviderResult:
        payload = self._anonymize_callable(
            content,
            level=level,
            sender_code=sender_code,
            recipient_code=recipient_code,
            input_type=input_type,
        )
        data = payload.get("data", {})
        normalized_entries = normalize_mapping_entries(data)

        items: List[ProviderItem] = []
        for entry in normalized_entries:
            items.append(
                ProviderItem(
                    original=entry.original,
                    placeholder=entry.placeholder,
                    entity_type=entry.entity_type,
                )
            )

        return ProviderResult(
            anonymized_content=str(data.get("anonymizedContent", "")),
            has_pii=bool(data.get("hasPII")),
            items=items,
            raw_payload=payload,
        )
