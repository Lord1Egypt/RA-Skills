"""Convergence checker — classifies a round into one of five states.

The checker is *pure*: given the same inputs it always returns the same
ConvergenceResult.  It does not mutate any state.

Decision order (highest priority first):

  1. BLOCKED           — if blocked flag is set
  2. BUDGET_EXHAUSTED  — if any budget is exhausted AND not converged
  3. FIXED_POINT       — if candidate set is identical to previous round
  4. NO_GAIN           — if no unresolved branches remain
  5. DIVERGED          — otherwise (still changing, budget available)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from .propositions import proposition_fixed_point, proposition_termination
from .types import ConvergenceResult, ConvergenceStatus


@dataclass
class ConvergenceChecker:
    """Evaluates convergence state from round metrics.

    Parameters
    ----------
    max_iterations : int
        Total iteration budget.
    max_evidence_requests : int
        Total evidence-request budget.
    """

    max_iterations: int
    max_evidence_requests: int

    def __post_init__(self) -> None:
        ok, reason = proposition_termination(
            self.max_iterations, self.max_evidence_requests
        )
        if not ok:
            raise ValueError(f"ConvergenceChecker: {reason}")

    # -- main API ---------------------------------------------------------

    def evaluate(
        self,
        round_index: int,
        candidate_set_prev: Iterable[str],
        candidate_set_curr: Iterable[str],
        iterations_used: int,
        evidence_requests_used: int,
        unresolved_branches: int = 0,
        blocked: bool = False,
        blocking_reasons: Optional[Iterable[str]] = None,
    ) -> ConvergenceResult:
        """Classify the current round's convergence status.

        Decision order: BLOCKED > BUDGET_EXHAUSTED > FIXED_POINT > NO_GAIN > DIVERGED.
        """
        prev = frozenset(candidate_set_prev)
        curr = frozenset(candidate_set_curr)
        blocking = tuple(blocking_reasons or ())

        # 1. Blocked?
        if blocked:
            return ConvergenceResult(
                status=ConvergenceStatus.BLOCKED,
                round_index=round_index,
                candidate_set_prev=prev,
                candidate_set_curr=curr,
                iterations_used=iterations_used,
                iterations_max=self.max_iterations,
                evidence_requests_used=evidence_requests_used,
                evidence_requests_max=self.max_evidence_requests,
                unresolved_branches=unresolved_branches,
                blocked=True,
                blocking_reasons=blocking,
            )

        budget_exhausted = (
            iterations_used >= self.max_iterations
            or evidence_requests_used >= self.max_evidence_requests
        )

        # Fixed point check (P-2) — done regardless of budget so the
        # classification is correct even when budget happens to coincide
        # with a fixed point.
        fp_holds, _ = proposition_fixed_point(prev, curr)

        # 2. Budget exhausted AND not a true fixed point?
        if budget_exhausted and not fp_holds:
            return ConvergenceResult(
                status=ConvergenceStatus.BUDGET_EXHAUSTED,
                round_index=round_index,
                candidate_set_prev=prev,
                candidate_set_curr=curr,
                iterations_used=iterations_used,
                iterations_max=self.max_iterations,
                evidence_requests_used=evidence_requests_used,
                evidence_requests_max=self.max_evidence_requests,
                unresolved_branches=unresolved_branches,
                blocked=False,
            )

        # 3. Fixed point?
        if fp_holds:
            return ConvergenceResult(
                status=ConvergenceStatus.FIXED_POINT,
                round_index=round_index,
                candidate_set_prev=prev,
                candidate_set_curr=curr,
                iterations_used=iterations_used,
                iterations_max=self.max_iterations,
                evidence_requests_used=evidence_requests_used,
                evidence_requests_max=self.max_evidence_requests,
                unresolved_branches=unresolved_branches,
                blocked=False,
            )

        # 4. No gain (all branches resolved)?
        if unresolved_branches <= 0:
            return ConvergenceResult(
                status=ConvergenceStatus.NO_GAIN,
                round_index=round_index,
                candidate_set_prev=prev,
                candidate_set_curr=curr,
                iterations_used=iterations_used,
                iterations_max=self.max_iterations,
                evidence_requests_used=evidence_requests_used,
                evidence_requests_max=self.max_evidence_requests,
                unresolved_branches=0,
                blocked=False,
            )

        # 5. Still diverging.
        return ConvergenceResult(
            status=ConvergenceStatus.DIVERGED,
            round_index=round_index,
            candidate_set_prev=prev,
            candidate_set_curr=curr,
            iterations_used=iterations_used,
            iterations_max=self.max_iterations,
            evidence_requests_used=evidence_requests_used,
            evidence_requests_max=self.max_evidence_requests,
            unresolved_branches=unresolved_branches,
            blocked=False,
        )

    # -- convenience ------------------------------------------------------

    def is_true_convergence(
        self,
        round_index: int,
        candidate_set_prev: Iterable[str],
        candidate_set_curr: Iterable[str],
        iterations_used: int,
        evidence_requests_used: int,
        unresolved_branches: int = 0,
        blocked: bool = False,
        blocking_reasons: Optional[Iterable[str]] = None,
    ) -> bool:
        """Shorthand: return True iff the status represents true convergence
        (FIXED_POINT or NO_GAIN).

        This is the guard against callers misclassifying "budget exhausted"
        as "converged" — the single most common semantic error in
        iterative audit systems.
        """
        result = self.evaluate(
            round_index=round_index,
            candidate_set_prev=candidate_set_prev,
            candidate_set_curr=candidate_set_curr,
            iterations_used=iterations_used,
            evidence_requests_used=evidence_requests_used,
            unresolved_branches=unresolved_branches,
            blocked=blocked,
            blocking_reasons=blocking_reasons,
        )
        return result.is_true_convergence
