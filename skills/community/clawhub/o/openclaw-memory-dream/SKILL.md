---
name: memory-dream
description: Auto-consolidates agent memory files after sessions — like REM sleep for AI agents. Prevents MEMORY.md from growing unbounded by using an LLM to prune stale context, resolve contradictions, and tighten what remains. Supports persistent DM channels via session-gap detection.
---

# memory-dream

Auto-consolidates agent memory files after sessions — like REM sleep for AI agents.

## What it does

As an AI agent accumulates sessions, its memory files can get cluttered: vague date references ("yesterday", "last week"), stale context that no longer applies, and contradictions where newer information superseded older entries but both remain.

**memory-dream** runs automatically in the background once enough sessions have passed and enough time has elapsed. It uses the configured LLM to quietly clean up memory files, resolving contradictions, replacing vague date references with actual dates, removing stale entries, and preserving everything that still matters.

Without it: MEMORY.md grows unbounded until it gets truncated on load.  
With it: memory stays tight, relevant, and useful automatically.

Works standalone — no other plugins required. Optionally uses [lossless-claw](https://clawhub.ai) session summaries for richer consolidation context if that plugin is also installed.

## Installation

```bash
openclaw plugins install @mitchelldavis44/openclaw-memory-dream
```

## Configuration (`openclaw.json`)

```json
{
  "plugins": {
    "entries": {
      "memory-dream": {
        "enabled": true,
        "config": {
          "minSessions": 5,
          "minHours": 24,
          "memoryFiles": ["MEMORY.md"],
          "model": "claude-haiku-4-5"
        }
      }
    }
  }
}
```

| Option | Default | Description |
|---|---|---|
| `minSessions` | `5` | Session boundaries since last consolidation before triggering |
| `minHours` | `24` | Hours since last consolidation before triggering |
| `memoryFiles` | `["MEMORY.md"]` | Memory files to consolidate (relative to workspace root) |
| `model` | *(agent default)* | LLM used for consolidation (cheap model recommended) |

Both conditions must be met before consolidation triggers.

> **Session detection in persistent channels:** In DM-style channels where there's no discrete session lifecycle (e.g. Slack DMs), the plugin detects session boundaries via inactivity gaps — a gap of 30+ minutes between messages counts as a new session.

## Status tool

```
memory_dream_status
```

Returns session count, last run time, next trigger estimate, and whether consolidation is currently running.
