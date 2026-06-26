---
name: pingharbor
description: Query uptime monitors, heartbeat monitors, manage sites, retrieve incidents, create monitors, and fetch SLA reports from your PingHarbor account.
homepage: https://pingharbor.com
user-invocable: true
metadata: {"openclaw":{"emoji":"âš“","homepage":"https://pingharbor.com","primaryEnv":"PINGHARBOR_API_KEY","requires":{"env":["PINGHARBOR_API_KEY"]}}}
---

# PingHarbor â€” Uptime & Heartbeat Monitoring

Connect to your PingHarbor account to monitor website uptime, track cron jobs via heartbeat monitors, manage sites, query incidents, and pull SLA reports â€” all via the PingHarbor MCP server.

## Authentication

Set your PingHarbor API key as an environment variable:

```
PINGHARBOR_API_KEY=ph_your_api_key_here
```

Generate a key at: **Administration â†’ API Keys** inside your PingHarbor dashboard.

## MCP Endpoint

```
https://api.pingharbor.com/functions/v1/mcp
```

Pass the key as a Bearer token:

```
Authorization: Bearer $PINGHARBOR_API_KEY
```

## Available Tools

| Tool | Description |
|------|-------------|
| `list_monitors` | List all monitors and their current status |
| `get_incidents` | Retrieve recent incidents and downtime events |
| `create_monitor` | Create a new uptime monitor programmatically |
| `get_monitor_report` | Fetch SLA and response time report for a monitor |
| `list_heartbeat_monitors` | List all heartbeat monitors and their health status |
| `create_heartbeat_monitor` | Create a new heartbeat monitor with webhook URL |
| `list_sites` | List all sites for the authenticated account |
| `create_site` | Create a new site to group monitors together |

## Example Usage

> "List all my monitors and show me which ones are currently down."

> "Get incidents from the last 7 days for monitor ID xyz."

> "Create a monitor for https://example.com with a 60-second check interval."

> "Show me the SLA report for my main API monitor."

> "List my heartbeat monitors and show which ones have missed a heartbeat."

> "Create a heartbeat monitor for my nightly database backup that runs every 24 hours with a 60-minute grace period."

> "List all my sites."

> "Create a new site called 'Production' for https://myapp.com."

## Config (~/.openclaw/openclaw.json)

```json
{
  "skills": {
    "entries": {
      "pingharbor": {
        "enabled": true,
        "apiKey": "ph_your_api_key_here"
      }
    }
  }
}
```

Or via environment variable injection:

```json
{
  "skills": {
    "entries": {
      "pingharbor": {
        "enabled": true,
        "env": {
          "PINGHARBOR_API_KEY": "ph_your_api_key_here"
        }
      }
    }
  }
}
```