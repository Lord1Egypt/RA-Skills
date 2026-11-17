<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Infrastructure & Deployment → CICD_GUIDE.md

## Purpose

This mapping rule transforms the **CI/CD Strategy** and **Deployment Architecture** sections of the Infrastructure & Deployment document (AP artifact) into a comprehensive CI/CD pipeline guide — a root-level operational document that tells a DevOps engineer exactly how to set up, maintain, and evolve the project's delivery pipeline.

**Output:** `info/CICD_GUIDE.md` — placed at project root alongside `info/CONTRIBUTING.md` and `info/PROJECT_INSTRUCTIONS.md`

**Relationship to git-workflow.md:** The `git-workflow.md` steering file (produced by `mapping/infra-to-config.md`) defines CI pipeline stages as RULES (GIT-CI-NN) — what the pipeline MUST do. `info/CICD_GUIDE.md` is the operational companion — HOW to set up and configure the pipeline, quality gates, rollback procedures, and troubleshooting.

---

## MANDATORY: Stage Sub-Role — Automation Engineer

During THIS activity, ALSO adopt the mindset of an **Automation Engineer**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Write tool-agnostic pipeline guidance — describe WHAT stages must do, not HOW in a specific CI tool's YAML syntax
- Think about rollback from the start — every deployment rule must have an undo path; "no deploy without rollback plan" is non-negotiable
- Treat quality gates as production safety nets — disabling a gate "temporarily" is how permanent degradation starts
- Cross-reference git-workflow.md GIT-CI-NN rules — this guide EXPANDS those enforcement rules into operational procedures
- Ensure secrets management is consistent with security-rules.md — two docs, one truth about credential handling

### Anti-Patterns for This Activity
- Do NOT invent coverage targets or latency SLOs — use AP values; if absent, use `{from AP}` placeholder
- Do NOT make the guide tool-specific (GitHub Actions YAML, Jenkinsfile) — keep it operational and portable
- Do NOT skip rollback procedures for any depth level — every project needs them regardless of AP detail

### Quality Check
A good output from this activity sounds like:
- "Quality gate: SAST critical = 0 tolerance (pipeline fails). SAST high = 3 max (pipeline warns). Dependency CVE critical = 0 (blocks deployment)."
- "Rollback time target: <5 minutes from decision to restored. Automatic trigger: >5% 5xx rate for 2 minutes → previous image redeployed."

---

## Source (AP Artifact)

**Primary Document:** Infrastructure & Deployment (typically `10_Infrastructure_Deployment.md` or `design/integration-infrastructure.md` — Part B)

**Sections to extract:**

| Section | Contains | Maps To |
|---------|----------|---------|
| CI/CD Strategy | Pipeline philosophy, tooling preferences, automation level | Pipeline Overview + Tooling section |
| Pipeline Stages | Build/test/scan/deploy stage definitions | Pipeline Stages section |
| Quality Gates | Thresholds for passing (coverage, lint, SAST severity) | Quality Gates section |
| Deployment Strategy | Deployment method (rolling, blue-green, canary) | Deployment Strategy section |
| Environment Strategy | Dev/staging/prod topology, promotion rules | Environment Promotion section |
| Rollback Strategy | How to undo failed deployments | Rollback Procedures section |
| Artifact Management | Image registry, versioning, retention | Artifact Management section |
| Release Strategy | Versioning, tagging, changelog generation | Release Process section |

**Additional sources:**
- Technology Stack (build tools, test runners, container tooling)
- Security Architecture (SAST/DAST requirements, secret management)
- Quality Attributes (performance SLOs that become gate thresholds)
- `git-workflow.md` steering file (already generated — cross-reference for consistency)

---

## Target: CICD_GUIDE.md (ALWAYS)

### Role

Comprehensive operational guide for CI/CD pipeline setup and maintenance. Answers: "How do I configure and operate the delivery pipeline for this project?" This is NOT a steering file (not enforceable by AI-GCE) — it's a human-readable operations manual.

### Structure

