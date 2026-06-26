#!/usr/bin/env python3
"""Build shared redaction plan objects from mapping entries."""

from __future__ import annotations

from typing import Any, List, Sequence

from modeio_redact.core.models import MappingEntry, RedactionPlan
from modeio_redact.planning.resolver import resolve_plan_spans


def _normalize_mapping_entries(mapping_entries: Sequence[Any]) -> List[MappingEntry]:
    normalized: List[MappingEntry] = []
    for raw in mapping_entries:
        if isinstance(raw, MappingEntry):
            normalized.append(raw)
            continue
        if isinstance(raw, dict):
            entry = MappingEntry.from_raw(raw)
            if entry is not None:
                normalized.append(entry)
    return normalized


def build_redaction_plan(canonical_text: str, mapping_entries: Sequence[Any]) -> RedactionPlan:
    """Build canonical redaction plan from normalized map entries."""
    normalized_entries = _normalize_mapping_entries(mapping_entries)
    spans = resolve_plan_spans(canonical_text=canonical_text, mapping_entries=normalized_entries)
    warnings = []
    if normalized_entries and not spans:
        warnings.append("No canonical spans resolved from mapping entries.")
    return RedactionPlan(spans=spans, mapping_entries=normalized_entries, warnings=warnings)
