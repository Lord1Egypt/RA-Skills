<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-ILC — Session Continuity

**Purpose:** Define how AI-ILC maintains state across sessions and resumes cleanly after interruption. This file specifies the state file schema, resume logic, and edge cases.

---

## State File: `ilc-state.md`

The workflow maintains a single state file at the root of the output directory. This file is the source of truth for where the workflow is, what decisions have been made, and what comes next.

**Created:** During Stage 1 (Capture) — immediately after the idea is logged.
**Updated:** After EVERY stage completion — never deferred.
**Location:** `{output_root}/ilc-state.md`

---

## State File Schema

```markdown
# ILC State — {Idea Name}

## Workflow State
| Field | Value |
|-------|-------|
| **Idea Name** | {name} |
| **Idea ID** | {NNN — zero-padded Register ID} |
| **Idea Folder** | {NNN}-{idea-slug}/ |
| **Status** | {Captured / Shaped / Evaluated / Scoped / Approved / Routed / Parked / Rejected} |
| **Current Stage** | {1-6 or Complete} |
| **Depth Level** | {Minimal / Standard / Comprehensive} |
| **Domain Detected** | {architecture / governance / devops / testing / licensing / pmo / general} |
| **Route** | {pending / new-project / change-request / feature-backlog} |
| **Brief File** | {relative path under Idea Folder, or pending} |
| **Created** | {ISO date} |
| **Last Updated** | {ISO date} |
| **Producer Version** | AI-ILC v1.0.0 |

## Completed Stages
| # | Stage | Completed | Key Output |
|---|-------|-----------|-----------|
| 1 | Capture | {date} | Idea registered |
| 2 | Shape | {date or pending} | Idea Statement |
| 3 | Evaluate | {date or pending} | Score: {n}/35 |
| 4 | Scope | {date or pending} | Scope defined |
| 5 | Approve | {date or pending} | Decision: {approve/park/reject} |
| 6 | Route & Handoff | {date or pending} | Route: {destination} |

## Pending Decisions
- {Any unresolved question or deferred choice, or "None"}

## Configuration
| Field | Value |
|-------|-------|
| **Output Root** | {path} |
| **Project Exists?** | {Yes / No / Unknown} |
| **Project Name** | {name if known, or N/A} |

## Score (populated after Stage 3)
| Criterion | Score |
|-----------|:-----:|
| Problem Clarity | {1-5} |
| User Need | {1-5} |
| Strategic Fit | {1-5} |
| Differentiation | {1-5} |
| Feasibility | {1-5} |
| Reusability | {1-5} |
| Chain Value | {1-5} |
| **Total** | {n}/35 |
```

---

## Resume Flow

When a session starts and `ilc-state.md` exists:

```
1. Load ilc-state.md
2. Display resume summary:
   "Found idea '{name}' at Stage {n} ({stage_name}).
    Status: {status} | Depth: {level} | Last updated: {date}
    Resume from here? [Yes / Start fresh / Show full state]"
3. If user confirms resume:
   a. Load the stage detail file for current stage
   b. Check for pending decisions — present them first
   c. Continue from where the workflow left off
4. If user says "start fresh":
   a. Archive current state (rename to ilc-state-{date}.md)
   b. Begin new Capture stage
```

---

## State Transitions

| From Status | Valid Transitions | Trigger |
|-------------|------------------|---------|
| _(new)_ | → Captured | Stage 1 completes |
| Captured | → Shaped | Stage 2 completes |
| Shaped | → Evaluated | Stage 3 completes |
| Evaluated | → Scoped / Parked / Rejected | Stage 4 completes OR early exit at Evaluate gate |
| Scoped | → Approved / Parked / Rejected | Stage 5 completes |
| Approved | → Routed | Stage 6 completes |
| Routed | → _(terminal)_ | Workflow complete |
| Parked | → Captured _(re-entry)_ | User revisits parked idea |
| Rejected | → _(terminal)_ | Final — idea stays in register for audit |

---

## Edge Cases

### 1. Session interrupted mid-stage
- State file reflects the LAST COMPLETED stage (not the current one)
- On resume, the current stage restarts from the beginning
- No partial-stage state is persisted (avoids corruption)

### 2. User changes depth mid-workflow
- Allowed at any gate
- State file `Depth Level` updated immediately
- Subsequent stages adapt to the new depth
- Previously-completed stages are NOT re-run (they used whatever depth was active at that time)

### 3. Multiple ideas in the same workspace
- Each idea gets its own `ilc-state.md` — but v1.0 supports ONE active idea at a time
- Each idea's artifacts (Idea Statement, briefs, decision record) live in its own `{NNN}-{idea-slug}/` subfolder, keyed by the stable Register ID — so multiple ideas never collide in a flat folder
- If a state file exists with Status ≠ terminal, the user must close it (complete / park / reject) before starting a new idea
- The Idea Register tracks ALL ideas regardless of state file lifecycle (its status-sectioned tables are the at-a-glance funnel view)

### 4. Park and revisit
- When parked: state file Status = Parked; user provides a revisit date (stored in Pending Decisions)
- On revisit: load state, confirm the idea is still relevant, resume from the stage where it was parked
- If the world changed significantly: user can choose to restart from Shape (re-evaluate with new context)

### 5. State file accidentally deleted
- The Idea Register still has the entry (register is separate from state)
- Workflow cannot resume without state — must restart from Capture
- Previous briefs/decisions in the output folder still exist (not lost)

### 6. Multiple sessions working on the same idea
- NOT supported in v1.0 (single-user, single-session model)
- If detected (state file modified externally), warn user and ask for confirmation before proceeding

---

## Successor Handoff State

When AI-ILC completes (Status = Routed), the state file becomes the **marker file** that successor packages detect:

| Successor | Reads from `ilc-state.md` | Uses |
|-----------|---------------------------|------|
| AI-PILC | Route = `new-project` or `change-request` | Idea Name, Depth Level, Brief File path |
| AI-DLC v1 | Route = `feature-backlog` | Idea Name, Brief File path |

The state file is **read-only** after routing is complete. AI-ILC does not modify it further.

---

## Commands Related to State

| User says | Action |
|-----------|--------|
| "Resume" | Load state, confirm position, continue |
| "What's the status?" | Display state summary (status, stage, depth, pending decisions) |
| "Start fresh" | Archive state, begin new Capture |
| "Park this" | Set Status = Parked, log revisit date, close cleanly |
| "Reject this" | Set Status = Rejected, log rationale, close cleanly |

---

*Version: 1.0.0 | Part of AI-ILC — AI-Driven Idea Life Cycle*
