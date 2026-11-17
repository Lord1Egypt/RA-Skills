"""Leading candidate selection — deterministic ranking.

Selects the leading candidates from the eligible alternatives based on
the evaluation mode.  No weights, thresholds, or tie-breakers are invented.
"""

from __future__ import annotations

from decimal import Decimal

from ..models.enums import AlternativeStatus, EvaluationMode
from ..models.schemas import AlternativeEvaluation, DecisionRequest


def select_leading_candidates(
    request: DecisionRequest,
    evaluations: list[AlternativeEvaluation],
) -> list[str]:
    """Deterministically select leading candidates.

    - CONSTRAINT_ONLY: all eligible alternatives are leading.
    - WEIGHTED: top-scoring eligible alternatives using a simple gap heuristic.
    """
    eligible = [
        e for e in evaluations if e.status == AlternativeStatus.ELIGIBLE
    ]

    if not eligible:
        return []

    if request.evaluation_mode == EvaluationMode.CONSTRAINT_ONLY:
        return sorted(e.alternative_id for e in eligible)

    if request.evaluation_mode == EvaluationMode.WEIGHTED:
        # Sort by total_score descending; those with no score sort last
        scored = [(e, e.total_score or Decimal("-inf")) for e in eligible]
        scored.sort(key=lambda x: x[1], reverse=True)

        if not scored:
            return []

        # Leading: top candidate(s) within a 5% gap of the best score
        best_score = scored[0][1]
        if best_score == Decimal("-inf"):
            return [scored[0][0].alternative_id]

        gap_threshold = abs(best_score) * Decimal("0.05") if best_score != Decimal("0") else Decimal("0.05")
        leading = [
            e.alternative_id
            for e, score in scored
            if (best_score - score) <= gap_threshold
        ]
        return leading

    return sorted(e.alternative_id for e in eligible)