```markdown
<!-- AI-DWG generated | source: Infrastructure & Deployment | date: {generation-date} -->

# CI/CD Pipeline Guide — {System Name}

## Overview

**Pipeline philosophy:** {from AP — e.g., "Automated everything, manual approval for production only"}
**CI tool:** {from AP — e.g., GitHub Actions / GitLab CI / Azure DevOps / Jenkins / AWS CodePipeline}
**Container registry:** {from AP — e.g., ECR / Docker Hub / GitHub Container Registry / Harbor}
**Artifact storage:** {from AP — e.g., S3 / Artifactory / GitHub Packages}
**Deployment target:** {from AP — e.g., Kubernetes / ECS / App Service / VM / Serverless}

---

## Pipeline Stages

<!-- begin: AP-sourced -->

```
┌────────┐   ┌────────┐   ┌────────┐   ┌──────────┐   ┌──────────┐   ┌────────────┐
│  LINT  │──►│  TEST  │──►│ BUILD  │──►│ SECURITY │──►│  DEPLOY  │──►│  VALIDATE  │
│        │   │        │   │        │   │   SCAN   │   │(staging) │   │ (post-dep) │
└────────┘   └────────┘   └────────┘   └──────────┘   └──────────┘   └────────────┘
  ▲ every      ▲ every      ▲ PR to       ▲ PR to        ▲ merge       ▲ after
    push         push        protected     protected      to {branch}    deploy
```

| Stage | Trigger | Runs On | Duration Target | Blocking? |
|-------|---------|---------|:---------------:|:---------:|
| Lint | Every push | All branches | < {n} min | ✅ Yes |
| Unit Test | Every push | All branches | < {n} min | ✅ Yes |
| Integration Test | PR to protected branch | PR branches | < {n} min | ✅ Yes |
| Build | PR to protected branch | PR branches | < {n} min | ✅ Yes |
| Security Scan (SAST) | PR to protected branch | PR branches | < {n} min | ✅ Yes |
| Dependency Audit | PR to protected branch | PR branches | < {n} min | ⚠️ Warn |
| Deploy (staging) | Merge to {branch} | Protected branch | < {n} min | — |
| Smoke Test | After staging deploy | Staging env | < {n} min | ✅ Yes |
| Deploy (production) | {from AP — manual trigger / tag / release} | Release trigger | < {n} min | ✅ Manual gate |
| Post-deploy validation | After production deploy | Production | < {n} min | ⚠️ Alert |

<!-- end: AP-sourced -->

---

## Quality Gates

<!-- begin: AP-sourced -->

Quality gates define the minimum thresholds that MUST pass before code can progress through the pipeline.

### Gate Thresholds

| Gate | Metric | Threshold | Enforcement |
|------|--------|:---------:|-------------|
| Code lint | Lint errors | 0 | Pipeline fails if any lint error |
| Code format | Format violations | 0 | Pipeline fails OR auto-fix |
| Unit test coverage | Line coverage % | {from AP — e.g., ≥80%} | Pipeline fails below threshold |
| Unit test pass | Test failures | 0 | Pipeline fails on any failure |
| Integration test pass | Test failures | 0 | Pipeline fails on any failure |
| SAST (critical) | Critical vulnerabilities | 0 | Pipeline fails if any critical |
| SAST (high) | High vulnerabilities | {from AP — e.g., 0 / ≤3} | Pipeline fails / warns |
| Dependency audit | Known CVEs (critical/high) | 0 critical | Pipeline fails; high = warn |
| Build success | Build errors | 0 | Pipeline fails |
| Image size | Container image size | {from AP — e.g., <500MB} | Warn if exceeded |
| Performance (optional) | p95 latency vs. baseline | {from AP — e.g., <10% regression} | Warn in staging |

### Gate Escalation

| Situation | Action |
|-----------|--------|
| Gate fails on feature branch | Developer fixes before re-requesting review |
| Gate fails on protected branch | Highest priority — blocks all merges until resolved |
| Flaky test (passes on retry) | Mark as flaky; fix within {from AP — e.g., 2 sprints} |
| SAST false positive | Suppress with justification comment + team approval |

<!-- end: AP-sourced -->

---

## Deployment Strategy

<!-- begin: AP-sourced -->

**Method:** {from AP — e.g., Rolling Update / Blue-Green / Canary / Recreate}

### How Deployment Works

{Description derived from AP deployment strategy section — 3-5 sentences explaining the mechanism}

### Deployment Rules

| Rule | Standard |
|------|----------|
| CICD-DEP-01 | {from AP — e.g., Zero-downtime required for all production deployments} |
| CICD-DEP-02 | {from AP — e.g., Database migrations run BEFORE application deploy (forward-compatible)} |
| CICD-DEP-03 | {from AP — e.g., Feature flags gate all user-visible changes in production} |
| CICD-DEP-04 | {from AP — e.g., Canary: 5% traffic for 15 minutes → 25% for 15 minutes → 100%} |
| CICD-DEP-05 | {from AP — e.g., Health check must pass for 60 seconds before marking deploy successful} |
| CICD-DEP-06 | {from AP — e.g., No deployments during peak hours ({time window})} |

### Pre-deployment Checklist

- [ ] All quality gates pass on the release candidate
- [ ] Database migration tested in staging
- [ ] Rollback procedure verified in staging
- [ ] Monitoring dashboards accessible
- [ ] On-call engineer identified
- [ ] Release notes prepared (from changelog)
- [ ] Downstream consumers notified (if breaking change)

<!-- end: AP-sourced -->

---

## Environment Promotion

<!-- begin: AP-sourced -->

```
local (dev) ──► CI (test) ──► staging ──► production
     │              │              │            │
 dev machine    ephemeral     persistent    live traffic
 docker-compose  per-pipeline  shared team   restricted
