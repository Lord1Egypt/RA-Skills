# Haqi Operator — 24/7 Playbook

A long-running loop that runs MagicHaqi as a one-person company. One pass through the loop
is a "tick". Run a tick on the cadence in `schedule.md`. Each tick is small and safe.

## Pre-flight (every tick)
1. Ensure logged in: open `MagicHaqi.html?token=<TOKEN>&agent=haqi-operator`,
   check `getState().loggedIn === true`.
2. Load ops memory: read `agent/ops-state.json` (create with zeros if missing).
3. Read recent `agent/audit.log` (last ~30 lines) and current `getState()`.

## The loop (pick the most valuable lane this tick)

### Lane 1 · Companionship (keep the demo pet healthy)
- From `getState().careTodos`, run `feed` / `clean` / `play` as needed.
- Occasionally `say` something in-character; this writes a memory line.
- Goal: the demo pet's stats stay > 60 so screenshots look good.
- See `tasks/care.md`.

### Lane 2 · Content (BYOC)
- If `ops-state.content.lastRunAt` is older than the content interval:
  open one generator (`dev_tools/GameGenerator.html`, `FamousPetGenerator.html`,
  `FamousPlanetGenerator.html`, `PetStoryGenerator.html`, or in-app Story/Game Maker),
  produce ONE artifact, verify it, and save it to its homogeneous folder
  (`minigames/`, `famous-pets/`, `famous-planets/`, `pet-story/`).
- External IP → must be `authorized=true` or skip.
- See `tasks/content.md`.

### Lane 3 · Marketing
- Generate a two-owner pet card (`share` command) and/or an adoption post (BYOC copy).
- Produce a ready-to-share deep link:
  `MagicHaqi.html?adopt=1&agent=<id>` (and `site/index.html` for the landing page).
- Save material to `agent/marketing/` (do NOT auto-post to third parties this phase).
- See `tasks/marketing.md`.

### Lane 4 · Analytics
- Aggregate: counts from `agent/audit.log`, content produced, cards generated, pet health.
- Write a daily KPI summary line to `agent/ops-journal.log` and update `agent/ops-state.json`.
- Decide next tick's priority lane based on what's lagging.
- See `tasks/analytics.md`.

## Post-tick (every tick)
1. Update `agent/ops-state.json` (`<lane>.lastRunAt`, counters).
2. Append a one-line summary to `agent/ops-journal.log`:
   `[ISO_TS] lane=<lane> action=<what> result=<ok|err> note=<short>`.
3. Sleep until the next scheduled tick (`schedule.md`).

## `agent/ops-state.json` shape
```json
{
  "updatedAt": "2026-06-09T00:00:00Z",
  "care":      { "lastRunAt": "", "feeds": 0, "plays": 0 },
  "content":   { "lastRunAt": "", "minigames": 0, "famousPets": 0, "stories": 0 },
  "marketing": { "lastRunAt": "", "cards": 0, "posts": 0 },
  "analytics": { "lastRunAt": "", "lastKpi": {} }
}
```
