"""Deep-report portal (module C, v0.6) — in-memory index.

Keeps an ordered catalogue of published reports per subject, each carrying the
digest of its reproducible raw records.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReportRef:
    report_id: str
    subject_id: str
    title: str
    digest: str
    created_at: str = ""  # ISO-8601 string
    path: str | None = None


class InMemoryReportPortal:
    id = "in-memory-report-portal"

    def __init__(self) -> None:
        self._reports: list[ReportRef] = []

    def add(self, ref: ReportRef) -> None:
        self._reports.append(ref)

    def index(self, subject_id: str) -> list[ReportRef]:
        return [r for r in self._reports if r.subject_id == subject_id]

    def latest(self, subject_id: str) -> ReportRef | None:
        items = self.index(subject_id)
        return items[-1] if items else None

    def all(self) -> list[ReportRef]:
        return list(self._reports)


__all__ = ["InMemoryReportPortal", "ReportRef"]
