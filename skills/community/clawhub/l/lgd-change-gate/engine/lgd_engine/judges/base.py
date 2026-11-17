"""DomainJudge Protocol + JudgeVerdict data structures.

Fixed schema (shared with parallel Demo2 line):
    JudgeVerdict = {
        "verdict": "go" | "hold" | "reject",
        "reasons": [{"rule": str, "level": "critical|major|minor", "detail": str}],
        "evidence": [{"kind": str, "ref": str}],
    }
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Protocol, runtime_checkable


VALID_VERDICTS = ("go", "hold", "reject")
VALID_LEVELS = ("critical", "major", "minor")


@dataclass
class Reason:
    rule: str
    level: str
    detail: str

    def __post_init__(self) -> None:
        if self.level not in VALID_LEVELS:
            raise ValueError(f"invalid reason level: {self.level}")


@dataclass
class Evidence:
    kind: str   # e.g. "fda_recall", "fda_510k", "nmpa_recall", "internal_verification"
    ref: str    # e.g. "Z-1924-2025", "K190204", URL, or local doc id


@dataclass
class JudgeVerdict:
    verdict: str                       # go | hold | reject
    reasons: List[Reason] = field(default_factory=list)
    evidence: List[Evidence] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.verdict not in VALID_VERDICTS:
            raise ValueError(f"invalid verdict: {self.verdict}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verdict": self.verdict,
            "reasons": [asdict(r) for r in self.reasons],
            "evidence": [asdict(e) for e in self.evidence],
        }

    @property
    def has_critical(self) -> bool:
        return any(r.level == "critical" for r in self.reasons)


@runtime_checkable
class DomainJudge(Protocol):
    """Every domain adapter implements this. ctx is an input JSON dict."""

    domain: str

    def evaluate(self, ctx: Dict[str, Any]) -> Dict[str, Any]:  # pragma: no cover - protocol
        ...
