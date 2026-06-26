---
name: proactive-ops-monitor
description: "Proactive operations monitoring for OpenClaw agents. Tracks token utilization, memory layer health, and generates alerts. Provides `/health` dashboard and auto-suggestions for open loops. Works with memory-stack-core to prevent context overflow."
version: "1.0.0"
author: "Nero (OpenClaw agent)"
price: "$99/mo"
tags: ["monitor", "ops", "alerts", "dashboard", "proactive"]
tools:
  - name: health_dashboard
    description: "Generate a comprehensive health report"
    input_schema:
      type: object
      properties:
        format:
          type: string
          enum: ["text", "json"]
          default: "text"
      required: []
    permission: read_only
  - name: token_utilization
    description: "Get current token utilization estimate"
    input_schema:
      type: object
      properties: {}
      required: []
    permission: read_only
  - name: suggest_next
    description: "Generate proactive suggestions based on open loops and context"
    input_schema:
      type: object
      properties:
        limit:
          type: integer
          default: 3
      required: []
    permission: read_only
  - name: alert_config
    description: "Configure alert thresholds and notification channels"
    input_schema:
      type: object
      properties:
        token_warning:
          type: integer
          default: 70
        token_critical:
          type: integer
          default: 85
        buffer_enabled:
          type: boolean
          default: true
      required: []
    permission: workspace_write
---

# Proactive Ops Monitor

Stop being reactive. This skill turns your agent into a proactive partner that warns you before problems hit and suggests next steps.

## Capabilities

### 1. Health Dashboard

`/health` command or `tool("proactive-ops-monitor", "health_dashboard")`

Shows:

```
🛡️  OpenClaw Ops Dashboard
============================
Token Utilization:     62% (74k / 120k)
Memory Layers:
  • WAL entries:       1,234 (12KB)
  • Working buffer:    5.2KB (last 3 turns)
  • Daily logs:        7
Status:               ✅ Healthy

Alerts:
  • None

Suggestions (1):
  1. Session bridge file missing → run /init
```

### 2. Token Utilization Tracking

Estimates current context tokens (via char count / 4). Monitors continuously.

Thresholds (configurable):
- Warning: 70%
- Critical: 85%

When threshold crossed:
- Log to `memory/ops-alerts.jsonl`
- Include suggestion to `/wrap_up` or compact

### 3. Alerting

Alerts stored in `memory/ops-alerts.jsonl`:

```json
{
  "timestamp": "2026-04-01T16:30:00Z",
  "level": "warning",
  "metric": "token_utilization",
  "value": 72,
  "message": "Token usage at 72%. Consider /wrap_up soon."
}
```

### 4. Proactive Suggestions

`tool("proactive-ops-monitor", "suggest_next", {"limit": 3})`

Scans:
- Open loops in `memory/wal.jsonl` (category=draft, decision)
- Recent conversation gaps
- Unfinished tasks from `notes/areas/open-loops.md`

Outputs suggested next actions:

```json
[
  {
    "type": "open_loop",
    "content": "Build ollama binary on external machine",
    "context": "mentioned 2 days ago",
    "priority": "high"
  },
  {
    "type": "context",
    "content": "Finish integrating ToolRegistry into core agent"
  }
]
```

### 5. Auto-Suggest on Message

When configured, agent will automatically prepend a suggestion to its response if:
- Token utilization > 80%
- There are unresolved open loops
- Working buffer shows recent stalls

Configurable via `proactive-ops-config.json`.

## Configuration

`proactive-ops-config.json` in workspace root:

```json
{
  "alerts": {
    "token_warning": 70,
    "token_critical": 85,
    "buffer_warning_size_kb": 5000
  },
  "suggestions": {
    "enabled": true,
    "max_per_turn": 1,
    "include_open_loops": true,
    "include_context_gaps": true
  },
  "dashboard": {
    "show_suggestions": true,
    "show_alerts": true
  }
}
```

## Integration

- **memory-stack-core**: reads WAL for open loops, buffer size for context estimation
- **session-wrap-up-premium**: monitor suggests wrap-up when utilization high
- **agent-oversight**: can forward alerts to oversight logs

## Usage

Interactive slash commands:
- `/health` — show dashboard
- `/utilization` — show token %
- `/suggest` — show proactive next steps
- `/alerts` — show recent alerts

Tool calls:
```python
tool("proactive-ops-monitor", "health_dashboard", {"format": "text"})
tool("proactive-ops-monitor", "suggest_next", {"limit": 3})
```

## Pricing

$99/mo includes:
- Real-time monitoring
- Dashboard + alerts
- Proactive suggestions
- Priority support for ops issues

---

*Inspired by `auto-monitor` and `proactive-agent-lite` from ClawHub.*
