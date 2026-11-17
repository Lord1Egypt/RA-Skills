---
name: oo-magichour
description: "Magic Hour (magichour.ai). Use this skill for ANY Magic Hour request — reading, creating, updating, and deleting data. Whenever a task involves Magic Hour, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Magic Hour"
  author: "OOMOL"
  version: "1.0.2"
  services: ["magichour"]
  icon: "https://static.oomol.com/logo/third-party/magichour.svg"
---

# Magic Hour

Operate **Magic Hour** through your OOMOL-connected account. This skill calls the `magichour` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Magic Hour. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "magichour" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "magichour" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_ai_clothes_changer` — AI Clothes Changer. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_face_editor` — AI Face Editor. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_gif_generator` — AI GIF Generator. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_headshot_generator` — AI Headshot Generator. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_image_editor` — AI Image Editor. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_image_generator` — AI Image Generator. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_image_upscaler` — AI Image Upscaler. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_meme_generator` — AI Meme Generator. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_music_generator` — AI Music Generator. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_qr_code_generator` — AI QR Code Generator. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_talking_photo` — AI Talking Photo. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_ugc_ad` — AI UGC Ad Generator. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_video_editor` — AI Video Editor. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_video_translator` — AI Video Translator. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_video_upscaler` — AI Video Upscaler. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_voice_cloner` — AI Voice Cloner. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_ai_voice_generator` — AI Voice Generator. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_animation` — Animation. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_audio_to_video` — Audio-to-Video. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_auto_subtitle_generator` — Auto Subtitle Generator. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_body_swap` — Body Swap. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_character_replace` — Character Replace. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_face_detection` — Face Detection. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_face_swap` — Face Swap Video. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_face_swap_photo` — Face Swap Photo. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_head_swap` — Head Swap. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_image_background_remover` — Image Background Remover. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_image_to_video` — Image-to-Video. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_lip_sync` — Lip Sync. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_photo_colorizer` — Photo Colorizer. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_text_to_video` — Text-to-Video. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `create_video_to_video` — Video-to-Video. Submit the asynchronous task and use the linked result action to retrieve completion and downloads. [write]
- `delete_audio_projects` — Delete audio. [destructive]
- `delete_image_projects` — Delete image. [destructive]
- `delete_video_projects` — Delete video. [destructive]
- `get_account` — Get account details.
- `get_audio_projects` — Get audio details.
- `get_face_detection` — Get face detection details.
- `get_image_projects` — Get image details.
- `get_video_projects` — Get video details.
- `list_saved_items` — List saved items.
- `upload_asset` — Upload an asset from a public URL to Magic Hour storage and return its reusable file_path. Maximum 20 MiB; larger hosted files can be passed directly to generation actions. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Magic Hour state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Magic Hour is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/magichour
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Magic Hour homepage: https://magichour.ai
- API documentation: https://docs.magichour.ai/
