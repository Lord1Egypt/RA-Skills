# Sleep Branch (Unified)

Use this branch for sleep analysis, recovery interpretation, and Feishu logging.

## Scope
- Analyze sleep screenshots or recovery metrics.
- Extract sleep stages, score, duration, and HRV.
- Upsert results into the Feishu sleep-recovery schema.

## Recognition Rules
- Identify the source app (e.g., Apple Health, AutoSleep, Android).
- Extract duration (min), sleep score, recovery state, and fatigue risk.
- Do not present consumer wearable data as clinical fact.

## Persistence Rules (Feishu)
- Target the **English-only** internal schema fields.
- Ensure date and datetime formatting align with the table field type.
- Resolve any custom field labels via `field_aliases`.

## Standard Upsert Template
```bash
lark-cli base +record-upsert \
  --as user \
  --base-token <base_token> \
  --table-id <sleep_recovery_table_id_or_name> \
  --field 'Date=2026-04-30' \
  --field 'Source App=AutoSleep' \
  --field 'Total Sleep Minutes=430' \
  --field 'Sleep Score=82' \
  --field 'Recovery State=Good' \
  --field 'Fatigue Risk=Low' \
  --field 'One-Line Summary=Sleep duration recovered' \
  --field 'HRV=58'
```

## Boundary
The sleep table is a raw table. Weekly or monthly assessments belong to the reporting branch.
