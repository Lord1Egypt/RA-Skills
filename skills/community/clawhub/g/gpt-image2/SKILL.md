---
name: gpt-image2
description: "Generate high-quality images with GPT Image 2 (OpenAI gpt-image-2) via the ClawdChat tool gateway. Use when the user asks to create / generate / draw / paint an image, mentions GPT image, gpt-image-2, OpenAI image generation, or needs accurate text rendering (posters, infographics, menu typography), strict multi-element prompt following, image-to-image with subject/identity preservation, or specific styles such as Ghibli / Pixar / LEGO / cyberpunk / claymation / Pop Mart figurine."
homepage: https://clawdchat.cn
metadata:
  emoji: "🖼️"
  category: creative
  version: "0.1.0"
  language: en
  publisher: clawdchat
  requires:
    primary_credential:
      type: clawdchat_api_key
      managed_by: uno-cli skill
      stored_at: ~/.clawdchat/credentials.json
      obtained_via: interactive `uno login` command (delegates to ClawdChat OAuth, see https://clawdchat.cn)
      scope: "Used as Authorization Bearer token to call the ClawdChat tool gateway. The credential is acquired and stored by the uno-cli skill; this skill only reuses it via the `uno` CLI and never reads, prints, or transmits the file directly."
    config_paths:
      - ~/.clawdchat/credentials.json (read-only, owned by uno-cli)
    network_endpoints:
      - "ClawdChat tool gateway (HTTPS, via uno-cli) — receives the prompt and reference-image URLs"
    write_actions:
      - "Submits paid image-generation jobs (300 credits per submit). Each call deducts ClawdChat credits from the logged-in account."
      - "Writes no local files. Generated image URLs are returned in the response; the agent decides whether to download them."
    cost:
      gpt_image2_submit: "300 credits per call"
      gpt_image2_result: "0 credits per call"
  openclaw:
    requires:
      bins: ["uno"]
    skills: ["uno-cli"]
---

# GPT Image 2 — High-quality AI image generation

> Powered by ClawdChat — calls OpenAI `gpt-image-2` through the Uno tool gateway.

## What this skill does

Two thin command-line invocations against the public ClawdChat tool gateway:

| Tool slug | Purpose | Cost |
|---|---|---|
| `gpt-image-2.gpt_image2_submit` | Submit a generation job, returns `job_id` immediately (async) | **300 credits / call** |
| `gpt-image-2.gpt_image2_result` | Poll job status / fetch image URL when ready | 0 credits |

This skill ships **no local Python code**. It defers all credential, transport and rate-limit handling to the `uno-cli` companion skill.

## Credentials & permissions (please read before first use)

- **Credential type**: ClawdChat API key (Bearer token).
- **Where it lives**: `~/.clawdchat/credentials.json`. The file is **created and owned by the `uno-cli` skill**; this skill never opens, prints or copies it.
- **How it was obtained**: the user runs `uno login` in `uno-cli`, which opens an OAuth flow on https://clawdchat.cn and stores the resulting token.
- **What it authorises**: calling the ClawdChat tool gateway as the logged-in user. Each `gpt_image2_submit` deducts 300 credits from that account.
- **Network egress**: the user's `prompt` text and any `reference_image_urls` are sent to the ClawdChat gateway over HTTPS. **Do not paste private, confidential, or personally-identifying content into the prompt unless you are comfortable with the gateway's data handling — see https://clawdchat.cn for the data policy.**
- **Logging out / revoking**: run `uno logout` (managed by `uno-cli`).

## Cost transparency & confirmation rule

Every `gpt_image2_submit` call costs the logged-in account real credits. The agent **must**:

1. Show the user the planned prompt, size, style, and number of images **before** the first call.
2. Ask for explicit confirmation when the user has not already approved a generation in the current turn.
3. For multi-image batches (`n > 1`) or retries, treat each submission as a separate spending event and confirm again unless the user has pre-authorised the batch.
4. On `error` responses, surface the error to the user instead of silently retrying.

Polling via `gpt_image2_result` is free; only `submit` spends credits.

## Setup

This skill depends on the `uno-cli` skill (declared in `metadata.openclaw.skills`).

1. Install `uno-cli` (skipping if already installed):

   ```bash
   clawhub install uno-cli
   ```

   On platforms that honour `metadata.openclaw.skills`, this dependency is installed automatically when this skill is installed.

2. Log in once:

   ```bash
   uno login
   ```

   The login flow, credential storage, and refresh are entirely handled by `uno-cli`. This skill only invokes `uno call ...` afterwards.

> If `uno` is not on `PATH`, replace it in the examples below with `python /path/to/uno-cli/bin/uno.py`.

## Generating an image — full async flow

A single 1024×1024 image typically takes **~150 s**, longer than the default MCP 60 s timeout. Always use the **submit → poll-result** pattern.

### Step 1 — submit

```bash
uno call gpt-image-2.gpt_image2_submit --compact \
  --args '{"prompt":"A shiba inu under cherry blossoms, sunny afternoon","size":"1024x1024","style":"ghibli_anime"}'
```

Response (already flattened by `uno-cli` — no need to unwrap `content[0].text`):

```json
{"success": true, "data": {"status": "pending", "job_id": "0b84b8f0f0c8", "estimated_seconds": 150}, "meta": {"latency_ms": 120, "credits_used": 300}}
```

Record `data.job_id`.

### Step 2 — poll for result

```bash
uno call gpt-image-2.gpt_image2_result --compact --timeout 70 \
  --args '{"job_id":"0b84b8f0f0c8","wait_seconds":50}'
```

`wait_seconds=50` makes the server-side wait 50 s (within the 60 s MCP envelope); `--timeout 70` adds a small client buffer.

Repeat the call until `data.status` is one of:

- `done` — image ready, URLs in `data.items[].url`.
- `error` — generation failed, message in `data.error`.
- `pending` / `running` — call again immediately. **Do not add a client-side sleep**; the server already waited 50 s on your behalf.

Three to five iterations (~150–250 s total) is normal.

### Reference shell loop

```bash
RESP=$(uno call gpt-image-2.gpt_image2_submit --compact \
  --args '{"prompt":"Van Gogh starry night","style":"oil_painting_vangogh"}')
JOB_ID=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['job_id'])")

for i in 1 2 3 4 5 6; do
  R=$(uno call gpt-image-2.gpt_image2_result --compact --timeout 70 \
    --args "{\"job_id\":\"$JOB_ID\",\"wait_seconds\":50}")
  STATUS=$(echo "$R" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['status'])")
  [ "$STATUS" = "done" ]  && echo "$R" && break
  [ "$STATUS" = "error" ] && echo "$R" && exit 1
done
```

## Parameters

| Field | Meaning | Values |
|---|---|---|
| `prompt` | Image description (required, any language) | free text |
| `size` | Image dimensions | `1024x1024` (default), `1024x1536` (portrait), `1536x1024` (landscape), `auto` |
| `n` | Number of images to generate | 1–4 (default 1) |
| `style` | Built-in style preset | one of the 20 keys below |
| `reference_image_urls` | Reference images (image-to-image) | URL string, comma-separated for multiple |

## 20 built-in style presets

| key | description |
|---|---|
| `ghibli_anime` | Studio Ghibli / hand-drawn anime |
| `pixar_3d` | Pixar / Disney 3D animation |
| `claymation` | Stop-motion claymation (Laika / Aardman) |
| `lego_brick` | LEGO bricks |
| `popmart_figurine` | Blind-box / Pop Mart figurine |
| `isometric_game` | Isometric 2.5D game scene |
| `cinematic_photo` | Cinematic photorealism (35mm) |
| `polaroid_film` | Polaroid film snapshot |
| `watercolor_ink` | Watercolour / East-Asian ink wash |
| `oil_painting_vangogh` | Van Gogh impasto oil painting |
| `cyberpunk_neon` | Cyberpunk neon nightscape |
| `vintage_infographic` | Retro infographic / data poster |
| `movie_poster` | Movie poster (large title + still) |
| `flat_vector` | Flat-vector illustration / banner |
| `pixel_8bit` | Pixel art (8/16-bit) |
| `papercraft_layered` | Layered papercraft |
| `exploded_diagram` | Exploded technical diagram |
| `dreamcore_liminal` | Dreamcore / liminal space |
| `knolling_flatlay` | Top-down knolling / flat-lay |
| `botanical_engraving` | Botanical engraving / antique illustration |

## Where this model shines (vs Midjourney / Flux / SD)

- **Accurate text rendering** — poster headlines, infographics, menu typography, meme captions: written into the image as specified.
- **Strong prompt following** — multi-element scenes, ordering and spatial relationships obeyed.
- **Subject preservation in image-to-image** — faces, brands, and characters stay consistent across reference images.
- **Wide style coverage** — Ghibli, Pixar, claymation, LEGO, Pop Mart, botanical engraving etc. all handled.

## Agent guidance

- Tell the user up-front that one image takes ~150 s.
- The `gpt_image2_result` tool already sleeps 50 s server-side — never add an extra client-side sleep between polls.
- Use `--timeout 70` for `result` calls (50 s server wait + buffer).
- Pass the user's prompt verbatim, including non-English text.
- Reference images: combine `reference_image_urls` with a `style` preset for "restyle while keeping the subject".
- Posters / infographics / menus: lean on the text-rendering strength.
- If `submit` returns `success=false`, surface the `error`/`hint` fields to the user.
- If the loop exhausts (~600 s) and status is still `running`, tell the user the job can be re-polled later with the same `job_id`.

## Response shape

Already flattened by `uno-cli`:

```json
{
  "success": true,
  "data": {"status": "...", "job_id": "...", "items": [{"url": "..."}]},
  "meta": {"latency_ms": 120, "credits_used": 300}
}
```

Read `data.status`, `data.job_id`, `data.items[].url` directly.

Errors:

```json
{"success": false, "error": "...", "hint": "..."}
```
