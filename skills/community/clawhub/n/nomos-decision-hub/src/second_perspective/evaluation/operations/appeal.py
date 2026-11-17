"""Appeal workflow (module C, v0.6) — in-memory state machine.

Enforces the legal transition graph so a dispute cannot jump straight from
``FILED`` to ``RESOLVED``; every illegal move raises instead of silently
corrupting the case state.
"""

from __future__ import annotations

from .base import AppealCase, AppealStatus

_APPEAL_TRANSITIONS: dict[AppealStatus, set[AppealStatus]] = {
    AppealStatus.FILED: {AppealStatus.TRIAGED, AppealStatus.REJECTED},
    AppealStatus.TRIAGED: {AppealStatus.UNDER_REVIEW, AppealStatus.REJECTED},
    AppealStatus.UNDER_REVIEW: {AppealStatus.RESOLVED, AppealStatus.REJECTED},
    AppealStatus.RESOLVED: set(),
    AppealStatus.REJECTED: set(),
}


class InMemoryAppealWorkflow:
    id = "in-memory-appeal-workflow"

    def __init__(self) -> None:
        self._cases: dict[str, AppealCase] = {}

    def file(self, case: AppealCase) -> AppealCase:
        if case.case_id in self._cases:
            raise ValueError(f"appeal already filed: {case.case_id}")
        self._cases[case.case_id] = case
        return case

    def advance(
        self, case_id: str, to: AppealStatus, note: str = ""
    ) -> AppealCase:
        case = self._require(case_id)
        target = AppealStatus(to)
        if target not in _APPEAL_TRANSITIONS[case.status]:
            raise ValueError(
                f"illegal appeal transition: {case.status.value} -> {target.value}"
            )
        case.status = target
        if note:
            case.resolution = note
        return case

    def get(self, case_id: str) -> AppealCase | None:
        return self._cases.get(case_id)

    def all(self) -> list[AppealCase]:
        return [self._cases[k] for k in sorted(self._cases)]

    def _require(self, case_id: str) -> AppealCase:
        case = self._cases.get(case_id)
        if case is None:
            raise KeyError(f"unknown appeal case: {case_id}")
        return case


__all__ = ["InMemoryAppealWorkflow"]
