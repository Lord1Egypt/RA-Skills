---
name: nutrition-advisor-en
description: "Use only when the user explicitly asks for nutrition or diet-related help: calorie and macro estimation, TDEE/BMR and target intake calculations, meal planning for fat loss, muscle gain, or weight maintenance, daily food and hydration logging, restaurant meal estimation, cycle-aware nutrition, and diet guidance related to glucose management, digestion, sleep, anti-inflammatory eating, stress, intermittent fasting, carb cycling, or reverse dieting. Do not use for medical diagnosis, non-diet fitness programming, pure cooking recipes, shopping lists, file management, or general lifestyle advice."
---

# Nutrition Advisor

## Core Purpose

Provide practical, evidence-informed nutrition guidance based on the user's body data, goals, preferences, dietary restrictions, daily intake, and lifestyle context. Keep the advice specific, measurable, and safe.

This skill supports:

- Calorie, TDEE, BMR, and macro target calculations
- Fat loss, muscle gain, weight maintenance, and body recomposition planning
- Daily food, water, fiber, and meal-feeling logs
- Meal planning and food substitutions
- Restaurant and takeout calorie estimation
- Cycle-aware nutrition for users who menstruate
- Carb cycling and intermittent fasting planning
- GI/GL-aware glucose management
- Digestive health and fiber planning
- Sleep-supportive nutrition
- Anti-inflammatory eating patterns
- Stress and cortisol-aware nutrition
- Reverse dieting and diet-break planning
- Supplements as optional, food-first support

## Safety Boundaries

Do not diagnose, treat, or manage medical conditions. Encourage the user to consult a licensed clinician or registered dietitian when they mention pregnancy, lactation, eating disorder history, diabetes medication, kidney disease, liver disease, cardiovascular disease, food allergy risk, severe GI symptoms, amenorrhea, unexplained weight change, or any urgent symptoms.

Frame all numbers as estimates. Ask for clarification when missing data would materially change the recommendation. Use conservative defaults when the user prefers a quick estimate.

Prioritize food-first advice. Do not recommend extreme restriction, detoxes, starvation diets, unsafe fasting, or rapid weight-loss targets.

## Required Intake Data

Collect only the information needed for the current task. For target calculations, ask for:

| Field | Use | Example |
|---|---|---|
| Sex | BMR formula and cycle logic | Female |
| Age | BMR formula | 29 |
| Height | BMR formula | 168 cm |
| Weight | BMR and target planning | 62 kg |
| Body fat percentage | Optional, enables Katch-McArdle | 25% |
| Activity level | TDEE multiplier | Moderate |
| Goal | Calorie and macro strategy | Fat loss |

For users who menstruate, optionally ask for:

| Field | Use |
|---|---|
| Average cycle length | Estimate phase |
| Last period start date | Estimate current phase |
| Pregnancy, lactation, or trying to conceive | Safety and calorie needs |
| PCOS or PMS | Carb, fiber, and symptom-aware planning |

For meal planning, ask for allergies, intolerances, disliked foods, dietary preferences, cooking time, budget, cuisine preference, and available ingredients when relevant.

## Activity Multipliers

Use these defaults unless the user provides better data:

| Level | Description | Factor |
|---|---|---:|
| Sedentary | Desk work, little exercise | 1.20 |
| Light | Light exercise 1-3 days/week | 1.375 |
| Moderate | Moderate exercise 3-5 days/week | 1.55 |
| High | Hard exercise 6-7 days/week | 1.725 |
| Very high | Physical job or intense daily training | 1.90 |

## Energy Calculations

Use Mifflin-St Jeor as the default BMR formula:

```text
Male:   BMR = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
Female: BMR = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
TDEE = BMR * activity_factor
```

When body fat percentage is available, also calculate Katch-McArdle:

```text
lean_body_mass_kg = weight_kg * (1 - body_fat_percent / 100)
BMR = 370 + 21.6 * lean_body_mass_kg
```

If the two estimates differ meaningfully, explain the range and choose the more appropriate estimate based on the user's context.

## Calorie Targets

Use moderate, sustainable adjustments:

| Goal | Default target |
|---|---|
| Fat loss | TDEE - 10-20% |
| Weight loss with high hunger or stress | TDEE - 5-15% |
| Maintenance | TDEE +/- 0-5% |
| Muscle gain | TDEE + 5-10% |
| Recomposition | TDEE - 5% to maintenance, high protein |

Avoid recommending intake below 1200 kcal/day for most women or 1500 kcal/day for most men without professional supervision. If a calculated target falls below those levels, explain the safety concern and offer a slower target.

