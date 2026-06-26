---
name: magic-need
description: Capture tool and data needs from AI agents during task execution. When an agent identifies it needs a tool, API, or data source that doesn't exist, this skill provides a CLI to register that need. Needs are categorized automatically and can be reviewed periodically to build an integration roadmap. Use when the agent realizes it needs something that isn't available — e.g., "I would need X API to do this properly", "If I had access to Y logs I could investigate", "A tool that does Z would be useful here".
---

# magic-need

Capture what your AI agent wishes it had. Let your agent spec your product for you.

## Overview

When an AI agent is executing a task and hits a wall because it lacks data or tools, instead of just failing or working around it, this skill lets the agent register exactly what it's missing. Over time, this builds a prioritized roadmap of integrations and features.

Inspired by Sonarly's `magic_fetch` concept — give the agent a "tool that does nothing" and let it tell you what it actually needs.

## Usage

### As an Agent (During Task Execution)

When you realize you need something you don't have:

```bash
# Option 1: Use the CLI directly
node ~/.openclaw/skills/magic-need/scripts/cli.js "API for recent deploys of service X"

# Option 2: Use via shell exec
exec({
  command: 'node ~/.openclaw/skills/magic-need/scripts/cli.js "CPU metrics for upstream service"'
})
```

The CLI will:
1. Save the need to `~/.magic-need/needs.json`
2. Auto-categorize it (integration, observability, devops, auth, database, storage)
3. Return a confirmation with the need ID

### As a Human (Reviewing Needs)

```bash
# List all needs
node scripts/cli.js list

# Generate a report (grouped by category)
node scripts/cli.js report

# Archive resolved needs
node scripts/cli.js clear
```

## Auto-Categorization

Needs are automatically categorized based on description keywords:

| Category | Keywords | Example Need |
|----------|----------|--------------|
| `integration` | api, endpoint | "API for fetching user data" |
| `observability` | metric, log, monitor | "Error logs from last hour" |
| `devops` | deploy, pipeline, ci | "Recent deployments of service X" |
| `auth` | user, auth, login, permission | "Auth tokens for service Y" |
| `database` | database, db, query, schema | "Query to get active users" |
| `storage` | file, storage, upload, s3 | "Upload files to cloud storage" |
| `general` | (default) | Other needs |

## Data Format

Needs are stored as JSON in `~/.magic-need/needs.json`:

```json
[
  {
    "id": "j8ldlr",
    "description": "API for recent deploys",
    "createdAt": "2026-03-07T18:09:18.123Z",
    "status": "pending",
    "category": "integration"
  }
]
```

## Report Format

The `report` command outputs a formatted summary:

```
🪄 **Magic Need Report** — 4 pending

🔌 **INTEGRATION** (2)
  • API for recent deploys of auth-service
  • Feature flags toggled recently

📊 **OBSERVABILITY** (1)
  • CPU metrics for upstream database

📝 **GENERAL** (1)
  • Tool to visualize data flow
```

## Best Practices

### Good Need Descriptions

Be specific about what you need:

- ✅ "API endpoint for deploys in the last 2 hours, filtered by service name"
- ✅ "CPU and memory metrics for upstream auth-service pods"
- ✅ "Feature flags that changed in the last 24h for api-gateway"
- ✅ "Sentry errors grouped by affected user segment"

### Bad Need Descriptions

Avoid vague descriptions:

- ❌ "need more data"
- ❌ "can't do this without tools"
- ❌ "would be nice to have logs"

### Integration Roadmap

Periodically review the generated reports to:
1. Identify patterns (which categories have the most needs?)
2. Prioritize integrations (which needs block the most tasks?)
3. Build the most impactful tools first

## CLI Reference

See `scripts/cli.js` for the full implementation.

### Commands

| Command | Description |
|---------|-------------|
| `cli.js "description"` | Register a new need |
| `cli.js list` | List all needs |
| `cli.js report` | Generate formatted report |
| `cli.js clear` | Archive pending needs |

## Cron Integration

To receive daily reports, set up a cronjob:

```bash
# Daily at 10 PM
0 22 * * * node ~/.openclaw/skills/magic-need/scripts/cli.js report | your-notification-script
```

Or use OpenClaw's cron system to send reports to a Discord channel.
