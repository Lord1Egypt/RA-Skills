"""Hub-level models — HubAnalysisRequest, HubReport, and supporting types."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import Field

from .enums import ScenarioOutcomeStatus
from .schemas import (
    AlgorithmAuditEvent,
    CausalReconstructionReport,
    CognitiveAuditReport,
    DecisionRecord,
    DecisionRequest,
    DeviationSignal,
    PolicySnapshot,
    ScenarioDefinition,
    StrictModel,
)


class HubPolicySnapshot(StrictModel):
    """Snapshot of the hub-level policy used during analysis."""

    policy_id: str
    version: str
    max_scenarios: int
    run_causal_reconstruction: bool
    run_cognitive_audit: bool
    build_information_priorities: bool


class ScenarioResult(StrictModel):
    """Result of a single declared-scenario stress run."""

    scenario: ScenarioDefinition
    outcome_status: ScenarioOutcomeStatus
    evaluation_result: object | None = None
    issues: list[str] = Field(default_factory=list)


class InformationPriority(StrictModel):
    """A prioritised information item from the information queue."""

    tier: str
    item: str
    rationale: str
    alternative_ids: list[str] = Field(default_factory=list)
    responsibility: str | None = None


class HubReport(StrictModel):
    """Sealed hub-level report containing all analysis results."""

    hub_run_id: str
    hub_version: str
    decision_record: DecisionRecord
    scenarios: list[ScenarioResult] = Field(default_factory=list)
    cognitive_audit: CognitiveAuditReport | None = None
    causal_reconstruction: CausalReconstructionReport | None = None
    information_priorities: list[InformationPriority] = Field(default_factory=list)
    hub_policy: HubPolicySnapshot
    algorithm_audit_verified: bool
    report_hash: str = Field(default="", pattern=r"^$|^[0-9a-f]{64}$")
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class HubAnalysisRequest(StrictModel):
    """Request body for the Hub analysis endpoint."""

    decision: DecisionRequest
    scenarios: list[ScenarioDefinition] = Field(default_factory=list)
    deviation_signals: list[DeviationSignal] = Field(default_factory=list)
    run_causal_reconstruction: bool = False
    run_cognitive_audit: bool = False