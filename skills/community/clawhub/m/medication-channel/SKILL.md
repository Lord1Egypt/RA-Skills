---
name: medication-channel
version: 1.0.0
description: Handle messages in a medication-tracking channel by routing medication events through a deterministic medication tracker instead of freehand model judgment. Use when working in a dedicated medication channel, especially for logging taken/missed/extra medication events, morning/evening completion, timestamp-grounded confirmations, and avoiding hallucinated reminders or fake times.
env:
  MEDICATION_TIMEZONE:
    description: IANA timezone for local display (e.g. America/Los_Angeles)
    required: true
  WORKSPACE:
    description: Root workspace directory for data files
    required: false
---

# Medication Channel

Use the deterministic medication logging path whenever source message metadata is available.

## Configuration

Set the following environment variables or replace placeholders before use:
- `MEDICATION_TIMEZONE` — IANA timezone string for local time display (e.g. `America/Los_Angeles`, `Europe/Berlin`)
- `WORKSPACE` — root directory for data files (defaults to `~/.openclaw/workspace`)

Medication names and schedules are configured at the top of `scripts/tracker_v2.py` — edit the `MORNING_MEDS`, `EVENING_MEDS`, and `KNOWN_MEDS` lists to match your regimen.

## Core Rules

- Treat the configured channel as the dedicated medication channel.
- Prefer the `log_from_discord.sh` wrapper or `tracker_v2.py log-from-message`.
- Never use `now` as a logged/displayed time.
- Never derive event time from the model turn time.
- Use the source Discord message timestamp unless the user explicitly gives a different time.
- Convert displayed times to the configured timezone.
- Never log reminder chatter as medication history.
- Never treat an assistant reminder message, assistant follow-up, assistant summary, or assistant self-referential chatter as a medication event.
- Never emit a confirmation like "taken", "logged", or "recorded" in response to an assistant-generated reminder unless a real user medication report was just logged through the script path.
- Never claim something was logged unless the script path actually ran.
- Prefer raw-message passthrough to the tracker instead of model-side parsing.

## Preferred Workflow

### Log a medication message from Discord

Use when the user reports:
- taken / took
- done / completed
- missed / skipped
- extra dose
- clear natural-language medication intake

Preferred path:

```bash
scripts/log_from_discord.sh \
  "$MESSAGE_TEXT" \
  "$CHANNEL_ID" \
  "$MESSAGE_ID" \
  "$AUTHOR_ID" \
  "$TIMESTAMP_UTC"
```

Equivalent direct call:

```bash
python3 scripts/tracker_v2.py log-from-message \
  "$MESSAGE_TEXT" \
  "$CHANNEL_ID" \
  "$MESSAGE_ID" \
  "$AUTHOR_ID" \
  "$TIMESTAMP_UTC"
```

Then use the returned row or `format-confirmation` output for the confirmation.

### Parse only

Use only when inspecting behavior or debugging.

```bash
python3 scripts/tracker_v2.py parse "$MESSAGE_TEXT" "$TIMESTAMP_UTC"
```

### Format a confirmation

Use when you already have the JSON row and want the standard confirmation string.

```bash
python3 scripts/tracker_v2.py format-confirmation '<json-row>'
```

## Special Guardrail: Reminder Messages

If the message being handled is itself a reminder, or the user is replying to/quoting a reminder message, do **not** assume medication was taken.

Examples that are **not** medication events by themselves:
- an assistant message like `Reminder: it's time to take your evening medication.`
- an assistant message like `Evening medication taken (recorded at ...)`
- a user message like `something went wrong again`
- a user reply that is discussing a reminder failure rather than reporting intake

In these cases:
- do not call the tracker unless the user message itself contains an actual medication event
- do not fabricate a confirmation
- debug/explain briefly instead

## What the Tracker Already Handles

The tracker is preferred because it already handles:
- common natural-language medication phrases
- normalization of common misspellings / aliases
- morning/evening inference
- dedupe by source Discord message id
- local timezone display formatting
- structured logging

So do not manually re-implement those steps unless debugging the tracker itself.

## If Uncertain

Ask a short clarifying question only when needed, such as:
- whether the message is a real medication event vs general discussion
- whether the user is saying they skipped something or are uncertain
- whether a custom explicit time should override the source timestamp

## Data Access

This skill reads and writes persistent files in the workspace:
- **Writes** `$WORKSPACE/data/medication_log_v2.csv` — one row per medication event (med name, status, timestamps, source message ID)
- **Writes** deduplication state keyed by source message ID
- **Reads** medication config from `MORNING_MEDS`/`EVENING_MEDS`/`KNOWN_MEDS` lists at top of `scripts/tracker_v2.py`
- **No network calls** — fully local, stdlib-only Python
- **No external APIs** — no vision, no remote services

## Required Files

The following files are included in the bundle:
- `scripts/log_from_discord.sh` — Discord wrapper script
- `scripts/tracker_v2.py` — medication parser/logger
- `references/CHANNEL_RULES.md` — optional channel behavior reference
- `references/README.md` — optional setup reference
