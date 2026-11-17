<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# DevOps & Deployment — Derivation Logic

## Purpose

Derives DevOps and deployment rules (GOV-DEVOPS-*) from `git-workflow.md` and `docker-compose.yml`. This is a HYBRID category: built-in baseline provides universal Git/CI safety; steering enriches with project-specific pipeline, branching, deployment, and DR rules.

---

## MANDATORY: Stage Sub-Role — Automation Engineer

During THIS activity, ALSO adopt the mindset of an **Automation Engineer**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in deployment safety: every rule should prevent a class of production incident (data loss, downtime, unauthorized change)
- Derive branch strategy, merge policy, and environment config from git-workflow.md — never assume a standard
- Treat migration safety as Tier A (immediate): a destructive schema change is dangerous from the moment it's written
- Consider the full deployment lifecycle: build → test → stage → approve → deploy → verify → rollback readiness
- Map DR rules to Tier 3 (pre-release) — operational readiness is a go-live concern, not a construction concern

### Anti-Patterns for This Activity
- Do NOT assume "standard" Git workflows — derive from what git-workflow.md actually states
- Do NOT mix deployment rules with code quality rules (DevOps = infrastructure/pipeline, not code style)
- Do NOT generate DR rules without phase-gating them to Go-Live (they're irrelevant during construction)

### Quality Check
A good output from this activity sounds like:
- "GOV-DEVOPS-012: No column renames/drops without expand-contract. Derived from git-workflow.md → Migration Strategy. Enforced by migration-safety.json (fileEdited, Tier A 🔴). Pattern: `**/Migrations/**/*.cs`."
- "docker-compose.yml confirms PostgreSQL + Redis. This confirms database-rules.md technology choice. No environment-specific overrides detected."

---

## Source Files

| File | What to Extract |
|------|----------------|
| `git-workflow.md` | Branch strategy, commit conventions, CI/CD pipeline stages, deployment gates, merge strategy, environment strategy |
| `docker-compose.yml` | Infrastructure services, environments defined, database technology confirmation |
| `testing-strategy.md` | CI/CD quality gate thresholds (feeds GOV-CICD — separate generator) |

---

## Built-in Baseline (Always Generated)

| Rule ID | Statement | Rationale |
|---------|-----------|-----------|
| GOV-DEVOPS-BASELINE-01 | No direct push to main/protected branches — PR required | Universal Git safety |
| GOV-DEVOPS-BASELINE-02 | Database migration MUST have a rollback method (Down/revert) | Data safety — destructive operations reversible |
| GOV-DEVOPS-BASELINE-03 | No force push to protected branches | Git safety — history preservation |

---

## Steering-Enriched Rules

### From `git-workflow.md` → Branch Strategy

| Steering Content | Generated Rule |
|-----------------|---------------|
| "Feature branches: feature/{module}-{feature}" | GOV-DEVOPS-007: Branch naming follows `feature/{module}-{feature}` pattern |
| "One module per branch — never mix modules" | GOV-DEVOPS-008: Commits in feature branch touch only one module |
| "Squash merge to main" | GOV-DEVOPS-009: Merge strategy is squash (clean history) |
| "Delete feature branches after merge" | GOV-DEVOPS-010: Auto-delete on merge enabled |

### From `git-workflow.md` → CI/CD Pipeline

| Steering Content | Generated Rule |
|-----------------|---------------|
| "Pipeline stages: Build → Test → Security → Coverage → Deploy" | GOV-DEVOPS-001: Pipeline has all required stages |
| "Every PR triggers full gate" | GOV-DEVOPS-003: PR pipeline includes all quality gates |
| "Pipeline blocks merge on gate failure" | GOV-DEVOPS-004: Branch protection requires pipeline success |

### From `git-workflow.md` → Deployment Strategy

| Steering Content | Generated Rule |
|-----------------|---------------|
| "Production deploy requires manual approval" | GOV-DEVOPS-019: Manual approval gate before production |
| "Staging auto-deploys on merge to main" | GOV-DEVOPS-020: Staging deployment is automatic |
| "Blue-green deployment" | GOV-DEVOPS-017: Zero-downtime deployment strategy documented |
| "Instant rollback capability" | GOV-DEVOPS-018: Previous version retained for immediate rollback |

### From `git-workflow.md` → Migration Strategy

| Steering Content | Generated Rule |
|-----------------|---------------|
| "Migrations run BEFORE deployment" | GOV-DEVOPS-011: Migration step precedes app deployment in pipeline |
| "Backward-compatible schema changes only" | GOV-DEVOPS-012: No column renames/drops without expand-contract |
| "Expand-contract for breaking changes" | GOV-DEVOPS-013: Breaking schema changes split across deployments |
| "Every migration has Down() method" | GOV-DEVOPS-014: Rollback method implemented for every migration |

### From `git-workflow.md` → Environment Strategy

| Steering Content | Generated Rule |
|-----------------|---------------|
| "Four environments: Local, CI, Staging, Production" | GOV-DEVOPS-022: All four environments defined |
| "Config via environment variables" | GOV-DEVOPS-025: No environment-specific values hardcoded |
| "No production data in non-prod (GDPR)" | GOV-DEVOPS-024: Data anonymization for non-prod environments |

### From `git-workflow.md` → DR/Incident Response

| Steering Content | Generated Rule |
|-----------------|---------------|
| "DR strategy documented with RTO/RPO" | GOV-DEVOPS-038: DR strategy exists with tier classification |
| "Backup verification daily" | GOV-DEVOPS-040: Automated restore job runs daily |
| "Incident response: DETECT → TRIAGE → FIX → POST-MORTEM" | GOV-DEVOPS-044: Incident response process documented |
| "Production incident → steering file update" | GOV-DEVOPS-046: Post-mortem includes steering update action |

---

## Tier Assignment

| Rules | Tier | Rationale |
|-------|:----:|-----------|
| GOV-DEVOPS-BASELINE-01/02/03 | 1 | Universal safety — active from Day 0 |
| GOV-DEVOPS-001 through 047 (full set) | 2 | CI/CD must exist (Tier 2 readiness criterion) |
| DR/incident rules (038-047) | 3 | Operational readiness for production |

---

## Hook Mapping

| Hook | Event | Rules Enforced |
|------|-------|----------------|
| `migration-safety.json` | fileEdited (Tier A 🔴) | GOV-DEVOPS-012/013/014, GOV-DEVOPS-BASELINE-02 |
| `pre-pr-checklist.json` | userTriggered | GOV-DEVOPS-003/004/007/008 |
| `post-task-governance.json` | postTaskExecution | GOV-DEVOPS-005 (architecture tests) |

---

## Phase Applicability

| Phase | Rules Active |
|-------|-------------|
| Setup | GOV-DEVOPS-BASELINE-01/02/03 only |
| Foundation | + GOV-DEVOPS-001/006/007/008 (pipeline + branch strategy) |
| Construction+ | Full GOV-DEVOPS-* set (Tier 2) |
| Go-Live | + DR/incident rules (Tier 3) |
