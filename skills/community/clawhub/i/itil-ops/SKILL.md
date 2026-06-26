---
name: itil-ops
description: >
  ITIL-aligned incident, problem, and change management for AI agents.
  Use when: detecting service crashes, analyzing recurring failures, tracking
  incidents to resolution, performing root cause analysis, managing change
  requests, running health audits, or building operational review pipelines.
  Implements ITIL 4 practices adapted for autonomous agent operations:
  Incident Management, Problem Management, Change Management, Event Management,
  and Continual Improvement. Works with systemd, cron, journalctl, and
  coordination task boards.
---

# ITIL Ops — IT Service Management for AI Agents

Structured incident, problem, and change management adapted from ITIL 4 for autonomous agent operations.

## Core Concepts

### Severity Levels

| Level | Meaning | Response | Example |
|-------|---------|----------|---------|
| **P1** | Critical — service down, data at risk | Immediate alert + auto-remediate | Crash loop, disk full, OOM |
| **P2** | High — degraded service | Alert within 1h | Service restarts, auth failures |
| **P3** | Medium — non-critical issue | Next review cycle | Cron timeouts, broken files |
| **P4** | Low — cosmetic/minor | Track, fix when convenient | Log warnings, config drift |

### Incident vs Problem vs Change

- **Incident**: Something broke. Restore service ASAP. (reactive)
- **Problem**: Pattern of incidents. Find and fix root cause. (proactive)
- **Change**: Planned modification. Assess risk before executing. (controlled)

## Incident Management

### Detection Sources

Scan these in order of criticality:

1. **Service crashes** — `journalctl --user -u SERVICE --since "12 hours ago"` for watchdog timeouts, SIGABRT, SIGSEGV, core dumps
2. **Cron failures** — consecutive error count > 2 in job state files
3. **Health endpoints** — HTTP health checks returning non-200
4. **Resource pressure** — disk > 80%, RAM > 80%, swap active
5. **Data integrity** — schema validation failures, broken files, load errors

### Detection Script

Run `scripts/itil-review.sh` to scan all sources. It outputs:
- `ITIL_CLEAR` if nothing found (reply HEARTBEAT_OK)
- Formatted report with incidents and problems if issues detected

### Incident Lifecycle

```
DETECTED → CLASSIFIED (P1-P4) → DIAGNOSED → RESOLVED → CLOSED
                                      ↓
                              (3+ occurrences)
                                      ↓
                              ESCALATE TO PROBLEM
```

### Auto-Classification Rules

```bash
# P1 — Critical
- Service crash count >= 3 in 12h (crash loop)
- Disk usage >= 90%
- RAM usage >= 90%
- Data loss detected

# P2 — High
- Service crashed 1-2 times
- 3+ services down simultaneously
- Auth/token failures affecting operations
- Cron job with 5+ consecutive failures

# P3 — Medium
- Broken data files (schema violations)
- Memory load errors > 10 in 12h
- Cron job with 3-4 consecutive failures
- Disk usage 80-89%

# P4 — Low
- 1 service down (non-critical)
- Config warnings
- Log noise
```

### Creating Incident Tickets

When incidents are found, create coordination tasks:

```
Title: [ITIL-INC] <brief description>
Body:
- Severity: P1/P2/P3/P4
- Category: service|cron|memory|disk|security
- Detected: <timestamp>
- Detail: <what happened>
- Impact: <what's affected>
- Action: <what to do>
```

## Problem Management

### Pattern Detection

An incident becomes a problem when:
- Same error occurs **3+ times in 24h**
- Same incident type recurs **across 2+ review cycles**
- Multiple related incidents share a **common root cause**

### Root Cause Analysis (RCA)

When a problem is identified:

1. **Gather evidence** — journal logs, error messages, state files, recent changes
2. **Timeline** — reconstruct the sequence of events
3. **5 Whys** — ask why iteratively until you reach the actual root cause
4. **Fix classification**:
   - **Quick fix** — config change, file repair, timeout bump
   - **Code fix** — bug in script or daemon, needs PR
   - **Architecture fix** — design flaw, needs redesign

### Problem Ticket Format

