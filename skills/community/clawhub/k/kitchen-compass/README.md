# Kitchen Compass

A OpenClaw / Claude skill for planning the week's dinners — conversationally.

You have 20-ish dinners you actually cook. The problem isn't that you need more recipes. It's that every Sunday you have to pick which four or five to do this week, and somehow you end up with chicken three nights in a row and ordering Chipotle on Thursday.

Home cooking is less satisfying when it takes Operation Desert Storm level planning and logistics to pull off. 

Kitchen Compass turns it into a conversation with an agent:

> **You:** Plan me an easy week. We had burger bowls last night.
>
> **Agent:** *(records the history event, runs the planner against your recipes)* Here's an easy week built off what you just cooked — Slow Cooker Garlic Parmesan Chicken Tuesday, Baked Pork Chops with garlic mashed potatoes Wednesday, Sheet-Pan Shrimp Fajitas Thursday. Different protein each night, nothing that needs much effort, and it keeps you away from burger bowls since you just had them.
>
> **You:** Swap the shrimp for something my kids will eat.
>
> **Agent:** *(re-queries the planner with a family-table constraint)* Swapped to Slow Cooker Short Ribs — better family-table fit and still low friction on a weeknight.

And when it's time to cook, the recipe comes back in the same conversation:

> **You:** Need to start the garlic parm chicken for tonight, can you send me the recipe?
>
> **Agent:** Yep — here you go.
>
> **Slow Cooker Garlic Parmesan Chicken**
>
> - Serves: about 4, maybe 5 with extra sides
> - Prep: 15–20 min
> - Cook: 6–7 hrs low or 3–4 hrs high
>
> **Ingredients**
>
> - 8 bone-in, skin-on chicken thighs
> - 2 tsp garlic salt
> - 2 tsp paprika
> - 2 tsp pepper
> - 6 cloves garlic, minced
> - 6 tbsp extra virgin olive oil, divided
> - 2 lb baby potatoes, halved or quartered
> - 2 cups shredded Parmesan
> - Parsley, optional
>
> **Instructions**
>
> 1. Mix garlic salt, paprika, and pepper in a small bowl.
> 2. ...

Gone are the days of digging through a drawer for the index card, or scrolling past fourteen pop-up ads and a blogger's Tuscany honeymoon story to find out how long to sear the chicken. Your recipes live in your data root; the agent surfaces them on request.

Under the hood there's a deterministic planning engine — weighted scoring, hard constraints, history-aware, composition-aware — but you don't drive it. The agent drives it. You talk.

## What you need

Kitchen Compass is a **skill**, not a standalone app. It needs an agent host with filesystem access to be useful.

**Primary host: Openclaw.** This is the host it was built against and the one to install on first. Openclaw is model-agnostic (run it against Claude, or whatever else you prefer) and it runs the agent against your local filesystem, which means your recipes, history, and inventory all live on your machine and persist between conversations.

**Should also work, but untested:** Claude Code and Claude Cowork. Both can read and write the local filesystem and invoke scripts, so the skill should operate normally in either environment. File an issue if you try one and it misbehaves.

**Not a fit:** a chat interface with no connected filesystem. The skill needs to persist recipes, history, and inventory between turns.

## What you can say to it

Once installed, the agent handles all of these conversationally:

### Planning

- "Plan me a cheap week."
- "Build a balanced plan for hosting on Saturday."
- "Give me four easy dinners — nothing fussy."
- "Why did you pick the short ribs?" (the agent reads you the per-pick reasons)
- "Swap Wednesday for something low-carb."

### Recording what you cooked

- "We had burger bowls tonight."
- "Made the short ribs for Sunday dinner."
- "Planned pasta for Thursday but we ended up doing takeout."

History shapes next week's plan automatically. Dinners you actually made count more than dinners you only planned.

### Pulling up a recipe when it's time to cook

- "What's in burger bowls again?"
- "Pull up the short ribs recipe."
- "Read me the steps for the pork chops."
- "What sides go with the baked chicken?"

The full recipe — ingredients, steps, your house notes — comes back in chat. No searching, no ads, no hunting.

### Adding a new recipe

The recommended path is to hand the agent a link. "Add this recipe to my catalog: *https://some-food-blog.example.com/fantastic-salmon*" and the agent will read the page, pull the actual recipe out, and write it to your catalog in the right schema. A photo or a copy-paste works the same way.

You can layer house changes on top in plain language:

