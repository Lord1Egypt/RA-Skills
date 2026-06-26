# Vault Structure Template

A starter vault layout optimized for human-agent collaboration. Adapt to your domain.

## Recommended Layout

```
vault/
  _context/                  # Orchestration (agent state)
    status.md                # What's active, blocked, completed
    tasks.md                 # Prioritized task list
    decisions.md             # Decision log with rationale
    context-map.md           # Project-to-file index
    scratchpad.md            # Working memory (clear daily)
    learnings.md             # Operational knowledge

  foundations/               # Cross-project strategy
    product-vision.md
    roadmap.md
    architecture.md

  product/                   # Product-specific
    features/
    sprints/
    design/
    engineering/

  company/                   # Operations
    customer-discovery/
    market-research/
    legal/                   # Read-only for agent
    marketing/
    hiring/

  research/                  # Technical research
    analysis/
    experiments/

  journal/                   # Session history
    sessions/                # Per-session handoff logs
    weekly/                  # Weekly reviews

  decisions/                 # Formal decision records

  work/                      # Agent output
    drafts/                  # In-progress work
    research/                # Research briefs
    output/                  # Polished deliverables

  archive/                   # Superseded files
```

## Naming Conventions

- Folders: `lowercase-kebab-case`
- Files: `lowercase-kebab-case.md`
- Dates in filenames: `YYYY-MM-DD` prefix (e.g., `2026-03-25-session-1.md`)

## Frontmatter Standard

Every active document should include:

```yaml
---
title: "Document Title"
type: spec | research | decision | article | note
status: draft | active | stale | archived
project: product | engine | company | foundations
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - relevant-tag
---
```

## Folder Semantics

The folder a file lives in carries semantic meaning. The agent uses this for context:

| Location | Agent Interprets As |
|----------|-------------------|
| `product/sprints/` | Current development work |
| `product/features/` | Feature specifications |
| `company/legal/` | Sensitive, read-only |
| `company/customer-discovery/` | User research and interview data |
| `research/` | Technical investigation, not yet productized |
| `decisions/` | Past choices with rationale (institutional memory) |
| `work/drafts/` | Agent's in-progress output |
| `work/output/` | Agent's polished deliverables |
| `archive/` | Historical, low-priority for active work |

## Adapting for Your Domain

This template assumes a software product company. Adapt the middle layer:

**Consulting firm:**
Replace `product/` with `clients/`, `research/` with `frameworks/`, add `proposals/`.

**Content creator:**
Replace `product/` with `content/`, add `ideas/`, `published/`, `newsletter/`.

**Research lab:**
Replace `product/` with `projects/`, expand `research/` into subdomains.

The `_context/`, `journal/`, `decisions/`, `work/`, and `archive/` layers stay the same regardless of domain. They're about collaboration patterns, not subject matter.
