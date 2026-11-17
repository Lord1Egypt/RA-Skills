<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Management Framework — Consolidated Spine Template (AI-ADLC)

| Field | Value |
|-------|-------|
| **Package** | AI-ADLC (Architecture Design Life Cycle) |
| **Phase Code** | `ADLC` |
| **Role** | Required producer — second chain package to append (after AI-PILC typically creates the spine) |
| **Registers Produced** | 4 (Decision, Change, Issue, Lessons) |
| **Contract Reference** | Management Framework Contract v1.2.0 + Multi-Project Output & State Contract v1.0.0 |

---

## Purpose

This template defines how AI-ADLC contributes to the **shared governance spine** — the consolidated `management_framework/` folder that tracks project decisions, changes, issues, and lessons across the AI-* Family chain.

AI-ADLC is typically the **second required producer** — the spine already exists from AI-PILC, so the default path is **append**. If the user runs AI-ADLC standalone (no predecessor), it creates the spine from scratch.

---

## Registers AI-ADLC Does NOT Produce

| Register | Why Not |
|----------|---------|
| Action Items | The Architecture Workbook tracks outstanding items; duplicating in Actions would split ownership |
| Assumptions & Dependencies | Assumptions are resolved during the Architecture Vision stage — by the time ADLC writes to the spine, they are decisions, not open assumptions |

AI-ADLC writes to the **4 universal registers** only.

---

## Boundary: Decision_Log vs. ADR

This is the most important distinction for ADLC governance:

| Record Type | Goes In | Examples |
|-------------|---------|----------|
| **Architecture Decision Record** | `ADR/ADR-{NNN}.md` (within the Architecture Package) | Technology choice, pattern selection, API style, data model approach |
| **Sub-threshold decision** | `management_framework/Decision_Log.md` | "Use numbered output structure", "Defer multi-tenancy to Phase 2", "Include brownfield ADR" |

**Rule:** If a decision has *architectural significance* (affects system structure, quality attributes, or technology) → it is an **ADR**. If it is a *process/workflow/scope* decision during architecture design → it goes in the **Decision_Log** with an `ADLC-D-*` prefix.

The two records are complementary, not competing. ADRs are formal architecture artifacts (published in the AP); the Decision_Log captures the process trail around them.

---

## Behavior: Append-if-Exists / Create-if-Absent

```
1. DETECT the spine by marker:
   → Scan for management_framework/MANAGEMENT_FRAMEWORK.md
   → Multi-project default location: {project_root}/management_framework/ (sibling of architecture/),
     where {project_root} = pdlc-ws/projects/PRJ-{ABBREV}-{slug}/.
   → Detection path: user-provided path → {project_root}/management_framework/ →
     pdlc-ws/projects/*/management_framework/ → predecessor (pip/) project root → ask user.

2. IF marker found (spine exists — typical in chain mode):
   → APPEND ADLC-phase entries to the 4 registers.
   → Use project-qualified ID prefix ADLC-{ABBREV}-{TYPE}-{N} (e.g. ADLC-XYZ-D-1).
   → Add/update the ADLC row in the index's "Contributing Phases" table.
   → DO NOT touch other phases' rows (additive, non-destructive).

3. IF marker NOT found (standalone — no predecessor has run):
   → CREATE management_framework/ at the project root ({project_root}/management_framework/).
   → Generate the index file (MANAGEMENT_FRAMEWORK.md) using the standard template.
   → Generate the 4 registers from the schemas below.
   → This package operates exactly as standalone (/).
```

---

## ID Assignment Protocol (Numbering — OI-031)

Every entry ID uses the format `ADLC-{ABBREV}-{TYPE}-{N}` where `{N}` is a sequential integer. To assign `{N}`:

```
1. READ the target register file (e.g. Decision_Log.md).
2. SCAN all existing rows for this phase+project prefix (ADLC-{ABBREV}-{TYPE}-*).
3. FIND the highest {N} value currently present.
4. ASSIGN {N} = highest + 1 (or 1 if no existing entries for this prefix).
5. WRITE the new entry with the assigned ID.
```

**Concurrency model:** The AI-* Family operates in a single-user, single-agent model. The scan-and-increment protocol is safe because only one writer operates on a given register at a time. If future parallelism is introduced (multiple agents writing the same register concurrently), a reservation or locking mechanism would be required — that is explicitly deferred.

**Carry-forward continuity:** When a spine is carried forward into a dev workspace (DWG hinge), numbering continues from the last assigned `{N}` — never resets to 1.

---

## Register Schemas (ADLC Phase)

All schemas carry the **Phase** column per the contract. AI-ADLC uses prefix `ADLC-`.

### Decision_Log.md
```markdown
# Decision Log

<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

| ID | Phase | Date | Decision | Context / Options Considered | Rationale | Decision Maker | Impact | Status |
|----|-------|------|----------|------------------------------|-----------|----------------|--------|:------:|
| ADLC-{ABBREV}-D-1 | ADLC | {date} | {decision} | {context} | {rationale} | {maker} | {impact} | ✅ Final |
```

**Status values:** ✅ Final · ☐ Pending · 🔄 Under Review · ⏸️ Deferred · ❌ Reversed

