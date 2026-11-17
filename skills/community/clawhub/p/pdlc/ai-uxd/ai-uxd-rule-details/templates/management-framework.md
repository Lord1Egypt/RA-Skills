<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-UXD
generatedVersion: 1.0.0
source: "management-framework-contract"
generatedOn: "{ISO-date}"
ownership: hybrid
---

# Management Framework — Governance Spine (AI-UXD)

**Scope:** Per-project governance trail
**Contributing Phase:** AI-UXD (UX Design Life Cycle)
**Phase Code:** UXD
**ID Formats:** project-qualified — `UXD-{ABBREV}-D-{N}` (Decision), `UXD-{ABBREV}-C-{N}` (Change), `UXD-{ABBREV}-I-{N}` (Issue), `UXD-{ABBREV}-L-{N}` (Lesson)
**Location:** `{project_root}/management_framework/` where `{project_root}` = `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/` (sibling of `ux/`)
**Contract:** MANAGEMENT_FRAMEWORK_CONTRACT.md v1.2.0 + OUTPUT_AND_STATE_CONTRACT.md v1.0.0

---

## Purpose

Defines how AI-UXD contributes to the **shared governance spine** — the consolidated `management_framework/` folder that tracks project decisions, changes, issues, and lessons across the AI-* Family chain. AI-UXD writes **UX-design governance** entries (e.g. accessibility-baseline decisions, design-system versioning, WCAG-target selection). It writes to the **4 universal registers** only (no Action Items / Assumptions — those are tracked in the UXP working artifacts).

---

## Contributing Phases

| Phase Code | Package | Status |
|:---:|---|:---:|
| UXD | AI-UXD (UX Design) | Active |

---

## Behavior: Append-if-Exists / Create-if-Absent

```
1. DETECT the spine by marker:
   → Scan for management_framework/MANAGEMENT_FRAMEWORK.md
   → Multi-project default location: {project_root}/management_framework/ (sibling of ux/),
     where {project_root} = pdlc-ws/projects/PRJ-{ABBREV}-{slug}/.
   → Detection path: user-provided path → {project_root}/management_framework/ →
     pdlc-ws/projects/*/management_framework/ → predecessor project root → ask user.

2. IF marker found (spine exists — typical, PILC/ADLC created it):
   → APPEND UXD-phase entries to the 4 registers.
   → Use project-qualified ID prefix UXD-{ABBREV}-{TYPE}-{N} (e.g. UXD-XYZ-D-1).
   → Add/update the UXD row in the index's "Contributing Phases" table.
   → DO NOT touch other phases' rows (additive, non-destructive).

3. IF marker NOT found (UXD originating — no predecessor):
   → CREATE management_framework/ at the project root ({project_root}/management_framework/).
   → Generate the index file (MANAGEMENT_FRAMEWORK.md) using the standard template.
   → Generate the 4 registers from the schemas below.
   → This package operates exactly as standalone (/).
```

---

## ID Assignment Protocol (Numbering — OI-031)

Every entry ID uses the format `UXD-{ABBREV}-{TYPE}-{N}` where `{N}` is a sequential integer. To assign `{N}`:

```
1. READ the target register file (e.g. Decision_Log.md).
2. SCAN all existing rows for this phase+project prefix (UXD-{ABBREV}-{TYPE}-*).
3. FIND the highest {N} value currently present.
4. ASSIGN {N} = highest + 1 (or 1 if no existing entries for this prefix).
5. WRITE the new entry with the assigned ID.
```

**Concurrency model:** The AI-* Family operates in a single-user, single-agent model. The scan-and-increment protocol is safe because only one writer operates on a given register at a time. If future parallelism is introduced (multiple agents writing the same register concurrently), a reservation or locking mechanism would be required — that is explicitly deferred.

**Carry-forward continuity:** When a spine is carried forward into a dev workspace (DWG hinge), numbering continues from the last assigned `{N}` — never resets to 1.

---

## Register Schemas (UXD Phase)

All schemas carry the **Phase** column per the contract. AI-UXD uses prefix `UXD-{ABBREV}-`.

### Decision_Log.md
```markdown
# Decision Log

<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

| ID | Phase | Date | Decision | Context / Options Considered | Rationale | Decision Maker | Impact | Status |
|----|-------|------|----------|------------------------------|-----------|----------------|--------|:------:|
| UXD-{ABBREV}-D-1 | UXD | {date} | {decision} | {context} | {rationale} | {maker} | {impact} | ✅ Final |
```

**When to log:** WCAG conformance target selection, design-system versioning, token architecture decisions, persona-set scope, multi-brand/i18n activation.

### Change_Log.md
```markdown
# Change Log

<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

| ID | Phase | Date Raised | Description | Raised By | Impact Assessment | Approval Status | Approved By | Date Approved | Implemented |
|----|-------|:-----------:|-------------|-----------|-------------------|:---------------:|-------------|:-------------:|:-----------:|
| UXD-{ABBREV}-C-1 | UXD | {date} | {description} | {role} | {scope/design impact} | ☐ Pending | _[TBD]_ | — | ☐ No |
```

**When to log:** design-system breaking changes, IA restructure, flow redesign, depth change.

### Issue_Log.md
```markdown
# Issue Log

<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

| ID | Phase | Date Raised | Issue | Severity | Area | Owner | Status | Resolution | Resolved |
|----|-------|:-----------:|-------|:--------:|------|:-----:|:------:|-----------|:--------:|
| UXD-{ABBREV}-I-1 | UXD | {date} | {issue} | {H/M/L} | {area} | {owner} | ☐ Open | — | — |
```

**When to log:** accessibility blockers, conflicting persona needs, missing research input, unresolvable IA trade-offs.

### Lessons_Learned.md
```markdown
# Lessons Learned

<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

| ID | Phase | Date | Lesson | Context | Action Taken | Category |
|----|-------|------|--------|---------|--------------|----------|
| UXD-{ABBREV}-L-1 | UXD | {date} | {lesson} | {what happened} | {corrective action} | {Process/Design/Accessibility/Governance} |
```

**Category note:** AI-UXD adds "Design" and "Accessibility" as categories (in addition to Process/Governance).

---

## Standalone vs. Chain Behavior (Summary)

| Mode | What Happens |
|------|-------------|
| **Standalone / originating** (no predecessor) | AI-UXD creates the spine from scratch with 4 registers. Self-contained. |
| **Chain** (spine exists from PILC/ADLC) | AI-UXD appends `UXD-{ABBREV}-*` entries to existing registers. One consolidated record. |
| **Brownfield** (existing non-conforming `management_framework/`) | Add marker + Phase columns non-destructively; do not renumber existing entries. |

---

## Contributing Phases Row (for the Index)

When AI-UXD appends to an existing spine, it adds this row to `MANAGEMENT_FRAMEWORK.md`:

```markdown
| UXD | AI-UXD | {date} | Decision, Change, Issue, Lessons |
```

---

*Template Version: 1.1.0 | Contract: MANAGEMENT_FRAMEWORK_CONTRACT.md v1.3.0 + OUTPUT_AND_STATE_CONTRACT.md v1.0.0 | Package: AI-UXD | Phase code: UXD | IDs: project-qualified UXD-{ABBREV}-{TYPE}-{N}*
