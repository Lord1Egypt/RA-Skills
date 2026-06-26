---
name: openclaw-usage-dashboard
description: Interactive local dashboard for OpenClaw API usage. Shows token consumption, request counts, and system health across all configured LLM models — broken down by model, agent, and time period (hour/day/week/month/year). Reads session logs directly; no external service needed, data stays local. Use when a user asks about token usage, model activity, how many requests were made, usage by agent, system health, or wants a usage overview. Triggers on "usage dashboard", "token usage", "how many requests", "model usage", "usage by agent", "usage stats", "system health", "ram usage".
---

# OpenClaw Usage Dashboard

A zero-dependency Node.js dashboard that reads your OpenClaw session logs and shows token usage, model activity, and system health in real time. Runs entirely on localhost — no data ever leaves your machine.

## Usage

```bash
node server.js
```

Open **http://localhost:7842** in your browser.

### Custom port

```bash
node server.js --port 8080
```

## What It Shows

- **Timeline chart** — requests over time with Models / Agents / Both filter toggle
- **Model cards** — token counts and request counts per model, sorted by most used
- **Agent activity** — breakdown of requests per agent
- **Session heatmap** — activity distribution by hour of day
- **Token efficiency** — cache hit ratio and average prompt size
- **System health** — RAM (VM-aware on macOS), disk, uptime, OpenClaw version
- **Period selector** — Hour / Day / Week / Month / Year (keyboard shortcuts `1`–`5`)

## Requirements

- Node.js 18+ (no `npm install` needed — zero external dependencies)
- OpenClaw session logs at `~/.openclaw/agents/*/sessions/*.jsonl`

## Platform Support

| Platform | Supported |
|----------|-----------|
| macOS    | ✅        |
| Linux    | ✅        |
| Windows  | ✅        |