```
Title: [ITIL-PRB] <root cause description>
Body:
- Related incidents: <list>
- Root cause: <what's actually broken>
- Evidence: <logs, patterns, data>
- Fix applied: <immediate remediation>
- Fix needed: <permanent solution>
- Prevention: <how to prevent recurrence>
```

### Known Error Database

Track resolved problems in state file (`itil-state.json`):

```json
{
  "last_review": "2026-03-22T04:19:50Z",
  "last_incident_count": 2,
  "last_problem_count": 1,
  "known_errors": {
    "memory-content-dict": {
      "description": "Scripts writing content as dict instead of string",
      "root_cause": "Missing json.dumps() in memory file writers",
      "fix": "Wrap content in json.dumps() before saving",
      "fixed_date": "2026-03-22"
    }
  }
}
```

## Change Management

### Pre-Change Checklist

Before modifying services, configs, or infrastructure:

1. **What's changing?** — specific files, services, configs
2. **Why?** — linked incident/problem ticket
3. **Risk?** — what could go wrong
4. **Rollback plan?** — how to undo if it breaks
5. **Test?** — how to verify it worked
6. **Notify?** — does the human need to know

### Change Categories

| Type | Approval | Example |
|------|----------|---------|
| **Standard** | Pre-approved, just do it | Restart service, bump timeout |
| **Normal** | Inform human, wait for OK | New cron job, config change |
| **Emergency** | Fix now, inform after | Service down, data at risk |

### Post-Change Verification

After any change:
1. Check service status — `systemctl --user status SERVICE`
2. Watch logs for 60s — `journalctl --user -u SERVICE -f --since "now"`
3. Run health check — `scripts/itil-review.sh`
4. Verify no new errors in first 5 minutes

## Event Management

### Log Monitoring Patterns

```bash
# Service crashes
journalctl --user -u SERVICE --since "12h ago" | grep -ciE "watchdog timeout|killed|SIGABRT|SIGSEGV|failed with"

# Memory/resource issues
journalctl --user -u SERVICE --since "12h ago" | grep -c "Failed to load"

# Auth failures
journalctl --user -u SERVICE --since "12h ago" | grep -ciE "unauthorized|403|token expired|auth fail"
```

### Health Check Endpoints

Check services with curl:
```bash
curl -sf --max-time 5 "$URL" >/dev/null 2>&1 || echo "DOWN"
```

Configure endpoints in the review script for your environment.

## Continual Improvement

### Review Cadence

| Review | Frequency | Purpose |
|--------|-----------|---------|
| **Incident review** | Every 12h | Detect and classify new issues |
| **Problem review** | Weekly | Identify patterns, track RCA progress |
| **Capacity review** | Weekly | Disk, RAM, memory count trends |
| **Process review** | Monthly | Are our detection rules catching real issues? |

### KPIs to Track

- **MTTR** (Mean Time to Resolve) — how fast do we fix incidents?
- **Incident recurrence rate** — are the same things breaking?
- **False positive rate** — are we alerting on non-issues?
- **Known error resolution** — are problems getting permanent fixes?

### State Tracking

The review script maintains `itil-state.json` with:
- Last review timestamp and results
- Incident/problem counts per review
- System metrics (disk, RAM, restart count)
- Cross-review pattern detection data

## Cron Setup

### Recommended Schedule

```bash
# Incident review — every 12 hours
openclaw cron add --name "itil-review" --every "12h" \
  --model "anthropic/claude-sonnet-4-6" --timeout-seconds 180 \
  --session isolated \
  --message "Run ITIL review: bash ~/.skcapstone/agents/lumina/scripts/itil-review.sh"

# Weekly problem review (Sunday 9 AM)
# Analyze the week's incidents, identify patterns, suggest improvements
```

## File Structure

```
itil-ops/
├── SKILL.md              # This file
├── scripts/
│   └── itil-review.sh    # Main review script (scan + classify + report)
└── references/
    └── itil4-agent-mapping.md  # ITIL 4 → Agent operations reference
```

## Integration Points

- **Coordination tasks** — `skcapstone coord create` for incident/problem tickets
- **Memory snapshots** — `skmemory_snapshot` to record resolutions for future reference
- **Heartbeat** — integrate with existing heartbeat to run lightweight checks
- **Cron** — scheduled reviews via OpenClaw cron system
- **Alerting** — Telegram/Discord delivery for P1/P2 issues
