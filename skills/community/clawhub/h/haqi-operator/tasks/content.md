# Task: Content production (BYOC)

Goal: steadily grow MagicHaqi's content (mini-games, famous pets, themed planets,
storybooks) using your own generative compute — the app provides prompts, schemas and
sandboxes; you provide the generation.

## Generators (open in the browser, operate like a person)
| Artifact        | Tool                                   | Output folder      |
|-----------------|----------------------------------------|--------------------|
| Mini-game       | `dev_tools/GameGenerator.html` or in-app Game Maker | `minigames/` |
| Famous pet      | `dev_tools/FamousPetGenerator.html`    | `famous-pets/`     |
| Themed planet   | `dev_tools/FamousPlanetGenerator.html` | `famous-planets/`  |
| Pet storybook   | `dev_tools/PetStoryGenerator.html` or in-app Story Maker | `pet-story/` |
| Art assets      | `dev_tools/ArtAssetGenerator.html`     | (referenced by the above) |
| Shop item       | `dev_tools/ShopItemGenerator.html`     | `famous-planets/*_shopitems.json` |

## Steps (one artifact per run)
1. Pick the lagging artifact type from `agent/ops-state.json`.
2. Open the matching generator page. Read its on-page schema / config sections.
3. Generate ONE artifact with your compute, honoring the schema and constraints.
4. Verify it (mini-games must run in the sandbox; JSON must match the index schema).
5. Save it to its homogeneous folder and update the relevant `_*_index.json`.
6. Increment the counter in `agent/ops-state.json`.

## Compliance
- External IP (characters, brands) must be explicitly `authorized=true`, else skip.
- Prefer original / Haqi-native content for safe viral spread.
