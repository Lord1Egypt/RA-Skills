<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 2: Routing Table Build

## Purpose

Construct the routing table that governs all flow decisions — starting from the canonical family chain as the default, then layering per-project profiles and active toggles.

---

## Steps

### Step 1: Load Canonical Default Routes

The base routing table is derived from the AI-* Family chain contracts:

```markdown
## Default Routing Table (Canonical)

| # | From | To (Successor) | Type | Condition |
|---|------|----------------|------|-----------|
| R1 | AI-ILC | AI-PILC / AI-POLC / AI-PPM | Conditional | Based on ILC `Route` field value |
| R2 | AI-PILC | AI-PPM (register · prioritize · authorize) | Sequential (same-layer) | PIP complete → AI-PPM intake (if PPM absent → route direct to AI-POLC) |
| R3 | AI-PPM | AI-POLC | Dispatch (cross-layer) | Authorization issued → open Project layer at AI-POLC |
| R4 | AI-POLC | AI-UXD | Sequential | PBP complete → UXD starts |
| R5 | AI-UXD | AI-ADLC | Sequential | UXP complete → ADLC starts |
| R6 | AI-ADLC | AI-DWG | Sequential | AP complete → DWG starts (all 3 inputs now exist by sequence) |
| R7 | AI-DWG | AI-DLC v1 | Sequential | Workspace ready → build starts |
| R8 | AI-GCE | — (alongside AI-DLC v1) | Companion | Continuous — no routing trigger |
| R9 | AI-TGE | — (alongside AI-DLC v1) | Companion | Continuous — no routing trigger |
| R10 | AI-PPM | AI-FLO (dispatch) | Cross-layer | Dispatch authorization → FLO carries down |

> **Project-layer sequence:** The default route into the Project layer is **AI-PILC → AI-PPM → AI-POLC → AI-UXD → AI-ADLC → AI-DWG** (sequential). Each package feeds the next: POLC defines *what* to build (PBP), UXD designs the *experience* for that backlog (UXP), ADLC designs the *structure* to support that experience (AP). By the time ADLC completes, all three inputs for DWG are guaranteed present. If AI-PPM is absent, AI-PILC routes directly to AI-POLC (graceful degradation,). Feedback loops (ADLC→POLC cost/risk, ADLC→UXD constraints) provide iterative refinement without changing the forward sequence.

### Fan-In: AI-DWG Readiness Rule (Simplified by Sequential Guarantee)

| Feed | Package | Expected? | Marker | Sequential Guarantee |
|------|---------|:---------:|--------|---------------------|
| Product Backlog (PBP) | AI-POLC | **YES** | `polc-state.md` Status=Complete | Completed before UXD starts (R4) |
| UX Design (UXP) | AI-UXD | **YES** | `uxd-state.md` Status=Complete | Completed before ADLC starts (R5) |
| Architecture Package (AP) | AI-ADLC | **YES** | `adlc-state.md` Status=Complete | Terminal predecessor — triggers DWG (R6) |

In the default sequential flow, **all three are guaranteed present** by the time AI-DWG starts (ADLC is the terminal predecessor). DWG validates presence (not waits for parallel completion). For brownfield/partial scenarios, DWG still accepts any non-empty subset (≥1) with user-approved exception + acknowledged reduced coverage.
```

### Step 2: Filter by Package Availability

Remove routes involving packages that don't exist in this workspace:

```
Package availability filter:

  ❌ AI-TGE not detected → R8 removed (no companion to track)
  ❌ AI-GCE not detected → R7 removed
  ✅ All other packages detected → routes retained
  
  Active routes: {N} of 9 canonical
```

### Step 3: Apply Per-Project Profiles

For each known project, check if a dispatch authorization exists with scope constraints:

| Project ID | Dispatch Scope | Skip | Effect on Routes |
|------------|---------------|------|-----------------|
| PRJ-ERP-2026-001 | Full | — | All routes apply |
| PRJ-CRM-2026-002 | Design-only | AI-POLC, AI-UXD | R2 fan-out reduced to ADLC only; R4/R5 skipped |
| PRJ-MOB-2026-003 | Custom | AI-ADLC | R2 fan-out = UXD + POLC only; R3 skipped |

```
Per-project profiles applied:

  PRJ-ERP-2026-001: Full (9 routes active)
  PRJ-CRM-2026-002: Skip [AI-POLC, AI-UXD] (6 routes active)
  PRJ-MOB-2026-003: Skip [AI-ADLC] (7 routes active)
```

### Step 4: Apply Active Toggles

Check for any runtime toggles from previous sessions:

```
Active toggles:

  PRJ-CRM-2026-002: AI-UXD toggled ON (2026-06-16) — overrides skip
  → Route R4 restored for this project
  
  Updated: PRJ-CRM-2026-002 now has 7 routes active
```

### Step 5: Validate Routing Table

Check for issues:
- ⚠️ Orphan routes (successor doesn't exist)
- ⚠️ Unreachable packages (no route leads to them)
- ⚠️ Circular routes (A→B→A without loop mediation)
- ⚠️ Fan-in with ALL gate feeds skipped (DWG with no predecessors)

```
Validation results:

  ✅ No orphan routes
  ✅ No unreachable packages
  ✅ No circular routes
  ✅ Each fan-in target has at least one gate feed active (full gate = all three)
  
  Routing table is valid.
```

### Step 6: Produce `routing-table.md`

Write the complete routing table to `flow-orchestration/routing-table.md`:

```markdown
# Routing Table — AI-FLO

**Generated:** {date}
**Topology:** Mode {X}
**Projects:** {N}

## Canonical Routes (Active)

| # | From | To | Type | Active For |
|---|------|-----|------|------------|
| R1 | AI-ILC | AI-PILC / AI-POLC / AI-PPM | Conditional | All |
| R2 | AI-PILC | AI-PPM | Sequential | All |
| R3 | AI-PPM | AI-POLC | Dispatch | Per profile |
| R4 | AI-POLC | AI-UXD | Sequential | Per profile |
| R5 | AI-UXD | AI-ADLC | Sequential | Per profile |
| R6 | AI-ADLC | AI-DWG | Sequential | Per profile |
|... |... |... |... |... |

## Per-Project Profiles

| Project ID | Mode | Skip | Active Toggles |
|------------|------|------|----------------|
| PRJ-ERP-2026-001 | Full | — | — |
| PRJ-CRM-2026-002 | Skip | [AI-UXD] | — |

## Fan-In Rules (Simplified by Sequential Model)

| Target | Inputs (guaranteed by sequence) | Brownfield Exception |
|--------|---------------------------------|---------------------|
| AI-DWG | AP (AI-ADLC) + PBP (AI-POLC) + UXP (AI-UXD) | Proceed with <3 only on user approval (reduced coverage) |
```

---

## Gate

**Approval required before proceeding to Stage 3.**

Operator must confirm:
- Default routes are correct for this workspace
- Per-project profiles accurately reflect dispatch intent
- Any active toggles are still valid
- No validation warnings remain unaddressed

---

## Transition

```
✅ Stage 2 complete. Routing table built.

  Active routes: {N} | Projects profiled: {N} | Toggles: {N}
  
  Moving to Stage 3: Initializing flow state (project positions +
  configuration).
```

Load `configure/flow-state-init.md`.

---

*Part of AI-FLO v1.0.0*
