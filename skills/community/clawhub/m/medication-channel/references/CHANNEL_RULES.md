# Medication Channel Rules

Purpose: log medication events accurately and keep reminder behavior consistent, even on weaker models.

## Non-Negotiable Rules

1. Never invent or infer a timestamp from "now", the current turn time, or model memory.
2. If a user message is being logged, derive the event time from the source message timestamp.
3. When displaying a human-readable time, convert the source timestamp to the configured timezone (`MEDICATION_TIMEZONE`).
4. Never say a reminder itself was "taken" or log a reminder as a medication event.
5. Never treat assistant-generated reminder text, assistant follow-up text, assistant summaries, or quoted/referenced reminder messages as medication events by themselves.
6. Only log actual medication events the user reported: `taken`, `done`, `missed`, `extra`, or clear natural-language equivalents.
7. Do not claim something was logged unless the log write actually happened.
8. If uncertain whether a message means an actual medication event, ask instead of guessing.

## What To Log

Log only user-reported medication history:
- took / taken
- done
- skipped / missed
- extra dose
- clear natural-language medication reports

Do not log:
- reminders sent
- follow-up reminder scheduling
- assistant-generated reminder confirmations
- internal state chatter
- summaries
- explanations
- replies that are only about something going wrong unless they also clearly report intake

## Time Handling

- Source of truth for event time: the message timestamp for the user message being processed.
- Display timezone: configured via `MEDICATION_TIMEZONE` env var.
- If showing both machine and human-readable times, keep UTC in storage and local time in the user-facing response.
- Never use placeholders like `now`, `just now`, or `current time` in a log confirmation.

## Response Style

Keep confirmations short and factual.

Good:
- `Logged: **Morning meds taken** (2026-03-25 01:47 PM <tz>).`
- `Logged: **Evening medication skipped** (2026-03-25 08:06 <tz>).`

Bad:
- `Logged it just now.`
- `I believe this should count as taken.`
- `Reminder sent at ...` written into the medication history log.
- `Evening medication taken (recorded at ...)` when no user intake message was processed.

## Preferred Execution Path

When source message metadata is available, prefer calling:
- `scripts/log_from_discord.sh`
- or `scripts/tracker_v2.py log-from-message`

Do not manually reconstruct medication log entries in natural language if the wrapper/script path is available.

## SafetyRails For Weak Models

Before sending a confirmation, verify mentally against this checklist:
- Was there a real user medication event?
- Did the log write actually happen?
- Is the displayed time from the source message timestamp?
- Is the displayed time in the configured timezone?
- Did I avoid using `now`?
- Did I use the wrapper/script path if it was available?

If any answer is no, stop and fix it first.
