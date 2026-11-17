<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 3: Flow State Initialization

## Purpose

Create or update `flo-state.md` with each project's current position in the chain, configure operational parameters (timeouts, fallback rules), and produce the initial route map.

---

## Steps

### Step 1: Determine Project Positions

For each discovered project, read its package markers to determine where it currently sits:

```
Position detection:

  PRJ-ERP-2026-001:
    pilc-state.md  → Status: Complete (2026-06-10)
    adlc-state.md  → Status: Complete (2026-06-14)
    polc-state.md  → Status: In Progress
    uxd-state.md   → Not found
    → Position: AI-POLC (In Progress)
    → Next hop: waiting-for-fan-in (DWG needs AP ✓ + PBP pending)

  PRJ-CRM-2026-002:
    pilc-state.md  → Status: Complete (2026-06-12)
    adlc-state.md  → Status: In Progress
    → Position: AI-ADLC (In Progress)
    → Next hop: AI-DWG (after ADLC completes + readiness check)
```

### Step 2: Configure Operational Parameters

Present configuration options to operator:

```
⚙️ Flow Configuration

  Hold timeout (how long before auto-resolve):
  [Default: 5 business days] → ___

  Optional-feed wait (how long to wait for enrichment feeds):
  [Default: same as hold timeout] → ___

  Stall threshold (how long before flagging no-movement):
  [Default: 7 days] → ___

  Auto-resolve rule when timeout expires:
  [A] Upstream-wins — PPM authority prevails (default)
  [B] Latest-signal-wins — most recent, regardless of source
  [C] Always escalate — never auto-resolve (operator must act)
  [D] Custom per conflict type

  Roll-up schedule:
  [A] On demand only (default)
  [B] Every session start
  [C] Weekly (operator triggers)

  Press Enter to accept all defaults, or configure individually.
```

### Step 3: Build Project Entries

For each project, construct the `flo-state.md` entry:

```markdown
## Project: {Project Name}

| Field | Value |
|-------|-------|
| Project ID | {PRJ-ABBREV-YYYY-NNN} |
| Workspace Ref | {./ or /path/to/remote/} |
| Current Package | {package name} |
| Current Status | {In Progress / Complete / Blocked / Cancelled} |
| Next Hop | {next package or waiting-for-fan-in} |
| Priority | {from dispatch or default #N} |
| Dispatched | {date or "pre-FLO"} |
| Last Activity | {most recent state file timestamp} |
| Profile | {Full / skip: [list]} |

### Active Toggles

| Package | Status | Toggled | Reason |
|---------|--------|---------|--------|
| {pkg} | {on/off} | {date or —} | {reason or —} |

### Position History

| Date | From | To | Trigger |
|------|------|----|---------|
| {date} | — | AI-PILC | Initial dispatch |
| {date} | AI-PILC | AI-ADLC | pilc-state.md Complete |
```

### Step 4: Detect Existing Anomalies

Before finalizing, check for issues that already exist:

- **Stalls:** Any project with `Last Activity` older than the stall threshold?
- **Orphans:** Any project markers found with no matching dispatch record?
- **Conflicts:** Any state where upstream and downstream signals already disagree?

```
Anomaly scan:

  ⚠️ PRJ-CRM-2026-002: Last activity 12 days ago (threshold: 7) → stall warning
  ✅ No orphan projects
  ✅ No pre-existing conflicts
```

### Step 5: Initialize Routing Log

Create `routing-log.md` (or verify it exists if resuming):

```markdown
# Routing Log — AI-FLO

**Created:** {date}
**Workspace:** {topology mode}

| # | Timestamp | Project ID | From | To | Type | Trigger | Operator | Notes |
|---|-----------|------------|------|-----|------|---------|----------|-------|
| 1 | {now} | — | — | — | Init | FLO configured | @{operator} | Mode {X}, {N} projects |
```

### Step 6: Produce Initial Route Map

Generate a visual summary of all projects and their positions:

```
📊 Route Map (initial):

  Portfolio Layer:
    AI-ILC ⇢ AI-PILC ⇢ AI-PPM ✅

  Edge:
    AI-FLO ← configured (this session)

  Project Layer:
    PRJ-ERP-2026-001:  PILC ✅ → POLC ✅ → UXD ✅ → [ADLC ⚡] → DWG (waiting)
    PRJ-CRM-2026-002:   PILC ✅ → [POLC ⚡] → UXD (waiting) → ADLC → DWG
    PRJ-MOB-2026-003:   [PILC ⚡] → POLC → UXD → ADLC → DWG

  Legend: ✅ = complete | ⚡ = in progress | ⏸ = blocked | 🚫 = skipped
```

### Step 7: Write `flo-state.md`

Commit all data to the state file:
- Header (package, version, topology, dates)
- Configuration (timeouts, fallback rules, roll-up schedule)
- All project entries (positions, profiles, toggles, history)

---

## Gate

**Approval required before proceeding to Phase 2 (Route).**

Operator must confirm:
- Project positions are accurate (no false positives)
- Configuration parameters are acceptable
- Any detected anomalies are acknowledged
- Route map correctly represents current state

---

## Transition

```
✅ Stage 3 complete. Flow state initialized.

  Topology: Mode {X}
  Projects: {N} tracked ({N} active, {N} stalled)
  Config:   timeout={N}d, stall={N}d, resolve={rule}
  
  AI-FLO is now operational. Entering hybrid mode:
  • Ask "status" for the dashboard
  • Give commands to route
  • I'll alert you when something needs attention
  
  {If pending alerts exist:}
  ⚠️ {N} alerts require your attention. Type "conflicts" to review.
```

Phase 2 stages (4-7) execute on demand as routing events occur.
Phase 3 stages (8-10) run continuously in the background.

---

*Part of AI-FLO v1.0.0*
