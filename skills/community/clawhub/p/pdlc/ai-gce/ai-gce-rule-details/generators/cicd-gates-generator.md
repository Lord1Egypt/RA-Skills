<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# CI/CD Quality Gates — Derivation Logic

## Purpose

Derives CI/CD quality gate rules (GOV-CICD-*) from `testing-strategy.md` and `git-workflow.md`. HYBRID: built-in baseline ensures tests pass; steering provides specific thresholds.

---

## MANDATORY: Stage Sub-Role — Automation Engineer

During THIS activity, ALSO adopt the mindset of an **Automation Engineer**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in pipeline stages: every quality gate is a pass/fail checkpoint with measurable thresholds
- Derive thresholds from steering, never invent them — if testing-strategy.md says 80%, the rule says 80%
- Consider gate placement: what runs on PR vs. merge vs. deploy determines when enforcement fires
- Ensure gates are automatable: if a CI system can't check it, it's not a CI/CD gate rule
- Link coverage-check hooks to actual threshold values from the steering file

### Anti-Patterns for This Activity
- Do NOT create CI/CD rules without specific numeric thresholds (aspirational gates are useless)
- Do NOT assume pipeline stages — derive them from git-workflow.md explicitly
- Do NOT conflate CI quality gates with governance checks (CI gates = automated, governance = may need human judgment)

### Quality Check
A good output from this activity sounds like:
- "GOV-CICD-002: Line coverage ≥ 80% at PR gate. Derived from testing-strategy.md → Coverage Targets. Enforced by coverage-check.json (agentStop, Tier B). Tier 2."
- "Built-in baseline: GOV-CICD-BASELINE-02 — security scan 0 Critical/High. This fires regardless of whether testing-strategy.md exists."

---

## Source Files

| File | What to Extract |
|------|----------------|
| `testing-strategy.md` | Coverage targets (line %, branch %), test types required, security scan expectations |
| `git-workflow.md` | Pipeline stages, what runs on PR vs. merge vs. deploy |

---

## Built-in Baseline

| Rule ID | Statement |
|---------|-----------|
| GOV-CICD-BASELINE-01 | Unit tests MUST pass (0 failures) before merge |
| GOV-CICD-BASELINE-02 | Security scan MUST report 0 Critical/High findings before merge |

---

## Steering-Enriched Rules

| Steering Content | Generated Rule |
|-----------------|---------------|
| "Line coverage ≥ 80%" | GOV-CICD-002: Coverage ≥ 80% at PR gate |
| "Branch coverage ≥ 70%" | GOV-CICD-003: Branch coverage ≥ 70% at PR gate |
| "Architecture violations = 0" | GOV-CICD-005: Architecture boundary tests pass |
| "Smoke tests after staging deploy" | GOV-CICD-006: Smoke suite passes post-staging |
| "Error rate < baseline + 1% post-prod" | GOV-CICD-007: Error rate threshold monitored post-deploy |

---

## Hook: `coverage-check.json`

- **Event:** agentStop (Tier B)
- **Checks:** GOV-CICD-002/003 — coverage meets stated thresholds

## Hook: `pre-pr-checklist.json` (shared)

- **Checks:** GOV-CICD-001/002/003/005 as part of PR readiness

## Tier: 2 (CI pipeline must exist — Tier 2 readiness criterion)
