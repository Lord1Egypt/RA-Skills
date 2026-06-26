# Kitchen Compass planning logic

This document explains, in human-readable terms, how Kitchen Compass currently builds weekly dinner plans and how optional signals like inventory are supposed to fit into that logic.

This is a companion to:
- `recipe-schema.md`
- `runtime-contract.md`
- `inventory-logic.md`
- `scripts/build_weekly_plan.py`

Shared machine-used constants live in code.
This document is the product/logic explanation layer.

## Why this document exists
Kitchen Compass already has real planner logic in code.

What this document does is make the intent legible:
- what the planner optimizes for
- what it treats as hard constraints vs soft preferences
- how presets actually shape results
- how composition/history influence scoring
- where optional signals like inventory enter the stack

## Active v1 scope
The planner is currently built for:
- **dinner** selection
- with supporting **side** or **protein-pairing** suggestions when the recipe composition calls for it

It is **not** a full-meal-type planner.
Breakfast, snack, appetizer, dessert, and component recipes can exist in the system, but the active planner is dinner-first.

## Core planning principle
Kitchen Compass does **not** try to find the single "best recipe" in a vacuum.
It tries to build a **good week**.

That means the planner is optimizing for week-level balance, not just individual-recipe appeal.

Examples:
- one dinner being great is not enough if it makes the whole week too annoying
- using the same protein too often is usually bad
- stacking too many side-dependent dinners is usually bad
- repeating something too recently is usually bad

So the planner is a **ranked selection system with week-level guardrails**.

## What the planner uses today
The current planner uses these inputs:

### 1. Recipe metadata from the generated query catalog
This comes from validated recipe markdown and includes things like:
- effort
- ingredient friction
- cost
- status (`trusted`, `testing`, `aspirational`)
- serving profile
- diet modes
- context/occasion
- composition flags
- pairing intelligence

### 2. Household defaults
Current household preferences drive:
- `planning.default_preset`
- `planning.default_dinners_per_week`

### 3. Meal history
If history exists and is not ignored, the planner uses recent dinner history to avoid over-repeating:
- exact recipes
- protein families
- structural roles

### 4. Remembered inventory
If `inventory/items.json` exists, the planner can apply a small capped bonus to already-valid dinners when remembered inventory clearly supports them.

## Planner flow
At a high level, the planner works like this:

### Step 1 — build the dinner candidate pool
The planner starts from dinner recipes in the generated catalog.

It then filters that pool by preset-level rules:
- if the preset requires a diet mode, only dinners in that lane survive
  - example: `low-carb` requires the `low-carb` diet mode
- if aspirational dinners are not allowed, they are removed from the pool

### Step 2 — enforce hard mix limits
Before a dinner can be added, it must pass hard week-level guardrails for that preset.

Examples of hard guardrails:
- too many involved dinners
- too many medium/high-friction dinners
- too many expensive dinners
- too many testing or aspirational meals
- too many dinners that require side support

These are not just score penalties.
They can make a candidate ineligible for the week entirely.

### Step 3 — score each valid candidate against the current week state
For each still-eligible dinner, the planner calculates a score.

That score is influenced by:
- preset weights
- what is already selected for the week
- recent history, if available
- remembered inventory, if it supports the recipe

### Step 4 — pick the highest-ranked valid dinner
The planner sorts candidates by:
1. score descending
2. title as a stable tiebreaker

Then it picks the best valid option and repeats until it fills the target number of dinners or runs out of valid candidates.

### Step 5 — explain the selected dinner
After selection, the planner adds a human explanation layer:
- why the dinner made the cut
- what composition it has
- whether it wants a side
- whether it needs a protein add-on
- what side is suggested if pairing intelligence can provide one
- whether remembered inventory helped the pick

## Hard constraints vs soft preferences
This distinction matters.

### Hard constraints
These determine whether a recipe is even allowed into the week.
Examples:
- too many involved meals
- too many expensive meals
- too many aspirational/testing meals
- too many side-dependent dinners
- preset diet-mode gate (for example low-carb)

### Soft preferences
These influence ranking, but do not force or ban a meal by themselves.
Examples:
- easy vs moderate vs involved
- low vs medium vs high ingredient friction
- cheap vs medium vs expensive
- trusted vs testing vs aspirational
- self-contained vs wants-side vs needs-protein-pairing
- comfort-food / hosting / sale-trigger context
- repeat-protein pressure
- recent-history penalties
- inventory support

## Current scoring signals
The current scoring logic uses a weighted system.
The exact numbers live in code, but the signal categories are:

### Effort
Bias toward easier dinners in easier presets.
Penalty for involved dinners where they would make the week too heavy.

### Ingredient friction
Bias toward dinners with simpler, less annoying shopping/execution burden.
Penalty for stacking too many medium/high-friction meals.

### Cost
Bias toward cheaper dinners in cheap/balanced weeks.
Penalty for expensive dinners in routine weeks.

### Status
Bias toward trusted house recipes.
Smaller tolerance for testing meals.
Penalty or exclusion for aspirational meals depending on the run.

### Serving profile
Bias toward recipes that fit the current household use case.

### Composition
Bias depends on whether a dinner is:
- `self-contained`
- `wants-side`
- `needs-protein-pairing`
- `flexible`

In general:
- self-contained dinners get a planning bonus
- side-dependent dinners get some penalty
- protein-pairing dinners get a stronger penalty because they require more assembly to feel complete

### Context / occasion
Small bonuses or penalties can apply for contexts like:
- `sale-trigger`
- `hosting`
- `comfort-food`

