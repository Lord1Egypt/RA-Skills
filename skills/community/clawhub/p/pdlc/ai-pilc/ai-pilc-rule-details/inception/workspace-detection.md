<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Workspace Detection

## Stage: 1 of 16
## Phase: 🔵 INCEPTION
## Execution: ALWAYS

---

## Purpose

Detect whether this is a fresh start or a resumed workflow, configure the output environment, and establish the management framework. This stage produces no project deliverable — it sets up the workspace for everything that follows.

---

## Depth Adaptation

N/A — This stage is depth-independent. Workspace setup is identical regardless of project complexity. Depth level is determined at Stage 2 (Source Document Ingestion) after assessing the source material.

---

## Step-by-Step Execution

### Step 1: Check for Existing State

1. Scan the workspace for `pilc-state.md` in these locations (in order):
   - `pdlc-ws/projects/*/pip/pilc-state.md` (**default multi-project layout** — see Step 5)
   - `./pilc-state.md`
   - `./pilc-docs/pilc-state.md`
   - `./{numbered_folder_root}/pilc-state.md`
   - Any directory the user has specified as output root
2. **If one or more projects are found (multi-project active-project selection):**
   - Read `pdlc-ws/projects/PROJECTS.md` (the registry, if present) → identify the ★ active project.
   - Prompt the user:
     ```
     This workspace already has these projects:
       ★ {active Project ID} — {folder}   (active)
         {other Project ID} — {folder}
     Work on the active project, start initiation for a different existing project, or create a NEW project? [active / pick / new]
     ```
   - On `active`/`pick` → load that project's `pilc-state.md` and follow the **Session Resumption Flow** (`common/session-continuity.md`).
   - On `new` → proceed to Step 1b (origination of a new project).
3. If a single `pilc-state.md` is found → load state and follow **Session Resumption Flow**.
4. If NONE found → proceed to Step 1b (predecessor detection + origination).

> **Active-project rule (`OUTPUT_AND_STATE_CONTRACT.md` §8):** exactly one project is ★ active at a time. AI-PILC operates on the chosen project and, if it switches the active project, updates the ★ pointer in `pdlc-ws/projects/PROJECTS.md`.

---

### Step 1b: Detect AI-ILC Predecessor (Chain Awareness)

Scan for the AI-ILC predecessor marker `ilc-state.md` in common locations:
- `./ilc-state.md`
- `../ilc-state.md` (sibling folder)
- Any directory the user has specified

**If `ilc-state.md` found:**
1. Read the `Route` field — confirm it targets `project` (or a value that resolves to AI-PILC)
2. Read the `Status` field — confirm it shows "Approved" or "Complete"
3. If both confirm → flag for Mode E intake at Stage 2: "AI-ILC brief detected. Stage 2 will offer the AI-ILC Brief intake mode."
4. Store in session context: `predecessor_detected: AI-ILC`, `ilc_state_path: {path}`
5. Proceed to Step 2

**If NOT found → proceed to Step 2** (normal — AI-ILC is optional; its absence is the default path)

> **OR-input (optional predecessor):** AI-ILC is an optional pre-stage. AI-PILC works identically without it. Detection is informational — it enriches Stage 2's intake options but doesn't change workspace setup.

---

### Step 2: Collect Project Identity

Ask the user:

```markdown
### Q-CFG-01: Project Name

**Context:** This name will appear in all deliverables, the state file, and folder structure.

**Your input:** What is the name of this project or initiative?

**Format expected:** Short title (e.g., "CRM Platform Upgrade", "Digital Transformation Programme", "Cloud Migration")

**Note:** This can be changed later — it's not a binding decision.
```

Wait for response. Store as `{project_name}`.

---

### Step 2a: Mint the Project ID (Correlation Key)

The **Project ID** is the unique key that threads this project through the entire AI-* Family — it is the value AI-FLO routes on and AI-PPM aggregates portfolio roll-ups against. It MUST be minted now (Stage 1), not deferred to the Charter, and once set it is **immutable** (the Charter later confirms it, never regenerates it).