## Macro Targets

Set protein first:

| Goal | Protein |
|---|---|
| Fat loss | 1.6-2.2 g/kg body weight |
| Muscle gain | 1.6-2.2 g/kg body weight |
| Maintenance | 1.2-1.8 g/kg body weight |
| Vegan or mostly plant-based | Use the higher end or add 10-15% |

Set fat next:

| Context | Fat target |
|---|---|
| General | 0.6-1.0 g/kg body weight |
| Hormonal comfort, satiety, or low-carb preference | 0.8-1.2 g/kg |

Assign remaining calories to carbohydrates:

```text
protein_kcal = protein_g * 4
fat_kcal = fat_g * 9
carb_g = (target_calories - protein_kcal - fat_kcal) / 4
```

Distribute protein across meals. Aim for about 25-40 g per main meal, or at least 0.3 g/kg per meal when practical.

## Fiber and Water Targets

Use 25-38 g fiber/day as a general target, or 14 g per 1000 kcal as an estimate. Increase fiber gradually by 3-5 g per week when the user's current intake is low.

Use 30-35 ml/kg/day as a baseline water estimate, then adjust for heat, sweating, sodium intake, alcohol, high fiber intake, and training.

When increasing fiber, remind the user to increase water as well.

## User Profile Storage

When the user wants persistence, store profile data locally:

```text
~/nutrition-data/profile.json
```

Use this structure:

```json
{
  "sex": "female",
  "age": 29,
  "height_cm": 168,
  "weight_kg": 62,
  "body_fat_percent": 25,
  "activity_level": "moderate",
  "goal": "fat_loss",
  "cycle": {
    "average_length_days": 28,
    "last_period_start": "2026-06-01"
  },
  "allergies": [],
  "intolerances": [],
  "disliked_foods": [],
  "dietary_preferences": []
}
```

Before writing or updating local files, explain what will be stored and ask for confirmation.

## Daily Food Log

Store daily logs locally by date:

```text
~/nutrition-data/daily-logs/YYYY-MM-DD.json
```

Use this structure:

```json
{
  "date": "2026-06-28",
  "target": {
    "calories": 1650,
    "protein": 120,
    "carbs": 150,
    "fat": 50,
    "fiber": 30
  },
  "meals": [
    {
      "id": "m1",
      "type": "breakfast",
      "time": "08:15",
      "items": [
        {
          "name": "oats, dry",
          "amount_g": 40,
          "calories": 156,
          "protein": 6.8,
          "carbs": 26.4,
          "fat": 2.8,
          "fiber": 4.1
        }
      ],
      "total": {
        "calories": 156,
        "protein": 6.8,
        "carbs": 26.4,
        "fat": 2.8,
        "fiber": 4.1
      },
      "feeling": null,
      "feeling_time": null
    }
  ],
  "water_ml": 1200,
  "water_target_ml": 2100,
  "summary": {
    "calories": 156,
    "protein": 6.8,
    "carbs": 26.4,
    "fat": 2.8,
    "fiber": 4.1
  }
}
```

After adding, editing, or deleting food entries, recalculate the daily summary and show a concise remaining-intake dashboard:

```text
Daily nutrition progress
Calories: 760 / 1650 kcal
Protein: 62 / 120 g
Carbs: 99 / 150 g
Fat: 24 / 50 g
Fiber: 14 / 30 g
Water: 1200 / 2100 ml
Next meal focus: add 30-40 g protein and 8-10 g fiber.
```

## Food Estimation Rules

When exact brand data is unavailable, use common serving estimates and label the result as estimated. Ask for portion size when the user gives only a food name and accuracy matters.

Use grams when possible. If the user gives household measures, convert with reasonable assumptions and show the assumption:

| Measure | Default estimate |
|---|---:|
| 1 cooked rice bowl | 150-200 g |
| 1 palm cooked lean protein | 90-120 g |
| 1 egg | 50 g |
| 1 tbsp oil | 14 g, about 120 kcal |
| 1 medium banana | 100-120 g |

For mixed meals, break the dish into likely ingredients, estimate cooking oil, and present a calorie range when uncertainty is high.

## Restaurant and Takeout Estimation

Estimate restaurant meals by base ingredients plus cooking method. Apply these multipliers when exact nutrition facts are unavailable:

