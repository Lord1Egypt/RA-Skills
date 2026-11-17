<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Session Continuity

## Purpose

AI-ADLC architecture design typically spans multiple sessions (days or weeks). This document defines how the workflow preserves state, resumes gracefully, and ensures no decisions or design context is lost between sessions.

---

## State File Specification

### Location

The state file is always located at: `{output_root}/adlc-state.md`.

In the standard multi-project layout, `{output_root}` = `{project_root}/architecture/` where `{project_root}` = `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/`. So the marker resolves to `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/architecture/adlc-state.md`. The shared spine is a sibling at `{project_root}/management_framework/`. (See `OUTPUT_AND_STATE_CONTRACT.md` §4.)

### Structure

```markdown
# AI-ADLC State — {system_name}

## Configuration

| Key | Value |
|-----|-------|
| System Name | {system_name} |
| Project ID | {project_id}  (adopted from PIP; minted only if ADLC originates) |
| Project Handle | PRJ-{ABBREV} |
| Project Root | {project_root}  (= pdlc-ws/projects/PRJ-{ABBREV}-{slug}/) |
| Started | {ISO 8601 timestamp} |
| Last Updated | {ISO 8601 timestamp} |
| Producer Version | AI-ADLC v1.1.0 |
| Workflow Depth | {Minimal / Standard / Comprehensive} |
| Output Structure | {numbered / phase-folders / custom} |
| Output Root | {path}  (= {project_root}/architecture/) |
| Input Source | {PIP path / PRD path / "verbal" / "brownfield"} |
| Input Mode | {Full PIP / Requirements Doc / Verbal / Brownfield} |
| Current Phase | {phase_name} |
| Current Stage | {stage_number} |
| Status | {In Progress / Paused / Complete} |

## Progress

| Stage # | Stage Name | Status | Completed | Notes |
|:-------:|------------|:------:|:---------:|-------|
| 1 | Workspace Detection | ✅ Done | {timestamp} | |
| 2 | Requirements Ingestion | ✅ Done | {timestamp} | Mode: {PIP/PRD/Verbal} |
| 3 | Architecture Vision | ✅ Done | {timestamp} | {n} principles defined |
| 4 | System Context (C4 L1) | ✅ Done | {timestamp} | {n} actors, {m} external systems |
| 5 | Container Design (C4 L2) | 🔄 Active | — | In progress |
| 6 | Technology Stack | ⏳ Pending | — | |
| 7 | Multi-Tenancy | ⏳ Pending | — | Conditional |
| 8 | Security & Identity | ⏳ Pending | — | |
| 9 | Data Architecture | ⏳ Pending | — | |
| 10 | API Architecture | ⏳ Pending | — | |
| 11 | Integration & Infrastructure | ⏳ Pending | — | |
| 12 | Component Design (C4 L3) | ⏳ Pending | — | |
| 13 | Package Assembly | ⏳ Pending | — | |

## ADR Register

| ADR # | Title | Stage | Status | Decision Summary |
|:-----:|-------|:-----:|:------:|-----------------|
| ADR-001 | {title} | 6 | Accepted | {1-line summary} |
| ADR-002 | {title} | 7 | Accepted | {1-line summary} |

## Architecture Principles (from Stage 3)

| ID | Principle | One-Line Summary |
|:--:|-----------|-----------------|
| P1 | {name} | {summary} |
| P2 | {name} | {summary} |

## Key Constraints (from Stage 3)

| Constraint | Source | Impact |
|-----------|--------|--------|
| {constraint} | {source} | {impact} |

## Open Questions (from Workbook)

| # | Question | Priority | Raised At | Target Stage |
|---|----------|:--------:|:---------:|:------------:|
| 1 | {question} | {H/M/L} | Stage {n} | Stage {m} |

## Containers (from Stage 5)

| Container | Technology | Responsibility |
|-----------|-----------|---------------|
| {name} | {tech or TBD} | {what it does} |
```

---

## Session Start Behavior

### Step 1: Detect State

1. Scan for `adlc-state.md`, in order:
   - `pdlc-ws/projects/*/architecture/adlc-state.md` (**default multi-project layout**)
   - `./adlc-state.md`
   - `./{system_name}/adlc-state.md`
   - `./architecture/adlc-state.md`
2. **If multiple projects are found:** read `pdlc-ws/projects/PROJECTS.md` for the ★ active project and run the active-project selection prompt (resume the chosen project, or start architecture for one that has a PIP but no architecture).
3. If still NOT found → treat as fresh start (go to core-workflow Stage 1).

### Step 2: Load State

1. Read the complete state file
2. Parse configuration, progress, ADR register, principles, constraints, containers
3. Identify the current active stage

### Step 3: Load Architecture Context

Unlike AI-PILC (which only needs state), AI-ADLC requires loading **architectural context** for meaningful resumption:

1. Load the Architecture Vision (principles + constraints) — needed for ALL stages
2. Load the System Context (actors + externals) — needed from Stage 5 onward
3. Load the Container list — needed from Stage 6 onward
4. Load ADR summaries — needed for consistency checking

