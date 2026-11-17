<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Management Framework — Consolidated Spine Template (AI-ILC)

| Field | Value |
|-------|-------|
| **Package** | AI-ILC (Idea Life Cycle) |
| **Phase Code** | `ILC` |
| **Role** | Contributor — idea-stage decisions seed the governance spine at the earliest point |
| **Registers Produced** | 2 (Decision, Lessons) |
| **Contract Reference** | Management Framework Contract v1.2.0 + Multi-Project Output & State Contract v1.0.0 |

---

## Purpose

This template defines how AI-ILC contributes to the **shared governance spine**. AI-ILC is the optional pre-stage package — it runs before AI-PILC to evaluate and approve ideas. Its governance contribution is lightweight: logging the **idea-gate decisions** (approve/park/reject) and any **lessons** from the evaluation process.

AI-ILC may be the **very first** package to run on a project, so in some chains it will **create** the spine. In others (rare — e.g., user manually seeds a spine first), it **appends**.

---

## Registers AI-ILC Produces

| Register | What ILC Logs | Example |
|----------|---------------|---------|
| Decision Log | Idea-gate decisions (approve, park, reject, merge, scope) | `ILC-MTA-D-1: Idea 010 APPROVED as standalone package AI-UXD` |
| Lessons Learned | Evaluation process insights | `ILC-MTA-L-1: Feedback-coupling analysis was the tiebreaker — add to standard evaluation` |

AI-ILC does NOT produce Change Log, Issue Log, Action Items, or Assumptions — those are project-execution concerns, not idea-stage concerns.

---

## Behavior: Append-if-Exists / Create-if-Absent

```
1. DETECT the spine by marker:
   → Scan for management_framework/MANAGEMENT_FRAMEWORK.md
   → Multi-project default location: {project_root}/management_framework/,
     where {project_root} = pdlc-ws/projects/PRJ-{ABBREV}-{slug}/.
   → Detection path: user-provided path → {project_root}/management_framework/ →
     pdlc-ws/projects/*/management_framework/ →./management_framework/ → ask user.

2. IF marker found (spine exists):
   → APPEND ILC-phase entries to Decision_Log and Lessons_Learned.
   → Use project-qualified ID prefix ILC-{ABBREV}-{TYPE}-{N} (e.g. ILC-MTA-D-1).
   → Add/update the ILC row in the index's "Contributing Phases" table.
   → DO NOT touch other phases' rows (additive, non-destructive).

3. IF marker NOT found (no spine — ILC is first):
   → CREATE management_framework/ at the project root ({project_root}/management_framework/).
   → Generate the index file (MANAGEMENT_FRAMEWORK.md) using the standard template.
   → Generate Decision_Log.md and Lessons_Learned.md from the schemas below.
   → Other registers are created later by AI-PILC when it runs.
```

---

## ID Assignment Protocol (Numbering — OI-031)

Every entry ID uses the format `ILC-{ABBREV}-{TYPE}-{N}` where `{N}` is a sequential integer. To assign `{N}`:

```
1. READ the target register file (e.g. Decision_Log.md).
2. SCAN all existing rows for this phase+project prefix (ILC-{ABBREV}-{TYPE}-*).
3. FIND the highest {N} value currently present.
4. ASSIGN {N} = highest + 1 (or 1 if no existing entries for this prefix).
5. WRITE the new entry with the assigned ID.
```

**Concurrency model:** The AI-* Family operates in a single-user, single-agent model. The scan-and-increment protocol is safe because only one writer operates on a given register at a time. If future parallelism is introduced (multiple agents writing the same register concurrently), a reservation or locking mechanism would be required — that is explicitly deferred.

**Carry-forward continuity:** When a spine is carried forward into a dev workspace (DWG hinge), numbering continues from the last assigned `{N}` — never resets to 1.

---

## Register Schemas (ILC Phase)

### Decision_Log.md
```markdown
<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

# Decision Log

| ID | Phase | Date | Decision | Context / Options Considered | Rationale | Decision Maker | Impact | Status |
|----|-------|------|----------|------------------------------|-----------|----------------|--------|:------:|
| ILC-{ABBREV}-D-1 | ILC | {date} | {idea gate decision} | {options evaluated} | {rationale} | {user/sponsor} | {downstream impact} | ✅ Final |
```

**Typical ILC decisions:**
- Idea approved → proceed to AI-PILC (or direct to AI-ADLC)
- Idea parked → revisit on {date}
- Idea rejected → rationale documented
- Idea merged with another → combined identity rule
- Scope confirmed at idea stage → build scope locked

---

### Lessons_Learned.md
```markdown
<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

# Lessons Learned

| ID | Phase | Date | Lesson | Context | Action Taken | Category |
|----|-------|------|--------|---------|--------------|----------|
| ILC-{ABBREV}-L-1 | ILC | {date} | {lesson} | {what happened during evaluation} | {corrective action} | {Process/Evaluation/Governance} |
```

---

## When AI-ILC Records (Mapping to Stages)

| ILC Stage | Registers Touched | Example |
|:---------:|-------------------|---------|
| Capture | — | (No governance — just idea intake) |
| Shape | — | (Shaping is a draft — no decisions logged) |
| Evaluate | Decisions | `ILC-MTA-D-1: Scored 28/35 — PROCEED` |
| Scope | Decisions | `ILC-MTA-D-2: v1.0 scope = 7 capabilities; v1.1 deferred` |
| Approve | Decisions, Lessons | `ILC-MTA-D-3: APPROVED — proceed to build` |

---

## Contributing Phases Row (for the Index)

```markdown
| ILC | AI-ILC | {date} | Decision, Lessons |
```

---

## Standalone vs. Chain Behavior (Summary)

| Mode | What Happens |
|------|-------------|
| **Standalone** (no predecessor has run) | AI-ILC creates the spine from scratch with 2 registers + index. Self-contained. |
| **Chain** (spine exists) | AI-ILC appends `ILC-{ABBREV}-*` entries. One consolidated record. |

---

*Template Version: 1.1.0 | Contract: MANAGEMENT_FRAMEWORK_CONTRACT.md v1.2.0 + OUTPUT_AND_STATE_CONTRACT.md v1.0.0 | Package: AI-ILC | Phase code: ILC | IDs: project-qualified ILC-{ABBREV}-{TYPE}-{N}*
