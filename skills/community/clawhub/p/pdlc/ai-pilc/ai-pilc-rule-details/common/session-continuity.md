<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Session Continuity

## Purpose

AI-PILC workflows may span multiple sessions (days, weeks, or longer). This document defines how the workflow preserves state, resumes gracefully, and ensures no progress is lost between sessions.

---

## State File Specification

### Location

The state file is always located at: `{output_root}/pilc-state.md`.

In the standard multi-project layout, `{output_root}` = `{project_root}/pip/` where `{project_root}` = `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/`. So the marker resolves to `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/pip/pilc-state.md`. The governance spine is a sibling of `pip/` at `{project_root}/management_framework/`. (See `OUTPUT_AND_STATE_CONTRACT.md` §4.)

### Structure

```markdown
# AI-PILC State — {project_name}

## Configuration

| Key | Value |
|-----|-------|
| Project Name | {project_name} |
| Project ID | {project_id} |
| Project Handle | PRJ-{ABBREV} |
| Project Root | {project_root}  (= pdlc-ws/projects/PRJ-{ABBREV}-{slug}/) |
| Route | project |
| Originating Idea | {idea_ref} |
| derivedFrom | {idea_ref} |
| originType | project |
| Started | {ISO 8601 timestamp} |
| Last Updated | {ISO 8601 timestamp} |
| Producer Version | AI-PILC v1.0.0 |
| Workflow Depth | {Minimal / Standard / Comprehensive} |
| Output Structure | numbered |
| Output Root | {path}  (= {project_root}/pip/) |
| Source Document | {path or "inline"} |
| Current Phase | {phase_name} |
| Current Stage | {stage_number} |
| Status | {In Progress / Paused / Complete} |

## Progress

| Stage # | Stage Name | Status | Completed | Notes |
|:-------:|------------|:------:|:---------:|-------|
| 1 | Workspace Detection | ✅ Done | {timestamp} | |
| 2 | Source Document Ingestion | ✅ Done | {timestamp} | Depth: Standard |
| 3 | Requirement Structuring | ✅ Done | {timestamp} | |
| 4 | Requirements Analysis | ✅ Done | {timestamp} | 3 critical, 5 high findings |
| 5 | Clarification Cycle | ✅ Done | {timestamp} | 8 questions resolved |
| 6 | Feasibility Assessment | 🔄 Active | — | In progress |
| 7 | Prioritization | ⏳ Pending | — | |
| ... | ... | ... | ... | |

## Decisions Made

| Decision ID | Stage | Summary |
|:-----------:|:-----:|---------|
| D-001 | 2 | Source accepted; complexity = High; depth = Standard |
| D-002 | 5 | AI automation boundary: rule-based auto-executes, AI requires confirmation |
| ... | ... | ... |

## Open Items

| Type | ID | Description | Owner | Due |
|------|:--:|-------------|-------|-----|
| Action | A-003 | Confirm budget envelope with Finance | Sponsor | Before Stage 8 |
| Issue | I-001 | Technical Lead not yet identified | PM | Before Stage 9 |
| ... | ... | ... | ... | ... |

## Register Counts

| Register | Entries |
|----------|:-------:|
| Decisions | {n} |
| Changes | {n} |
| Issues | {n} |
| Actions | {n} |
| Assumptions | {n} |
| Lessons | {n} |
```

---

## Session Start Behavior

When a new session begins, the AI MUST follow this sequence:

### Step 1: Detect State

1. Scan for `pilc-state.md`, in order:
   - `pdlc-ws/projects/*/pip/pilc-state.md` (**default multi-project layout**)
   - `{output_root}/pilc-state.md` (the expected location from state, if known)
   - `./pilc-state.md`
   - `./pilc-docs/pilc-state.md`
   - `./{numbered_folder_root}/pilc-state.md`
2. **If multiple projects are found:** read `pdlc-ws/projects/PROJECTS.md` for the ★ active project and run the active-project selection prompt (see `inception/workspace-detection.md` Step 1) — resume the chosen project, or originate a new one.
3. If exactly one is found → load it and resume.
4. If still NOT found → treat as fresh start (go to core-workflow Stage 1).

### Step 2: Load State

