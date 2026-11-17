<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-UXD — Session Continuity

**Purpose:** How to resume an interrupted AI-UXD workflow. Covers state file interpretation, resume logic, and edge cases.

---

## State File Specification

The workflow state lives in `uxd-state.md` within the UXP output folder. This file is:
- Created at Stage 1 (Workspace Detection)
- Updated at every stage transition
- The single source of truth for workflow position

### Required Fields

```yaml
---
package: AI-UXD
version: 1.0.0
projectId: {PRJ-{ABBREV}-{YYYY}-{NNN} — adopted from PIP/AP, or minted if UXD originates}
projectHandle: PRJ-{ABBREV}
projectRoot: pdlc-ws/projects/PRJ-{ABBREV}-{slug}/
outputRoot: pdlc-ws/projects/PRJ-{ABBREV}-{slug}/ux/
created: {ISO date}
last_updated: {ISO date}
---
```

Plus the Workflow State table, Completed Stages log, Conditional Features flags, and Downstream Signals status.

---

## Resume Flow

### Step 1: Detect State File

On session start, scan for `uxd-state.md`:
1. Check user-provided path (if given)
2. Scan `pdlc-ws/projects/*/ux/uxd-state.md` (**default multi-project layout**), then legacy locations: `./ux-design/`, `./design/`, `./uxd/`, project root
3. If more than one project is found → read `pdlc-ws/projects/PROJECTS.md` for the ★ active project and prompt the user to resume the active project or pick another (active-project flow, `OUTPUT_AND_STATE_CONTRACT.md` §8)
4. If not found → fresh start (display welcome message)
5. If found → enter resume mode

### Step 2: Read and Validate State

Parse `uxd-state.md` and extract:
- Current Phase and Stage number
- Mode (A/B/C/D)
- Depth (Minimal/Standard/Comprehensive)
- Conditional feature flags
- Completed stages list
- Downstream signal status

Validate:
- Version compatibility (warn if state version > package version)
- Stage number in valid range (1-16)
- All completed stages have artifacts listed

### Step 3: Present Resume Options

Display:

```
Resuming AI-UXD v1.0.0
━━━━━━━━━━━━━━━━━━━━━━
Project: {projectId}
Mode: {A/B/C/D} | Depth: {level}
Current: Phase {N} — Stage {X}: {stage name}
Completed: {Y}/16 stages

[R] Resume from Stage {X}
[B] Back to Stage {X-1} (re-review last completed)
[S] Show full status (all stages + artifacts)
[D] Change depth level
```

### Step 4: Continue

Based on user selection:
- **[R]**: Load the detail file for Stage X, continue from where interrupted
- **[B]**: Load Stage X-1 detail file, present its deliverable for re-review
- **[S]**: Display full Completed Stages table with artifact paths
- **[D]**: Update depth, recalculate conditional features, continue

---

## Edge Cases

### Mid-Stage Interruption

If a session ends mid-stage (stage started but not gate-approved):
- State file shows the stage as Current but NOT in Completed list
- On resume: restart the stage from the beginning (load detail file fresh)
- Any partial artifacts from the interrupted stage are treated as drafts — present for user review

### Mode Change After Start

Mode cannot change after Stage 1 is complete. If the user needs a different mode:
- Acknowledge the request
- Warn: "Changing mode after Stage 1 requires restarting. Existing artifacts will be preserved but may not align with the new mode."
- If confirmed: reset Current Stage to 1, clear Completed Stages

### Depth Change Mid-Workflow

Depth CAN change after Stage 1:
- **Upgrading** (Minimal → Standard → Comprehensive): additional conditional features activate; already-completed stages may produce additional artifacts on the next relevant stage
- **Downgrading** (Comprehensive → Standard → Minimal): conditional features deactivate; already-produced conditional artifacts remain but no new ones generate

### Missing Artifacts

If state file references artifacts that don't exist on disk:
- Flag the discrepancy: "State file shows {artifact} was produced at Stage {N}, but the file is not found at {path}."
- Offer: "[1] Re-generate artifact | [2] Update state to remove reference | [3] Provide new path"

### Multiple UXP Folders

If multiple `uxd-state.md` files are detected:
- List all found instances with their paths and project IDs
- Ask user to select which one to resume
- Never assume — always confirm

---

## State File Update Protocol

At each stage transition:
1. Add the completed stage to the Completed Stages table
2. Update Current Phase and Current Stage to the next stage
3. Update `last_updated` timestamp
4. If conditional features changed: update Conditional Features table
5. If handoff completed: update Downstream Signals table

**Never modify completed stage entries retroactively** — they are an audit trail.

---

## Cross-Session Artifact Persistence

All artifacts are persisted as markdown files in the UXP folder. They survive between sessions:
- Stage detail files reference artifacts by relative path
- If an artifact exists, the stage can reference/revise it rather than creating from scratch
- The state file's Completed Stages table is the index of what exists

---

*Part of AI-UXD v1.0.0 | Reference: core-workflow.md § State Management*
