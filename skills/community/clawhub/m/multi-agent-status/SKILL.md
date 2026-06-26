---
name: multi-agent-status
description: Cross-agent health monitoring for multi-host OpenClaw deployments. Each agent pushes structured status reports (JSON) to a central location. A PM/monitoring agent reads them and alerts on failures. Works across Windows, Linux, and mixed environments.
version: 1.0.0
tags:
  - monitoring
  - multi-agent
  - health
  - status
  - cron
  - ops
  - dashboard
---

# Multi-Agent Status Reporter

## Overview

In a multi-agent OpenClaw deployment, each agent monitors itself but has blind spots. This skill solves that by having every agent push structured health reports to a shared location, where a monitoring agent reads and alerts on issues.

## Architecture

```
Agent A (Host 1) --push--> /shared/agent-status/agent-a.json
Agent B (Host 2) --push--> /shared/agent-status/agent-b.json
Agent C (Host 3) --push--> /shared/agent-status/agent-c.json
                                    ↓
                          Monitor Agent reads all
                          → alerts on failures
                          → updates dashboard
```

## What Gets Reported

Each agent pushes a JSON status report containing:
- **Gateway health** — is the RPC probe passing?
- **Cron status** — total crons, how many erroring, which ones
- **Active projects** — what the agent is working on
- **Timestamp** — so the monitor knows if a report is stale (agent might be down)

## Setup

**Scripts available in the [Collective Skills repo](https://github.com/Bobalouie44/collective-skills/tree/main/references)**

### 1. Create shared status directory

On your central/shared host:
```bash
mkdir -p /path/to/agent-status
chmod 777 /path/to/agent-status
```

**Scripts are in [`references/`](https://github.com/Bobalouie44/collective-skills/tree/main/references)**

### 2. Configure each agent

Copy the script from `references/agent-status-report.sh` to your preferred location and make it executable:

```bash
#!/bin/bash
# agent-status-report.sh
AGENT_NAME="my-agent"
STATUS_DIR="/path/to/agent-status"
REPORT="$STATUS_DIR/$AGENT_NAME.json"

# Get gateway status
GW_STATUS=$(openclaw gateway status 2>&1)
if echo "$GW_STATUS" | grep -q "RPC probe: ok"; then
    GATEWAY="healthy"
elif echo "$GW_STATUS" | grep -q "RPC probe: failed"; then
    GATEWAY="failed"
else
    GATEWAY="unknown"
fi

# Count cron errors
CRON_LIST=$(openclaw cron list 2>&1)
TOTAL=$(echo "$CRON_LIST" | grep -c "ok\|error" || echo 0)
ERRORS=$(echo "$CRON_LIST" | grep -c "error" || echo 0)

# Write report
cat > "$REPORT" << EOF
{
  "agent": "$AGENT_NAME",
  "timestamp": "$(date -Iseconds)",
  "gateway": "$GATEWAY",
  "crons": {
    "total": $TOTAL,
    "errors": $ERRORS
  }
}
EOF

echo "Status report pushed at $(date)"
```

For remote agents (different hosts), use SCP to push:
```bash
# Add to the end of the script:
scp "$REPORT" user@central-host:/path/to/agent-status/
```

### 3. Add cron job (every 4 hours recommended)

```bash
openclaw cron add \
  --name "agent-status-report" \
  --every "4h" \
  --message "Run the agent status report script" \
  --no-deliver
```

### 4. Configure the monitor agent

The monitoring agent's HEARTBEAT.md should include:

```markdown
## Agent Status Check
1. Read all files in /path/to/agent-status/*.json
2. For each agent:
   - Is gateway healthy? If "failed" → alert immediately
   - Any cron errors? If errors > 0 → ping the agent
   - Is timestamp recent (within 8 hours)? If stale → agent may be down
3. Update DASHBOARD.md with findings
```

## Alert Thresholds

| Condition | Action |
|-----------|--------|
| Gateway `failed` | Alert human immediately |
| Cron errors ≥ 2 | Ping owning agent for ETA on fix |
| Report stale (>8h) | Ping agent — might be down |
| Report missing | Agent never pushed — check if configured |

## Example Dashboard

```markdown
# Agent Health Dashboard
*Last updated: 2026-04-02 14:00*

| Agent | Host | Gateway | Crons | Errors | Last Report |
|-------|------|---------|-------|--------|-------------|
| Hyjack | OPT1 | ✅ healthy | 16 | 2 | 10m ago |
| Rook | PC-147 | ✅ healthy | 9 | 0 | 2h ago |
| Dozer | Vigo | ✅ healthy | 3 | 0 | 1h ago |

⚠️ Hyjack: 2 cron errors (Research Scout, sunday-self-compassion)
```

## Windows Support

For Windows agents, copy `references/agent-status-report.ps1` and run it with:

```powershell
# agent-status-report.ps1
$timestamp = Get-Date -Format "o"
$tempFile = "$env:TEMP\agent-status.json"

# Gateway check
$gwStatus = openclaw gateway status 2>&1 | Out-String
if ($gwStatus -match "RPC probe: ok") { $gw = "healthy" }
elseif ($gwStatus -match "RPC probe: failed") { $gw = "failed" }
else { $gw = "unknown" }

# Build report
@{
    agent = "my-agent"
    timestamp = $timestamp
    gateway = $gw
} | ConvertTo-Json | Out-File $tempFile -Encoding utf8

# Push to central host
scp $tempFile user@central-host:/path/to/agent-status/my-agent.json
```

## Notes

- SSH key auth required for cross-host pushes. Set up passwordless SSH first.
- The monitor agent should be on the same host as the status directory for local reads.
- Reports are intentionally small (<1KB) to minimize storage and transfer overhead.
- Stale detection (>8h) assumes 4h push interval. Adjust threshold if you change interval.
