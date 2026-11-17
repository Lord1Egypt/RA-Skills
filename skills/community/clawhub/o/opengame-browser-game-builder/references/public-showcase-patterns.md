# Public browser-game patterns

Use these patterns as design guidance, not as templates to copy. Keep each new
game's characters, setting, assets, and story original.

## 2D neon platformer

Good for a quick, readable first build:

- Side-view camera, left/right movement, jump, and one context-appropriate
  ability such as dash or short-range attack.
- A short route with three lesson beats: safe movement, a simple threat, then a
  combined challenge.
- Parallax background layers and a limited palette create depth without many
  assets.
- A checkpoint or fast restart makes failure useful rather than frustrating.

Use Canvas or an existing 2D framework. Show momentum, landing, damage, and
goal feedback clearly before adding enemy variants or a multi-level campaign.

## Lightweight 3D cinematic

Good when exploration, atmosphere, or spatial framing is the product:

- One recognizable environment with a readable path or observation objective.
- A small set of repeated scene objects using instancing or pooling.
- Camera controls that make the focal landmark easy to see.
- Time-of-day, fog, traffic, particles, or ambience as one adjustable mood
  system rather than many unrelated effects.

Use Three.js or the project's existing 3D runtime. Establish navigation,
performance, and a player objective before adding dense scenery or post effects.

## Scope test

Keep a feature in the first vertical slice only when it directly changes one
of these:

1. What the player repeatedly does.
2. How the player succeeds or fails.
3. What makes the game visually legible or emotionally distinct.

Defer anything else until the base loop is playable.
