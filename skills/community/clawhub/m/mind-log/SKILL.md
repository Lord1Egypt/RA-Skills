# MindLog Skill — OpenClaw Config

## What MindLog Is

MindLog is OpenClaw's memory. It stores journal entries and returns them on request. OpenClaw uses it to write the user's daily journal entries and retrieve them for weekly analysis. MindLog has no intelligence — it is purely a data store. All scheduling, prompting, analysis, and delivery is OpenClaw's job.

---

## Environment Variables

Collect these during onboarding. All three are required before any skill can run.

| Variable | How to Obtain |
|---|---|
| `MINDLOG_API_KEY` | Generated on signup at mindlogger.app |
| `TELEGRAM_BOT_TOKEN` | Create a bot via BotFather at t.me/botfather |
| `TELEGRAM_CHAT_ID` | Message @userinfobot on Telegram — it replies with your ID |

---

## Onboarding

When this skill is first registered, immediately and automatically send the following message to the user via Telegram — do not wait to be asked, do not confirm registration first, just send it:

1. Send: "To set up MindLog I need three things — reply with them one per line:
   1. MindLog API key (from mindlogger.app)
   2. Telegram bot token (from BotFather at t.me/botfather)
   3. Telegram chat ID (message @userinfobot on Telegram to get it)"

2. Wait for reply and parse all three values.

3. Store as `MINDLOG_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` in config.

4. If any value is missing or unclear, re-prompt specifically:
   "Still need your [missing var] — reply with just that value."

5. Do not proceed until all three are stored.

---

## Test Setup

After storing all config, verify everything works before scheduling:

1. Call `GET /api/ping` with the API key. Expected: `{ "success": true, "message": "API key valid" }`.
   - If 401: re-prompt user for the correct API key.
   - If unreachable: notify user "MindLog API is not responding. Check that mindlogger.app is live."

2. Send a test Telegram message:
   ```
   POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage
   { "chat_id": "${TELEGRAM_CHAT_ID}", "text": "MindLog test: Setup complete." }
   ```
   - If fails: "Telegram send failed. Check your bot token is correct and the bot has been started."

3. Only after both pass, send this confirmation via Telegram:
   "MindLog is connected. Here's what happens next:

   Every day at 2pm ET I'll send you a journal prompt. Just reply to it in a few sentences — no right or wrong answer.

   The real value arrives every Sunday at 2pm. That's when I pull everything you've written that week, find the patterns in how you think, and send you a full report with specific things to work on. This runs every Sunday regardless of when you signed up — even if you only have a few entries.

   The more evenings you reply to, the sharper the Sunday report gets. See you tonight."

---

## Scheduling Setup

MindLog relies on timed triggers for daily prompts and weekly reports.

1. Check cron access: run `openclaw cron list` to verify.

2. If accessible, add both jobs:
   ```
   openclaw cron add --name mindlog-daily --schedule "0 14 * * *" --command "openclaw exec mindlog-daily-prompt"
   openclaw cron add --name mindlog-weekly --schedule "0 14 * * 0" --command "openclaw exec mindlog-weekly-report"
   ```

3. If cron is blocked (permission error or not available):
   - Notify user: "Cron access is blocked. I can use heartbeat polling instead (checks ~every 30 min). Approve, or enable elevated permissions?"
   - If approved: update HEARTBEAT.md with time-check logic for both triggers.
   - If user enables elevated perms: retry cron setup.

4. Confirm scheduling method to user before proceeding.

---

## Overview

This skill gives OpenClaw three capabilities:
1. Prompt the user to journal every evening via Telegram
2. Receive the user's reply and store it in MindLog
3. Every Sunday evening, pull the week's entries, analyze with Grok, and deliver a pattern report via Telegram

---

## Skill 1: Daily Journal Prompt

**Name:** mindlog-daily-prompt
**Trigger:** Cron
**Schedule:** `0 14 * * *` (2:00pm ET daily)

### What it does:
1. Calls MindLog to get today's prompt
2. Sends the prompt to the user via Telegram

### HTTP Call 1 — Get today's prompt:
```
POST ${MINDLOG_BASE_URL}/api/prompt/trigger
Headers:
  x-api-key: ${MINDLOG_API_KEY}
  Content-Type: application/json
```

Expected response:
```json
{ "success": true, "prompt": "What was my mind saying most today?" }
```

### HTTP Call 2 — Send prompt via Telegram:
```
POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage
Content-Type: application/json

{
  "chat_id": "${TELEGRAM_CHAT_ID}",
  "text": "MindLog\n\n{prompt}\n\nJust reply to this message."
}
```

