---
name: synthesize
description: |
  Merges, dedupes, ranks, and formats research findings into a report. Use after research agents return results from multiple channels to produce a ranked report
version: 1.9.8
triggers:
  - merge
  - rank
  - format
  - report
metadata: {"openclaw": {"homepage": "https://github.com/athola/claude-night-market/tree/master/plugins/tome", "emoji": "\ud83e\udd9e"}}
source: claude-night-market
source_plugin: tome
---

> **Night Market Skill** — ported from [claude-night-market/tome](https://github.com/athola/claude-night-market/tree/master/plugins/tome). For the full experience with agents, hooks, and commands, install the Claude Code plugin.


# Finding Synthesis

## When To Use

- After research agents return results from multiple channels
- Producing a final ranked report from raw findings

## When NOT To Use

- No research session is active (run `/tome:research` first)
- Refining a single channel (use `/tome:dig` instead)

Merge findings from all channels into a ranked report.

## Workflow

1. Merge: `tome.synthesis.merger.merge_findings()`
2. Rank: `tome.synthesis.ranker.rank_findings()`
3. Group: `tome.synthesis.ranker.group_by_theme()`
4. Format: `tome.output.report.format_report()`

## Output Formats

- **report**: Full sectioned markdown
- **brief**: Condensed 1-2 pages
- **transcript**: Raw session log
