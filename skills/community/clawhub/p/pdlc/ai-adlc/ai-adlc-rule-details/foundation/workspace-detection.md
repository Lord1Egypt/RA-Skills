<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Workspace Detection & Context Loading

## Stage: 1 of 13
## Phase: 🔵 FOUNDATION
## Execution: ALWAYS

---

## Purpose

Detect whether this is a fresh start or resumed workflow, configure the output environment, detect available inputs (PIP, existing architecture, requirements), and establish the Architecture Workbook and ADR structure. This stage produces no architecture artifact — it sets up the workspace for everything that follows.

---

## Depth Adaptation

N/A — this stage is depth-independent. Workspace detection and setup execute identically regardless of project complexity.

---

## Step-by-Step Execution

### Step 1: Check for Existing State

1. Scan for `adlc-state.md`, in order:
   - `pdlc-ws/projects/*/architecture/adlc-state.md` (**default multi-project layout**)
   - `./adlc-state.md`
   - `./{system_name}/adlc-state.md`
   - `./architecture/adlc-state.md`
   - Any directory the user has specified
2. **If multiple projects are found:** read `pdlc-ws/projects/PROJECTS.md` for the ★ active project and prompt: work on the active project, pick another, or start architecture for a project that has a PIP but no architecture yet. Resume the chosen project's `adlc-state.md`, or proceed to Step 2 for a project without ADLC output.
3. If exactly one is found → load it and follow **Session Resumption Flow** (`common/session-continuity.md`).
4. If NONE found → proceed to Step 2 (fresh start — origination or PIP adoption).

---

### Step 2: Collect System Identity

Ask the user:

```markdown
### Q-CFG-01: System/Project Name

**Context:** This name will appear in all architecture documents, diagrams, ADRs, and the state file.

**Your input:** What is the name of the system or platform being designed?

**Format expected:** Short identifier (e.g., "Fleet Management System", "Payment Gateway", "Logistics Platform")
```

Wait for response. Store as `{system_name}`.

---

### Step 3: Initialize Output Structure

The document sub-structure inside `architecture/` is **deterministic — always numbered**. Do NOT ask the user. This matches the pattern used by AI-PILC (`pip/01_*`) and all other lifecycle packages.

```
architecture/
├── 01_Architecture_Vision.md
├── 02_System_Context_C4L1.md
├── 03_Containers_C4L2.md
├──...
├── ADR/
│   └── ADR-000_Template.md
├── Architecture_Workbook.md
└── adlc-state.md
```

Record `Output Structure: numbered` in the state file.

---

### Step 4: Configure Output Location

The output location is **fixed** — `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/architecture/` (the standard multi-project layout). There is no user choice for the project folder path. This aligns with `OUTPUT_AND_STATE_CONTRACT.md` §3 (the Always-On Rule).

- **If a PIP is detected** (Step 5): adopt that project — `{project_root}` = the PIP's project root (one level up from its `pip/`); ADLC output → `{project_root}/architecture/`. The Project ID is **adopted, never re-minted** (Step 5a).
- **If originating** (no PIP — ADLC run first): derive `{ABBREV}`/`{slug}` from the system name and create `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/`, then output to `architecture/`.

Set `{output_root}` = `{project_root}/architecture/`. The spine lives at `{project_root}/management_framework/`.

> **Brownfield exception:** if the workspace already contains ADLC output in an older flat layout, detect it on first run and inform the user: "Existing architecture output found at `{path}`. AI-ADLC now uses `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/architecture/` as the standard location. I'll operate in the standard location — you may migrate existing artifacts at your convenience." Never force-move existing files.

---

### Step 5: Detect Available Inputs

Scan the workspace for existing context:

#### Check for AI-PILC Output (PIP)

Look for (in order):
- `pdlc-ws/projects/*/pip/pilc-state.md` (**default multi-project layout**)
- `pilc-state.md` (anywhere in workspace — legacy/flat)
- Numbered PIP folders (`01_Requirement_Submission/`, `04_Project_Charter/`, etc.)
- `PROJECT_INITIATION_PACKAGE_README.md`

