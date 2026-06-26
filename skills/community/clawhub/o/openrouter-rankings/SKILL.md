---
name: openrouter-rankings
description: Fetch and track OpenRouter AI model rankings (weekly trends, top models, top apps, market share). Use when user asks about OpenRouter rankings, AI model popularity, token usage statistics, or wants weekly automated reports.
license: MIT
---

# OpenRouter Rankings Tracker

Fetch and track OpenRouter's AI model usage rankings.

---

## Quick Start

```bash
# Fetch current rankings
node scripts/fetch.js

# With options
node scripts/fetch.js --save --push
```

---

## What It Captures

| Section | Data |
|---------|------|
| **Top Models** | Weekly token usage, growth % |
| **Top Apps** | Apps consuming most tokens |
| **Market Share** | Provider market distribution |
| **Highlights** | Fastest growing, #1 model/app |

---

## Output Format

Data saved to `~/.openclaw/data/openrouter-rankings/YYYY-MM-DD.json`

```json
{
  "fetchedAt": "2026-03-10T02:15:00.000Z",
  "source": "https://openrouter.ai/rankings",
  "period": "This Week",
  "topModels": [...],
  "marketShare": [...],
  "topApps": [...],
  "highlights": {...}
}
```

---

## Cron Integration

Set up weekly automated fetch:

```json
{
  "name": "openrouter-weekly",
  "schedule": { "kind": "cron", "expr": "0 9 * * 1" },
  "payload": { "kind": "agentTurn", "message": "Fetch OpenRouter rankings and push to Feishu" },
  "sessionTarget": "isolated"
}
```

---

## Options

| Flag | Description |
|------|-------------|
| `--save` | Save to JSON file |
| `--push` | Push to Feishu (requires config) |
| `--compare` | Compare with last week |

---

## Data Structure

See [references/data-structure.md](references/data-structure.md) for detailed schema.
