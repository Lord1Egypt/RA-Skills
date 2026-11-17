<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Agent: FLO Health Check (FHC__)

**AG-ID:** FLO-AG-02
**Package:** AI-FLO
**Shortcut:** `FHC__`
**Version:** 1.0.0

---

## Purpose

A **bootstrap health check** that validates whether AI-FLO can operate in the current workspace. Unlike FIA__ (which checks integrity of existing state), FHC__ answers the question: **"Is this workspace ready for FLO? Can FLO actually engage here?"**

Designed to be the first thing you run when installing FLO in a destination workspace. It validates the preconditions, attempts a discovery scan, and produces a readiness verdict.

---

## When to Invoke

- First time installing FLO in a destination workspace
- After AI-DWG generates a workspace (to verify FLO can route)
- When FLO activation produces unexpected behavior
- As a diagnostic when routing seems broken
- To produce evidence that FLO can (or cannot) function

---

## Invocation

Type `FHC__` in any prompt. No parameters needed — the check is always workspace-scoped.

Optional modifiers:
- `FHC__ verbose` — include raw file contents in evidence
- `FHC__ fix` — attempt to resolve simple issues (create missing files, suggest corrections)

---

## Health Check Protocol

### Phase 1: Precondition Checks (Can FLO Even Start?)

| # | Check | What It Validates | PASS | FAIL |
|---|-------|-------------------|------|------|
| PC-1 | FLO steering loaded | `core-engine.md` (or equivalent) is in the active steering/rules location | FLO can activate | FLO is not installed |
| PC-2 | Rule details accessible | `ai-flo-rule-details/` folder exists and contains expected subfolders | Stage files can load | FLO can activate but not execute stages |
| PC-3 | At least one sibling package present | Any `*-state.md` marker OR package steering exists (PILC, ADLC, POLC, etc.) | Something to route | FLO has nothing to observe |
| PC-4 | FAMILY_BINDINGS.md exists | The routing graph source exists at the family root | Routing graph can build | FLO cannot determine edges — no routing possible |
| PC-5 | GATE_PROTOCOL.md exists | Gate matching rules exist at family root | Gate validation can run | FLO routes without gate validation (degraded) |
| PC-6 | FAMILY_INTERFACE.md exists | Family discovery anchor present | Family can be registered | Minor — FLO still works with bindings alone |

### Phase 2: Discovery Scan (Does FLO See the Topology?)

| # | Check | What It Validates | PASS | FAIL |
|---|-------|-------------------|------|------|
| DS-1 | Bindings parseable | FAMILY_BINDINGS internal edge table has at least 1 valid edge | Routing graph has structure | Bindings file exists but is empty/malformed |
| DS-2 | Marker files scannable | FLO can read at least one `*-state.md` with valid structure | Position tracking possible | No markers to scan (no projects have run yet) |
| DS-3 | Entity ID resolvable | At least one marker contains a non-placeholder `entityId` / `projectId` | FLO can track a real entity | Only templates present — no real projects |
| DS-4 | Edge targets exist | Every "To" package in the bindings edge table has its steering/rules present | Routes lead to real packages | Some routes lead nowhere (partial install) |
| DS-5 | Fan-in gates defined | At least one fan-in rule exists in bindings | FLO can coordinate multi-feed | Simple sequential only (not necessarily wrong) |

### Phase 3: Operational Readiness (Can FLO Actually Route?)

| # | Check | What It Validates | PASS | FAIL |
|---|-------|-------------------|------|------|
| OR-1 | At least one entity in routable state | A marker shows `status: complete` for a non-terminal package | FLO can propose a handoff | Nothing to route yet (workspace is idle) |
| OR-2 | flo-state.md writable | FLO can create/update its state file in the expected location | State persistence works | Permission or path issue |
| OR-3 | routing-log.md writable | FLO can create/append its audit trail | Audit trail works | Cannot log (degraded operation) |
| OR-4 | No conflicting FLO instances | No central FLO registry lists this workspace as controlled (unless expected) | This FLO is authoritative | Dormant — central FLO owns this workspace |
| OR-5 | Topology mode determinable | Workspace signals allow FLO to determine Mode 1/2/3 | Routing scope is clear | Ambiguous topology — needs operator input |

### Phase 4: End-to-End Proof (Can FLO Complete One Cycle?)

This phase only runs if Phase 3 passes with at least one routable entity.

