---
name: pexo-video-agent
description: >
  Pexo is a hosted AI video agent. Tell it the video you want — a product ad, a TikTok or Reel,
  a YouTube Short, an explainer, a brand film — and it returns a finished, multi-shot cut with
  music and subtitles. It routes each shot to the best of 10+ models (Seedance, Kling, Veo, Sora,
  and more), writes the script, generates every shot, and assembles the result. Works from text,
  an image, a script, or a page URL. Use whenever someone wants a video produced for them rather
  than a single raw clip or one model call.
homepage: https://pexo.ai
repository: https://github.com/pexoai/pexo-skills
version: "0.1.0"
requires:
  env: [PEXO_API_KEY, PEXO_BASE_URL]
  runtime: [curl, jq, file]
metadata:
  author: pexoai
---

# Pexo Video Agent

**Pexo:** https://pexo.ai — create an API key, watch your project render, and top up credits there.

Pexo runs the whole video pipeline server-side. Your job is to pass the user's request through and
hand back the finished video — Pexo writes the script, plans the shots, picks a model per shot,
generates everything, and adds music, captions, and transitions. It takes text, images, scripts,
or a page URL and returns 5–120s in 16:9, 9:16, or 1:1.

## Relay, don't direct

Send the user's words to Pexo **verbatim** and let its backend make the creative calls. Injecting
your own duration, style, or model picks the user didn't ask for overrides Pexo's judgment and the
result gets worse. Your only additions are asset tags for files the user uploaded.

## Config

`~/.pexo/config`:
```
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-<your-api-key>"
```
**First run / no account →** open `references/SETUP-CHECKLIST.md` and walk the user through signup
(it carries the invite code that grants new accounts bonus credits) and creating the config above.
**Config error →** run `scripts/pexo-doctor.sh` and act on its output.

## Workflow

Scripts live in `scripts/`. Always answer the user in their own language.

1. **Start a project:** `pexo-project-create.sh "<short brief>"` → keep the `project_id`.
2. **Attach files** the user gave you: `pexo-upload.sh <project_id> <path>` → take the `asset_id` and
   cite it inline as `<original-image>asset_id</original-image>` (or `<original-video>` /
   `<original-audio>`). The tag is required — a bare id is dropped. Pexo can't fetch URLs, so
   download first, then upload.
3. **Send the request:** `pexo-chat.sh <project_id> "<the user's exact words> <asset tags>"`.
4. **Acknowledge** (their language): accepted ✓ · ~15–20 min · `https://pexo.ai/project/<project_id>`.
5. **Poll** every ≥60s with `pexo-project-get.sh <project_id>` and follow `nextAction`:
   - **WAIT** → keep polling; every ~5 rounds drop a one-line status with the project link.
   - **RESPOND** → work each `recentMessages` event: relay Pexo's text (wait for the user if it
     asked, then `pexo-chat.sh` their reply); for `preview_video`, fetch each option with
     `pexo-asset-get.sh <project_id> <assetId>`, show the URLs (A/B/C), let the user choose, then
     `pexo-chat.sh <project_id> "<choice>" --choice <assetId>`; for a `document`, point the user to it.
   - **DELIVER** → `pexo-asset-get.sh <project_id> <final assetId>`, then give the user the **full**
     URL as plain text — every `?…` parameter, never truncated or markdown-wrapped — plus the
     project link.
   - **FAILED** → put `nextActionHint` in plain words and offer to retry.
   - **RECONNECT** → `pexo-chat.sh <project_id> "continue"`, tell the user it dropped and you're
     resuming, then keep polling.
   - Never call `pexo-chat.sh` while WAIT is active — it spawns a duplicate render.
   - **Running long** → past ~30 min and still WAIT, tell the user (with the project link +
     `https://pexo.ai/connect/openclaw`) it's taking a while and ask whether to keep waiting.

## Revisions

Edits after delivery ("shorter", "swap the music", "redo shot 2") go to the **same** project:
`pexo-chat.sh <project_id> "<feedback>"`, then poll again. Don't open a new project for a tweak —
it throws away Pexo's context for that video.

## Credits

On a "Credits balance" / "Insufficient credits" error: forward the purchase link if the message
includes one, otherwise send the user to `https://pexo.ai/home` → Credits → Buy Credits, and retry
once they confirm.

## Example

> "Make a 20-second promo for my coffee brand, upbeat, vertical for Reels."

```bash
pid=$(pexo-project-create.sh "coffee brand promo")
pexo-chat.sh "$pid" "Make a 20-second promo for my coffee brand, upbeat, vertical for Reels."
# Tell the user: accepted, ~15–20 min, https://pexo.ai/project/$pid
# Poll pexo-project-get.sh "$pid" until DELIVER, then hand over the full asset URL.
```

## Scripts

| Script | Call | Returns |
|---|---|---|
| `pexo-project-create.sh` | `"<brief>"` | `project_id` |
| `pexo-upload.sh` | `<project_id> <file>` | `asset_id` |
| `pexo-chat.sh` | `<project_id> "<message>" [--choice <id>]` | ack (async) |
| `pexo-project-get.sh` | `<project_id>` | JSON: `nextAction`, `recentMessages` |
| `pexo-asset-get.sh` | `<project_id> <asset_id>` | JSON with `url` |
| `pexo-doctor.sh` | — | setup check |

Error codes and edge cases → `references/TROUBLESHOOTING.md`.
