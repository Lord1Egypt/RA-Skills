---
name: openclaw-dreaming-setup
description: Configure and manage OpenClaw Dreaming — background memory consolidation, auto-promotion to MEMORY.md, dream diary
version: 1.0.0
tags:
  - openclaw
  - dreaming
  - memory
  - automation
  - memory-core
---

# OpenClaw Dreaming Setup

Configure and manage OpenClaw's Dreaming system — the background memory consolidation that promotes short-term notes into long-term `MEMORY.md`.

## When to Use

- User wants to enable/configure Dreaming for automatic memory consolidation
- Checking dreaming status, phase health, or promotion history
- Troubleshooting blocked dreaming or heartbeat issues
- Managing dream diary (DREAMS.md)
- Manual memory promotion or backfill

## What is Dreaming?

Dreaming automatically:
1. **Light phase** — stages recent daily notes and session transcripts
2. **REM phase** — extracts patterns and recurring themes
3. **Deep phase** — promotes strong signals into `MEMORY.md`

It runs as a background cron job tied to heartbeat.

## Quick Setup

### Enable Dreaming

Add to `openclaw.json`:

```json5
{
  plugins: {
    entries: {
      "memory-core": {
        config: {
          dreaming: {
            enabled: true,
            // Optional: custom schedule (default: 03:00 daily)
            frequency: "0 3 * * *",
            timezone: "Asia/Jerusalem",
          },
        },
      },
    },
  },
}
```

Then restart gateway: `openclaw gateway restart`

### With Skill Workshop (recommended combo)

```json5
{
  plugins: {
    entries: {
      "memory-core": {
        config: {
          dreaming: {
            enabled: true,
          },
        },
      },
      "skill-workshop": {
        enabled: true,
        config: {
          autoCapture: true,
          approvalPolicy: "pending",
          reviewMode: "hybrid",
        },
      },
    },
  },
}
```

### With Active Memory

```json5
{
  plugins: {
    entries: {
      "active-memory": {
        enabled: true,
        config: {
          enabled: true,
          agents: ["main"],
          allowedChatTypes: ["direct"],
          modelFallback: "zai/glm-5-turbo",
          queryMode: "recent",
          promptStyle: "balanced",
          timeoutMs: 15000,
        },
      },
      "memory-core": {
        config: {
          dreaming: { enabled: true },
        },
      },
    },
  },
}
```

## Commands Reference

### Check Status

```bash
# Via slash command (in chat)
/dreaming status

# Via CLI
openclaw memory status --deep
```

### Manual Promotion

```bash
# Preview what would be promoted
openclaw memory promote

# Apply promotion
openclaw memory promote --apply

# Limit candidates
openclaw memory promote --limit 5

# Explain why a specific topic would/wouldn't promote
openclaw memory promote-explain "claw-earn wallet"
```

### Dream Diary

```bash
# View dream diary
cat ~/openclaw-data/workspace/DREAMS.md

# View specific phase reports
ls ~/openclaw-data/workspace/memory/dreaming/
cat ~/openclaw-data/workspace/memory/dreaming/deep/2026-04-24.md
```

### REM Harness (preview without writing)

```bash
# Preview REM reflections
openclaw memory rem-harness

# Preview as JSON
openclaw memory rem-harness --json
```

### Historical Backfill

```bash
# Preview grounded diary from past notes
openclaw memory rem-harness --path memory/2026-04-23.md --grounded

# Apply backfill
openclaw memory rem-backfill --path memory/2026-04-23.md

# Stage for deep promotion
openclaw memory rem-backfill --path memory/2026-04-23.md --stage-short-term

# Rollback if needed
openclaw memory rem-backfill --rollback
```

## Dreaming Phase Model

| Phase | Purpose | Writes to MEMORY.md? |
|-------|---------|---------------------|
| Light | Sort and stage recent notes | No |
| REM | Extract patterns and themes | No |
| Deep | Promote strong candidates | **Yes** |

Deep ranking signals:
- Frequency (0.24) — how often the topic appears
- Relevance (0.30) — retrieval quality
- Query diversity (0.15) — different contexts
- Recency (0.15) — time-decayed freshness
- Consolidation (0.10) — multi-day recurrence
- Conceptual richness (0.06) — tag density

## Troubleshooting

| Problem | Check |
|---------|-------|
| Dreaming never runs | `heartbeat.every` must be > 0 (e.g., `30m`) |
| Status shows "blocked" | Default agent needs heartbeat enabled |
| No promotions | Need more daily notes and variety |
| MEMORY.md growing too fast | Adjust `minScore` threshold |

### Heartbeat dependency

Dreaming rides the default agent's heartbeat. If heartbeat is broken:
1. Check `agents.defaults.heartbeat.every` — must be positive (e.g., `"30m"`)
2. Don't override heartbeat on a specific agent without including the default
3. `/dreaming status` will say "blocked" if heartbeat is missing

## Important Notes

- Dreaming is opt-in and disabled by default
- Default schedule: 03:00 daily (configurable via `frequency`)
- Only grounded memory snippets are promoted, not diary entries
- `DREAMS.md` is for human reading; `MEMORY.md` is for the agent
- Promotion is reversible via `--rollback`
