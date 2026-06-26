# Nutrition-pro onboarding script

Follow these steps exactly. Do not skip any. Do not ask all questions at once.

## Step 1 — Check if already set up

Run: `memory_get MEMORY.md`

If MEMORY.md contains a filled `## Nutrition profile` section:
  Say: "You're already set up! Here's your current profile:"
  Read and display the `## Who you are`, `## Goal narrative`, and `## Nutrition profile` sections.
  Ask if they want to update anything. Stop here.

## Step 2 — Explain what we're setting up (one sentence)

Say: "I'll set up daily nutrition tracking. I need 5 quick things from you."

## Step 3 — Ask one question at a time, wait for answer before next

Question 1: "What's the one thing you're trying to achieve with food right now?
(e.g. 'lose weight before summer', 'build muscle', 'eat more protein', 'just be
more aware of what I eat') — in your own words."
  - Write their exact answer (not a paraphrase) to `## Goal narrative` in MEMORY.md
  - This is the most important question — it shapes every summary and suggestion

Question 2: "What's your daily calorie goal? (If unsure, I can estimate it — just tell me
your weight, height, age, and activity level.)"
  - If they give a number: use it directly
  - If they ask for an estimate: use the Harris-Benedict TDEE formula from SKILL.md.
    Show the result and confirm before using.

Question 3: "Daily protein goal in grams? (Common targets: 0.8g × body weight in kg for
maintenance, 1.6–2.2g × kg for muscle building)"

Question 4: "Any dietary restrictions or food allergies I should know about?
(e.g. gluten-free, dairy-free, nut allergy, vegan)"

Question 5: "What time do you usually have breakfast, lunch, and dinner?
(e.g. 8am, 1pm, 8pm)"

## Step 4 — Write to MEMORY.md

Take the answers and write the full profile to MEMORY.md.
Read the template from `nutrition-pro/MEMORY_TEMPLATE.md`, fill in all known values, then
append the filled template as a new section. Do NOT overwrite existing content.

For `## Who you are`: write a first-pass paragraph using what you know so far.
It will be rewritten after the first week of real data. Example first-pass:
"You're just getting started with nutrition tracking. Your goal: {GOAL_NARRATIVE}.
Calorie target is {KCAL} kcal/day with {PROTEIN}g protein. {DIET_NOTE}"

Leave `## Trusted meals` and `## Patterns` empty — they fill in over time.

## Step 5 — Set up heartbeat integration

Read `nutrition-pro/HEARTBEAT_SNIPPET.md`.
Run: `memory_get HEARTBEAT.md` to check current contents.
If "nutrition-pro" is not already present: append the snippet to HEARTBEAT.md.

## Step 6 — Offer cron jobs

Say: "Do you want proactive reminders? I can check in with you once, twice, or three times a day.
Here's what's available:

  • Morning summary — shows yesterday's totals and starts your day
  • Evening check-in — asks what you ate, logs it, shows today's summary
  • Weekly report — every Monday, a full week breakdown
  • Sunday synthesis — runs quietly every Sunday night and rewrites your profile
    and pattern summary so I know you better over time (recommended)

You can pick any combination. Which ones do you want? (e.g. 'just the evening one',
'morning and evening', 'all three + synthesis', or 'none')"

Collect their choices, then for each chosen reminder ask what time they want it.
Ask times one at a time, only for the reminders they selected:
  - If morning chosen: "What time do you want your morning summary? (e.g. 7am, 8:30am)"
  - If evening chosen: "What time do you want your evening check-in? (e.g. 7pm, 9pm)"
  - If weekly chosen: "What time on Monday? (e.g. 9am)" — day is always Monday

Parse each time into 24h hour and minute for the cron expression (e.g. "8:30am" → hour=8, min=30).

Then follow the "Setting up proactive reminders" section in SKILL.md, running only the
cron commands for the reminders the user selected, substituting their chosen times.
If the user selected Sunday synthesis, run that cron command too.

If none: say "No problem. You can always ask me to set them up later by saying
'set up nutrition reminders'."

## Step 7 — Confirm and offer first log

Say: "You're all set! Your {KCAL_TARGET} kcal target is saved.
Want to log your first meal now?"

If yes: follow the meal-logging flow from the main SKILL.md.