```

| Environment | Purpose | Deployed From | Promotion Trigger | Access |
|-------------|---------|:-------------:|:----------------:|--------|
| Local (dev) | Developer iteration | docker-compose | Manual | Individual |
| CI (test) | Automated validation | Pipeline build | Every push/PR | CI only |
| Staging | Pre-production validation | {from AP — merge to develop/main} | Auto on merge | Team |
| Production | Live system | {from AP — tag/release/manual} | {from AP — manual approval / auto} | Restricted |

### Promotion Rules

| Rule | Standard |
|------|----------|
| CICD-PROM-01 | Code MUST pass through ALL preceding environments before production |
| CICD-PROM-02 | Staging must mirror production infrastructure (scale can differ, topology must match) |
| CICD-PROM-03 | {from AP — e.g., Minimum 24h in staging before production promotion} |
| CICD-PROM-04 | Same artifact (image/package) promotes through environments — never rebuild per environment |
| CICD-PROM-05 | Environment-specific configuration via environment variables ONLY — not baked into artifact |

<!-- end: AP-sourced -->

---

## Rollback Procedures

<!-- begin: AP-sourced -->

### Automatic Rollback Triggers

| Trigger | Threshold | Action |
|---------|:---------:|--------|
| Health check failure | {from AP — e.g., 3 consecutive failures} | Automatic rollback to previous version |
| Error rate spike | {from AP — e.g., >5% 5xx in 2 minutes} | Automatic rollback |
| Latency spike | {from AP — e.g., p95 > 2x baseline for 3 minutes} | Alert + manual decision |
| Memory/CPU spike | {from AP — e.g., >90% for 5 minutes} | Alert + manual decision |

### Manual Rollback Process

1. **Identify** — Confirm the deployment caused the issue (check timing, metrics, logs)
2. **Decide** — Rollback vs. hotfix forward (prefer rollback if issue is severe)
3. **Execute** — {from AP — e.g., redeploy previous image tag / switch blue-green / rollback canary}
4. **Verify** — Confirm metrics return to baseline
5. **Communicate** — Notify team + stakeholders
6. **Post-mortem** — Document in `management_framework/Issue_Log.md`

### Rollback Rules

| Rule | Standard |
|------|----------|
| CICD-RB-01 | Every deployment MUST have a tested rollback path — no deploy without rollback |
| CICD-RB-02 | Database migrations MUST be backward-compatible (rollback doesn't require data migration) |
| CICD-RB-03 | Previous {from AP — e.g., 5} deployment artifacts retained for quick rollback |
| CICD-RB-04 | Rollback time target: {from AP — e.g., <5 minutes from decision to restored} |
| CICD-RB-05 | Post-rollback: incident created, deploy freeze until root cause identified |

<!-- end: AP-sourced -->

---

## Artifact Management

<!-- begin: AP-sourced -->

| Aspect | Standard |
|--------|----------|
| Image tagging | {from AP — e.g., `{version}-{git-sha-short}` — e.g., `1.2.3-abc1234`} |
| Tag immutability | {from AP — e.g., Tags are immutable — never overwrite a published tag} |
| Retention policy | {from AP — e.g., Keep last 30 versions; delete untagged after 7 days} |
| Registry | {from AP — e.g., ECR per environment / single registry with env prefix} |
| Vulnerability scanning | {from AP — e.g., Scan images on push; block deployment if critical CVE found} |
| Base image updates | {from AP — e.g., Dependabot/Renovate auto-PR for base image updates weekly} |

<!-- end: AP-sourced -->

---

## Release Process

<!-- begin: AP-sourced -->

### Version Scheme

{from AP — e.g., Semantic Versioning: MAJOR.MINOR.PATCH}

- **MAJOR**: Breaking changes (API contracts, data schemas)
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes, security patches

### Release Steps

1. Ensure `{branch}` is green (all gates pass)
2. {from AP — e.g., Create release branch `release/x.y.z` from develop}
3. Update version in {from AP — e.g., `package.json` / `pom.xml` / `version.py`}
4. Generate changelog from conventional commits since last release
5. Create git tag: `v{x.y.z}`
6. Tag triggers production pipeline
7. Monitor post-deploy metrics
8. Announce release (changelog + release notes)

### Changelog Generation

{from AP — e.g., Auto-generated from Conventional Commits using `git-cliff` / `standard-version` / `semantic-release`}

<!-- end: AP-sourced -->

---

## Secrets Management

<!-- begin: AP-sourced -->

| Aspect | Standard |
|--------|----------|
| Secret store | {from AP — e.g., AWS Secrets Manager / HashiCorp Vault / GitHub Secrets / Azure Key Vault} |
| CI secrets | {from AP — e.g., Injected as pipeline environment variables — never in code} |
| Rotation | {from AP — e.g., Automated rotation every 90 days for service accounts} |
| Access | {from AP — e.g., Least privilege — only the pipeline role and production deployment role} |
| Audit | {from AP — e.g., All secret access logged; alerts on unauthorized access attempts} |

### Rules

| Rule | Standard |
|------|----------|
| CICD-SEC-01 | NEVER commit secrets to the repository — use `.gitignore` for all secret files |
| CICD-SEC-02 | Pipeline secrets injected at runtime — masked in logs |
| CICD-SEC-03 | Different secrets per environment — staging and production NEVER share credentials |
| CICD-SEC-04 | Secret rotation must NOT require code changes — use dynamic references |

<!-- end: AP-sourced -->

---

## Monitoring & Observability (Post-Deploy)

<!-- begin: AP-sourced -->

### Deployment Metrics to Watch

| Metric | Baseline Comparison | Alert If |
|--------|:-------------------:|----------|
| Error rate (5xx) | vs. pre-deploy average | > {from AP — e.g., 1% / 2x baseline} |
| Latency (p95) | vs. pre-deploy p95 | > {from AP — e.g., 150% of baseline} |
| CPU utilization | vs. pre-deploy average | > {from AP — e.g., 80%} |
| Memory utilization | vs. pre-deploy | > {from AP — e.g., 85%} |
| Request throughput | vs. pre-deploy | < {from AP — e.g., 80% of expected} |
| Active instances | Expected count | Below minimum threshold |

### Post-Deploy Validation Window

- **Duration:** {from AP — e.g., 30 minutes after production deploy}
- **Action during window:** Monitor all metrics above; prepare for rollback
- **On-call:** {from AP — e.g., Deploying engineer stays available for 1 hour post-deploy}

<!-- end: AP-sourced -->

---

## Pipeline Troubleshooting

### Common Failures

| Failure | Likely Cause | Resolution |
|---------|-------------|------------|
| Lint fails | Code formatting violation | Run `{lint-fix-command}` locally before pushing |
| Tests fail locally but pass in CI | Environment difference | Check `.env` settings; verify docker-compose services running |
| Tests pass locally but fail in CI | Dependency on local state | Ensure tests are isolated; no hardcoded paths |
| Build timeout | Large dependency install | Check cache configuration; optimize dependency resolution |
| Security scan blocks | New CVE in dependency | Update dependency; if no fix available, create exception with justification |
| Deploy fails (staging) | Infrastructure issue / config mismatch | Check environment variables; verify infrastructure state |
| Deploy fails (production) | Same as staging + traffic impact | Rollback immediately; investigate in staging |

### Pipeline Optimization Tips

- Cache dependencies between pipeline runs (node_modules, Maven .m2, pip cache)
- Parallelize independent stages (lint + unit tests can run simultaneously)
- Use incremental builds where supported by the build tool
- Run expensive checks (integration tests, SAST) only on PR branches, not every push
- Keep pipeline definitions in version control (pipeline-as-code)
- Monitor pipeline duration; set alerts if >2x normal

---

## Anti-Patterns (DO NOT)

1. **DO NOT** deploy on Fridays (or before weekends/holidays) without explicit approval
2. **DO NOT** skip staging — even "small" changes can have unexpected impact
3. **DO NOT** share secrets between environments
4. **DO NOT** manually patch production without going through the pipeline
5. **DO NOT** disable quality gates "temporarily" — degradation is permanent once allowed
6. **DO NOT** deploy without a rollback plan
7. **DO NOT** ignore post-deploy metrics — the deploy isn't done until validation passes
8. **DO NOT** let pipeline failures stay red — fix immediately or revert the causing change
```

