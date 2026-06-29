---
name: pixellab-ai
description: PixelLab AI asset workflow and API helper for generating pixel-art images, conversions, rotations, animations, layered sprites, modular outfits/equipment, tilesets, UI assets, prompt enhancement, and consistent game-art packs. Requires the user's own PixelLab API key in PIXELLAB_API_KEY for live generation. Use when users ask Codex or OpenClaw to plan recipe-based PixelLab asset packs, prepare dry-run manifests, run PixelLab endpoints, poll jobs, download assets, build galleries, or validate game-ready sprite layers.
license: MIT-0
permissions:
  env:
    - PIXELLAB_API_KEY
    - PIXELLAB_API_BASE
    - PIXELLAB_TIMEOUT_SEC
    - PIXELLAB_POLL_INTERVAL_SEC
    - PIXELLAB_MAX_POLLS
    - PIXELLAB_MAX_DOWNLOAD_BYTES
  network:
    - https://api.pixellab.ai
  filesystem:
    read:
      - explicit manifest and payload paths under the selected PixelLab output folder
      - optional explicit --env-file path when the user provides one
    write:
      - selected PixelLab output folder for manifests, results, logs, downloads, galleries, and approvals
  commands:
    - python3
metadata:
  requires_api_key: true
  api_key_env: PIXELLAB_API_KEY
  account_url: https://www.pixellab.ai/
  api_token_url: https://api.pixellab.ai/mcp
  openclaw_skill_key: pixellab-ai
  openclaw_primary_env: PIXELLAB_API_KEY
  openclaw_requires_api_key: true
  openclaw_required_bin: python3
---

# PixelLab AI

## Easy Install

Copy-paste this to any coding agent or IDE that supports local skills:

```text
Install the ClawHub skill `pixellab-ai`, then set `PIXELLAB_API_KEY` in the local shell or host secret manager; use the skill to turn my rough asset idea into a visual brief before live PixelLab generation.
```

Command-line install from a skills directory:

```bash
npx --yes clawhub install pixellab-ai --force
export PIXELLAB_API_KEY='PASTE_YOUR_KEY_HERE'
```

If your agent does not use ClawHub, copy or install the `pixellab-ai/` folder into that agent's skills directory. The only runtime secret it needs is `PIXELLAB_API_KEY`.

PixelLab account: `https://www.pixellab.ai/`
PixelLab token page: `https://api.pixellab.ai/mcp`

Use PixelLab as an asset workflow system, not just a prompt endpoint. Route each request to the right endpoint family, prepare a JSON payload, run the helper when the user has configured `PIXELLAB_API_KEY`, and report the endpoint, result file, and downloaded assets.

Core rule: do not make users learn the PixelLab docs before getting usable game assets. Choose the endpoint, prepare payloads, preflight cost, submit/poll safely, save candidates, build contact sheets, promote approved files, and validate outputs.

Invocation rule: use this skill only when the user explicitly asks for PixelLab, `pixellab-ai`, PixelLab API/MCP setup, or PixelLab-style asset workflow help. Do not invoke it for generic image, art, or game-asset requests unless PixelLab is named or clearly intended.

## Secret Boundary

- Requires API key: yes. Live PixelLab generation needs the user's own PixelLab account token. Users can start at `https://www.pixellab.ai/` and get a PixelLab MCP/API token at `https://api.pixellab.ai/mcp`.
- It is safe and required to name the local env var `PIXELLAB_API_KEY`; never reveal, print, commit, package, or upload the key value stored in it.
- Do not ask the user to paste the key into chat. Prefer a local env var or OpenClaw `skills.entries.pixellab-ai.apiKey` secret config.
- The helper reads `PIXELLAB_API_KEY` from the process environment. It does not auto-discover local secret files; pass `--env-file PATH` only when the user provides an explicit local file.
- `PIXELLAB_API_BASE` defaults to `https://api.pixellab.ai`; custom HTTPS bases require the explicit `--allow-custom-base` flag and should be trusted test endpoints only.
- If the key is missing, stop after preparing payloads and setup instructions. Do not fake generated assets.
- ClawHub uploads should contain this skill package only. Each installer must provide their own PixelLab key locally.

