---
name: gpt-image-2-generation
description: Generate images from text prompts using the WellAPI gpt-image-2 model. Use this skill whenever the user asks to create, draw, render, or generate an image, picture, illustration, artwork, photo, or visual from a textual description. Handles API key onboarding, authenticated requests to https://wellapi.ai/v1/images/generations, and decoding the returned base64 image into a local file.
version: 1.0.0
license: MIT
metadata:
  openclaw:
    primaryEnv: WELLAPI_API_KEY
    envVars:
      - name: WELLAPI_API_KEY
        required: false
        description: WellAPI bearer token used to authenticate against the gpt-image-2 endpoint. If unset, the skill will read it from the local config file or prompt the user to enter one.
    requiredBinaries:
      - python3
    capabilities:
      - network
      - filesystem
---

# gpt-image-2-generation

Generate images from natural-language prompts using the **gpt-image-2** model hosted at [WellAPI](https://wellapi.ai). The skill calls `POST https://wellapi.ai/v1/images/generations`, decodes the returned `b64_json`, and writes the image to disk.

## When to use

Trigger this skill when the user asks for things like:

- "Generate an image of a sunset over the ocean"
- "Draw a cat wearing a top hat"
- "Create a 1024x1024 picture of …"
- "Make an illustration / poster / artwork of …"
- Any other request to produce a visual from a textual description.

If the user asks for image *editing* (in-painting, variations, etc.), this skill currently only covers text-to-image generation; tell the user so.

## Prerequisites

1. **API key** — The user must supply a WellAPI key.
   - If the environment variable `WELLAPI_API_KEY` is set, it will be used.
   - Otherwise the skill looks for a local config file:
     - Linux/macOS: `~/.config/gpt-image-2-generation/config.json`
     - Windows:    `%USERPROFILE%\.config\gpt-image-2-generation\config.json`
   - If neither is present, the skill prompts the user to register and enter a key (see *First-run onboarding* below).
2. **Python 3.7+** with the standard library only (no third-party packages required).

## First-run onboarding (no API key found)

When no key can be located, **before making any API call** show the user this short prompt verbatim (translate to the user's language if appropriate) — do **not** expand it into multiple "options / methods", do **not** show shell commands, do **not** ask follow-up questions like "do you already have a key":

> 请粘贴你的 **WellAPI API Key**。
> 如果还没有，请前往 https://wellapi.ai/register?channel=c_qqn3vdvc 注册后领取免费 API Key。
>
> Please paste your **WellAPI API Key**.
> If you don't have one yet, register at https://wellapi.ai/register?channel=c_qqn3vdvc to get a free key.

Wait for the user to reply with the key, then call the helper script to securely store it:

```bash
python3 scripts/setup_api_key.py
```

The script reads the key from stdin and persists it to the per-user config file with `0600` permissions. Never echo or log the full key after it is captured. Do not describe environment-variable alternatives unless the user explicitly asks.

## How to generate an image

Use the bundled script `scripts/generate_image.py`. It accepts CLI arguments, builds the request, sends it with `Authorization: Bearer <key>`, decodes the base64 image, and writes the file.

### Required argument

| Flag | Meaning |
|------|---------|
| `--prompt` | The text description of the image to generate. |

### Optional arguments (defaults match the WellAPI example)

| Flag | Default | Allowed values |
|------|---------|----------------|
| `--n`        | `1`         | integer, number of images |
| `--size`     | `1024x1024` | e.g. `512x512`, `1024x1024`, `1024x1536`, `1536x1024` |
| `--quality`  | `low`       | `low`, `medium`, `high` |
| `--format`   | `jpeg`      | `jpeg`, `png`, `webp` |
| `--model`    | `gpt-image-2` | model name |
| `--output`   | `./gpt-image-2_<timestamp>.<format>` | output file path. When `--n > 1`, an index suffix is added. |
| `--api-key`  | (auto)      | overrides env / config file |
| `--timeout`  | `600` (or `$WELLAPI_TIMEOUT`) | HTTP timeout in seconds. The endpoint is **synchronous** and a single image typically takes **1–3 minutes**, so keep this generous. |

### Example invocations

```bash
# Minimal
python3 scripts/generate_image.py --prompt "大海"

# Custom size + format + output path
python3 scripts/generate_image.py \
  --prompt "A futuristic city skyline at dusk, cyberpunk style" \
  --size 1024x1024 \
  --quality high \
  --format png \
  --output ./city.png
```

The script prints the absolute path(s) of the saved image(s) on success and exits non-zero on failure.

## Request / response contract

**Request body** sent to `https://wellapi.ai/v1/images/generations`:

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

**Headers**

```
Authorization: Bearer <WELLAPI_API_KEY>
Content-Type: application/json
```

**Response** (the image is in `data[i].b64_json`):

```json
{
  "created": 1778236581,
  "data": [{ "b64_json": "iVBORw0KGg..." }],
  "output_format": "png",
  "quality": "low",
  "size": "1024x1024",
  "usage": { "input_tokens": 8, "output_tokens": 196, "total_tokens": 204 }
}
```

The skill base64-decodes each `b64_json` entry and writes the bytes to disk using `output_format` (or the requested `--format`) as the file extension.

## Workflow for the agent

1. Parse the user's image request → extract `prompt`, and any explicit `size`, `quality`, `format`, `n`.
2. Resolve the API key (env → config file → prompt user via `scripts/setup_api_key.py`).
3. Run `scripts/generate_image.py` with the parsed arguments. **The endpoint is synchronous and commonly takes 1–3 minutes — wait for the script to return; do not abort or retry early.** If your tool runner has its own command timeout, raise it (e.g. ≥ 600s) before invoking the script.
4. Report the saved file path(s) to the user. If running in an environment that can render images, also display the result.
5. On HTTP errors, surface the upstream error message verbatim and suggest checking the API key, quota, or prompt content. On a real timeout, retry once or pass `--timeout` / set `WELLAPI_TIMEOUT` to a larger value.

### Non-200 responses → group capacity hint

Whenever WellAPI returns a non-200 status (typical examples: `400`, `401`, `403`, `404`, `429`, `5xx`), the script appends a remediation hint to its error output. **Always relay this hint to the user verbatim** — the most common root cause is that the API Key's group does not have available capacity for `gpt-image-2`.

Tell the user (translate to their language if needed):

> 接口返回非 200 状态码，可能是该 API Key 所属分组资源不足。请登录 https://wellapi.ai 的「API 令牌管理」，把此 API Key 的分组修改为 **「官转OpenAI分组」** 或 **「优质官转OpenAI分组」**，保存后重新让我生成图片即可。

Only after the user confirms they have switched groups (or explicitly asks to retry) should you re-invoke `scripts/generate_image.py`. Do not silently retry on 4xx/5xx — the same group will fail again.

## Files in this skill

- `SKILL.md` — this file (metadata + instructions)
- `scripts/generate_image.py` — performs the generation
- `scripts/setup_api_key.py` — interactive helper to store the API key
- `scripts/api_key.py` — shared helpers for locating/loading the key
- `README.md` — marketplace listing

## Security notes

- The API key is stored locally in the user's home directory with `0600` permissions and is **never** committed, logged, or echoed.
- All network traffic goes only to `https://wellapi.ai`.
- The skill does not execute or evaluate any data returned by the API beyond base64-decoding the image bytes.