---

## Transformation Rules

| AP Content | Transformation | Output Section |
|-----------|---------------|----------------|
| CI/CD strategy philosophy | Summarize in Overview | Overview |
| Pipeline stage definitions | Convert to stage table with triggers + duration targets | Pipeline Stages |
| Quality gate thresholds | Convert to gate threshold table + escalation rules | Quality Gates |
| Deployment method (rolling/canary/blue-green) | Describe mechanism + derive CICD-DEP rules | Deployment Strategy |
| Environment topology | Convert to promotion flow + CICD-PROM rules | Environment Promotion |
| Rollback strategy | Convert to trigger table + manual procedure + CICD-RB rules | Rollback Procedures |
| Artifact registry + retention | Convert to artifact management standards | Artifact Management |
| Versioning + release cadence | Convert to release steps + version scheme | Release Process |
| Secret management approach | Convert to CICD-SEC rules | Secrets Management |
| SLOs + monitoring approach | Convert to deployment metrics table + validation window | Monitoring |
| Technology stack (build tools) | Inform Quick Start and Troubleshooting commands | Troubleshooting |

### Numbering Convention

| Prefix | Domain |
|--------|--------|
| CICD-DEP-NN | Deployment rules |
| CICD-PROM-NN | Promotion rules |
| CICD-RB-NN | Rollback rules |
| CICD-SEC-NN | Secret management rules |

