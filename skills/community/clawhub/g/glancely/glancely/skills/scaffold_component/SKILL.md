---
name: glancely-scaffold
description: >
  Create new personal trackers from natural language. Infer fields, cron,
  and notification text from the user's description. Propose before building.
---

## Flow: Intent → Propose → Confirm → Scaffold

### 1. Analyze the user's goal

When the user says something like "I want to track my workouts" or
"build a reading habit," infer:

- **name**: snake_case, lowercase. E.g. "workout", "reading", "water_intake".
- **fields**: name:type pairs. Common types: text, int, float, bool.
  - "track workouts with type and duration" → type:text, duration_minutes:int
  - "log water in ml" → amount_ml:int
  - "reading habit with book title and pages" → book_title:text, pages_read:int
  - Always add a `note TEXT` field by default for free-form comments.
- **cron**: when should the user be prompted?
  - Morning habit: "0 8 * * *"
  - Evening habit: "0 21 * * *"
  - Multiple times: "0 9,14,21 * * *"
  - Weekly: "0 9 * * 1" (Monday)
- **notification**: what prompt text to send?
  - "Time to log your workout?"
  - "How many pages did you read today?"
  - "Log your water intake"

### 2. Propose a plan

List what will be created. Do NOT run any commands yet. Format:

> "I'll create a tracker called `workout` with fields:
> - type (text)
> - duration_minutes (int)
> - note (text)
>
> Cron: daily at 9pm. Notification: 'Time to log your workout?'
>
> Dashboard will show a Workout panel. Sound good?"

Wait for the user to confirm or revise. If they want changes, revise the plan
and ask again.

### 3. Scaffold

Once confirmed, run for each tracker:

```bash
glancely scaffold \
  --name <name> \
  --title "<Title>" \
  --field <name:type> ... \
  --cron "<expr>" \
  --notify "<text>" \
  --cron-tz "America/Denver"
```

Ask the user for their timezone if not specified (default: America/Denver).

The scaffold command:
- Creates `<name>/` under `~/.glancely/components/`
- Renders component.toml, migrations, log.py, stats.py from templates
- Runs migrations (creates tables in ~/.glancely/data.db)
- Registers cron job in openclaw (if `~/.glancely/openclaw.toml` exists)
- Rebuilds the dashboard

### 4. After scaffold

Tell the user what was created and how to use it:

> "Done! Your workout tracker is ready:
> - Log: `glancely workout log --type run --duration-minutes 30`
> - Dashboard: `glancely dashboard open`
> - You'll get a daily prompt at 9pm."

## Reference examples

Study these examples for patterns:
- `examples/mood/` — simple text+score tracker
- `examples/reminder/` — add/done/list with due dates
- `examples/mit/` — one-entry-per-day pattern
- `examples/diary_logger/` — time-tracking with external API
