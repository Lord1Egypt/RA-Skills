# OpenClaw Tally

> Tokens tell you how much you paid. Tasks tell you what you got.

**Task-level efficiency analytics for OpenClaw.** Stop counting tokens — start measuring what actually got done and what it cost.

## 🛠️ Installation

Install the owner-qualified release:
```bash
openclaw skills install @jonathanjing/openclaw-tally
```

## Quick Start

```bash
# Requires Node.js 22+

# 1. Install dependencies
npm install

# 2. Initialize the database
npm run migrate

# 3. Run the test suite
npm test
```

Installing this skill does not register an OpenClaw hook or slash command. Connect the exported library through an explicit plugin or operator-owned integration before processing runtime events.

## Security & Privacy

- **Local only**: All data stays on your machine. No external network calls.
- **No message content stored**: Only metadata (token count, model, session_id).
- **Sandboxed writes**: Database defaults to `~/.openclaw/tally/tally.db`; tests may use an explicit path under `/tmp`.
- **Hook scope**: No hook is registered by the skill. A future integration must disclose its event scope before enablement.

## Core Concepts

### Task

A unit of user intent — from a simple question ("What time is it in Tokyo?") to a multi-day campaign ("Scan job market daily"). Every dollar spent is attributed to a task.

### TES (Task Efficiency Score)

```
TES = quality_score / (normalized_cost × complexity_weight)
```

Higher is better. A TES > 2.0 means excellent value; < 0.5 means you're overpaying.

### Complexity Levels

- **L1 (Reflex)**: Single-turn Q&A, no tools
- **L2 (Routine)**: Multi-turn or 1–3 tool calls
- **L3 (Mission)**: Multiple tools + file I/O + external APIs
- **L4 (Campaign)**: Sub-agents + cron + cross-session continuity

## Proposed integration commands

- `/tasks list [--level L3] [--status completed]` — List recent tasks
- `/tasks stats [--period 30d]` — Summary statistics
- `/tasks this-week` — This week's task summary
- `/tasks show <task_id>` — Task detail view
- `/tasks report --dimension model` — Model efficiency breakdown
- `/tasks cron-health` — Cron job health check

## Architecture

Three-layer design:

1. **Task Detector** — Identifies task boundaries from message stream
2. **Task Ledger** — Attributes token costs to task IDs (SQLite)
3. **Analytics Engine** — Computes TES and powers dashboards/reports

## Full Specification

These commands are design targets in the PRD, not commands registered by the current skill bundle.

See `{baseDir}/PRD.md` for the complete product requirements document.

## License

MIT © Jony Jing
