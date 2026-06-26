# Cron Automation

Use cron for all periodic work. In `autonomous_live` mode, cron is the heartbeat of the agent — it must run reliably 24/7.

## Recommended jobs

| Job | Interval | Modes |
|---|---|---|
| Market scan + signal + execution | 2 min | `autonomous_live`, `live` |
| Market scan + signal (no execution) | 5 min | `approval`, `paper` |
| Risk reconciliation | 2 min | all |
| Post-trade review | 30 min | all |
| Learning consolidation (update_metrics) | 60 min | all |
| Daily summary + journal flush | Daily 00:00 | all |

## Scan interval

In `autonomous_live` mode, the default scan interval is **2 minutes**.
This can be reduced to 1 minute or increased to 5 minutes via config.
Shorter intervals increase API usage; check Aster rate limits.

## Rules

- Always check `mode` at the top of every cron cycle.
- Always check circuit breakers before execution.
- In `paper`: simulate only — no real orders.
- In `approval`: prepare proposals only — no real orders without approval.
- In `live` / `autonomous_live`: execute directly (subject to approval config).
- Disable cron execution immediately on halt.
- Every cron cycle must produce a journal entry (even if decision is `wait`).

## 24/7 continuity

In `autonomous_live` mode:
- Cron must survive system restarts (use launchd on macOS, systemd on Linux).
- On startup, always reconcile state before first execution cycle.
- If the agent was offline and positions exist, reconcile before placing new orders.
- Log all restarts and reconciliation events.

## Cron templates

See `openclaw-cron-templates.json` for ready-to-use OpenClaw cron job definitions.
See `deploy.launchd.plist` and `deploy.systemd.service` for system-level 24/7 deployment.
