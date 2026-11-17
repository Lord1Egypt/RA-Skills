<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: git-workflow.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Infrastructure & Deployment | date: {generation-date} -->

# Git Workflow

## Branching Model
**Strategy:** {GitFlow / Trunk-Based / GitHub Flow}

<!-- begin: AP-sourced -->
| Branch | Purpose | Protected |
|--------|---------|:---------:|
| main | Production-ready | ✅ |
| {develop} | Integration | ✅ |
| feature/{ticket}-{desc} | New features | ❌ |
| bugfix/{ticket}-{desc} | Bug fixes | ❌ |
| hotfix/{ticket}-{desc} | Emergency fixes | ❌ |

| Rule | Standard |
|------|----------|
| GIT-BR-01 | Naming: {type}/{ticket-id}-{kebab-desc} |
| GIT-BR-02 | Branch from: {source branch} |
| GIT-BR-03 | Merge to: {target branch} via PR |
| GIT-BR-04 | Protected: no direct push — PR with {n} approvals |
| GIT-BR-05 | Delete after merge |
| GIT-BR-06 | Max age: {days} |
| GIT-BR-07 | Merge strategy: {squash/rebase/merge commit} |
<!-- end: AP-sourced -->

## Commit Conventions
<!-- begin: AP-sourced -->
Format: `{type}({scope}): {subject}`
Types: feat, fix, refactor, docs, test, chore, perf, ci
Scope: module name from module-structure.md

| Rule | Standard |
|------|----------|
| GIT-CMT-01 | Conventional Commits format |
| GIT-CMT-02 | Imperative, lowercase, max 72 chars |
| GIT-CMT-03 | Scope = module name |
| GIT-CMT-04 | BREAKING CHANGE in footer |
| GIT-CMT-05 | Reference ticket |
| GIT-CMT-06 | Atomic: one change per commit |
<!-- end: AP-sourced -->

## Pull Request Process
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| GIT-PR-01 | Every change via PR |
| GIT-PR-02 | Title: conventional commit format |
| GIT-PR-03 | Reviewers: {n} peer + CODEOWNER |
| GIT-PR-04 | Use PR template |
| GIT-PR-05 | CI must pass |
| GIT-PR-06 | Max size: {lines} |
<!-- end: AP-sourced -->

## CI/CD Pipeline
<!-- begin: AP-sourced -->
| Stage | Trigger | Gate |
|-------|---------|:----:|
| Lint | Every push | ✅ |
| Test | Every push | ✅ |
| Build | PR to protected | ✅ |
| Security | PR to protected | ✅ |
| Deploy staging | Merge to {branch} | — |
| Deploy production | {trigger} | ✅ Manual |
<!-- end: AP-sourced -->

## Environments
<!-- begin: AP-sourced -->
| Environment | Deployed From | Access |
|-------------|:-------------:|--------|
| Local | docker-compose | Individual |
| Staging | {branch} | Team |
| Production | {branch/tag} | Restricted |
<!-- end: AP-sourced -->

## Releases
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| GIT-REL-01 | Versioning: {SemVer} |
| GIT-REL-02 | Source of truth: {git tags} |
| GIT-REL-03 | Trigger: {tag push / manual} |
| GIT-REL-04 | Changelog: {auto/manual} |
<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/infra-to-config.md` (Target 1).
