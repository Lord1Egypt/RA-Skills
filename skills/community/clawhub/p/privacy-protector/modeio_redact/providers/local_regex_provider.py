#!/usr/bin/env python3
"""Local regex anonymization provider adapter."""

from __future__ import annotations

from typing import List, Optional

from modeio_redact.detection.detect_local import detect_sensitive_local
from modeio_redact.providers.base import ProviderItem, ProviderResult


class LocalRegexProvider:
    """Provider wrapping detect_local output into shared contracts."""

    key = "local-regex"

    def redact(
        self,
        content: str,
        *,
        level: str,
        input_type: str,
        sender_code: Optional[str] = None,
        recipient_code: Optional[str] = None,
    ) -> ProviderResult:
        del level
        del input_type
        del sender_code
        del recipient_code

        local_result = detect_sensitive_local(content)
        items: List[ProviderItem] = []
        for raw in local_result.get("items", []):
            placeholder = (raw.get("maskedValue") or "").strip()
            original = (raw.get("value") or "").strip()
            entity_type = (raw.get("type") or "unknown").strip() or "unknown"
            if not placeholder or not original:
                continue
            items.append(
                ProviderItem(
                    original=original,
                    placeholder=placeholder,
                    entity_type=entity_type,
                )
            )

        return ProviderResult(
            anonymized_content=local_result.get("sanitizedText", ""),
            has_pii=bool(items),
            items=items,
            raw_payload={"localDetection": local_result},
        )
