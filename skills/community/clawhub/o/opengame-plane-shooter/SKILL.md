---
name: opengame-plane-shooter
description: Design original 2D browser plane-shooter prototypes with continuous movement, readable threat waves, a route-and-resource decision, clear terminal states, and fast retry. Use when creating or revising a mobile-portrait or desktop browser shooter; do not use for 3D/WebGL games, fixed-base defense games, or copying an existing game's assets or identity.
---

# OpenGame Plane Shooter

Build an original, small-scope arcade shooter whose main decision is positioning under pressure. Keep the result runnable in a browser and make its game state inspectable enough to test rather than relying on screenshots alone.

Project homepage: <https://opengame.app>

## Start with a bounded brief

Confirm all of the following before coding:

- The target: `mobile-portrait` or `desktop`.
- A fresh output directory and a single HTML entry point or an existing project to revise.
- A one-sentence player promise.
- One visible world resource that the player protects, restores, charges, or routes.

For a design-only request, return the player promise, controls, pressure object, threat types, and route/resource choice. Do not create files or claim testing.

Example:

```text
Use $opengame-plane-shooter to create a mobile portrait game called Signal Orchard Escort.
The player weaves through weather debris, collects charge, and spends it in damaged orchard lanes.
```

## Design the playable kernel

1. Give the player continuous two-axis movement by touch/pointer for mobile and keyboard/mouse for desktop.
2. Keep combat simple: auto-fire or one repeated action, so positioning remains the primary decision.
3. Add two readable threat jobs: light rhythm pressure and a slower priority hazard. Make their silhouettes and behavior distinct.
4. Make hits, pickups, danger, and recovery visible in the playfield through motion, damage, particles, color, or world-state changes.
5. Add a route-and-resource decision that changes the active run: take a risky pickup route, enter a timing field, choose which lane to repair, or spend charge where it matters.
6. Escalate density, cadence, speed, and threat mix in readable steps.
7. Provide designed `ready`, `playing`, `complete` or `gameover`, and `retry` states.

Invent the world object before naming enemies or pickups. Let it change the verbs and decisions, not only the title, palette, or HUD. Avoid a passive loop where auto-fire and counters rise without the player's movement changing risk or outcome.

## Respect the target

### Mobile portrait

- Fit a 390px-wide viewport without horizontal overflow.
- Keep touch targets at least 44 CSS pixels and keep critical objects clear of the thumb area.
- Support arrow keys and WASD as fallbacks.
- Keep the player, immediate threats, progress, and pressure readable without tiny labels.

### Desktop

- Use the browser space as a scene; do not present a fixed phone card in the center.
- State controls on the ready screen and support keyboard plus pointer input.
- Use wider space for approach distance, lanes, pickups, and route pressure.

## Preserve originality and safety

- Use only original, licensed, or procedurally generated visuals, audio, and code.
- Do not copy another game's names, characters, sprites, sounds, HUD layout, enemy formations, level data, tuning, or recognizable identity.
- Do not add analytics, ad SDKs, remote scripts, CDN assets, credentials, or hidden outbound links.
- Prefer vector, canvas, gradients, particles, and original assets over unverified third-party media.

## Make it testable

Expose a small debug surface when the project permits it:

```js
window.__opengameDebug = {
  snapshot: () => ({ state, score, health, progress, player: { x, y } }),
  act: (action) => { /* route through real game functions */ }
};
```

Support `start`, `guide`, `idle`, `badInput`, and `retry`, or clear equivalents. Debug actions must invoke the same gameplay state transitions as real input. Test that real input changes state, guided play meaningfully differs from idle play, a terminal state is reachable, retry resets the run, and no external requests occur.

## Finish with a concise handoff

Report the output path, target, player promise, controls, route/resource decision, test evidence, and any unresolved human review for feel, visual quality, accessibility, licensing, or IP. Never describe a prototype as release-ready merely because it runs.
