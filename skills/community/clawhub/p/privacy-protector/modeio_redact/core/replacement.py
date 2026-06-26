#!/usr/bin/env python3
"""Shared text replacement helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Sequence, Tuple

from modeio_redact.core.models import MappingEntry


@dataclass
class ReplacementResult:
    content: str
    total_replacements: int
    replacements_by_type: Dict[str, int] = field(default_factory=dict)


def build_replacement_pairs(
    entries: Sequence[MappingEntry],
    direction: Literal["redact", "restore"],
) -> List[Tuple[str, str]]:
    pairs: List[Tuple[str, str]] = []
    seen: set = set()

    for entry in entries:
        if direction == "restore":
            source, target = entry.placeholder, entry.original
        else:
            source, target = entry.original, entry.placeholder
        if not source:
            continue
        dedupe_key = (source, target)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        pairs.append((source, target))

    pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
    return pairs


def apply_text_replacements(
    text: str,
    entries: Sequence[MappingEntry],
    direction: Literal["redact", "restore"],
) -> ReplacementResult:
    result_text = text
    total = 0
    by_type: Dict[str, int] = {}
    pairs = build_replacement_pairs(entries=entries, direction=direction)

    source_to_type: Dict[str, str] = {}
    for entry in entries:
        source = entry.placeholder if direction == "restore" else entry.original
        if source and source not in source_to_type:
            source_to_type[source] = entry.entity_type

    for source, target in pairs:
        count = result_text.count(source)
        if count <= 0:
            continue
        result_text = result_text.replace(source, target)
        total += count
        entity_type = source_to_type.get(source, "unknown")
        by_type[entity_type] = by_type.get(entity_type, 0) + count

    return ReplacementResult(
        content=result_text,
        total_replacements=total,
        replacements_by_type=by_type,
    )
