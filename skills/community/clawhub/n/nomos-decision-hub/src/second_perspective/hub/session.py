"""Three-layer reconstruction session engine.

Replaces single-shot causal reconstruction with a bounded, hash-chained,
human-gated iterative process:

    round i:  forward propagation → backward tracing → delta reconstruction
    seal:     each round is hash-linked to the previous round
    advance:  only a human decision (approve / supply_evidence / reject) may
              move the session to the next round
    stop:     the session converges (fixed point / no gain) or its budget is
              exhausted

Design invariants (aligned with NOMOS core):
  - No guessing: every hypothesis is a candidate; human verification decides.
  - Deterministic: each round derives exclusively from declared inputs.
  - Auditable: rounds form a session-level hash chain (`session_root_hash`).
  - Bounded: `max_iterations` and `max_evidence_requests` cap the process.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from uuid import uuid4

from ..canonical import canonical_json
from ..decision.reconstruction import (
    CausalReconstructor,
    apply_delta_vars,
    _collect_delta_invalidated,
)
from ..models.enums import (
    AssumptionState,
    ConvergenceKind,
    ReconstructionKind,
    SessionStatus,
)
from ..models.schemas import (
    ConvergenceReport,
    DeltaVar,
    DecisionRequest,
    DeviationSignal,
    ReconstructionSession,
    SessionRound,
)


def _hash_round(round_: SessionRound, previous_hash: str | None) -> str:
    """Compute a round's root hash from its canonical payload."""
    payload = {
        "round_index": round_.round_index,
        "kind": round_.kind.value,
        "invalidated_assumption_ids": round_.invalidated_assumption_ids,
        "hypothesis_ids": [h.id for h in round_.hypotheses],
        "unresolved_branches": round_.unresolved_branches,
        "convergence_kind": round_.convergence.kind.value if round_.convergence else None,
        "candidate_set_changed": (
            round_.convergence.candidate_set_changed if round_.convergence else None
        ),
        "applied_delta_vars": [dv.path for dv in round_.applied_delta_vars],
        "assumption_states": round_.assumption_states,
        "requires_human_decision": round_.requires_human_decision,
        "previous_round_hash": previous_hash,
    }
    return hashlib.sha256(canonical_json(payload)).hexdigest()


def _hash_session(session: ReconstructionSession) -> str:
    """Compute the session root hash over the entire round chain."""
    payload = {
        "session_id": session.session_id,
        "round_hashes": [r.round_root_hash for r in session.rounds],
        "assumption_states": session.assumption_states,
        "status": session.status.value,
    }
    return hashlib.sha256(canonical_json(payload)).hexdigest()


