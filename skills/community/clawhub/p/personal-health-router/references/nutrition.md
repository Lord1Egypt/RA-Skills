# Nutrition Branch (Unified)

Use this branch for meal recognition, calorie estimation, and Feishu logging.

## Scope
- Analyze meal photos or food descriptions.
- Map a structured meal result into a Feishu nutrition-meal schema.
- Rebuild nutrition daily history when required.

## Recognition Rules
- Extract only visible food items.
- Estimate calories, protein, sodium, carbs, fat, and fiber conservatively.
- State uncertainty when portions or hidden ingredients (e.g., oil, salt) are unclear.

## Persistence Rules (Feishu)
- Target the **English-only** internal schema fields.
- Use `lark-cli base +record-upsert` for raw-write.
- If the user uses custom field labels, resolve them via `field_aliases` in config.

## Standard Upsert Template
```bash
lark-cli base +record-upsert \
  --as user \
  --base-token <base_token> \
  --table-id <nutrition_meal_table_id_or_name> \
  --field 'Logged At=2026-04-30 19:15' \
  --field 'Food Description=Chicken rice + vegetables' \
  --field 'Calories (kcal)=650' \
  --field 'Protein (g)=38' \
  --field 'Sodium (mg)=920' \
  --field 'Fiber (g)=9'
```

## Boundary
Do not mix first-pass recognition with full monthly/weekly rebuilds unless explicitly requested.
