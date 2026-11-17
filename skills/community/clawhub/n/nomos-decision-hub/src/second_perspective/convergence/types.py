"""Convergence types — status enum and result dataclass.

Five-state classification (superset of the existing ConvergenceKind):

  FIXED_POINT      candidate set stable — true convergence
  NO_GAIN          no unresolved branches — true convergence
  BUDGET_EXHAUSTED budget ran out — NOT convergence, requires human
  DIVERGED         still changing with budget remaining
  BLOCKED          hit a blocking condition — requires human

The two "true convergence" states (FIXED_POINT, NO_GAIN) have
``is_true_convergence() == True``.  The other three do not.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import FrozenSet


class ConvergenceStatus(StrEnum):
    """Why a session stopped — or whether it should stop."""

    FIXED_POINT = "fixed_point"
    NO_GAIN = "no_gain"
    BUDGET_EXHAUSTED = "budget_exhausted"
    DIVERGED = "diverged"
    BLOCKED = "blocked"

    @property
    def is_true_convergence(self) -> bool:
        """True iff this status represents genuine convergence (not a forced
        stop due to budget or blocking)."""
        return self in (ConvergenceStatus.FIXED_POINT, ConvergenceStatus.NO_GAIN)

    @property
    def requires_human(self) -> bool:
        """True iff a human decision is required before proceeding."""
        return self in (
            ConvergenceStatus.BUDGET_EXHAUSTED,
            ConvergenceStatus.BLOCKED,
        )

    @property
    def is_terminal(self) -> bool:
        """True iff the session should stop (converged or forced stop)."""
        return self != ConvergenceStatus.DIVERGED


@dataclass(frozen=True)
class ConvergenceResult:
    """Full convergence evaluation output.

    Fields
    ------
    status : ConvergenceStatus
        The classified status.
    round_index : int
        0-based index of the round this result corresponds to.
    candidate_set_prev : frozenset[str]
        Leading candidates from the *previous* round (used for fixed-point check).
    candidate_set_curr : frozenset[str]
        Leading candidates from the *current* round.
    iterations_used : int
        Number of iteration budget units consumed so far.
    iterations_max : int
        Total iteration budget.
    evidence_requests_used : int
        Number of evidence requests made so far.
    evidence_requests_max : int
        Total evidence-request budget.
    unresolved_branches : int
        Count of open hypothesis / unexplored branches remaining.
    blocked : bool
        Whether a blocking condition was hit (e.g. structural integrity failure).
    blocking_reasons : tuple[str, ...]
        Human-readable reasons for the blocked state, if any.
    """

    status: ConvergenceStatus
    round_index: int
    candidate_set_prev: FrozenSet[str] = frozenset()
    candidate_set_curr: FrozenSet[str] = frozenset()
    iterations_used: int = 0
    iterations_max: int = 0
    evidence_requests_used: int = 0
    evidence_requests_max: int = 0
    unresolved_branches: int = 0
    blocked: bool = False
    blocking_reasons: tuple[str, ...] = ()

    # -- convenience mirrors of ConvergenceStatus props --------------------

    @property
    def is_true_convergence(self) -> bool:
        return self.status.is_true_convergence

    @property
    def requires_human(self) -> bool:
        return self.status.requires_human

    @property
    def is_terminal(self) -> bool:
        return self.status.is_terminal
