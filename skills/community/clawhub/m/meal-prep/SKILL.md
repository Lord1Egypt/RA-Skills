---
name: meal-prep
slug: meal-prep
description: "Weekly meal prep plan from fridge ingredients with nutrition and shopping list."
---

# Meal Prep

Use this skill when the user wants to turn their available ingredients into a structured weekly meal plan with nutrition info, cooking timeline, and a shopping list.

## Good triggers

- "Plan my weekly meals from what's in my fridge."
- "What can I cook with chicken breast, eggs, and broccoli?"
- "Meal prep for weight loss, 1800 kcal/day."
- "Optimize my ingredient usage to minimize waste."
- "Generate a shopping list for a week of healthy meals for 2."

## Workflow

1. **Parse ingredients.** Accept a comma-separated list or natural language description of available ingredients. Normalize names and match against a basic ingredient database (produce, meat, dairy, pantry staples).

2. **Flag perishables.** Identify ingredients that spoil quickly (leafy greens, fresh meat, dairy, herbs) — these must be used first.

3. **Plan weekly menu (5-7 days).**
   - Apply dietary goal: weight-loss (calorie deficit), muscle-gain (high protein), balanced, or none
   - Apply serving count (default 1 person)
   - Vary cuisine across days to avoid boredom (e.g., Mon: Chinese stir-fry, Tue: Western salad, Wed: Italian, Thu: Japanese, Fri: Mexican)
   - Self-consistency: each ingredient appears in at least one meal; leftover ingredients are noted

4. **Label each meal with:**
   - Cooking time (min)
   - Estimated calories (kcal)
   - Macronutrient ratio (protein / carbs / fat %)
   - Dietary labels (high-protein, low-carb, vegetarian, etc.)

5. **Generate shopping list.** Group missing items by supermarket section:
   - Produce → Meats/Fish → Dairy → Dry goods → Spices/Condiments → Frozen
   - Mark items the user already has (from ingredient list)

6. **Optimize ingredient usage order.** Build a day-by-day consumption schedule:
   - Day 1-2: Perishable-first meals
   - Day 3-4: Semi-perishable (root veg, tofu, eggs)
   - Day 5-7: Shelf-stable / frozen ingredients

7. **Build cooking timeline.** Provide a preparation schedule in minutes:
   - **Sunday batch prep** (wash & chop veg, marinate proteins, cook grains)
   - **Daily assembly** (per-day cooking time, usually 10-30 min)
   - Total weekly time estimate

8. **Deliver complete plan.** Structured output:
   - Ingredient inventory (with perishability flags)
   - 7-day meal calendar (table: day, meal, time, kcal, macros)
   - Shopping list (categorized, items user has marked as ✓)
   - Ingredient usage schedule (day-by-day)
   - Batch prep timeline
   - Notes on substitutions and waste-reduction tips

## Sample prompt

```
meal-prep plan --ingredients "鸡胸肉500g,西兰花2颗,鸡蛋12个,番茄4个" --people 2 --goal weight-loss
```
