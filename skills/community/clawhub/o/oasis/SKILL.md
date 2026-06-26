---
name: oasis
description: Enables an agent to work inside Oasis 3D worlds — place catalog objects, craft procedural scenes with shaders and textures, paint ground tiles, move avatars, take screenshots, and drive Forge text-to-3D conjuration through the Oasis MCP tool surface.
version: 0.4.0
author: Levi
license: MIT
metadata:
  hermes:
    tags: [oasis, mcp, world-building, 3d, integrations, creative]
---

# Oasis

Oasis is a local-first 3D world that agents can inspect, modify, navigate, and build through a shared MCP tool surface. Humans run Oasis on their laptop; agents use these tools to co-create 3D scenes with them in real time.

This skill teaches you HOW TO USE those tools effectively once the user has already connected you to their Oasis. It does not cover installation — see the user's setup docs at https://parzival-moksha.github.io/oasis/docs/getting-started/quickstart/ if they need help connecting.

## When To Use

Use this skill when:
- the user wants you to inspect, place, remove, paint, light, move, or screenshot inside Oasis
- the user wants to craft a procedural scene (campfire, garden, cyberpunk alley, shrine, etc.)
- the user wants a 3D asset conjured via text-to-3D
- the user wants you to move your avatar or take visual verification shots

Do not use this skill for generic coding unless Oasis integration is part of the task.

## What You Can Do

The Oasis MCP tool surface supports:
- world state and world summary (`get_world_state`, `get_world_info`)
- object search and asset search (`search_assets`, `query_objects`)
- placing, modifying, and removing catalog objects (`place_object`, `modify_object`, `remove_object`)
- crafting procedural scenes (`craft_scene`, `get_craft_guide`, `get_craft_job`)
- sky, ground presets, tile paint, and lights (`set_sky`, `set_ground_preset`, `paint_ground_tiles`, `add_light`, `modify_light`)
- embodied agent avatars (`set_avatar`, `walk_avatar_to`, `play_avatar_animation`, `list_avatar_animations`)
- viewport and avatar screenshots (`screenshot_viewport`, `screenshot_avatar`, `avatarpic_merlin`, `avatarpic_user`)
- Forge conjuration workflows (`conjure_asset`, `process_conjured_asset`, `place_conjured_asset`, `list_conjured_assets`, `get_conjured_asset`, `delete_conjured_asset`)
- world management (`list_worlds`, `create_world`, `load_world`, `clear_world`)
- behavior hints (`set_behavior`)

The agent should usually:
1. call `get_world_state` or `get_world_info` to understand the current scene
2. call `query_objects` or `search_assets` as needed
3. make a world mutation
4. use screenshot tools when visual verification matters

## Self-Craft Is The Default

When the user asks you to build something procedural (a campfire, a shrine, a crystal cluster, a fountain), **you write the primitives yourself** and pass them as the `objects` array to `craft_scene`. Do not delegate to the sculptor unless explicitly asked.

```
craft_scene({
  name: "Arcane campfire",
  position: [0, 0, 0],
  objects: [
    { type: "cylinder", position: [0, 0.08, 0], scale: [0.55, 0.08, 0.55], color: "#3b2a1d", roughness: 0.92 },
    { type: "flame", position: [0, 0.3, 0], scale: [0.22, 0.35, 0.22], color: "#fff4dd", color2: "#ff7a00", color3: "#9b1d00" },
    { type: "particle_emitter", position: [0, 0.75, 0], scale: [0.45, 0.85, 0.45], color: "#ffb347", particleCount: 80, particleType: "ember" },
    { type: "crystal", position: [0.65, 0.32, 0.1], scale: [0.22, 0.6, 0.22], rotation: [0.14, 0.3, -0.08], color: "#4338ca", color2: "#8b5cf6", seed: 11 }
  ]
})
```

What you have access to (call `get_craft_guide` for the live spec):
- **Geometry**: `box`, `sphere`, `cylinder`, `cone`, `torus`, `plane`, `capsule`, `text`
- **Shaders**: `flame`, `flag`, `crystal`, `water`, `particle_emitter`, `glow_orb`, `aurora`
- **Animations**: `rotate`, `bob`, `pulse`, `swing`, `orbit` (with `type`, `speed`, `axis`, `amplitude`)
- **Textures**: 20 presets including `stone`, `cobblestone`, `marble`, `concrete`, `grass`, `sand`, `snow`, `metal`, `wood`, `kn-planks`, `kn-cobblestone`, `kn-roof`, `kn-wall`. Apply via `texturePresetId` + `textureRepeat`.
- **Material fields**: `metalness`, `roughness`, `opacity`, `emissive`, `emissiveIntensity`, `color2`, `color3`

Rules the craft runtime enforces:
- No ground planes, sky domes, or background walls — Oasis already provides the world.
- Use shader primitives aggressively for fire, cloth, crystal, water, glow, aurora.
- Many small overlapping primitives beat one oversized primitive.
- Non-zero rotation on at least some primitives.

### When to use sculptor fallback

`craft_scene({ prompt: "...", strategy: "sculptor" })` delegates scene generation to a separate coder subprocess on the Oasis host. It costs a real LLM call, takes several seconds, and streams primitives in as they arrive. Use it only if:
- The user explicitly asks you to delegate ("have the sculptor do it")
- The scene is so ambitious you'd rather have a dedicated coder agent sketch it first

Otherwise: self-craft. You are an LLM. You can write the JSON.

