# Memory Template - Heartbeat

Create `~/heartbeat/memory.md` with this structure:

```markdown
# Heartbeat Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Environment
timezone: Europe/Madrid
active_hours: "08:00-22:00"
mode: conservative | balanced | aggressive

## Heartbeat Scope
mission: "Short sentence describing heartbeat objective"
signals:
- signal_1
- signal_2
- signal_3

## Timing Policy
default_interval: 30m
burst_interval: 5m
cooldown_default: 30m
exact_time_jobs_to_cron:
- "daily summary at 09:00"
- "weekly report on monday 08:30"

## Cost and Risk
expensive_checks:
- check_name
precheck_strategy: "Describe cheap gate before expensive call"
alert_noise_tolerance: low | medium | high

## Notes
<!-- Lessons learned from heartbeat tuning -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still calibrating heartbeat | Keep refining intervals and guards |
| `complete` | Stable and reliable policy | Only adjust on explicit feedback |
| `paused` | User paused optimization | Avoid proactive tuning suggestions |

## Key Principles

- Prefer explicit timing decisions over implicit assumptions.
- Every expensive check needs a gate condition.
- Every alert needs a cooldown.
