#!/usr/bin/env python3
"""Residual leak scanning utilities."""

from __future__ import annotations

from typing import Any, List, Sequence

from modeio_redact.core.models import MappingEntry, ResidualFinding


def scan_for_residuals(
    text: str,
    mapping_entries: Sequence[Any],
    *,
    part_id: str,
) -> List[ResidualFinding]:
    """Return residual findings when original values remain in output text."""
    findings: List[ResidualFinding] = []
    seen = set()
    for entry in mapping_entries:
        if isinstance(entry, MappingEntry):
            original = entry.original.strip()
        elif isinstance(entry, dict):
            original = str(entry.get("original") or "").strip()
        else:
            continue
        if not original or original in seen:
            continue
        seen.add(original)
        if original in text:
            findings.append(
                ResidualFinding(
                    part_id=part_id,
                    text=original,
                    evidence="original value still present in output",
                )
            )
    return findings