---

## Key Rules for This Mapping

1. **Tool-agnostic language** — describe WHAT the pipeline must do, not HOW in a specific CI tool's syntax. The team configures tool-specific implementation (GitHub Actions YAML, Jenkins Groovy, etc.)
2. **Cross-reference git-workflow.md** — pipeline stages must be consistent with GIT-CI-NN rules already generated. This guide EXPANDS on those rules with operational detail.
3. **Thresholds come from AP** — don't invent coverage targets or latency SLOs. If AP doesn't specify, use placeholder `{from AP}` and note the gap.
4. **Rollback is non-negotiable** — every project gets rollback procedures regardless of AP depth. If AP doesn't specify, derive a sensible default from the deployment method.
5. **Secrets section cross-references security-rules.md** — must be consistent with security steering file.
6. **Artifact management reflects tech stack** — container-based projects get image tagging rules; serverless gets package versioning; bare metal gets binary management.
7. **This is operational, not enforcement** — unlike steering files, this guide is for humans to read and follow. AI-GCE does NOT derive hooks from this file.

---

## Depth Adaptation

| Depth | CICD_GUIDE.md Content |
|-------|----------------------|
| **Minimal** | Pipeline stages table + quality gates + basic deployment rules + rollback basics (~2 pages) |
| **Standard** | Full structure as defined above — all sections populated (~4-5 pages) |
| **Comprehensive** | Full structure + pipeline architecture diagram + multi-region deployment details + disaster recovery integration + compliance evidence collection per stage + SLA-driven gate tuning + pipeline security hardening (signed artifacts, SBOM) |

---

## Reconciliation Behavior

| Change | Impact | Action |
|--------|--------|--------|
| Deployment strategy changed (rolling → canary) | Major rewrite of Deployment Strategy + Rollback sections | Rewrite affected sections; flag for team training |
| New quality gate added | Quality Gates table updated | Add gate; verify threshold with user |
| New environment added | Environment Promotion section + table | Add environment; update promotion flow |
| CI tool changed (GitHub Actions → GitLab CI) | Overview section (tool name); guide structure unchanged | Update tool reference; content stays tool-agnostic |
| SLO thresholds changed | Quality Gates + Monitoring sections | Update thresholds; check consistency with performance-standards.md |
| Secret management approach changed | Secrets Management section | Rewrite; verify consistency with security-rules.md |
| Rollback method changed | Rollback Procedures section | Rewrite procedure; update trigger table |

---

## Relationship to Other Files

| File | Relationship |
|------|-------------|
| `rules/git-workflow.md` | Contains CI rules (GIT-CI-NN) as enforcement. CICD_GUIDE expands these into operational detail. |
| `rules/security-rules.md` | Security scanning gates + secret handling must be consistent. |
| `rules/testing-strategy.md` | Test requirements feed quality gate definitions (coverage %, test types). |
| `rules/performance-standards.md` | Performance SLOs feed post-deploy monitoring thresholds. |
| `info/CONTRIBUTING.md` | References CICD_GUIDE for pipeline details. |
| `info/PROJECT_INSTRUCTIONS.md` | Points to CICD_GUIDE for pipeline operations. |
| `management_framework/Issue_Log.md` | Rollback incidents logged here. |
