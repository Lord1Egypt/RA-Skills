# Setup Guide

## For the Human

1. **Create a workspace directory** for your personal-os
2. **Set up basic files:**
   - `STATE.md` — your projects and current status
   - `TODO.md` — active tasks
   - `DECISIONS.md` — decision log
   - `PENDING-DECISIONS.md` — blocked decisions
   - `HEARTBEAT-LOG.md` — activity log
3. **Start working with your AI collaborator**
4. **Update the system after each significant conversation or action**

## For the AI

After each conversation:

1. Read `STATE.md`, `DECISIONS.md`, `TODO.md`
2. Update relevant files with new decisions, progress, or changes
3. Write a summary to `HEARTBEAT-LOG.md`
4. Generate review drafts periodically

## Key Principle

The system stays current because the AI keeps it current.

## Cron Jobs (Optional)

Set up periodic health checks and review generation:

- Every 30 min: consistency check
- Every 1 hour: system maintenance
- Every day: review generation
- Every week: deeper review

## No Command Required

The AI should not wait for commands.

The AI reads the system, understands the human, and acts proactively.

## Metrics That Matter

- Decision log completeness
- Review regularity
- Task status accuracy
- System freshness (time since last update)
