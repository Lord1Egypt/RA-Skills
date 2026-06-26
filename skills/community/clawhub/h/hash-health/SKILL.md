---
name: hash-health
description: Hash Health — personal nutrition tracking, meal logging, medication management, and daily health dashboard. Use when user mentions food, meals, eating, logging, nutrition, calories, macros, medications, or health tracking.
metadata: {"openclaw":{"emoji":"🥗","requires":{"env":["HASH_HEALTH_TOKEN"]},"primaryEnv":"HASH_HEALTH_TOKEN","homepage":"https://hash-claude-mcp.vercel.app"}}
---

You are connected to Hash Health, a personal nutrition and health tracking platform.

> All data is sent to the user's own Hash Health account. No data goes to third parties.

---

## CRITICAL RULES

**Food image received** (user sends a photo):
1. Call `hash_upload_image` immediately with the image — do NOT describe or ask first
2. Call `detectIngredients` with your visual analysis as text parameters
3. Show detected ingredients from the tool result — ask "Confirm to save, or edit?"
4. After user confirms → call `analyze_food` with `image_path` from step 1

**Food text received** ("I ate X", "log X", "save X"):
- Call `hash_analyze_and_log` immediately — no asking first

**Only pause point:** After `detectIngredients` returns, show the list and wait for "yes/save/looks good" before calling `analyze_food`.

**Never:**
- Describe the food or give your own nutrition estimates before calling tools
- Ask "shall I log this?" before calling tools
- Call `analyze_food` before user confirms ingredients
- Save a meal unless user explicitly says save/log/track

---

## Auth check

Before any request call `hash_get_daily_nutrition` with no arguments. If auth error → tell user:
> "Set your `HASH_HEALTH_TOKEN` in OpenClaw settings. Get it from Hash Health app → Settings → Advanced → Generate API Key."

---

## Setup

```
POST https://hash-claude-mcp.vercel.app/api/mcp
Authorization: Bearer $HASH_HEALTH_TOKEN
Content-Type: application/json
Accept: application/json, text/event-stream
```

All calls use JSON-RPC:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": { "name": "<tool_name>", "arguments": { ... } },
  "id": 1
}
```

Result is always in `response.result.content[0].text`

---

## Log a meal — from image

### Step 1 — Upload the image immediately (no text to user first)

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "hash_upload_image",
    "arguments": {
      "image_url": "<attachment URL if available>",
      "image_data_url": "<data:image/jpeg;base64,... if available>",
      "mime_type": "image/jpeg"
    }
  },
  "id": 1
}
```

Provide exactly ONE of: `image_url`, `image_data_url`, or `image_base64`.
Save the `path` from the response — you will pass it to `analyze_food` later.

### Step 2 — Call `detectIngredients` with your visual analysis

Pack everything you see in the image into the parameters. Pass ALL ingredients — if you pass a vague list you get a generic result.

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "detectIngredients",
    "arguments": {
      "food_name": "<dish name you identified>",
      "ingredients_list": [
        "rice ~200g",
        "egg ~50g",
        "onion ~30g",
        "oil ~10g"
      ],
      "portion_size": "<total estimated weight e.g. 290g>",
      "visual_notes": "<brief description e.g. fried rice in a bowl>"
    }
  },
  "id": 2
}
```

### Step 3 — Show result and ask for confirmation

Display the ingredient list from the tool result verbatim, then ask:
> "Detected: Egg Fried Rice
> 1. Rice (~200g)
> 2. Egg (~50g)
> 3. Onion (~30g)
> 4. Oil (~10g)
> ✅ Confirm to save, or tell me what to add/edit/remove?"

### Step 4 — Wait for confirmation, then call `analyze_food`

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "analyze_food",
    "arguments": {
      "food_name": "<dish name>",
      "selected_ingredients": ["rice", "egg", "onion", "oil"],
      "ingredient_sizes_g": {
        "rice": "200g",
        "egg": "50g",
        "onion": "30g",
        "oil": "10g"
      },
      "is_customized_ingredients": true,
      "save_to_history": true,
      "image_path": "<path from hash_upload_image step>"
    }
  },
  "id": 3
}
```

Show: dish name, calories, protein, carbs, fat. Confirm saved ✅

**Important:** `selected_ingredients` is an array of names. `ingredient_sizes_g` is an object mapping name → gram string. Never use `ingredients_list` in `analyze_food`.

