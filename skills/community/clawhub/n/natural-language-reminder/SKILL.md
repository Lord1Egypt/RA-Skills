---
name: remind-me
description: Set reminders using natural language. Automatically creates one-time cron jobs and logs to markdown.
metadata: {"clawdbot":{"emoji":"⏰","requires":{"bins":["bash","date","jq","openclaw"]},"config":{"TO":{"required":true,"prompt":"What is your recipient ID? (e.g. Telegram chat ID — send /start to @userinfobot to find it)"},"CHANNEL":{"required":false,"default":"telegram","prompt":"Delivery channel? (telegram / slack / etc.)"},"TIMEZONE":{"required":true,"prompt":"What is your timezone? (e.g. Europe/Kyiv, America/New_York — see https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)"},"REMINDERS_FILE":{"required":false,"default":"~/reminders.md","prompt":"Where to store the reminder log? (default: ~/reminders.md)"}}}}
---

# Remind Me

Natural language reminders that fire automatically. Uses cron for scheduling, markdown for logging.

## Usage

### One-Time Reminders
Just ask naturally:
- "Remind me to pay for Gumroad later today"
- "Remind me to call mom tomorrow at 3pm"
- "Remind me in 2 hours to check the oven"
- "Remind me next Monday at 9am about the meeting"

### Recurring Reminders
For repeating reminders:
- "Remind me every hour to stretch"
- "Remind me every day at 9am to check email"
- "Remind me every Monday at 2pm about the meeting"
- "Remind me weekly to submit timesheet"

## How It Works

1. Parse the time from your message
2. Create a one-time cron job with `--at`
3. Log to `$REMINDERS_FILE` (default: `~/reminders.md`) for history
4. At the scheduled time, you get a message

## Time Parsing

### One-Time Reminders

**Relative:**
- "in 5 minutes" / "in 2 hours" / "in 3 days"
- "later today" → 17:00 today
- "this afternoon" → 17:00 today
- "tonight" → 20:00 today

**Absolute:**
- "tomorrow" → tomorrow 9am
- "tomorrow at 3pm" → tomorrow 15:00
- "next Monday" → next Monday 9am
- "next Monday at 2pm" → next Monday 14:00

**Dates:**
- "January 15" → Jan 15 at 9am
- "Jan 15 at 3pm" → Jan 15 at 15:00
- "2026-01-15" → Jan 15 at 9am
- "2026-01-15 14:30" → Jan 15 at 14:30

### Recurring Reminders

**Intervals:**
- "every 30 minutes"
- "every 2 hours"

**Daily:**
- "daily at 9am"
- "every day at 3pm"

**Weekly:**
- "weekly" → every Monday at 9am
- "every Monday at 2pm"
- "every Friday at 5pm"

## Reminder Log

All reminders are logged to `$REMINDERS_FILE` (default: `~/reminders.md`):

```markdown
- [scheduled] 2026-01-06 17:00 | Pay for Gumroad (id: abc123)
- [recurring] every 2h | Stand up and stretch (id: def456)
- [recurring] cron: 0 9 * * 1 | Weekly meeting (id: ghi789)
```

**Status:**
- `[scheduled]` — one-time reminder waiting to fire
- `[recurring]` — repeating reminder (active)
- `[sent]` — one-time reminder already delivered

## Setup

During installation, the bot will auto-detect what it can and ask for the rest:

| Variable | Auto-detected? | Description |
|----------|---------------|-------------|
| `TIMEZONE` | ❌ **must ask** | Affects cron scheduling — cannot be guessed reliably |
| `TO` | ❌ **must ask** | Recipient ID — cannot be guessed |
| `CHANNEL` | ✅ default `telegram` | Ask only if user wants a different channel |
| `REMINDERS_FILE` | ✅ default `~/reminders.md` | Ask only if user wants a custom path |

**Bot setup flow:**
1. Ask: *"What is your timezone?"* (e.g. `Europe/Kyiv` — see [tz database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones))
2. Ask: *"What is your recipient ID?"* (e.g. Telegram chat ID — user can get it via @userinfobot)
3. Write answers into `config.env` in the skill directory
4. Scripts source `config.env` automatically on every run

**config.env** (generated during setup):
```bash
TIMEZONE="Europe/Kyiv"
TO="463113011"
CHANNEL="telegram"
REMINDERS_FILE="/home/clawd/reminders.md"
```

## Manual Commands

```bash
# List pending reminders
cron list

# View reminder log
cat ~/reminders.md

# Remove a scheduled reminder
cron rm <job-id>
```

## Agent Implementation

Scripts load `config.env` automatically — no flags needed at runtime.

### One-Time Reminders

When the user says "remind me to X at Y":

```bash
bash "$SKILL_DIR/create-reminder.sh" "X" "Y"
```

### Recurring Reminders

When the user says "remind me every X to Y":

```bash
bash "$SKILL_DIR/create-recurring.sh" "Y" "every X"
```

Both scripts automatically:
1. Source `config.env` from the skill directory
2. Parse the time/schedule (always outputs ISO 8601 timestamp for `--at`)
3. Call `openclaw cron add` with the parsed schedule
4. Log to `$REMINDERS_FILE`
5. Return confirmation with job ID
