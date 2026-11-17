from __future__ import annotations

from threading import RLock
from typing import Protocol

from ..models.hub import HubReport
from ..models.schemas import ReconstructionSession
from .integrity import verify_hub_report


class HubReportRepository(Protocol):
    def put(self, report: HubReport) -> None: ...

    def get(self, hub_run_id: str) -> HubReport | None: ...


class InMemoryHubReportRepository:
    """Immutable development store for sealed Hub reports."""

    def __init__(self) -> None:
        self._reports: dict[str, HubReport] = {}
        self._lock = RLock()

    def put(self, report: HubReport) -> None:
        with self._lock:
            if not verify_hub_report(report):
                raise ValueError("Hub report fails integrity verification")
            if report.hub_run_id in self._reports:
                raise ValueError(f"Hub report {report.hub_run_id} already exists")
            self._reports[report.hub_run_id] = report.model_copy(deep=True)

    def get(self, hub_run_id: str) -> HubReport | None:
        with self._lock:
            report = self._reports.get(hub_run_id)
            if report is None:
                return None
            if not verify_hub_report(report):
                raise ValueError(f"integrity verification failed for {hub_run_id}")
            return report.model_copy(deep=True)


class SessionRepository(Protocol):
    """Protocol for reconstruction session persistence."""

    def put(self, session: ReconstructionSession) -> None: ...

    def get(self, session_id: str) -> ReconstructionSession | None: ...


class InMemorySessionRepository:
    """In-memory development store for reconstruction sessions."""

    def __init__(self) -> None:
        self._sessions: dict[str, ReconstructionSession] = {}
        self._lock = RLock()

    def put(self, session: ReconstructionSession) -> None:
        with self._lock:
            if session.session_id in self._sessions:
                raise ValueError(f"Session {session.session_id} already exists")
            self._sessions[session.session_id] = session.model_copy(deep=True)

    def update(self, session: ReconstructionSession) -> None:
        """Replace an existing session (immutable revision pattern)."""
        with self._lock:
            if session.session_id not in self._sessions:
                raise ValueError(f"Session {session.session_id} does not exist")
            self._sessions[session.session_id] = session.model_copy(deep=True)

    def get(self, session_id: str) -> ReconstructionSession | None:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return None
            return session.model_copy(deep=True)
