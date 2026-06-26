# Intent-to-Spec Examples

Use with:
- `scripts/parse_nl_intent.py`
- `scripts/intent_to_cron_spec.py`

## Pipeline

```bash
printf '给我设置一个3分钟的闹钟，3分钟后提醒我，我在泡面' \
  | python3 scripts/parse_nl_intent.py \
  | python3 scripts/intent_to_cron_spec.py
```

## Example 1 — Reminder

Input intent:
- `intentType: reminder`
- `scheduleType: at`
- `interval: 3m`

Output spec shape:
- `sessionTarget: main`
- `payload.kind: systemEvent`
- `schedule.kind: at`
- `notes.deriveAtFromNow: 3m`
- `needsReview: true` until exact `at` timestamp is resolved

## Example 2 — Session injection loop

Input intent:
- `intentType: session-injection`
- `scheduleType: every`
- `interval: 10m`
- `targetScope: current-session`

Output spec shape:
- `sessionTarget: isolated`
- `payload.kind: agentTurn`
- `delivery.mode: none`
- `notes.sessionBindingRequired: true`

## Example 3 — Scheduled visible worker

Input intent:
- `intentType: scheduled-worker`
- `deliveryMode: announce`

Output spec shape:
- `sessionTarget: isolated`
- `delivery.mode: announce`
- `delivery.channel: null`
- `delivery.to: null`
- `needsReview: true`

## Design rule

This transformer should be conservative.

If exact time, explicit target, or current-session binding is still ambiguous, keep placeholders and return `needsReview: true` instead of silently guessing.
