# Internet Research Sources (Heartbeat)

Research date: 2026-03-04

## Primary Sources

1. OpenClaw Docs - Heartbeats
   - https://docs.openclaw.ai/advanced/heartbeats
   - Key takeaways used:
     - heartbeat can run continuously on an interval
     - default example interval is 30m
     - define timezone and active hours to prevent off-hour noise
     - when no action is needed, return HEARTBEAT_OK

2. OpenClaw Docs - Cron vs Heartbeat
   - https://docs.openclaw.ai/advanced/cron-vs-heartbeat
   - Key takeaways used:
     - cron for exact-time execution
     - heartbeat for adaptive/reactive monitoring
     - hybrid model is recommended in many workflows
     - use cheap prechecks to control API/token cost

3. OpenClaw CLI System Skill
   - https://docs.openclaw.ai/openclaw-cli/system-skill
   - Key takeaways used:
     - HEARTBEAT command contract supports exact no-op token
     - heartbeat behavior should remain deterministic and lightweight

## How these sources were applied

- Converted docs guidance into a production template (`heartbeat-template.md`).
- Added decision rules for cron handoff in `SKILL.md` and `qa-checklist.md`.
- Added concrete use-case patterns in `use-cases.md`.
