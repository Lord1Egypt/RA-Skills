<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-FLO — Session Continuity

**Purpose:** Rules for maintaining state across sessions, resuming flow operations, and ensuring no routing data is lost between interactions.

---

## State Persistence

AI-FLO's state is persisted in files (not in session memory):

| File | Role | Append/Overwrite |
|------|------|:----------------:|
| `flo-state.md` | Current positions, topology, project entries | Overwrite (latest state) |
| `routing-table.md` | Active routing rules + profiles | Overwrite |
| `routing-log.md` | Audit trail of all routing events | Append-only |
| `conflict-alerts/CA-*.md` | Active/resolved conflicts | Create + update |
| `dispatch-records/DR-*.md` | Dispatch history | Create (immutable) |
| `roll-up-reports/RU-*.md` | Roll-up snapshots | Create (immutable) |
| `readiness-checks/RC-*.md` | Fan-in evaluations | Create + update |

---

## Resume Protocol

When a new session starts and `flo-state.md` exists:

### Step 1: Read State
- Load `flo-state.md` → topology mode, all project entries
- Load `routing-table.md` → active routes and profiles
- Scan `conflict-alerts/` for any HOLDING conflicts

### Step 2: Display Resume Summary

```
Resuming AI-FLO (Mode {1/2/3}). {N} active projects tracked.

  Projects in motion:
  • PRJ-ERP-2026-001 — at AI-DWG (In Progress, day 3)
  • PRJ-CRM-2026-002 — at AI-ADLC (Blocked, day 12) ⚠️
  
  Pending alerts: {N}
  • 1 conflict (HOLDING): PRJ-CRM priority collision
  • 1 stall warning: PRJ-CRM no movement 12 days
  
  [S] Show full status | [A] Address alerts | [C] Continue routing
```

### Step 3: Enter Hybrid Mode
- Dashboard available on request
- Any pending alerts surface immediately
- Commands available for routing operations

---

## State Integrity Rules

1. **`flo-state.md` is the source of truth** — if session memory and state file disagree, state file wins
2. **Routing log is append-only** — never edit or delete entries; corrections are new entries with type "Correction"
3. **Conflict alerts are never deleted** — resolved ones stay (status: CLOSED) for audit
4. **Dispatch records are immutable** — once created, never modified (amendments are new records)
5. **No secrets** — never store credentials, API keys, or sensitive data in state files
6. **Portable paths** — use relative paths within the workspace; absolute only for remote `workspace_ref` in Mode 2/3
7. **Project ID is the correlation key** — every record references it; never use project name as the key (names change, IDs don't)

---

## Session Boundaries

### What Survives Between Sessions
- All file-based state (everything in `flow-orchestration/`)
- Project positions, routing table, profiles, toggles
- Conflict states (including HOLDING)
- The routing log (full history)

### What Does NOT Survive
- In-progress operations that weren't committed (if session ends mid-handoff, the handoff wasn't executed)
- Unsaved configuration changes (always write to state before confirming)
- Alert acknowledgments that weren't committed (re-alert on resume)

---

## Multi-Session Awareness

FLO may be invoked in different contexts across sessions:

| Context | FLO's Behavior |
|---------|---------------|
| Same workspace, new session | Resume from `flo-state.md` |
| Different workspace, Mode 2/3 (remote project) | Read-only position tracking (no dispatch authority) |
| Operator changed something manually between sessions | Detect drift at resume (compare state file vs. actual markers) |

### Drift Detection (on resume)

At resume, FLO scans local markers and compares against `flo-state.md`:
- If a project's actual marker status has ADVANCED beyond what FLO recorded → update state (project moved while FLO was offline)
- If a project's marker is BEHIND what FLO recorded → alert (unexpected regression — possible rework or manual intervention)
- Log any detected drift as an Info-level event

---

## Timeout Tracking Across Sessions

Conflict hold timeouts are tracked by DATE, not by session:
- `hold_since: 2026-06-15` in the conflict alert
- On resume: calculate `today - hold_since` to determine if timeout has passed
- If timeout passed while FLO was offline → immediately apply fallback resolution + log

---

*Part of AI-FLO v1.0.0*
