"""Execution audit builder — constructs the hash-chained audit ledger
for a full decision evaluation run.
"""

from __future__ import annotations

from ..audit.ledger import AlgorithmAuditLedger
from ..models.schemas import (
    AlgorithmAuditEvent,
    AlternativeEvaluation,
    CounterfactualResult,
    DecisionRequest,
    FailureBranch,
    RobustnessReport,
    StrictModel,
)


class ExecutionAuditLedger(StrictModel):
    """Sealed audit ledger for a single execution run."""

    events: list[AlgorithmAuditEvent] = []
    root_hash: str | None = None


def build_execution_audit(
    *,
    request: DecisionRequest,
    input_fingerprint: str,
    issues: list,
    evaluations: list[AlternativeEvaluation],
    failure_branches: list[FailureBranch],
    counterfactuals: list[CounterfactualResult],
    robustness: RobustnessReport,
    leading_candidate_ids: list[str],
    status: object,
    policy: object,
) -> ExecutionAuditLedger:
    """Build the hash-chained algorithm audit ledger for a full evaluation.

    Each major evaluation stage appends a deterministic audit event to the
    ledger.  The final `root_hash` is the SHA-256 of the last event's hash.
    """
    ledger = AlgorithmAuditLedger()

    # Stage 1: input fingerprint
    ledger.append(
        stage="evaluation",
        rule_id="INPUT_FINGERPRINT",
        operation="fingerprint_request",
        inputs={"decision_id": request.decision_id},
        output={"input_fingerprint": input_fingerprint},
    )

    # Stage 2: structural audit
    ledger.append(
        stage="audit",
        rule_id="STRUCTURAL_AUDIT",
        operation="structural_audit",
        inputs={"alternative_count": len(request.alternatives)},
        output={"issue_count": len(issues), "blocking_issue_count": sum(1 for i in issues if i.blocking)},
    )

    # Stage 3: alternative evaluation
    eligible_count = sum(1 for e in evaluations if e.status.value == "eligible")
    incomplete_count = sum(1 for e in evaluations if e.status.value == "incomplete")
    ledger.append(
        stage="evaluation",
        rule_id="DETERMINISTIC_EVALUATION",
        operation="evaluate_alternatives",
        inputs={"evaluation_mode": request.evaluation_mode.value},
        output={
            "total_evaluated": len(evaluations),
            "eligible": eligible_count,
            "incomplete": incomplete_count,
        },
    )

    # Stage 4: failure branches
    ledger.append(
        stage="counterfactual",
        rule_id="FAILURE_BRANCHES",
        operation="build_failure_branches",
        inputs={"assumption_count": len(request.assumptions)},
        output={"branch_count": len(failure_branches)},
    )

    # Stage 5: counterfactual analysis
    changed = sum(1 for c in counterfactuals if c.decision_changed)
    ledger.append(
        stage="counterfactual",
        rule_id="COUNTERFACTUAL_ANALYSIS",
        operation="analyze_counterfactuals",
        inputs={"critical_assumption_count": len(failure_branches)},
        output={"counterfactual_count": len(counterfactuals), "decision_changed_count": changed},
    )

    # Stage 6: robustness analysis
    ledger.append(
        stage="robustness",
        rule_id="ROBUSTNESS_ANALYSIS",
        operation="analyze_robustness",
        inputs={"sensitivity_delta": str(policy.sensitivity_delta) if hasattr(policy, "sensitivity_delta") else "0.1"},
        output={
            "pareto_frontier_size": len(robustness.pareto_frontier_ids),
            "fragile_criterion_count": len(robustness.fragile_criterion_ids),
        },
    )

    # Stage 7: leading candidates
    ledger.append(
        stage="selection",
        rule_id="LEADING_CANDIDATE_SELECTION",
        operation="select_leading_candidates",
        inputs={"eligibility_count": len(leading_candidate_ids)},
        output={"leading_candidate_ids": leading_candidate_ids},
    )

    # Stage 8: final status
    ledger.append(
        stage="governance",
        rule_id="DECISION_STATUS",
        operation="determine_status",
        inputs={"audit_passed": True},
        output={"status": status.value},
    )

    return ExecutionAuditLedger(
        events=ledger.events,
        root_hash=ledger.root_hash,
    )