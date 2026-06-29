# API Coverage Matrix

Last refreshed: 2026-06-21 from public PixelLab API metadata.

This matrix covers route selection and package examples. It is not a claim that every route has been live-run with credits in this package. Use the helper with `/v1` or `/v2` prefixed paths, for example `/v2/create-image-pixflux`.

Refresh public API metadata into a run folder:

```bash
python3 pixellab-ai/scripts/pixellab_workflow.py refresh-api-metadata --output-dir ./pixellab-output/api-refresh
```

As of the current public metadata check, v1 exposes 8 legacy paths and v2 exposes 63 paths. Prefer v2 for new work; use v1 only for legacy routes or explicit user requests.

## Status Legend

- `example`: this package includes a JSON payload example or an equivalent reusable example.
- `routed`: `SKILL.md` or `endpoint-mapping.md` routes to the endpoint, but no dedicated payload file is bundled.
- `management`: list/get/export/tag/status endpoint; call with `get` or `patch` and the relevant account-owned id.
- `metadata`: documentation or account metadata endpoint.

## Core Account, Jobs, And Metadata

| Path | Methods | Status | Use |
|---|---:|---|---|
| `/balance` | GET | metadata | Check account balance/credit status before expensive runs. |
| `/background-jobs/{job_id}` | GET | management | Poll async generation jobs; the helper supports `--poll`. |
| `/llms.txt` | GET | metadata | Fetch PixelLab's agent-readable API context when current docs are needed. |

## Image Creation, Conversion, And Editing

| Path | Methods | Status | Use |
|---|---:|---|---|
| `/create-image-pixflux` | POST | example | General pixel-art text-to-image. |
| `/create-image-pixflux-background` | POST | example | Background-specific Pixflux generation. |
| `/create-image-pixen` | POST | example | General larger pixel-art image generation. |
| `/create-image-bitforge` | POST | example | Reference/init/palette-friendly generation. |
| `/generate-image-v2` | POST | example | Modern async generation with reference/style inputs. |
| `/generate-with-style-v2` | POST | example | Consistent pack generation from style reference images. |
| `/image-to-pixelart` | POST | example | Convert source art into pixel art at a target size. |
| `/image-to-pixelart-pro` | POST | example | Pro conversion flow for a source image and optional description. |
| `/edit-image` | POST | example | Single-image text edit with output dimensions. |
| `/edit-images-v2` | POST | example | Multi-image edit or reference-guided edit. |
| `/remove-background` | POST | example | Transparent PNG/background removal. |
| `/resize` | POST | example | Pixel-art-aware resizing from reference image. |
| `/inpaint` | POST | example | Synchronous masked replacement on a source image. |
| `/inpaint-v3` | POST | example | Async masked replacement with structured image+size objects. |

## Characters, Objects, Rotations, And Management

| Path | Methods | Status | Use |
|---|---:|---|---|
| `/create-character-v3` | POST | example | Modern character creation; returns character id and job id. |
| `/create-character-pro` | POST | routed | Pro character creation when advanced controls are needed. |
| `/create-character-with-4-directions` | POST | routed | Four-direction character pack. |
| `/create-character-with-8-directions` | POST | routed | Eight-direction character pack. |
| `/create-character-state` | POST | example | Re-pose or state-edit an existing character. |
| `/animate-character` | POST | example | Character animation by id; equivalent family to `/characters/animations`. |
| `/characters/animations` | POST | example | Collection route for character animation by id. |
| `/characters` | GET | management | List account characters with `limit` and `offset`. |
| `/characters/{character_id}` | GET | management | Fetch an account-owned character with this helper. Account cleanup is intentionally outside this skill's supported workflow. |
| `/characters/{character_id}/tags` | PATCH | management | Update character tags with a `tags` array. |
| `/characters/{character_id}/zip` | GET | management | Download/export a character ZIP when available; use a binary-capable downloader with the configured PixelLab API key because the JSON helper does not save binary ZIP responses. |
| `/create-1-direction-object` | POST | routed | One-direction object creation. |
| `/create-8-direction-object` | POST | routed | Eight-direction object creation. |
| `/objects` | GET | management | List account objects. |
| `/objects/{object_id}` | GET | management | Fetch an account-owned object with this helper. Account cleanup is intentionally outside this skill's supported workflow. |
| `/objects/{object_id}/states` | POST | example | Create a new state for an existing object. |
| `/objects/{object_id}/animations` | POST | example | Animate an existing object. |
| `/objects/{object_id}/select-frames` | POST | example | Split selected object frames into new objects. |
| `/objects/{object_id}/tags` | PATCH | example | Update object tags with a `tags` array. |
| `/objects/{object_id}/dismiss-review` | POST | management | Dismiss review state on an owned object. |
| `/rotate` | POST | example | Rotate a single source image to another facing direction. |
| `/generate-8-rotations-v2` | POST | example | Pro 8-direction rotation workflow. |
| `/generate-8-rotations-v3` | POST | example | Modern 8-direction pack from a first frame. |
| `/estimate-skeleton` | POST | example | Estimate animation skeleton keypoints from an image. |

