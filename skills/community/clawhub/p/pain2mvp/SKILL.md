---
name: pain2mvp
description: Discover and structure product opportunities from public user discussions, then convert top opportunities into a lightweight PRD for a coding agent. Use when the user needs direction on what to build, or wants to find recurring pain points, unmet needs, competitor complaints, or market signals around an idea, user group, or product category.
version: 1.0.2
metadata:
  openclaw:
    install:
      - kind: brew
        formula: jq
        bins: [jq]
    skillKey: pain2mvp
    requires:
      bins:
        - node
        - npm
      env:
        - TIDB_DATABASE_URL
    primaryEnv: TIDB_DATABASE_URL
---

# Painpoint To MVP

## Modes

1. Discovery mode: find and rank product opportunities from public user discussion evidence.
2. PRD mode: turn one persisted opportunity into a lightweight PRD for a coding agent.

If the user asks for both, discovery comes first.

## Hard Rules

- `references/contracts.md` is the only runtime contract reference.
- Only inspect scripts when a documented helper command fails unexpectedly or when explicitly modifying this skill.
- Read `references/contracts.md` once per run, not repeatedly.

## Preferred Commands

Use these commands for normal operation:

- `npm run bootstrap:tidb`
- `npm run tidb -- save-evidence-batch`
- `npm run tidb -- save-opportunity-batch`
- `npm run tidb -- get-opportunity`
- `npm run tidb -- save-prd`
- `npm run tidb -- get-prd`
- `npm run tidb -- list-runs`

Compatibility-only commands:

- `npm run tidb -- save-evidence`
- `npm run tidb -- save-opportunity`

Use the single-row save commands only for manual recovery or compatibility flows.

## Normal Execution Defaults

- Check required environment once per run.
- Collect evidence first, then persist in batch.
- Prefer JSON via stdin over temp files.
- Use `--input-file` only when the payload is too large or awkward for stdin.

## Discovery Mode

1. Read `references/contracts.md` once.
2. Check required environment.
3. Collect evidence with search/scraping tools or skills (e.g. bundled websearch, meirkad/bright-data, buksan1950/reddit-readonly).
4. Persist all evidence with `save-evidence-batch`.
5. Cluster and rank opportunities using the contract rubric.
6. Persist ranked opportunities with `save-opportunity-batch`.
7. Return a ranked summary with `run_id`, `opportunity_id`, score, confidence, and caveats.

## PRD Mode

1. Resolve the target opportunity by `opportunity_id`, or by `run_id` plus rank when explicitly provided.
2. Read the persisted opportunity with `get-opportunity`.
3. Generate the PRD from the persisted opportunity and its evidence, not chat memory.
4. Persist the PRD with `save-prd`.
5. Return the human-readable PRD and include `prd_id`.

## Non-Drift Rules

- Never invent SQL. Use the documented helper commands.
- Never generate a PRD from an unpersisted opportunity summary.
- Never use conversational numbering like "opportunity #2" as the only identifier once results are persisted.
- Never claim product-market fit.
- When evidence is weak, say `insufficient evidence`.
- Preserve contradictions when sources disagree.

## Quality Bar

- Prefer repeated, concrete complaints over clever one-offs.
- Distinguish category pain from vendor-specific complaints.
- Keep evidence traceable through `source_url`, `pain_cluster_id`, and persisted identifiers.
- Optimize PRDs for a coding agent with explicit scope, non-goals, constraints, and acceptance criteria.
