<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-POLC — Session Continuity

**Purpose:** Rules for resuming AI-POLC across sessions. The AI reads this to restore context and continue seamlessly from where the user left off.

---

## State File Specification

AI-POLC persists all session state in `polc-state.md` — the marker file that also enables downstream detection.

### Required Fields

```yaml
---
package: AI-POLC
version: 1.0.0
status: {in-progress | ready | operating}
projectId: {PRJ-{ABBREV}-{YYYY}-{NNN} — adopted from predecessor, or minted if POLC originates}
projectHandle: PRJ-{ABBREV}
projectRoot: pdlc-ws/projects/PRJ-{ABBREV}-{slug}/
outputRoot: pdlc-ws/projects/PRJ-{ABBREV}-{slug}/backlog/
project-name: {project name}
---

## Current State
- Phase: {1-6}
- Stage: {1-16}
- Depth: {minimal | standard | comprehensive}
- Mode: {standalone | chain}
- Tier 2: {active | inactive}
- Active Extensions: [{list or "none"}]

## Context Factors
- Architecture Pattern: {value or "unknown"}
- Team Topology: {value or "unknown"}
- Delivery Methodology: {value or "unknown"}
- Scale: {value or "unknown"}
- Product Maturity: {value or "unknown"}
- Market/User Type: {value or "unknown"}
- Regulatory/Compliance: {value or "unknown"}
- Funding Model: {value or "unknown"}
- Stakeholder Density: {value or "unknown"}
- Tech Debt Burden: {value or "unknown"}
- Data-Driven Capability: {value or "unknown"}
- Release Strategy: {value or "unknown"}
- Outsourcing/Distribution: {value or "unknown"}

## Backlog Summary
- Total Epics: {N}
- Prioritized: {N}
- In Release Plan: {N}
- Current Priority Model: {WSJF | MoSCoW | value-effort | custom | "not yet selected"}

## Upstream Reads (last timestamps)
- pdlc-ws/projects/*/pip/pilc-state.md: {ISO-date or "not detected"}
- pdlc-ws/projects/*/architecture/adlc-state.md: {ISO-date or "not detected"}
- pdlc-ws/projects/*/ux/uxd-state.md: {ISO-date or "not detected"}
- ilc-state.md: {ISO-date or "not detected"}
- aidlc-docs/: {ISO-date or "not detected"}

## DoR/DoD Version
- DoR: {version or "not defined"}
- DoD: {version or "not defined"}

## Pending Decisions
- {list of decisions awaiting user input, or "none"}

## Last Session Summary
- Date: {ISO-date}
- What was done: {brief summary}
- Next action: {what should happen next}
```

---

## Resume Protocol

When a session starts and `polc-state.md` already exists:

### Step 1: Load State

1. Read `polc-state.md` completely
2. Restore: current phase, stage, depth, mode, tier activation, extensions
3. Note any pending decisions

### Step 2: Scan for Upstream Changes

Run the session-start routine (defined in `core-workflow.md`):

1. Check `ilc-state.md` — new feature routed?
2. Check governance spine — new PILC-C entries since last timestamp?
3. Check `uxd-state.md` — timestamp newer than recorded?
4. Check `aidlc-docs/` — changes since last review?

Present any detected changes to the user before resuming.

### Step 3: Confirm Context

Present to the user:

```
Resuming AI-POLC session for: {project-name}
Current position: Phase {N}, Stage {N} ({stage name})
Depth: {level}
Mode: {standalone | chain}
{If upstream changes detected: list them}
{If pending decisions: list them}

Continue from Stage {N}, or would you like to do something else?
```

### Step 4: Proceed

Based on user response:
- **Continue** → Load the relevant stage detail file and proceed
- **Different stage** → Navigate to requested stage (Operations phase stages can be entered directly)
- **Process upstream changes** → Handle detected changes first

---

## State Transitions

