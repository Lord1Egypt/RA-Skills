---
name: habit-tracker
description: "Track daily habits, streaks, and completions locally. Triggers on: habit, streak, track habit, log exercise, log habit, weekly review, habit status, did I exercise today, habit check, morning routine."
---

# Habit Tracker Skill

Local habit tracking via JSON files. No external services or API keys.
Data lives in `~/.openclaw/workspace/habits/` (override with `HABIT_DATA_DIR` env var).

Scripts live in `scripts/` relative to this file.
Resolve all script paths relative to this skill's `scripts/` directory.

---

## Commands

### List habits
```
python scripts/setup_habits.py --list
```

### Add a habit
```
python scripts/setup_habits.py --add "Habit Name" --frequency daily|weekday|weekly --emoji 🏋️
```
- `--frequency` defaults to `daily` if omitted
- `--emoji` is optional

### Remove (archive) a habit
```
python scripts/setup_habits.py --remove "Habit Name"
```
History is preserved. Habit is soft-deleted.

### Log a habit completion
```
python scripts/log_habit.py "Habit Name"
python scripts/log_habit.py "Habit Name" --date 2024-01-15
python scripts/log_habit.py "Habit Name" --undo
```
- Accepts exact name, partial name, or ID
- Prevents duplicate logging (safe to re-run)
- `--undo` removes today's log entry

### Check status
```
python scripts/status.py
python scripts/status.py --json
python scripts/status.py --date 2024-01-15
```
Outputs current streak, longest streak, today's completion, and 7/30-day rates.

### Weekly review
```
python scripts/weekly_review.py
python scripts/weekly_review.py --week 2024-01-15
python scripts/weekly_review.py --output ~/Desktop/review.md
python scripts/weekly_review.py --obsidian
```
Generates a formatted markdown report. `--obsidian` saves to `vault/habits/weekly-reviews/YYYY-MM-DD.md`.

---

## Interpreting User Requests

| User says | Action |
|-----------|--------|
| "Did I exercise today?" | `status.py --json` → find habit by name |
| "Log my run / I exercised" | `log_habit.py "Exercise"` |
| "What's my reading streak?" | `status.py --json` → extract streak for reading |
| "Log yesterday's meditation" | `log_habit.py "Meditation" --date YYYY-MM-DD` |
| "Weekly review" | `weekly_review.py` |
| "Add habit: cold shower" | `setup_habits.py --add "Cold Shower"` |
| "Show all habits" | `setup_habits.py --list` |
| "Remove journaling" | `setup_habits.py --remove "Journaling"` |

---

## Frequency Semantics

- `daily` — expected every calendar day
- `weekday` — Mon–Fri only; weekend skips don't break streaks
- `weekly` — once per 7-day window; streak = consecutive weeks with ≥1 completion

---

## Output Handling

- `status.py` (no `--json`): print directly to user
- `status.py --json`: parse and reformat as a clean bullet list for Discord
- `weekly_review.py`: offer to save to Obsidian (`--obsidian`) or print inline
- Always confirm after `log_habit.py` with what was logged and current streak

---

## Data Location

```
~/.openclaw/workspace/habits/
├── habits.json   # habit definitions
└── log.json      # daily completion records
```

Both files are auto-created. See `references/data-format.md` for schema details.
