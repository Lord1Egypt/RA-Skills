<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Management Framework — Consolidated Spine Template (AI-PILC)

| Field | Value |
|-------|-------|
| **Package** | AI-PILC (Project Initiation Life Cycle) |
| **Phase Code** | `PILC` |
| **Role** | Required producer — first chain package to create-or-append the spine |
| **Registers Produced** | 6 (Decision, Change, Issue, Action, Assumptions, Lessons) |
| **Contract Reference** | Management Framework Contract v1.2.0 + Multi-Project Output & State Contract v1.0.0 |

---

## Purpose

This template defines how AI-PILC produces the **shared governance spine** — the consolidated `management_framework/` folder that tracks all project decisions, changes, issues, actions, assumptions, and lessons across the AI-* Family chain.

AI-PILC is typically the **first package** in the chain to run, so in most chains it will **create** the spine (marker absent). In edge cases (e.g., AI-ILC seeded it first, or the user runs out of order), it **appends** to an existing spine.

---

## Behavior: Append-if-Exists / Create-if-Absent

```
1. DETECT the spine by marker:
   → Scan for management_framework/MANAGEMENT_FRAMEWORK.md
   → Multi-project default location: {project_root}/management_framework/ (sibling of pip/),
     where {project_root} = pdlc-ws/projects/PRJ-{ABBREV}-{slug}/.
   → Detection path: user-provided path → {project_root}/management_framework/ →
     pdlc-ws/projects/*/management_framework/ → ./management_framework/ → ask user.

2. IF marker found (spine exists):
   → APPEND PILC-phase entries to the existing registers.
   → Use project-qualified ID prefix PILC-{ABBREV}-{TYPE}-{N} (e.g. PILC-CRM-D-1).
   → Add/update the PILC row in the index's "Contributing Phases" table.
   → DO NOT touch other phases' rows (additive, non-destructive).

3. IF marker NOT found (no spine):
   → CREATE management_framework/ at the project root ({project_root}/management_framework/).
   → Generate the index file (MANAGEMENT_FRAMEWORK.md) from the template below.
   → Generate all 6 registers from the schemas below.
   → This package operates exactly as standalone (self-contained spine, one consolidated record).
```

---

## ID Assignment Protocol (Numbering — OI-031)

Every entry ID uses the format `PILC-{ABBREV}-{TYPE}-{N}` where `{N}` is a sequential integer. To assign `{N}`:

```
1. READ the target register file (e.g. Decision_Log.md).
2. SCAN all existing rows for this phase+project prefix (PILC-{ABBREV}-{TYPE}-*).
3. FIND the highest {N} value currently present.
4. ASSIGN {N} = highest + 1 (or 1 if no existing entries for this prefix).
5. WRITE the new entry with the assigned ID.
```

**Concurrency model:** The AI-* Family operates in a single-user, single-agent model. The scan-and-increment protocol is safe because only one writer operates on a given register at a time. If future parallelism is introduced (multiple agents writing the same register concurrently), a reservation or locking mechanism would be required — that is explicitly deferred.

**Carry-forward continuity:** When a spine is carried forward into a dev workspace (DWG hinge), numbering continues from the last assigned `{N}` — never resets to 1.

---

## Index File Template (Marker)

> This is `management_framework/MANAGEMENT_FRAMEWORK.md` — the marker AND human entry point.

```markdown
<!-- Shared governance spine | contract v1.2.0 -->

# Management Framework

Consolidated governance spine for **{project_name}** (Project ID: `{project_id}`).
Each phase of the AI-* chain appends its decisions, changes, issues, and lessons here, tagged by phase.

## Registers
| Register | Purpose |
|----------|---------|
| Decision_Log.md | Decisions below formal-artifact threshold |
| Change_Log.md | Scope / approach / timeline changes |
| Issue_Log.md | Blockers and problems |
| Lessons_Learned.md | Insights to carry forward |
| Action_Items.md | Tracked follow-ups |
| Assumptions_Dependencies.md | Assumptions & dependencies |

## Contributing Phases
| Phase | Package | First Contributed | Registers Touched |
|-------|---------|-------------------|-------------------|
| PILC | AI-PILC | {date} | Decision, Change, Issue, Action, Assumptions, Lessons |

## Conventions
- Entry IDs are project-qualified, phase-prefixed: `{PHASE}-{ABBREV}-{TYPE}-{N}`.
- Entries are append-only — never edit or delete another phase's rows.
- Filter by the Phase column to view a single phase's governance.
- Detection by marker: this file's presence means "a consolidated spine exists here."
```

---

## Register Schemas (PILC Phase)

All schemas carry the **Phase** column per the contract. AI-PILC uses prefix `PILC-`.

### Decision_Log.md
```markdown
# Decision Log

<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

| ID | Phase | Date | Decision | Context / Options Considered | Rationale | Decision Maker | Impact | Status |
|----|-------|------|----------|------------------------------|-----------|----------------|--------|:------:|
| PILC-{ABBREV}-D-1 | PILC | {date} | {decision} | {context} | {rationale} | {maker} | {impact} | ✅ Final |
```

**Status values:** ✅ Final · ☐ Pending · 🔄 Under Review · ⏸️ Deferred · ❌ Reversed

**Governance rules:**
1. All decisions with scope, budget, or timeline impact MUST be recorded.
2. Numbered sequentially per the ID Assignment Protocol above, project-qualified (`PILC-{ABBREV}-D-1`, `PILC-{ABBREV}-D-2`, ...).
3. Entries never deleted — only status-updated.
4. Architecture decisions that warrant an ADR → recorded in `ADR/` (AI-ADLC), NOT here.

