<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-POLC
generatedVersion: 1.0.0
source: "management-framework-contract"
generatedOn: "{ISO-date}"
ownership: hybrid
---

# Management Framework — Governance Spine

**Scope:** Per-project governance trail
**Contributing Phase:** AI-POLC (Product Ownership Life Cycle)
**Phase Code:** POLC
**ID Formats:** project-qualified — `POLC-{ABBREV}-D-{N}` (Decision), `POLC-{ABBREV}-C-{N}` (Change), `POLC-{ABBREV}-I-{N}` (Issue), `POLC-{ABBREV}-L-{N}` (Lesson)
**Location:** `{project_root}/management_framework/` where `{project_root}` = `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/` (sibling of `backlog/`)
**Contract:** MANAGEMENT_FRAMEWORK_CONTRACT.md v1.2.0 + OUTPUT_AND_STATE_CONTRACT.md v1.0.0

---

## Contributing Phases

| Phase Code | Package | Status |
|:---:|---|:---:|
| POLC | AI-POLC (Product Ownership) | Active |

---

## Registers

AI-POLC contributes to four universal registers:

### Decision Log (`Decision_Log.md`)

Records significant product decisions.

| ID | Date | Phase | Decision | Rationale | Status |
|---|---|:---:|---|---|:---:|
| POLC-{ABBREV}-D-1 | {date} | POLC | {Decision description} | {Why} | Open |

**When to log:** Priority model selection, scope acceptance/rejection, MVP boundary, DoR/DoD establishment, stakeholder escalation outcomes.

### Change Log (`Change_Log.md`)

Records changes to product governance or backlog structure.

| ID | Date | Phase | Change | Trigger | Impact | Status |
|---|---|:---:|---|---|---|:---:|
| POLC-{ABBREV}-C-1 | {date} | POLC | {What changed} | {Why} | {Affected items} | Open |

**When to log:** Reprioritization, DoR/DoD updates, release plan changes, epic scope changes, roadmap pivots.

### Issue Log (`Issue_Log.md`)

Records blockers and product-level issues.

| ID | Date | Phase | Issue | Severity | Owner | Status |
|---|---|:---:|---|:---:|---|:---:|
| POLC-{ABBREV}-I-1 | {date} | POLC | {Issue description} | {H/M/L} | {Role} | Open |

**When to log:** DLC blockers, stakeholder conflicts, dependency issues, assumption invalidation.

### Lessons Learned (`Lessons_Learned.md`)

Records product ownership insights.

| ID | Date | Phase | Lesson | Category | Action |
|---|---|:---:|---|---|---|
| POLC-{ABBREV}-L-1 | {date} | POLC | {What was learned} | {Category} | {Follow-up} |

**When to log:** Prioritization model effectiveness, estimation accuracy, stakeholder management insights, DoR/DoD calibration.

---

## Behavior Rules

- **Append-if-exists:** If `{project_root}/management_framework/MANAGEMENT_FRAMEWORK.md` already exists, append POLC-* entries to existing registers
- **Create-if-absent:** If no spine exists, create `{project_root}/management_framework/` (sibling of `backlog/`) with marker + registers
- **Non-destructive:** NEVER edit or delete another phase's entries
- **Namespace collision-free:** project-qualified `POLC-{ABBREV}-*` prefix prevents ID conflicts across phases AND across projects (`PILC-{ABBREV}-*`, `ADLC-{ABBREV}-*`, etc.)

---

## ID Assignment Protocol (Numbering — OI-031)

Every entry ID uses the format `POLC-{ABBREV}-{TYPE}-{N}` where `{N}` is a sequential integer. To assign `{N}`:

```
1. READ the target register file (e.g. Decision_Log.md).
2. SCAN all existing rows for this phase+project prefix (POLC-{ABBREV}-{TYPE}-*).
3. FIND the highest {N} value currently present.
4. ASSIGN {N} = highest + 1 (or 1 if no existing entries for this prefix).
5. WRITE the new entry with the assigned ID.
```

**Concurrency model:** The AI-* Family operates in a single-user, single-agent model. The scan-and-increment protocol is safe because only one writer operates on a given register at a time. If future parallelism is introduced (multiple agents writing the same register concurrently), a reservation or locking mechanism would be required — that is explicitly deferred.

**Carry-forward continuity:** When a spine is carried forward into a dev workspace (DWG hinge), numbering continues from the last assigned `{N}` — never resets to 1.

---

*Template Version: 1.1.0 | Contract: MANAGEMENT_FRAMEWORK_CONTRACT.md v1.3.0 + OUTPUT_AND_STATE_CONTRACT.md v1.0.0 | Package: AI-POLC | Phase code: POLC | IDs: project-qualified POLC-{ABBREV}-{TYPE}-{N}*
