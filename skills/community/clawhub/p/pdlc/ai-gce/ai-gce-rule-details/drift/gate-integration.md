<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Gate Integration — Drift Pre-Check (Step 0)

## Purpose

Defines how drift detection integrates with gate evaluation so that **unresolved HARD drift blocks advancement**. Adds a pre-check (Step 0) ahead of the existing gate-matching stack, plus advisory surfacing and platform-specific enforcement.

**Grounding:** Implements `MIDFLIGHT_DRIFT_GOVERNANCE_DESIGN.md` §9.

---

## MANDATORY: Stage Sub-Role — Audit Specialist

Audit Specialist mindset (gates are binary; hard drift is non-negotiable). ADDS a dimension.

### Anti-Patterns
- Do NOT let advisory drift block a gate — it informs only
- Do NOT pass a gate with unresolved HARD drift (unless platform can't enforce — then disclose)
- Do NOT re-detect from scratch at the gate if a recent scan exists — read the register

---

## Gate Evaluation Extension (Step 0)

The existing GATE_PROTOCOL matching stack gains a pre-check:

```
GATE EVALUATION (extended):

  Step 0 (NEW): DRIFT PRE-CHECK
    - Read .governance/drift-register.md (via manifest.files.driftRegister)
    - Count entries WHERE status == OPEN AND classification == HARD
      (OPEN is the only unresolved hard state on the register; routing/digest
       progress is tracked off-register and does not affect the gate count)
    - IF count > 0: BLOCK (conflict C10 — Drift Gate Block)
        → "⛔ {count} unresolved hard drift(s). Resolve before advancing."
    - IF count == 0: PASS → proceed to Step 1

  Step 1: STRUCTURE (interfaceVersion)
  Step 2: TYPE NAME (emits-type match)
  Step 3: TYPE VERSION (semver range)
  Step 4: MANDATORY (field coverage)
  Step 5: OPTIONAL (strictness-based)
```

Drift is checked FIRST — a workspace with unresolved hard drift never reaches structural gate matching.

---

## Advisory Drift at Gates

Advisory is surfaced, never blocks:

```
IF advisory_open_count > 0:
  INFO: "ℹ️ {count} advisory drift(s) logged. Non-blocking. Run DFT__ for details."
```

---

## Platform-Specific Enforcement

HOW the block is enforced depends on the platform (from `manifest.platformTargets`):

| Platform | Enforcement mechanism | Block strength |
|----------|----------------------|----------------|
| Kiro | Agent + hook (`agentStop`/pre-gate) reads register | Automatic — can hard-stop |
| Claude Code | Subagent + `PreToolUse` hook (exit code 2) | Automatic — deterministic block |
| Cursor | Advisory rule text + CI/CD gate | CI-level (editor advisory) |
| Codex | Advisory + CI/CD gate | CI-level |
| Generic | CI/CD script fails on hard drift | Pipeline-level |

**Disclosure:** on platforms where editor-level blocking isn't possible (Cursor/Codex/Generic), `PLATFORM_NOTES.md` states that hard-drift enforcement is CI/CD-level, not editor-level. Honest — the register + advisory always exist; only the *automatic block* varies.

---

## Build-Profile Gate Behavior (Parked)

The drift design (§9.3) varies gate strictness by `buildProfile` (freestyle = advisory-only). **`buildProfile` is PARKED.** When absent, GCE uses the **standard** gate behavior: HARD drift BLOCKS, advisory INFORMS. (The freestyle "nothing blocks" mode activates only when the build-profile axis is unparked.)

| Build Profile | Hard Drift Gate | Advisory Gate |
|---------------|:---------------:|:-------------:|
| (parked/absent — default) | BLOCK | INFO |
| spec-driven *(when unparked)* | BLOCK | INFO |
| freestyle *(when unparked)* | INFO only | INFO |

---

## Conflict Type C10 (FLO Integration)

Drift blocking is expressed as a new FLO conflict type:

| # | Type | Description | Severity | Resolution |
|---|------|-------------|----------|------------|
| C10 | Drift Gate Block | Entity cannot advance — unresolved HARD drift | Critical (hold) | Route drift → disposition → re-baseline → re-scan → release |

Integrates with FLO's existing `flag-and-hold`: the entity holds until drift resolves, then FLO re-evaluates the gate. (FLO side implemented in Phase P6.)

---

## When the Gate Check Fires

| Trigger | Who | Behavior |
|---------|-----|----------|
| `DFT__` (on-demand) | user | Full scan → register → report gate status |
| Session-end (`SEG__`) | session agent | Scan + flag new hard drift in session report |
| Pre-advance | FLO | Read register; block advance if hard drift open |

Prefer reading a recent register over re-scanning at the gate; re-scan only if the register is stale (baseline changed since `lastScanTimestamp`).

---

## Interaction with Other Files

| Related | Relationship |
|---------|--------------|
| `drift/drift-register.md` | Source of the HARD-drift count |
| `drift/drift-detection-engine.md` | Produces/refreshes the register the gate reads |
| `templates/agents/drift-detect-agent.md` | The agent that runs the scan feeding the gate |
| (AI-FLO) | Owns C10 conflict + advance pre-check |

---

## Output Validation

- [ ] Step 0 pre-check reads register (not a fresh scan unless stale)
- [ ] Unresolved HARD (status == OPEN) blocks; advisory informs
- [ ] Enforcement mechanism selected per `platformTargets`
- [ ] Non-blocking platforms disclose CI/CD-level enforcement in `PLATFORM_NOTES.md`
- [ ] Standard gate behavior used when `buildProfile` absent (parked)
- [ ] C10 conflict emitted for FLO hold