1. Auto-generate a candidate using the format: `PRJ-{ABBREV}-{YYYY}-{NNN}`
   - `{ABBREV}` — 3–5 uppercase letters derived from the project name (e.g., "CRM Platform Upgrade" → `CRM`)
   - `{YYYY}` — current year
   - `{NNN}` — sequence, default `001` in standalone mode
2. Confirm with the user:

```markdown
### Q-CFG-01b: Project ID

**Context:** This is the project's unique identifier — the correlation key used across every package in the AI-* Family (routing, portfolio roll-up, cross-document consistency). It is set once and never changes.

**Proposed ID:** `{generated_project_id}`

**Options:**
- (a) Accept the proposed ID
- (b) Provide your own ID (e.g., an existing PMO/portfolio code)

**Recommended:** Option (a)
**Rationale:** The generated ID follows the family convention `PRJ-{ABBREV}-{YEAR}-{NNN}` and is guaranteed unique within a standalone run.

**Note:** If this project is governed by AI-PPM (portfolio), the portfolio may assign or reconcile the `{NNN}` sequence to guarantee uniqueness across the whole portfolio.

**Your Decision:** _[awaiting input]_
```

Wait for response. Store as `{project_id}`.

3. **Idea lineage (derivedFrom):** Record the originating idea reference for traceability (per `contracts/TRACEABILITY_CONTRACT.md`):

   - **If `ilc-state.md` was detected (Mode D intake):** `derivedFrom` is **REQUIRED** — auto-populate from the idea ID found in `ilc-state.md`. Do NOT ask the user; the value is already known.
   - **If standalone (no `ilc-state.md`):** Ask the user:

```markdown
### Q-CFG-01c: Originating Idea (Optional)

**Context:** If this project came from an approved idea (AI-ILC), recording the idea reference preserves the idea → project → portfolio lineage (Traceability Contract §4-A).

**Your input:** Idea ID / brief reference, or "none".
```

Store as `{idea_ref}` (default: `none` for standalone; auto-populated for ILC intake).

The Project ID and idea lineage are recorded as Decision `D-002` when the Decision Log is created (Step 6).

---

### Step 3: Apply Output Structure (Numbered — Always)

The deliverable sub-structure inside `pip/` is always **numbered**. This is not a user choice — do not ask. Record `Output Structure: numbered` in state and proceed.

Store in session context: `output_structure: numbered`

---

### Step 4: Configure Output Location

Derive the **project handle** and **slug** for the folder name:
- `{ABBREV}` — reuse the abbreviation from the Project ID minted in Step 2a (e.g. `PRJ-CRM-2026-001` → `CRM`).
- `{slug}` — the project name lower-cased, spaces → hyphens, punctuation stripped (e.g. "CRM Platform Upgrade" → `crm-platform-upgrade`).

The output location is **fixed** — `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/` with PILC deliverables in `pip/`. There is no user choice for the project folder path. This aligns with `OUTPUT_AND_STATE_CONTRACT.md` §3 (the Always-On Rule — `projects/` structure is mandatory in all conditions).

- Set `{project_root}` = `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/`.
- Set `{output_root}` = `{project_root}/pip/` — PILC's own deliverables + `pilc-state.md` live here.
- The governance spine lives at `{project_root}/management_framework/` (a sibling of `pip/`, shared across packages — Step 6).

> **Brownfield exception:** if the workspace already contains PILC output in an older flat layout, detect it on first run and inform the user: "Existing PILC output found at `{path}`. AI-PILC now uses `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/pip/` as the standard location. I'll operate in the standard location — you may migrate existing artifacts at your convenience." Never force-move existing files.

---

### Step 5: Create Folder Structure

Create the project folder, PILC's `pip/` output folder, and the project-root spine. The numbered deliverable sub-structure lives **inside `pip/`**; the `management_framework/` spine is a **sibling of `pip/`** at the project root (shared across packages).