---

## Log a meal — from text

**Trigger:** "log X", "I ate X", "save X", "track X" — call immediately, no asking.

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "hash_analyze_and_log",
    "arguments": {
      "food_name": "<dish name and description>",
      "save": true,
      "language": "en"
    }
  },
  "id": 1
}
```

Show: dish name, calories, protein, carbs, fat. Confirm saved.

---

## Check today's nutrition

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "hash_get_daily_nutrition",
    "arguments": { "date": "<YYYY-MM-DD or omit for today>" }
  },
  "id": 1
}
```

Display: calories, protein (g), carbs (g), fat (g), fiber (g), streak.

---

## Daily dashboard

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "hash_daily_dashboard",
    "arguments": { "date": "<YYYY-MM-DD or omit>" }
  },
  "id": 1
}
```

---

## View meal history

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "hash_get_meal_history",
    "arguments": {
      "limit": 10,
      "date": "<YYYY-MM-DD or omit for today>"
    }
  },
  "id": 1
}
```

JSON.parse the `analysis` field — see **Parsing meal analysis data** below.

---

## Delete a meal

Step 1 — get meal ID:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": { "name": "hash_get_meal_history", "arguments": { "limit": 20 } },
  "id": 1
}
```

Step 2 — confirm: "Delete [dish name] logged at [time]?"

Step 3 — delete:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "hash_delete_meal",
    "arguments": { "id": "<UUID>" }
  },
  "id": 2
}
```

---

## Weekly report

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": { "name": "hash_weekly_report", "arguments": {} },
  "id": 1
}
```

---

## List medications

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": { "name": "hash_get_medications", "arguments": {} },
  "id": 1
}
```

---

## Add a medication

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "hash_add_medication",
    "arguments": {
      "name": "<medication name>",
      "dosage": "<e.g. 500mg>",
      "frequency": "<e.g. twice daily>",
      "time_of_day": ["morning", "evening"],
      "notes": ""
    }
  },
  "id": 1
}
```

---

## Delete a medication

Step 1 — get ID: `hash_get_medications`
Step 2 — confirm with user
Step 3:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "hash_delete_medication",
    "arguments": { "id": <numeric id> }
  },
  "id": 2
}
```

Note: medication `id` is a **number**, not a string.

---

## Bedtime summary

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": { "name": "hash_get_bedtime_summary", "arguments": {} },
  "id": 1
}
```

---

## Nutrition chat

**When:** User asks a health/nutrition question.

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "nutrition_chat",
    "arguments": {
      "messages": [
        { "role": "user", "content": "<user's question>" }
      ]
    }
  },
  "id": 1
}
```

---

## Parsing meal analysis data

The `analysis` field in meal history is always a **JSON string** — always `JSON.parse()` it first.

Two possible formats:

| Value | Format A (current) | Format B (legacy) |
|-------|-------------------|-------------------|
| Dish name | `dishName` | `dish` |
| Calories | `nutritionalInfo.calories_kcal` | `nutrition.calories` |
| Protein | `nutritionalInfo.proteins_g` | `nutrition.protein` |
| Carbs | `nutritionalInfo.carbohydrates_g` | `nutrition.carbs` |
| Fat | `nutritionalInfo.fats_g` | `nutrition.fat` |
| Fiber | `nutritionalInfo.fiber_g` | `nutrition.fiber` |
| Sugar | `nutritionalInfo.sugar_g` | `nutrition.sugar` |
| Serving size | `estimatedServingSize_g` | `estimated_serving_size_g` |
| Category | `category` | `category` |
| Summary | `analysis` | `summary` |

Detect format: `dishName` present → Format A. `dish` present → Format B.

Always display:
```
🍽 <dish name>
Calories: X kcal | Protein: Xg | Carbs: Xg | Fat: Xg | Fiber: Xg
```

---

## Rules

- Always use today's date (YYYY-MM-DD) when no date is specified.
- Never guess a meal UUID or medication ID — look it up first.
- Always confirm before deleting.
- Medication `id` is a number — not a string.
- Never ask the user to paste their token in chat — always use OpenClaw environment settings.
- If token is missing/invalid: "Set your `HASH_HEALTH_TOKEN` in OpenClaw settings. Hash Health app → Settings → Advanced → Generate API Key."
