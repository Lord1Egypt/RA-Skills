<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Change Management — Derivation Logic

## Purpose

Derives change management rules (CM-*) from `project-governance.md` phase gate requirements. Tier 3 ONLY — these rules activate at pre-release when the team needs formal change readiness.

---

## MANDATORY: Stage Sub-Role — Audit & Compliance Specialist

During THIS activity, ALSO adopt the mindset of an **Audit & Compliance Specialist**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in release readiness: change management rules exist to prevent go-live failures, not to slow construction
- Ensure every CM rule maps to a verifiable artifact (change plan, training record, rollback procedure)
- Phase-gate strictly: CM rules are IRRELEVANT before Integration phase — enforce nothing prematurely
- Consider stakeholder impact: UAT sign-off, communication plans, and training are about people readiness, not code readiness
- Treat rollback documentation as a safety control — no release without proven recovery capability

### Anti-Patterns for This Activity
- Do NOT activate CM rules during Construction phase (they serve no purpose there)
- Do NOT generate CM rules if project-governance.md has no go-live/release section
- Do NOT conflate change management with sprint governance (CM = release-level, Sprint = iteration-level)

### Quality Check
A good output from this activity sounds like:
- "CM-010: Rollback criteria + procedure documented per module. Tier 3, Integration+ phase. Verified by change-readiness-gate.json (preTaskExecution). Skips silently during Construction."
- "project-governance.md mentions UAT requirement → CM-004/005 generated. Training section absent → CM-006 NOT generated (no steering = no rule)."

---

## Source: `project-governance.md` → Phase Gate Criteria for Integration/Go-Live

| Gate Criteria | Generated Rule |
|--------------|---------------|
| "Change management plan before release" | CM-001: Change management plan exists before Integration phase |
| "Stakeholder communication plan" | CM-002: Stakeholder map covers all impacted groups |
| "UAT required per module" | CM-004: UAT scenarios trace to requirements; CM-005: UAT sign-off per module |
| "Training before go-live" | CM-006: Role-based training complete before go-live |
| "Rollback documented" | CM-010: Rollback criteria + procedure documented per module |

---

## No Built-in Baseline

Change management is entirely project-specific and only relevant at release time. If the project has no go-live planned, CM rules are never activated.

---

## Hook: `change-readiness-gate.json`

- **Event:** preTaskExecution (Tier 3)
- **Phase-check:** Only enforces during Integration and Go-Live phases. Construction tasks skip silently.
- **Checks:** CM-001/002/004/005/006/010

---

## Tier: 3 (pre-release enforcement only)

## Phase: Integration → Go-Live (CM rules are irrelevant before Integration)
