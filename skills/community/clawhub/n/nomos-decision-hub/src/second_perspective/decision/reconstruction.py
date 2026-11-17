"""Causal reconstruction engine — trace observed deviations backward to root causes.

This module is the mirror image of causal.py. Where `invalidation_closure` propagates
assumption failures *forward* (A1 fails → what else breaks?), this module traces
*backward* (deviation observed → which assumption failure could explain it?).

Design invariants (aligned with NOMOS core):
  - No guessing: output is a set of candidate hypotheses, not a single "answer".
  - Deterministic: every trace path is derived from the declared dependency graph.
  - Audit trail: each reconstruction step generates AlgorithmAuditEvent entries.
  - Information-first: every hypothesis explicitly lists what is missing.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from ..models.enums import ConvergenceKind, IssueSeverity
from ..models.schemas import (
    AlgorithmAuditEvent,
    CausalReconstructionReport,
    ConvergenceReport,
    DecisionRequest,
    DeltaVar,
    DeviationSignal,
    RootCauseHypothesis,
)
from .causal import invalidation_closure
from .engine import IntelligentDecisionEngine


# ── Graph helpers ────────────────────────────────────────────────────


def build_reverse_dependency_map(assumptions: list) -> dict[str, list[str]]:
    """Build reverse dependency graph from declared assumption dependencies.

    Forward:  A1.dependencies = [A2, A3]  →  "A1 depends on A2 and A3"
    Reverse:  A2 → [A1], A3 → [A1]        →  "A2 failure affects A1"

    This is the topological inverse needed for backward tracing.
    """
    reverse: dict[str, list[str]] = {}
    for assumption in assumptions:
        for dep in assumption.dependencies:
            reverse.setdefault(dep, []).append(assumption.id)
    for assumption in assumptions:
        reverse.setdefault(assumption.id, [])
    return reverse


def build_assumption_index(assumptions: list) -> dict[str, object]:
    """Index assumptions by ID for O(1) lookup."""
    return {a.id: a for a in assumptions}


def build_evidence_index(evidence_list: list) -> dict[str, object]:
    """Index evidence by ID."""
    return {e.id: e for e in evidence_list}


# ── Signal-to-assumption mapping ─────────────────────────────────────


def _match_signal_to_assumptions(
    signal: DeviationSignal,
    assumptions: list,
    evidence_index: dict[str, object],
) -> list[str]:
    """Return assumption IDs that could explain a single deviation signal.

    Matching logic:
      1. If the signal's metric name appears in an assumption's falsification_condition,
         that assumption is a candidate observed-failure.
      2. Exclude assumptions that have non-expired, supplied evidence directly backing them
         (the evidence says "this assumption holds", so it's less likely the root cause).
    """
    metric_lower = signal.metric.lower()
    candidates: list[str] = []

    for assumption in assumptions:
        # Loose match: metric name appears in falsification condition
        if metric_lower not in assumption.falsification_condition.lower():
            continue

        # Evidence check: if ALL of this assumption's evidence is supplied
        # and none is expired, the assumption is "verified" — skip it.
        if assumption.evidence_ids:
            all_supplied = True
            for eid in assumption.evidence_ids:
                ev = evidence_index.get(eid)
                if ev is None:
                    all_supplied = False
                    break
                from ..models.enums import EvidenceStatus

                if ev.status != EvidenceStatus.SUPPLIED:
                    all_supplied = False
                    break
                if ev.valid_until is not None and ev.valid_until <= signal.observed_at:
                    all_supplied = False
                    break
            if all_supplied:
                continue  # evidence says this assumption is fine

        candidates.append(assumption.id)

    return candidates


# ── Backward BFS ──────────────────────────────────────────────────────


def _backward_bfs(
    seed_assumption_ids: set[str],
    reverse_dep: dict[str, list[str]],
    assumption_index: dict[str, object],
    evidence_index: dict[str, object],
) -> dict[str, list[str]]:
    """BFS backward from observed failures to potential root causes.

    Returns:
        {root_id: [full chain from root to nearest seed]}

    Traversal rules:
      - Follow reverse_dep edges upward (against the dependency direction).
      - Stop at nodes where evidence is supplied and not expired (verified assumptions).
      - Record the root of each trace — the farthest node reached before stopping.
    """
    roots: dict[str, list[str]] = {}

    for seed in sorted(seed_assumption_ids):
        if seed not in reverse_dep:
            # Isolated node: it is its own root
            roots[seed] = [seed]
            continue

        # BFS
        visited: set[str] = {seed}
        frontier: list[tuple[str, list[str]]] = [(seed, [seed])]
        local_roots: list[tuple[str, list[str]]] = []

        while frontier:
            current, path = frontier.pop(0)
            parents = reverse_dep.get(current, [])

            if not parents:
                local_roots.append((current, list(path)))
                continue

            has_unverified_parent = False
            for parent in parents:
                if parent in visited:
                    continue
                visited.add(parent)

                # Check if parent is "verified" by evidence
                parent_assumption = assumption_index.get(parent)
                if parent_assumption and parent_assumption.evidence_ids:
                    all_supplied = True
                    for eid in parent_assumption.evidence_ids:
                        ev = evidence_index.get(eid)
                        if ev is None:
                            all_supplied = False
                            break
                        from ..models.enums import EvidenceStatus

                        if ev.status != EvidenceStatus.SUPPLIED:
                            all_supplied = False
                            break
                    if all_supplied:
                        # Verified parent: stop here, current is effectively a root
                        local_roots.append((current, list(path)))
                        continue

                new_path = [parent] + path
                frontier.append((parent, new_path))
                has_unverified_parent = True

            if not has_unverified_parent and not parents:
                local_roots.append((current, list(path)))

        for root_id, chain in local_roots:
            if root_id not in roots or len(chain) > len(roots[root_id]):
                roots[root_id] = chain

    return roots


# ── Severity estimation ──────────────────────────────────────────────


def _estimate_severity(
    assumption_id: str,
    assumption_index: dict[str, object],
    affected_signal_count: int,
) -> IssueSeverity:
    """Estimate root cause severity based on criticality and blast radius."""
    assumption = assumption_index.get(assumption_id)
    if assumption is None:
        return IssueSeverity.WARNING

    is_critical = getattr(assumption, "critical", False)
    has_responsibility = getattr(assumption, "responsibility", None) is not None

    if is_critical and affected_signal_count >= 2:
        return IssueSeverity.ERROR
    if is_critical and not has_responsibility:
        return IssueSeverity.ERROR
    if is_critical or affected_signal_count >= 2:
        return IssueSeverity.WARNING
    return IssueSeverity.INFO


# ── Missing evidence ──────────────────────────────────────────────────


def _collect_missing_evidence(
    chain: list[str],
    assumption_index: dict[str, object],
    evidence_index: dict[str, object],
) -> list[str]:
    """Collect evidence IDs along the causal chain that are missing or expired."""
    missing: list[str] = []
    for aid in chain:
        assumption = assumption_index.get(aid)
        if assumption is None:
            continue
        for eid in getattr(assumption, "evidence_ids", []):
            ev = evidence_index.get(eid)
            if ev is None:
                missing.append(eid)
                continue
            from ..models.enums import EvidenceStatus

            if ev.status != EvidenceStatus.SUPPLIED:
                missing.append(eid)
    return sorted(set(missing))


# ── Audit event builder ───────────────────────────────────────────────


def _build_audit_event(
    sequence: int,
    stage: str,
    rule_id: str,
    operation: str,
    inputs: dict,
    output,
    previous_hash: str | None,
) -> AlgorithmAuditEvent:
    """Build a single audit event with hash linking, matching ledger.py convention."""
    import hashlib

    from ..canonical import canonical_json

    # Build payload as dict, compute hash, then construct the pydantic model
    payload = {
        "sequence": sequence,
        "stage": stage,
        "rule_id": rule_id,
        "operation": operation,
        "inputs": inputs,
        "output": output,
        "references": [],
        "previous_event_hash": previous_hash,
    }
    digest = hashlib.sha256(canonical_json(payload)).hexdigest()
    payload["event_hash"] = digest
    return AlgorithmAuditEvent(**payload)


# ── Main engine ───────────────────────────────────────────────────────


class CausalReconstructor:
    """Deterministic backward causal tracer.

    Takes deviation signals from the perception layer and traces backward
    along the declared assumption dependency graph to identify candidate
    root cause hypotheses.  Does NOT produce a single "answer" — output is
    a structured set of hypotheses for human verification.
    """

    def reconstruct(
        self,
        request: DecisionRequest,
        signals: list[DeviationSignal],
    ) -> CausalReconstructionReport:
        reconstruction_id = f"REC-{uuid4().hex[:12].upper()}"
        audit_events: list[AlgorithmAuditEvent] = []
        prev_hash: str | None = None
        seq = 0

        # ── Phase 0: build indices ──
        assumption_index = build_assumption_index(request.assumptions)
        evidence_index = build_evidence_index(request.evidence)
        reverse_dep = build_reverse_dependency_map(request.assumptions)

        seq += 1
        ev = _build_audit_event(
            seq, "reconstruction", "REC-INDEX",
            "build_reverse_dep",
            {"assumption_count": len(request.assumptions)},
            {"reverse_edge_count": sum(len(v) for v in reverse_dep.values())},
            prev_hash,
        )
        audit_events.append(ev)
        prev_hash = ev.event_hash

        # ── Phase 1: map signals to affected assumptions ──
        signal_to_assumptions: dict[str, list[str]] = {}
        all_seed_ids: set[str] = set()

        for signal in signals:
            matched = _match_signal_to_assumptions(signal, request.assumptions, evidence_index)
            signal_to_assumptions[signal.metric] = matched
            all_seed_ids.update(matched)

        seq += 1
        ev = _build_audit_event(
            seq, "reconstruction", "REC-MAP",
            "signal_to_assumption_mapping",
            {"signals": [s.metric for s in signals]},
            {"matched_assumptions": sorted(all_seed_ids)},
            prev_hash,
        )
        audit_events.append(ev)
        prev_hash = ev.event_hash

        # ── Phase 2: backward BFS ──
        root_chains = _backward_bfs(all_seed_ids, reverse_dep, assumption_index, evidence_index)

        seq += 1
        ev = _build_audit_event(
            seq, "reconstruction", "REC-BFS",
            "backward_bfs",
            {"seed_count": len(all_seed_ids), "seeds": sorted(all_seed_ids)},
            {"root_count": len(root_chains), "roots": sorted(root_chains.keys())},
            prev_hash,
        )
        audit_events.append(ev)
        prev_hash = ev.event_hash

        # ── Phase 3: build hypotheses ──
        hypotheses: list[RootCauseHypothesis] = []
        for root_id, chain in root_chains.items():
            # Determine which signals this root explains
            explained: list[str] = []
            for metric, matched in signal_to_assumptions.items():
                if any(node in matched for node in chain):
                    explained.append(metric)

            missing = _collect_missing_evidence(chain, assumption_index, evidence_index)

            # Verification action
            root_assumption = assumption_index.get(root_id)
            root_name = getattr(root_assumption, "statement", root_id) if root_assumption else root_id
            verification = (
                f"验证假设 [{root_id}] {root_name}：检查证据 "
                + (", ".join(missing[:3]) if missing else "无缺失证据，确认 falsification_condition 是否已触发")
            )

            severity = _estimate_severity(root_id, assumption_index, len(explained))

            hypotheses.append(
                RootCauseHypothesis(
                    id=f"RH-{uuid4().hex[:8].upper()}",
                    root_assumption_id=root_id,
                    causal_chain=chain,
                    explained_signals=explained,
                    missing_evidence_ids=missing,
                    verification_action=verification,
                    dependency_depth=len(chain) - 1,
                    severity=severity,
                )
            )

        # Sort: ERROR first, then by depth (shorter chain = more likely root)
        severity_order = {IssueSeverity.ERROR: 0, IssueSeverity.WARNING: 1, IssueSeverity.INFO: 2}
        hypotheses.sort(key=lambda h: (severity_order.get(h.severity, 2), h.dependency_depth))

        # Phase 4: identify unresolved branches (signal without any matched assumption)
        unresolved = [
            metric for metric, matched in signal_to_assumptions.items() if not matched
        ]

        seq += 1
        ev = _build_audit_event(
            seq, "reconstruction", "REC-HYPOTHESES",
            "build_hypotheses",
            {"root_count": len(root_chains)},
            {
                "hypothesis_count": len(hypotheses),
                "unresolved_branches": unresolved,
            },
            prev_hash,
        )
        audit_events.append(ev)
        prev_hash = ev.event_hash

        # ── Phase 5: compute root hash ──
        import hashlib

        from ..canonical import canonical_json

        if audit_events:
            final_payload = {
                "last_event_hash": audit_events[-1].event_hash,
                "reconstruction_id": reconstruction_id,
                "hypothesis_count": len(hypotheses),
            }
            audit_root = hashlib.sha256(canonical_json(final_payload)).hexdigest()
        else:
            audit_root = None

        return CausalReconstructionReport(
            reconstruction_id=reconstruction_id,
            hypotheses=hypotheses,
            signal_count=len(signals),
            root_candidate_count=len(root_chains),
            unresolved_branches=unresolved,
            algorithm_audit=audit_events,
            algorithm_audit_root_hash=audit_root,
        )

    def reconstruct_with_delta(
        self,
        request: DecisionRequest,
        signals: list[DeviationSignal],
        delta_vars: list[DeltaVar],
        engine: IntelligentDecisionEngine | None = None,
    ) -> ConvergenceReport:
        """Third layer — delta reconstruction.

        Applies declared correction variables (delta_vars) to a deep copy of the
        decision request, re-runs the deterministic evaluator, and reports whether
        the leading candidate set changed and whether the session has converged.

        The engine never invents corrections: every mutation mirrors a declared
        DeltaVar, and the whole re-run is recorded as hash-chained audit events.
        """
        from ..version import VERSION

        engine = engine or IntelligentDecisionEngine()
        reconstruction_id = f"REC-{uuid4().hex[:12].upper()}"
        audit_events: list[AlgorithmAuditEvent] = []
        prev_hash: str | None = None
        seq = 0

        # Deterministic replay identity: pin decision_id and evaluation_as_of so
        # the before/after evaluations are comparable and reproducible.
        replay_time = request.evaluation_as_of or datetime.now(timezone.utc)
        decision_id = request.decision_id or f"DEC-DELTA-{uuid4().hex[:12].upper()}"
        baseline = request.model_copy(
            update={"decision_id": decision_id, "evaluation_as_of": replay_time}
        )

        seq += 1
        ev = _build_audit_event(
            seq, "reconstruction", "DELTA-BASELINE",
            "pin_replay_identity",
            {"decision_id": decision_id, "delta_var_count": len(delta_vars)},
            {"evaluation_as_of": replay_time.isoformat()},
            prev_hash,
        )
        audit_events.append(ev)
        prev_hash = ev.event_hash

        # ── Phase 1: baseline evaluation ──
        before = engine.evaluate(baseline)
        before_candidates = before.leading_candidate_ids

        seq += 1
        ev = _build_audit_event(
            seq, "reconstruction", "DELTA-BEFORE",
            "baseline_evaluation",
            {"decision_id": decision_id},
            {"leading_candidate_ids": before_candidates},
            prev_hash,
        )
        audit_events.append(ev)
        prev_hash = ev.event_hash

        # ── Phase 2: apply delta_vars ──
        patched = apply_delta_vars(baseline, delta_vars)
        invalidated = _collect_delta_invalidated(baseline, delta_vars)

        seq += 1
        ev = _build_audit_event(
            seq, "reconstruction", "DELTA-APPLY",
            "apply_delta_vars",
            {"delta_vars": [dv.path for dv in delta_vars]},
            {"invalidated_assumption_ids": invalidated},
            prev_hash,
        )
        audit_events.append(ev)
        prev_hash = ev.event_hash

        # ── Phase 3: re-evaluate ──
        after = engine.evaluate(patched)
        after_candidates = after.leading_candidate_ids
        candidate_set_changed = set(before_candidates) != set(after_candidates)

        seq += 1
        ev = _build_audit_event(
            seq, "reconstruction", "DELTA-AFTER",
            "delta_evaluation",
            {"candidate_set_changed": candidate_set_changed},
            {"leading_candidate_ids": after_candidates},
            prev_hash,
        )
        audit_events.append(ev)
        prev_hash = ev.event_hash

        # ── Phase 4: convergence judgement ──
        kind = ConvergenceKind.FIXED_POINT if not candidate_set_changed else ConvergenceKind.NO_GAIN
        is_converged = not candidate_set_changed
        reason = (
            "Fixed-point reached: re-evaluation after applying declared delta_vars "
            "produced the same leading candidate set, so further iteration adds nothing."
            if is_converged
            else "No fixed point yet: candidate set changed under the declared delta_vars; "
            "a human decision is required before the next round."
        )

        seq += 1
        ev = _build_audit_event(
            seq, "reconstruction", "DELTA-CONVERGE",
            "convergence_judgement",
            {"before": before_candidates, "after": after_candidates},
            {"kind": kind.value, "is_converged": is_converged},
            prev_hash,
        )
        audit_events.append(ev)
        prev_hash = ev.event_hash

        # ── Phase 5: root hash ──
        import hashlib

        from ..canonical import canonical_json

        final_payload = {
            "last_event_hash": audit_events[-1].event_hash,
            "reconstruction_id": reconstruction_id,
            "kind": kind.value,
        }
        audit_root = hashlib.sha256(canonical_json(final_payload)).hexdigest()

        return ConvergenceReport(
            kind=kind,
            reconstruction_id=reconstruction_id,
            delta_vars=delta_vars,
            before_leading_candidate_ids=before_candidates,
            after_leading_candidate_ids=after_candidates,
            candidate_set_changed=candidate_set_changed,
            invalidated_assumption_ids=invalidated,
            is_converged=is_converged,
            reason=reason,
            algorithm_audit=audit_events,
            algorithm_audit_root_hash=audit_root,
        )


def apply_delta_vars(
    request: DecisionRequest,
    delta_vars: list[DeltaVar],
) -> DecisionRequest:
    """Return a deep copy of the request with declared delta_vars applied verbatim.

    Supported path forms:
      - ``"A2"`` — falsify assumption A2 (propagated through the dependency graph);
                   dependent alternatives lose that assumption's support.
      - ``"criteria.K1.weight"`` — rewrite one criterion weight.
      - ``"alternatives.S1.metrics.cost"`` — rewrite one alternative metric.

    Every mutation is a direct mirror of a declared DeltaVar — the engine never
    invents corrections. Unsupported paths raise ValueError (fail closed).
    """
    patched = request.model_copy(deep=True)
    assumption_index = {a.id: a for a in patched.assumptions}

    for dv in delta_vars:
        parts = dv.path.split(".")
        if len(parts) == 1:
            # Assumption falsification path: "A2"
            if parts[0] not in assumption_index:
                raise ValueError(f"delta path '{dv.path}' does not name a declared assumption")
            invalidated, _ = invalidation_closure(patched, parts[0])
            invalidated_set = {parts[0], *invalidated}
            # Drop alternatives whose declared assumption support is now falsified.
            patched = patched.model_copy(
                update={
                    "alternatives": [
                        alt
                        for alt in patched.alternatives
                        if not (set(alt.required_assumptions) & invalidated_set)
                    ]
                }
            )
        elif len(parts) == 3 and parts[0] == "criteria":
            criterion_id, field = parts[1], parts[2]
            if field != "weight":
                raise ValueError(f"unsupported criterion delta field: '{field}'")
            found = any(c.id == criterion_id for c in patched.criteria)
            if not found:
                raise ValueError(f"delta path '{dv.path}' does not name a declared criterion")
            from decimal import Decimal as _Decimal

            try:
                new_weight = _Decimal(str(dv.value))
            except Exception as exc:  # pragma: no cover - defensive
                raise ValueError(
                    f"delta path '{dv.path}' requires a numeric weight, got {dv.value!r}"
                ) from exc
            if not (new_weight >= _Decimal("0") and new_weight <= _Decimal("1")):
                raise ValueError(f"delta path '{dv.path}' weight out of range 0..1: {new_weight}")
            patched = patched.model_copy(
                update={
                    "criteria": [
                        c.model_copy(update={"weight": new_weight}) if c.id == criterion_id else c
                        for c in patched.criteria
                    ]
                }
            )
        elif len(parts) == 4 and parts[0] == "alternatives" and parts[2] == "metrics":
            alternative_id, _, metric = parts[1], parts[2], parts[3]
            found = any(a.id == alternative_id for a in patched.alternatives)
            if not found:
                raise ValueError(f"delta path '{dv.path}' does not name a declared alternative")
            new_alternatives = []
            for alt in patched.alternatives:
                if alt.id == alternative_id:
                    metrics = dict(alt.metrics)
                    metrics[metric] = dv.value
                    new_alternatives.append(alt.model_copy(update={"metrics": metrics}))
                else:
                    new_alternatives.append(alt)
            patched = patched.model_copy(update={"alternatives": new_alternatives})
        else:
            raise ValueError(f"unsupported delta path: '{dv.path}'")

    return patched


def _collect_delta_invalidated(
    request: DecisionRequest,
    delta_vars: list[DeltaVar],
) -> list[str]:
    """Collect assumption IDs invalidated by the declared delta_vars."""
    assumption_index = {a.id for a in request.assumptions}
    invalidated: set[str] = set()
    for dv in delta_vars:
        parts = dv.path.split(".")
        if len(parts) == 1 and parts[0] in assumption_index:
            closure, _ = invalidation_closure(request, parts[0])
            invalidated.update({parts[0], *closure})
    return sorted(invalidated)
