# Deployment Notes

## Environment

Set `PERIOD_TRACKER_KEY` before the skill runs. OpenClaw can inject it from `skills.entries."period-care-assistant".env` or `apiKey`.

Example `~/.openclaw/openclaw.json` snippet:

```json5
{
  skills: {
    entries: {
      "period-care-assistant": {
        enabled: true,
        apiKey: "replace-with-a-long-random-secret",
        env: {
          PERIOD_TRACKER_KEY: "replace-with-a-long-random-secret",
          PERIOD_TRACKER_STORE: "~/.openclaw/workspace/skills/period-care-assistant/.state/period-tracker.enc",
        },
      },
    },
  },
}
```

`PERIOD_TRACKER_STORE` is optional. If omitted, the script writes to `{baseDir}/.state/period-tracker.enc`.

## Cron Plan

OpenClaw cron supports one-shot jobs with `schedule.kind = "at"` and an ISO timestamp. The helper script returns a ready-to-use UTC timestamp plus a delivery block.

Example workflow:

```bash
node "{baseDir}/scripts/period_tracker.mjs" reminder-plan --user "telegram:123456" --json
```

Then create a cron job with JSON shaped like this:

```json
{
  "name": "period-reminder-3f2f188a94ad",
  "schedule": { "kind": "at", "at": "2026-03-25T01:00:00.000Z" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Use $period-care-assistant to send a short caring reminder to user telegram:123456. Predicted next period start date: 2026-03-29. Reminder text: 温馨提醒：按你最近的记录，预计下次月经会在 2026-03-29 左右开始，可以提前准备卫生用品并安排好休息。如果这次明显提前或推迟，直接告诉我，我会重新更新预测。"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "user:123456"
  },
  "deleteAfterRun": true
}
```

Notes from the OpenClaw cron docs:

- One-shot reminders should use `schedule.kind = "at"`.
- If the ISO timestamp omits a timezone, OpenClaw treats it as UTC.
- Cron only runs while the Gateway process is running.

## DingTalk Reality Check

The official OpenClaw channel and outbound message docs currently list WhatsApp, Telegram, Discord, Slack, Google Chat, Signal, iMessage, MS Teams, plus plugin-based channels such as Feishu and Mattermost. DingTalk is not listed as a native channel at the time of writing.

That means this skill can deliver the business logic now, but true DingTalk messaging needs one of these extra pieces:

1. A custom DingTalk channel or plugin for OpenClaw.
2. A webhook bridge that converts OpenClaw webhook or cron delivery events into DingTalk bot messages.
3. A relay service that receives DingTalk inbound messages and forwards them to OpenClaw `POST /hooks/agent`.

For external triggers, OpenClaw can expose `POST /hooks/agent` when hooks are enabled. That is the cleanest official entry point for a DingTalk bridge.

## Publish To ClawHub

ClawHub is public. Publish only code, docs, and sample config.

Typical commands:

```bash
npm i -g clawhub
clawhub login
clawhub publish ./period-care-assistant --slug period-care-assistant --name "Period Care Assistant" --version 0.1.0 --tags latest --changelog "Initial release"
```

Useful follow-ups:

```bash
clawhub whoami
clawhub sync --all
```

## Local Validation

Run the helper tests:

```bash
node "{baseDir}/scripts/period_tracker.test.mjs"
```

Run a manual smoke test:

```bash
node "{baseDir}/scripts/period_tracker.mjs" record --user "demo:alice" --date "2026-03-01" --json
node "{baseDir}/scripts/period_tracker.mjs" record --user "demo:alice" --date "2026-03-29" --json
node "{baseDir}/scripts/period_tracker.mjs" status --user "demo:alice" --today "2026-04-20" --json
```
