# Cron Orchestration

> **Scheduled task management for true background autonomous operation**
> Priority: HIGH | Category: Operations

## Overview

Sessions have no state when closed. True autonomous work requires scheduled wake-ups. This skill enables overnight operation through cron jobs that wake the agent to continue work.

## The Problem

```yaml
scenario: "Assign task at 10pm, expect completion by morning"
reality:
  - "Session closed at midnight"
  - "Agent loses all state"
  - "Task stops at 20% completion"
  - "Agent idle until you notice"

gap: "6-8 hours of lost productivity"
```

## The Solution: Cron-Based Wake-Ups

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     OVERNIGHT OPERATION                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   22:00 - User assigns task                                  │
│   22:01 - Agent decomposes task, updates Todo.md             │
│   22:02 - Agent begins work                                  │
│                                                              │
│   00:00 - Session compresses (context loss starts)           │
│                                                              │
│   02:00 ──┐                                                  │
│            ├─ CRON WAKE #1                                   │
│   02:01 ──┤  - Check Todo.md                                 │
│            │  - Resume in-progress task                      │
│            │  - Update progress-log.md                       │
│            │  - Continue work                                │
│                                                              │
│   04:00 ──┐                                                  │
│            ├─ CRON WAKE #2                                   │
│   04:01 ──┤  - Check Todo.md                                 │
│            │  - Pick next task                               │
│            │  - Update progress-log.md                       │
│            │  - Continue work                                │
│                                                              │
│   06:00 ──┐                                                  │
│            ├─ CRON WAKE #3                                   │
│   06:01 ──┤  - Final check                                   │
│            │  - Complete remaining tasks                     │
│            │  - Generate morning briefing                    │
│            │  - Return to idle                               │
│                                                              │
│   08:00 - User wakes to complete work                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Cron Schedule Strategy

### Standard Overnight Schedule

```bash
#!/bin/bash
# overnight-schedule.sh

# Wake #1: Early night check
openclaw cron add \
  --name "overnight-early" \
  --cron "0 2 * * *" \
  --message "Check Todo.md. Resume in-progress tasks. Update progress-log.md. Continue highest priority work."

# Wake #2: Mid-night continuation
openclaw cron add \
  --name "overnight-mid" \
  --cron "0 4 * * *" \
  --message "Review Todo.md. Start next pending task. Document progress. Continue work."

# Wake #3: Pre-dawn finalization
openclaw cron add \
  --name "overnight-final" \
  --cron "0 6 * * *" \
  --message "Complete remaining tasks. Generate morning briefing. Summarize overnight work. Mark complete tasks."

# Morning briefing (for user)
openclaw cron add \
  --name "morning-briefing" \
  --cron "0 7 * * *" \
  --message "Generate comprehensive morning briefing in progress-log.md with completed tasks, failures, and next steps."
```

### Alternative Schedules

#### Light Operation (Less Frequent)
```bash
# For lower-priority or less time-sensitive work
openclaw cron add --name "light-nightly" --cron "0 3 * * *" \
  --message "Check Todo.md and continue priority tasks."

openclaw cron add --name "light-morning" --cron "0 6 * * *" \
  --message "Complete work and generate briefing."
```

#### Heavy Operation (More Frequent)
```bash
# For high-priority, time-sensitive work
openclaw cron add --name "heavy-hourly" --cron "0 * * * *" \
  --message "Hourly check: Todo.md status, continue work, update progress."

# Plus overnight wake-ups
```

#### Weekend-Only Operation
```bash
# For work that can wait until weekends
openclaw cron add --name "weekend-start" --cron "0 22 * * 6" \
  --message "Starting weekend work batch. Review Todo.md for weekend tasks."

openclaw cron add --name "weekend-check" --cron "0 2,6,10 * * 0" \
  --message "Weekend work check. Continue tasks, update progress."

openclaw cron add --name "weekend-end" --cron "0 18 * * 0" \
  --message "Complete weekend work. Generate summary. Prepare for Monday."
```

## Cron Message Templates

### Standard Work Continuation

