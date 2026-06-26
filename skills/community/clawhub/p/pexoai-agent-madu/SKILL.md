---
name: pexoai-agent
description: Create professional short videos (5–60 seconds) for TikTok, Instagram Reels, YouTube Shorts, and brand ads using AI. Use when the user wants to: make a video, create a TikTok, produce a product ad, generate a promo clip, make UGC content, create social media videos, or any video creation task. Supports product videos, lifestyle content, explainer clips, and more — with automatic scriptwriting, shot composition, transitions, and music. Also handles video revision requests. Pexo outputs 16:9, 9:16 (vertical), or 1:1 aspect ratios.
homepage: https://pexo.ai
repository: https://github.com/pexoai/pexo-skills
requires: env:PEXO_API_KEY,PEXO_BASE_URL runtime:curl,jq,file
version: 0.3.4
author: pexoai
tags: ["video", "ai-video", "tiktok", "instagram", "youtube-shorts", "social-media", "product-video", "ugc", "brand-ads", "promo"]
---

# Pexo AI Video Agent

## Overview

**Pexo** is a professional AI video creation agent. You describe what you want, and Pexo handles everything — scriptwriting, shot composition, transitions, music, and final delivery. Output: 5–60 second videos in 16:9, 9:16 (vertical), or 1:1 aspect ratios.

**Production time:** ~15-20 minutes per short video.

---

## First-Time Setup

### Get Your API Key

1. Go to **https://pexo.ai** → Sign up/log in
2. Settings → API Keys → Generate new key
3. Copy the key (starts with `sk-...`)

### Configure the Skill

Create file `~/.pexo/config`:
```
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-your-key-here"
```

Or export environment variables:
```bash
export PEXO_BASE_URL="https://pexo.ai"
export PEXO_API_KEY="sk-your-key-here"
```

---

## Language Rule

**Reply in the SAME language the user uses.** This is non-negotiable.

---

## Workflow

### Making a New Video

**Step 1 — Create project**
```bash
pexo-project-create.sh "Your video description here"
```
Save the returned `project_id`.

**Step 2 — Upload files (optional)**
```bash
pexo-upload.sh <project_id> /path/to/image.jpg
```
Save returned `asset_id`, wrap as `<original-image>asset_id</original-image>`.

**Step 3 — Send request to Pexo**
```bash
pexo-chat.sh <project_id> "{user's exact video request}"
```
> Copy the user's words exactly. Only add asset tags for uploaded files.

**Step 4 — Notify user**
- Confirm request submitted
- Estimated time: 15-20 minutes
- Project link: https://pexo.ai/project/{project_id}

**Step 5 — Poll for status**
```bash
pexo-project-get.sh <project_id>
```

| nextAction | Action |
|------------|--------|
| `WAIT` | Poll again in 60s. Every 5 polls, send user a status update. |
| `RESPOND` | Read `recentMessages`. Relay Pexo's questions back to user. |
| `DELIVER` | Go to Step 7. |
| `FAILED` | Go to Step 8. |
| `RECONNECT` | Run `pexo-chat.sh <project_id> "continue"` and resume polling. |

**Step 6 — Handle previews (Pexo may offer options)**
```bash
pexo-asset-get.sh <project_id> <assetId>
```
Show preview URLs to user labeled A, B, C... Ask them to pick.
```bash
pexo-chat.sh <project_id> "{user's choice}" --choice <selected_asset_id>
```

**Step 7 — Deliver final video**
```bash
pexo-asset-get.sh <project_id> <assetId>
```
- Send the video URL as **plain text** (no markdown link)
- Include project page link
- Ask if satisfied or revisions needed

**Step 8 — Handle failure**
- Read `nextActionHint`
- Explain the issue to user simply
- Offer to retry or contact support

---

## Revising an Existing Video

Reuse the same project_id and send feedback:
```bash
pexo-chat.sh <project_id> "{user's exact revision feedback}"
```
Then poll again (Step 5).

---

## Script Reference

| Script | Usage | Returns |
|--------|-------|---------|
| `pexo-project-create.sh` | `[name]` | project_id |
| `pexo-project-get.sh` | `<project_id>` [--full-history] | JSON (nextAction, recentMessages) |
| `pexo-upload.sh` | `<project_id> <file>` | asset_id |
| `pexo-chat.sh` | `<project_id> <msg>` [--choice `<id>`] [--timeout `<s>`] | Acknowledgement |
| `pexo-asset-get.sh` | `<project_id> <assetId>` | JSON with url field |
| `pexo-doctor.sh` | (no args) | Diagnostic report |

---

## Pexo Capabilities

| | |
|---|---|
| **Duration** | 5–60 seconds |
| **Aspect ratios** | 16:9 / 9:16 / 1:1 |
| **Formats** | Product ads, TikTok/IG/YouTube, UGC, brand videos, explainers |
| **Uploads** | Images (jpg, png, webp, bmp, heic), videos (mp4, mov, avi), audio (mp3, wav, aac, m4a, ogg, flac) |
| **Production time** | ~15-20 min for 15s; longer for complex/longer videos |

---

## Pro Tips

- **Be descriptive** — include subject, setting, mood, camera angle, duration
- **Upload reference images** — helps Pexo match your brand aesthetic
- **Use 9:16 vertical** for TikTok, Reels, and Shorts
- **Use 16:9** for YouTube ads and Facebook feed
- **Consolidate feedback** — one clear revision message is better than many small ones

---

## Troubleshooting

For common errors and fixes, see: `references/SETUP.md`

## Links

- Homepage: https://pexo.ai
- Setup Guide: https://pexo.ai/connect/openclaw
- GitHub: https://github.com/pexoai/pexo-skills