### In-week repetition
The planner penalizes:
- repeating the same protein family too often
- stacking too many side-dependent dinners
- stacking too many medium/high-friction meals
- stacking too many moderate/involved dinners
- stacking too many testing meals

### History-aware drift control
If history is enabled, the planner also penalizes or rewards based on recency.

It cares about:
- exact recipe repeats
- recent protein-family concentration
- recent structural-role concentration
- whether something has not appeared in a long time

This is how Kitchen Compass avoids feeling repetitive across weeks, not just inside one generated week.

### Inventory-aware lift
If remembered inventory clearly supports a recipe, the planner can apply a small capped bonus.

This bonus is intentionally weaker than hard constraints and most core scoring categories.
It is there to help with practical tie-breaking and gentle nudging, not to turn the week into a freezer dump.

## Presets — what they really mean
The presets are not just labels.
They change both:
- hard mix limits
- scoring weights

### `balanced`
Default practical week.
Goal:
- mostly trusted meals
- low friction overall
- one slightly more interesting slot at most

### `easy`
Weeknight convenience bias.
Goal:
- low effort
- low friction
- highly proven meals
- minimal stacking of annoying dinners

### `cheap`
Savings-first bias.
Goal:
- favor cheap dinners
- still keep friction low enough that savings feel worth it

### `low-carb`
Keep the planner inside the low-carb lane.
Goal:
- only choose dinners tagged for low-carb participation
- still preserve variety and week quality

### `hosting-friendly`
Allow a more special / shareable dinner mix.
Goal:
- tolerate one bigger or more special meal
- still avoid building a week that is all projects

## Composition and side logic
Composition is one of the most important structural planner inputs.

### `self-contained`
This dinner should feel complete on its own.
No side is required.

### `wants-side`
This dinner is a main, but it is better with a side.
The planner can try to attach a suggested side from pairing intelligence.

### `needs-protein-pairing`
This is more like a base dinner concept than a complete protein-centered meal.
The planner can attach a suggested protein add-on.

### `flexible`
This dinner can stand on its own, but a side is optional.

## History logic in practical terms
The planner reads dinner history as a recency/variety signal.

### It discourages:
- exact repeats too soon
- recent overuse of the same protein family
- recent overuse of the same structural role

### It slightly rewards:
- dinners that have not shown up recently

### It weights history events differently
- `made` events count more than `planned` events

That keeps real cooked behavior more important than tentative plans.

## Inventory logic in practical terms
Inventory is now a real planner signal.

By default it stays deliberately small.
If `planning.prioritize_inventory` is set to `true`, strong inventory matches get pulled up more aggressively, but inventory still does not outrank hard constraints or repair a bad week.

### What it does
It can make a valid dinner more attractive when:
- the meal already fits the preset
- the meal already passes hard constraints
- remembered inventory clearly supports it
- the saved quantity is still positive

### What it does not do
It does **not**:
- silently subtract inventory after planning or history writes
- override preset fit
- override week-quality guardrails
- pretend to know exact recipe-consumption math

### Matching lanes
The current implementation uses three soft match lanes:
- explicit recipe slug match — strongest
- inventory search-term match against recipe title/slug/ingredients/planning text — medium
- broad core-protein lane match — weakest

### Quantity behavior
Quantity affects the size of the bonus only approximately.
That means:
- more clearly usable quantity can get a fuller bonus
- a small positive quantity can still get a reduced bonus
- zero quantity gives no bonus

This is a remembered-practicality model, not exact stock accounting.

### Explanation behavior
When inventory helps a selected dinner, planner output says so plainly.

Example style:
- `Inventory support: you already have 3 lb ground beef in the freezer (matches recipe text for ground beef)`

If inventory does not help, the planner stays quiet about it.

## Why the planner is not just a filter
Kitchen Compass is not doing:
- hard meal-by-meal elimination based on a giant rule tree
- LLM-generated arbitrary rankings
- "pick from whatever sounds good today"

It is doing:
- contract-based candidate generation
- weighted scoring
- mix constraints
- history-aware variety control
- composition-aware explanation
- inventory-aware soft bonuses

That is much more stable and debuggable.

## Design hierarchy
Planner signal order should remain:
1. **Hard constraints**
2. **Core scoring signals**
3. **Week-balance shaping**
4. **History-aware shaping**
5. **Optional planning signals**
   - inventory

Weekly deal briefs sit **outside** that stack.
They can influence a user's decision to pivot the week, but not by entering planner scoring.

This is the mechanism that keeps optional signals useful without letting them take over.

## What still lives only in code
Even with this doc, some things still live most precisely in code:
- exact per-preset numeric weights
- exact threshold cutoffs for repeat/history penalties
- exact hard-cap counts per preset
- exact inventory bonus cap and quantity-tier math

That is okay.
This doc is meant to make the logic understandable and editable in principle, not duplicate every literal numeric constant.

## How to use this document
Use this doc when:
- evaluating whether the planner is behaving rationally
- deciding where a new signal belongs
- deciding whether something should be a hard constraint or soft bonus
- deciding whether a new feature fits the planner cleanly
- tuning planner behavior without turning it into a black box

## Strong design rule going forward
If a new feature cannot answer these questions, it probably should not enter the planner yet:
- Is it a hard constraint or a soft signal?
- What existing logic can it override, if any?
- How should it affect explanations?
- How do users correct it when it is wrong?

That rule is especially important for inventory and anything adjacent to stores or external deal-awareness work.
