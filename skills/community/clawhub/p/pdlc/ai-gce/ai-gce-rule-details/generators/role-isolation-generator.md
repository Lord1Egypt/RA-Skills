<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Role Isolation — Derivation Logic

## Purpose

Derives role isolation and segregation of duties rules (GOV-ROLE-*) from `role-isolation.md`, `CODEOWNERS`, and `TEAM_AGREEMENTS.md`. This is a HYBRID category: built-in baseline ensures minimum segregation; steering enriches with team-specific roles and rules.

---

## MANDATORY: Stage Sub-Role — Security Architect

During THIS activity, ALSO adopt the mindset of a **Security Architect**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in segregation of duties: the core security principle is that no single person should control all steps of a critical process
- Evaluate role combinations for conflict of interest: Session Owner + Reviewer is NEVER acceptable regardless of team size
- Scale isolation rules to team reality — 2-person teams need soft isolation, not impossible 5-role separation
- Treat self-approval attempts as security events worthy of logging, not just governance failures
- Map CODEOWNERS entries to enforcement hooks — ownership without enforcement is aspirational

### Anti-Patterns for This Activity
- Do NOT create role rules that are impossible to follow for small teams (use scaling rules)
- Do NOT treat all segregation violations equally — financial/security segregation is 🔴, documentation review is 🟡
- Do NOT generate ownership rules without verifying CODEOWNERS actually exists

### Quality Check
A good output from this activity sounds like:
- "GOV-ROLE-004: Session Owner ≠ Reviewer. Derived from role-isolation.md Segregation table + Built-in Baseline. Enforced by segregation-check.json (postTaskExecution). Tier 2, phase Construction+."
- "Team size = 3 → GOV-ROLE-023 (soft isolation) active. One person may hold 2 roles but NEVER Session Owner + Reviewer."

---

## Source Files

| File | What to Extract |
|------|----------------|
| `role-isolation.md` | Roles defined, MUST NOT lists, segregation table, approval chains, AI role boundaries, scaling rules |
| `CODEOWNERS` | Module → owner mapping, steering file ownership, contract ownership |
| `TEAM_AGREEMENTS.md` | PR approval requirements, review process commitments |

---

## Built-in Baseline (Always Generated)

These rules exist regardless of steering content:

| Rule ID | Statement | Rationale |
|---------|-----------|-----------|
| GOV-ROLE-BASELINE-01 | Code author MUST NOT be the code approver (for any PR) | Universal Git safety — prevents unchecked code |
| GOV-ROLE-BASELINE-02 | Production deploy MUST require approval from someone who did not write the code | Segregation of duties — deploy ≠ write |
| GOV-ROLE-BASELINE-03 | Self-approval attempts MUST be logged as security events | Audit trail for segregation violations |

---

## Steering-Enriched Rules

### From `role-isolation.md` → Roles Table

For each role defined in the steering file's roles table, generate:
- One rule confirming role existence in RACI (GOV-ROLE-001)
- One rule per "MUST NOT" entry (GOV-ROLE-003)

| Steering Content | Generated Rule |
|-----------------|---------------|
| "5 roles: Domain Expert, Session Owner, Reviewer, QA, Security" | GOV-ROLE-001: All five roles documented with named people |
| "Reviewer MUST NOT be the same person as Session Owner for same module" | GOV-ROLE-004: Session Owner ≠ Reviewer |
| "Security role reviews all auth/authz changes" | GOV-ROLE-010: Security-sensitive PRs require Security role sign-off |

### From `role-isolation.md` → Scaling Rules

| Team Size | Generated Rule |
|:---------:|---------------|
| 2-3 | GOV-ROLE-023: Soft isolation — one person may wear 2 roles, but NEVER Session Owner + Reviewer |
| 4-5 | GOV-ROLE-024: Standard isolation — dedicated roles per primary function |
| 6+ | GOV-ROLE-025: Strict isolation — no role overlap |

### From `CODEOWNERS`

For each CODEOWNERS entry, generate ownership verification rules:

| CODEOWNERS Entry | Generated Rule |
|-----------------|---------------|
| `src/Modules/Finance/** @finance-reviewer` | GOV-ROLE-017: Finance module changes require @finance-reviewer approval |
| `rules/architecture-*.md @architect` | GOV-ROLE-016: Architecture steering changes require @architect approval |
| `contracts/** @api-reviewer` | GOV-ROLE-019: Contract changes require @api-reviewer + consuming teams |

### From `TEAM_AGREEMENTS.md`

| Agreement Content | Generated Rule |
|------------------|---------------|
| "PRs require at least 1 CODEOWNER approval" | GOV-ROLE-013: CODEOWNER approval required on all PRs |
| "No PR > 400 lines without tech lead approval" | GOV-ROLE-CUSTOM: Large PRs need escalated review |

---

## Tier Assignment

| Rules | Tier | Rationale |
|-------|:----:|-----------|
| GOV-ROLE-BASELINE-01/02/03 | 1 | Universal safety — active from day 0 |
| GOV-ROLE-001 through GOV-ROLE-031 (full set) | 2 | Team-specific segregation needs team context to exist |
| SOX-related segregation (financial creator ≠ approver) | 3 | Compliance-level segregation for regulated industries |

---

## Hook Mapping

| Hook | Event | Rules Enforced |
|------|-------|----------------|
| `segregation-check.json` | postTaskExecution | GOV-ROLE-004/005/006/007 |
| `post-task-governance.json` | postTaskExecution | GOV-ROLE-BASELINE-01 (author ≠ approver reminder) |
| `pre-pr-checklist.json` | userTriggered | GOV-ROLE-013 (CODEOWNER approval), GOV-ROLE-009 (self-approval blocked) |

---

## Phase Applicability

| Phase | Rules Active |
|-------|-------------|
| Setup | GOV-ROLE-BASELINE-01/02/03 only |
| Foundation | + GOV-ROLE-001 (roles documented) |
| Construction+ | Full GOV-ROLE-* set (Tier 2) |

---

## Team Topology Integration

GOV-ROLE rules feed into GOV-TT rules. The team topology generator (`team-topology-generator.md`) reads CODEOWNERS and module-structure.md for ownership-level rules. Role isolation focuses on INDIVIDUAL duties; team topology focuses on TEAM ownership boundaries.