1. Read the complete state file
2. Parse configuration, progress, decisions, and open items
3. Identify the current active stage (status = 🔄 Active or first ⏳ Pending)

### Step 3: Present Resumption Summary

Display to the user:

```
🔄 AI-PILC Session Resumed

📋 Project: {project_name}
🆔 Project ID: {project_id}
📍 Current Position: Stage {n} — {stage_name} ({phase_name} Phase)
📅 Last Activity: {last_updated}
✅ Completed: {n} stages
⏳ Remaining: {n} stages

📊 Quick Status:
   • Decisions logged: {n}
   • Open actions: {n}
   • Open issues: {n}

Shall I:
(a) Continue from where we left off (Stage {n}: {stage_name})
(b) Show a summary of what's been completed so far
(c) Go back to a previous stage for revision
(d) Show open items that need attention
```

### Step 4: Confirm Position

- Wait for user to confirm or redirect
- If user confirms (a) → resume the active stage
- If user selects (b) → display completed stages summary, then ask what to do
- If user selects (c) → ask which stage to revisit; update state accordingly
- If user selects (d) → display open actions/issues; ask if any are resolved

---

## Session End Behavior

When a session is about to end (user signals stop, timeout, or natural breakpoint):

### Graceful Save

1. Update `pilc-state.md` with current position
2. Mark the active stage as 🔄 Active (not ⏳ Pending — it was started)
3. Save any in-progress drafts to the output folder (even if incomplete, marked as DRAFT)
4. Log a Lesson Learned if appropriate (e.g., "Session ended mid-stage; recommend completing Feasibility scoring in next session")

### Auto-Save Triggers

The state file MUST be updated:
- After every stage completion
- After every decision is logged
- After every gate approval
- When user requests a pause
- Before any potentially destructive operation

---

## Resuming Mid-Stage

If a session ended in the middle of a stage (not at a gate), the workflow must:

1. Check if a partial draft exists for that stage's deliverable
2. If YES → load the draft and present: "I found an in-progress draft for {stage_name}. Shall I continue from here, or start this stage fresh?"
3. If NO → re-enter the stage from the beginning (re-read inputs, regenerate)

**Context recovery:** The AI should re-read:
- The source document (or its structured form from Stage 3)
- The most recent completed deliverable (for context)
- Any decisions made in the current phase
- Open items relevant to the current stage

---

## Multi-Day Workflow Patterns

AI-PILC is designed for projects that take multiple sessions to initiate. Common patterns:

| Pattern | Description | Guidance |
|---------|-------------|----------|
| **Sprint session** | User completes 2-4 stages in one long session | Normal flow; gates between stages |
| **Daily check-in** | User does one stage per day | State file is critical; resume summary each day |
| **Stakeholder gap** | User pauses to collect input from others | Log pending items as Actions; resume when answers arrive |
| **Iterative refinement** | User returns to revise earlier stages after learning more | Update state; re-enter earlier stage; cascade changes forward |
| **Parallel tracks** | User works on Planning stages in flexible order | State tracks each independently; stages 10-14 can run in any order |

---

## Stage Reordering Rules

While the default flow is sequential (1→16), some stages can be reordered:

### Fixed Order (Must Not Reorder)
- Stages 1-3 (INCEPTION) — must be first; builds foundation
- Stage 4 before Stage 5 — analysis must precede clarification
- Stage 6 before Stage 7 — feasibility before prioritization
- Stage 8 before Stage 9 — business case before charter
- Stage 16 (Package Assembly) — must be last

### Flexible Order (User Can Reorder)
- Stages 10-14 (PLANNING) — can be done in any order based on user preference
- Stage 15 can be started any time after Stage 9

### Reorder Logging
When user requests reordering:
1. Log in Decision Log: "User reordered stages: {original} → {new order}. Rationale: {reason}"
2. Update state file progress section to reflect new sequence
3. Proceed with user's preferred order

---

## Edge Cases

### Corrupted State File
If the state file exists but cannot be parsed:
1. Inform the user: "State file found but appears corrupted. I can see the output files that exist."
2. Scan the output folder structure for completed deliverables
3. Infer progress from what files exist
4. Present inferred state for user confirmation
5. Recreate state file from inferred + confirmed state