If found → flag as: "PIP detected at: {path}", and record the project root (one level up from `pip/`).

#### Step 5a: Adopt the Project ID (never re-mint)

If a PIP is found, read `Project ID`, `Project Handle`, and `Project Root` from `pilc-state.md` and **adopt** them unchanged — AI-ADLC never mints a new ID when a project already exists (correlation-key rule,). Persist them into `adlc-state.md` (Step 10).

**Originator-eligibility (no PIP found):** AI-ADLC is originator-eligible (`OUTPUT_AND_STATE_CONTRACT.md` §7). If no PIP and no existing project, ADLC **mints** `PRJ-{ABBREV}-{YYYY}-{NNN}` (asking the user for name/abbreviation), creates `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/`, seeds the spine + the `pdlc-ws/projects/PROJECTS.md` registry row (★ active), then proceeds — create-if-absent, exactly like the default originator.

#### Check for Requirements Documents

Look for common patterns:
- `**/requirements*.md`
- `**/PRD*.md`
- `**/__input/**`
- `**/specs/**`

If found → flag as: "Requirements document(s) detected: {paths}"

#### Check for Existing Architecture (Brownfield)

Look for:
- Existing C4 diagrams or architecture docs
- `**/architecture/**`
- `**/ADR/**`
- Previous `adlc-state.md` (archived)

If found → flag as: "Existing architecture artifacts detected: {paths}"

#### Check for AI-UXD Output (UXP — same-layer peer)

AI-UXD runs concurrently with AI-ADLC (same Project layer). Scan for its marker (direct same-layer read — no AI-FLO):
- `pdlc-ws/projects/*/ux/uxd-state.md` (**default multi-project layout**)
- legacy `./ux/`, `./ux-design/`, `./design/`

If found → flag as: "UX Design Package detected at: {path}" and feed it into Stage 2 (the **UX→Architecture feed**: user flows, client/platform needs, and the accessibility target become architecture drivers/NFRs).

> **Ordering reality (+ reconciliation):** ADLC frequently runs *before* UXD completes, so `uxd-state.md` may be absent now. That is fine — architecture proceeds standalone. If a UXP appears or updates **after** the AP exists, Stage 2 offers a non-destructive reconciliation pass over the UX-driven drivers/NFRs (see `requirements-ingestion.md`). Absence never blocks.

#### Check for AI-POLC Output (PBP — same-layer peer)

AI-POLC runs concurrently with AI-ADLC (same Project layer). Scan for its marker (direct same-layer read — no AI-FLO):
- `pdlc-ws/projects/*/backlog/polc-state.md` (**default multi-project layout**)
- legacy `./backlog/`, `./product-backlog/`

If found → flag as: "Product Backlog Package detected at: {path}" and feed it into Stage 2 (the **Product→Architecture feed**: functional scope, priorities, expected scale/volume, business constraints, roadmap timing become architecture drivers).

> **Ordering reality (+ reconciliation):** ADLC frequently runs *before* POLC completes, so `polc-state.md` may be absent now. That is fine — architecture proceeds from PIP or standalone input. If a PBP appears or updates **after** the AP exists, Stage 2 offers a non-destructive reconciliation pass over the Product-driven scope/priority changes (see `requirements-ingestion.md`). Absence never blocks.
> 
> **Architecture → Product cost loop (§5 Loop 2):** When architecture produces cost/risk verdicts that reshape prioritization, ADLC records this in the Architecture Workbook as a feedback signal for POLC — it does NOT directly modify the backlog. POLC reads the AP and decides whether to re-prioritize.

---

### Step 6: Present Detection Results

```markdown
## Workspace Scan Results

| Detected | Path | Usable As |
|----------|------|-----------|
| {PIP / Requirements / Architecture / None} | {path} | {Input for Stage 2} |

**Input mode determined:** {PIP / Document / Verbal / Brownfield}
```

If multiple input sources found, ask:

