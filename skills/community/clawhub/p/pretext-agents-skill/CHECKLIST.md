# CHECKLIST.md — Build Acceptance Checklist

## Core

- [ ] Uses Pretext for actual text measurement/layout, not just by name
- [ ] Uses Three.js only where spatial rendering matters
- [ ] Has one clear signature interaction
- [ ] Has one calm readable state
- [ ] Has one active/high-energy state
- [ ] Picks at least one clear ecosystem pattern: Textura / Pinch-Type / Breaker / Dokobot / Editorial / Variable ASCII

## Hero

- [ ] Hero is visually dominant
- [ ] Hero interaction starts quickly
- [ ] Hero is readable before interaction
- [ ] Hero can recover after disruption

## Motion

- [ ] Motion explains hierarchy or force
- [ ] Pointer response is smooth
- [ ] No constant jittery micro-motion everywhere
- [ ] Destruction has recovery/reset logic

## Text system

- [ ] Text home positions are preserved
- [ ] Re-layout occurs only when needed
- [ ] Decorative text does not duplicate key copy excessively
- [ ] Ambient rails / HUD / ASCII remain secondary
- [ ] Mobile text scaling is intentional if large hero type is used

## Performance

- [ ] No one-mesh-per-glyph disaster when batching is possible
- [ ] Particles are pooled or bounded
- [ ] Hidden/offscreen work is minimized
- [ ] Mobile density is reduced
- [ ] Reduced-motion path exists
- [ ] Canvas is used for hot collision loops when that is simpler than WebGL

## UX

- [ ] There is at least one stable interaction-free zone
- [ ] Important content remains readable/selectable when needed
- [ ] Effects do not block basic navigation
- [ ] The prototype can be screen-recorded cleanly

## Code quality

- [ ] Scene logic is separated from content data
- [ ] Tuning values are centralized
- [ ] No dead debug code left behind
- [ ] File layout is understandable to another agent
- [ ] The chosen ecosystem pattern is visible in the architecture

## Common failure checks

- [ ] Not just “particles on a black background”
- [ ] Not just “DOM page with random shader blob”
- [ ] Not just “cool hero, dead rest of page”
- [ ] Not just “everything moves, nothing matters”
- [ ] Not just “five borrowed demos smashed together”
