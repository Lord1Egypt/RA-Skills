---
name: per-agent-compression-universal
version: 1.4.0
description: Zero-config memory consolidation for multi-agent OpenClaw deployments. Auto-discovers agents and registers staggered cron tasks with full state tracking, deduplication, and domain-aware extraction.
author: OpenClaw CTO
license: MIT
tags:
  - memory
  - automation
  - cron
  - compression
  - multi-agent
capabilities:
  - memory-consolidation
  - workspace-isolation
  - agent-auto-discovery
  - state-persistence
  - deduplication
entry:
  type: installer
  installScript: install.sh
  uninstallScript: uninstall.sh
  postInstallMessage: Per-agent compression tasks registered for all discovered agents with full state tracking and deduplication. Note: Skill is in active testing; see README for limitations and manual verification steps.
---

# Per-Agent Memory Compression Skill

## Overview

This skill automates weekly memory consolidation for multi-agent OpenClaw deployments. It discovers all agents with workspaces and registers staggered cron tasks that compress old daily notes into long-term memory files.

## Key Features

- **Auto-discovery**: Finds all agents via `openclaw agents list`
- **Workspace isolation**: Each agent compresses its own memory
- **State persistence**: Tracks processed notes in `.compression_state.json`
- **Deduplication**: Avoids duplicate entries
- **Domain awareness**: Includes DOMAIN_CONTEXT for tailored extraction
- **Zero config**: Just run `./install.sh`

## Installation

```bash
cd /root/.openclaw/workspace/skills/per-agent-compression-universal
./install.sh
```

This creates 5 staggered tasks (if you have 5 agents) running Sundays 03:00-05:00 Shanghai time.

## What It Does

1. Pre-check paths and initialize state
2. List daily notes older than 7 days (skip recent)
3. Sort oldest first, process up to 5 notes per run
4. For each note:
   - Read content
   - Extract factual info (preferences, decisions, personal info)
   - Append to target files with date headers
   - Move original to `memory/processed/`
5. Update state file
6. Clean working buffer
7. Send DingTalk summary

## File Structure

Each agent workspace should have:
- `memory/YYYY-MM-DD.md` (daily notes)
- `USER.md`, `IDENTITY.md`, `SOUL.md`, `MEMORY.md` (targets)

After running:
- `memory/.compression_state.json` (state tracking)
- `memory/processed/` (moved old notes)

## Customization

Edit `install.sh` to adjust:
- Stagger offsets (`OFFSETS` array)
- Domain context per agent (`DOMAIN_CONTEXT` associative array)
- Cron expression (currently Sundays)

## Troubleshooting

- **Task hangs**: Check STATE_FILE path uses `{WORKSPACE}` (uppercase), not `{workspace}`
- **No notes processed**: Ensure there are daily notes older than 7 days
- **Timeout**: Increase `--timeout` in install.sh (default 1200s)
- **Delivery fails**: Verify DingTalk connector configured with `to` field

## Uninstall

```bash
./uninstall.sh
```

Removes all `per_agent_compression_*` tasks.

## Version

Current: 1.3.4 (fixes STATE_FILE case sensitivity bug)

## Support

See README.md for full documentation.