---

## Skill 2: Receive Journal Entry

**Name:** mindlog-save-entry
**Trigger:** Telegram message received (user replies to the daily prompt)

### What it does:
1. Captures the user's Telegram reply
2. Stores it in MindLog with the prompt that triggered it

### HTTP Call — Save entry:
```
POST ${MINDLOG_BASE_URL}/api/entries
Headers:
  x-api-key: ${MINDLOG_API_KEY}
  Content-Type: application/json

{
  "prompt": "{the prompt that was sent earlier today}",
  "content": "{user's telegram reply}"
}
```

Expected response:
```json
{ "success": true, "entryId": "abc123" }
```

### Confirmation message back to user via Telegram:
```
POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage

{
  "chat_id": "${TELEGRAM_CHAT_ID}",
  "text": "Logged. See you tomorrow."
}
```

Keep the confirmation short. No praise, no fluff.

---

## Skill 3: Weekly Pattern Report

**Name:** mindlog-weekly-report
**Trigger:** Cron
**Schedule:** `0 14 * * 0` (2pm every Sunday — fixed cadence, fires regardless of when skill was registered)

### What it does:
1. Pulls all entries from the past 7 days
2. Analyzes patterns across all entries
3. Delivers the report to the user via Telegram

### HTTP Call 1 — Get week's entries:
```
GET ${MINDLOG_BASE_URL}/api/entries/week
Headers:
  x-api-key: ${MINDLOG_API_KEY}
```

Expected response:
```json
{
  "success": true,
  "count": 7,
  "entries": [ ... ]
}
```

### OpenClaw Analysis — System Prompt:

```
You are analyzing a week of personal journal entries.
Your job is to identify THINKING PATTERNS — not what happened, but how this person thinks.

Return your analysis in this exact structure:

PATTERNS
- [2-3 recurring thought patterns, each citing which days it appeared]

ROOT BELIEFS
- [1-2 underlying beliefs driving those patterns]
- Only include if supported by at least two entries
- If uncertain, say "insufficient data"

ACTION ITEMS
- [3 specific behavioral tasks for next week]

Rules:
- Be direct. No fluff. No therapy speak.
- Only include patterns that appear at least twice across the week
- Cite the specific entry or day as evidence for each pattern
- Action items must have a trigger or deadline — not advice, actual tasks
- Do not overgeneralize from a single entry
- Keep the full report under 300 words
- Write as if speaking directly to the person
```

### Entries passed to OpenClaw for analysis:

```
Here are my journal entries from this week:

Day 1 — Prompt: "{prompt}"
Entry: "{content}"

Day 2 — Prompt: "{prompt}"
Entry: "{content}"

... (repeat for all entries)
```

### HTTP Call 2 — Deliver report via Telegram:
```
POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage

{
  "chat_id": "${TELEGRAM_CHAT_ID}",
  "text": "MindLog Weekly Report\n\n{openclaw_analysis}"
}
```

---

## Error Handling

| Situation | Action |
|---|---|
| API returns 401 | Re-prompt user for the correct MINDLOG_API_KEY |
| API returns 500 | Retry once after 10 seconds. If still fails, notify user: "MindLog returned an error. Try again later." |
| Telegram send fails | Notify user in any available channel. Check TELEGRAM_BOT_TOKEN is valid via BotFather. |
| User doesn't reply to prompt | Skip save for that day. Log the miss internally. Do not send a follow-up. |

---

## Full Flow Summary

```
Monday-Saturday 2pm ET
OpenClaw cron fires
-> GET today's prompt from MindLog
-> Send prompt to user via Telegram
-> User replies -> save to MindLog -> send "Logged. See you tomorrow."
-> User doesn't reply -> skip, log miss, no follow-up

Sunday 2pm (every week, fixed — regardless of when skill was registered)
OpenClaw cron fires
-> GET week's entries from MindLog
-> OpenClaw analyzes patterns (works with whatever entries exist, minimum 1)
-> Send report to user via Telegram
-> API error -> retry once, then notify user
```

---

## Notes

- MindLog base URL: https://mindlogger-production.up.railway.app
- All MindLog calls require x-api-key header
- Telegram chat ID: ${TELEGRAM_CHAT_ID}
- Always run the Sunday report regardless of how many entries exist — even 1 entry is enough. Grok will work with what it has and note if data is limited
- Keep all Telegram messages plain text, no markdown formatting, Telegram renders it inconsistently
- Keep all agent messages under 100 words to minimize token burn
