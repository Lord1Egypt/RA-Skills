---
name: memory-dreaming
description: "Autonomous memory consolidation for OpenClaw agents — like REM sleep. Periodically gathers signal from daily logs, session transcripts, and learnings; consolidates into MEMORY.md; syncs structured knowledge to an Obsidian vault (or any markdown knowledge base); tracks plans; prunes stale entries. Use when: (1) setting up periodic memory maintenance, (2) manually triggering a dream cycle, (3) configuring Obsidian vault sync, (4) agent memory is getting noisy/contradictory and needs consolidation."
---

# Memory Dreaming

Autonomous memory consolidation ("dreaming") for OpenClaw agents. Runs as a cron job, consolidates scattered daily notes into curated long-term memory, and syncs structured knowledge to an Obsidian vault.

## Quick Start

1. Install: `clawhub install oryanmoshe/memory-dreaming`
2. Configure your vault path (optional): edit `dreaming-config.json` in your workspace
3. Set up the cron: run `scripts/setup-cron.sh`
4. Done — the agent dreams automatically every 8 hours

To trigger a dream manually, tell the agent: "Run a dream cycle now."

## How It Works

The dream cycle has 4 phases, inspired by biological REM sleep and Claude Code's AutoDream:

### Phase 1: Orient
Read current memory state — MEMORY.md, recent daily logs, learnings, dreaming log. Build a map of what exists and when it was last touched.

### Phase 2: Gather Signal
Search for high-value information added since the last dream:
- **Daily logs** (`memory/YYYY-MM-DD.md`) since last dream
- **Learnings** (`.learnings/*.md`) — pending corrections, errors, best practices
- **Session transcripts** — grep for corrections ("actually...", "no that's wrong"), decisions ("let's do X"), proper nouns, preferences
- **Plan files** — scan workspace for `task_plan.md` files

Key: grep narrowly for high-signal patterns. Don't read full transcripts — that burns tokens for marginal value.

### Phase 3: Consolidate
Update MEMORY.md with gathered signal:
- **Merge** duplicate entries (same fact from 3 sessions → one entry)
- **Absolute dates** — convert "yesterday" → "2026-03-25"
- **Delete** contradicted facts (if preference changed, remove old one)
- **Remove** stale entries (references to deleted files, completed tasks)
- **Promote** high-priority learnings from `.learnings/` to MEMORY.md

### Phase 4: Sync
Push consolidated knowledge to external targets:
- **Obsidian vault** (opt-in) — create/update notes with tags, wikilinks, full depth
- **Plan tracking** — ensure every `task_plan.md` has a corresponding `Plans/<name>.md` in the vault
- **Dreaming log** — write what changed, tokens used, duration

## Gate

The cron fires on schedule but the dream cycle only executes if **≥6 hours** have passed since the last dream (checked via `dreaming-log.md` timestamp). This prevents wasted runs when nothing has changed.

## Configuration

Create `dreaming-config.json` in your workspace root to customize. All fields are optional — sensible defaults are used.

See `assets/dreaming-config.json` for the full schema with defaults.

Key options:
- `schedule` — cron expression (default: `"0 */8 * * *"`)
- `model` — which model runs the dream (default: `"anthropic/claude-sonnet-4-6"`)
- `gate.minHours` — minimum hours between dreams (default: `6`)
- `obsidian.enabled` — enable vault sync (default: `false`)
- `obsidian.vaultPath` — absolute path to Obsidian vault
- `delivery.mode` — `"none"` or `"announce"` changes to a channel

## Obsidian Sync Details

When enabled, the sync phase:
1. Compares MEMORY.md sections against existing vault notes
2. Creates new notes in configured subfolders (`People/`, `Projects/`, `Plans/`, `Tools/`)
3. Updates existing notes with new information (appends, doesn't overwrite)
4. Follows formatting rules: tags on first line, `[[wikilinks]]` throughout, full depth content
5. Tracks plans: scans for `task_plan.md` files → creates/updates `Plans/<name>.md`

For detailed sync behavior, see `references/obsidian-sync.md`.

## Manual Dream

Tell the agent any of these:
- "Run a dream cycle"
- "Consolidate memory"
- "Dream now"
- "Sync to obsidian"

The agent reads this skill and executes the 4-phase cycle immediately, ignoring the gate.

## Setup Script

```bash
# Creates the cron job in OpenClaw
bash scripts/setup-cron.sh
```

The script reads `dreaming-config.json` (or uses defaults) and creates an isolated agentTurn cron job. See `scripts/setup-cron.sh` for details.

## Architecture

For the detailed 4-phase architecture, design decisions, and how this compares to Claude Code AutoDream, see `references/architecture.md`.

## What This Skill Does NOT Do

- Does not replace QMD indexing (QMD handles search, this handles consolidation)
- Does not delete source files (daily logs are never removed, only consolidated from)
- Does not modify source code or project files
- Does not run without explicit setup (cron must be created via setup script)
