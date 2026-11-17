# Recovery Standardization Pattern

## Overview

When applying a standardized change across many skills (e.g., recovery contract, OKR additions, security fixes), use this pattern:

## Step 1: Audit

For each skill, read its SKILL.md and check:
1. Does it have a `## Recovery Behavior` section referencing `spec-ocas-recovery.md`?
2. Does it have `intents.jsonl` and `evidence.jsonl` in its Storage layout?
3. Does it have `schedule_adherence` and `data_integrity` OKRs?
4. For AUDIT skills (already have recovery): verify completeness, don't duplicate

## Step 2: Prepare Patches

For each skill, prepare:
- Recovery Behavior section text (customized to skill's actual patterns)
- Storage layout additions
- OKR additions
- Empty `evidence.jsonl` and `intents.jsonl` file creation

## Step 3: Execute via Subagent Batching

Use `delegate_task` with a `tasks` array to parallelize:
- Batch 2-4 skills per subagent
- Each subagent gets: skill path, what to check, what to add
- Subagent reads SKILL.md, verifies existing content, applies patches

## Step 4: Verify

After all subagents complete:
- Spot-check a few SKILL.md files
- Verify empty data files were created
- Write summary document

## Key Pitfalls

- Don't duplicate existing content — always check first
- Customize Recovery Behavior to reference skill's actual patterns (not generic copy-paste)
- AUDIT skills need gap checks only, not full rewrites
- On-demand skills: gap detection is N/A
- Storage layout paths vary by skill (some use `{agent_root}/commons/data/`, others `<hermes-home>/data/`)
