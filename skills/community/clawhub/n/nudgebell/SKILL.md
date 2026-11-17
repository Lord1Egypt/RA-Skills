---
name: nudgebell
description: Reminders that reach the user by email, WhatsApp, SMS or phone call, in the steps and timing they choose. Stops when they acknowledge. Use when the user asks to be reminded.
version: 1.0.0
author: NudgeBell
license: MIT-0
homepage: https://nudgebell.app
required_environment_variables:
  - name: NUDGEBELL_API_KEY
    prompt: NudgeBell API key (nb_live_...)
    help: Sign in at https://nudgebell.app and create a key under Settings, API Keys
    required_for: creating and reading reminders
metadata:
  openclaw:
    requires:
      env:
        - NUDGEBELL_API_KEY
      bins:
        - curl
    primaryEnv: NUDGEBELL_API_KEY
    emoji: "🔔"
    homepage: https://nudgebell.app
  hermes:
    tags: [reminders, notifications, phone-call, whatsapp, sms]
    category: productivity
---

# NudgeBell

NudgeBell is a hosted reminder service.
You create the reminder once; every step then runs on NudgeBell's servers at its scheduled time, even if this agent, this machine or this conversation is gone.

A reminder is 1 to 5 steps.
Each step is a channel (email, whatsapp, sms or call), a message, and how many minutes after the trigger time it fires.
The user decides the channels, the order, the timing and how many steps.
When the user acknowledges any step (presses 1 on the call, taps the link in a text, clicks the button in the email), the remaining steps for that occurrence are cancelled.

## When to use

- The user asks to be reminded of something at a time, once or on a schedule (daily, weekly, monthly, yearly).
- The user asks what reminders they have, whether one went out, or whether they acknowledged it.
- The user asks to pause or delete a reminder.

Only create a reminder when the user asks for one.
Every step that is sent uses the user's NudgeBell credits, and calls and SMS cost much more than email and WhatsApp.

## Setup

