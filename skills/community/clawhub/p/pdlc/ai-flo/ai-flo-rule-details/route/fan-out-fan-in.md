<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 5: Fan-Out / Fan-In

## Purpose

Coordinate sequential routing handoffs and join validation (confirming all predecessor outputs exist before a successor starts). In the sequential PDLC model (POLC→UXD→ADLC→DWG), fan-out is limited to specific multi-target scenarios; the primary Project-layer flow is a linear chain.

---

## Trigger

This stage executes when:
- A package completes that has multiple successors (true fan-out — e.g., AI-ILC, AI-UXD dual output)
- A package is the target of a validation gate that checks presence of multiple predecessor outputs (AI-DWG)
- Operator requests `check readiness [project-id]`

---

## Fan-Out

### When It Happens

| Trigger | Fan-Out Targets | Notes |
|---------|-----------------|-------|
| AI-ILC completes | Depends on `Route` field (may fan to PILC + PPM) | Conditional — not always a fan-out |
| AI-UXD completes | AI-ADLC (next in sequence) + AI-POLC (feedback: personas handoff) | Primary successor = ADLC; feedback to POLC is secondary |

> **Project-layer entry — Sequential (POLC→UXD→ADLC→DWG).** When the Project layer opens, **AI-POLC is the first package** (defines what to build), followed by **AI-UXD** (designs the experience), then **AI-ADLC** (designs the architecture). This is a strict sequential chain — each feeds the next. There is NO parallel fan-out from PPM to all three. Dispatch from PPM targets AI-POLC only.

### Fan-Out Execution (when applicable)

```
📤 Fan-Out Detected: {Project ID}

  Source: {triggering package}
  Targets:
  
  | # | Target | Type | Status | Action |
  |---|--------|------|--------|--------|
  | 1 | {primary successor} | Sequential (next in chain) | Ready to start | Handoff instruction |
  | 2 | {feedback target} | Feedback (secondary) | Receives output copy | Notify |
  
  Confirm fan-out? [Y] Route all | [P] Route partial (select) | [H] Hold
```

### Fan-Out Rules

1. The primary Project-layer flow is sequential (POLC→UXD→ADLC→DWG) — NOT a parallel fan-out
2. True fan-out only occurs for: AI-ILC (conditional routing), AI-UXD dual output (ADLC + POLC feedback)
3. Each target is tracked independently in `flo-state.md`
4. If a target is skipped (profile) or toggled OFF, it's excluded from the fan-out
5. Log one routing-log entry per target (Type=Hop)

---

## Fan-In (Validation Gate)

### When It Happens

| Target | Expected Inputs | How they arrive | Behavior when an input is missing |
|--------|-----------------|-----------------|-----------------------------------|
| AI-DWG | AP (AI-ADLC) **+** PBP (AI-POLC) **+** UXP (AI-UXD) | **Sequentially guaranteed:** POLC→UXD→ADLC means all 3 exist when ADLC completes | Warn (brownfield/partial scenario); show each predecessor's status; require explicit user approval to proceed with fewer |

> **Sequential guarantee simplifies fan-in.** In the default sequential flow (POLC→UXD→ADLC→DWG), by the time AI-ADLC completes (the terminal predecessor), PBP and UXP are already complete (they were prerequisites for starting UXD and ADLC respectively). DWG validates presence of all three as a sanity check, not as a parallel-convergence wait. Proceeding with fewer than three is a **brownfield exception with acknowledged reduced coverage** — it only happens in partial/skip scenarios, never in the default flow.

### Fan-In Evaluation (Presence Validation)

When AI-ADLC completes (the terminal predecessor), FLO validates that all three inputs exist:

```
🔄 Fan-In Validation: {Project ID} → AI-DWG

  Expected inputs (sequential guarantee):
  | Input | Source | Marker | Status |
  |-------|--------|--------|--------|
  | Product Backlog (PBP) | AI-POLC | polc-state.md | ✅ Complete (2026-06-15) |
  | UX Design (UXP) | AI-UXD | uxd-state.md | ✅ Complete (2026-06-16) |
  | Architecture Package (AP) | AI-ADLC | adlc-state.md | ✅ Complete (2026-06-17) |

  Readiness: ✅ ALL PRESENT (sequential guarantee met) — recommend proceed.
```

