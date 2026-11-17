"""Interaction model — types and declarations.

An *interaction* is a named relationship among two or more assumptions such
that the joint effect of their simultaneous failure differs from the sum of
each failing alone.

Conventions
-----------
E(I)  = joint effect of interaction I
e(h)  = first-order effect of assumption h
Δ(I)  = interaction strength  =  E(I) − Σ e(h)

Δ > 0  → CONJUNCTIVE  (amplification: failure together is worse)
Δ < 0  → DISJUNCTIVE  (redundancy: failure together is less than sum)
Δ = 0  → DEGENERATE   (no interaction; retained to prove "we checked")
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import FrozenSet


class InteractionEffect(StrEnum):
    """Qualitative classification of an interaction's sign."""

    CONJUNCTIVE = "conjunctive"   # Δ > 0 — amplification
    DISJUNCTIVE = "disjunctive"   # Δ < 0 — redundancy
    DEGENERATE = "degenerate"     # Δ = 0 — no interaction


@dataclass(frozen=True)
class AssumptionInteraction:
    """A single declared interaction among assumptions.

    Fields
    ------
    id : str
        Stable identifier, e.g. "I_policy_supply".
    member_ids : frozenset[str]
        The assumptions participating in this interaction.  Must have size ≥ 2.
    description : str
        Human-readable explanation of *why* these assumptions interact.
    interaction_strength : float | None
        Δ(I) — the difference between joint effect and sum of first-order
        effects.  None means "declared but not yet quantified"; a numeric
        value must come from explicit human declaration (I-1).
    """

    id: str
    member_ids: FrozenSet[str]
    description: str = ""
    interaction_strength: float | None = None

    def __post_init__(self) -> None:
        if len(self.member_ids) < 2:
            raise ValueError(
                f"Interaction {self.id!r} must have at least 2 members, "
                f"got {len(self.member_ids)}"
            )

    @property
    def effect(self) -> InteractionEffect:
        """Qualitative sign of the interaction."""
        if self.interaction_strength is None:
            return InteractionEffect.DEGENERATE
        if self.interaction_strength > 0:
            return InteractionEffect.CONJUNCTIVE
        if self.interaction_strength < 0:
            return InteractionEffect.DISJUNCTIVE
        return InteractionEffect.DEGENERATE


@dataclass(frozen=True)
class InteractionDeclaration:
    """Full input to the interaction engine.

    A declaration is *pure input* — everything the engine needs must be here;
    the engine never invents strengths, members, or interactions.
    """

    interactions: tuple[AssumptionInteraction, ...] = ()
    first_order_effects: dict[str, float] = field(default_factory=dict)
    """Per-assumption first-order effect magnitudes.  Keys are assumption IDs."""

    amplification_ceiling: float = 2.0
    """Multiple of Σ|first-order| above which cumulative interaction is capped.
    Corresponds to invariant I-3 (effect boundedness).
    """
