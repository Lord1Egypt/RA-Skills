from __future__ import annotations

import logging
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from ..audit.auditor import StructuralAuditor
from ..audit.execution import build_execution_audit
from ..models.enums import (
    AlternativeStatus,
    DecisionStatus,
    IssueSeverity,
)
from ..models.schemas import (
    AuditIssue,
    DecisionRequest,
    DecisionResult,
    FailureBranch,
)
from ..version import VERSION
from .causal import invalidation_closure
from .counterfactual import analyze_counterfactuals
from .evaluator import evaluate_alternative
from .integrity import fingerprint_request
from .policy import DecisionPolicy
from .robustness import analyze_robustness
from .selection import select_leading_candidates

ENGINE_VERSION = VERSION

logger = logging.getLogger(__name__)


class IntelligentDecisionEngine:
    """
    Deterministic evaluator.

    It never invents weights, evidence, thresholds, owners, or missing metrics.
    It produces leading candidates under supplied parameters, then requires
    a separate human approval record.
    """

    def __init__(
        self,
        auditor: StructuralAuditor | None = None,
        policy: DecisionPolicy | None = None,
    ):
        self.auditor = auditor or StructuralAuditor()
        self.policy = policy or DecisionPolicy()

    def evaluate(self, request: DecisionRequest) -> DecisionResult:
        decision_id = request.decision_id or f"DEC-{uuid4().hex[:12].upper()}"
        evaluation_as_of = request.evaluation_as_of or datetime.now(timezone.utc)
        request = request.model_copy(
            update={
                "decision_id": decision_id,
                "evaluation_as_of": evaluation_as_of,
            }
        )

        issues, responsibility_map, unresolved = self.auditor.audit(
            request,
            self.policy,
            evaluation_as_of,
        )
        evaluations = [
            evaluate_alternative(request, alternative)
            for alternative in request.alternatives
        ]

        for evaluation in evaluations:
            for metric in evaluation.missing_metrics:
                path = f"alternatives.{evaluation.alternative_id}.metrics.{metric}"
                issues.append(
                    AuditIssue(
                        code="MISSING_METRIC",
                        severity=IssueSeverity.ERROR,
                        path=path,
                        message="Required metric is absent; deterministic evaluation cannot continue.",
                        blocking=self.policy.require_all_alternatives_complete,
                    )
                )
                unresolved.append(path)

            for evidence_id in evaluation.unavailable_evidence_ids:
                path = f"alternatives.{evaluation.alternative_id}.evidence_ids.{evidence_id}"
                issues.append(
                    AuditIssue(
                        code="ALTERNATIVE_EVIDENCE_UNAVAILABLE",
                        severity=IssueSeverity.ERROR,
                        path=path,
                        message="Alternative evidence is missing or disputed.",
                        blocking=self.policy.require_all_alternatives_complete,
                    )
                )
                unresolved.append(path)

        eligible = [
            evaluation
            for evaluation in evaluations
            if evaluation.status == AlternativeStatus.ELIGIBLE
        ]
        eligible_ids = [evaluation.alternative_id for evaluation in eligible]

        leading_ids = select_leading_candidates(request, evaluations)

        failure_branches = self._build_failure_branches(request, leading_ids)
        counterfactuals = analyze_counterfactuals(
            request,
            evaluations,
            leading_ids,
            failure_branches,
        )
        robustness = analyze_robustness(
            request,
            evaluations,
            leading_ids,
            self.policy.sensitivity_delta,
        )

        blocking = any(issue.blocking for issue in issues)
        incomplete = any(
            item.status == AlternativeStatus.INCOMPLETE for item in evaluations
        )
        if blocking or (incomplete and self.policy.require_all_alternatives_complete):
            status = DecisionStatus.EVIDENCE_PENDING
        elif not eligible:
            status = DecisionStatus.AUDIT_FAILED
        else:
            status = DecisionStatus.HUMAN_APPROVAL_REQUIRED

        audit_passed = status == DecisionStatus.HUMAN_APPROVAL_REQUIRED
        logger.info(
            "evaluate done decision_id=%s status=%s audit_passed=%s issues=%d alternatives=%d leading=%d unresolved=%d",
            decision_id,
            status.value,
            audit_passed,
            len(issues),
            len(evaluations),
            len(leading_ids),
            len(unresolved),
        )
        trace = [
            {
                "stage": "audit",
                "rule_id": "STRUCTURAL_AUDIT",
                "message": f"Structural audit produced {len(issues)} issue(s).",
                "references": sorted({issue.code for issue in issues}),
            },
            {
                "stage": "evaluation",
                "rule_id": "DETERMINISTIC_EVALUATION",
                "message": f"Evaluated {len(evaluations)} alternative(s).",
                "references": [item.alternative_id for item in evaluations],
            },
            {
                "stage": "counterfactual",
                "rule_id": "ASSUMPTION_FAILURE_RESELECTION",
                "message": f"Recomputed {len(counterfactuals)} assumption-failure scenario(s).",
                "references": [item.trigger_assumption_id for item in counterfactuals],
            },
            {
                "stage": "robustness",
                "rule_id": "PARETO_AND_WEIGHT_SENSITIVITY",
                "message": "Computed Pareto exposure and deterministic weight perturbations.",
                "references": robustness.fragile_criterion_ids,
            },
            {
                "stage": "governance",
                "rule_id": "HUMAN_APPROVAL_GATE",
                "message": f"Decision state resolved to {status}.",
                "references": [request.decision_owner.owner],
            },
        ]

        policy_snapshot = self.policy.snapshot()
        input_fingerprint = fingerprint_request(request)
        ledger = build_execution_audit(
            request=request,
            input_fingerprint=input_fingerprint,
            issues=issues,
            evaluations=evaluations,
            failure_branches=failure_branches,
            counterfactuals=counterfactuals,
            robustness=robustness,
            leading_candidate_ids=leading_ids,
            status=status,
            policy=policy_snapshot,
        )

        return DecisionResult(
            decision_id=decision_id,
            status=status,
            objective=request.objective,
            evaluation_mode=request.evaluation_mode,
            audit_passed=audit_passed,
            issues=issues,
            alternatives=evaluations,
            eligible_alternative_ids=eligible_ids,
            leading_candidate_ids=leading_ids,
            failure_branches=failure_branches,
            responsibility_map=responsibility_map,
            unresolved_variables=sorted(set(unresolved)),
            robustness=robustness,
            counterfactuals=counterfactuals,
            trace=trace,
            algorithm_audit=ledger.events,
            algorithm_audit_root_hash=ledger.root_hash,
            policy=policy_snapshot,
            engine_version=ENGINE_VERSION,
            input_fingerprint=input_fingerprint,
            evaluation_as_of=evaluation_as_of,
            human_approval_required=True,
            generated_at=evaluation_as_of,
        )

    @staticmethod
    def _build_failure_branches(
        request: DecisionRequest,
        leading_ids: list[str],
    ) -> list[FailureBranch]:
        branches: list[FailureBranch] = []
        leading_set = set(leading_ids)
        total_candidates = len(leading_ids)

        for assumption in request.assumptions:
            if not assumption.critical:
                continue

            invalidated, affected = invalidation_closure(request, assumption.id)
            affected_leading = sorted(leading_set.intersection(affected))
            ratio = (
                Decimal(len(affected_leading)) / Decimal(total_candidates)
                if total_candidates
                else Decimal("0")
            ).quantize(Decimal("0.000001"))

            effect = (
                "The affected alternatives lose their declared validity basis; "
                "their eligibility must be recomputed before approval."
            )
            branches.append(
                FailureBranch(
                    assumption_id=assumption.id,
                    expression=f"¬{assumption.id} ⇒ ΔD",
                    invalidated_assumption_ids=invalidated,
                    affected_alternative_ids=affected,
                    affected_leading_candidate_ids=affected_leading,
                    candidate_exposure_ratio=ratio,
                    structural_effect=effect,
                )
            )

        return branches