## Security Scan Notes

ClawHub and SkillSpector may report environment-variable and network-flow findings for this package. Those findings describe the disclosed PixelLab API path:

- The helper reads `PIXELLAB_API_KEY` from the local process environment because PixelLab live generation requires user-owned API authentication.
- The key is used only as a bearer token for PixelLab API requests to `https://api.pixellab.ai`; it must not be printed, committed, uploaded, or copied into chat.
- PixelLab API requests can send prompts, payload JSON, and optional user-provided reference images to PixelLab.
- Asset download requests fetch URLs returned by PixelLab into the selected output folder and do not include `PIXELLAB_API_KEY`.
- `run --yes` can spend PixelLab credits, so review manifests, payloads, and budget output before live runs.

Treat those scan notes as required disclosure for a legitimate authenticated API helper, not permission to broaden network, file, or secret access.

## Beginner-Safe Workflow

1. Classify the task: create from scratch, transform an image, build a consistent asset family, rotate views, animate, build maps/tiles/UI, or enhance a weak prompt.
2. Load only the reference files and helper commands needed for that task type. Do not load the whole PixelLab reference corpus or run every helper command for every job.
3. For consistency-sensitive jobs, write a plain-English visual brief from the user's rough words before spending credits. Do not make the user know PixelLab prompt structure.
4. Decide the seed/reference plan: use caller-provided seed images, generate a small seed set for review, or proceed text-only with drift risk stated.
5. For multi-asset requests, create a manifest with `scripts/pixellab_workflow.py plan`; do not hand-run dozens of ad hoc calls.
6. Run `lint-manifest`, `repair-placeholders`, `budget`, and `balance-preflight` before spending credits.
7. Use a worker subagent or separate child context for live API calls. Give it the manifest, the relevant reference files only, and the exact commands it needs; main session output must be paths, costs, selected indexes, and short errors only.
8. Run the manifest only with explicit generation intent: `run --manifest ... --yes --continue-on-error`.
9. Review `candidates/` with `contact-sheet` or `gallery`; use `approve-candidate` to copy the chosen file into `approved/`.
10. Run `inspect-assets` or `validate-sprites` before calling assets game-ready.
11. Return recipe/endpoint, manifest, payloads, compact results, candidates, approved files, cost summary, validation report, and errors.

Standard folders: `payloads/`, `results/`, `seed-candidates/`, `candidates/`, `approved/`, `downloads/`, `reports/`, `logs/events.jsonl`.

## Job Scope And Seed Gate

Before a live run, keep the agent and any worker subagent scoped to this job:

- Load only references that match the asset type: endpoint mapping for routing, prompt cheatsheet for prompting, sprite layering for modular animation, YouTube/community notes only when those workflow details are relevant.
- Run only needed helper commands. A one-off sprite may need one payload and one call; a bulk pack needs manifest, lint, budget, balance, run, review, cost, and validation.
- Do not send PNG/base64 contents through the main session. The worker should return file paths, compact JSON, candidate indexes, costs, and short errors.
- If the request depends on a consistent cast, world style, brand, UI kit, animation family, or tileset, ask whether the user wants to provide seed/reference images or wants the agent to generate a small seed set for review before bulk generation.
- Put generated seed review images in `seed-candidates/` with stable names from the manifest, such as `project_slug_seed_candidate_01.png`, plus a `project_slug_seed_candidates_contact_sheet.png` review sheet.
- If the user declines seed review or asks to proceed, run text-only but report that consistency may drift and require more retries.

## Plain-English Visual Brief Gate

For named characters, recurring enemies, mascots, game worlds, UI kits, tilesets, or anything that must stay consistent, do this before generating art:

1. Take the user's rough description and turn it into a short visual brief. The user can say messy things like "make a chunky old wizard and a tiny nervous robot dog companion"; the agent must translate that into usable PixelLab drawing commands.
2. Ask at most three identity-critical questions if the rough description is missing something that cannot be safely inferred. Examples: "human or animal?", "friendly or scary?", "side-view or top-down?". Do not interrogate the user about every color and accessory.
3. Fill ordinary gaps with explicit defaults that fit the game: body shape, palette, camera view, pose, outline weight, transparency, sprite size, and what not to include.
4. Save or report the brief before seed generation. The manifest writes the expected path in `seed_reference_gate.visual_brief_path`, usually `reports/project_slug_visual_brief.md`.
5. Generate 2-4 seed candidates only after the brief is clear, save them under `seed-candidates/`, make a contact sheet, and get an approved anchor before bulk generation.
6. If the seed is visually wrong, fix the visual brief and seed anchors before making more assets. Do not keep generating a whole pack from a bad identity anchor.

