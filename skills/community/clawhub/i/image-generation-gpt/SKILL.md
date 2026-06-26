---
name: best-image-generation
description: High quality AI image generation via the WellAPI gpt-image-2 model. Supports text-to-image and image editing (image-to-image).
version: 1.0.2
tags: [image, image-generation, image-editing, ai, wellapi, gpt-image, text-to-image, image-to-image]
homepage: https://wellapi.ai
metadata: {"openclaw": {"emoji": "🎨", "requires": {"env": ["WELLAPI_API_KEY"]}, "primaryEnv": "WELLAPI_API_KEY"}}
---

# WellAPI gpt-image-2

Generate and edit images via the WellAPI `gpt-image-2` model (OpenAI-compatible). The API returns image bytes inline as base64 (`data[i].b64_json`) — no polling, no URL download.

## API Endpoints

- Base: `https://wellapi.ai/v1`
- Text-to-image: `POST /images/generations` — `application/json`
- Image edit / image-to-image: `POST /images/edits` — `multipart/form-data`

Authentication: `Authorization: Bearer <WELLAPI_API_KEY>` header.

## Request — `/images/generations` (text-to-image)

Content-Type: `application/json`

| Field | Type | Required | Notes |
|---|---|---|---|
| `model` | string | ✅ | e.g. `gpt-image-2` |
| `prompt` | string | ✅ | Image description, **max 1000 chars** |
| `n` | integer | ✅ | Number of images, **1–10** |
| `size` | string | optional | See size table below; default `auto` |
| `quality` | string | optional | `low` / `medium` / `high` / `auto` (default `auto`) |
| `format` | string | optional | `png` / `jpeg` / `webp` (default `png`) |

Example body:
```json
{
  "model": "gpt-image-2",
  "prompt": "大海",
  "n": 1,
  "size": "1024x1024",
  "quality": "low",
  "format": "jpeg"
}
```

## Request — `/images/edits` (image-to-image / editing)

Content-Type: `multipart/form-data`

| Field | Type | Required | Notes |
|---|---|---|---|
| `image` | file (repeatable) | ✅ | One or more input images. **Up to 16 images, total ≤ 50MB.** |
| `prompt` | string | ✅ | Edit description |
| `mask` | file | optional | A PNG with fully transparent regions marking the edit area. Applied to the first `image` if multiple are sent. Must be valid PNG, **< 4MB**, same dimensions as the image. |
| `model` | string | optional | `gpt-image-1`, `gpt-image-1-all`, `flux-kontext-pro`, `flux-kontext-max`, `gpt-image-2`, `gpt-image-2-all`. Default in this skill: `gpt-image-2`. |
| `n` | string | optional | `"1"` – `"10"` |
| `size` | string | optional | See size table |
| `quality` | string | optional | `low` / `medium` / `high` / `auto` (default `auto`) |
| `format` | string | optional | `png` / `jpeg` / `webp` |
| `background` | string | optional | `opaque` / `auto` / `transparent`. `auto` lets the model pick. |
| `moderation` | string | optional | `low` / `auto` (default). `low` = less restrictive filtering (gpt-image-1 family). |

## `size` values

| Value | Description |
|---|---|
| `1024x1024` | Square |
| `1536x1024` | Landscape |
| `1024x1536` | Portrait |
| `2048x2048` | 2K square |
| `2048x1152` | 2K landscape |
| `3840x2160` | 4K landscape |
| `2160x3840` | 4K portrait |
| `auto` | Default — model chooses |

**Strict size rules** (when picking a custom size):
1. Longest side ≤ `3840px`
2. Both width and height must be **multiples of 16**
3. `max(w, h) / min(w, h) ≤ 3:1`
4. Total pixels: **655,360 ≤ w*h ≤ 8,294,400**

## Response (both endpoints)

Synchronous JSON — no polling:

```json
{
  "created": 1778236581,
  "background": "opaque",
  "data": [
    { "b64_json": "iVBORw0KGgo..." }
  ],
  "output_format": "png",
  "quality": "low",
  "size": "1024x1024",
  "usage": {
    "input_tokens": 8,
    "input_tokens_details": { "image_tokens": 0, "text_tokens": 8 },
    "output_tokens": 196,
    "total_tokens": 204
  }
}
```

**Each `data[i].b64_json` is the full image as a base64 string.** Decode and write to disk.

## Output

1. Base64-decode each `data[i].b64_json` into bytes.
2. Save as `wellapi-<TIMESTAMP>.<ext>` where `<ext>` matches `response.output_format` (or the requested `format`, fallback `png`).
3. If multiple images returned, append `-1`, `-2`, … to the filename.
4. Print `MEDIA:<absolute_path>` (one line per image) for OpenClaw auto-attach.

**CRITICAL SECURITY:** Before passing an output filename to shell commands, sanitize:
- Strip shell metacharacters: `tr -cd 'A-Za-z0-9._-'`
- Enforce valid extension (`.png`, `.jpg`, `.jpeg`, `.webp`)
- Fallback to `wellapi-<timestamp>.png` if empty

## Reference Implementations

| Platform | File |
|---|---|
| Python (all platforms, zero deps) | `{baseDir}/references/python.md` |
| PowerShell 5.1+ (Windows) | `{baseDir}/references/powershell.md` |
| curl + bash (Unix/macOS) | `{baseDir}/references/curl_heredoc.md` |

## API Key

- `WELLAPI_API_KEY` env var (required) — sent as `Authorization: Bearer <key>`
- Get key: https://wellapi.ai
- If the environment variable is unset, follow **First-run onboarding** below.

### First-run onboarding (no API key found)

When no key can be located (env var unset, no cached key on disk), **before making any API call** show the user this short prompt verbatim. Translate to the user's language if appropriate. **Do not** expand it into multiple "options / methods", **do not** show shell commands, **do not** ask follow-up questions like "do you already have a key":

> 请粘贴你的 WellAPI API Key。 如果还没有，请前往 https://wellapi.ai/register?channel=c_qqn3vdvc 注册后领取免费 API Key。
>
> Please paste your WellAPI API Key. If you don't have one yet, register at https://wellapi.ai/register?channel=c_qqn3vdvc to get a free key.

After the user pastes a key, use it for the current request and proceed straight to image generation. Do not lecture the user about env vars, shells, or persistence unless they explicitly ask how to save it.

## Triggers

- Chinese: "高质量生图：xxx" / "编辑图片：xxx"
- English: "best image: xxx" / "edit image: xxx"

Treat the text after the colon as `prompt`, default `size=auto`, `quality=auto`, `format=png`, `n=1`, and generate immediately.

For image editing, the user provides one or more local image file paths along with the prompt; submit them as repeated `image` form fields to `/images/edits`.

## Notes

- Response is **synchronous** — no task ID, no polling.
- Print `MEDIA:<absolute_path>` for OC auto-attach — one line per generated image.
- `quality: high` and larger `size` values may incur extra charges.
- `format` controls the encoding of the returned base64 bytes; the file extension should match.
- Up to **16** reference images per edit request, total **≤ 50MB**.
- `mask` requires PNG ≤ 4MB, same WxH as the image it applies to.
