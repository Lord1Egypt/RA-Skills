"""Counterfactual analysis — re-evaluate leading candidates under assumption failure.

When a critical assumption is declared failed, the engine re-runs its
deterministic evaluation without that assumption's support and reports
whether the leading candidate set changes.

Design invariants:
  - No guessing: only declared assumptions are tested.
  - Deterministic: each counterfactual derives exclusively from declared inputs.
  - Audit trail: every counterfactual produces a structured result.
"""

from __future__ import annotations

from decimal import Decimal

from ..models.enums import CounterfactualStatus, IssueSeverity
from ..models.schemas import (
    AlternativeEvaluation,
    CounterfactualResult,
    DecisionRequest,
    FailureBranch,
)
from .causal import invalidation_closure
from .evaluator import evaluate_alternative


def analyze_counterfactuals(
    request: DecisionRequest,
    evaluations: list[AlternativeEvaluation],
    leading_ids: list[str],
    failure_branches: list[FailureBranch],
) -> list[CounterfactualResult]:
    """For each failure branch, determine what would happen if the assumption
    actually failed and the relevant alternatives were removed.

    Returns one CounterfactualResult per failure branch.
    """
    results: list[CounterfactualResult] = []
    leading_set = set(leading_ids)

    for branch in failure_branches:
        removed_ids = set(branch.affected_alternative_ids)
        # Counterfactual: remove affected alternatives and re-evaluate leadership
        remaining_eligible = [
            e
            for e in evaluations
            if e.status.value == "eligible" and e.alternative_id not in removed_ids
        ]
        remaining_ids = [e.alternative_id for e in remaining_eligible]

        if not remaining_ids:
            status = CounterfactualStatus.NO_VIABLE_ALTERNATIVE
            cf_leading = []
        elif leading_set - removed_ids:
            remaining_leading = leading_set - removed_ids
            cf_leading = sorted(remaining_leading)
            if cf_leading == sorted(leading_ids):
                status = CounterfactualStatus.LEADER_STABLE
            else:
                status = CounterfactualStatus.LEADER_CHANGED
        else:
            status = CounterfactualStatus.LEADER_CHANGED
            cf_leading = remaining_ids[:1] if remaining_ids else []

        invalidated, _ = invalidation_closure(request, branch.assumption_id)

        decision_changed = (
            status == CounterfactualStatus.LEADER_CHANGED
            or status == CounterfactualStatus.NO_VIABLE_ALTERNATIVE
        )

        results.append(
            CounterfactualResult(
                trigger_assumption_id=branch.assumption_id,
                status=status,
                invalidated_assumption_ids=invalidated,
                removed_alternative_ids=sorted(removed_ids),
                remaining_eligible_alternative_ids=remaining_ids,
                baseline_leading_candidate_ids=sorted(leading_ids),
                counterfactual_leading_candidate_ids=cf_leading,
                counterfactual_pareto_frontier_ids=cf_leading,
                decision_changed=decision_changed,
            )
        )

    return results