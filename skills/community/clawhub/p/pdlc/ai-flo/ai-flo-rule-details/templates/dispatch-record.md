<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Dispatch Record: DR-{Project-ID}

| Field | Value |
|-------|-------|
| Project ID | {PRJ-ABBREV-YYYY-NNN} |
| Project Name | {name} |
| Dispatched | {ISO date} |
| Source | AI-PPM DA-{Project-ID} |
| Priority | #{N} |
| Scope | {Full / Design-only / Custom} |
| Profile | skip: {[list] or "none"} |
| Entry Point | {first package(s)} |

---

## Constraints (from PPM Authorization)

| Constraint | Value | Enforcement |
|------------|-------|-------------|
| Budget Ceiling | ${amount} | Re-authorize if exceeded |
| Timeline Deadline | {date or "N months from dispatch"} | Escalate if at risk |
| Team Allocation | {teams/FTE} | No reallocation without PPM approval |
| Dependencies | {list or "none"} | Block until resolved |

---

## Routing Instructions

| # | Target Package | Action | Input Path | Notes |
|---|----------------|--------|-----------|-------|
| 1 | {AI-ADLC} | Start architecture design | {PIP path} | — |
| 2 | {AI-UXD} | Start UX design | {PIP path} | — |
| 3 | {AI-POLC} | Start product ownership | {PIP path} | — |

---

## Operator Action Required

Start sessions for the listed packages, pointing each at the input path.
AI-FLO will track progress via marker detection.

---

## Routing Outcome (updated after execution)

| Target | Started | Completed | Skipped | Notes |
|--------|:-------:|:---------:|:-------:|-------|
| {AI-ADLC} | {date or —} | {date or —} | {—} | — |
| {AI-UXD} | {date or —} | {date or —} | {✅ toggled off} | {reason} |
| {AI-POLC} | {date or —} | {date or —} | {—} | — |

---

*Immutable once created. Amendments are new dispatch records referencing this one.*
