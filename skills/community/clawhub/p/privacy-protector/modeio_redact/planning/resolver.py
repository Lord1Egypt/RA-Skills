#!/usr/bin/env python3
"""Canonical span resolution helpers for redaction plans."""

from __future__ import annotations

from typing import List, Sequence, Tuple

from modeio_redact.core.models import MappingEntry, PlanSpan


def _is_overlapping(start: int, end: int, ranges: Sequence[Tuple[int, int]]) -> bool:
    for existing_start, existing_end in ranges:
        if start < existing_end and end > existing_start:
            return True
    return False


def resolve_plan_spans(canonical_text: str, mapping_entries: Sequence[MappingEntry]) -> List[PlanSpan]:
    """Resolve non-overlapping spans from mapping entries in canonical text."""
    candidates: List[Tuple[str, str, str]] = []
    for entry in mapping_entries:
        original = entry.original.strip()
        placeholder = entry.placeholder.strip()
        entity_type = entry.entity_type.strip() or "unknown"
        if not original or not placeholder:
            continue
        candidates.append((original, placeholder, entity_type))

    candidates.sort(key=lambda item: len(item[0]), reverse=True)

    spans: List[PlanSpan] = []
    occupied: List[Tuple[int, int]] = []

    for original, placeholder, entity_type in candidates:
        search_from = 0
        while True:
            start = canonical_text.find(original, search_from)
            if start < 0:
                break
            end = start + len(original)
            search_from = start + 1
            if _is_overlapping(start, end, occupied):
                continue
            occupied.append((start, end))
            spans.append(
                PlanSpan(
                    start=start,
                    end=end,
                    original=original,
                    placeholder=placeholder,
                    entity_type=entity_type,
                )
            )

    spans.sort(key=lambda item: (item.start, item.end))
    return spans
