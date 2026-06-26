---
name: image-calorie-tracker
description: >
  Photo Calorie Tracker - Recognizes food photos, logs daily calorie intake, and analyzes any date range.
  Use when: the user sends food images or asks about calories over the past X days.
  NOT for: weight change analysis, detailed nutrition breakdowns, or workout plan design.
---

# 🔥 Photo Calorie Tracker (image-calorie-tracker)

Recognizes food photos, logs daily calorie intake, and generates reports.

## When to Run

- The user sends food images
- The user asks about calories over the past X days (X is any number)

## Workflow

### Log Meals
1. Copy images to `/root/.openclaw/workspace/temp_qqdata/YYYY-MM-DD-meal.jpg`
2. Use the `image` tool to recognize food
3. Estimate calories for each food item
4. Update `/root/.openclaw/workspace/memory/YYYY-MM-DD.md`

### Generate Report
1. Read records for the target dates from `/root/.openclaw/workspace/memory/`
2. Read the target calories from `/root/.openclaw/workspace/skills/image-calorie-tracker/config/target_calorie.txt`
3. Output the report in the required format

## Output Format

```
📊 Calorie Tracking | Target:{target}

【MM-DD】{status}
  {Breakfast if any}: {calories}
  {Lunch if any}: {calories}
  {Dinner if any}: {calories}
  {Snack if any}: {calories}
```

### Status Rules
- **Incomplete**: lunch or dinner is missing (breakfast does not count)
- **{percent}%**: difference between total calories and target; positive means over, negative means under

### Meal Display Rules
- Show only lunch, dinner, and snack (breakfast not counted)
- Omit meals that are not recorded
- Calorie unit: kcal

## Meal Definitions

- **Lunch**: around 12:00, about 300-800 kcal
- **Dinner**: around 18:00, about 400-1000 kcal
- **Snack**: snacks/desserts between lunch and dinner

## Food Calorie Reference

| Category | Food | Calories (per 100g) |
|------|------|--------------|
| Staples | Rice | 130 kcal |
| Staples | Mixed grain rice | 120 kcal |
| Meat | Fried chicken cutlet | 280 kcal |
| Meat | Stir-fried pork slices | 180 kcal |
| Vegetables | Green pepper with pork | 150 kcal |
| Vegetables | Shredded potatoes | 120 kcal |
| Bakery | Bread/Cake | 250-350 kcal |

## File Paths

- Temp images: `/root/.openclaw/workspace/temp_qqdata/`
- Daily records: `/root/.openclaw/workspace/memory/YYYY-MM-DD.md`
- Target calories: `/root/.openclaw/workspace/skills/image-calorie-tracker/config/target_calorie.txt`

## Example Output

```
📊 Calorie Tracking | Target:2100

【03-16】+7%
  Lunch: 1115

【03-17】Incomplete
  Lunch: 820
  Snack: 280
```
