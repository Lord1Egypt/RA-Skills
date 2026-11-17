"""Deterministic alternative evaluator.

Evaluates a single alternative against the declared criteria and constraints.
No weights, evidence, thresholds, or missing metrics are invented by the engine.
"""

from __future__ import annotations

import decimal
from decimal import Decimal

from ..models.enums import (
    AlternativeStatus,
    ConstraintKind,
    ConstraintOperator,
    EvaluationMode,
    EvidenceStatus,
    ScoringRule,
)
from ..models.schemas import (
    AlternativeEvaluation,
    ConstraintCheck,
    CriterionScore,
    DecisionRequest,
)


def evaluate_alternative(
    request: DecisionRequest,
    alternative: object,
) -> AlternativeEvaluation:
    """Deterministically evaluate one alternative.

    Returns the evaluation result with constraint checks, criterion scores,
    and lists of missing metrics / unavailable evidence.
    """
    from ..models.schemas import Alternative

    if not isinstance(alternative, Alternative):
        raise TypeError(f"expected Alternative, got {type(alternative).__name__}")

    # ── Check evidence availability ──
    evidence_index = {e.id: e for e in request.evidence}
    unavailable: list[str] = []
    for eid in alternative.evidence_ids:
        ev = evidence_index.get(eid)
        if ev is None or ev.status != EvidenceStatus.SUPPLIED:
            unavailable.append(eid)

    # ── Constraint checks ──
    constraint_checks: list[ConstraintCheck] = []
    hard_passed = True
    for constraint in request.constraints:
        actual = alternative.metrics.get(constraint.metric)
        passed = _check_constraint(constraint.operator, actual, constraint.expected)
        constraint_checks.append(
            ConstraintCheck(
                constraint_id=constraint.id,
                passed=passed,
                actual=actual,
                expected=constraint.expected,
                reason=_constraint_reason(constraint, passed, actual),
            )
        )
        if constraint.kind == ConstraintKind.HARD and not passed:
            hard_passed = False

    # ── Criterion scoring ──
    criterion_scores: list[CriterionScore] = []
    missing_metrics: list[str] = []
    for criterion in request.criteria:
        metric_value = alternative.metrics.get(criterion.metric)
        if metric_value is None:
            missing_metrics.append(criterion.metric)
            continue
        actual = Decimal(str(metric_value))
        normalized = _normalize_score(
            actual,
            criterion.min_value,
            criterion.max_value,
            criterion.scoring_rule,
            criterion.target_value,
        )
        criterion_scores.append(
            CriterionScore(
                criterion_id=criterion.id,
                actual=actual,
                normalized_score=normalized,
                weighted_score=normalized * criterion.weight,
            )
        )

    # ── Composite scoring ──
    if request.evaluation_mode == EvaluationMode.WEIGHTED and criterion_scores:
        base_score = sum(cs.weighted_score for cs in criterion_scores)
    else:
        base_score = None

    # Soft constraint penalty
    soft_penalty = Decimal("0")
    for check in constraint_checks:
        if check.passed is False:
            # Find the constraint to get the penalty
            for c in request.constraints:
                if c.id == check.constraint_id and c.kind == ConstraintKind.SOFT and c.penalty is not None:
                    soft_penalty += c.penalty

    total_score = (base_score - soft_penalty) if base_score is not None else None

    # ── Status determination ──
    if not hard_passed:
        status = AlternativeStatus.INELIGIBLE
    elif missing_metrics or unavailable:
        status = AlternativeStatus.INCOMPLETE
    else:
        status = AlternativeStatus.ELIGIBLE

    return AlternativeEvaluation(
        alternative_id=alternative.id,
        status=status,
        hard_constraints_passed=hard_passed,
        constraint_checks=constraint_checks,
        criterion_scores=criterion_scores,
        base_score=base_score,
        soft_constraint_penalty=soft_penalty,
        total_score=total_score,
        missing_metrics=missing_metrics,
        unavailable_evidence_ids=unavailable,
    )


def _check_constraint(
    operator: ConstraintOperator,
    actual: object,
    expected: object,
) -> bool | None:
    """Check a single constraint. Returns None if actual is missing."""
    if actual is None:
        return None

    # Non-numeric comparison (boolean, string, etc.)
    if operator in (ConstraintOperator.EQ, ConstraintOperator.NE):
        if operator == ConstraintOperator.EQ:
            return actual == expected
        return actual != expected

    # Numeric comparison
    try:
        a = Decimal(str(actual))
        e = Decimal(str(expected)) if expected is not None else Decimal("0")
    except (ValueError, TypeError, decimal.InvalidOperation):
        return None

    ops = {
        ConstraintOperator.GT: lambda: a > e,
        ConstraintOperator.GTE: lambda: a >= e,
        ConstraintOperator.LT: lambda: a < e,
        ConstraintOperator.LTE: lambda: a <= e,
        ConstraintOperator.IN: lambda: str(actual) in (str(x) for x in (expected if isinstance(expected, list) else [expected])),
        ConstraintOperator.NOT_IN: lambda: str(actual) not in (str(x) for x in (expected if isinstance(expected, list) else [expected])),
    }
    handler = ops.get(operator)
    if handler is None:
        return None
    try:
        return handler()
    except Exception:
        return None


def _constraint_reason(constraint: object, passed: bool | None, actual: object) -> str:
    """Human-readable reason for a constraint check result."""
    c = constraint
    if passed is True:
        return f"{c.metric} satisfies {c.operator} {c.expected}"
    if passed is False:
        return f"{c.metric} = {actual} violates {c.operator} {c.expected} (kind={c.kind})"
    return f"{c.metric} could not be evaluated (actual={actual})"


def _normalize_score(
    actual: Decimal,
    min_val: Decimal,
    max_val: Decimal,
    rule: ScoringRule,
    target: Decimal | None = None,
) -> Decimal:
    """Normalise a raw metric value to a 0-1 score."""
    if rule == ScoringRule.HIGHER_IS_BETTER:
        return (actual - min_val) / (max_val - min_val) if max_val != min_val else Decimal("0")
    if rule == ScoringRule.LOWER_IS_BETTER:
        return (max_val - actual) / (max_val - min_val) if max_val != min_val else Decimal("0")
    if rule == ScoringRule.TARGET_IS_BETTER and target is not None:
        distance = abs(actual - target)
        max_dist = max(target - min_val, max_val - target)
        if max_dist == Decimal("0"):
            return Decimal("1")
        return Decimal("1") - (distance / max_dist)
    return Decimal("0")