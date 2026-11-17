"""Information priority queue — structured prioritisation of missing information.

Identifies and prioritises information gaps that need to be filled before
a decision can be approved.  Every priority is derived from declared inputs.
"""

from __future__ import annotations

from ..models.enums import InformationPriorityTier, IssueSeverity
from ..models.hub import InformationPriority
from ..models.schemas import DecisionRequest, DecisionResult


def build_information_priorities(
    request: DecisionRequest,
    result: DecisionResult,
) -> list[InformationPriority]:
    """Build a prioritised queue of information items.

    Tiers:
      - BLOCKING: missing evidence or metrics that block evaluation.
      - LEADER_EXPOSED: information gaps affecting leading candidates.
      - STRUCTURAL: structural weaknesses in the decision structure.
      - REVIEW: items for human review.
    """
    priorities: list[InformationPriority] = []

    leading_set = set(result.leading_candidate_ids)

    # ── BLOCKING: unresolved variables ──
    for var in result.unresolved_variables:
        priorities.append(
            InformationPriority(
                tier=InformationPriorityTier.BLOCKING.value,
                item=f"Unresolved path: {var}",
                rationale="This variable is missing; deterministic evaluation cannot proceed without it.",
                alternative_ids=sorted(leading_set) if leading_set else [],
                responsibility=request.decision_owner.owner,
            )
        )

    # ── BLOCKING: audit issues ──
    for issue in result.issues:
        if issue.blocking:
            priorities.append(
                InformationPriority(
                    tier=InformationPriorityTier.BLOCKING.value,
                    item=f"[{issue.code}] {issue.message}",
                    rationale=f"Path: {issue.path}",
                    alternative_ids=[],
                    responsibility=request.decision_owner.owner,
                )
            )

    # ── LEADER_EXPOSED: leading candidates with missing metrics ──
    for alt_eval in result.alternatives:
        if alt_eval.alternative_id in leading_set and alt_eval.missing_metrics:
            priorities.append(
                InformationPriority(
                    tier=InformationPriorityTier.LEADER_EXPOSED.value,
                    item=f"Leading candidate {alt_eval.alternative_id} missing metrics: "
                         + ", ".join(alt_eval.missing_metrics),
                    rationale="Leading candidate scores are incomplete, affecting ranking reliability.",
                    alternative_ids=[alt_eval.alternative_id],
                )
            )

    # ── STRUCTURAL: fragile criteria ──
    for cid in result.robustness.fragile_criterion_ids:
        priorities.append(
            InformationPriority(
                tier=InformationPriorityTier.STRUCTURAL.value,
                item=f"Fragile criterion: {cid}",
                rationale="Weight perturbation on this criterion changes the leading candidate set.",
                alternative_ids=sorted(leading_set),
            )
        )

    # ── STRUCTURAL: counterfactual decision changes ──
    for cf in result.counterfactuals:
        if cf.decision_changed:
            priorities.append(
                InformationPriority(
                    tier=InformationPriorityTier.STRUCTURAL.value,
                    item=f"Counterfactual risk: assumption {cf.trigger_assumption_id} failure changes decision",
                    rationale=(
                        f"Removed alternatives: {cf.removed_alternative_ids}; "
                        f"counterfactual leaders: {cf.counterfactual_leading_candidate_ids}"
                    ),
                    alternative_ids=cf.removed_alternative_ids,
                )
            )

    # ── REVIEW: non-blocking warnings ──
    for issue in result.issues:
        if not issue.blocking and issue.severity in (IssueSeverity.WARNING, IssueSeverity.ERROR):
            priorities.append(
                InformationPriority(
                    tier=InformationPriorityTier.REVIEW.value,
                    item=f"[{issue.severity.value}] {issue.code}: {issue.message}",
                    rationale=issue.path,
                    alternative_ids=[],
                )
            )

    return priorities