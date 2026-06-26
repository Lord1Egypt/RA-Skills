# HEARTBEAT.md Template - OpenClaw

Use this as a production baseline for OpenClaw heartbeat tuning.

## Template

```markdown
# HEARTBEAT

## Objective
Keep the user informed about high-value changes while minimizing noisy or expensive checks.

## Runtime Contract
- If no actionable event is found: return exactly HEARTBEAT_OK
- If actionable: return concise action output and next-step recommendation

## Timing
- timezone: Europe/Madrid
- activeHours: 08:00-22:00
- defaultInterval: 30m
- burstInterval: 5m (only during active incidents)

## Monitors
1. Inbox triage (cheap precheck)
   - Trigger only if unread_urgent >= 1
2. Build status (cheap precheck)
   - Trigger only if last_build_state == failed
3. Calendar proximity check (cheap precheck)
   - Trigger only if next_event_minutes <= 30

## Escalation and Cooldown
- Critical incident: escalate immediately, cooldown 15m
- Important update: aggregate and send every 60m max
- Duplicate events during cooldown: suppress

## Cron Handoff
- Exact-time daily digest at 09:00 -> cron
- Weekly KPI report monday 08:30 -> cron

## Cost Guardrails
- Never call paid APIs unless precheck threshold is met
- If paid API is needed, cap to one call per cycle category

## Weekly Tuning
- If monitor signal quality < 20% for 7 days, extend interval
- If missed-event rate > 10%, shorten interval or add monitor
```

## Notes

- Keep this file focused on runtime behavior, not documentation prose.
- Prefer deterministic thresholds over vague wording.
