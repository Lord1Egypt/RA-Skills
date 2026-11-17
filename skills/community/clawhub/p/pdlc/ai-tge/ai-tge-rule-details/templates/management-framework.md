<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Management Framework — Spine Contribution Guide (AI-TGE)

| Field | Value |
|-------|-------|
| **Package** | AI-TGE (Test Governance Engine) |
| **Phase Code** | `TGE` |
| **Role** | Contributor — logs test-governance decisions to the shared spine; primary operational record remains `.governance/test/` |
| **Registers Contributed To** | 2 (Decision, Lessons) |
| **Contract Reference** | Management Framework Contract v1.2.0 + Multi-Project Output & State Contract v1.0.0 |

---

## Purpose

AI-TGE's primary record is its own `.governance/test/` folder (test register, coverage reports, debt scorecard, defect log). That remains unchanged — it is the **detailed test-governance operational record**.

This guide defines when and how AI-TGE also writes **summary governance entries** to the shared project spine. The spine entries are the human-readable, cross-phase governance record; `.governance/test/` is the detailed test-specific record.

---

## What AI-TGE Logs to the Spine (and What It Does NOT)

| Logs to Spine (summary, human-governance) | Stays in `.governance/test/` (detail, operational) |
|-------------------------------------------|----------------------------------------|
| `TGE-XYZ-D-1: Test strategy finalized — pyramid model, 80% coverage target` | Full `test-strategy.md` document |
| `TGE-XYZ-D-2: Risk acceptance — module X deliberately untested (low blast radius)` | Debt scorecard entry + risk score |
| `TGE-XYZ-D-3: Brownfield assessment — 45% existing coverage, 23 gaps identified` | Complete brownfield gap map |
| `TGE-XYZ-L-1: Architecture reconciliation added 8 tests — reconcile earlier next time` | Register delta details |

**Rule of thumb:** if a human PM reading the Decision Log would care about it as a *project governance decision* → it goes in the spine. If it's a test register entry, coverage calculation, or risk score → it stays in `.governance/test/`.

---

## Behavior: Append-if-Exists Only

AI-TGE **reads from AI-ADLC + AI-DWG** and observes AI-DLC v1. The spine will typically exist by the time AI-TGE runs. Therefore:

```
1. DETECT the spine by marker: management_framework/MANAGEMENT_FRAMEWORK.md
   → Multi-project location: {project_root}/management_framework/,
     where {project_root} = pdlc-ws/projects/PRJ-{ABBREV}-{slug}/.
   → In a dev workspace (carried-forward spine): ./management_framework/.
2. APPEND TGE-phase entries to Decision_Log and Lessons_Learned.
3. Use project-qualified ID prefix TGE-{ABBREV}-{TYPE}-{N} (e.g. TGE-XYZ-D-1).
4. Add/update the TGE row in the index's "Contributing Phases" table.
5. DO NOT touch other phases' rows.
```

**Edge case (standalone AI-TGE — Architecture Only mode, no spine):** If marker is not found, AI-TGE does NOT create the spine. Log the entries to the console/output and note "No governance spine found — entries not persisted to management_framework/."

---

## ID Assignment Protocol (Numbering — OI-031)

Every entry ID uses the format `TGE-{ABBREV}-{TYPE}-{N}` where `{N}` is a sequential integer. To assign `{N}`:

```
1. READ the target register file (e.g. Decision_Log.md).
2. SCAN all existing rows for this phase+project prefix (TGE-{ABBREV}-{TYPE}-*).
3. FIND the highest {N} value currently present.
4. ASSIGN {N} = highest + 1 (or 1 if no existing entries for this prefix).
5. WRITE the new entry with the assigned ID.
```

**Concurrency model:** The AI-* Family operates in a single-user, single-agent model. The scan-and-increment protocol is safe because only one writer operates on a given register at a time. If future parallelism is introduced (multiple agents writing the same register concurrently), a reservation or locking mechanism would be required — that is explicitly deferred.

**Carry-forward continuity:** When a spine is carried forward into a dev workspace (DWG hinge), numbering continues from the last assigned `{N}` — never resets to 1.

---

## Register Schemas (TGE Phase)

### Decision_Log.md (append)
```markdown
| ID | Phase | Date | Decision | Context / Options Considered | Rationale | Decision Maker | Impact | Status |
|----|-------|------|----------|------------------------------|-----------|----------------|--------|:------:|
| TGE-{ABBREV}-D-1 | TGE | {date} | {test governance decision} | {context} | {rationale} | {user/QA lead} | {impact} | ✅ Final |
```

**Typical TGE decisions:**
- Test strategy finalized (model, coverage target, depth level)
- Risk acceptance (component deliberately untested — rationale documented)
- Override of a derived test requirement (user disagrees with AI's derivation)
- Brownfield baseline accepted (existing coverage level acknowledged)
- Architecture reconciliation — new tests added / old tests deprecated

### Lessons_Learned.md (append)
```markdown
| ID | Phase | Date | Lesson | Context | Action Taken | Category |
|----|-------|------|--------|---------|--------------|----------|
| TGE-{ABBREV}-L-1 | TGE | {date} | {lesson} | {what happened} | {corrective action} | {Testing/Process/Architecture} |
```

---

## When AI-TGE Records (Mapping to Stages)

| TGE Stage | Registers Touched | Example |
|:---------:|-------------------|---------|
| 4 (Brownfield Assessment) | Decisions | `TGE-XYZ-D-1: Brownfield baseline — 45% coverage, 23 gaps` |
| 5 (Test Strategy) | Decisions | `TGE-XYZ-D-2: Test pyramid adopted — unit 70% / integration 20% / E2E 10%` |
| 6 (Risk Scoring) | Decisions | `TGE-XYZ-D-3: 3 Critical-risk gaps accepted (team capacity)` |
| 10 (Architecture Reconciliation) | Decisions, Lessons | `TGE-XYZ-L-1: AP change added 8 new requirements — reconcile earlier` |
| 12 (Debt Reassessment) | Lessons | `TGE-XYZ-L-2: Debt reduced from 15→7 in 2 sprints — risk scoring drove focus` |

---

## Contributing Phases Row (for the Index)

```markdown
| TGE | AI-TGE | {date} | Decision, Lessons |
```

---

*Template Version: 1.1.0 | Contract: MANAGEMENT_FRAMEWORK_CONTRACT.md v1.2.0 + OUTPUT_AND_STATE_CONTRACT.md v1.0.0 | Package: AI-TGE | Phase code: TGE | IDs: project-qualified TGE-{ABBREV}-{TYPE}-{N}*