Use this structure for each important character or object:

```text
Name/role: short plain-English identity.
Game use: playable hero, companion, enemy, NPC, pickup, UI icon, tileset motif, etc.
Body: size, shape, age/creature type, proportions, readable silhouette.
Face/expression: eyes, mouth, emotion, personality.
Clothing/materials: outfit, shell/armor/fur/metal/cloth, key colors.
Pose/camera: side-view, low top-down, high top-down, facing direction, idle stance.
Accessories/signature features: one to three things that must be visible.
Palette/style: palette, outline, shading, detail level, target game era.
Do not include: things that would make the identity wrong.
Approval criteria: what must be true before this becomes the seed/reference.
```

Then convert it into labeled PixelLab prompt blocks:

```text
Body: compact side-view playable hero with a strong readable silhouette.
Face: kind tired eyes, simple confident expression, visible at 64x64.
Clothing: short blue coat, tan gloves, dark boots, small belt pouch.
Pose: idle platformer stance, knees slightly bent, facing right in profile.
Accessories: small brass lantern, no oversized weapon.
Palette: limited NES-style colors, crisp outline, transparent background.
```

## Optional MCP Strategy

PixelLab's MCP/Vibe Coding interface is separate from the REST API. Use it only when the current client already exposes PixelLab MCP tools or the user explicitly asks to configure MCP. Do not make a long-lived PixelLab MCP server mandatory for this skill, because some clients expose large tool/resource schemas in context.

- Default for bulk production: use this skill's manifest + REST helper scripts. They provide dry-run payloads, skip-existing reruns, timeout resume, contact sheets, candidate approval, cost rollups, and local file paths.
- Optional MCP path: when tools such as `create_character`, `animate_character`, `create_topdown_tileset`, `create_sidescroller_tileset`, `create_isometric_tile`, `create_map_object`, or `get_balance` are already available, call only the job-relevant tools from a worker subagent.
- MCP jobs are non-blocking: record returned IDs, poll with the matching `get_*` tool, download to project folders, and return only paths/IDs/costs/errors to the main session.
- Do not paste MCP docs, images, base64, or broad tool lists into the main session. If MCP docs are needed, have the worker read `https://api.pixellab.ai/mcp/docs` or the relevant `pixellab://docs/...` resource only for that job.
- If MCP is not configured, do not pretend it is available. Use REST helper commands when an API key is configured, or stop at payload/manifest preparation.

## Guided Recipes

Use recipes when the user asks for a pack, game, character family, UI set, tileset, enemy group, or anything with more than one output.

List bundled recipes:

```bash
python3 pixellab-ai/scripts/pixellab_workflow.py list-recipes
```

Create a dry-run manifest without spending credits:

```bash
python3 pixellab-ai/scripts/pixellab_workflow.py plan \
  --recipe nes-platformer-pack \
  --brief "cozy forest NES side scroller with a hero and magical companion" \
  --output-dir ./pixellab-output/forest-platformer \
  --project-slug forest-platformer \
  --seed 123
```

Preflight before live generation:

```bash
python3 pixellab-ai/scripts/pixellab_workflow.py lint-manifest \
  --manifest ./pixellab-output/forest-platformer/asset-manifest.json
python3 pixellab-ai/scripts/pixellab_workflow.py repair-placeholders \
  --manifest ./pixellab-output/forest-platformer/asset-manifest.json
python3 pixellab-ai/scripts/pixellab_workflow.py budget \
  --manifest ./pixellab-output/forest-platformer/asset-manifest.json
python3 pixellab-ai/scripts/pixellab_workflow.py balance-preflight \
  --output-dir ./pixellab-output/forest-platformer
```