```markdown
### Q-CFG-04: Primary Input Source

**Context:** I found multiple input sources. Which should I use as the primary reference?

**Found:**
- {Source 1}: {path}
- {Source 2}: {path}

**Options:**
- (a) Use {Source 1} as primary
- (b) Use {Source 2} as primary
- (c) Use both — {Source 1} as primary, {Source 2} as supplementary

**Your Decision:** _[awaiting input]_
```

---

### Step 7: Create Folder Structure

Output nests under the project root. `{output_root}` = `{project_root}/architecture/`; the spine is a sibling at `{project_root}/management_framework/`.

```
pdlc-ws/projects/PRJ-{ABBREV}-{slug}/                ← {project_root}
├── management_framework/                     ← shared spine (create-if-absent, Step 9b)
├── pip/                                      ← AI-PILC output (if PIP exists)
└── architecture/                             ← {output_root} — AI-ADLC output
    ├── ADR/
    │   └── ADR-000_Template.md
    ├── Architecture_Workbook.md
    └── adlc-state.md
```

> The spine is a **sibling** of `architecture/` at the project root (shared across packages), not inside `architecture/`. The `adlc-state.md` marker is always at `{output_root}/` (= `{project_root}/architecture/`).

---

### Step 8: Create ADR Template

Create `ADR/ADR-000_Template.md` using template `templates/adr-template.md`.

This serves as the reference format for all ADRs produced during the workflow.

---

### Step 9: Create Architecture Workbook

Create `Architecture_Workbook.md` with initial structure:

```markdown
# {system_name} — Architecture Workbook

**Purpose:** Living document tracking architecture decisions backlog, open questions, and discussion notes.

---

## Decision Backlog

| # | Decision Area | Key Question | Priority | Status |
|---|--------------|--------------|:--------:|:------:|
| 1 | _[To be populated during workflow]_ | | | |

---

## Open Questions

_None yet — questions will be added as they arise during design._

---

## Discussion Notes

_Captured during architecture sessions._

---

## Architecture Sessions Log

| Session | Date | Stages Covered | Key Outcomes |
|:-------:|:----:|:---------------|:-------------|
| 1 | {today} | Stage 1: Workspace Detection | Setup complete; input mode: {mode} |

---

*Last Updated: {date}*
```

---

### Step 9b: Contribute to the Governance Spine (Append-if-Exists / Create-if-Absent)

The spine lives at `{project_root}/management_framework/` (sibling of `architecture/`). Detect by marker (`management_framework/MANAGEMENT_FRAMEWORK.md`):
- **If it exists** (typical — AI-PILC created it): append `ADLC-{ABBREV}-{TYPE}-{N}` entries to the 4 registers (Decision, Change, Issue, Lessons) and add the ADLC row to the index's Contributing Phases table. Non-destructive — never touch other phases' rows.
- **If absent** (ADLC originating): create it from `templates/management-framework.md` with project-qualified IDs.

Also update `pdlc-ws/projects/PROJECTS.md` (create-if-absent): set this project's `ADLC` column to `wip`/`done`, bump `Updated`. See `PROJECTS_REGISTRY_SPEC.md`.

---

### Step 10: Create State File

Create `{output_root}/adlc-state.md`:

```markdown
# AI-ADLC State — {system_name}

## Configuration

| Key | Value |
|-----|-------|
| System Name | {system_name} |
| Project ID | {project_id}  (adopted from PIP, or minted if ADLC originates) |
| Project Handle | PRJ-{ABBREV} |
| Project Root | {project_root}  (= pdlc-ws/projects/PRJ-{ABBREV}-{slug}/) |
| derivedFrom | {pip_ref or idea_ref} |
| Started | {timestamp} |
| Last Updated | {timestamp} |
| Workflow Depth | _[To be determined at Stage 2]_ |
| Output Structure | numbered |
| Output Root | {output_root}  (= {project_root}/architecture/) |
| Input Source | {path or mode} |
| Input Mode | {PIP / Document / Verbal / Brownfield} |
| Current Phase | FOUNDATION |
| Current Stage | 1 |
| Status | In Progress |

## Progress

| Stage # | Stage Name | Status | Completed | Notes |
|:-------:|------------|:------:|:---------:|-------|
| 1 | Workspace Detection | 🔄 Active | — | |
| 2 | Requirements Ingestion | ⏳ Pending | — | |
| 3 | Architecture Vision | ⏳ Pending | — | |
| 4 | System Context (C4 L1) | ⏳ Pending | — | |
| 5 | Container Design (C4 L2) | ⏳ Pending | — | |
| 6 | Technology Stack | ⏳ Pending | — | |
| 7 | Multi-Tenancy & Isolation | ⏳ Pending | — | Conditional |
| 8 | Security & Identity | ⏳ Pending | — | |
| 9 | Data Architecture | ⏳ Pending | — | |
| 10 | API Architecture | ⏳ Pending | — | |
| 11 | Integration & Infrastructure | ⏳ Pending | — | |
| 12 | Component Design (C4 L3) | ⏳ Pending | — | |
| 13 | Package Assembly | ⏳ Pending | — | |

## ADR Register

| ADR # | Title | Stage | Status | Decision Summary |
|:-----:|-------|:-----:|:------:|-----------------|
| — | _None yet_ | — | — | — |

## Architecture Principles

_To be defined in Stage 3._

## Key Constraints

_To be defined in Stage 3._

## Containers

_To be defined in Stage 5._

## Open Questions

_None yet._

## Dashboard Summary (machine-readable — AI-DFE reads this)

<!-- Roll-up for the dashboard `arch` pane (Architect tab). Emit this block into adlc-state.md; AI-DFE reads it when present, else extracts/zeros. Keep current at Assembly. -->
~~~yaml
dashboard-summary:
  vision: { status: "{draft | approved}", statement: "{one-line architecture vision}", optimisesFor: [] }
  c4Progress: { context: "{complete|in-progress|pending}", container: "{...}", component: "{...}", code: "{...}" }
  nfrs: {}            # keyed by name -> { defined: true, target: "{...}", priority: "{Critical|High|Medium|Low}" }
  techStack:          # grouped lists
    languages: []
    frameworks: []
    databases: []
    infrastructure: []
    messaging: []
    observability: []
~~~
```

---

### Step 11: Present Completion

Update state: Stage 1 = ✅ Done. Current Stage = 2.

Display:

```
✅ Stage 1: Workspace Detection — Complete

📋 System: {system_name}
📁 Output: {output_root}/ ({structure_type})
📐 ADR folder: Ready (template created)
📓 Architecture Workbook: Initialized
🔄 State tracking: Active
📄 Input detected: {what was found — mode}

Next → Stage 2: Requirements Ingestion
I'll now load and analyze your input to extract architecture-relevant requirements.

{If PIP detected:}
I found a Project Initiation Package. I'll load the Charter, Scope, NFRs, and constraints from it.

{If document detected:}
I found requirements document(s). I'll analyze them for architecture drivers.

{If nothing detected:}
No existing documents found. I'll interview you to establish the architecture context.

Proceeding...
```

---

## Error Handling

| Situation | Response |
|-----------|----------|
| User provides no system name | Use "Untitled System"; note "Rename at any time" |
| Folder creation fails | Inform user; suggest alternative path |
| PIP detected but incomplete | Load what exists; note gaps; supplement in Stage 2 |
| Multiple conflicting architectures found | Ask user which is current; archive others |
| User wants to skip setup | Use defaults (standard `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/architecture/`, numbered docs); project name still required |
| **Brownfield — existing flat layout found** | If existing architecture output sits in an older flat layout (root-level `adlc-state.md` / `{system}_Architecture/`), do NOT force-relocate. Offer a one-time, user-approved, non-destructive restructure into `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/architecture/`, or honor the existing path in place. Never renumber existing ADRs/entries. |

---

## Defaults (if user says "just use defaults")

| Setting | Default |
|---------|---------|
| Output structure | Numbered documents + ADR/ subfolder, inside `{project_root}/architecture/` |
| Output location | `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/architecture/` (adopts the detected project, or creates one) |
| System name | Must be provided (no default) |
