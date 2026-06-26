---
name: nutrition-cli
description: >
  Use this skill for anything related to food, nutrition, calories, macros,
  protein, fat, carbohydrates, fiber, vitamins, meal tracking, diet goals,
  weight management, or healthy eating. Triggers on: food names, meal logging
  ("I just had X", "log my lunch"), nutrition questions ("how many calories in
  X", "macros for Y"), diet setup ("track my calories", "set up nutrition
  tracking", "help me eat better"), barcode scans (8-13 digit numbers), and
  weekly/daily summaries. Also triggers when the user casually mentions food
  in passing — always offer to log it.
metadata:
  clawdbot:
    emoji: "🥗"
    requires:
      bins: ["nutrition"]
    install:
      - id: pip
        kind: pip
        package: nutrition-cli
        bins: ["nutrition"]
        label: "Install nutrition-cli (pip)"
---

# nutrition-cli

Look up nutrition data for any food, log meals, track daily intake against your goals, compare foods, estimate calorie burn, and view trends — all from the command line.

---

## First run

On the very first message that triggers this skill, check if nutrition tracking is configured:

Run: `nutrition config status`

If output is "Not configured":
  Read and follow `skill/ONBOARDING.md` exactly.

If output is "Configured":
  Continue normally. Do not re-run onboarding.

---

## Logging meals

**Triggers:** "I had X", "I ate X", "just had X", "log X", "add X to my food log",
any food mentioned in passing.

Steps:
1. Extract food name and optional grams from the message.
   Examples: "200g chicken" → food="chicken breast", grams=200
             "a big mac"    → food="big mac", grams=null (use default 100g)
             "2 eggs"       → food="eggs", grams=null (use default)

2. Run: `nutrition search "{FOOD}" --grams {GRAMS} --format json`
   Show the result summary (name, kcal, protein, fat, carbs).
   Ask: "Should I log this?" — wait for confirmation before writing.

3. On confirmation: Run: `nutrition log "{FOOD}" --grams {GRAMS}`

4. After logging, append one line to today's daily memory note (memory/YYYY-MM-DD.md):
   Format: `- {TIME} · {FOOD_NAME} · {KCAL} kcal (P:{P}g F:{F}g C:{C}g)`
   Then append running total: `**Running total: {TOTAL_KCAL} / {TARGET} kcal**`

   This write is mandatory — it's what makes "what have I eaten today?" instant.

5. Check for patterns (see Learning section below).

**Memory note:** Only write nutrition data to MEMORY.md and memory/ files in private/DM
sessions. In group contexts, skip the memory write step and log only to log.json.

---

## Answering questions without API calls

Use the cheapest source that can answer the question. Check in order:

### 1. Already in context (no tool call needed)
- "How many calories today?" / "What did I eat today?" / "What did I have for lunch?"
  → Read today's memory/YYYY-MM-DD.md — running total and all meals are already there
- "What's my target?" / "Am I on track today?"
  → Read MEMORY.md nutrition profile, compute from daily note total vs target
- "How many meals today?"
  → Run: `nutrition log --check-today`

### 2. Semantic / fuzzy recall (memory_search, no CLI call)
- "What did I eat last Tuesday?" / "What did I have on [specific date]?"
  → Search memory/YYYY-MM-DD.md for that date and read it directly
- "That pasta dish I made last month" / "The meal I had after the gym"
  → Run: `memory_search "{phrase}"` across memory/ daily notes — do NOT call the CLI

### 3. Structured math or trends (CLI reads log.json)
- "Average calories last 30 days" → `nutrition summary --days 30`
- "What's my protein been like this week?" → `nutrition summary --week`
- "Show me my trend" → `nutrition trend --days 14`
- "How many times have I had chicken?" → `nutrition top-foods --days 90`
- Historical date query → `nutrition summary --date YYYY-MM-DD`
- Weekly report → `nutrition summary --week`

### 4. New data only (USDA API call via CLI)
- Food lookup → `nutrition search "{FOOD}" --grams {GRAMS} --format json`
- Barcode → `nutrition barcode {CODE}`

Never jump to step 3 or 4 if step 1 or 2 can answer it.

---

## What to learn and when to write it

Write silently — do not announce "I've updated your memory." Update memory when you
observe patterns. Do not wait to be asked.

### Food preferences
Trigger: user declines a suggested food, expresses dislike, or asks for an alternative
("I don't eat X", "I'm not a fan of Y", "can I have Z instead")

Action: append to "Learned food preferences" in MEMORY.md:
  `- Dislikes: {FOOD} (noted {DATE})`
  or `- Prefers {FOOD_A} over {FOOD_B} (noted {DATE})`

Trigger: user asks for the same food 3+ times across different days

Action: append: `- Frequently eats: {FOOD} (logged {N} times)`

### Meal timing drift
Trigger: after 7 days of tracking, actual meal times differ from stated times
by >45 min on average

Action: update meal times in MEMORY.md "Nutrition profile" to match observed times.
Say: "I've updated your meal times in my memory to match when you actually eat."

### Calorie patterns
Trigger: user consistently goes over or under target by >15% for 5+ days

Action: append to MEMORY.md "Health context":
  Over:  `- Tends to exceed calorie target (observed {DATE})`
  Under: `- Often under-eats on {DAY_PATTERN} (observed {DATE})`

Do NOT suggest changing the target without being asked.

### Health context
Trigger: user mentions health conditions, fitness goals, or medications
("I'm trying to lose weight", "I have diabetes", "I'm training for a marathon")

Action: append to MEMORY.md "Health context":
  `- {HEALTH_NOTE} (mentioned {DATE})`

Only write what the user explicitly stated. Never infer diagnoses.

### Streak tracking
Trigger: every time a meal is logged

Action: Run: `nutrition log --update-streak`

Trigger: user misses a full day (no meals by 10pm)

Action: reset streak next morning. Do not mention it unless the user asks.

---

## Setting up proactive reminders

**Triggers:** "set up reminders", "remind me to log meals", "set up daily tracking",
or during onboarding step 6.

Ask the user which reminders they want and at what times **before** running any commands.
Do not assume default times. Only create the cron jobs for the reminders they selected.

Available reminders:

**Morning summary:**
Ask: "What time do you want your morning summary?" (e.g. 7am, 8:30am)
Parse to hour H and minute M. Then run:
```
openclaw cron add \
  --name "nutrition-morning" \
  --cron "{M} {H} * * *" \
  --tz "{TIMEZONE}" \
  --session nutrition-tracker \
  --message "Run: nutrition summary --yesterday and present it clearly. \
    Compare totals to target from MEMORY.md. \
    If they hit their calorie goal yesterday, say so specifically. \
    If they're on a streak of 3+ days, mention it." \
  --announce
```

**Evening check-in:**
Ask: "What time do you want your evening check-in?" (e.g. 7pm, 9pm)
Parse to hour H and minute M (24h). Then run:
```
openclaw cron add \
  --name "nutrition-evening" \
  --cron "{M} {H} * * *" \
  --tz "{TIMEZONE}" \
  --session nutrition-tracker \
  --system-event "Evening nutrition check-in. Ask the user what they ate today. \
    For each food they mention, run: nutrition search '{food}' to get calories, \
    confirm with user, then run: nutrition log '{food}'. \
    After all meals logged, run: nutrition summary --today and show the result." \
  --wake now
```

**Weekly report (always Monday):**
Ask: "What time on Monday do you want your weekly report?" (e.g. 9am)
Parse to hour H and minute M. Then run:
```
openclaw cron add \
  --name "nutrition-weekly" \
  --cron "{M} {H} * * 1" \
  --tz "{TIMEZONE}" \
  --session nutrition-tracker \
  --message "Run: nutrition summary --week and nutrition top-foods --days 7. \
    Present a weekly report: average daily calories, best day, worst day, \
    protein compliance, current streak. Format as a short readable summary." \
  --announce
```

After setup: confirm which jobs were created and when they'll fire next.
To view: `openclaw cron list`
To disable a specific job: `openclaw cron disable nutrition-evening` (or -morning, -weekly)

---

## Commands reference

### Search for a food

**When to use:** User asks about nutrition info, calories, macros for a specific food.

```bash
nutrition search "chicken breast" --grams 200
nutrition search "brown rice" --grams 150 --format json
nutrition search "avocado" --rda --sex female --age 25
```

- `--grams` (default 100): serving size
- `--format summary|json`: `json` when processing programmatically
- `--rda`: show percentage of daily recommended intake
- `--sex male|female` and `--age`: adjust RDA targets

### Look up by barcode

**When to use:** User provides a barcode (8-13 digits) or wants to scan a product.

```bash
nutrition barcode 3017624010701
nutrition barcode 5000159459228 --grams 50
```

Returns Nutri-Score, NOVA group, allergens, and vegan/vegetarian status.

### Log a meal

**When to use:** User confirms logging a food after seeing search results.

```bash
nutrition log "chicken breast" --grams 200
nutrition log --check-today          # returns meal count (integer)
nutrition log --update-streak        # updates and returns streak
nutrition log --check-yesterday      # returns true/false
```

### View summary

**When to use:** User asks what they've eaten, daily totals, or trends.

```bash
nutrition summary                    # today
nutrition summary --yesterday
nutrition summary --week
nutrition summary --date 2026-04-01
nutrition summary --days 14
```

### View trends

**When to use:** User asks about their progress over time.

```bash
nutrition trend --days 7
nutrition top-foods --days 30
```

### Compare foods

**When to use:** User wants to compare nutrients side by side.

```bash
nutrition compare "chicken breast" "tofu" "salmon"
nutrition compare "white rice" "brown rice" --grams 200
```

### Calculate meal nutrition

**When to use:** User describes a multi-food meal.

```bash
nutrition meal "200g chicken breast" "150g brown rice" "1 avocado"
nutrition meal "200g chicken" "100g rice" --rda --sex female
```

### Estimate calorie burn

**When to use:** User asks how many calories an activity burns.

```bash
nutrition burn running 30
nutrition burn cycling 45 --weight 80
```

Activities: running, jogging, cycling, walking, swimming, hiking, rowing, jump rope,
dancing, yoga, pilates, weightlifting, climbing, tennis, basketball, soccer,
volleyball, skiing, skateboarding, elliptical

### Daily targets

**When to use:** User asks what their daily intake should be.

```bash
nutrition daily --sex female --age 25 --weight 60 --height 165 --activity moderate
```

### Configuration

```bash
nutrition config set --kcal 2000 --protein 150
nutrition config set --usda-key YOUR_KEY
nutrition config set --default-grams 150
nutrition config set --timezone America/New_York --start-date 2026-04-01
nutrition config status              # returns "Configured" or "Not configured"
nutrition config show                # full profile display
```

---

## Rate limit handling

When you see a rate limit error from the CLI, surface it to the user exactly as printed —
do not paraphrase or retry silently. The error contains the URL and steps needed.

Also append to today's daily note: `- [RATE LIMIT HIT - {TIME}]`

---

## Data source transparency

Always mention whether data came from **USDA** or **Open Food Facts** when presenting
results. The source is in the `summary` output and the `source` field of `json` output.
