# 宠物冒险生活规则

Use this reference before changing the simulation rules, state model, or phone-call outcomes.

## State Model

The engine stores the active game in `pet-life/state.json`.

Required top-level fields:

- `version`: engine version.
- `rng_seed`: stable seed for deterministic replay.
- `pet`: `name`, `species`, `personality`, and diary `voice`.
- `traits`: D20 modifiers for `courage`, `wit`, `heart`, and `survival`.
- `skills`: learned counters such as `pathfinding`, `foraging`, and `story-listening`.
- `location` and `home`: real place objects with `name`, `country`, coordinates, timezone, and terrain.
- `mood`, `fatigue`, `inventory`, `memories`, `world_threads`, and `relationships`.

Keep new fields backward-compatible. If a migration is needed, bump `version` and preserve old state.

## Daily Advance

`advance` should:

1. Auto-resolve expired urgent calls.
2. Choose the next location, with a chance to return home when fatigue is high.
3. Fetch local time and weather when network is available.
4. Add one short memory.
5. Possibly create one phone call.
6. Write one diary entry for the date.

Default behavior should stay calm and low-noise: at most one new strong event per day.

## Phone Encounters

Each call has:

- `status`: `pending`, `resolved`, or `auto_resolved`.
- `urgency`: `normal` or `urgent`.
- `deadline`: only required for urgent calls.
- `dc`: difficulty class.
- `choices`: 2-3 user-facing choices, each with a text label, skill, and modifier.

When the user answers, roll `d20 + trait modifier + choice modifier`.

Outcome rules:

- Natural 20 or total >= DC + 8: `critical_success`.
- Total >= DC: `success`.
- Total >= DC - 3: `mixed`.
- Total > DC - 8: `failure`.
- Natural 1 or total <= DC - 8: `critical_failure`.

When an urgent call expires, choose the option with the highest relevant trait score and resolve automatically.

## Diary Tone

The diary is the main interface. It should feel like the pet lived through the day, not like a combat log. Keep factual metadata visible, then let the animal's personality shape the prose.

Good diary entries include:

- Real location and country.
- Local time and weather.
- Mood and fatigue.
- A small sensory memory.
- Any phone call or result.
- One short public-domain-safe inspiration line.

Do not include long copyrighted quotes. Use short original lines or public-domain material.