```
Check Todo.md. Pick up incomplete or in-progress tasks.
Continue execution cycle following execution-discipline rules.
Update progress-log.md with each cycle completed.
If all tasks complete, generate summary and return to idle.
```

### Focused Task Completion

```
Check Todo.md for tasks tagged [urgent/overnight].
Focus on completing these tasks first.
Document any blockers in progress-log.md.
Escalate if blocked for >30 minutes.
```

### Maintenance & Housekeeping

```
Run maintenance cycle:
1. Check for stale tasks (>4 hours in progress)
2. Review and update progress-log.md
3. Clean up temporary files
4. Verify system health
5. Update task statistics
```

### Error Recovery

```
Check progress-log.md for recent failures.
Review lessons.md for patterns.
Attempt recovery on failed tasks.
Document recovery attempts.
Escalate if recovery fails.
```

## Cron Job Configuration

### Job Specification

```yaml
cron_job:
  name: "descriptive-job-name"
  schedule: "standard_cron_format"
  enabled: true
  timeout: 3600  # 1 hour max
  max_retries: 3
  on_failure: "notify"

  message_template: |
    Your message here with:
    - Clear instructions
    - Expected actions
    - Success criteria

  context:
    include:
      - "Todo.md"
      - "progress-log.md"
      - "STATE.md"

    exclude:
      - "Large session logs"
      - "Temporary files"
```

### Advanced Configuration

```bash
# Create cron with resource limits
openclaw cron add \
  --name "resource-limited-job" \
  --cron "0 3 * * *" \
  --message "Task description" \
  --max-tokens 50000 \
  --max-duration 1800 \
  --priority low \
  --on-failure notify

# Create cron with dependencies
openclaw cron add \
  --name "dependent-job" \
  --cron "30 3 * * *" \
  --message "Follow-up task" \
  --requires "resource-limited-job"

# Create cron with conditional execution
openclaw cron add \
  --name "conditional-job" \
  --cron "0 4 * * *" \
  --message "Task if pending > 0" \
  --condition "Todo.md has pending tasks"
```

## Cron Integration with Skills

### With task-autonomy.md

```yaml
integration:
  cron_wake:
    1: "Read Todo.md"
    2: "Select highest-priority incomplete task"
    3: "Resume execution from task-autonomy cycle"
    4: "Update Todo.md with discovered subtasks"
    5: "Continue until task complete or time limit"
```

### With progress-logging.md

```yaml
integration:
  wake_logging:
    - "Log cron wake in progress-log.md"
    - "Record session ID"
    - "Note tasks picked up"
    - "Document work performed"

  sleep_logging:
    - "Log session end in progress-log.md"
    - "Record tasks in progress"
    - "Note session state for recovery"
```

### With memory-persistence.md

```yaml
integration:
  state_recovery:
    wake:
      - "Read STATE.md for session context"
      - "Read MEMORY.md for relevant context"
      - "Resume with full context"

    sleep:
      - "Update STATE.md with current work"
      - "Save any new decisions to MEMORY.md"
```

## Cron Job Examples

### Example 1: Full Overnight Work Cycle

```bash
#!/bin/bash
# Deploy full overnight schedule

# Early night - Resume work
openclaw cron add \
  --name "overnight-2am" \
  --cron "0 2 * * *" \
  --message "OVERNIGHT WORK CYCLE 1/3
Check Todo.md for incomplete or in-progress tasks.
Resume highest-priority task.
Follow execution-discipline.md rules.
Update progress-log.md after each cycle.
Discover and add new tasks to Todo.md as needed.
Continue until task complete or 03:45 approaches.
At 03:45, save state and prepare for next wake."

# Mid night - Continue work
openclaw cron add \
  --name "overnight-4am" \
  --cron "0 4 * * *" \
  --message "OVERNIGHT WORK CYCLE 2/3
Review progress-log.md for context.
Check Todo.md for pending tasks.
Start next highest-priority task.
Follow execution-discipline.md rules.
Update progress-log.md after each cycle.
Discover and add new tasks to Todo.md as needed.
Continue until task complete or 05:45 approaches.
At 05:45, save state and prepare for final wake."

# Pre-dawn - Finalize work
openclaw cron add \
  --name "overnight-6am" \
  --cron "0 6 * * *" \
  --message "OVERNIGHT WORK CYCLE 3/3
Review progress-log.md for context.
Check Todo.md for remaining tasks.
Complete all possible tasks.
Generate comprehensive morning briefing:
- Tasks completed overnight
- Tasks failed with reasons
- Tasks blocked and what's needed
- Metrics (tokens, time, success rate)
- Ready for review items
Move completed tasks to archive.
Update task statistics.
Return to idle state awaiting user."
```

