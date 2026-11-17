---
name: oo-pixellab
description: "PixelLab (pixellab.ai). Use this skill for ANY PixelLab request — reading, creating, updating, and deleting data. Whenever a task involves PixelLab, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "PixelLab"
  author: "OOMOL"
  version: "1.0.5"
  services: ["pixellab"]
  icon: "https://static.oomol.com/logo/third-party/pixellab.png"
---

# PixelLab

Operate **PixelLab** through your OOMOL-connected account. This skill calls the `pixellab` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected PixelLab. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pixellab" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pixellab" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `animate_with_skeleton` — Generate synchronous PixelLab animation frames from a reference character image and per-frame skeleton keypoints. [write]
- `animate_with_text_legacy` — Generate four animation frames synchronously with PixelLab's original text animation model. [write]
- `convert_to_pixel_art` — Convert a PNG or JPEG image to pixel art synchronously.
- `create_pixen_image` — Generate one pixel-art image synchronously with the PixelLab Pixen model. [write]
- `create_pixflux_image` — Generate one pixel-art image synchronously with the PixelLab Pixflux model. [write]
- `delete_character` — Delete a persisted PixelLab character and its associated animations. [destructive]
- `delete_object` — Delete one persisted PixelLab object. [destructive]
- `delete_ui_asset` — Delete one saved PixelLab UI asset. [destructive]
- `dismiss_object_review` — Discard all candidate frames for a one-direction object awaiting review. [destructive]
- `download_character_zip` — Export one persisted PixelLab character as a ZIP transit file.
- `enhance_animation_prompt` — Expand a motion description using the visible content of one or two animation frames. [write]
- `enhance_character_prompt` — Expand a short description into a model-ready PixelLab v3 character prompt. [write]
- `enhance_pixen_prompt` — Expand a short description into a model-ready PixelLab Pixen image prompt. [write]
- `estimate_skeleton` — Estimate PixelLab skeleton keypoints from a PNG or JPEG character image.
- `get_background_job` — Poll a PixelLab background animation job and store completed image frames in OOMOL file transit.
- `get_balance` — Retrieve the current PixelLab USD credit and subscription generation balances.
- `get_character` — Retrieve one persisted PixelLab character with rotations and animations.
- `get_object` — Retrieve one persisted PixelLab object with rotations, review frames, and animations.
- `get_ui_asset` — Retrieve one saved PixelLab UI asset and its generation status.
- `inpaint_image_legacy` — Inpaint a masked area synchronously with PixelLab's original image model. [write]
- `list_characters` — List persisted PixelLab characters with offset pagination.
- `list_objects` — List persisted PixelLab objects with offset pagination.
- `list_ui_assets` — List saved PixelLab UI assets with offset pagination.
- `remove_background` — Remove a pixel-art image background synchronously and return a transparent PNG. [destructive]
- `resize_image` — Resize pixel art synchronously while preserving its pixel-art appearance. [write]
- `rotate_image` — Rotate or tilt a pixel-art character or object synchronously. [write]
- `select_object_frames` — Keep selected candidate frames from a one-direction object review as individual objects. [write]
- `start_animate_object` — Submit one or more directional animation jobs for an existing PixelLab object. [write]
- `start_convert_to_pixel_art_pro` — Start Pro conversion of a PNG or JPEG image to automatically scaled pixel art. [write]
- `start_create_character_4_directions` — Start creation of a persisted PixelLab character with four directional rotations. [write]
- `start_create_character_8_directions` — Start creation of a persisted PixelLab character with eight directional rotations. [write]
- `start_create_character_animation` — Start one or more background jobs that add an animation to a persisted character. [write]
- `start_create_character_pro` — Start Pro creation of a persisted eight-direction PixelLab character. [write]
- `start_create_character_state` — Start creation of an edited state for an existing persisted character. [write]
- `start_create_character_v3` — Start v3 creation or rotation of a persisted eight-direction PixelLab character. [write]
- `start_create_object_1_direction` — Start creation of a persisted one-direction PixelLab object. [write]
- `start_create_object_8_directions` — Start creation of a persisted PixelLab object with eight directional rotations. [write]
- `start_create_object_state` — Start creation of an edited state for an existing PixelLab object. [write]
- `start_create_ui_asset` — Start creation of a saved PixelLab Pro UI panel asset. [write]
- `start_edit_animation` — Start a consistent Pro text-guided edit across animation frames. [write]
- `start_edit_image_legacy` — Start PixelLab's original text-guided image editing operation. [write]
- `start_edit_images` — Start a consistent Pro edit across one or more pixel-art images. [write]
- `start_generate_image` — Start Pro text-to-pixel-art generation with optional subject and style reference images. [write]
- `start_generate_rotations` — Start generation of eight directional rotations from one reference character frame. [write]
- `start_generate_rotations_pro` — Start Pro generation of eight directional rotations using a reference, style, or concept image. [write]
- `start_generate_ui` — Start Pro generation of a pixel-art game UI element. [write]
- `start_generate_with_style` — Start Pro pixel-art generation that matches one to four supplied style images. [write]
- `start_inpaint` — Start Pro mask-guided inpainting of a pixel-art image. [write]
- `start_interpolation` — Start Pro interpolation between two pixel-art keyframes. [write]
- `start_pixflux_background` — Start asynchronous Pixflux pixel-art image generation. [write]
- `start_portrait_character_conversion` — Start Pro conversion between a bust portrait and a full-body character sprite. [write]
- `start_text_animation` — Start an asynchronous PixelLab animation from a first frame and a text description of the character motion. [write]
- `start_text_animation_pro` — Start Pro text-guided animation from a reference character image. [write]
- `start_transfer_outfit` — Start Pro transfer of an outfit or appearance across animation frames. [write]
- `update_character_tags` — Replace the user-defined tags on a persisted PixelLab character. [write]
- `update_object_tags` — Replace the user-defined tags on a persisted PixelLab object. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change PixelLab state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — PixelLab is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/pixellab
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- PixelLab homepage: https://www.pixellab.ai/
- API documentation: https://api.pixellab.ai/v2/docs