- "Drop the cilantro."
- "We use half a cup of olive oil instead of the full cup it calls for."
- "Add 'finish under the broiler for two minutes' at the end — I like the skin crispy."

The agent tracks both the original and your house version, so you always know what the source recipe said and what you changed.

### Leaving notes on existing recipes

Plain-language comments become structured recipe updates.

- "The garlic parmesan chicken takes longer than the recipe says because I broil it at the end. Update the recipe."
- "The roasted broccoli is better at 425 than 400. Save that."
- "We always double the garlic in the mashed potatoes."

### Inventory

- "Put two pounds of ground beef in the freezer."
- "Used the last of the pork chops."
- "What's in the freezer right now?"

Inventory nudges the planner toward dinners you already have ingredients for.

### Querying the catalog

- "What beef recipes do I have?"
- "Show me self-contained dinners that don't need a side."
- "What can I make with what's in the freezer?"

### Weekly deals

- "Scan this week's Aldi flyer." (the agent walks the saved retrieval recipe)
- "Here are the key deals — which ones should I build this week's plan around?"

After reviewing the deals, you decide which to incorporate. The agent replans with those proteins or ingredients in mind. Deals never enter planner scoring automatically — that's deliberate, so you don't end up eating what's on sale instead of what fits the week.

### Shopping lists

- "Build me a shopping list for this week's plan. Leave out spices and pantry staples we already have."

The agent reads the plan, consolidates ingredients across recipes, and subtracts anything you've told it is already in the pantry or freezer.

## Not a recipe discovery tool — the right home for the ones you do discover

Kitchen Compass won't recommend dinners you've never heard of. What it *will* do is give you the exact right place to store that great recipe you came across on Instagram, or the one your sister-in-law mentioned at Thanksgiving, or the one you pulled off a blog last year and swore you'd make again.

Hand it to the agent, tell it about your house changes, and it's in rotation the next time you plan a week. The recipes you discover stop evaporating.

## Quick verification (optional)

If you want to prove the engine works before wiring it up to an agent, the scripts run standalone:

```bash
git clone https://github.com/drewsadik-ctrl/kitchen-compass.git
cd kitchen-compass
python3 scripts/setup_household.py --data-root ~/kitchen-compass-data
python3 scripts/build_recipe_query_index.py --data-root ~/kitchen-compass-data
python3 scripts/build_weekly_plan.py --data-root ~/kitchen-compass-data --preset balanced
```

You'll get a rendered weekly plan against the shipped sample household. Once you've seen that work, point Openclaw (or your other agent host) at the skill directory and a data root, and stop running the scripts by hand.

## What a plan looks like

Real output from the sample household on the balanced preset. This is what the agent is reading (and paraphrasing) when it tells you about your week:

```
# Balanced week

Default practical week: mostly trusted, low-friction dinners with one slot
for something slightly more interesting.

- Target dinners: 3
- Picked dinners: 3
- Protein variety: {"beef": 1, "chicken": 1, "pork": 1}
- Effort mix: {"easy": 3}
- Friction mix: {"low": 3}

## Dinner 1 — Burger Bowls
- Why it made the cut: easy to cook; low ingredient friction; trusted house
  recipe; good family-table fit; self-contained dinner
- Composition: self-contained dinner this week; no extra side is required.

## Dinner 2 — Slow Cooker Garlic Parmesan Chicken
- Why it made the cut: easy to cook; low ingredient friction; trusted house
  recipe; good family-table fit; self-contained dinner
- Composition: self-contained dinner this week; no extra side is required.

## Dinner 3 — Baked Pork Chops
- Why it made the cut: easy to cook; low ingredient friction; trusted house
  recipe; good family-table fit; needs side support
- Composition: treat this as a main that wants a side: Garlic Mashed Potatoes.
- Suggested side: Garlic Mashed Potatoes — dinner explicitly asks for
  garlic mashed potatoes.
```

The per-pick reason strings are the planner's main debugging surface. The agent surfaces them when you ask.

## What it does not

- **Scrape retailer circulars autonomously.** Deal retrieval is manual or guided. The per-store retrieval notes capture what worked last time, so it gets easier with repetition.
- **Plan breakfast, lunch, snacks, or desserts.** v1 is dinner plus side.
- **Track real-time stock.** Inventory is remembered approximate state, not a live count.
- **Wash your car.**

## Design principles

**Explainability over cleverness.** Every pick comes with reason strings. The LLM isn't making the picks — it's running a deterministic engine and explaining what came out. That separation is what keeps the planner trustworthy even when the conversation feels magical.

