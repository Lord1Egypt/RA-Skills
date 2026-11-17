<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: generated
---
# Template: CICD_GUIDE.md

```markdown
<!-- AI-DWG generated | source: Infrastructure & Deployment | date: {generation-date} -->

# CI/CD Pipeline Guide — {System Name}

## Overview

**Pipeline philosophy:** {from AP — e.g., "Automate everything; manual approval only for production"}
**CI tool:** {from AP — e.g., GitHub Actions / GitLab CI / Azure DevOps}
**Container registry:** {from AP — e.g., ECR / GHCR / Docker Hub}
**Artifact storage:** {from AP — e.g., S3 / GitHub Packages}
**Deployment target:** {from AP — e.g., Kubernetes / ECS / App Service}

---

## Pipeline Stages

| Stage | Trigger | Duration Target | Blocking? |
|-------|---------|:---------------:|:---------:|
| Lint | Every push | < 2 min | ✅ |
| Unit Test | Every push | < 5 min | ✅ |
| Integration Test | PR to protected branch | < 10 min | ✅ |
| Build | PR to protected branch | < 5 min | ✅ |
| Security Scan | PR to protected branch | < 5 min | ✅ |
| Deploy (staging) | Merge to {branch} | < 10 min | — |
| Smoke Test | After staging deploy | < 3 min | ✅ |
| Deploy (production) | {trigger from AP} | < 10 min | ✅ Manual |

---

## Quality Gates

| Gate | Threshold | Enforcement |
|------|:---------:|-------------|
| Lint errors | 0 | Fail |
| Test coverage | {from AP — e.g., ≥80%} | Fail |
| Test failures | 0 | Fail |
| Critical vulnerabilities | 0 | Fail |
| High vulnerabilities | {from AP} | Fail/Warn |
| Build errors | 0 | Fail |

---

## Deployment Strategy

**Method:** {from AP — Rolling / Blue-Green / Canary}

Pre-deployment checklist:
- [ ] All quality gates pass
- [ ] Database migration tested in staging
- [ ] Rollback procedure verified
- [ ] Monitoring dashboards accessible
- [ ] On-call engineer identified

---

## Environment Promotion

| Environment | Deployed From | Promotion Trigger |
|-------------|:-------------:|:-----------------:|
| Local (dev) | docker-compose | Manual |
| CI (test) | Pipeline build | Every push/PR |
| Staging | Merge to {branch} | Auto |
| Production | {from AP} | {from AP — manual/auto} |

---

## Rollback Procedures

**Triggers:** Health check failure, error rate spike (>5% 5xx), latency spike

**Process:**
1. Confirm deployment caused the issue
2. Decide: rollback vs. hotfix forward
3. Execute rollback ({method from AP})
4. Verify metrics return to baseline
5. Communicate to team + stakeholders
6. Document in `management_framework/Issue_Log.md`

---

## Secrets Management

- Secrets injected as environment variables at runtime
- Never committed to repository
- Different secrets per environment
- Rotation: {from AP — e.g., every 90 days}

---

## Post-Deploy Monitoring

| Metric | Alert Threshold |
|--------|:---------------:|
| Error rate (5xx) | > {from AP — e.g., 1%} |
| Latency (p95) | > {from AP — e.g., 150% baseline} |
| CPU utilization | > {from AP — e.g., 80%} |
| Memory utilization | > {from AP — e.g., 85%} |

**Validation window:** {from AP — e.g., 30 minutes post-deploy}
```

## Filling Instructions

This template is populated by `mapping/infra-to-cicd.md`.

**Source artifacts:**
- Infrastructure & Deployment (primary — CI/CD strategy, deployment topology, rollback)
- Technology Stack (build tools, test runners)
- Security Architecture (SAST requirements, secret management)
- Quality Attributes (SLOs that become gate thresholds)

**Cross-references after generation:**
- Verify pipeline stages match GIT-CI-NN rules in `rules/git-workflow.md`
- Verify secrets section consistent with `rules/security-rules.md`
- Verify quality gate thresholds match `rules/testing-strategy.md`
- Reference from `info/PROJECT_INSTRUCTIONS.md` and `info/CONTRIBUTING.md`

**Generation rules:**
- ALWAYS generate — every project needs CI/CD guidance regardless of complexity
- Content is tool-agnostic (describe what, not tool-specific syntax)
- Thresholds come from AP; if AP doesn't specify, use sensible defaults and mark for team review
- Rollback section is non-negotiable regardless of AP depth
