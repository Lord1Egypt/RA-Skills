"""Forward invalidation propagation — cascading assumption failure.

When an assumption fails, `invalidation_closure` propagates that failure
forward through the declared dependency graph.  If A1 depends on A2 and A2
fails, then A1 is also invalidated because its declared support is gone.

Design invariants:
  - Deterministic: the closure follows only declared edges.
  - No guessing: if an assumption has no declared dependencies and is not
    the trigger, it is not affected.
  - Audit trail: each propagation step is a first-class operation.

v0.4 addition: `invalidation_closure_with_interaction` extends first-order
propagation with interaction-aware joint effects (when an interaction
declaration is supplied).  The original function is unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from ..models.schemas import DecisionRequest


def invalidation_closure(
    request: DecisionRequest,
    trigger_assumption_id: str,
) -> tuple[list[str], list[str]]:
    """Return (invalidated_ids, affected_alternative_ids).

    *invalidated_ids* — all assumptions transitively invalidated when
    *trigger_assumption_id* fails, including the trigger itself.

    *affected_alternative_ids* — alternatives whose required_assumptions
    overlap with the invalidated set.
    """
    assumption_index = {a.id: a for a in request.assumptions}
    if trigger_assumption_id not in assumption_index:
        return [], []

    # BFS forward through the dependency graph
    invalidated: set[str] = set()
    frontier = {trigger_assumption_id}

    while frontier:
        current = frontier.pop()
        if current in invalidated:
            continue
        invalidated.add(current)
        # Find all assumptions that depend on `current`
        for a_id, assumption in assumption_index.items():
            if a_id not in invalidated and current in assumption.dependencies:
                frontier.add(a_id)

    # Affected alternatives
    affected = [
        alt.id
        for alt in request.alternatives
        if set(alt.required_assumptions) & invalidated
    ]

    return sorted(invalidated), sorted(affected)


@dataclass(frozen=True)
class InteractionPropagationResult:
    """Result of interaction-aware invalidation propagation.

    Extends the plain (invalidated, affected) tuple with interaction detail
    for audit and downstream scoring hooks.
    """

    invalidated_ids: list[str]
    affected_alternative_ids: list[str]
    triggered_interaction_ids: list[str]
    first_order_sum: Decimal
    interaction_contribution: Decimal
    total_effect: Decimal
    ceiling_applied: bool


def invalidation_closure_with_interaction(
    request: DecisionRequest,
    trigger_assumption_id: str,
) -> tuple[list[str], list[str], InteractionPropagationResult | None]:
    """First-order invalidation closure + interaction layer (if declared).

    Returns ``(invalidated_ids, affected_alt_ids, interaction_result_or_None)``.

    When the request carries no ``interaction_declaration``, the third
    element is ``None`` and the function behaves exactly like
    ``invalidation_closure`` — zero behavioural change for v0.3 callers.
    """
    invalidated, affected = invalidation_closure(request, trigger_assumption_id)

    decl = request.interaction_declaration
    if decl is None or not decl.interactions:
        return invalidated, affected, None

    # ── Lazy import: interaction engine is optional for non-interaction use ──
    from ..interaction.engine import InteractionEngine
    from ..interaction.model import (
        AssumptionInteraction,
        InteractionEffect,
        InteractionDeclaration as _EngineDeclaration,
    )

    engine_decl = _EngineDeclaration(
        interactions=tuple(
            AssumptionInteraction(
                id=inter.id,
                member_ids=frozenset(inter.member_ids),
                interaction_strength=float(inter.interaction_strength),
            )
            for inter in decl.interactions
        ),
        first_order_effects={k: float(v) for k, v in decl.first_order_effects.items()},
        amplification_ceiling=float(decl.amplification_ceiling),
    )
    engine = InteractionEngine(engine_decl)
    effect = engine.joint_effect(set(invalidated))

    _QUANT = Decimal("0.000000000001")
    total = Decimal(str(effect.total_effect)).quantize(_QUANT)
    fo_sum = Decimal(str(effect.first_order_sum)).quantize(_QUANT)
    # Actual interaction contribution = total - first_order, which correctly
    # reflects ceiling clipping when ceiling_applied is True.
    actual_interaction = (total - fo_sum).quantize(_QUANT)
    result = InteractionPropagationResult(
        invalidated_ids=invalidated,
        affected_alternative_ids=affected,
        triggered_interaction_ids=sorted(ix.id for ix in effect.triggered_interactions),
        first_order_sum=fo_sum,
        interaction_contribution=actual_interaction,
        total_effect=total,
        ceiling_applied=effect.ceiling_applied,
    )
    return invalidated, affected, result