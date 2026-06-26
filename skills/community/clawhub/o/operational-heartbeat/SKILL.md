---
name: operational-heartbeat
description: Automated daily health check for OpenClaw instances. Verifies memory file presence, detects stale/overdue cron jobs, and surfaces system status. Intended for scheduled execution via cron.
---

1. Ensure memory file exists for today:
   - Path: memory/YYYY-MM-DD.md
   - If missing, create with minimal template

2. Check cron job health:
   - Use `cron list` to fetch all jobs
   - For each job, verify state.nextRunAtMs is in the future
   - Flag jobs with consecutiveErrors > 0 or lastRunStatus != 'ok'
   - Count stale/overdue jobs

3. Optional: promote learnings from recent memory files (if configured)

4. Report summary:
   - Memory file: created/exists
   - Cron jobs: total, healthy, stale count
   - Any errors or warnings

Implementation notes:
- Use a small Node.js script to parse cron JSON and filter stale jobs
- Comparison: new Date().getTime() vs nextRunAtMs
- Consider timezone-aware scheduling
- Exit 0 if healthy; non-zero if issues found