**Standard layout — numbered deliverables (always):**

```
pdlc-ws/projects/
├── PROJECTS.md                          ← registry (Step 6b)
└── PRJ-{ABBREV}-{slug}/                  ← {project_root}
    ├── management_framework/             ← governance spine (project root, shared)
    └── pip/                              ← {output_root} — AI-PILC deliverables
        ├── pilc-state.md                 ← marker
        ├── 01_Requirement_Submission/
        ├── 02_Screening_Prioritization/
        ├── 03_Business_Case/
        ├── 04_Project_Charter/
        ├── 05_Stakeholder_Management/
        ├── 06_Scope_Planning/
        ├── 07_Resource_Budget/
        ├── 08_Risk_Management/
        ├── 09_Governance_Communication/
        └── 10_Project_Kickoff/
```

> **Why the spine is one level up from `pip/`:** the spine is the *shared* per-project governance record that ADLC/UXD/POLC also append to. It belongs to the **project**, not to PILC, so it sits at the project root beside the other packages' output folders (`architecture/`, `ux/`, `backlog/`).

---

### Step 6: Create the Governance Spine (Create-if-Absent)

The spine lives at `{project_root}/management_framework/` (sibling of `pip/`). Detect it by marker first (`management_framework/MANAGEMENT_FRAMEWORK.md`) — **append-if-exists, create-if-absent** per `MANAGEMENT_FRAMEWORK_CONTRACT.md` v1.2.0 and `templates/management-framework.md`.

If absent, create the index marker + the six registers using templates from `templates/`:

1. `{project_root}/management_framework/MANAGEMENT_FRAMEWORK.md` — index/marker
2. `…/Decision_Log.md` · `…/Change_Log.md` · `…/Issue_Log.md` · `…/Action_Items.md` · `…/Assumptions_Dependencies.md` · `…/Lessons_Learned.md`

**IDs are project-qualified** — `PILC-{ABBREV}-{TYPE}-{N}` (e.g. `PILC-CRM-D-1`) so they never collide across projects in one workspace.

**Populate with initial entries:**
- Decision Log → `PILC-{ABBREV}-D-1`: "Output structure: numbered (standard). Project name: {project_name}."
- Decision Log → `PILC-{ABBREV}-D-2`: "Project ID assigned: {project_id}. Originating idea: {idea_ref}."
- Assumptions → `PILC-{ABBREV}-AD-1`: "Source requirement document is available and represents stakeholder intent."

---

### Step 6b: Create / Update the Projects Registry (Create-if-Absent)

Maintain `pdlc-ws/projects/PROJECTS.md` per `PROJECTS_REGISTRY_SPEC.md` (shared, create-if-absent):

1. If `pdlc-ws/projects/PROJECTS.md` is absent → create it from `templates/projects-registry.md`, add this project's row, and set it ★ active.
2. If present → append this project's row (if missing); set `PILC = wip`/`done` in this project's row only; bump `Updated`. If the user chose to make this the active project, move the ★ pointer here (clearing the previous ★).
3. Never edit another project's row.

---

### Step 7: Create State File

Create `{output_root}/pilc-state.md` with initial content:

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
| Started | {current_timestamp} |
| Last Updated | {current_timestamp} |
| Workflow Depth | _[To be determined at Stage 2]_ |
| Output Structure | numbered |
| Output Root | {output_root}  (= {project_root}/pip/) |
| Source Document | _[To be provided at Stage 2]_ |
| Current Phase | INCEPTION |
| Current Stage | 1 |
| Status | In Progress |

## Progress

