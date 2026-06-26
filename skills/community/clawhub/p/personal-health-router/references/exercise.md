# Exercise Branch (Unified)

Use this branch for workout extraction, training summary, and Feishu logging.

## Scope
- Analyze workout screenshots or training summaries.
- Extract metrics (duration, calories, HR, distance, load).
- Upsert results into the Feishu exercise schema.

## Recognition Rules
- Extract only visible metrics.
- Assess training load conservatively (Light, Medium, High).
- Provide same-day or next-day training guidance based on effort.

## Persistence Rules (Feishu)
- Target the **English-only** internal schema fields.
- Map workout types into the configured enum options if possible.
- Use `lark-cli base +record-upsert` for logging.

## Standard Upsert Template
```bash
lark-cli base +record-upsert \
  --as user \
  --base-token <base_token> \
  --table-id <exercise_workout_table_id_or_name> \
  --field 'Logged At=2026-04-30 07:10' \
  --field 'Source App=Garmin' \
  --field 'Workout Type=Run' \
  --field 'Duration Minutes=42' \
  --field 'Calories (kcal)=410' \
  --field 'Load=Medium' \
  --field 'One-Line Summary=Steady aerobic run'
```

## Boundary
Do not trigger full summary rebuilds from a single workout write unless requested.
