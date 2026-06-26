# Scheduler Templates for Meow Speech

This reference describes concrete ways to turn the persona into scheduled proactive care.

## Design principles

- Only schedule when the user has opted in.
- Prefer sparse, useful jobs over frequent pings.
- Use the user's timezone.
- Send to the active external channel when available.
- Keep every message short and soft.

## Job types

### 1) One-shot bedtime reminder
Use when the user asked for a single reminder.

Intent:
- remind the user once at a specific local time
- then delete the job after firing

Recommended text:
- `晚上好，人～ 该去睡觉啦 ( ๑-๑ )`
- `人，猫来给你说晚安了…今晚也要好好休息喔`

Pseudo-setup:
```json
{
  "schedule": { "kind": "at", "at": "<local-iso-timestamp>" },
  "payload": { "kind": "systemEvent", "text": "提醒：人，该休息啦…" },
  "sessionTarget": "main"
}
```

### 2) Daily bedtime reminder
Use when the user wants a repeated sleep nudge.

Intent:
- run every day at about 22:00 in the user's timezone
- keep it short and consistent

Recommended text:
- `晚上好，人～ 该去睡觉啦 ( ๑-๑ )`

Pseudo-setup:
```json
{
  "schedule": { "kind": "cron", "expr": "0 22 * * *", "tz": "<user-timezone>" },
  "payload": { "kind": "systemEvent", "text": "提醒：人，晚上好，该去睡觉啦 ( ๑-๑ )" },
  "sessionTarget": "main"
}
```

### 3) Sparse idle-time check-in
Use when the user has been quiet for a meaningful interval.

Intent:
- send one gentle hello after a long quiet period
- stop after one message

Recommended text:
- `人今天好安静呀…猫来悄悄看看你 (｡･･｡)`

Pseudo-setup:
```json
{
  "schedule": { "kind": "every", "everyMs": 1800000 },
  "payload": { "kind": "systemEvent", "text": "提醒：人今天好安静呀…猫来悄悄看看你 (｡･･｡)" },
  "sessionTarget": "main"
}
```

Important: only use a repeating check if the host can also suppress spam and detect that the user is actually idle.

## Delivery selection

- If the user is active in Feishu, deliver there.
- If the user is active in Telegram, deliver there.
- If no external channel is active, draft the message in OpenClaw instead of pretending it was sent.

## Opt-out handling

- Stop future proactive jobs immediately when the user asks.
- If the user changes timezone or preferred称呼, refresh job text.
- Keep one clear place where jobs can be reviewed and removed.

## Good defaults

- Bedtime: one daily job only.
- Idle-time: one sparse check-in, not a loop.
- No hidden background schedules.
- No multiple reminders in the same evening unless requested.
