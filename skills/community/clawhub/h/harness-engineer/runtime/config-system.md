# CONFIGURATION SYSTEM

Multi-layer configuration with deep merge. Later sources override earlier ones.

## CONFIG PRIORITY (lowest to highest)

| Priority | Source | Location | Notes |
|----------|--------|----------|-------|
| 1 (lowest) | Skill defaults | Embedded in skill .md files | Always present |
| 2 | User settings | ~/.harness/settings.json | User-level preferences |
| 3 | Project settings | .harness/settings.json | Committed to repo |
| 4 (highest) | Local override | .harness/settings.local.json | Gitignored |
| 5 | Environment | HARNESS_* env vars | Runtime overrides |

## DEEP MERGE ALGORITHM

When multiple sources define the same key:
- Objects: merge recursively (combine keys from all sources)
- Arrays: highest-priority source wins (array replaced, not concatenated)
- Scalars: highest-priority source wins
- Unknown keys in settings files: log warning, preserve

Example:
  Source 1 (skill): { max_parallel_agents: 3, loop_mode: "single-pass" }
  Source 3 (project): { max_parallel_agents: 5 }
  Result: { max_parallel_agents: 5, loop_mode: "single-pass" }

## SCHEMA

Supported keys in settings files:
  loop_mode: "single-pass" | "continuous"
  max_parallel_agents: number
  gc_interval: number (cycles)
  cost.per_cycle_budget_usd: number
  cost.model_tier: "haiku" | "sonnet" | "opus"
  block_destructive_commands: boolean

Unknown keys are preserved (forward-compatible) but logged as warnings.

## OVERRIDE EXAMPLE

To override max_parallel_agents for a specific project without affecting global config:
  1. Create .harness/settings.json in the project root:
     { "max_parallel_agents": 6 }
  2. Commit to repo (team-level setting)
  3. For local-only override: use .harness/settings.local.json (gitignored)
