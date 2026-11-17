<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Sprint Governance — Derivation Logic

## Purpose

Derives sprint governance rules (GOV-SPRINT-*) from `project-governance.md`. Ensures sprint planning and review discipline.

---

## MANDATORY: Stage Sub-Role — Audit & Compliance Specialist

During THIS activity, ALSO adopt the mindset of an **Audit & Compliance Specialist**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in cadence evidence: sprint governance rules verify that planning/review artifacts EXIST, not their quality
- Respect project-specificity: if project-governance.md has no sprint section, generate ZERO GOV-SPRINT rules
- Ensure sprint rules are auditable: "sprint plan exists" is verifiable; "sprint was well-planned" is not
- Consider the audit trail: sprint artifacts are evidence of process discipline for compliance audits
- Tie sprint rules to periodic-audit (not real-time hooks) — sprint artifacts are reviewed on cadence, not per-file

### Anti-Patterns for This Activity
- Do NOT generate sprint rules when project-governance.md lacks sprint cadence information
- Do NOT create rules that judge sprint content quality (only existence and structure)
- Do NOT assign sprint rules to Tier 1 — sprint governance needs established team cadence (Tier 2)

### Quality Check
A good output from this activity sounds like:
- "GOV-SPRINT-001: Sprint plan exists at `docs/sprints/sprint-{N}.md`. Verified by periodic-audit.json during full scan. Tier 2, Construction+ phase."
- "project-governance.md has no sprint section → zero GOV-SPRINT rules generated. This is correct behavior."

---

## Source: `project-governance.md` → Sprint Cadence Section

| Steering Content | Generated Rule |
|-----------------|---------------|
| "Sprint length: 2 weeks" | GOV-SPRINT-001: Sprint plan exists per sprint (`docs/sprints/sprint-{N}.md`) |
| "Planning: Monday of sprint start" | GOV-SPRINT-002: Sprint plan has explicit goal statement |
| "Review: Friday of sprint end" | GOV-SPRINT-003: Capacity allocation documented |
| "Retrospective after review" | GOV-SPRINT-004: Sprint review notes appended |
| — | GOV-SPRINT-005: At least one retro action item per sprint |

## No Built-in Baseline

Sprint governance is entirely project-specific. If project-governance.md has no sprint section, no GOV-SPRINT rules are generated.

## Hook: `periodic-audit.json` (checks GOV-SPRINT during full scan)

## Tier: 2
