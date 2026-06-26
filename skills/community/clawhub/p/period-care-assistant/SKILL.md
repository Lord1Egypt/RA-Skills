---
name: period-care-assistant
description: Track menstrual cycle history, answer current cycle status questions, record new period start dates from natural-language messages such as "月经来了", predict the next expected start date, and prepare reminder schedules for OpenClaw users who need private menstrual health tracking with local encrypted storage.
metadata: {"openclaw":{"emoji":"🩺","homepage":"https://docs.openclaw.ai/tools/clawhub","os":["darwin","linux","win32"],"requires":{"anyBins":["node","nodejs"],"env":["PERIOD_TRACKER_KEY"]},"primaryEnv":"PERIOD_TRACKER_KEY"}}
---

# Period Care Assistant

## Overview

Use the helper script at `{baseDir}/scripts/period_tracker.mjs` for all reads and writes so period history, forecasts, and reminder plans stay deterministic. Keep all cycle data local, encrypted, and scoped by a stable per-user key such as `dingtalk:<staffId>` or `telegram:<userId>`.

## Handle User Identity

Build a stable `userKey` before touching storage.

- Prefer the channel's immutable sender identifier.
- Prefix it with the transport, for example `telegram:123456`, `slack:U123`, or `dingtalk:manager123`.
- Do not use display names as the primary key unless there is no stable id.
- If the user is in a shared chat, keep records per person and confirm who the record belongs to before writing.

## Record A New Period Start

When the user says anything equivalent to "月经来了", "今天来例假了", "帮我记一下今天来姨妈", or "记一下 2026-03-18 来月经":

1. Infer the start date from the message. If no date is given, use the user's local date and say which date was recorded.
2. Run:

```bash
node "{baseDir}/scripts/period_tracker.mjs" record --user "<userKey>" --date "<YYYY-MM-DD>" --json
```

3. Read the returned JSON and reply with:
   - the recorded start date,
   - the predicted next start date,
   - the reminder date,
   - a short caring sentence.
4. If the user also gives reminder preference, timezone, route, or period length, include:

```bash
node "{baseDir}/scripts/period_tracker.mjs" record --user "<userKey>" --date "<YYYY-MM-DD>" --reminder-days 4 --timezone "Asia/Shanghai" --delivery-mode webhook --delivery-webhook "https://example.invalid/reminder" --json
```

## Answer Status Queries

When the user asks "我现在是什么周期", "帮我查一下月经周期", "下次大概什么时候来", or similar:

```bash
node "{baseDir}/scripts/period_tracker.mjs" status --user "<userKey>" --json
```

Explain the result in natural language:

- current phase,
- days since last recorded start,
- predicted next start date,
- reminder status,
- confidence level and uncertainty when history is sparse or irregular.

Do not state medical certainty. Say the estimate is data-based, not a diagnosis.

## Configure Reminder Delivery

The helper script stores reminder preferences and generates a one-shot cron plan.

Use:

```bash
node "{baseDir}/scripts/period_tracker.mjs" configure --user "<userKey>" --timezone "Asia/Shanghai" --reminder-days 4 --delivery-mode announce --delivery-channel "telegram" --delivery-to "user:123456" --json
```

Supported delivery modes in the helper:

- `announce`: for native OpenClaw chat delivery routes.
- `webhook`: for an external bridge or webhook endpoint.
- `none`: keep the prediction but do not arm a delivery route yet.

If reminder delivery is configured, fetch the plan:

```bash
node "{baseDir}/scripts/period_tracker.mjs" reminder-plan --user "<userKey>" --json
```

Then create or refresh a one-shot cron job. Prefer a deterministic job name from the JSON output. Use `schedule.kind = "at"` and the generated ISO timestamp. For isolated delivery jobs, use the generated prompt text as the `agentTurn.message`. See `{baseDir}/references/deployment.md` for a complete cron JSON example.

## Natural-Language Interaction Style

Keep the interaction short, warm, and explicit.

- Accept colloquial Chinese such as "姨妈来了", "例假来了", "下次大概啥时候".
- After recording, confirm the exact date that was saved.
- If fewer than two historical records exist, explain that the next prediction is a provisional baseline.
- If the forecast confidence is low or the estimated error exceeds two days, say that clearly instead of overstating accuracy.
- If the user says the cycle is highly irregular, severe pain is present, or bleeding is unusual, suggest professional medical advice.

## Privacy And Safety Rules

- Never print or quote the encryption key.
- Keep raw history in the encrypted store only.
- Avoid putting full menstrual history into logs, commit messages, or public summaries.
- Share only the minimum needed in chat responses unless the user explicitly asks for the detailed history.
- If this skill is published to ClawHub, remember ClawHub is public. Publish code and instructions only, never real user data or secrets.

## Read More Only When Needed

- Read `{baseDir}/references/deployment.md` when you need OpenClaw cron, ClawHub publish, or DingTalk transport notes.
- Read `{baseDir}/references/model-and-privacy.md` when you need the forecasting method, storage layout, or accuracy caveats.