### Source Document Changed
If user indicates the source requirements have been updated since last session:
1. Ask: "Has the scope changed significantly, or are these clarifications/corrections?"
2. If clarifications → update relevant artifacts going forward; no need to restart
3. If significant change → recommend revisiting from Stage 3 (Requirement Structuring)
4. Log in Change Log: "Source document updated. Impact: {assessment}"

### User Wants to Restart
If user explicitly requests a fresh start:
1. Confirm: "This will archive the current state and begin fresh. Proceed?"
2. If confirmed → rename existing state file to `pilc-state-{timestamp}.archived.md`
3. Begin from Stage 1
4. Log in Lessons Learned: "Workflow restarted. Reason: {user's reason}"

---

## State File Maintenance Rules

1. **Never overwrite** — always append or update in place
2. **Timestamps** — use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
3. **Atomic updates** — update state immediately after the event, not in batches
4. **Human-readable** — state file is Markdown; user can read it directly
5. **No secrets** — never store credentials, API keys, or sensitive personal data in state
6. **Portable** — state file references relative paths only (portable across machines)
7. **Project ID is immutable** — once minted at Stage 1, `Project ID` never changes. It is the family-wide correlation key (AI-FLO routing, AI-PPM roll-up). The Charter (Stage 9) confirms it; it must never be regenerated or re-formatted mid-workflow.


---

## Output Structure Conventions

The `Output Structure` field in `pilc-state.md` is always `numbered` — the deliverable layout **inside `pip/`** is fixed (not a user choice). In the standard multi-project layout everything nests under the project root; the spine is a sibling of `pip/`. The "Flat" layout below is retained for **backwards-compatibility detection only** (older single-project output) — it is never offered to the user for new work.

### Numbered (Always — Standard)

```
pdlc-ws/projects/
├── PROJECTS.md                          ← registry + active pointer
└── PRJ-{ABBREV}-{slug}/                  ← {project_root}
    ├── management_framework/             ← governance spine (project root, shared)
    │   ├── MANAGEMENT_FRAMEWORK.md
    │   ├── Decision_Log.md · Change_Log.md · Issue_Log.md
    │   ├── Action_Items.md · Assumptions_Dependencies.md · Lessons_Learned.md
    │   └── dashboards/                   ← per-project dashboards (DASHBOARD contract §2)
    └── pip/                              ← {output_root} — AI-PILC deliverables
        ├── pilc-state.md
        ├── 01_Requirement_Intake_Form.md
        ├── 02_Requirements_Analysis_Report.md
        ├── … (03–12 deliverables) …
        └── PROJECT_INITIATION_PACKAGE_README.md
```

### Flat (Legacy — Backwards-Compat Detection Only)

```
pdlc-ws/projects/PRJ-{ABBREV}-{slug}/
├── management_framework/                 ← governance spine (project root, shared)
└── pip/                                  ← {output_root}
    ├── pilc-state.md
    ├── pilc-docs/
    │   ├── inception/ · assessment/ · justification/
    │   ├── authorization/ · planning/ · mobilization/
    └── PROJECT_INITIATION_PACKAGE_README.md
```

**Detection guarantee:** Regardless of deliverable structure, these are ALWAYS findable:
- `pilc-state.md` — always at `{output_root}/` (= `{project_root}/pip/`) — the marker file
- `PROJECT_INITIATION_PACKAGE_README.md` — always at `{output_root}/`
- `management_framework/` — always at `{project_root}/management_framework/` (one level up from `pip/`)

**Why this matters:** AI-ADLC scans `pdlc-ws/projects/*/pip/pilc-state.md` (and legacy locations) for its input marker. Once found, it knows the project root, reads the shared spine one level up, and writes its own output into `{project_root}/architecture/` — regardless of PILC's deliverable structure choice.

---

## Skipping and Customization

Users may request to:
- **Skip a stage** → Log decision with rationale; mark as "Skipped" in state
- **Combine stages** → Execute both but produce a single merged deliverable
- **Add custom stages** → Insert at user-specified position; track in state
- **Change depth mid-workflow** → Update state; adjust remaining stages accordingly
- **Stop early** → Generate partial package with completeness report noting what's missing

All customizations are logged in the Decision Log.