| Stage # | Stage Name | Status | Completed | Notes |
|:-------:|------------|:------:|:---------:|-------|
| 1 | Workspace Detection | 🔄 Active | — | Setting up |
| 2 | Source Document Ingestion | ⏳ Pending | — | |
| 3 | Requirement Structuring | ⏳ Pending | — | |
| 4 | Requirements Analysis | ⏳ Pending | — | |
| 5 | Clarification Cycle | ⏳ Pending | — | Conditional |
| 6 | Feasibility Assessment | ⏳ Pending | — | |
| 7 | Prioritization | ⏳ Pending | — | |
| 8 | Business Case Development | ⏳ Pending | — | |
| 9 | Project Charter | ⏳ Pending | — | |
| 10 | Stakeholder Management | ⏳ Pending | — | |
| 11 | Scope Definition | ⏳ Pending | — | |
| 12 | Resource & Budget Planning | ⏳ Pending | — | |
| 13 | Risk Management | ⏳ Pending | — | |
| 14 | Governance & Communication | ⏳ Pending | — | |
| 15 | Kickoff Preparation | ⏳ Pending | — | |
| 16 | Package Assembly | ⏳ Pending | — | |

## Decisions Made

| Decision ID | Stage | Summary |
|:-----------:|:-----:|---------|
| PILC-{ABBREV}-D-1 | 1 | Output structure: numbered. Project: {project_name}. |
| PILC-{ABBREV}-D-2 | 1 | Project ID assigned: {project_id}. Originating idea: {idea_ref}. |

## Open Items

_None yet._

## Register Counts

| Register | Entries |
|----------|:-------:|
| Decisions | 2 |
| Changes | 0 |
| Issues | 0 |
| Actions | 0 |
| Assumptions | 1 |
| Lessons | 0 |
```

---

### Step 8: Present Completion

Update state: Stage 1 = ✅ Done. Current Stage = 2.

Display:

```
✅ Stage 1: Workspace Detection — Complete

📋 Project: {project_name}
🆔 Project ID: {project_id}
📁 Project root: {project_root}  (deliverables in pip/, spine at management_framework/)
🗂  Registry: pdlc-ws/projects/PROJECTS.md  (this project set ★ active)
📊 Management registers: 6 created
🔄 State tracking: Active

Next → Stage 2: Source Document Ingestion
I need your source requirement document to continue.

How would you like to provide it?
  (a) File path in this workspace
  (b) Paste the content here
  (c) Describe your project idea verbally

Which works for you?
```

---

## Automatic Proceed

This stage auto-proceeds to Stage 2 after user provides their source preference. There is no separate gate between Stage 1 and Stage 2 — the completion message naturally transitions into Stage 2's intake.

---

## Error Handling

| Situation | Response |
|-----------|----------|
| User provides no project name | Use "Untitled Project" and note: "You can rename at any time" |
| Folder creation fails (permissions) | Inform user; suggest alternative path; do NOT proceed without a writable output location |
| State file already exists but user says "fresh start" | Archive existing: rename to `pilc-state-{timestamp}.archived.md`; create new |
| User wants to skip setup questions | Use defaults (standard `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/` layout, numbered deliverables); log as decision |
| **Brownfield — existing flat layout found** | If a pre-existing flat `{name}-pip/` or root-level `pilc-state.md` is detected (older single-project layout), do NOT force-relocate. Inform the user: "Existing PILC output found at `{path}`. AI-PILC now uses `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/pip/` as the standard location. I'll operate in the standard location — you may migrate existing artifacts at your convenience." Offer a **one-time, user-approved, non-destructive** restructure into `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/` if the user wants. Never renumber existing human entries. |

---

## Configuration Defaults

If user says "just use defaults" or "skip setup":

| Setting | Default Value |
|---------|---------------|
| Output structure | Standard `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/` layout — deliverables in `pip/` (numbered), spine at the project root |
| Output location | `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/` (project root); PILC deliverables under `pip/` |
| Project name | Must still be provided (no default) |
| Project ID | Auto-generated `PRJ-{ABBREV}-{YEAR}-001` from project name; user may override |
| Originating idea | `none` |

> **Note:** The numbered folder structure is always used — there is no flat-folder option. This is a fixed convention, not a user-configurable setting.
