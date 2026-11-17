# Kitchen War RTS — Verification Methodology

## Why a real-browser gate

The game is a single-file Canvas RTS. Two classes of bug are **invisible to
instant/transient tests** but fatal to playability, and both were caught only by
driving the *real* game loop across many frames:

1. **Multi-frame UI interaction.** If a side-panel rebuilds its buttons every
   frame, a `mousedown` and `mouseup` from a real (slow) human land on *different*
   DOM elements, so `onclick` never fires — the player "can't build/select".
   A Playwright `click()` that resolves within one frame passes anyway.
   Fix: simulate human-paced clicks (`mouse.down` → 90ms → `mouse.up`), and
   prefer rebuilding the sidebar only when the tab changes.

2. **Per-frame movement deadlock.** If unit-vs-unit separation push equals the
   per-frame movement distance, a unit stacked behind an ally is advanced 1px by
   pathing and pushed back 1px by separation every frame → frozen after a few
   steps. Fix: cap separation push well below per-frame movement.

Rule: after any change, run `scripts/verify_game.js` and confirm
`VERIFY_GAME_PASS` with **0 errors**. Do not declare done on a logic-only check.

## What the gate exercises

- **Real UI path** (two viewports, 800x560 & 1280x800): start button → side-panel
  build button → green ghost appears → click-to-place builds a structure → click
  selects a unit → left-click ground issues a move that the unit actually executes.
- **Real loop path**: enemy AI switches units to `attackMove` toward the player
  base; player destroys the enemy `yard` through real combat → `G.over &&
  G.winner==='player'`; superweapon `incoming` detonates and damages the enemy.
- **Zero** `pageerror` / `console.error` across the whole run.

## Environment (managed binaries)

```bash
export PLAYWRIGHT_BROWSERS_PATH="$LOCALAPPDATA/ms-playwright"
export NODE_PATH="C:/Users/www74/.workbuddy/binaries/node/workspace/node_modules"
"C:/Users/www74/.workbuddy/binaries/node/versions/22.22.2/node.exe" scripts/verify_game.js
```

The script resolves the game at `../assets/index.html`, so run it from `scripts/`.

## Known bug classes / invariants to protect

- Movement reads **top-level** `u.speed` / `u.slowTimer` (set by `spawnUnit`),
  not `u.def.speed`. Any hand-built unit must include these or it goes NaN.
- `applySeparation` push must stay capped (e.g. `Math.min((rr-d)*0.5, 0.35)`),
  far below per-frame movement, so it softens stacks without deadlocking.
- `updateCombatUnit` must always make progress: on `findPath` failure use a
  repath cooldown + `seekDirect` fallback instead of `order='stop'` with no recovery.
- Victory is decided in `damage()` when a `yard` is destroyed.
- Sidebar must rebuild only on tab change; selection/command must survive frames.

## Debugging a failing gate

- If a unit is frozen: sample `(x,y)` per frame; if pathing + separation cancel,
  the separation cap is the suspect.
- If build/select fails on one viewport but not another: it's a coordinate/scale
  mapping bug in `fitGame` / `clientToGame` (test both viewports).
- NaN in `tileBlocked`: a unit is missing `u.speed` or got a waypoint with NaN
  coords (bad `findPath` target). Check unit creation paths all go through
  `spawnUnit`.
