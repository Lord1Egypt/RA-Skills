"""Assumption interaction layer — v0.4 upgrade (G1: first-order gap).

Extends the first-order ¬A ⇒ ΔD causal model with interaction-aware joint
effects: ¬(A1 ∧ A2) ⇒ ΔD_amplified, ¬(A1 ∨ A2) ⇒ ΔD_redundant.

Design invariants (I-1 through I-4):
  I-1  Non-conjectural   — interaction strength Δ must be explicitly declared;
                           the engine never estimates or learns it.
  I-2  Order conservation — every member of an interaction must exist in the
                           declared assumption set.
  I-3  Effect boundedness — cumulative interaction effect ≤
                           amplification_ceiling × Σ|first-order effects|.
  I-4  Monotonicity       — adding failed assumptions never revokes a triggered
                           interaction (union semantics).
"""

from .model import (
    AssumptionInteraction,
    InteractionEffect,
    InteractionDeclaration,
)
from .invariants import InvariantViolation, validate_all
from .engine import InteractionEngine

__all__ = [
    "AssumptionInteraction",
    "InteractionEffect",
    "InteractionDeclaration",
    "InvariantViolation",
    "validate_all",
    "InteractionEngine",
]
