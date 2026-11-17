"""Ethics review workflow (module B, v0.6).

Ethics review is a human judgement; this module provides the *workflow* — a
validated state machine with an attributable audit trail — not the judgement
itself. Consistent with the NOMOS kernel, the engine never approves or rejects
autonomously: humans drive every transition, and each one is recorded.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol


class EthicsStatus(str, Enum):
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"


_ETHICS_TRANSITIONS: dict[EthicsStatus, set[EthicsStatus]] = {
    EthicsStatus.PENDING: {
        EthicsStatus.UNDER_REVIEW,
        EthicsStatus.REJECTED,
        EthicsStatus.ESCALATED,
    },
    EthicsStatus.UNDER_REVIEW: {
        EthicsStatus.APPROVED,
        EthicsStatus.REJECTED,
        EthicsStatus.ESCALATED,
    },
    EthicsStatus.ESCALATED: {
        EthicsStatus.UNDER_REVIEW,
        EthicsStatus.APPROVED,
        EthicsStatus.REJECTED,
    },
    EthicsStatus.APPROVED: set(),
    EthicsStatus.REJECTED: set(),
}


@dataclass
class EthicsReviewCase:
    case_id: str
    subject_id: str
    concern: str
    status: EthicsStatus = EthicsStatus.PENDING
    reviewers: list[str] = field(default_factory=list)
    decision_note: str | None = None
    history: list[dict[str, str]] = field(default_factory=list)


class EthicsReviewWorkflow(Protocol):
    id: str

    def open(self, case: EthicsReviewCase) -> EthicsReviewCase: ...
    def advance(
        self, case_id: str, to: EthicsStatus, reviewer: str = "", note: str = ""
    ) -> EthicsReviewCase: ...
    def get(self, case_id: str) -> EthicsReviewCase | None: ...


class InMemoryEthicsReview:
    """In-memory ethics review workflow (deterministic, zero dependency)."""

    id = "in-memory-ethics-review"

    def __init__(self) -> None:
        self._cases: dict[str, EthicsReviewCase] = {}

    def open(self, case: EthicsReviewCase) -> EthicsReviewCase:
        if case.case_id in self._cases:
            raise ValueError(f"ethics case already open: {case.case_id}")
        self._cases[case.case_id] = case
        return case

    def advance(
        self,
        case_id: str,
        to: EthicsStatus,
        reviewer: str = "",
        note: str = "",
    ) -> EthicsReviewCase:
        case = self._require(case_id)
        target = EthicsStatus(to)
        if target not in _ETHICS_TRANSITIONS[case.status]:
            raise ValueError(
                f"illegal ethics transition: {case.status.value} -> {target.value}"
            )
        previous = case.status.value
        case.status = target
        if reviewer and reviewer not in case.reviewers:
            case.reviewers.append(reviewer)
        if note:
            case.decision_note = note
        case.history.append(
            {"from": previous, "to": target.value, "reviewer": reviewer, "note": note}
        )
        return case

    def get(self, case_id: str) -> EthicsReviewCase | None:
        return self._cases.get(case_id)

    def all(self) -> list[EthicsReviewCase]:
        return [self._cases[k] for k in sorted(self._cases)]

    def _require(self, case_id: str) -> EthicsReviewCase:
        case = self._cases.get(case_id)
        if case is None:
            raise KeyError(f"unknown ethics case: {case_id}")
        return case


__all__ = [
    "EthicsReviewCase",
    "EthicsReviewWorkflow",
    "EthicsStatus",
    "InMemoryEthicsReview",
]