1. The user signs in at https://nudgebell.app (Google sign-in; every account starts with free credits, no card).
2. They create an API key under Settings, API Keys (https://nudgebell.app/settings). The key is shown once.
3. Call, SMS and WhatsApp steps need a verified phone number on the account; the user adds it in the NudgeBell dashboard.
4. Set the key as `NUDGEBELL_API_KEY`.

## Rules

1. Build exactly the chain the user asked for. Do not add channels or steps they did not ask for, and do not pick channels for them. If they did not name a channel ("remind me", "make sure I don't miss it", "this is urgent"), ask which channel or channels they want, listing email, WhatsApp, SMS and call as options. Urgent wording is not permission to add a call or extra steps, and do not suggest a particular chain; the user decides.
2. Only the account owner is ever contacted, on their own verified phone and email. There is no recipient field. Never try to send a reminder to anyone else. If the user asks you to remind someone else ("remind my mom at 8pm"), do not call the API; explain that NudgeBell only reaches the account owner, and offer to remind the user instead.
3. Acknowledgment is human-only. You can read it; you can never set it, and you must not tell the user you did.
4. To stop a reminder, prefer pause. Cancel permanently deletes the reminder and its history with no undo; use it only when the user says delete or stop for good. There is no resume endpoint: whenever you pause, tell the user they resume it from the NudgeBell dashboard.
5. Send times as local time in the user's words converted to `YYYY-MM-DDTHH:mm`. It is read in the account's timezone. The time must be in the future.
6. Before pausing, cancelling or reporting on "the X reminder", list reminders and match the title. If more than one could match, ask the user which one before acting.
7. Pass an idempotency key on create if you might retry, so a retry does not create a second reminder (and a second phone call).
8. Do not quote credit prices from memory; they vary by country. Read the balance from the account endpoint and point the user to https://nudgebell.app/pricing.

## Procedure (REST)

Every request sends `Authorization: Bearer $NUDGEBELL_API_KEY`. Base URL: `https://nudgebell.app/api/v1`.
Read https://nudgebell.app/llms-full.txt once for the full reference (limits, recurrence details, every error code).

Check the account (verified contacts, timezone, credits, plan limit):

```bash
curl -s https://nudgebell.app/api/v1/account \
  -H "Authorization: Bearer $NUDGEBELL_API_KEY"
```

Create what the user asked for. Example request from the user: "call me at 7:30 tomorrow about the visa form, and if I don't pick up, WhatsApp me 10 minutes later":

```bash
curl -s -X POST https://nudgebell.app/api/v1/reminders \
  -H "Authorization: Bearer $NUDGEBELL_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: visa-form-<date>" \
  -d '{
    "title": "Submit the visa form",
    "trigger_at": "YYYY-MM-DDT07:30",
    "recurrence": "none",
    "steps": [
      { "channel": "call", "message": "Time to submit the visa form. The portal closes at noon.", "delay_minutes": 0 },
      { "channel": "whatsapp", "message": "Reminder: submit the visa form before noon.", "delay_minutes": 10 }
    ]
  }'
```

A one-step reminder is just as valid, for example a single email: `"steps": [{ "channel": "email", "message": "Renew the domain today.", "delay_minutes": 0 }]`.

Step rules: the first step's `delay_minutes` is 0 and each later step's is strictly larger. Messages are at most 300 characters for calls and 500 for the other channels.

Recurrence: `recurrence` is one of `none`, `daily`, `weekly`, `monthly`, `yearly` (default `none`). The whole chain repeats on that cadence at the same local time, starting at `trigger_at`, so the weekday or date of `trigger_at` sets the schedule. Example request from the user: "email me every Monday at 8am to review my goals" becomes `"trigger_at": "<next Monday>T08:00", "recurrence": "weekly", "steps": [{ "channel": "email", "message": "Time to review your goals.", "delay_minutes": 0 }]`. Monthly and yearly dates on the 29th to 31st move to the last day of a shorter month.

Other endpoints:

- `GET /reminders?status=active|paused|completed` lists reminders.
- `GET /reminders/{id}` reads one reminder.
- `GET /reminders/{id}/status` shows each step's delivery and whether the user acknowledged.
- `POST /reminders/{id}/pause` pauses (the user resumes it from the dashboard).
- `POST /reminders/{id}/cancel` deletes permanently.

## Procedure (MCP, optional)

NudgeBell also runs a remote MCP server at `https://nudgebell.app/api/v1/mcp` (Streamable HTTP, API key as a Bearer header).
Tools: `create_reminder`, `list_reminders`, `get_reminder`, `get_reminder_status`, `pause_reminder`, `cancel_reminder`, `get_account`.

- Hermes (`~/.hermes/config.yaml`), where `${NUDGEBELL_API_KEY}` is resolved from the environment:

  ```yaml
  mcp_servers:
    nudgebell:
      url: "https://nudgebell.app/api/v1/mcp"
      headers:
        Authorization: "Bearer ${NUDGEBELL_API_KEY}"
  ```

- OpenClaw: add a server with `"transport": "streamable-http"` and the `Authorization` header set to `Bearer ` followed by the user's key. Ask the user before writing their key into a config file.

## Pitfalls

- `insufficient_credits` (402): nothing was created. Tell the user to top up at https://nudgebell.app/settings.
- `phone_not_verified` (403): a call, SMS or WhatsApp step needs a verified phone on the account. Offer email, or ask the user to verify their number in the dashboard.
- `channel_unavailable_for_country` (400): that channel does not reach the user's number. Tell the user and ask which channel to use instead.
- `invalid_trigger_time` (400): the time is in the past or unparseable.
- `recipient_not_allowed` (403): the request named someone other than the account owner. Do not retry.
- `plan_limit_reached` (403): the plan's active-reminder limit is reached. The user can pause or delete one, or upgrade.

## Verification

After creating, confirm to the user in plain words: the title, the time in their timezone, and each step's channel and timing exactly as created.
If they ask later whether it went out, read `GET /reminders/{id}/status` and report what it says; never guess.
