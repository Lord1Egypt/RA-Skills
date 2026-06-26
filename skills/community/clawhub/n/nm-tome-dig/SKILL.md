---
name: dig
description: |
  Refines an active research session by drilling deeper into a subtopic. Use after tome:research to narrow results to a specific channel or angle
version: 1.9.8
triggers:
  - refinement
  - interactive
  - drill-down
metadata: {"openclaw": {"homepage": "https://github.com/athola/claude-night-market/tree/master/plugins/tome", "emoji": "\ud83e\udd9e"}}
source: claude-night-market
source_plugin: tome
---

> **Night Market Skill** — ported from [claude-night-market/tome](https://github.com/athola/claude-night-market/tree/master/plugins/tome). For the full experience with agents, hooks, and commands, install the Claude Code plugin.


# Dig Deeper

## When To Use

- Drilling into a subtopic after an initial research session
- Narrowing results to a specific channel (e.g. papers only)

## When NOT To Use

- Starting a new research topic (use `/tome:research` first)
- Synthesizing results (use `/tome:synthesize`)

Refine an active research session interactively.

## Workflow

1. Load most recent session via SessionManager
2. Parse the subtopic and optional channel filter
3. Dispatch targeted search (single agent or all channels)
4. Merge new findings into existing session
5. Re-rank and update the saved report
6. Present new findings to user

## Error Cases

- No active session: "Start a session first with
  `/tome:research \"topic\"`"
- Specified channel not in original session: warn and
  suggest available channels
