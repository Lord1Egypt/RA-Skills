"""Robustness analysis — Pareto frontier and weight sensitivity.

Deterministic checks that identify fragile criteria and stable leaders
under declared weight perturbations.
"""

from __future__ import annotations

from decimal import Decimal

from ..models.enums import ScoringRule
from ..models.schemas import (
    AlternativeEvaluation,
    DecisionRequest,
    RobustnessReport,
    SensitivityCase,
)


def analyze_robustness(
    request: DecisionRequest,
    evaluations: list[AlternativeEvaluation],
    leading_ids: list[str],
    sensitivity_delta: Decimal,
) -> RobustnessReport:
    """Compute Pareto frontier, run weight sensitivity, and identify fragile criteria.

    The engine never invents perturbation ranges — it uses the declared
    `sensitivity_delta` from the policy.
    """
    # ── Pareto frontier: alternatives not dominated by any other ──
    pareto_ids = _compute_pareto_frontier(evaluations, request)

    # ── Weight sensitivity ──
    sensitivity_cases: list[SensitivityCase] = []
    fragile_ids: set[str] = set()

    if request.evaluation_mode.value == "weighted" and request.criteria:
        # Baseline scores
        score_map = {e.alternative_id: e.total_score for e in evaluations if e.total_score is not None}

        for criterion in request.criteria:
            for direction in ("up", "down"):
                adjustment = sensitivity_delta if direction == "up" else -sensitivity_delta
                adjusted = min(max(criterion.weight + adjustment, Decimal("0")), Decimal("1"))

                # Redistribute to keep sum = 1
                remaining = [c for c in request.criteria if c.id != criterion.id]
                total_other = sum(c.weight for c in remaining)
                if total_other == Decimal("0"):
                    adjusted_weights = {
                        c.id: (Decimal("1") - adjusted) / len(remaining) if remaining else Decimal("0")
                        for c in remaining
                    }
                else:
                    scale = (Decimal("1") - adjusted) / total_other
                    adjusted_weights = {
                        c.id: c.weight * scale for c in remaining
                    }
                adjusted_weights[criterion.id] = adjusted

                # Recompute scores
                alt_scores: dict[str, Decimal] = {}
                for alt_eval in evaluations:
                    score = Decimal("0")
                    for cs in alt_eval.criterion_scores:
                        w = adjusted_weights[cs.criterion_id]
                        score += cs.normalized_score * w
                    alt_scores[alt_eval.alternative_id] = score

                # Determine leading candidates under adjusted weights
                sorted_alts = sorted(alt_scores.items(), key=lambda x: x[1], reverse=True)
                adjusted_leading = [alt_id for alt_id, _ in sorted_alts[:len(leading_ids)]] if leading_ids else (
                    [sorted_alts[0][0]] if sorted_alts else []
                )

                if set(adjusted_leading) != set(leading_ids):
                    fragile_ids.add(criterion.id)

                sensitivity_cases.append(
                    SensitivityCase(
                        criterion_id=criterion.id,
                        direction=direction,
                        adjusted_weight=adjusted,
                        adjusted_weights=adjusted_weights,
                        alternative_scores=alt_scores,
                        leading_candidate_ids=adjusted_leading,
                    )
                )

    # ── Stable leaders: appear in the leading set under all perturbations ──
    leading_set = set(leading_ids)
    if sensitivity_cases:
        stable = leading_set.copy()
        for case in sensitivity_cases:
            stable &= set(case.leading_candidate_ids)
        stable_ids = sorted(stable)
    else:
        stable_ids = sorted(leading_set)

    # ── Ranking stability — fraction of sensitivity cases where the top-1
    #     candidate did not change ──
    if sensitivity_cases and leading_ids:
        top1 = leading_ids[0]
        stable_count = sum(1 for case in sensitivity_cases if case.leading_candidate_ids and case.leading_candidate_ids[0] == top1)
        ranking_stability = Decimal(stable_count) / Decimal(len(sensitivity_cases))
    else:
        ranking_stability = Decimal("1") if leading_ids else None

    return RobustnessReport(
        pareto_frontier_ids=pareto_ids,
        sensitivity_cases=sensitivity_cases,
        fragile_criterion_ids=sorted(fragile_ids),
        stable_leader_ids=stable_ids,
        ranking_stability=ranking_stability,
    )


def _compute_pareto_frontier(
    evaluations: list[AlternativeEvaluation],
    request: DecisionRequest,
) -> list[str]:
    """Compute the Pareto frontier: alternatives not dominated by any other.

    An alternative A dominates B if A is at least as good as B on all criteria
    and strictly better on at least one.
    """
    if not request.criteria:
        return [e.alternative_id for e in evaluations if e.status.value == "eligible"]

    # Build score matrix: {alternative_id: {criterion_id: normalized_score}}
    scores: dict[str, dict[str, Decimal]] = {}
    for eval_ in evaluations:
        if eval_.status.value == "eligible":
            scores[eval_.alternative_id] = {
                cs.criterion_id: cs.normalized_score for cs in eval_.criterion_scores
            }

    pareto: list[str] = []
    for a_id in scores:
        dominated = False
        for b_id in scores:
            if a_id == b_id:
                continue
            a_scores = scores[a_id]
            b_scores = scores[b_id]
            # Check if B dominates A
            at_least_as_good = all(
                b_scores.get(cid, Decimal("0")) >= a_scores.get(cid, Decimal("0"))
                for cid in a_scores
            )
            strictly_better = any(
                b_scores.get(cid, Decimal("0")) > a_scores.get(cid, Decimal("0"))
                for cid in a_scores
            )
            if at_least_as_good and strictly_better:
                dominated = True
                break
        if not dominated:
            pareto.append(a_id)

    return sorted(pareto)