class ReconstructionSessionEngine:
    """Drives a ReconstructionSession round by round.

    The engine is intentionally passive: ``advance()`` performs exactly one
    round and then requires a human decision. It never auto-loops.
    """

    def __init__(self, reconstructor: CausalReconstructor | None = None) -> None:
        self.reconstructor = reconstructor or CausalReconstructor()

    def start(
        self,
        request: DecisionRequest,
        signals: list[DeviationSignal],
        *,
        max_iterations: int = 5,
        max_evidence_requests: int = 20,
    ) -> ReconstructionSession:
        session = ReconstructionSession(
            session_id=f"SESS-{uuid4().hex[:12].upper()}",
            request=request,
            deviation_signals=signals,
            assumption_states={
                assumption.id: AssumptionState.ASSUMED for assumption in request.assumptions
            },
            status=SessionStatus.ACTIVE,
            max_iterations=max_iterations,
            max_evidence_requests=max_evidence_requests,
            created_at=datetime.now(timezone.utc),
        )
        return session

    def advance(
        self,
        session: ReconstructionSession,
        delta_vars: list[DeltaVar] | None = None,
    ) -> ReconstructionSession:
        """Execute exactly one three-layer reconstruction round.

        Returns the updated session. The round always ends in
        ``AWAITING_HUMAN`` unless a stop condition is already met.
        """
        delta_vars = delta_vars or []
        round_index = len(session.rounds)
        previous_hash = session.rounds[-1].round_root_hash if session.rounds else None

        # ── Layer 1: forward propagation (invalidation_closure) ──
        invalidated_ids = _collect_delta_invalidated(session.request, delta_vars)
        invalidated_ids = sorted(
            set(invalidated_ids)
            | set(self._forward_invalidated(session.request, session.assumption_states))
        )

        # ── Layer 2: backward tracing (existing second layer) ──
        report = self.reconstructor.reconstruct(session.request, session.deviation_signals)
        hypotheses = report.hypotheses if report else []
        unresolved = report.unresolved_branches if report else []

        # ── Layer 3: delta reconstruction (new third layer) ──
        convergence: ConvergenceReport | None = None
        if delta_vars:
            convergence = self.reconstructor.reconstruct_with_delta(
                session.request,
                session.deviation_signals,
                delta_vars,
            )

        # ── Assumption state updates from this round ──
        states = dict(session.assumption_states)
        for assumption_id in invalidated_ids:
            if assumption_id in states:
                states[assumption_id] = AssumptionState.FALSIFIED

        # ── Stop-condition check before sealing the round ──
        stop_status, stop_kind = self._stop_condition(
            session=session,
            round_index=round_index,
            convergence=convergence,
            hypotheses=hypotheses,
            unresolved=unresolved,
        )
        requires_human = stop_status in (SessionStatus.ACTIVE, SessionStatus.AWAITING_HUMAN)

        round_ = SessionRound(
            round_index=round_index,
            kind=(
                ReconstructionKind.DELTA_RECONSTRUCTION
                if convergence is not None
                else ReconstructionKind.BACKWARD_TRACING
            ),
            invalidated_assumption_ids=invalidated_ids,
            hypotheses=hypotheses,
            unresolved_branches=unresolved,
            convergence=convergence,
            applied_delta_vars=delta_vars,
            assumption_states=states,
            round_root_hash=None,  # filled by _hash_round below
            previous_round_hash=previous_hash,
            requires_human_decision=requires_human,
        )
        round_ = round_.model_copy(update={"round_root_hash": _hash_round(round_, previous_hash)})

        updated = session.model_copy(
            update={
                "rounds": [*session.rounds, round_],
                "assumption_states": states,
                "status": stop_status,
                "convergence_kind": stop_kind,
                "sealed_at": datetime.now(timezone.utc) if stop_status in (
                    SessionStatus.CONVERGED,
                    SessionStatus.BUDGET_EXCEEDED,
                ) else session.sealed_at,
            }
        )
        updated = updated.model_copy(update={"session_root_hash": _hash_session(updated)})
        return updated

    def human_decision(
        self,
        session: ReconstructionSession,
        *,
        approved: bool = False,
        evidence_status: dict[str, AssumptionState] | None = None,
    ) -> ReconstructionSession:
        """Record a human decision and re-open the session for the next round.

        ``approved=True`` seals the session as CONVERGED (final human sign-off).
        ``evidence_status`` maps assumption IDs to VERIFIED / FALSIFIED /
        UNFALSIFIABLE, updating the monotone assumption-state machine.
        """
        if session.status == SessionStatus.SEALED:
            return session

        states = dict(session.assumption_states)
        for assumption_id, state in (evidence_status or {}).items():
            if assumption_id not in states:
                continue
            # Monotone: never regress a terminal state.
            if state in (AssumptionState.VERIFIED, AssumptionState.FALSIFIED, AssumptionState.UNFALSIFIABLE):
                states[assumption_id] = state

        if approved:
            updated = session.model_copy(
                update={
                    "assumption_states": states,
                    "status": SessionStatus.SEALED,
                    "sealed_at": datetime.now(timezone.utc),
                }
            )
            return updated.model_copy(update={"session_root_hash": _hash_session(updated)})

        return session.model_copy(
            update={
                "assumption_states": states,
                "status": SessionStatus.ACTIVE,
            }
        )

    @staticmethod
    def _forward_invalidated(
        request: DecisionRequest,
        assumption_states: dict[str, AssumptionState],
    ) -> list[str]:
        """Assumptions already falsified in the session state machine."""
        return [
            assumption_id
            for assumption_id, state in assumption_states.items()
            if state == AssumptionState.FALSIFIED
        ]

    def _stop_condition(
        self,
        *,
        session: ReconstructionSession,
        round_index: int,
        convergence: ConvergenceReport | None,
        hypotheses: list,
        unresolved: list[str],
    ) -> tuple[SessionStatus, ConvergenceKind | None]:
        """Deterministic stop judgement for the current session.

        Delegates to ``ConvergenceChecker`` (introduced in v0.4) for the
        formal classification, then maps the result back to the existing
        ``SessionStatus`` / ``ConvergenceKind`` API surface so callers are
        unaffected.

        Returns (status, convergence_kind):
          - FIXED_POINT: delta re-evaluation changed neither candidates nor
            the hypothesis set (nothing further to learn).
          - NO_GAIN: no unresolved branches remain AND no open (ASSUMED)
            assumptions left to verify.
          - BUDGET: iteration or evidence budget exhausted.
        """
        # Lazy import: convergence module is pure increment, no hard dependency
        from ..convergence.checker import ConvergenceChecker
        from ..convergence.types import ConvergenceStatus as CS

        evidence_requests = sum(
            len(round_.applied_delta_vars) + len(round_.hypotheses) for round_ in session.rounds
        ) + (len(hypotheses) if hypotheses else 0)

        # Build candidate sets for fixed-point detection (P-2)
        if session.rounds and session.rounds[-1].convergence is not None:
            prev_candidates = session.rounds[-1].convergence.after_leading_candidate_ids
        else:
            prev_candidates = []
        curr_candidates = (
            convergence.after_leading_candidate_ids if convergence is not None else []
        )

        checker = ConvergenceChecker(
            max_iterations=session.max_iterations,
            max_evidence_requests=session.max_evidence_requests,
        )

        # Fixed-point requires a real previous round's candidate set.
        # On round 0 there is no previous round, so pass a sentinel set
        # that guarantees fp_holds is False (empty == empty is a false
        # positive on the very first round).
        has_prev_round = bool(session.rounds) and session.rounds[-1].convergence is not None
        result = checker.evaluate(
            round_index=round_index,
            candidate_set_prev=prev_candidates if has_prev_round else [""],
            candidate_set_curr=curr_candidates,
            iterations_used=round_index + 1,
            evidence_requests_used=evidence_requests,
            unresolved_branches=len(unresolved),
        )

        if result.status == CS.FIXED_POINT:
            # Only meaningful when a delta reconstruction actually ran
            if convergence is not None and convergence.is_converged and not hypotheses:
                return SessionStatus.CONVERGED, ConvergenceKind.FIXED_POINT
            return SessionStatus.AWAITING_HUMAN, None

        if result.status == CS.NO_GAIN:
            # Domain constraint: no-gain also requires all assumptions settled
            open_assumptions = sum(
                1 for state in session.assumption_states.values()
                if state == AssumptionState.ASSUMED
            )
            if not unresolved and open_assumptions == 0:
                return SessionStatus.CONVERGED, ConvergenceKind.NO_GAIN
            return SessionStatus.AWAITING_HUMAN, None

        if result.status == CS.BUDGET_EXHAUSTED:
            return SessionStatus.BUDGET_EXCEEDED, ConvergenceKind.BUDGET

        # BLOCKED or DIVERGED → still work to do
        return SessionStatus.AWAITING_HUMAN, None


__all__ = ["ReconstructionSessionEngine"]