### Example 2: Maintenance Schedule

```bash
# Daily maintenance
openclaw cron add \
  --name "daily-maintenance" \
  --cron "0 3 * * *" \
  --message "DAILY MAINTENANCE
1. Check for stale tasks (mark if >4 hours in progress)
2. Review progress-log.md for patterns
3. Clean up temporary files
4. Run openclaw doctor --fix
5. Update task statistics
6. Generate daily summary"

# Weekly deep clean
openclaw cron add \
  --name "weekly-cleanup" \
  --cron "0 3 * * 0" \
  --message "WEEKLY CLEANUP
1. Archive completed tasks older than 7 days
2. Review and update LESSONS.md
3. Check for security updates
4. Run openclaw security audit
5. Clean up old logs
6. Generate weekly report"
```

## Monitoring Cron Jobs

### List Active Jobs

```bash
# List all cron jobs
openclaw cron list

# Show job details
openclaw cron show overnight-2am

# Show job history
openclaw cron history --since=24h

# Show job statistics
openclaw cron stats --by=job
```

### Debug Cron Issues

```bash
# Show recent cron logs
openclaw logs --cron --since=24h

# Test cron job manually
openclaw cron test overnight-2am

# Validate cron schedule
openclaw cron validate --cron "0 2 * * *"

# Dry-run cron job
openclaw cron run --dry-run overnight-2am
```

## Cron Job Management

### Enable/Disable Jobs

```bash
# Disable job temporarily
openclaw cron disable overnight-2am

# Enable job
openclaw cron enable overnight-2am

# Disable all overnight jobs
openclaw cron disable --pattern "overnight-*"

# Enable all overnight jobs
openclaw cron enable --pattern "overnight-*"
```

### Update Jobs

```bash
# Update job schedule
openclaw cron update overnight-2am --cron "0 1 * * *"

# Update job message
openclaw cron update overnight-2am --message "New message"

# Update job configuration
openclaw cron update overnight-2am --timeout 1800
```

### Delete Jobs

```bash
# Delete single job
openclaw cron delete overnight-2am

# Delete multiple jobs by pattern
openclaw cron delete --pattern "test-*"

# Delete all jobs (with confirmation)
openclaw cron delete --all --confirm
```

## Best Practices

### DO ✅

```yaml
good_practices:
  scheduling:
    - "Space wake-ups appropriately (not too frequent)"
    - "Allow sufficient time for work between wake-ups"
    - "Consider task complexity when setting frequency"

  messaging:
    - "Be specific about what to do"
    - "Reference relevant skills by name"
    - "Include success criteria"

  monitoring:
    - "Log cron job executions"
    - "Track success/failure rates"
    - "Review logs regularly"

  maintenance:
    - "Periodically review job necessity"
    - "Clean up old/unused jobs"
    - "Update messages based on learned patterns"
```

### DON'T ❌

```yaml
bad_practices:
  scheduling:
    - "Don't wake up every few minutes (token waste)"
    - "Don't overlap wake-up times"
    - "Don't schedule during peak usage hours"

  messaging:
    - "Don't use vague instructions"
    - "Don't assume context is preserved"
    - "Don't skip references to skills"

  operations:
    - "Don't create jobs without testing"
    - "Don't forget about jobs (monitor them)"
    - "Don't let failed jobs persist without investigation"
```

## Key Takeaway

**Sessions end, but cron jobs persist.** Proper cron orchestration turns a chatbot into infrastructure that works while you sleep.

---

**Related Skills**: `task-autonomy.md`, `progress-logging.md`, `memory-persistence.md`
