---
name: lingxi-agent-monitor
category: monitoring
description: "Monitor OpenClaw Agent health, uptime, task status, and system metrics. Automatic alerts on failures, performance degradation, or unusual behavior. Includes memory management, session cleanup, and proactive self-healing."
version: 1.0
---

# lingxi-agent-monitor

Proactive health monitoring and self-healing for AI Agent systems built on OpenClaw.

## What It Monitors

| Metric | Check | Alert Threshold |
|--------|-------|-----------------|
| Agent Uptime | Is agent alive? | Any downtime |
| Session Count | Active sessions | > 20 or < 1 |
| Memory Usage | Agent memory consumption | > 80% |
| Task Queue | Pending/failed tasks | > 5 failed |
| MCP Connections | External tool connectivity | Any failure |
| API Latency | Tool response time | > 5 seconds |
| Error Rate | Tool call failure % | > 10% |

## Usage

### Trigger Commands

```
"System health check"  → Full health scan + report
"Agent status"        → Quick status summary
"Memory check"         → Focus on memory metrics
"Task queue check"     → Focus on pending/failed tasks
"Alert me if..."      → Configure custom alert rules
```

## Health Report Format

```markdown
# Agent Health Report — YYYY-MM-DD HH:MM

## System Status
| Component | Status | Latency | Notes |
|-----------|--------|---------|-------|
| OpenClaw Gateway | ✅ Healthy | 45ms | |
| MCP Server | ✅ Connected | 120ms | |
| GitHub Integration | ✅ OK | 200ms | |
| ZeroGPU | ✅ OK | 80ms | |

## Session Overview
- Active sessions: 3
- Avg session duration: 23m
- Memory: 1.2GB / 4GB (30%)

## Recent Activity
- Tasks completed: 47
- Tasks failed: 2 (4.3%)
- Avg task duration: 1m 12s

## Alerts (if any)
- [ ] No critical alerts
- ⚠️ Warning: ZeroGPU latency > 500ms (3 occurrences)
```

## Alert Levels

| Level | Trigger | Action |
|-------|---------|--------|
| 🔴 Critical | Agent down, all tools failing | Immediate notification + restart attempt |
| 🟡 Warning | Degraded performance, > 10% error rate | Scheduled notification |
| 🔵 Info | New session, task milestone | Log only |

## Self-Healing Actions

When issues are detected, the agent can automatically:

1. **Restart failed MCP connections**
2. **Clean up stale sessions** (sessions idle > 2 hours)
3. **Flush memory cache** when usage > 80%
4. **Retry failed tool calls** (up to 3 attempts)
5. **Switch to backup providers** (e.g., GitHub API fallback)

## Configuration

```json
{
  "alert_channels": ["log", "notification"],
  "memory_threshold_pct": 80,
  "session_idle_timeout_min": 120,
  "max_sessions": 20,
  "error_rate_threshold_pct": 10,
  "latency_threshold_ms": 5000,
  "self_heal_enabled": true,
  "health_check_interval_min": 15
}
```

## Cron Schedule

```
*/15 * * * * → Health check every 15 minutes
0 */2 * * *  → Deep memory cleanup every 2 hours
```

## Installation

```bash
clawhub install lingxi-agent-monitor
```

## Integration with External Alerting

For external alerts (Slack, Discord, PagerDuty):

```bash
# In your notification workflow
curl -X POST $SLACK_WEBHOOK \
  -H "Content-Type: application/json" \
  -d '{"text": "🔴 Agent Alert: $ALERT_MESSAGE"}'
```

## Memory Management

When memory usage is high:
1. Archive completed session summaries to memory files
2. Clear intermediate computation cache
3. Merge small memory files into consolidated ones
4. Prune session history beyond retention limit

## Dashboard Endpoint

If running with n8n bridge:
```
GET /agent-monitor/dashboard  → HTML dashboard with real-time status
GET /agent-monitor/metrics   → JSON metrics endpoint
GET /agent-monitor/alerts     → JSON alert history
```
