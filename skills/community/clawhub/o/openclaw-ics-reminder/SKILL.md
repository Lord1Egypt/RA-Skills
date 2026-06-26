---
name: openclaw-ics-reminder
description: ICS-backed reminder operations through the reminder worker API. Use when the user asks to create, list, cancel, or rotate reminder-style calendar items such as "remind me tomorrow at 3pm", "set a recurring reminder", "list my reminders", or "rotate my calendar feed token".
homepage: https://github.com/Cute-angel/ics-reminder-skill
metadata: {"clawdbot":{"emoji":"📅","skillKey":"ics-reminder","requires":{"bins":["node"],"env":["REMINDER_API_TOKEN","REMINDER_API_BASE_URL"]},"primaryEnv":"REMINDER_API_TOKEN"}}
---

# ICS Reminder
Use this skill when the user intent is to create or manage a reminder-like event that should appear in a subscribed calendar feed.


Reminder operations through `scripts/reminder-client.mjs`.

## Create a reminder

```bash
node {baseDir}/scripts/reminder-client.mjs create --stdin
```

Required create fields:
- `title`
- `start_at`
- `timezone`

Optional create fields:
- `notes`
- `location`
- `url`
- `all_day`
- `rrule`
- `alarm_offset_minutes`
- `source_text`
- `idempotency_key`

## List reminders

```bash
node {baseDir}/scripts/reminder-client.mjs list
```

## Delete a reminder

```bash
node {baseDir}/scripts/reminder-client.mjs delete "<id>"
```

## Rotate ICS feed token

```bash
node {baseDir}/scripts/reminder-client.mjs rotate
```

## Notes

- Read `REMINDER_API_TOKEN` from the environment.
- Read `REMINDER_API_BASE_URL` from the environment.
- If `REMINDER_API_BASE_URL` is missing, stop and ask for configuration instead of guessing a local or remote endpoint.
- Always use `scripts/reminder-client.mjs`; do not embed raw HTTP calls in the skill.
- Ask a concise follow-up only when date, time, timezone, or recurrence is missing or ambiguous.
- Keep raw user text inside the JSON request body only; do not splice it into shell flags, URLs, or command fragments.
- Read [references/time-parsing-rules.md](references/time-parsing-rules.md) for ambiguous dates, recurrence, all-day reminders, or past times.
- Read [references/api-contract.md](references/api-contract.md) before calling the helper script.
- Read [references/openclaw-config.md](references/openclaw-config.md) when the user needs help wiring the skill into `~/.openclaw/openclaw.json`.
- Confirm normalized schedule details in the final response and never reveal bearer tokens or raw secret values.
