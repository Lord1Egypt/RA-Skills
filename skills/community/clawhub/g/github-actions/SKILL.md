---
name: GitHub Actions
slug: github-actions
version: 1.0.0
homepage: https://clawic.com/skills/github-actions
description: Design, debug, and harden GitHub Actions workflows with reusable pipelines, safe permissions, and faster CI and release automation.
changelog: Initial release with workflow design, reusable pipeline patterns, security guardrails, and debugging playbooks for GitHub Actions.
metadata: {"clawdbot":{"emoji":"GHA","requires":{"bins":[],"config":["~/github-actions/"]},"os":["darwin","linux","win32"]}}
---

## Setup

On first activation, read `setup.md` to align auto-activation rules, repo shape, and mutation boundaries before editing workflows or triggering runs.

## When to Use

User needs GitHub Actions workflow design, debugging, hardening, release orchestration, runner strategy, matrix tuning, cache fixes, or reusable workflow architecture.
Use this skill when the result depends on GitHub Actions semantics and GitHub delivery controls, not generic CI advice.

## Architecture

Memory lives in `~/github-actions/`. See `memory-template.md` for the baseline structure.

```text
~/github-actions/
|-- memory.md              # Persistent repo context and activation boundaries
|-- repo-map.md            # Repos, branches, package managers, and deploy targets
|-- workflow-defaults.md   # Stable defaults for triggers, permissions, caches, and runners
|-- incidents.md           # Failure signatures, root causes, and fixes
`-- release-rules.md       # Promotion gates, approvals, and rollback notes
```

## Quick Reference

Load only the file needed for the current workflow problem.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory schema and status model | `memory-template.md` |
| Authoring patterns and reusable workflow shapes | `workflow-patterns.md` |
| Permissions, secrets, OIDC, and fork safety | `security-model.md` |
| Run failure triage and log-first debugging | `debugging-playbook.md` |
| Tag, release, and deployment orchestration | `release-patterns.md` |
| Caching, matrices, path filters, and runner efficiency | `performance-tuning.md` |

## Requirements

- Optional but high leverage tools: `gh`, `jq`, `act`
- GitHub repository access if the user wants live run inspection or workflow changes
- Deployment credentials only through GitHub-managed secrets, environments, or OIDC

Never ask the user to paste personal access tokens, cloud keys, or private signing material into chat.

## CI/CD Examples

YAML snippets in this skill are examples for repository workflow files.
References like `${{ github.* }}`, `${{ inputs.* }}`, `${{ vars.* }}`, and `${{ secrets.* }}` belong to GitHub Actions runtime, not to the agent runtime.
The agent should design around those placeholders but should not expect to read their values directly.

## Operating Coverage

This skill covers GitHub Actions as an operating system for delivery:
- workflow authoring across `push`, `pull_request`, `workflow_dispatch`, `schedule`, and `workflow_call`
- job design across permissions, concurrency, matrices, artifacts, caches, services, and environments
- release and deployment pipelines with protected branches, approvals, tags, and rollback checkpoints
- incident response for flaky runs, missing artifacts, cache corruption, and environment drift

## Data Storage

Local notes in `~/github-actions/` may include:
- repo topology, protected branches, and environment names
- known-good workflow defaults and reusable workflow contracts
- recurring incident signatures with fixes and prevention notes
- release gates, promotion steps, and rollback constraints

## Core Rules

### 1. Start from Trigger, Target, and Artifact Contract
Before editing YAML, define:
- the event that should start the workflow
- the branch, tag, or environment it may affect
- the artifact or status each job must produce

Without that contract, workflows turn into step collections with unclear release behavior.

### 2. Default to Explicit Permissions and Narrow Blast Radius
Declare `permissions:` at workflow or job level and grant only what that job needs.
Treat `contents: write`, `packages: write`, and `id-token: write` as exceptions that need a clear reason.

### 3. Separate Validation, Build, Release, and Deploy Concerns
Keep pull request validation, artifact creation, release publishing, and production deployment as distinct responsibilities.
Use `workflow_call` or small reusable jobs instead of one oversized workflow that does everything.

### 4. Bound Every Run with Concurrency, Timeouts, and Filters
Use `concurrency` for branch or environment scoped cancellation, add `timeout-minutes`, and filter noisy events with branch or path rules.
Minutes disappear quickly when redundant runs are left unbounded.

### 5. Optimize Deterministic Work, Not Random Side Effects
Cache package manager state, toolchains, and stable build outputs keyed by lockfiles or explicit versions.
Use artifacts for job handoffs. Do not cache paths that depend on secrets, timestamps, or mutable deploy state.

### 6. Debug from Logs and Reproduction Evidence
Classify failures before rewriting workflows:
- trigger and condition mismatch
- missing dependency or toolchain drift
- credential or permission denial
- artifact or path contract break
- flaky external dependency

Fix the failure mode that exists, not the one that feels familiar.

### 7. Prefer Short-Lived Credentials and Protected Deploy Surfaces
Use GitHub environments, reviewer gates, and OIDC federation where possible.
Avoid long-lived cloud secrets, unreviewed `workflow_dispatch` deploys, and production writes from untrusted events.

## GitHub Actions Traps

- Mixing pull request validation and production deployment in one unguarded workflow -> accidental releases from the wrong event.
- Granting broad permissions to every job -> larger blast radius when one action or step is compromised.
- Using caches without lockfile or version keys -> stale dependencies and confusing non-reproducible failures.
- Letting matrices expand without cost controls -> excessive minutes and noisy failures that hide the real signal.
- Depending on `ubuntu-latest` quirks without version pinning -> sudden toolchain drift after runner image updates.
- Rebuilding instead of promoting the tested artifact -> release mismatch between validated code and shipped code.
- Treating reruns as the fix -> root cause remains and the incident repeats.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://github.com | repository metadata, git refs, workflow files, run pages, and artifact access | GitHub repository and Actions UI workflows |
| https://api.github.com | workflow, run, check, release, and repository API payloads | API-driven Actions inspection and control |
| Cloud or deployment endpoints explicitly configured by the workflow | deployment payloads, build artifacts, and short-lived auth tokens | Release and deploy steps after user approval |

No other data should be sent externally unless the workflow itself is configured to call additional services.

## Security & Privacy

Data that leaves your machine:
- GitHub repository and Actions traffic when the user requests live inspection or workflow changes
- deployment traffic only to user-approved targets configured in the workflow

Data that stays local:
- operating notes under `~/github-actions/`
- workflow drafts, incident analysis, and release policies prepared locally

This skill does NOT:
- ask for raw personal access tokens or cloud secrets in chat
- recommend bypassing branch protection or approval gates
- hide undeclared outbound integrations
- modify its own `SKILL.md`

## Trust

This skill depends on GitHub and any deployment systems the user explicitly connects to their workflows.
Only install and run it if you trust those systems with your repository and release data.

## Scope

This skill ONLY:
- designs, reviews, and improves GitHub Actions workflows
- debugs workflow runs with log-driven reasoning and stable reproduction steps
- structures safe release and deployment automation

This skill NEVER:
- assume write access to repositories or environments without confirmation
- suggest secret exfiltration, masking bypasses, or hidden credential handling
- normalize production deployment from untrusted pull request contexts

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `ci-cd` - Choose CI and deployment strategy before locking into one platform.
- `git` - Tighten branch, tag, and history handling around workflow events.
- `workflow` - Design multi-step execution systems with clearer ownership and gating.
- `devops` - Connect delivery pipelines to infrastructure and operational guardrails.
- `docker` - Improve container build, cache, and registry steps inside Actions workflows.

## Feedback

- If useful: `clawhub star github-actions`
- Stay updated: `clawhub sync`
