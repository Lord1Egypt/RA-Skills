"""Propositions — formally-stated, independently verifiable claims.

Each proposition function takes the relevant inputs and returns either
``(True, reason)`` (proposition holds) or ``(False, reason)`` (falsified).
These are *not* mathematical proofs in code — they are checkable statements
that correspond to proofs in the design document.  The code verifies the
premises hold; the proof itself is in the spec.

P-1  Termination        — finite budgets ⇒ guaranteed eventual termination.
P-2  Fixed point        — candidate set identical two rounds in a row ⇒
                          all subsequent rounds are identical (given a
                          deterministic evaluator).
P-3  Effect boundedness — cumulative interaction effect ≤ ceiling × Σ|first-order|.
"""

from __future__ import annotations

from typing import Iterable


# ---------------------------------------------------------------------------
# P-1  Termination
# ---------------------------------------------------------------------------

def proposition_termination(
    max_iterations: int,
    max_evidence_requests: int,
) -> tuple[bool, str]:
    """P-1: Termination guarantee.

    *Proof sketch:* both iteration and evidence-request budgets are finite
    positive integers; each round consumes at least 1 iteration unit; the
    well-ordering principle guarantees the process must reach 0 and stop.

    The code checks the *precondition* (budgets are finite positive ints);
    if that holds, the conclusion follows by the proof above.
    """
    if not isinstance(max_iterations, int) or max_iterations <= 0:
        return False, f"max_iterations must be positive int, got {max_iterations!r}"
    if not isinstance(max_evidence_requests, int) or max_evidence_requests < 0:
        return (
            False,
            f"max_evidence_requests must be non-negative int, got {max_evidence_requests!r}",
        )
    return (
        True,
        f"Both budgets finite positive: iterations={max_iterations}, "
        f"evidence_requests={max_evidence_requests}; "
        f"well-ordering guarantees termination in ≤{max_iterations} rounds.",
    )


# ---------------------------------------------------------------------------
# P-2  Fixed point
# ---------------------------------------------------------------------------

def proposition_fixed_point(
    prev_candidates: Iterable[str],
    curr_candidates: Iterable[str],
) -> tuple[bool, str]:
    """P-2: Fixed-point property.

    *Proof sketch:* the deterministic evaluator is a pure function of its
    input (the candidate hypothesis set + declared deltas).  If two
    consecutive rounds produce the same candidate set, then the *next*
    round receives the same input as the *current* round, hence must
    produce the same output — fixed point reached.

    ⚠️ This is the theoretical reason LLM must NOT participate in
    convergence assessment: an LLM-augmented evaluator is not a pure
    function and the fixed-point proof does not hold.
    """
    prev = frozenset(prev_candidates)
    curr = frozenset(curr_candidates)

    if prev == curr:
        return (
            True,
            f"Candidate set identical across rounds ({len(curr)} members).  "
            f"Deterministic pure-function evaluator ⇒ fixed point.",
        )
    added = curr - prev
    removed = prev - curr
    diff_parts = []
    if added:
        diff_parts.append(f"+{sorted(added)}")
    if removed:
        diff_parts.append(f"-{sorted(removed)}")
    return False, f"Candidate set changed: {' '.join(diff_parts)}"


# ---------------------------------------------------------------------------
# P-3  Effect boundedness
# ---------------------------------------------------------------------------

def proposition_effect_boundedness(
    first_order_sum_abs: float,
    interaction_amplifying_sum: float,
    ceiling_multiplier: float,
) -> tuple[bool, str]:
    """P-3: Effect boundedness (interaction layer invariant I-3 restated as a
    proposition about the convergence process).

    *Proof sketch:* each CONJUNCTIVE interaction contributes Δ; the engine
    applies min(Δ, ceiling) on the amplifying side; finite summation of
    bounded terms yields a bounded total.
    """
    if first_order_sum_abs < 0:
        return False, f"first_order_sum_abs must be ≥ 0, got {first_order_sum_abs}"
    if ceiling_multiplier < 1.0:
        return (
            False,
            f"ceiling_multiplier must be ≥ 1.0, got {ceiling_multiplier}",
        )

    ceiling = ceiling_multiplier * first_order_sum_abs
    if interaction_amplifying_sum <= ceiling:
        return (
            True,
            f"Amplifying interaction sum {interaction_amplifying_sum:.4f} ≤ "
            f"ceiling {ceiling:.4f} (×{ceiling_multiplier} of "
            f"{first_order_sum_abs:.4f}).",
        )
    return (
        False,
        f"Amplifying interaction sum {interaction_amplifying_sum:.4f} EXCEEDS "
        f"ceiling {ceiling:.4f} — boundedness violated.",
    )