This context is stored in the state file specifically so the AI doesn't need to re-read all documents.

### Step 4: Present Resumption Summary

```
🔄 AI-ADLC Session Resumed

📋 System: {system_name}
📍 Current Position: Stage {n} — {stage_name} ({phase_name} Phase)
📅 Last Activity: {last_updated}
✅ Completed: {n} stages
⏳ Remaining: {n} stages
📐 ADRs produced: {n}

🏗️ Architecture Context:
   • Principles: {n} defined (P1: {name}, P2: {name}, ...)
   • Constraints: {n} active
   • Containers: {n} identified
   • External systems: {n} mapped
   • Open questions: {n}

Shall I:
(a) Continue from where we left off (Stage {n}: {stage_name})
(b) Show what's been designed so far (architecture summary)
(c) Go back to a previous stage for revision
(d) Show open questions from the workbook
(e) Show ADR register
```

### Step 5: Confirm Position

Wait for user response before proceeding.

---

## Session End Behavior

### Graceful Save

1. Update `adlc-state.md` with current position
2. Mark active stage as 🔄 Active
3. Save any in-progress drafts (even incomplete, marked DRAFT)
4. Update Architecture Workbook with any new open questions
5. Ensure all ADRs produced this session are registered in state

### Auto-Save Triggers

State MUST be updated:
- After every stage completion
- After every ADR is produced
- After every gate approval
- When user requests a pause
- After principles or constraints are modified

---

## Resuming Mid-Stage

If session ended mid-stage:

1. Check if a partial draft exists for that stage's document
2. If YES → present: "I found an in-progress draft for {stage_name}. Continue from here or start fresh?"
3. If NO → re-enter stage from beginning using context from state file

**Context recovery priority:**
1. Architecture principles and constraints (always needed)
2. Container list (needed for design stages)
3. Technology decisions made so far (needed for consistency)
4. The specific stage's predecessor output (immediate input)

---

## Multi-Session Patterns for Architecture

| Pattern | Description | Guidance |
|---------|-------------|----------|
| **Decision workshop** | User brings a specific question ("should we use Kafka or RabbitMQ?") | Focus on that ADR; park other stages |
| **Phase-per-session** | One phase per sitting | Natural breakpoints at phase boundaries |
| **Deep dive** | One complex stage (e.g., multi-tenancy) takes a full session | Normal; architecture depth justifies it |
| **Stakeholder gap** | User pauses to consult team on a decision | Log in Workbook; resume when answer arrives |
| **Iteration** | User returns to revise after learning more in later stages | Update earlier docs; cascade consistency changes |
| **Brownfield update** | User has existing architecture; adding/changing components | Load existing; identify deltas; focus on changes |

---

## Stage Reordering Rules

### Fixed Order (Must Not Reorder)
- Stages 1-3 (FOUNDATION) — must come first
- Stage 4 before Stage 5 — context before containers
- Stage 5 before Stage 6 — containers before tech stack selection
- Stage 13 (Assembly) — must be last

### Flexible Order
- Stages 6-8 (DECISIONS) — can be done in any order based on what the user needs to decide first
- Stages 9-12 (DESIGN) — can be done in any order based on priority

### Reorder Logging
When user reorders:
1. Log in Architecture Workbook: "Stages reordered: {original} → {new}. Reason: {reason}"
2. Update state file
3. Verify no dependency issues (e.g., don't do data architecture before database is selected)

---

## Architectural Consistency on Resume

When resuming, the AI must verify consistency:

| Check | What Could Drift |
|-------|-----------------|
| Principles still hold | User may have discovered a principle needs changing |
| Constraints unchanged | New information may relax or tighten constraints |
| Container list stable | Earlier design may need revision based on later discoveries |
| ADRs not conflicting | Later decisions may invalidate earlier ones |

If inconsistency detected:
1. Flag to user: "I notice Stage {earlier} assumed X but Stage {later} decided Y. Should I update?"
2. Log the update in Architecture Workbook
3. Update affected documents

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| User wants to change a principle mid-workflow | Accept change; log in Workbook; flag which downstream documents may be affected |
| ADR needs reversal | Change ADR status to "Superseded by ADR-{nnn}"; produce new ADR; update affected docs |
| New external system discovered during DESIGN | Add to System Context (Stage 4 update); add integration in Stage 11 |
| Container split/merge during DESIGN | Update C4 L2; cascade to tech stack and component design |
| User provides new constraint | Add to state file constraints; check all existing decisions still comply |

---

## State File Maintenance Rules

1. **Never overwrite** — always update in place or append
2. **Timestamps** — ISO 8601 format
3. **Atomic updates** — update immediately after each event
4. **Human-readable** — user can read the state file directly
5. **Context-rich** — store enough architectural context in state that a session can resume without re-reading all documents
6. **No secrets** — never store credentials or sensitive security details in state
7. **Relative paths** — portable across machines
