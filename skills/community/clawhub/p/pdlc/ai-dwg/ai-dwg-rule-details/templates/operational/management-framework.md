<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: generated
---
# Management Framework — Consolidated Spine Template (AI-DWG)

| Field | Value |
|-------|-------|
| **Package** | AI-DWG (AI-Driven Workspace Generator) |
| **Phase Code** | `DWG` |
| **Role** | Required producer — generates/appends the development-phase registers into the shared governance spine |
| **Registers Produced** | 4 (Decision, Change, Issue, Lessons) |
| **Contract Reference** | Management Framework Contract v1.2.0 + Multi-Project Output & State Contract v1.0.0 |

---

## Purpose

This template defines how AI-DWG contributes to the **shared governance spine** — the consolidated `management_framework/` folder that tracks project decisions, changes, issues, and lessons across the AI-* Family chain.

AI-DWG is typically the **third required producer** in the chain (after AI-PILC and AI-ADLC). In chain mode, the spine already exists — AI-DWG **appends** its development-phase registers. In standalone mode (or when run first), it **creates** the spine from scratch.

---

## Registers AI-DWG Does NOT Produce

| Register | Why Not |
|----------|---------|
| Action Items | Development actions are tracked in project tickets / sprint backlogs, not in the governance spine |
| Assumptions & Dependencies | By the time AI-DWG runs, assumptions are resolved in the Architecture Package — they are decisions, not open assumptions |

AI-DWG writes to the **4 universal registers** only.

---

## Behavior: Append-if-Exists / Create-if-Absent

```
1. DETECT the spine by marker:
   → Scan for management_framework/MANAGEMENT_FRAMEWORK.md
   → Multi-project default location: {project_root}/management_framework/,
     where {project_root} = pdlc-ws/projects/PRJ-{ABBREV}-{slug}/.
   → Detection path: user-provided path → {project_root}/management_framework/ →
     pdlc-ws/projects/*/management_framework/ →./management_framework/ → ask user.

2. IF marker found (spine exists — typical in chain mode):
   → APPEND DWG-phase entries to the 4 registers.
   → Use project-qualified ID prefix DWG-{ABBREV}-{TYPE}-{N} (e.g. DWG-MTA-D-1).
   → Add/update the DWG row in the index's "Contributing Phases" table.
   → DO NOT touch other phases' rows (additive, non-destructive).

3. IF marker NOT found (standalone — no predecessor has run):
   → CREATE management_framework/ at the project root ({project_root}/management_framework/).
   → Generate the index file (MANAGEMENT_FRAMEWORK.md) using the standard template.
   → Generate the 4 registers from the schemas below.
   → This package operates exactly as standalone (/).
```

**Mode 3 (Brownfield Overlay) note:** If a non-conforming `management_framework/` already exists (no marker, different schema), AI-DWG adds the marker + Phase column non-destructively. Existing entries are NOT renumbered — they are left in place and AI-DWG's new entries begin with `DWG-{ABBREV}-*` prefixes alongside them.

---

## ID Assignment Protocol (Numbering — OI-031)

Every entry ID uses the format `DWG-{ABBREV}-{TYPE}-{N}` where `{N}` is a sequential integer. To assign `{N}`:

```
1. READ the target register file (e.g. Decision_Log.md).
2. SCAN all existing rows for this phase+project prefix (DWG-{ABBREV}-{TYPE}-*).
3. FIND the highest {N} value currently present.
4. ASSIGN {N} = highest + 1 (or 1 if no existing entries for this prefix).
5. WRITE the new entry with the assigned ID.
```

**Concurrency model:** The AI-* Family operates in a single-user, single-agent model. The scan-and-increment protocol is safe because only one writer operates on a given register at a time. If future parallelism is introduced (multiple agents writing the same register concurrently), a reservation or locking mechanism would be required — that is explicitly deferred.