| # | Check | What It Validates | PASS | FAIL |
|---|-------|-------------------|------|------|
| E2E-1 | Gate match executes | Pick one complete marker → run 5-step gate match against its outbound edge(s) | Gate logic works live | Gate match fails or is inapplicable |
| E2E-2 | Position update succeeds | Update flo-state.md with the detected position (non-destructive) | State writes work | Write failed |
| E2E-3 | Routing log entry appends | Write one Init/Drift entry to routing-log.md | Audit trail works | Append failed |
| E2E-4 | Handoff instruction producible | Generate (but do NOT execute) a handoff instruction for the next hop | Full cycle works | Something blocks handoff generation |

---

## Output Format

```
╔══════════════════════════════════════════════════════╗
║  FHC__ FLO Health Check Report                       ║
╠══════════════════════════════════════════════════════╣

  Workspace:     {path}
  Date:          {ISO date}
  FLO Version:   {from core-engine.md}

  ┌─────────────────────────────────────────────────┐
  │  VERDICT: {HEALTHY / DEGRADED / NOT READY}      │
  └─────────────────────────────────────────────────┘

  Phase 1 — Preconditions:       {N}/{6} pass
  Phase 2 — Discovery:           {N}/{5} pass
  Phase 3 — Operational:         {N}/{5} pass
  Phase 4 — End-to-End Proof:    {N}/{4} pass (or SKIPPED)

  Summary:
  • {One-line plain English diagnosis}
  • {What works}
  • {What doesn't}
  • {Recommended action}

╚══════════════════════════════════════════════════════╝
```

---

## Verdict Logic

| Condition | Verdict |
|-----------|---------|
| Phase 1 all PASS + Phase 2 all PASS + Phase 3 ≥3 PASS + Phase 4 ≥3 PASS | **HEALTHY** — FLO is fully operational |
| Phase 1 all PASS + Phase 2 ≥3 PASS + Phase 3 ≥1 PASS | **DEGRADED** — FLO can activate but has limitations |
| Phase 1 PC-1 FAIL or PC-4 FAIL | **NOT READY** — FLO cannot operate (missing critical prerequisites) |
| Phase 2 DS-3 FAIL (only templates, no real entities) | **IDLE** — FLO is installed correctly but no projects have run yet |

---

## Detailed Findings Format

```
✅ PC-1: FLO steering loaded
  Location: .kiro/steering/ai-flo-rules/core-engine.md
  Version: 2.0.0

❌ DS-3: Entity ID resolvable — FAILED
  Scanned: pilc-state.md, adlc-state.md, polc-state.md
  Result: All contain placeholder syntax ({PRJ-ABBREV-YYYY-NNN})
  Meaning: No real projects have been initiated. FLO has nothing to track.
  Action: Run AI-PILC (or any lifecycle package) to create a real project first.

⚠️ OR-1: At least one entity in routable state — WARNING
  Scanned: 2 markers with real entity IDs
  Result: All show status=in-progress (none complete)
  Meaning: FLO can observe but cannot propose handoffs yet.
  Action: Complete the current package stage to trigger routing.
```

---

## Artifacts Produced

After running, FHC__ produces a single report file:

```
_FLO_/
└── health-check/
    └── FHC-{YYYY-MM-DD}.md       (the full report)
```

If `FHC__ fix` was invoked and fixes were applied:
```
_FLO_/
└── health-check/
    ├── FHC-{YYYY-MM-DD}.md       (report)
    └── FHC-{YYYY-MM-DD}-fixes.md (what was fixed)
```

---

## Relationship to FIA__

| Aspect | FHC__ (Health Check) | FIA__ (Integrity Agent) |
|--------|---------------------|------------------------|
| **When** | Before/during setup — "can FLO work?" | During operation — "is FLO's state correct?" |
| **Assumes** | Nothing — tests from zero | FLO is already running with state |
| **Validates** | Preconditions + first-cycle proof | Ongoing state integrity (17 checks) |
| **Produces** | Readiness verdict + diagnosis | Integrity report + drift findings |
| **Destructive?** | Never (read-only, except `fix` mode) | Never (read-only) |

---

## Installation

1. Copy `flo-health-check.md` to destination workspace `.kiro/agents/` (or equivalent for your IDE)
2. Add shortcut `FHC__` to workspace rules:

```markdown
**`FHC__` shortcut triggers FLO Health Check.** When the user types `FHC__` (uppercase, with double underscore) anywhere in a prompt, immediately execute the FLO Health Check protocol defined in this agent. Scan workspace for AI-FLO prerequisites, attempt discovery, validate operational readiness, and produce a verdict report. No further clarification needed.
```

3. Invoke with `FHC__` in any prompt

---

## Evidence Collection

When you run `FHC__` in a workspace, the report (`FHC-{date}.md`) IS the evidence. It documents exactly what worked and what failed. Store it alongside your project's test artifacts or governance records for traceability.

---

*Part of AI-FLO v1.0.0 | AG-ID: FLO-AG-02*