Run only after payload review:

```bash
python3 pixellab-ai/scripts/pixellab_workflow.py run \
  --manifest ./pixellab-output/forest-platformer/asset-manifest.json \
  --yes --continue-on-error
```

`run` skips completed result files by default and resumes submitted/timeout jobs with saved job IDs. Use `--rerun-existing` only when the user intentionally wants a fresh paid generation.

Review and approve candidates:

```bash
python3 pixellab-ai/scripts/pixellab_workflow.py contact-sheet \
  --asset-root ./pixellab-output/forest-platformer/candidates/characters/hero/base
python3 pixellab-ai/scripts/pixellab_workflow.py approve-candidate \
  --manifest ./pixellab-output/forest-platformer/asset-manifest.json \
  --operation-id hero-idle \
  --index 1
```

`contact-sheet` writes visible candidate numbers onto the PNG and a sibling `contact-sheet-index.json` file mapping indexes to local files.

Validate layered sprite exports:

```bash
python3 pixellab-ai/scripts/pixellab_workflow.py validate-sprites \
  --root ./pixellab-output/forest-platformer/approved/characters/hero \
  --layers base,outfit,hair,weapon \
  --frame-glob 'walk_south_*.png' \
  --expected-size 64x64
```

Bundled recipes:

- `nes-platformer-pack`: playable hero, magical companion, ground tiles, parallax background, starter enemy, collectible, HUD.
- `modular-rpg-character`: neutral base character, animation payloads, outfit transfer, outfit-only layer cleanup, frame-grid contract.
- `sidescroller-tileset`: primary/cave platform tiles, props, far background.
- `ui-hud-pack`: HUD strip, inventory icons, menu panel, button states.
- `enemy-variant-pack`: walker, hopper, flyer, and shield enemy family.

## Helper Commands

Create a Pixflux image:

```bash
python3 pixellab-ai/scripts/pixellab_client.py post /v2/create-image-pixflux \
  --payload-file pixellab-ai/examples/create-image-pixflux.json \
  --quiet --asset-slug hero \
  --result-file ./pixellab-output/pixflux/result.json \
  --download-dir ./pixellab-output/pixflux
```

Create a tileset and poll if a background job is returned:

```bash
python3 pixellab-ai/scripts/pixellab_client.py post /v2/create-tileset \
  --payload-file pixellab-ai/examples/create-tileset.json \
  --poll --quiet --asset-slug ground-tileset \
  --result-file ./pixellab-output/tileset/result.json \
  --download-dir ./pixellab-output/tileset
```

Poll a known background job or resume a timed-out result:

```bash
python3 pixellab-ai/scripts/pixellab_client.py get /v2/background-jobs/JOB_ID \
  --poll --quiet \
  --result-file ./pixellab-output/job/result.json \
  --download-dir ./pixellab-output/job

python3 pixellab-ai/scripts/pixellab_client.py poll-result-file ./pixellab-output/job/result.json \
  --result-file ./pixellab-output/job/result.json \
  --download-dir ./pixellab-output/job
```

Remote account-management boundary: this skill is for asset generation, polling, downloading, review, approval, and validation. It does not provide account cleanup commands. Manage PixelLab account cleanup in the PixelLab UI or another explicitly scoped admin workflow.

## Routing Rules

