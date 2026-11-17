"""Interaction engine — computes joint effects under declared interactions.

Core operations
---------------
``triggered(failed_set)``
    Which declared interactions are fully contained in *failed_set*.

``joint_effect(failed_set)``
    Total effect = Σ first-order + Σ triggered Δ, with ceiling applied.

``augment(failed_set, new_failure)``
    Monotonic extension — add *new_failure* and return the new triggered set
    and cumulative effect.  Union semantics guarantees I-4 (monotonicity).

The engine is stateless: every method takes the full declaration and returns
a fresh result.  Stateful usage (e.g. tracking a running failure set) is the
caller's responsibility.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet

from .invariants import validate_all
from .model import (
    AssumptionInteraction,
    InteractionDeclaration,
    InteractionEffect,
)


@dataclass(frozen=True)
class InteractionResult:
    """Outcome of a joint-effect computation."""

    failed_assumptions: FrozenSet[str]
    triggered_interactions: tuple[AssumptionInteraction, ...]
    first_order_sum: float
    interaction_sum: float
    total_effect: float
    ceiling_applied: bool
    """True if the amplification ceiling clamped the interaction sum."""

    @property
    def effect_classification(self) -> InteractionEffect:
        """Overall qualitative sign of the interaction contribution."""
        if self.interaction_sum > 0:
            return InteractionEffect.CONJUNCTIVE
        if self.interaction_sum < 0:
            return InteractionEffect.DISJUNCTIVE
        return InteractionEffect.DEGENERATE


class InteractionEngine:
    """Computes interaction-aware joint failure effects.

    The engine validates the declaration on construction (I-1 through I-4)
    and then exposes stateless query methods.
    """

    def __init__(self, declaration: InteractionDeclaration) -> None:
        validate_all(declaration)
        self._declaration = declaration

    # -- queries -----------------------------------------------------------

    @property
    def declaration(self) -> InteractionDeclaration:
        return self._declaration

    def triggered(self, failed_assumptions: set[str] | frozenset[str]) -> tuple[AssumptionInteraction, ...]:
        """Return all interactions whose members are all in *failed_assumptions*.

        An interaction triggers when **every** member has failed — the
        interaction captures the joint effect of simultaneous failure.
        """
        failed = frozenset(failed_assumptions)
        return tuple(
            ix for ix in self._declaration.interactions
            if ix.member_ids.issubset(failed)
        )

    def joint_effect(self, failed_assumptions: set[str] | frozenset[str]) -> InteractionResult:
        """Compute the total effect of *failed_assumptions* including all
        triggered interactions.

        Formula
        -------
        first_order  = Σ e(h)  for h in failed
        interaction  = Σ Δ(I)  for each triggered interaction I (Δ ≠ None)
        raw_total    = first_order + interaction
        ceiling      = amplification_ceiling × Σ|e(h)| for all failed h
        total        = min(raw_total, ceiling)   # only if interaction > 0

        For negative (redundant) interactions, there is no floor clamp —
        redundancy reduces risk, which is bounded by the count of failed
        assumptions (cannot reduce below 0 in the limit, but we let the
        caller interpret negative values as "safer than individual sum").
        """
        failed = frozenset(failed_assumptions)
        triggered = self.triggered(failed)

        first_order_sum = sum(
            self._declaration.first_order_effects.get(h, 0.0)
            for h in failed
        )

        interaction_sum = sum(
            ix.interaction_strength
            for ix in triggered
            if ix.interaction_strength is not None
        )

        raw_total = first_order_sum + interaction_sum

        # Ceiling applies only to amplifying side (I-3)
        ceiling_applied = False
        if interaction_sum > 0:
            first_order_abs_sum = sum(
                abs(self._declaration.first_order_effects.get(h, 0.0))
                for h in failed
            )
            ceiling = self._declaration.amplification_ceiling * first_order_abs_sum
            if raw_total > first_order_sum + ceiling:
                # Ceiling caps the *interaction contribution*, not the total.
                raw_total = first_order_sum + ceiling
                ceiling_applied = True

        return InteractionResult(
            failed_assumptions=failed,
            triggered_interactions=triggered,
            first_order_sum=first_order_sum,
            interaction_sum=interaction_sum,
            total_effect=raw_total,
            ceiling_applied=ceiling_applied,
        )

    # -- monotonic extension (I-4) ----------------------------------------

    def augment(
        self,
        current_failed: set[str] | frozenset[str],
        new_failure: str,
    ) -> InteractionResult:
        """Add *new_failure* to the failure set and return the new result.

        Union semantics: the new failure set is current ∪ {new_failure}.
        This guarantees I-4 (monotonicity) — adding a failure never
        un-triggers a previously triggered interaction.
        """
        extended = set(current_failed) | {new_failure}
        return self.joint_effect(extended)
