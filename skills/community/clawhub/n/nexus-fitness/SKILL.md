# Nexus — Workout & Nutrition Tracker

Track workouts, meals, and weight from your terminal. Nexus is a CLI tool that stores fitness data in the cloud so you can log, query, and update your training and nutrition history.

## Installation

```bash
uv tool install nexus-fitness
```

## When to use this skill

Use Nexus when the user wants to:

- Log a workout (strength training, cardio, or any exercise)
- Log a meal or snack with nutrition info
- Log their body weight
- Check workout or meal history for a date or date range
- Update or correct a previous entry
- Manage fitness friends (add, accept, view friend data)

## Authentication

Before using Nexus, sign in with Google:

```bash
nexus auth login
```

Check auth status or sign out:

```bash
nexus auth status
nexus auth logout
```

## Commands

### `nexus log`

Log workouts, meals, or weight. Provide entries as JSON via file, inline, or stdin.

```bash
nexus log --file entries.json
nexus log --entries '[{"type":"workout","exercise":"bench_press","sets":[{"weight_kg":80,"reps":8}]}]'
cat entries.json | nexus log --stdin
nexus log --file workouts.json --date 2026-04-09
```

Entry types:
- **Strength workouts**: exercise name, exercise_key, sets (weight_kg, reps), notes
- **Cardio workouts**: exercise name, exercise_key, duration_min, distance_km, notes
- **Meals**: items with name, quantity, calories, protein_g, carbs_g, fat_g, meal_type
- **Weight**: weight_kg, notes

### `nexus history`

Fetch past entries with optional filtering by date, type, or friend.

```bash
nexus history
nexus history --date 2026-04-09
nexus history --type workout
nexus history --from-date 2026-04-01 --to-date 2026-04-09 --type meal
nexus history --friend-id abc123 --type weight
```

Options:
- `--date`: entries for a specific date
- `--from-date` / `--to-date`: date range query
- `--type`: filter by `workout`, `meal`, or `weight`
- `--friend-id`: view a friend's history

### `nexus update`

Modify an existing entry by its ID (get IDs from `nexus history`).

```bash
nexus update --entry-id 123 --file updated-entry.json
nexus update --entry-id 456 --data '{"exercise":"cycling","duration_min":45}'
```

### `nexus friends`

Manage social fitness connections.

```bash
nexus friends list
nexus friends add --code NEXUS-A1B2
nexus friends accept --display-name "John Doe"
nexus friends reject --display-name "Jane Smith"
nexus friends remove --display-name "Old Friend"
```

## Guidelines

- Nexus only handles exercise and nutrition data — don't try to use it for sleep, mood, or other tracking
- All logging is explicit — Nexus does not passively capture data
- When logging meals, provide calorie and macro estimates even if approximate
- Use exercise_key in lowercase_snake_case for consistency (e.g., `bench_press`, `pull_ups`)
- When the user says something vague like "I did chest today", ask for specifics (exercises, sets, reps, weight)

## Links

- Website: https://kushalsm.com/nexus
- GitHub: https://github.com/kiluazen/nexus
- Privacy Policy: https://kushalsm.com/nexus/privacy-policy
- Terms of Service: https://kushalsm.com/nexus/terms-of-service