## Animation And Layered Sprites

| Path | Methods | Status | Use |
|---|---:|---|---|
| `/animate-with-text-v3` | POST | example | Modern text animation from first frame and action. |
| `/animate-with-text-v2` | POST | example | Async text animation with reference image size, view, and direction. |
| `/animate-with-text` | POST | example | Legacy text animation route with description and frame controls. |
| `/animate-with-skeleton` | POST | example | Motion control from skeleton keypoints and reference image. |
| `/edit-animation-v2` | POST | example | Edit frame sequences; useful for removing/adding layers. |
| `/interpolation-v2` | POST | example | In-between animation from start/end key frames. |
| `/transfer-outfit-v2` | POST | example | Apply outfit or equipment reference across animation frames. |

## Prompt Enhancement

| Path | Methods | Status | Use |
|---|---:|---|---|
| `/enhance-pixen-prompt` | POST | example | Expand a weak general image prompt before spending generation credits. |
| `/enhance-character-v3-prompt` | POST | routed | Expand a character prompt before v3 character creation. |
| `/enhance-animation-v3-prompt` | POST | routed | Expand an animation action prompt before v3 animation. |

## Tiles, Maps, Isometric Assets, And UI

| Path | Methods | Status | Use |
|---|---:|---|---|
| `/create-tileset` | POST | example | Top-down lower/upper tileset generation. |
| `/tilesets` | GET, POST | routed | Collection route for tilesets; use create example shape for POST. |
| `/tilesets-sidescroller` | POST | routed | Collection route for sidescroller tilesets. |
| `/tilesets/{tileset_id}` | GET | management | Fetch account-owned tileset details/assets. |
| `/create-tileset-sidescroller` | POST | example | Sidescroller lower/upper tileset generation. |
| `/create-tiles-pro` | POST | example | Pro square/hex/isometric/octagon tile generation. |
| `/tiles-pro/{tile_id}` | GET | management | Fetch a Pro tile by id after async completion. |
| `/create-isometric-tile` | POST | example | Isometric tile generation. |
| `/isometric-tiles` | GET | management | List account isometric tiles. |
| `/isometric-tiles/{tile_id}` | GET | management | Fetch account-owned isometric tile details/assets. |
| `/map-objects` | POST | routed | Generate map objects from description. |
| `/generate-ui-v2` | POST | example | Pixel UI panel, icon, and HUD generation. |

## Known Finalization Gaps

- Live-run coverage is intentionally limited by account credits; validate payload shape before spending credits and report PixelLab error bodies exactly.
- Binary ZIP/export routes need a binary downloader, not the JSON helper. The skill currently documents that boundary instead of pretending ZIP exports are ordinary JSON assets.
- The YouTube corpus has complete channel inventory, but not every item has a durable full-text transcript markdown file. The distilled workflow references are included; the raw reproducibility audit lives outside the uploadable skill package.
- Visual-only tutorial moments still need screenshots when a transcript says "this setting" or "like this" without naming the control.
