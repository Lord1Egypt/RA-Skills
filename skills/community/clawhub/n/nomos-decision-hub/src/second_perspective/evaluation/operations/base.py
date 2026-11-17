"""Institution product & operations protocols (module C — placeholders, v0.6).

Covers the operating-body surface: public leaderboard, deep-report portal,
appeal workflow, and version-drift monitoring scheduling. Each is declared as a
Protocol with a minimal dataclass model; concrete implementations (hosting,
database, cron) are operational concerns living outside the deterministic kernel.

Status: interface placeholder. The dataclasses here are usable as-is; the
Protocols describe what an operating body must implement.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Protocol


class AppealStatus(str, Enum):
    FILED = "FILED"
    TRIAGED = "TRIAGED"
    UNDER_REVIEW = "UNDER_REVIEW"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"


@dataclass
class AppealCase:
    """A dispute filed against an audit conclusion or score."""

    case_id: str
    subject_id: str
    claim: str
    status: AppealStatus = AppealStatus.FILED
    evidence_refs: list[str] = field(default_factory=list)
    resolution: str | None = None


@dataclass(frozen=True)
class LeaderboardEntry:
    """One row of the public leaderboard (structure-audit axis)."""

    subject_id: str
    as_of: datetime
    scores: dict[str, float]
    composite: float | None = None
    evidence_digest: str | None = None  # links back to reproducible raw records


@dataclass(frozen=True)
class DriftSchedule:
    """A recurring re-evaluation schedule for version-drift monitoring."""

    subject_id: str
    cadence: str  # e.g. "daily" / "weekly" / cron expression
    corpus_id: str
    corpus_digest: str
    last_run: datetime | None = None
    enabled: bool = True


class Leaderboard(Protocol):
    id: str

    def publish(self, entry: LeaderboardEntry) -> None: ...
    def top(self, n: int) -> list[LeaderboardEntry]: ...


class ReportPortal(Protocol):
    id: str

    def index(self, subject_id: str) -> list[dict[str, Any]]: ...


class AppealWorkflow(Protocol):
    id: str

    def file(self, case: AppealCase) -> AppealCase: ...
    def advance(
        self, case_id: str, to: AppealStatus, note: str = ""
    ) -> AppealCase: ...


class DriftScheduler(Protocol):
    id: str

    def register(self, schedule: DriftSchedule) -> None: ...
    def due(self, now: datetime) -> list[DriftSchedule]: ...


__all__ = [
    "AppealCase",
    "AppealStatus",
    "AppealWorkflow",
    "DriftSchedule",
    "DriftScheduler",
    "Leaderboard",
    "LeaderboardEntry",
    "ReportPortal",
]