**Carry-forward continuity:** When a spine is carried forward into a dev workspace (DWG hinge), numbering continues from the last assigned `{N}` — never resets to 1. This is critical for DWG specifically: the planning-side spine may already have `PILC-MTA-D-1..5`, `ADLC-MTA-D-1..3`; DWG starts at `DWG-MTA-D-1` in the carried-forward copy and increments from there.

---

## Register Schemas (DWG Phase)

All schemas carry the **Phase** column per the contract. AI-DWG uses project-qualified prefix `DWG-{ABBREV}-`.

### Decision_Log.md
```markdown
<!-- AI-DWG generated | source: Project governance | date: {generation-date} -->
<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

# Decision Log

| ID | Phase | Date | Decision | Context / Options Considered | Rationale | Decision Maker | Impact | Status |
|----|-------|------|----------|------------------------------|-----------|----------------|--------|:------:|
| DWG-{ABBREV}-D-1 | DWG | {date} | {decision} | {context} | {rationale} | {maker} | {impact} | ✅ Final |
```

**When to log (DWG context):** Library choices, conditional steering-file inclusion/exclusion rationale, folder structure alternatives, mode selection (Mode 1/2/3), tech-stack-specific generation choices.

**NOT for:** Architecture decisions (those are ADRs in the AP) or project governance (those are in PILC's phase entries).

**Status values:** ✅ Final · ☐ Pending · 🔄 Under Review · ⏸️ Deferred · ❌ Reversed

---

### Change_Log.md
```markdown
<!-- AI-DWG generated | source: Project governance | date: {generation-date} -->
<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

# Change Log

| ID | Phase | Date Raised | Description | Raised By | Impact Assessment | Approval Status | Approved By | Date Approved | Implemented |
|----|-------|:-----------:|-------------|-----------|-------------------|:---------------:|-------------|:-------------:|:-----------:|
| DWG-{ABBREV}-C-1 | DWG | {date} | {description} | {role} | {steering-file/config impact} | ☐ Pending | _[TBD]_ | — | ☐ No |
```

**Status values:** ☐ Pending · 🔄 Under Assessment · ✅ Approved · ✅ Implemented · ❌ Rejected · ⏸️ Deferred

**Typical DWG changes:** Reconciliation decisions (accept/reject proposed steering updates), steering files added/removed post-generation, config merge overrides, depth-level adjustments.

---

### Issue_Log.md
```markdown
<!-- AI-DWG generated | source: Project governance | date: {generation-date} -->
<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

# Issue Log

| ID | Phase | Date Raised | Issue | Severity | Area | Owner | Status | Resolution | Resolved |
|----|-------|:-----------:|-------|:--------:|------|:-----:|:------:|-----------|:--------:|
| DWG-{ABBREV}-I-1 | DWG | {date} | {issue} | {H/M/L} | {area} | {owner} | ☐ Open | — | — |
```

**Status values:** ☐ Open · 🔄 Investigating · ✅ Resolved · ⏸️ On Hold · ❌ Escalated

**Typical DWG issues:** AP artifact missing (generation blocked), conflicting AP information, unknown technology (generic fallback needed), reconciliation conflict (AP-derived vs. team-customized content).

---

### Lessons_Learned.md
```markdown
<!-- AI-DWG generated | source: Project governance | date: {generation-date} -->
<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

# Lessons Learned

| ID | Phase | Date | Lesson | Context | Action Taken | Category |
|----|-------|------|--------|---------|--------------|----------|
| DWG-{ABBREV}-L-1 | DWG | {date} | {lesson} | {what happened} | {corrective action} | {Process/Technology/DX/Governance} |
```

**Category note:** AI-DWG adds "DX" (Developer Experience) as a category — this captures lessons about workspace ergonomics (e.g., "Generated 30 steering files but team only reads 5 — depth was too high for team size").

---

## Generation Rules

1. **ALWAYS generated** — every development workspace gets these registers (either in a new spine or appended to the existing one).
2. Registers start with headers + one example row (populated during development).
3. Entries are append-only — never delete logged items.
4. Each entry is sequentially numbered per the ID Assignment Protocol above.
5. AI-DLC v1 sessions should log decisions and lessons as they arise (using their own phase code if/when AI-DLC v1 contributes to the spine).
6. Sprint retros feed into `Lessons_Learned.md`.

---

## When AI-DWG Records (Mapping to Generation Steps)

| DWG Step | Registers Typically Touched | Example Entry |
|:--------:|---------------------------|---------------|
| Mode Detection | Decisions | `DWG-MTA-D-1: Mode 1 selected (greenfield — no existing workspace)` |
| Configuration Questions | Decisions | `DWG-MTA-D-2: Autonomy mode = Autopilot` |
| AP Reading | Issues | `DWG-MTA-I-1: Multi-tenancy doc missing — single-tenant assumed` |
| Conditional Triggers | Decisions | `DWG-MTA-D-3: resilience-standards.md generated (>3 integrations)` |
| Validation | Issues | `DWG-MTA-I-2: AP principle P4 not encoded in any steering file` |
| Reconciliation (Mode 2) | Changes, Decisions | `DWG-MTA-C-1: api-standards.md updated — new versioning strategy from ADR-012` |
| Brownfield (Mode 3) | Decisions, Lessons | `DWG-MTA-L-1: Existing.gitignore had 200+ entries — merge took manual review` |

---

## Relationship to Other Packages (Development Workspace Context)

> **Scope:** This section documents only the packages that **operate within this development workspace** — i.e., the packages that produce, enforce, or consume governance data here. Planning-phase packages (AI-ILC, AI-PILC, AI-POLC, AI-UXD, AI-PPM, AI-FLO) ran in the planning workspace *before* this workspace was generated — their contributions are already baked into the steering files and architecture. They do NOT append to this spine at runtime.

| Package | Phase Code | Registers | Primary Governance Mechanism |
|---------|:----------:|:---------:|------------------------------|
| **AI-DWG** | **`DWG`** | **Decision, Change, Issue, Lessons** | **Spine (workspace-generation governance)** |
| AI-GCE | `GCE` | Decision, Lessons | Spine (compliance decisions) + `.governance/compliance-log/` |
| AI-TGE | `TGE` | Decision, Lessons | Spine (test-governance decisions) + `.tge/` |
| AI-DLC v1 | `DLC` | Decision, Change, Issue, Lessons, Action | Spine (development-phase governance) |

> Planning-phase contributions (from AI-PILC, AI-ADLC, AI-POLC, AI-UXD) are captured as **source provenance** in the steering files' front-matter (`source:` field) — not as active spine participants. If the architecture or product backlog changes, the planning workspace runs AI-DWG reconciliation (Mode 2) to propagate updates here.

---

## Standalone vs. Chain Behavior (Summary)

| Mode | What Happens |
|------|-------------|
| **Standalone** (no predecessor has run) | AI-DWG creates the spine from scratch with 4 registers + index. Self-contained. |
| **Chain** (spine exists from prior planning) | AI-DWG appends `DWG-{ABBREV}-*` entries. One consolidated record. The spine may carry entries from the planning phase (PILC/ADLC/POLC/UXD prefixes) — these are historical provenance, not active participants in this workspace. |
| **Brownfield** (existing non-conforming `management_framework/`) | Add marker + Phase columns non-destructively; do not renumber existing entries. |

---

## Contributing Phases Row (for the Index)

When AI-DWG appends to an existing spine, it adds this row to `MANAGEMENT_FRAMEWORK.md`:

```markdown
| DWG | AI-DWG | {date} | Decision, Change, Issue, Lessons |
```

---

*Template Version: 1.1.0 | Contract: MANAGEMENT_FRAMEWORK_CONTRACT.md v1.2.0 + OUTPUT_AND_STATE_CONTRACT.md v1.0.0 | Package: AI-DWG | Phase code: DWG | IDs: project-qualified DWG-{ABBREV}-{TYPE}-{N}*
