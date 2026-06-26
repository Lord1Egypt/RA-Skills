#!/usr/bin/env python3
"""Shared data contracts for the modular redaction pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence


@dataclass(frozen=True)
class MappingEntry:
    """Single redaction mapping pair."""

    placeholder: str
    original: str
    entity_type: str = "unknown"

    @classmethod
    def from_raw(cls, raw: Dict[str, Any]) -> Optional["MappingEntry"]:
        if not isinstance(raw, dict):
            return None

        placeholder = raw.get("placeholder") or raw.get("anonymized") or raw.get("maskedValue")
        original = raw.get("original")
        if original is None:
            original = raw.get("value")

        if not isinstance(placeholder, str) or not isinstance(original, str):
            return None

        placeholder = placeholder.strip()
        original = original.strip()
        if not placeholder or not original:
            return None

        entity_type = raw.get("type")
        if not isinstance(entity_type, str) or not entity_type.strip():
            entity_type = "unknown"

        return cls(placeholder=placeholder, original=original, entity_type=entity_type)

    def to_dict(self) -> Dict[str, str]:
        return {
            "placeholder": self.placeholder,
            "original": self.original,
            "type": self.entity_type,
        }


@dataclass(frozen=True)
class MapRef:
    """Lightweight pointer to a map record."""

    map_id: str
    map_path: str
    entry_count: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mapId": self.map_id,
            "mapPath": self.map_path,
            "entryCount": self.entry_count,
        }

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "MapRef":
        return cls(
            map_id=str(raw.get("mapId") or ""),
            map_path=str(raw.get("mapPath") or ""),
            entry_count=int(raw.get("entryCount") or 0),
        )


@dataclass
class MapRecord:
    """Full map record persisted in local map store."""

    schema_version: str
    map_id: str
    created_at: str
    level: str
    source_mode: str
    input_hash: str
    anonymized_hash: str
    entries: Sequence[MappingEntry]

    @property
    def entry_count(self) -> int:
        return len(self.entries)

    def to_ref(self, map_path: str) -> MapRef:
        return MapRef(map_id=self.map_id, map_path=map_path, entry_count=self.entry_count)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schemaVersion": self.schema_version,
            "mapId": self.map_id,
            "createdAt": self.created_at,
            "level": self.level,
            "sourceMode": self.source_mode,
            "inputHash": self.input_hash,
            "anonymizedHash": self.anonymized_hash,
            "entryCount": self.entry_count,
            "entries": [entry.to_dict() for entry in self.entries],
        }


@dataclass(frozen=True)
class InputSource:
    """Normalized input source context for pipeline stages."""

    content: str
    input_type: str
    input_path: Optional[str]
    extension: Optional[str]
    handler_key: Optional[str]


@dataclass
class ExtractionBundle:
    """Adapter extraction output containing canonical text."""

    adapter_key: str
    canonical_text: str
    diagnostics: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class PlanSpan:
    """One canonical redaction span in normalized text coordinates."""

    start: int
    end: int
    original: str
    placeholder: str
    entity_type: str


@dataclass
class RedactionPlan:
    """Canonical plan derived from mapping entries."""

    spans: Sequence[PlanSpan]
    mapping_entries: Sequence[MappingEntry]
    warnings: List[str] = field(default_factory=list)

    @property
    def expected_count(self) -> int:
        return len(self.spans)


@dataclass
class ApplyReport:
    """Coverage report for apply stage."""

    expected_count: int
    found_count: int
    applied_count: int
    missed_spans: Sequence[PlanSpan] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ResidualFinding:
    """Post-redaction residual detection evidence."""

    part_id: str
    text: str
    evidence: Optional[str] = None


@dataclass
class VerificationReport:
    """Verification stage output."""

    passed: bool
    skipped: bool
    residual_count: int
    residuals: Sequence[ResidualFinding] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @classmethod
    def skipped_report(cls) -> "VerificationReport":
        return cls(passed=True, skipped=True, residual_count=0, residuals=(), warnings=[])


@dataclass
class OutputPipelineResult:
    """End-to-end output of apply/verify/finalize pipeline."""

    output_path: Optional[str]
    sidecar_path: Optional[str]
    apply_report: ApplyReport
    verification_report: VerificationReport
