"""Convergence formalization — v0.4 upgrade (G2: heuristic-judgement gap).

Replaces the heuristic string-matching convergence check with three
formally-stated propositions and a five-state classification.

Propositions
------------
P-1  Termination  — finite budgets ⇒ guaranteed termination.
P-2  Fixed point  — candidate set identical across two consecutive rounds
                    ⇒ fixed point (subsequent rounds are constant).
P-3  Effect boundedness — cumulative interaction effect ≤ ceiling × Σ|first-order|.

Classification
--------------
FIXED_POINT     — true convergence, no human required
NO_GAIN         — no unresolved branches, true convergence
BUDGET_EXHAUSTED — ran out of budget, NOT convergence (requires human)
DIVERGED        — still changing with budget remaining
BLOCKED         — hit a blocking condition (requires human)
"""

from .types import (
    ConvergenceStatus,
    ConvergenceResult,
)
from .checker import ConvergenceChecker
from .propositions import (
    proposition_termination,
    proposition_fixed_point,
    proposition_effect_boundedness,
)

__all__ = [
    "ConvergenceStatus",
    "ConvergenceResult",
    "ConvergenceChecker",
    "proposition_termination",
    "proposition_fixed_point",
    "proposition_effect_boundedness",
]
