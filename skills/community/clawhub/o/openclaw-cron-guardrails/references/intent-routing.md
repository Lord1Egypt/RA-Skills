# Intent Routing for Natural-Language Cron Requests

This skill is primarily for upstream agents, not for direct human CLI usage.

When the user speaks in natural language, map the request into one of these intent buckets before choosing cron structure.

## Intent bucket 1 — Reminder / alarm

Typical phrases:
- `remind me`
- `set an alarm`
- `remind me in X minutes`
- `remind me tomorrow morning`
- `alarm`

Default mapping:
- `sessionTarget: main`
- `payload.kind: systemEvent`
- one-shot schedule preferred

Do not overcomplicate these into isolated jobs unless the user explicitly wants background agent execution.

## Intent bucket 2 — Repeat loop / bounded repeat

Typical phrases:
- `every X minutes`
- `every X hours`
- `run every X minutes`
- `run N times`
- `for N runs`
- `loop`
- `tick`

Default mapping:
- reminder-like repeat → `main`
- worker-like repeat → `isolated + delivery.mode:none`

Important field extraction:
- interval
- total runs or stop condition
- whether output should be visible

## Intent bucket 3 — Session/thread prompt injection or push loop

Typical phrases:
- `inject a prompt into the current session`
- `inject a prompt into the current agent`
- `push the current thread every X minutes`
- `keep pushing this thread`
- `push it as far as you can`

Default mapping:
- treat as session-aware scheduled agent action
- preserve current-session / current-thread semantics explicitly
- do not rely on `channel=last` when delivery matters

If the request is really “nudge the current agent/thread repeatedly”, prefer a pattern that binds explicitly to the current context.

## Intent bucket 4 — Scheduled worker / scan / monitor / digest

Typical phrases:
- `daily`
- `nightly`
- `scheduled`
- `scan`
- `watch`
- `monitor`
- `check periodically`
- `summarize daily`

Default mapping:
- internal work → `isolated + delivery.mode:none`
- visible report → `isolated + explicit delivery.channel + delivery.to`

## Recommended extraction schema

Before using scripts or rendering commands, normalize the request into this shape:

```json
{
  "intentType": "reminder | repeat-loop | session-injection | scheduled-worker",
  "scheduleType": "at | every | cron",
  "timeExpression": "natural-language time or cron expression",
  "interval": "optional",
  "runCount": 0,
  "stopCondition": "optional",
  "targetScope": "main | current-session | current-thread | explicit-target | internal-worker",
  "deliveryMode": "none | announce | webhook",
  "userVisible": true,
  "taskText": "what the job should do"
}
```

Then map that normalized form into the concrete cron spec.

## Trigger guidance for skill activation

This skill should trigger not only on explicit `cron` mentions, but also on natural-language scheduling requests such as:
- reminders
- alarms
- recurring nudges
- prompt injections into the current session/thread
- daily/weekly/nightly scans and summaries

If the request is obviously about scheduling future or repeated agent action, this skill is likely relevant even if the word `cron` never appears.
