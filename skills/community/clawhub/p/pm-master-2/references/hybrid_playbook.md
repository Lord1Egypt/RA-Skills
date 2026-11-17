# Hybrid Delivery Playbook

Turns "hybrid" from a slogan into an executable cadence. Applies to `methodology=hybrid`: the macro layer uses stage gates/roadmaps
(waterfall style) to control investment decisions and compliance, while the micro layer uses Sprints / iterations (agile / iteration style) for incremental delivery.

## 1. Layers

| Layer | Purpose | Main artifacts | Cadence |
|------|------|----------|------|
| **Macro** | stage-gate investment decisions, portfolio alignment, external compliance | wbs (phases/waves), stage_gate_review, hybrid_governance | low frequency, heavy (at phase end) |
| **Micro** | incremental delivery, fast feedback, internal agility | sprint_plan / product_backlog / iteration_plan, burndown, definition_of_done | high frequency, light (1–4 weeks) |

> The boundary must be explicitly written in `hybrid_governance.md`: which part goes macro, which goes micro, where the gates are, and who decides.

## 2. Cadence

- **Macro cadence**: hold a stage-gate review (stage_gate_review) at the end of each phase; the next phase is released only when the checklist is all green.
- **Micro cadence**: Sprints / iterations of fixed length (2 weeks recommended), including planning, daily standup, review, and retrospective.
- **Alignment Review**: schedule an alignment review before each macro milestone (stage gate) to verify whether the micro-layer
  increments meet that gate's exit criteria. Without passing the alignment review, you cannot enter the stage gate.

## 3. Micro-Layer Plan Anatomy (Wave / Sprint Anatomy)

Taking "Wave + Sprint" as an example:

```
Stage gate G0 ── Wave 1 (macro: scope/goals)
              ├─ Sprint 1  (micro: increment a)
              ├─ Sprint 2  (micro: increment b)
              └─ Wave Exit Gate ── meets G1 entry
Stage gate G1 ── Wave 2 ...
```

- **Each Wave = one macro work package (WBS row)**; at least **1 Sprint / iteration plan** (micro layer) hangs beneath it.
- The micro-layer plan must include: goal, commitment, task list (with estimates), DoD.
- **Mandatory**: every hybrid project/component must have at least one micro-layer plan; otherwise the consistency check blocks delivery.

## 4. Exit Criteria and Entry Criteria

- **Wave/phase exit**: deliverables complete + DoD met + key risks mitigated + metrics on target (e.g., SPI ≥ 0.95).
- **Next-phase entry**: upstream dependencies ready (e.g., real data/resources in place) + upstream gate conclusion is "passed / conditionally passed".
- Exit/entry checklists are written into the corresponding `stage_gate_review.checklist` and the `acceptance` (DoD) column of the `wbs`.

## 5. Alignment Review Checklist

- [ ] Do the completed micro-layer increments cover the scope required by this stage gate?
- [ ] Does increment quality meet DoD? Did it pass the Wave Exit Gate?
- [ ] Are cross-layer dependencies (macro↔micro, component↔component) blocked? Are blockers escalated?
- [ ] Are EVM / velocity metrics healthy (CPI/SPI ≥ 0.95)? Are variances within tolerance?
- [ ] Do major changes go through change_log / CCB?

## 6. Change Control

Hybrid projects change fast, so a formal change channel is required:
- Any scope/schedule/resource change → raise a `change_request`, recording impact (scope/schedule/cost/risk).
- CCB (Change Control Board) review → conclusion written into `change_log`.
- Stage-gate conclusions and Wave Exit Gate conclusions are also included in `change_log` for traceability.

## 7. Consistency-Check Highlights (hybrid)

- A micro-layer plan (sprint / backlog / iteration) must exist → otherwise blocked.
- Having a `change_log` (CCB) is recommended → warning.
- The macro-layer wbs must form a dependency network (dependsOn) → otherwise blocked.
- Entering the execution/monitoring phase requires establishing an EVM baseline and running `evm.py` → otherwise blocked.

> See `methodology-hybrid.md` (forms and artifacts) and `templates-index.md` (template list).
