from __future__ import annotations

import logging
from uuid import uuid4

from ..audit.ledger import verify_algorithm_audit
from ..models.hub import HubAnalysisRequest, HubReport
from ..models.schemas import (
    DeltaVar,
    DeviationSignal,
    DecisionRequest,
    ReconstructionSession,
)
from ..service import DecisionService
from ..version import VERSION
from .cognitive import CognitiveRiskScanner
from .information import build_information_priorities
from .integrity import seal_hub_report
from .policy import HubPolicy
from .reconstruction import run_causal_reconstruction
from .repository import (
    HubReportRepository,
    InMemoryHubReportRepository,
    InMemorySessionRepository,
    SessionRepository,
)
from .scenario import analyze_scenarios
from .session import ReconstructionSessionEngine

logger = logging.getLogger(__name__)


class HubReportNotFoundError(LookupError):
    pass


class SessionNotFoundError(LookupError):
    pass


class IntelligentDecisionHub:
    """Orchestrates evaluation, audit, challenge, scenarios, governance records, and sessions."""

    def __init__(
        self,
        service: DecisionService | None = None,
        policy: HubPolicy | None = None,
        repository: HubReportRepository | None = None,
        session_repository: SessionRepository | None = None,
        session_engine: ReconstructionSessionEngine | None = None,
    ) -> None:
        self.service = service or DecisionService()
        self.policy = policy or HubPolicy()
        self.repository = repository or InMemoryHubReportRepository()
        self.session_repository = session_repository or InMemorySessionRepository()
        self.session_engine = session_engine or ReconstructionSessionEngine()
        self.cognitive_scanner = CognitiveRiskScanner(self.policy)

    def analyze(self, request: HubAnalysisRequest) -> HubReport:
        record = self.service.evaluate(request.decision)
        result = record.result
        scenario_results = analyze_scenarios(
            engine=self.service.engine,
            request=record.request,
            baseline=result,
            scenarios=request.scenarios,
        )
        reconstruction = (
            run_causal_reconstruction(record.request, request.deviation_signals)
            if request.run_causal_reconstruction
            else None
        )
        cognitive_report = (
            self.cognitive_scanner.scan(record.request, result)
            if request.run_cognitive_audit
            else None
        )
        report = HubReport(
            hub_run_id=f"HUB-{uuid4().hex[:12].upper()}",
            hub_version=VERSION,
            decision_record=record,
            scenarios=scenario_results,
            cognitive_audit=cognitive_report,
            causal_reconstruction=reconstruction,
            information_priorities=build_information_priorities(record.request, result),
            hub_policy=self.policy.snapshot(),
            algorithm_audit_verified=verify_algorithm_audit(
                result.algorithm_audit,
                result.algorithm_audit_root_hash,
            ),
            generated_at=result.evaluation_as_of,
        )
        report = seal_hub_report(report)
        self.repository.put(report)
        logger.info(
            "hub report sealed hub_run_id=%s decision_id=%s algorithm_audit_verified=%s scenarios=%d findings=%d",
            report.hub_run_id,
            record.result.decision_id,
            report.algorithm_audit_verified,
            len(report.scenarios),
            len(report.cognitive_audit.findings) if report.cognitive_audit else 0,
        )
        return report

    def get_report(self, hub_run_id: str) -> HubReport:
        report = self.repository.get(hub_run_id)
        if report is None:
            raise HubReportNotFoundError(hub_run_id)
        return report

    def start_session(
        self,
        request: DecisionRequest,
        signals: list[DeviationSignal] | None = None,
        *,
        max_iterations: int = 5,
        max_evidence_requests: int = 20,
    ) -> ReconstructionSession:
        """Start a new three-layer reconstruction session."""
        session = self.session_engine.start(
            request,
            signals or [],
            max_iterations=max_iterations,
            max_evidence_requests=max_evidence_requests,
        )
        self.session_repository.put(session)
        return session

    def advance_session(
        self,
        session_id: str,
        delta_vars: list[DeltaVar] | None = None,
    ) -> ReconstructionSession:
        """Advance a session by one round."""
        session = self._get_session(session_id)
        updated = self.session_engine.advance(session, delta_vars)
        self.session_repository.update(updated)
        return updated

    def human_session_decision(
        self,
        session_id: str,
        *,
        approved: bool = False,
        evidence_status: dict[str, str] | None = None,
    ) -> ReconstructionSession:
        """Record a human decision on a session."""
        session = self._get_session(session_id)
        from ..models.enums import AssumptionState
        mapped = {
            k: AssumptionState(v) for k, v in (evidence_status or {}).items()
        } if evidence_status else None
        updated = self.session_engine.human_decision(
            session, approved=approved, evidence_status=mapped,
        )
        self.session_repository.update(updated)
        return updated

    def get_session(self, session_id: str) -> ReconstructionSession:
        return self._get_session(session_id)

    def _get_session(self, session_id: str) -> ReconstructionSession:
        session = self.session_repository.get(session_id)
        if session is None:
            raise SessionNotFoundError(session_id)
        return session