**Brownfield/partial scenario** (when a package was skipped via profile):

```
🔄 Fan-In Validation: {Project ID} → AI-DWG

  Expected inputs:
  | Input | Source | Marker | Status |
  |-------|--------|--------|--------|
  | Product Backlog (PBP) | AI-POLC | polc-state.md | ✅ Complete (2026-06-15) |
  | UX Design (UXP) | AI-UXD | uxd-state.md | 🚫 Skipped (profile: Design-only) |
  | Architecture Package (AP) | AI-ADLC | adlc-state.md | ✅ Complete (2026-06-14) |

  Readiness: ⚠️ PARTIAL — 2 of 3 present (UXD skipped by profile)

  AI-DWG can generate the POLC + ADLC clusters; the UX cluster (design system,
  frontend a11y baseline) will be ABSENT.

  Options:
  [P] Proceed with 2/3 (user-approved exception — acknowledged reduced coverage)
  [H] Hold (no action)
```

### Readiness Rules

1. **Sequential guarantee:** In the default flow (POLC→UXD→ADLC→DWG), all three inputs are present when AI-ADLC completes — DWG validates presence, not parallel convergence
2. **Brownfield exception:** When a package is skipped (profile), DWG proceeds with the available subset — FLO warns, displays status, obtains explicit approval acknowledging reduced coverage
3. **A feed toggled OFF in the project profile** is treated as "not expected" — it's excluded from validation and noted in the readiness check
4. **Produce `readiness-check.md`** — one per evaluation, stored in `readiness-checks/`
5. **If AI-FLO is absent**, AI-DWG enforces this same validation gate (presence check + approval for partial) at its own intake — see `ai-dwg .../common/ap-reading-guide.md`

### Readiness Check Template

```markdown
# Readiness Check: RC-{Project-ID}

| Field | Value |
|-------|-------|
| Project ID | {ID} |
| Target | AI-DWG |
| Checked | {date} |
| Result | {ALL_PRESENT / PARTIAL_SKIP / MISSING} |

## Inputs (validated by sequential guarantee)

| Input | Source | Expected? | Status | Completed | Notes |
|-------|--------|:---------:|--------|-----------|-------|
| PBP | AI-POLC | ✅ Yes | Complete | {date} | Completed R4 (predecessor to UXD) |
| UXP | AI-UXD | ✅ Yes | Complete | {date} | Completed R5 (predecessor to ADLC) |
| AP | AI-ADLC | ✅ Yes | Complete | {date} | Terminal predecessor — triggered this check |

## Decision

| Choice | Date | Operator | Rationale |
|--------|------|----------|-----------|
| Proceed (all present) / Proceed with skip (exception) | {date} | @{name} | {rationale + acknowledged coverage gap if partial} |
```

---

## Special Case: AI-UXD Dual Output

AI-UXD has two distinct handoff paths when it completes:
1. **Full UXP → AI-ADLC** (next in sequence — ADLC receives UXP as input per R5)
2. **Personas/journeys → AI-POLC** (feedback — POLC consumes for backlog refinement/re-prioritization)

FLO routes both simultaneously but tracks them differently:
- Path 1 is the primary sequential handoff (Stage 6)
- Path 2 is a feedback handoff (secondary — does not block the forward chain)

---

## Logging

- Fan-out: one log entry per target (Type=Hop)
- Fan-in check: one log entry (Type=Hold if waiting, Type=Hop if proceeding)
- Readiness decisions: logged + stored as `RC-*.md`

---

## Gate

Operator confirms:
- Fan-out targets are correct
- Readiness assessment is accurate
- Proceed/wait decision for optional feeds

---

*Part of AI-FLO v1.0.0*
