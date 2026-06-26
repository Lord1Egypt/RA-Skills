---
name: percept-meetings
description: "Give your OpenClaw agent context from meetings captured by Zoom, Granola, or Omi wearables. Search transcripts, extract action items, identify speakers, and act on meeting outcomes. Use when the user asks about meetings, what was discussed, action items, follow-ups, who said what, meeting summaries, or when the agent needs meeting context to complete a task. Also triggers for: what did we talk about, meeting notes, transcript, action items, follow up on, schedule based on our meeting, what did [person] say."
---

# Percept Meetings

Give your OpenClaw agent ears. This skill connects meeting data from **Zoom**, **Granola**, and **Omi wearables** into your agent's context — searchable transcripts, speaker identification, entity extraction, and actionable follow-ups.

## Quick Start

### 1. Install Percept

```bash
pip install getpercept   # or: git clone https://github.com/GetPercept/percept
cd percept && pip install -e .
```

### 2. Connect a Source

**Granola** (zero config — reads local cache):
```bash
percept granola-sync
```

**Zoom** (needs OAuth app):
```bash
export ZOOM_ACCOUNT_ID=xxx ZOOM_CLIENT_ID=xxx ZOOM_CLIENT_SECRET=xxx
percept zoom-sync --days 7
```

**Omi wearable** (real-time):
```bash
percept serve --port 8900
# Configure Omi webhook → https://your-host:8900/webhook/transcript?token=YOUR_TOKEN
```

### 3. Use Meeting Context

Search what was discussed:
```bash
percept search "budget approval"
```

List recent transcripts:
```bash
percept transcripts --today
```

Check who was in meetings:
```bash
percept speakers
```

Get action items from latest meeting:
```bash
percept actions
```

## How to Use in Agent Workflows

### Finding Meeting Context

When the user asks about meetings or you need context from a past conversation:

```bash
# Search by topic
percept search "VectorCare API migration"

# Search by person
percept search "what did Sarah say"

# Recent meetings
percept transcripts --limit 5
```

Output is JSON — parse it for structured data.

### Acting on Meetings

When meetings produce action items or follow-ups:

1. Search for the relevant meeting: `percept search "<topic>"`
2. Extract action items from the transcript
3. Use other OpenClaw tools to execute (send emails, create tasks, schedule follow-ups)

Example flow: User says "follow up on what we discussed with the sales team"
→ `percept search "sales team"` → find action items → draft follow-up email

### Importing New Data

**Granola** auto-discovers meetings from `~/Library/Application Support/Granola/cache-v3.json`.
Run `percept granola-sync` to pull latest. Supports `--since YYYY-MM-DD` for date filtering.

**Zoom** requires a Server-to-Server OAuth app from marketplace.zoom.us:
- Scopes needed: `recording:read`, `user:read`
- Run `percept zoom-sync` to batch-import, or start webhook server for auto-import
- See [references/zoom-setup.md](references/zoom-setup.md) for detailed setup

**Omi** streams in real-time via webhook. See [references/omi-setup.md](references/omi-setup.md).

## Configuration

Percept stores data in `percept/data/percept.db` (SQLite with FTS5 full-text search).

Key env vars:
- `PERCEPT_DB_PATH` — custom database location
- `PERCEPT_API_TOKEN` — bearer token for API endpoints
- `ZOOM_ACCOUNT_ID`, `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET` — Zoom OAuth
- `GRANOLA_API_KEY` — Granola Enterprise API (optional; local cache works without it)

## Pipeline Health

```bash
percept status
```

Returns: server status, live stream status, today's conversation count, database stats.
