#!/usr/bin/env python3
"""Base provider protocol for anonymization backends."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Protocol, Sequence


@dataclass(frozen=True)
class ProviderItem:
    """Normalized provider item used to build mapping entries."""

    original: str
    placeholder: str
    entity_type: str


@dataclass
class ProviderResult:
    """Provider output for pipeline planning and persistence."""

    anonymized_content: str
    has_pii: bool
    items: Sequence[ProviderItem]
    raw_payload: Dict[str, Any] = field(default_factory=dict)


class RedactionProvider(Protocol):
    """Provider interface for local regex or remote API anonymization."""

    key: str

    def redact(
        self,
        content: str,
        *,
        level: str,
        input_type: str,
        sender_code: Optional[str] = None,
        recipient_code: Optional[str] = None,
    ) -> ProviderResult:
        """Return normalized provider result."""