**Hard constraints and soft signals stay separated.** Whether a recipe is *allowed* in the week is a different question from how it *ranks*. Preserving that boundary is what keeps a high-scoring week from being a miserable one.

**Your recipes, not somebody else's.** Kitchen Compass is not a recipe discovery tool. It operates on the dinners you already know how to make — and gives you a durable home for the new ones you find.

**Portable engine, separate user data.** The skill ships no real household data. The engine points at a `--data-root` you own. Move it, back it up, or version it independently.

**Authored vs. generated is enforced.** Recipes, household config, inventory state, history, and deal inputs are things you author (or that the agent writes on your behalf). Everything under `generated/` is rebuildable. Nothing under `generated/` is ever read back in as input.

## How the planner works

When the agent asks for a week, the planner runs a strict five-level signal hierarchy:

1. **Hard constraints.** Preset-level caps on involved meals, expensive meals, friction-heavy meals, aspirational or testing meals, and side-dependent dinners. These eliminate candidates regardless of how well they would otherwise score.
2. **Core scoring signals.** Weighted preferences over effort, friction, cost, trustedness, serving profile, composition, and context.
3. **Week-balance shaping.** Penalties for repeating a protein family, stacking side-dependent dinners, stacking moderate-or-involved meals.
4. **History-aware shaping.** Recent-repeat penalties, long-gap bonuses, recent protein and role concentration penalties. Dinners you actually made count more than dinners you only planned.
5. **Optional signals.** Remembered inventory contributes a small capped bonus that can nudge tie-breakers but cannot repair a bad week.

Weekly deal briefs sit **outside** that stack. They can inform a human decision to pivot the week, but they never enter planner scoring automatically.

Presets (`balanced`, `easy`, `cheap`, `low-carb`, `hosting-friendly`) change both hard caps and scoring weights. Full explanation in `references/planning-logic.md`. Exact numbers live in `scripts/planner/presets.py`.

## Repository layout

- `SKILL.md` — instructions for the agent operating Kitchen Compass
- `scripts/` — CLI entrypoints the agent invokes, plus the `planner/` package (candidates, scoring, history, render)
- `scripts/contract.py` — single source of truth for schema constants and enums
- `references/` — recipe schema, runtime contract, planning logic, inventory logic, setup flow, deal brief contract, portability boundary
- `assets/sample-household/` — seeded sample recipes and household config
- `assets/recipe-template.md` — authoring template for new recipes
- `tests/` — pytest suite: contract alignment, validation, planner scoring, history, end-to-end golden path
- `Makefile` — `test`, `smoke`, `plan`

## Key scripts

The agent invokes these on your behalf. You don't need to memorize them. They're documented here for contributors and for debugging.

Each takes `--data-root <path>` or reads `KITCHEN_COMPASS_DATA_ROOT`. The legacy `FOOD_BRAIN_DATA_ROOT` still works but is deprecated.

- `setup_household.py` — bootstrap a fresh data root from the sample household
- `validate_recipes.py` — enforce the recipe schema
- `build_recipe_query_index.py` — rebuild the query catalog from validated recipes
- `build_weekly_plan.py` — render a weekly plan against a preset
- `query_recipes.py` — filter recipes by meal type, composition, diet, etc.
- `manage_inventory.py` — explicit inventory updates
- `record_meal_history.py` — append history events
- `manage_deal_sources.py` — saved stores, retrieval recipes, scan schedule
- `prepare_weekly_deal_scan.py` — weekly scan packet and per-store stubs
- `render_weekly_deal_brief.py` — single-store weekly brief
- `render_combined_weekly_deal_sheet.py` — combined weekly sheet grouped by category

## Developing

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

make test    # pytest: contract alignment, validation, planner scoring, history, golden path
make smoke   # full CLI golden path against a throwaway data root
make plan    # bootstrap a sample root and render one plan
```

Both `make test` and `make smoke` should pass before opening a PR. See [CONTRIBUTING.md](CONTRIBUTING.md) for the invariants — especially the frozen recipe schema and the rule against casually tuning planner weights.

## Status

v1. Built and daily-driven against Openclaw. Claude Code and Cowork should work but haven't been validated yet. The active planner guarantees dinner plus side. The deal workflow is manual or guided by design. Inventory is approximate household memory, not real-time stock. Everything documented here is honest about its seams.

## License

[MIT](LICENSE)
