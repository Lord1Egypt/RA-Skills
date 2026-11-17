"""LLM compliance types — permission tiers and violation model."""

from __future__ import annotations

from enum import IntEnum, StrEnum


class PermissionTier(StrEnum):
    """What an LLM call is allowed to do.

    Higher tiers include lower tiers (T3 includes T2 and T1).
    """

    T1_ANNOTATION = "t1_annotation"
    T2_PROPOSAL = "t2_proposal"
    T3_NARRATIVE = "t3_narrative"

    @property
    def rank(self) -> int:
        return {
            PermissionTier.T1_ANNOTATION: 1,
            PermissionTier.T2_PROPOSAL: 2,
            PermissionTier.T3_NARRATIVE: 3,
        }[self]

    def permits(self, required: "PermissionTier") -> bool:
        """True if this tier's rank is at least *required*."""
        return self.rank >= required.rank


class GuardViolationSeverity(StrEnum):
    """Severity of a guard violation."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class GuardViolationError(Exception):
    """Raised when LLM output violates the compliance guard.

    Attributes
    ----------
    rule : str
        Which invariant was violated (e.g. "L-1", "L-2", "L-3").
    severity : GuardViolationSeverity
        How serious the violation is.  CRITICAL means the output must be
        discarded entirely; lower severities may allow sanitized passthrough.
    detail : str
        Human-readable explanation.
    """

    def __init__(
        self,
        rule: str,
        severity: GuardViolationSeverity,
        detail: str,
    ) -> None:
        super().__init__(f"[{rule} {severity.value}] {detail}")
        self.rule = rule
        self.severity = severity
        self.detail = detail
