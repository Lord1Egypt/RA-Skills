<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# PR Governance — Derivation Logic

## Purpose

Derives PR governance rules (GOV-PR-*) from `git-workflow.md`, `TEAM_AGREEMENTS.md`, and `role-isolation.md`. HYBRID: built-in baseline ensures basic PR safety; steering enriches with project-specific review practices.

---

## MANDATORY: Stage Sub-Role — Audit & Compliance Specialist

During THIS activity, ALSO adopt the mindset of an **Audit & Compliance Specialist**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in review controls: PR governance ensures that code changes go through verified checkpoints before reaching production
- Enforce the trust spectrum: high-risk code (financial, security) gets zero-trust review, utility code gets standard review
- Derive commit conventions and size limits from team agreements — don't invent standards the team didn't agree to
- Ensure PR rules connect to role isolation: "reviewed by non-author" is both a PR rule and a segregation rule
- Treat pre-pr-checklist as a comprehensive readiness gate, not a quick check

### Anti-Patterns for This Activity
- Do NOT weaken "PR reviewed by non-author" — this is both built-in baseline AND segregation of duties
- Do NOT generate PR size limits without explicit team agreement in TEAM_AGREEMENTS.md
- Do NOT make PR rules that can't be verified at PR time (runtime checks don't belong here)

### Quality Check
A good output from this activity sounds like:
- "GOV-PR-002: Commit messages follow `{type}({scope}): {description}` format. Derived from git-workflow.md → Commit Convention. Checked by pre-pr-checklist.json (userTriggered). Tier 2."
- "GOV-PR-008: Financial logic PRs require zero-trust review (line-by-line). Derived from role-isolation.md → Trust Spectrum table."

---

## Source Files

| File | What to Extract |
|------|----------------|
| `git-workflow.md` | Commit convention format, branch naming, merge strategy |
| `TEAM_AGREEMENTS.md` | PR template requirements, review turnaround SLA, PR size limits |
| `role-isolation.md` | Review trust spectrum (which code gets zero-trust review) |

---

## Built-in Baseline

| Rule ID | Statement |
|---------|-----------|
| GOV-PR-BASELINE-01 | Tests MUST pass in CI before merge is allowed |
| GOV-PR-BASELINE-02 | PR MUST be reviewed by someone other than the author |

---

## Steering-Enriched Rules

| Steering Content | Generated Rule |
|-----------------|---------------|
| "Commit format: {type}({scope}): {description}" | GOV-PR-002: Commit messages follow convention |
| "No direct push to main" | GOV-PR-003: Branch protection enforced |
| "Review uses trust spectrum" | GOV-PR-008: High-risk code (financial, security) gets zero-trust review |
| "Financial calculations reviewed line-by-line" | GOV-PR-010: Financial logic PRs require explicit sign-off |
| "Security controls reviewed line-by-line" | GOV-PR-011: Security PRs require explicit sign-off |
| "PR size limit: 400 lines" | GOV-PR-CUSTOM: Large PRs flagged for splitting |

---

## Hook: `pre-pr-checklist.json`

- **Event:** userTriggered
- **Checks:** GOV-PR-001 through 012 + GOV-PR-BASELINE-01/02

## Tier: 2 (PR governance needs CI pipeline — Tier 2 readiness criterion)
