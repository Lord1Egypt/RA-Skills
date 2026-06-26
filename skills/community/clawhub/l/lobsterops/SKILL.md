---
name: lobsterops
description: AI Agent Observability & Debug Console - flight recorder and debug console for autonomous AI systems
version: 1.0.0
metadata:
  openclaw:
    emoji: "\U0001F99E"
    requires:
      bins:
        - node
      env: []
    homepage: https://github.com/noeldelisle/LobsterOps
---

# LobsterOps Skill

AI Agent Observability & Debug Console. A lightweight, flexible "black box flight recorder" and debug console for AI agents. Automatically captures agent thoughts, tool calls, decisions, errors, spawning events, and lifecycle transitions.

## Core Tasks

- "Log my agent activity to LobsterOps" - Initialize LobsterOps and begin recording agent events with structured logging
- "Show me what my agent did" - Query the event log and display a chronological trace of agent activity
- "Debug my agent's last session" - Use the debug console to step through agent execution with time-travel debugging
- "Analyze my agent's behavior patterns" - Run behavioral analytics to detect loops, failure patterns, and performance trends
- "Set up alerts for my agent" - Configure alerting rules for cost spikes, repeated failures, or anomalous behavior
- "Export my agent logs" - Export events to JSON, CSV, or Markdown format for sharing or auditing

## Environment Variable Contract

| Variable | Required | Description |
|----------|----------|-------------|
| `LOBSTER_STORAGE` | No | Storage backend type: `json`, `memory`, `sqlite`, or `supabase` (default: `json`) |
| `SUPABASE_URL` | If using supabase | Supabase project URL |
| `SUPABASE_KEY` | If using supabase | Supabase anon or service role key |

## Configuration

LobsterOps uses OpenClaw's config system. Place configuration at `.openclaw/workspace/config/lobsterops.json`:

```json
{
  "enabled": true,
  "storageType": "json",
  "storageConfig": {
    "dataDir": "./agent-logs",
    "maxAgeDays": 30
  },
  "piiFiltering": {
    "enabled": true,
    "patterns": ["email", "phone", "ssn", "creditCard", "ipAddress", "apiKey"]
  },
  "alerts": {
    "enabled": true,
    "rules": []
  }
}
```

### Storage Backend Options

**JSON Files (default, zero-config):**
```json
{ "storageType": "json", "storageConfig": { "dataDir": "./agent-logs" } }
```

**SQLite (lightweight production):**
```json
{ "storageType": "sqlite", "storageConfig": { "filename": "./lobsterops.db" } }
```

**Supabase (cloud, team collaboration):**
```json
{
  "storageType": "supabase",
  "storageConfig": {
    "supabaseUrl": "https://your-project.supabase.co",
    "supabaseKey": "your-anon-key"
  }
}
```

## Security & Guardrails

- LobsterOps includes built-in PII filtering that automatically redacts emails, phone numbers, SSNs, credit card numbers, IP addresses, and API keys from logged events
- All data is stored locally by default (JSON files or SQLite) - no data leaves the machine unless Supabase is explicitly configured
- The Supabase backend requires explicit URL and key configuration - credentials are never inferred or auto-discovered
- Event retention policies automatically clean up old data based on configurable age limits
- LobsterOps never modifies agent behavior - it is strictly read-only observation

## Troubleshooting

- **"Cannot find module 'sqlite3'"**: Run `npm install sqlite3` - only needed if using SQLite backend
- **"Supabase table does not exist"**: Create the required table in your Supabase dashboard using the DDL provided in the error message
- **Events not appearing**: Ensure `enabled: true` in config and that `await ops.init()` has been called
- **High disk usage**: Reduce `maxAgeDays` in storage config or run `await ops.cleanupOld()` manually
- **PII still visible in logs**: Check that `piiFiltering.enabled` is `true` and the relevant pattern types are listed