| Event | State Change |
|-------|-------------|
| First session start | status: `in-progress`, Phase 1, Stage 1 |
| Stage gate passed | Stage increments (or jumps if user directs) |
| Phase gate passed | Phase increments; new phase's first stage begins |
| PBP assembled (Stage 13 complete) | status: `ready` |
| First Operations stage entered | status: `operating` |
| Reprioritization | Backlog Summary updated; POLC-C logged |
| DoR/DoD change | DoR/DoD Version bumped; POLC-C logged |
| Extension activated | Added to Active Extensions list |
| Context factor established | Updated in Context Factors section |

---

## Cold Start vs. Warm Resume

| Scenario | Behavior |
|----------|----------|
| **No `polc-state.md` found** (scan `pdlc-ws/projects/*/backlog/polc-state.md` + legacy) | Cold start → Stage 1 (Workspace Detection) |
| **`polc-state.md` exists, status = in-progress** | Warm resume → present position, offer to continue |
| **`polc-state.md` exists, status = ready** | PBP complete → offer Operations (Stage 14-16) or modifications |
| **`polc-state.md` exists, status = operating** | Active product → Operations re-entry, upstream scan first |

---

## Multi-Session Patterns

### Pattern A: Initial Build (Sessions 1–N until PBP is assembled)

```
Session 1: Stage 1-3 (Foundation) → save state
Session 2: Resume → Stage 4-5 (Strategy start) → save state
Session 3: Resume → Stage 6-7 (Strategy finish) → save state
Session 4: Resume → Stage 8-10 (Governance) → save state
Session 5: Resume → Stage 11-13 (Stakeholders + Assembly) → status=ready
```

### Pattern B: Operations Cycle (Standalone mode — repeating)

```
Session N: Resume (operating) → Stage 14 (refine) → Stage 15 (accept) → save
Session N+1: Resume → upstream scan → Stage 14 (refine) → save
Session N+2: Resume → Stage 15 (accept) → Stage 16 (metrics) → save
```

### Pattern C: Operations On-Demand (Chain mode — re-entry)

```
Session N: Resume (operating) → upstream change detected (DLC completed 3 stories)
           → Stage 15 (accept/reject) → reprioritize → save
Session N+1: Resume → user says "refine the backlog" → Stage 14 → save
Session N+2: Resume → user says "review metrics" → Stage 16 → save
```

---

## What Gets Persisted vs. What Doesn't

| Persisted (in files) | NOT persisted (session-only) |
|---------------------|------------------------------|
| All state (polc-state.md) | Conversation history |
| All artifacts (vision, epics, etc.) | Intermediate reasoning |
| Governance spine entries | Draft options not selected |
| Context factors | Question-answer details |
| Upstream read timestamps | Extension detection history |

**Rule:** If the user can't continue without it next session, it MUST be in a file.

---

## MANDATORY: Incremental File Output

Every stage produces one or more output files. You MUST write these files to the workspace filesystem **immediately upon gate approval** — do NOT defer artifact creation to a later stage or to the Assembly phase (Stage 13).

**The rule:** When a user approves a gate, the stage's "Persist" / "Write" step has already happened or happens NOW. The file(s) listed in that stage's detail file are created/updated on disk before you transition to the next stage. The user should be able to see their project's artifacts building up incrementally as they progress through the workflow.

**Why:** Users lose confidence when they approve 4 phases of work and see nothing on disk. The Assembly stage (13) is for verification and packaging — not for first-time file creation.

**Minimum per-stage writes:**

| Stage | File(s) Written on Gate Approval |
|-------|----------------------------------|
| 1 | `polc-state.md` + `management_framework/` skeleton |
| 2 | `product-vision.md` |
| 3 | `po-charter.md` |
| 4 | `roadmap.md` |
| 5 | `epics/EPIC-NNN_*.md` (one per epic) |
| 6 | `prioritization-register.md` |
| 7 | `release-plan.md` |
| 8 | `definition-of-ready.md` + `definition-of-done.md` |
| 9 | `product-risk-register.md` |
| 10 | `traceability-matrix.md` |
| 11 | `stakeholder-map.md` |
| 12 | `release-notes-governance.md` |
| 13 | `PBP_README.md` (assembly summary) |

If a gate is approved but you haven't yet written the file, write it NOW before presenting the next stage's opening.

---

*Load this file at workflow start and on every resume.*