## Progressive Smoke Test

These are the five prompts a user typically sends to verify the connection. Each escalates what it proves working:

1. **Plain chat** — user says `hi`. You reply. Proves: chat layer works.
2. **World awareness** — user says `describe this world`. You call `get_world_state` and narrate sky/ground/object counts. Proves: MCP transport up.
3. **Asset search + placement** — user says `find a cyberpunk streetlamp and place one in front of me`. Expected: `search_assets` then `place_object`, the streetlamp appears.
4. **Self-craft** — user says `craft a small campfire with embers and a crystal cluster`. Expected: `craft_scene` with an `objects` array (not sculptor).
5. **Vision** — user says `take a screenshot and tell me what you see`. Expected: `screenshot_viewport` with `mode: "current"`.

If step 1 passes but step 2 fails, the user's Oasis MCP transport is unreachable from your side. Point them at the troubleshooting section of https://parzival-moksha.github.io/oasis/ .

If step 2-4 pass but step 5 fails, the Oasis browser tab is closed or the screenshot bridge is not mounted. Ask the user to open the Oasis in their browser.

## Screenshot Guidance

Screenshot tools depend on a live Oasis browser client — the user must have Oasis open in a browser tab for vision tools to work.

- When you take screenshots, prefer including `defaultAgentType="hermes"` so agent-view captures resolve cleanly.
- For the user's actual camera, use `screenshot_viewport` with `mode: "current"` or `views: [{ mode: "current" }]`.
- For a behind-the-avatar shot, use `screenshot_avatar` with `style: "third-person"` or `screenshot_viewport` with `mode: "third-person-follow"`.
- Prefer one `screenshot_viewport` call with a `views` array for multi-angle capture instead of many separate screenshot calls.
- Do not fall back to generic `browser_*` tools for Oasis world vision; those browsers run remotely and may point at the wrong world.

## Visual Truth

Oasis has three different truths you should keep straight:

- **World state**: persisted build data and live player context returned by `get_world_state` / `get_world_info`
- **Avatar embodiment**: agent avatars, movement targets, and avatar screenshots
- **Browser vision**: what the screenshot bridge can currently capture from the live client

Important:
- screenshot tools require a live Oasis browser client
- live player avatar and camera context are refreshed per turn, not continuously every frame
- a screenshot is stronger than verbal assumption when the user is asking about what is visible right now

## Forge And Conjuration

Oasis exposes Forge conjuration for generating new 3D assets from text when the catalog lacks what you need:
- `list_conjured_assets` — what's already been generated
- `get_conjured_asset` — inspect a specific asset's status
- `conjure_asset` — start a Meshy or Tripo generation
- `process_conjured_asset` — texture, remesh, rig, or animate an existing asset
- `place_conjured_asset` — place a conjured asset in the world
- `delete_conjured_asset` — remove from world and optionally from the Forge registry

Use them like this:
- `conjure_asset` to start generation
- `process_conjured_asset` for texture, remesh, rig, or animate
- `place_conjured_asset` to place or reposition an existing conjured asset

If the user wants a new 3D asset rather than a catalog asset, prefer these tools over pretending the asset already exists. Do not claim a generation is finished until the conjured asset status actually says so.

## Operating Guidance

- Prefer concise world-aware answers inside Oasis UI surfaces.
- Distinguish between player view, agent view, and external view.
- Do not pretend you see the world if screenshot capture is unavailable.
- When the user asks to move relative to them, use live player context or avatar screenshot tools instead of guessing.
- When the user asks for precise visual verification, use screenshot tools rather than narration alone.
- When the user asks for catalog or asset-library content, prefer `search_assets` then `place_object`. Use `craft_scene` for procedural primitives, not catalog assets.
- After building a scene, consider taking a screenshot and describing what landed — the user often wants visual confirmation.

## Features That Need Keys On The Oasis Host

The core tool surface (world state, placement, self-crafting, screenshots, plain chat, avatar movement) works with **zero API keys**. If a richer feature is needed and the key isn't set, the tool call returns a clear error. Do not retry — tell the user what key is missing.

Optional Oasis-side feature keys (the user sets these in their own Oasis `.env`, agent never touches them):

- Image generation, textures, concepts, terrain LLM → `OPENROUTER_API_KEY`
- Video generation → `FAL_KEY`
- Voice notes / TTS in agent panels → `ELEVENLABS_API_KEY`
- Forge conjuration via Meshy → `MESHY_API_KEY`
- Forge conjuration via Tripo (fast) → `TRIPO_API_KEY`
- `craft_scene` sculptor fallback → Claude Code CLI installed on Oasis host

## Limits

- This skill does not install Oasis; users install locally and connect you via MCP.
- This skill does not configure the user's agent runtime — that lives in the user's setup docs.
- The plugin injects compact context, but real build power comes from the Oasis MCP tool surface.
- Screenshot tools depend on a live Oasis browser client in the target world.

## Verification

Once connected, verify the tool surface in this order:

1. `get_world_info`
2. `get_world_state`
3. `search_assets`
4. one safe placement or walk tool
5. one screenshot tool with the live browser open

If `get_world_info` works but screenshot tools fail, the MCP transport is up and the browser bridge is the missing link — ask the user to open / focus their Oasis browser tab.

## References

- Setup + onboarding docs: https://parzival-moksha.github.io/oasis/
- Repo: https://github.com/Parzival-Moksha/oasis
- Read `references/current-oasis-transport.md` for the current Oasis MCP transport shape.