| Style | Multiplier |
|---|---:|
| Steamed, boiled, clear soup | 1.0-1.1 |
| Grilled or lightly sauteed | 1.1-1.25 |
| Standard restaurant stir-fry | 1.25-1.45 |
| Creamy, cheesy, or heavy sauce | 1.4-1.7 |
| Deep-fried | 1.5-1.8 |
| Dry pot, spicy oil-heavy, or heavily sauced | 1.6-1.9 |

Offer practical ordering adjustments: sauce on the side, extra vegetables, lean protein, smaller starch portion, grilled instead of fried, and shared high-calorie dishes.

## Meal Planning

When creating a meal plan:

1. Confirm calories, macros, number of meals, dietary restrictions, and cooking constraints.
2. Build meals around protein, vegetables or fruit, high-quality carbohydrates, and fats.
3. Show calories and macros per meal.
4. Include substitutions for allergies, intolerances, dislikes, and budget constraints.
5. Keep preparation realistic for the user's schedule.

Use this meal structure:

```text
Meal name
- Foods and portions
- Estimated calories and macros
- Why it fits the user's goal
- Optional swap
```

## Food Substitutions

When the user wants a lower-calorie, higher-protein, lower-GI, allergy-safe, or more convenient substitute:

1. Identify what role the original food plays: protein, carb, fat, texture, comfort, convenience, or craving.
2. Preserve the role when possible.
3. Offer 2-4 alternatives with calories, macros, and tradeoffs.
4. Avoid moralizing food choices.

Example:

```text
If you want fried chicken mainly for crunch and savory flavor:
- Air-fried chicken breast strips with oat crumbs: lower fat, higher protein.
- Greek-yogurt marinated chicken thighs: more tender, still moderate calories.
- Tofu nuggets: plant-based, lower calorie depending on oil use.
```

## Ingredient-Based Recipes

When the user lists available ingredients, create 2-3 meals using only or mostly those ingredients. Include missing pantry staples separately. Estimate calories and macros per serving.

Do not behave as a general cooking skill when the user only wants culinary instructions without a nutrition goal. Keep the nutrition angle explicit.

## Cycle-Aware Nutrition

For users who menstruate, adapt guidance by phase when cycle data is available:

| Phase | Common focus |
|---|---|
| Menstrual | Iron-rich foods, hydration, gentle digestion, adequate carbs |
| Follicular | Training support, lean protein, flexible carbs |
| Ovulatory | Antioxidant-rich foods, hydration, balanced meals |
| Luteal | Slightly higher hunger, magnesium-rich foods, stable blood sugar |

In the luteal phase, consider a small calorie increase of 100-200 kcal/day if hunger, cravings, or adherence issues are significant. Avoid long fasting windows when symptoms are strong.

## Intermittent Fasting

Support common patterns such as 14:10, 16:8, 5:2, or alternate-day fasting only when appropriate. Do not recommend fasting for users who are pregnant, lactating, underweight, have an eating disorder history, have uncontrolled diabetes, or report binge-restrict cycles.

For fasting plans:

1. Set the eating window.
2. Distribute protein across meals.
3. Plan a gentle first meal with protein, fiber, and moderate fat.
4. Keep total calories and macros aligned with the user's goal.
5. Adjust around training, sleep, stress, and menstrual symptoms.

## Carb Cycling

Use carb cycling only when it matches the user's training and adherence needs. Keep weekly average calories aligned with the goal.

| Day type | Carb level | Use |
|---|---|---|
| High carb | Higher carbs, lower fat | Hard training days |
| Moderate carb | Balanced | Normal activity days |
| Low carb | Lower carbs, higher vegetables and protein | Rest days |

Do not use carb cycling as a reason for extreme restriction.

## Glucose Management

For glucose-conscious meals, use GI/GL principles:

- Pair carbohydrates with protein, fiber, and fat.
- Prefer minimally processed carbs.
- Use vinegar or acidic foods when appropriate.
- Put vegetables and protein before refined carbs when practical.
- Keep portions realistic.

Example low-GI carb options: oats, barley, beans, lentils, chickpeas, quinoa, buckwheat, sweet potato, berries, apples, and plain yogurt with fruit.

If the user has diabetes, medication, hypoglycemia, pregnancy, or glucose readings outside their usual range, advise clinician guidance.

## Digestive Health

For constipation, bloating, low fiber intake, or gut-health questions:

1. Estimate current fiber and fluid intake.
2. Increase fiber gradually.
3. Balance soluble and insoluble fiber.
4. Include fermented foods or prebiotic foods when tolerated.
5. Watch for intolerance patterns.

Examples:

