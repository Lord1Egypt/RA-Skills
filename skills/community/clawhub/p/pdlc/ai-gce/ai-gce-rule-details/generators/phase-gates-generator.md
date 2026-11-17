<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Phase Gates — Derivation Logic

## Purpose

Derives phase gate rules (PG-*) from `project-governance.md` and `DEFINITION_OF_DONE.md`. Gates define what MUST exist before transitioning between project phases.

---

## MANDATORY: Stage Sub-Role — Audit & Compliance Specialist

During THIS activity, ALSO adopt the mindset of an **Audit & Compliance Specialist**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in control gates: phase transitions are the highest-stakes governance moments — missing a gate criterion risks delivering incomplete work
- Ensure gate criteria are evidence-based: "charter exists" is verifiable, "team is ready" is not
- Recognize that phase gates are the ONLY rules that can BLOCK transitions — all other rules warn
- Map gate criteria to specific artifacts (files, test results, sign-offs) that prove readiness
- Tier-gate appropriately: setup gates are Tier 1 (day 0), per-module gates are Tier 2, go-live gates are Tier 3

### Anti-Patterns for This Activity
- Do NOT create subjective gate criteria ("code is clean enough") — gates must be binary pass/fail
- Do NOT apply go-live gates during construction phase (phase-awareness is critical)
- Do NOT conflate Definition of Done (per-task) with phase gates (per-transition) — they're related but distinct

### Quality Check
A good output from this activity sounds like:
- "PG-FOUND-003: CI/CD pipeline operational with Build → Test → Security stages before Construction begins. Tier 2, Foundation phase. Enforced by post-task-governance.json."
- "Phase Gate Status: Can transition to Construction? ✅ Yes — all 6 Critical PG-SETUP rules pass. 1 Warning (documentation incomplete, non-blocking)."

---

## Source Files

| File | What to Extract |
|------|----------------|
| `project-governance.md` | Phase model, quality gates table, gate criteria per transition |
| `DEFINITION_OF_DONE.md` | Per-task completion criteria (feeds per-module gates) |

---

## Built-in Baseline

| Rule ID | Statement |
|---------|-----------|
| PG-BASELINE-01 | SOMETHING must exist (spec, design, or requirements) before implementation code is written |

---

## Gate Structure (From project-governance.md Phase Model)

The phase model in project-governance.md defines which transitions exist. For EACH transition, extract gate criteria:

| Transition | Rule Prefix | What Must Exist |
|-----------|:-----------:|-----------------|
| Setup → Foundation | PG-SETUP-* | Charter, RACI, steering files, team agreements, ADRs |
| Foundation → Construction | PG-FOUND-* | CI/CD working, auth framework, reference module, shared kernel |
| Per-module: Inception → Domain | PG-INCEP-* | Requirements spec, API contract, domain model documented |
| Per-module: Domain → Application | PG-DOM-* | Aggregates implemented, value objects immutable, no infra deps |
| Per-module: Application → Infra | PG-APP-* | Use cases implemented, DTOs defined, validation rules |
| Per-module: Infra → Presentation | PG-INFRA-* | Repositories implemented, migrations created |
| Per-module: Presentation → Tests | PG-PRES-* | Controllers match contract, auth on all endpoints |
| Per-module: Tests → Merge | PG-TEST-* | Unit tests, integration tests, contract tests, all pass, reviewed |
| Construction → Integration | PG-CONST-* | All modules tested individually, cross-module events flowing |
| Integration → Go-Live | PG-INTEG-* | E2E tests, security audit, UAT sign-off, rollback plan |

---

## Tier Progression

| Tier | Gates Active |
|:----:|-------------|
| 1 | PG-SETUP-* only (basic: Setup → Foundation) |
| 2 | + PG-FOUND-*, PG-INCEP-* through PG-TEST-* (per-module gates) |
| 3 | + PG-CONST-*, PG-INTEG-* (cross-module + go-live gates) |

---

## Hook Mapping

| Hook | Event | Rules Enforced |
|------|-------|----------------|
| `pre-code-spec-check.json` | preToolUse (write) | PG-INCEP-001/002 (spec + contract exist) |
| `post-task-governance.json` | postTaskExecution | All PG-* for current phase |
| `change-readiness-gate.json` | preTaskExecution | PG-CONST-*, PG-INTEG-* (Tier 3) |

---

## Key Rule

Phase gate rules are the ONLY rules that can BLOCK phase transitions. All other rules warn but don't block. When `periodic-audit.json` runs a full scan, it reports:

```
Phase Gate Status: Can transition to {next phase}? 
  ✅ Yes — all Critical PG-* rules pass
  ❌ No — {n} Critical items blocking: {list}
```
