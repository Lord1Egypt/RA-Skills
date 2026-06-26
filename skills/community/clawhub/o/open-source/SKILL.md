---
name: Open Source
slug: open-source
version: 1.0.0
homepage: https://clawic.com/skills/open-source
description: Find, evaluate, self-host, maintain, and publish open source projects with due diligence scoring, contributor workflows, and release governance.
changelog: "Initial release with discovery scoring, self-host screening, maintainer operations, and publication workflows."
metadata: {"clawdbot":{"emoji":"🌍","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/open-source/"]}}
---

## Setup

On first use, read `setup.md` silently and start helping immediately. This skill is useful from minute zero with no mandatory onboarding.

## When to Use

User needs anything around open source: finding projects, evaluating alternatives, self-hosting, contributing, maintaining, or publishing their own project. Use it when the user asks for practical decisions, not generic theory.

## Architecture

Working context lives in `~/open-source/`. Keep lightweight state and reusable notes there.

```text
~/open-source/
├── memory.md               # Current goals, stack, constraints, decisions
├── discovery-log.md        # Evaluated projects and scoring
├── roadmap.md              # Near-term maintenance and release plan
└── publishing-checklist.md # Release and distribution checkpoints
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup behavior and integration | `setup.md` |
| Memory structure and status model | `memory-template.md` |
| Discovery and ranking framework | `discovery-framework.md` |
| Self-host evaluation matrix | `self-host-screen.md` |
| Maintainer operations cadence | `maintainer-ops.md` |
| Publication and launch workflow | `publishing-playbook.md` |

## Core Rules

### 1. Build an Intent Map Before Recommending
- Start from user context: use case, stack, budget, team size, risk tolerance, and time horizon.
- If key constraints are missing, ask the minimum clarifier needed to avoid bad recommendations.
- Default output shape: shortlist, trade-offs, recommended next action.

### 2. Score Projects with Verifiable Signals
- Use `discovery-framework.md` to score each candidate on maintenance health, adoption, security posture, extensibility, and operational burden.
- Prefer projects with active maintainers, documented release cadence, and issue response discipline.
- Flag uncertainty explicitly when data is incomplete.

### 3. Separate Use Paths: Consume, Contribute, or Fork
- For consumption, optimize for reliability and migration safety.
- For contribution, optimize for governance quality and contributor experience.
- For fork decisions, require a clear business or architectural reason plus maintenance capacity.

### 4. Treat Self-Host as an Operations Commitment
- Run `self-host-screen.md` before proposing self-host by default.
- Require explicit discussion of backups, upgrades, observability, and incident ownership.
- If operational ownership is weak, recommend managed alternatives or phased rollout.

### 5. Run Maintainer Work in a Predictable Cadence
- Use `maintainer-ops.md` to structure triage, review, release, and deprecation work.
- Keep changelogs user-facing and avoid internal ranking language.
- Prefer small frequent releases over irregular large drops.

### 6. Publish with a Release Contract
- Use `publishing-playbook.md` for licensing, docs, versioning, distribution, and announcement readiness.
- Never publish without clear install path, compatibility notes, and rollback strategy.
- Announce what changed, who is affected, and how to upgrade safely.

### 7. Preserve Trust and Legal Hygiene
- Do not invent license interpretations. If licensing is unclear, state assumptions and advise legal review.
- Never recommend copying code into incompatible license contexts without warning.
- Distinguish opinion from evidence in all recommendation summaries.

## Open Source Traps

- Popularity-only selection: high stars without maintainer health leads to dead-end dependencies.
- "Self-host is always better": ignores hidden ops cost, on-call load, and security burden.
- Drive-by contributions: submitting PRs without project norms wastes maintainer time.
- Release without migration notes: breaks trust and increases support debt.
- Fork-by-frustration: temporary annoyance creates long-term maintenance tax.

## Security & Privacy

**Data that leaves your machine:**
- None by default from this skill definition.

**Data that stays local:**
- Optional working artifacts and notes in `~/open-source/` when the user asks to persist context.

**This skill does NOT:**
- Execute hidden network requests.
- Access unrelated local paths outside task scope.
- Auto-publish repositories or releases without explicit user intent.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `self-host` - Deploy and operate self-hosted services with security and reliability basics.
- `docker` - Build and run containerized workloads with practical operations guidance.
- `devops` - Structure delivery, automation, and operational workflows end to end.
- `git` - Manage repository workflows, branching, and change control safely.

## Feedback

- If useful: `clawhub star open-source`
- Stay updated: `clawhub sync`
