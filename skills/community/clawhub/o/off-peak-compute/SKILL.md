---
name: off-peak-compute
version: 1.0.1
description: Run heavy compute tasks overnight when GPU/cloud capacity is cheapest (spot pricing). Use when you have non-time-sensitive tasks that would benefit from off-peak availability. Tasks execute at 2 AM via cron.
author: clawde
priority: high
tags: [compute, scheduling, spot-pricing, optimization, cron]
---

# Off-Peak Compute Skill

**Core Insight:** Cloud providers sell pooled, variable capacity. Your effective quota depends on infrastructure load. Running heavy tasks overnight maximizes throughput when GPU farms are underutilized.

## What This Skill Does

- Provides a script template for queuing non-time-sensitive compute tasks
- Runs queued tasks automatically at 2 AM via cron
- Logs execution results for morning review

## Security Model

**Honest assessment of what runs:**

| Layer | Isolation | Privileges |
|-------|-----------|------------|
| Cron job | Separate process | Full user privileges |
| Agent session | New session (isolated from your current session) | Full access to your environment's credentials |
| Network calls | None | Whatever credentials the agent can access |

**What this means:**
- Tasks run with your user privileges
- Each task spawns a new agent session (isolated from each other)
- Sessions can access your environment's credentials
- There is no sandboxing or credential scoping

**Your responsibility:**
- Inspect tasks before adding them
- Don't embed secrets directly in the script
- Test tasks manually before scheduling
- Review what network actions tasks perform

## Setup (One-Time)

```bash
# Create directories
mkdir -p ~/.openclaw/workspace/scripts
mkdir -p ~/.openclaw/workspace/logs

# Copy the script template (see below)
# Path: ~/.openclaw/workspace/scripts/off-peak-compute.sh

# Make executable (owner only for security)
chmod 700 ~/.openclaw/workspace/scripts/off-peak-compute.sh

# Add cron job (runs at 2 AM daily)
(crontab -l 2>/dev/null | grep -v "off-peak-compute"; echo "0 2 * * * \$HOME/.openclaw/workspace/scripts/off-peak-compute.sh") | crontab -

# Verify
crontab -l | grep off-peak
```

## Script Template

Create `~/.openclaw/workspace/scripts/off-peak-compute.sh`:

```bash
#!/bin/bash
# off-peak-compute.sh
# 
# OFF-PEAK COMPUTE QUEUE
# Runs automatically at 2 AM via cron
# 
# SECURITY: Tasks run with your user privileges and can access
# your environment's credentials. Each task spawns a new agent
# session (isolated from each other). No sandboxing is provided.
# 
# REVIEW BEFORE ENABLING:
# - Remove sample tasks you don't want
# - Test tasks manually before scheduling
# - Be aware of credential scope for each task
# - Restrict permissions: chmod 700 this script
#
# ---------------------------------------------------------------------------

LOG_FILE="$HOME/.openclaw/workspace/logs/off-peak-compute.log"
SCRIPT_FILE="$HOME/.openclaw/workspace/scripts/off-peak-compute.sh"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
log "Off-peak compute run starting"
echo "========================================" >> "$LOG_FILE"

# Count tasks
TASK_COUNT=$(grep -c "^# TASK:" "$SCRIPT_FILE" 2>/dev/null || echo "0")

if [ "$TASK_COUNT" -eq 0 ]; then
    log "No tasks queued. Exiting."
    exit 0
fi

log "Found $TASK_COUNT task(s) to process"

# TASK TEMPLATE
# Copy and modify for each task. Be aware of:
# - Credential scope (what can this task access?)
# - Network actions (what external services does it call?)
# - File writes (where does it save results?)
#
# # TASK: <description>
# # Added: <date>
# # Credential scope: <what credentials does this use?>
# # Network actions: <what external services?>
# openclaw agent --agent <agent-id> --message "Task instructions here"
# # END TASK
# ---------------------------------------------------------------------------

# TASKS BELOW THIS LINE
# ---------------------------------------------------------------------------



# END OF TASKS
# ---------------------------------------------------------------------------

log "Run complete. Check log for results."
log "Remove completed tasks manually before next run."
```

## Adding Tasks

**Before adding a task, ask yourself:**

1. What credentials does this task need?
2. What network actions will it perform?
3. Where will it write files?
4. Have I tested it manually?

**Template:**

```bash
# TASK: Research competitive landscape
# Added: 2026-03-10
# Credential scope: web search API (no secrets)
# Network actions: web search, file write
openclaw agent --agent main --message "Research competitive landscape for X. Save results to ~/notes/research/findings.md"
# END TASK
```

## Checking Results

```bash
# View log
cat ~/.openclaw/workspace/logs/off-peak-compute.log

# Check for task output (wherever the task saves results)
ls -la ~/notes/research/
```

## When to Use This

**Good for off-peak:**
- Deep research (can wait 12-24 hours)
- Document summarization batches
- Model-intensive analysis
- Batch processing jobs

**NOT for off-peak:**
- Time-sensitive requests (emails, calendar)
- Interactive tasks requiring follow-up
- Urgent matters

## Cron Schedule

```
0 2 * * * $HOME/.openclaw/workspace/scripts/off-peak-compute.sh
```

Adjust timezone if needed.

## Why This Matters

Cloud providers sell pooled capacity. Overnight = lower demand = more throughput per token. This skill lets you queue heavy work for when capacity is cheapest.

---

*Created: 2026-03-10*
*Updated: 2026-03-10 — Honest security model, clear credential scope guidance*