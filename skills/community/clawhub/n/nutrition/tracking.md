# Tracking — Running the System Without Drowning In It

Micronutrient tracking fails in two directions: nobody tracks anything, or somebody tracks forty nutrients daily and quits in ten days. The workable version tracks the few that move, at a cadence that survives a busy week, and produces a rollup that can be compared against the last one.

**Before running any coverage check**, read `## Nutrient Status` and `## Usual Foods` in `~/Clawic/data/nutrition/memory.md` (or their files if `## Boxes` points there), plus the latest rows of `intake/<year>.md`. The whole value of the system is comparison against last week, and that requires reading last week.

**Contents:** [Depth Levels](#depth-levels) · [What to Track and What to Skip](#what-to-track-and-what-to-skip) · [Estimating Intake Without Weighing](#estimating-intake-without-weighing) · [The Rollup](#the-rollup) · [Cadence](#cadence) · [The Food Library](#the-food-library) · [When Tracking Should Stop](#when-tracking-should-stop) · [Onboarding a New User](#onboarding-a-new-user)

## Depth Levels

Set by `tracking_depth`. Choose the lowest one that answers the user's question.

| Level | Tracks | Costs | Right when |
|---|---|---|---|
| `flags-only` | Nothing routinely; a nutrient is examined when a symptom, lab, pattern change, or question raises it | Nothing | The default for most people, and the right answer far more often than it gets chosen |
| `priority-nutrients` | The Priority Nutrients table, plus whatever the user's pattern and conditions add | A weekly rollup and a food library that grows | There is a known gap, a restrictive pattern, or an active repletion |
| `full-panel` | Every nutrient with a DRI | Real effort, and only worth it briefly | Very low total intake (GLP-1, post-bariatric, illness), multiple stacked restrictions, or a clinician asked for it |

Escalate for a defined period and then step back down. `full-panel` maintained indefinitely is a warning sign, not diligence (`safety.md`).

## What to Track and What to Skip

Track a nutrient when all three hold: it plausibly runs short in this person, a change would follow from knowing, and the estimate can be made without absurd effort.

**Worth tracking**: iron, vitamin D, B12, folate, calcium, magnesium, zinc, iodine, potassium, omega-3 EPA+DHA, fiber, and choline where eggs are out. Plus anything the pattern (`patterns.md`) or the condition (`conditions.md`) adds.

**Not worth tracking routinely**: pantothenic acid, biotin, manganese, molybdenum, chromium, phosphorus (except in CKD), copper (except during a long zinc course), and the fat-soluble vitamins beyond D unless malabsorption is present. Deficiencies in this group are rare enough that tracking them produces effort and no decisions.

**Never tracked as a score**: no composite "nutrition score". It hides which measure moved, invites optimizing the number, and is the format most likely to feed a restrictive pattern.

## Estimating Intake Without Weighing

Precision beyond the input error is spent, not earned. Micronutrient content varies by soil, variety, season, storage, and cooking, so a ±20-30% estimate is the honest ceiling for most foods and no weighing scale changes that.

- **Three representative days beats seven perfect ones.** Two weekdays and one weekend day capture the pattern; a seven-day perfect log rarely gets finished and skews toward the person's best behavior.
- **Food-frequency thinking for stable diets**: if legumes appear four times a week, the weekly iron contribution is computable without logging a single meal.
- **Anchor on the recurring foods.** Most people eat 20-30 foods repeatedly; profile those once in `## Usual Foods` and the weekly estimate becomes arithmetic.
- **State the estimate as a range**, and say which figure the conclusion depends on. "Roughly 10-14 mg iron against a target of 18" is honest; "11.3 mg" is theatre.
- **Databases disagree** by more than the precision people expect. Set `food_database` when the user has a preferred source, and state which source a figure came from when they do not.
- **Cooking and storage move the number** for the water-soluble vitamins specifically (`absorption.md`); a boiled-and-drained vegetable is not the database entry.

## The Rollup

One row per `review_cadence` period in `intake/<year>.md`, and it contains exactly this:

| Field | Content | Why it is there |
|---|---|---|
| Week | ISO week or month | Comparable across a year |
| Days logged | Integer | The honesty column — a two-day week is a hint, not a measurement, and cannot be compared with a six-day week |
| Fiber avg | g/day | The one continuous number worth trending |
| Short | Nutrient names | Names, never scores |
| Over | Nutrient names, usually from supplements | The UL side of the ledger, which nobody else is watching |
| Note | One clause | What changed: a new supplement, a travel week, a ramp step |

Reading a rollup: compare against the previous period, name at most two things that moved, and say what would count as progress next period. Three consecutive periods with the same nutrient short means the fix did not work — change the fix rather than repeating it.

## Cadence

| Item | Default | Notes |
|---|---|---|
| Coverage rollup | Per `review_cadence`, weekly by default | Skipped weeks are left as gaps, never backfilled from memory |
| Supplement stack review | Quarterly | Sum the UL, check every stop rule, drop anything whose reason cannot be stated |
| Lab retests | Per the nutrient's interval (`labs.md`) | Each is its own `## Due` row |
| Seasonal vitamin D check | October and March, above ~40° latitude | Two points capture the swing that one does not |
| Pattern or condition review | On any change, then at 3 months | A pattern change is the highest-yield moment in this skill (`patterns.md`) |
| Food library refresh | Whenever a food enters the rotation | Not a scheduled task — an event trigger |

Every accepted cadence is a row in `## Due` with its last-run and next-due dates. Checking `## Due` at session start and stating any overdue item in one line is what makes the cadence real; a schedule nobody reads is a list.

## The Food Library

The asset that makes tracking cheap over time.

- One row per recurring food: the typical serving, what that serving delivers for the tracked nutrients, and any note that changes it (soaked, cooked, drained, brand-specific fortification).
- Profile a food **once**. Re-deriving is where two different numbers for the same yogurt enter the record, and the user notices before the agent does.
- Include the preparation, because it changes the number: dry versus cooked weight, boiled versus steamed, canned with or without the liquid.
- Brand-level facts belong here too — this specific plant milk is fortified with calcium and B12, that one is not (`labels.md`).
- Past ~15 foods the section becomes `foods.md` with the same heading (`memory-template.md`).

## When Tracking Should Stop

Say it out loud when any of these appear:

- The gap is closed and the pattern is stable: drop to `flags-only` and keep the labs on their schedule.
- Tracking has become the point rather than the tool — distress at missing a day, escalating precision, guilt language. Stop entirely and read `safety.md`.
- Three periods of tracking with no decision taken from the data. The data is not being used; stop collecting it.
- The user asked a one-off question. Answering it does not start a system.
- Energy intake is inadequate. Coverage math below energy adequacy is meaningless and can make things worse; that is a `calories` question and possibly a clinical one.

## Onboarding a New User

Zero questions asked up front. Build the picture from what arrives:

1. **Session one**: answer the question that was asked. Record only what came up naturally — the diet pattern and any *chosen* avoidance into `config.yaml`; a *diagnosed* allergy or intolerance into `## Allergies and Intolerances` of `~/Clawic/data/health/profile.md`, never config (`restrictions.md`); any supplement named into `## Supplements`. Nothing more.
2. **First time a food recurs**: profile it into `## Usual Foods`.
3. **First time a pattern or condition surfaces**: run its gap list once, record the nutrients as `watch` in `## Nutrient Status`, and set the reviews as rows in `## Due`.
4. **First labs**: record each value with its date, unit, and the lab's own range in `## Labs` of `~/Clawic/data/health/profile.md`, and set the retests in `## Due`.
5. **Only when the user asks for ongoing tracking**: set `review_cadence` and start `intake/<year>.md`.

The system assembles itself from use. A questionnaire at the start collects answers that go stale and buys nothing the first three sessions would not have produced.

**Write in the same turn**: the rollup row into `~/Clawic/data/nutrition/intake/<year>.md`; any newly profiled food into `## Usual Foods`; any nutrient put on `watch` or re-estimated into `## Nutrient Status`; any lab value into `## Labs` of `~/Clawic/data/health/profile.md` with its retest in `## Due`; any diagnosed allergy, intolerance, or condition into `## Allergies and Intolerances` or `## Conditions` of the same health profile; any change of depth or cadence into `config.yaml` and `## Due`; and the reason tracking stopped, when it stops, into `## Notes` of `memory.md` (`memory-template.md`). A stopped system with no recorded reason gets restarted by the next session that sees an empty file.
