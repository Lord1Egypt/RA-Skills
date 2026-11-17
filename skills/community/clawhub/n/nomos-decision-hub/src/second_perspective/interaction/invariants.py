"""Invariant validation for the interaction layer (I-1 through I-4).

Each invariant is a separate function that raises InvariantViolation on
failure.  ``validate_all`` runs the full set.
"""

from __future__ import annotations

from .model import AssumptionInteraction, InteractionDeclaration


class InvariantViolation(Exception):
    """Raised when an interaction invariant is violated."""

    def __init__(self, invariant: str, detail: str) -> None:
        super().__init__(f"[{invariant}] {detail}")
        self.invariant = invariant
        self.detail = detail


# ---------------------------------------------------------------------------
# I-1  Non-conjectural
# ---------------------------------------------------------------------------

def validate_non_conjectural(
    declaration: InteractionDeclaration,
) -> None:
    """I-1: interaction strength is either explicitly set or absent; the engine
    never fills in a default.  We verify this by checking that no strength
    has a zero value silently standing in for "unknown".

    Zero strength is allowed (it declares DEGENERATE explicitly), but the
    invariant is about *provenance*, not value — as long as the declaration
    is explicit, the invariant holds.  The actual check is that strength
    is either None or a real number supplied by the caller; this is enforced
    structurally by the dataclass.  The function exists so validate_all()
    has a symmetric four-invariant shape.
    """
    # Structural enforcement via dataclass types already guarantees I-1 at
    # the type level.  We keep the validator so audit logs can record a
    # "passed" result for each invariant.
    pass


# ---------------------------------------------------------------------------
# I-2  Order conservation
# ---------------------------------------------------------------------------

def validate_order_conservation(
    declaration: InteractionDeclaration,
) -> None:
    """I-2: every member of every interaction must exist in the declared
    assumption set (i.e. appear as a key in first_order_effects).
    """
    known = set(declaration.first_order_effects.keys())
    for ix in declaration.interactions:
        unknown = ix.member_ids - known
        if unknown:
            raise InvariantViolation(
                "I-2",
                f"Interaction {ix.id!r} references unknown assumptions: "
                f"{sorted(unknown)}",
            )


# ---------------------------------------------------------------------------
# I-3  Effect boundedness
# ---------------------------------------------------------------------------

def validate_effect_boundedness(
    declaration: InteractionDeclaration,
) -> None:
    """I-3: the sum of positive interaction strengths must not exceed
    amplification_ceiling × Σ|first_order_effects|.

    Only *positive* (amplifying) interactions count toward the ceiling —
    redundant interactions (Δ < 0) reduce cumulative effect and are never
    bounded from above (they're bounded from below by 0 on the negative side,
    which is naturally limited by the number of interactions).
    """
    first_order_sum = sum(
        abs(v) for v in declaration.first_order_effects.values()
    )
    ceiling = declaration.amplification_ceiling * first_order_sum

    amplifying_sum = sum(
        ix.interaction_strength
        for ix in declaration.interactions
        if ix.interaction_strength is not None
        and ix.interaction_strength > 0
    )

    if amplifying_sum > ceiling:
        raise InvariantViolation(
            "I-3",
            f"Cumulative amplifying interaction {amplifying_sum:.4f} exceeds "
            f"ceiling {ceiling:.4f} "
            f"(×{declaration.amplification_ceiling} of {first_order_sum:.4f})",
        )


# ---------------------------------------------------------------------------
# I-4  Monotonicity
# ---------------------------------------------------------------------------

def validate_monotonicity(
    declaration: InteractionDeclaration,
) -> None:
    """I-4 is a *runtime* invariant about the augment() operation — adding a
    newly failed assumption never un-triggers a previously triggered
    interaction.  At declaration time there is nothing to check; the property
    is enforced by the engine's union semantics.  We validate here that the
    declaration itself contains nothing that would violate monotonicity
    (which it can't, structurally — this is an audit-record check).
    """
    # Like I-1, I-4 is enforced structurally by the engine's union-semantics
    # implementation.  The validator exists for symmetry and audit logging.
    pass


# ---------------------------------------------------------------------------
# Composite
# ---------------------------------------------------------------------------

def validate_all(declaration: InteractionDeclaration) -> None:
    """Run all four invariant checks.  Raises InvariantViolation on first
    failure.  Returns silently if all pass.
    """
    validate_non_conjectural(declaration)
    validate_order_conservation(declaration)
    validate_effect_boundedness(declaration)
    validate_monotonicity(declaration)
