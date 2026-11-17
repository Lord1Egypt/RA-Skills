"""Typed contracts for compliance scanning.

The public CLI still exposes dictionaries for backwards compatibility.  These
models give the scanner a stable, serialisable contract underneath that
compatibility layer.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ScanMode(str, Enum):
    """Context in which the same compliance rules are interpreted."""

    CUSTOMER_COPY = "customer_copy"
    INTERNAL_REPORT = "internal_report"
    KNOWLEDGE = "knowledge"
    QUOTED_EVIDENCE = "quoted_evidence"


@dataclass(frozen=True)
class ScanHit:
    """One explainable rule hit.

    ``offset`` and ``end`` use Python string offsets.  A document-level rule
    without a concrete token (for example ``NO_METRIC``) uses ``-1`` for both.
    ``flag`` is retained for callers of the v1 static scanner; ``rule`` is the
    stable, more specific rule identifier for new integrations.
    """

    flag: str
    description: str
    offset: int
    end: int
    snippet: str
    rule: str
    mode: ScanMode
    severity: float
    hard: bool
    soft: bool

    def __post_init__(self) -> None:
        if self.hard == self.soft:
            raise ValueError("ScanHit 必须且只能标记为 hard 或 soft")
        if not 0.0 <= self.severity <= 1.0:
            raise ValueError("ScanHit.severity 必须在 0 到 1 之间")

    def to_dict(self) -> dict[str, Any]:
        """Return the compatibility shape plus the v1.4.2 context fields."""

        return {
            "flag": self.flag,
            "desc": self.description,
            "description": self.description,
            "offset": self.offset,
            "end": self.end,
            "snippet": self.snippet,
            "rule": self.rule,
            "mode": self.mode.value,
            "severity": self.severity,
            "hard": self.hard,
            "soft": self.soft,
        }


@dataclass(frozen=True)
class ScanResult:
    """Structured scanner result with a v1-compatible dictionary adapter."""

    mode: ScanMode
    text_length: int
    hits: tuple[ScanHit, ...] = ()
    penalty: float = 1.0

    @property
    def flags(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(hit.flag for hit in self.hits))

    @property
    def details(self) -> tuple[dict[str, Any], ...]:
        return tuple(hit.to_dict() for hit in self.hits)

    @property
    def hard_fail(self) -> bool:
        return any(hit.hard for hit in self.hits)

    def to_dict(self) -> dict[str, Any]:
        return {
            "flags": list(self.flags),
            "details": [dict(detail) for detail in self.details],
            "penalty": self.penalty,
            "hard_fail": self.hard_fail,
            "mode": self.mode.value,
            "text_length": self.text_length,
        }