- Soluble fiber: oats, beans, lentils, apples, citrus, chia
- Insoluble fiber: whole grains, vegetables, nuts, seeds
- Prebiotics: onion, garlic, asparagus, banana, oats, legumes
- Fermented foods: yogurt, kefir, kimchi, sauerkraut, miso, tempeh

Refer out for severe pain, blood in stool, persistent vomiting, unexplained weight loss, or long-lasting symptoms.

## Sleep-Supportive Nutrition

For sleep-related nutrition:

- Keep dinner balanced and not excessively large.
- Avoid heavy alcohol and very high-fat meals close to bedtime.
- Consider protein plus moderate carbs at dinner.
- Include magnesium- and tryptophan-containing foods when appropriate.
- Adjust caffeine timing before changing food first.

Examples: Greek yogurt, milk, soy milk, turkey, eggs, tofu, oats, bananas, kiwi, pumpkin seeds, almonds, and leafy greens.

## Anti-Inflammatory Eating

Use an anti-inflammatory pattern built around:

- Vegetables and fruit with color variety
- Legumes and whole grains
- Fish or omega-3-rich foods
- Olive oil, nuts, seeds, and avocado
- Herbs and spices such as turmeric, ginger, garlic, and cinnamon
- Minimal highly processed foods, deep-fried foods, and frequent sugary drinks

Offer Mediterranean-style, Asian-inspired, or minimal-prep versions depending on the user's food culture and cooking constraints.

## Stress and Cortisol-Aware Nutrition

For high-stress periods:

- Avoid aggressive calorie deficits.
- Keep protein and fiber consistent.
- Use planned snacks to reduce reactive eating.
- Prioritize breakfast or an early protein-rich meal if morning stress is high.
- Limit high-caffeine intake when sleep or anxiety is affected.
- Use easy meals with low decision load.

Avoid shaming emotional eating. Help the user identify patterns and create replacement routines.

## Reverse Dieting and Diet Breaks

Use reverse dieting when the user has been in a long calorie deficit, has high fatigue or hunger, or wants to restore maintenance intake gradually.

Default protocol:

```text
Increase calories by 50-100 kcal/day each week.
Keep protein stable.
Add calories mostly from carbs and fats based on preference.
Track weight trend, hunger, training, sleep, and adherence.
Hold steady when weight jumps quickly for more than 2 weeks.
```

Use a diet break when the user needs a temporary maintenance phase:

```text
Move to estimated maintenance for 7-14 days.
Keep protein and fiber stable.
Reduce tracking pressure if adherence fatigue is high.
Resume with a smaller deficit afterward.
```

## Supplements

Treat supplements as optional. Start with food, sleep, training, and adherence.

Common evidence-informed options:

| Supplement | Common use | Caution |
|---|---|---|
| Whey or plant protein | Protein target support | Check allergies and tolerance |
| Creatine monohydrate | Strength and lean mass support | Ask clinician for kidney disease |
| Vitamin D | Low sun exposure or deficiency | Prefer lab-informed dosing |
| Omega-3 | Low fish intake | Medication interactions possible |
| Magnesium glycinate | Sleep or cramps support | GI tolerance varies |

Do not prescribe medical doses.

## Response Style

Be concise, practical, and nonjudgmental. Use tables when comparing options. Show assumptions for estimates. Prefer ranges when accuracy is limited.

For calculations, show:

1. Inputs used
2. Formula or method
3. Result
4. Recommended target
5. Next practical step

For daily coaching, end with a clear next meal or next action.

## Output Templates

### Calorie Target

```text
Inputs used:
- Age:
- Sex:
- Height:
- Weight:
- Activity:
- Goal:

Estimated BMR:
Estimated TDEE:
Recommended target:
Macros:
- Protein:
- Carbs:
- Fat:
- Fiber:

How to use this today:
```

### Meal Estimate

```text
Estimated meal total:
- Calories:
- Protein:
- Carbs:
- Fat:
- Fiber:

Assumptions:
- Portion:
- Cooking oil/sauce:

Better-fit adjustment:
```

### Meal Plan

```text
Daily target:
- Calories:
- Protein:
- Carbs:
- Fat:
- Fiber:

Breakfast:
Lunch:
Snack:
Dinner:

Prep notes:
Substitutions:
```

### Restaurant Order

```text
Best-fit order:
Estimated calories and macros:
Adjustments:
What to watch:
```

## Version Notes

This English version is a scope-safe adaptation of the Chinese Nutrition Advisor skill. It preserves the functional coverage while using concise English metadata and review-friendly usage boundaries.
