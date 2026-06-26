## Who you are
<!-- Agent rewrites this paragraph weekly as it learns more — one synthesized summary -->
{WHO_YOU_ARE}

Example: "You're a 32-year-old training for a half marathon. Protein is your main
focus. You eat out a lot on weekdays and cook on weekends. You have a dairy
intolerance and prefer chicken over red meat. You're on a 14-day streak and
historically struggle with logging on Thursdays."

## Goal narrative
<!-- One sentence written by the user during onboarding or updated anytime -->
{GOAL_NARRATIVE}

Example: "I want to lose 8kg before my sister's wedding in September without feeling
like I'm on a diet."

## Nutrition profile
<!-- nutrition-pro managed section — do not edit manually -->
- Daily calorie target: {KCAL_TARGET} kcal
- Protein goal: {PROTEIN_G}g/day
- Fat limit: {FAT_G}g/day (optional)
- Carb limit: {CARBS_G}g/day (optional)
- Diet type: {DIET}
- Allergies / intolerances: {ALLERGIES}
- Preferred meal times: breakfast {BREAKFAST_TIME}, lunch {LUNCH_TIME}, dinner {DINNER_TIME}
- Timezone: {TIMEZONE}
- Tracking started: {START_DATE}
- Current streak: {STREAK} days
- Longest streak: {LONGEST_STREAK} days

## Trusted meals
<!-- Agent saves meals here after they are logged 3+ times with a confirmed weight.
     Once saved, no portion question is asked — weight is used directly. -->
| Meal name | Grams | Kcal | P | F | C | Times logged |
|---|---|---|---|---|---|---|
{TRUSTED_MEALS}

Example rows:
| Morning oats + milk | 80g oats / 240ml milk | 380 | 12g | 7g | 58g | 23x |
| Post-workout shake | 300ml milk + 1 scoop protein | 310 | 34g | 5g | 28g | 8x |
| Chicken breast + rice (home) | 180g chicken / 200g rice | 520 | 52g | 6g | 62g | 12x |

## Learned food preferences
<!-- Agent appends here when patterns emerge — do not delete -->
{FOOD_PREFERENCES}

## Patterns
<!-- Agent rewrites this section every Sunday based on the past 4 weeks of daily notes.
     Do not append to this section — always rewrite it in full. -->
{PATTERNS}

Example:
- Skips lunch on Thursdays and Fridays (observed 6 of last 8 weeks)
- Weekend calories run ~300 kcal above target on average
- Logs consistently in the morning, rarely logs dinner the same day
- Protein goal hit on training days, misses on rest days
- Tends to undereat when traveling (last 3 work trips: avg 1,400 kcal/day)

## Health context
<!-- Agent writes here when user mentions health goals, conditions, or medications.
     Only write what the user explicitly stated. Never infer diagnoses. -->
{HEALTH_CONTEXT}

## Lifecycle events
<!-- Agent writes here when user mentions upcoming travel, illness, events, or
     any temporary context that should change how data is interpreted. -->
{LIFECYCLE_EVENTS}

Example:
- Traveling: 2026-04-10 to 2026-04-14 (estimate restaurant meals, don't flag as deviation)
- Sick: 2026-03-22 (low intake expected, don't count as streak break)
- Training event: half marathon on 2026-05-18 (increase carb guidance week before)
- Holiday period: 2026-12-24 to 2026-01-02 (social eating expected, relax targets)