**Governance rules:**
1. Only sub-threshold decisions here (see ADR boundary above).
2. Numbered sequentially per the ID Assignment Protocol above, project-qualified (`ADLC-{ABBREV}-D-1`, `ADLC-{ABBREV}-D-2`,...).
3. Entries never deleted — only status-updated.
4. If a Decision_Log entry escalates to architectural significance → migrate to ADR (log a Change entry referencing the move).

---

### Change_Log.md
```markdown
# Change Log

<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

| ID | Phase | Date Raised | Description | Raised By | Impact Assessment | Approval Status | Approved By | Date Approved | Implemented |
|----|-------|:-----------:|-------------|-----------|-------------------|:---------------:|-------------|:-------------:|:-----------:|
| ADLC-{ABBREV}-C-1 | ADLC | {date} | {description} | {role} | {scope/design/timeline impact} | ☐ Pending | _[TBD]_ | — | ☐ No |
```

**Status values:** ☐ Pending · 🔄 Under Assessment · ✅ Approved · ✅ Implemented · ❌ Rejected · ⏸️ Deferred

**Typical ADLC changes:** scope reduction (less architecture docs), depth-level change, extension activation/deactivation, brownfield-mode switch.

---

### Issue_Log.md
```markdown
# Issue Log

<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

| ID | Phase | Date Raised | Issue | Severity | Area | Owner | Status | Resolution | Resolved |
|----|-------|:-----------:|-------|:--------:|------|:-----:|:------:|-----------|:--------:|
| ADLC-{ABBREV}-I-1 | ADLC | {date} | {issue} | {H/M/L} | {area} | {owner} | ☐ Open | — | — |
```

**Status values:** ☐ Open · 🔄 Investigating · ✅ Resolved · ⏸️ On Hold · ❌ Escalated

**Typical ADLC issues:** missing stakeholder input, technology constraint discovered mid-design, conflicting quality attributes, ADR reversal required.

---

### Lessons_Learned.md
```markdown
# Lessons Learned

<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

| ID | Phase | Date | Lesson | Context | Action Taken | Category |
|----|-------|------|--------|---------|--------------|----------|
| ADLC-{ABBREV}-L-1 | ADLC | {date} | {lesson} | {what happened} | {corrective action} | {Process/Architecture/Technology/Governance} |
```

**Category note:** AI-ADLC adds "Architecture" as a category (in addition to Process/People/Technology/Governance) — this captures lessons about the design process itself (e.g., "C4 L3 was too granular for this system's size").

---

## When AI-ADLC Records (Mapping to Stages)

> Example IDs below omit the project handle for brevity; actual IDs are project-qualified `ADLC-{ABBREV}-{TYPE}-{N}` (e.g. `ADLC-XYZ-D-1`).

| ADLC Stage | Registers Typically Touched | Example Entry |
|:----------:|---------------------------|---------------|
| 1 (Mode Detection) | Decisions | `ADLC-D-001: Input mode = PIP (full chain)` |
| 2 (Architecture Vision) | Decisions | `ADLC-D-002: Guiding principles finalized (6 principles)` |
| 3-4 (C4 L1/L2) | Issues | `ADLC-I-001: External system X undocumented` |
| 5 (Technology Stack) | Decisions | `ADLC-D-003: Selected PostgreSQL over DynamoDB (see ADR-003)` |
| 6-9 (Design) | Changes, Issues | `ADLC-C-001: API design depth reduced (Medium depth selected)` |
| 10-11 (Component + Integration) | Issues | `ADLC-I-002: Circular dependency between modules A and B` |
| 12 (Extensions) | Decisions | `ADLC-D-004: Activated DDD Tactical + Microservices extensions` |
| 13 (Assembly) | Lessons | `ADLC-L-001: Brownfield mode requires 30% more time — plan accordingly` |

---

## Relationship to the Architecture Workbook

The `Architecture_Workbook.md` (AI-ADLC's own output artifact) tracks **open design questions, discussion threads, and unresolved trade-offs** within the architecture process. It is NOT a governance register — it is a working artifact that gets resolved by the end of the ADLC workflow.

| Artifact | Purpose | Persists After ADLC? |
|----------|---------|:--------------------:|
| Architecture Workbook | Open design questions during ADLC | ❌ Resolved by Assembly |
| Decision_Log (spine) | Sub-threshold process decisions | ✅ Persists across chain |
| ADRs | Formal architecture decisions | ✅ Part of the Architecture Package |

---

## Standalone vs. Chain Behavior (Summary)

| Mode | What Happens |
|------|-------------|
| **Standalone** (no predecessor has run) | AI-ADLC creates the spine from scratch with 4 registers. Self-contained. |
| **Chain** (spine exists from AI-PILC or AI-ILC) | AI-ADLC appends `ADLC-*` entries to existing registers. One consolidated record. |
| **Brownfield** (existing non-conforming `management_framework/`) | Add marker + Phase columns non-destructively; do not renumber existing entries. |

---

## Contributing Phases Row (for the Index)

When AI-ADLC appends to an existing spine, it adds this row to `MANAGEMENT_FRAMEWORK.md`:

```markdown
| ADLC | AI-ADLC | {date} | Decision, Change, Issue, Lessons |
```

---

*Template Version: 1.2.0 | Contract: MANAGEMENT_FRAMEWORK_CONTRACT.md v1.3.0 + OUTPUT_AND_STATE_CONTRACT.md v1.0.0 | Package: AI-ADLC | Phase code: ADLC | IDs: project-qualified ADLC-{ABBREV}-{TYPE}-{N}*