- Simple one-off sprites: prefer `/v2/create-image-pixflux`, `/v2/create-image-pixen`, or `/v2/create-image-bitforge`. Do not default bulk sprite work to `/v2/generate-image-v2`.
- Pro/multi-candidate images: `/v2/generate-image-v2` and `/v2/generate-with-style-v2`; treat as candidate generation and require contact-sheet approval.
- Existing image cleanup or conversion: `/v2/image-to-pixelart`, `/v2/image-to-pixelart-pro`, `/v2/remove-background`, `/v2/resize`, `/v2/edit-image`, `/v2/edit-images-v2`, `/v2/inpaint`, or `/v2/inpaint-v3`.
- Directional views: `/v2/rotate` for one view or `/v2/generate-8-rotations-v3` for ordinary 8-direction packs; reserve `/v2/generate-8-rotations-v2` for Pro workflows.
- Animation: `/v2/animate-with-text-v3`, `/v2/animate-with-text-v2`, `/v2/animate-with-text`, `/v2/animate-with-skeleton`, `/v2/edit-animation-v2`, `/v2/interpolation-v2`, `/v2/transfer-outfit-v2`, `/v2/create-character-state`, `/v2/characters/animations`, `/v2/animate-character`, or `/v2/objects/{object_id}/animations`.
- Tiles: `/v2/create-tileset`, `/v2/create-tileset-sidescroller`, `/v2/create-tiles-pro`, or `/v2/create-isometric-tile`; do not generate tiles through generic image endpoints by default.
- UI: `/v2/generate-ui-v2`; do not generate UI panels/buttons through generic image endpoints by default.
- Map props/pickups/hazards: prefer `/v2/map-objects` or object workflows over generic image generation.
- Characters and objects: `/v2/create-character-v3`, `/v2/create-character-with-4-directions`, `/v2/create-character-with-8-directions`, `/v2/create-character-pro`, `/v2/create-character-state`, `/v2/create-1-direction-object`, `/v2/create-8-direction-object`, `/v2/characters`, `/v2/characters/{character_id}`, `/v2/objects`, `/v2/objects/{object_id}`, `/v2/objects/{object_id}/states`, `/v2/objects/{object_id}/select-frames`, or `/v2/objects/{object_id}/dismiss-review`.
- Account, jobs, and API metadata: `/v1/balance`, `/v2/balance`, `/v2/background-jobs/{job_id}`, `/v2/llms.txt`, or `refresh-api-metadata`.
- Prompt enhancement: `/v2/enhance-pixen-prompt`, `/v2/enhance-character-v3-prompt`, or `/v2/enhance-animation-v3-prompt`.

## Generation Rules

- Reuse a seed when the user wants near-variants; use `0` for random variation when the endpoint supports it.
- Prefer init/reference images for stronger control over color, pose, style, perspective, or family consistency.
- For packs, require style images/init images/palettes when the user cares about consistency; text-only batches drift.
- Expose endpoint fields for view, direction, outline, shading, detail, palette, and background handling when available.
- For maps, describe what should appear in the middle of the selected area.
- For weak direction control, combine view/direction parameters with prompt wording such as `in profile`, `facing right`, or `high top-down`.
- For character prompts, prefer labeled feature blocks such as `Body`, `Clothing`, `Expression`, `Pose`, `Accessories`, and `Aura` over one flat sentence.
- For character edits, inpaint only the trait that must change, prompt the full target sprite, and reuse the original as a low-strength init image.
- For animations, start with fewer frames when consistency matters more than length.
- For animation variants, reuse a finished animation as init frames and keep the seed consistent across frame batches.
- For layered animation sprites, establish the base motion and frame-grid contract before outfits/equipment; isolate outfit/equipment layers with edit-animation; keep frame count, order, canvas size, origin, and transparency identical across every layer.
- Never call output final until generated files exist, the selected candidate is in `approved/`, dimensions/transparency/nonblank checks pass, and any required game-engine import/atlas preview has been inspected.

## References

- `references/youtube-workflow-playbook.md`: distilled official YouTube workflow knowledge for assets, tiles, maps, UI, rotation, and animation.
- `references/community-discord-workflows.md`: distilled PixelLab Discord helpful-post recipes for prompts, init images, tilesets, canvas resizing, and animation reuse.
- `references/community-discord-tutorials.md`: PixelLab Discord `#tutorials` channel coverage, tutorial feed links, and channel-only workflow tips.
- `references/sprite-animation-layering.md`: game-ready sprite animation layering, modular outfits, frame-grid contracts, pivots, compositing, and cleanup workflows.
- `references/api-coverage-matrix.md`: current OpenAPI route coverage, helper method support, route status, and known finalization gaps.
- `references/official-youtube-index.md`: complete official channel inventory with topic tags and transcript status.
- `references/install-and-secrets.md`: Codex, OpenClaw, ClawHub, and API-key setup.
- `references/endpoint-mapping.md`: endpoint families, known limits, and error handling.
- `references/prompt-cheatsheet.md`: prompt patterns for characters, maps, tilesets, UI, and animation.
