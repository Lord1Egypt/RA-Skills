<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: generated
---
# Template: PROJECT_INSTRUCTIONS.md

```markdown
<!-- AI-DWG generated | source: Multiple AP artifacts | date: {generation-date} -->

# Project Instructions — {System Name}

## Quick Start

1. Clone: `git clone {repo-url}`
2. Copy `.env.example` → `.env` (fill in local values)
3. Infrastructure: `docker compose up -d`
4. Install: `{install-command}`
5. Migrate: `{migrate-command}`
6. Run: `{dev-command}`
7. Verify: open `{local-url}`

## Architecture at a Glance

{2-3 sentences from Architecture Vision}

**Stack:** {primary tech}  |  **Style:** {architecture style}  |  **Modules:** {count}

## Development Rules

All rules in `rules/`. Must-read files:

| File | Governs |
|------|---------|
| workspace-rules.md | Golden rules (read first) |
| coding-standards.md | Code patterns |
| module-structure.md | Module boundaries |
| api-standards.md | API conventions |
| database-rules.md | Schema + query rules |
| git-workflow.md | Branching + commits |
| testing-strategy.md | Test requirements |
| domain-context.md | Domain vocabulary |

## How to Contribute

→ [CONTRIBUTING.md](./CONTRIBUTING.md)

## New to the Team?

→ [ONBOARDING.md](./ONBOARDING.md)

## Key Commands

| Command | Purpose |
|---------|---------|
| `{install}` | Install dependencies |
| `{dev}` | Dev server |
| `{test}` | Run tests |
| `{lint}` | Lint code |
| `{build}` | Build |
| `docker compose up -d` | Start infrastructure |
| `{migrate}` | Run migrations |

## Architecture Decisions

ADRs document design rationale. Located at: `{adr-path}`
```

## Filling: Refer to `mapping/governance-derivation.md` (Target 1).