---

### Change_Log.md
```markdown
# Change Log

<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

| ID | Phase | Date Raised | Description | Raised By | Impact Assessment | Approval Status | Approved By | Date Approved | Implemented |
|----|-------|:-----------:|-------------|-----------|-------------------|:---------------:|-------------|:-------------:|:-----------:|
| PILC-{ABBREV}-C-1 | PILC | {date} | {description} | {name} | {scope/schedule/budget impact} | ☐ Pending | _[TBD]_ | — | ☐ No |
```

**Status values:** ☐ Pending · 🔄 Under Assessment · ✅ Approved · ✅ Implemented · ❌ Rejected · ⏸️ Deferred

**Change control process:** Raise → Assess (PM + Tech Lead) → Approve (per governance matrix) → Implement → Communicate.

---

### Issue_Log.md
```markdown
# Issue Log

<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

| ID | Phase | Date Raised | Issue | Severity | Area | Owner | Status | Resolution | Resolved |
|----|-------|:-----------:|-------|:--------:|------|:-----:|:------:|-----------|:--------:|
| PILC-{ABBREV}-I-1 | PILC | {date} | {issue} | {H/M/L} | {area} | {owner} | ☐ Open | — | — |
```

**Status values:** ☐ Open · 🔄 Investigating · ✅ Resolved · ⏸️ On Hold · ❌ Escalated

---

### Action_Items.md
```markdown
# Action Items

<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

| ID | Phase | Date Raised | Description | Owner | Due Date | Priority | Source | Status |
|----|-------|:-----------:|-------------|:-----:|:--------:|:--------:|--------|:------:|
| PILC-{ABBREV}-A-1 | PILC | {date} | {action} | {role} | {due} | {H/M/L} | {meeting/stage/review} | ☐ Open |
```

**Status values:** ☐ Open · 🔄 In Progress · ✅ Complete · ❌ Cancelled · ⏸️ On Hold

**Priority:** High (before next gate) · Medium (within 2 weeks) · Low (when convenient).

---

### Assumptions_Dependencies.md
```markdown
# Assumptions & Dependencies

<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

| ID | Phase | Date | Assumption / Dependency | Type | Impact if Invalid | Owner | Status |
|----|-------|------|-------------------------|:----:|-------------------|:-----:|:------:|
| PILC-{ABBREV}-AD-1 | PILC | {date} | {statement} | {A/D} | {impact} | {owner} | ☐ Open |
```

**Type:** A = Assumption · D = Dependency
**Status values:** ☐ Open · ✅ Validated · ❌ Invalid · ⏸️ Under Review

---

### Lessons_Learned.md
```markdown
# Lessons Learned

<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

| ID | Phase | Date | Lesson | Context | Action Taken | Category |
|----|-------|------|--------|---------|--------------|----------|
| PILC-{ABBREV}-L-1 | PILC | {date} | {lesson} | {what happened} | {corrective action} | {Process/People/Technology/Governance} |
```

---

## When AI-PILC Records (Mapping to Stages)

> Example IDs below omit the project handle for brevity; actual IDs are project-qualified `PILC-{ABBREV}-{TYPE}-{N}` (e.g. `PILC-CRM-D-1`).

| PILC Stage | Registers Typically Touched | Example Entry |
|:----------:|---------------------------|---------------|
| 2 (Requirement Structuring) | Assumptions | `PILC-AD-001: Assume internal API available` |
| 4 (Requirements Analysis) | Decisions, Actions | `PILC-D-001: Adopt phased delivery over big-bang` |
| 5 (Feasibility) | Issues, Assumptions | `PILC-I-001: Legal review pending` |
| 6 (Prioritization) | Decisions | `PILC-D-002: Priority = Build (over Buy)` |
| 7 (Clarification) | Changes | `PILC-C-001: Scope reduced from 5 to 3 modules` |
| 8 (Business Case) | Decisions, Lessons | `PILC-D-003: Cost ceiling set at £150K` |
| 9 (Charter) | Decisions | `PILC-D-004: Charter approved by Sponsor` |
| 10-14 (Planning) | Actions, Issues, Assumptions | `PILC-A-001: Confirm vendor availability by Sprint 0` |
| 15-16 (Mobilization) | Lessons | `PILC-L-001: Kick-off attendance was 60% — invite earlier` |

---

## Standalone vs. Chain Behavior (Summary)

| Mode | What Happens |
|------|-------------|
| **Standalone** (no predecessor has run) | AI-PILC creates the spine from scratch. Self-contained output. |
| **Chain** (spine already exists from AI-ILC or manual seeding) | AI-PILC appends `PILC-*` entries. One consolidated record. |

---

## Relationship to Individual Register Templates

The 6 individual register files (`templates/decision-log.md`, `templates/change-log.md`, etc.) remain as **standalone reference templates**. They are:
- Used when a user wants a single register outside the spine context.
- Compatible with the spine schema (same columns minus Phase — Phase is added when writing to the consolidated spine).
- NOT deprecated by this file.

This file is the **spine-aware master** — it governs how registers are created/appended in the consolidated spine, with the Phase column and phase-prefixed IDs.

---

*Template Version: 1.2.0 | Contract: MANAGEMENT_FRAMEWORK_CONTRACT.md v1.3.0 + OUTPUT_AND_STATE_CONTRACT.md v1.0.0 | Package: AI-PILC | Phase code: PILC | IDs: project-qualified PILC-{ABBREV}-{TYPE}-{N}*
