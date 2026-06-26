---
name: nano-banana-2
description: "Generate or edit images with the NanoPhoto.AI Nano Banana 2 API. Use when: (1) User wants text-to-image generation, (2) User wants image-to-image editing with public image URLs, (3) User mentions Nano Banana 2, AI image generation, image editing, Google Search enhanced prompts, or checking Nano Banana generation status. Supports aspect ratio, quality, optional Google Search prompt enhancement, status checks, and optional in-process polling from a single bundled script. Prerequisite: Obtain an API key at https://nanophoto.ai/settings/apikeys and configure env.NANOPHOTO_API_KEY."
metadata: {"openclaw":{"homepage":"https://nanophoto.ai","requires":{"env":["NANOPHOTO_API_KEY"]},"primaryEnv":"NANOPHOTO_API_KEY"}}
---

# Nano Banana 2

Generate or edit images through the NanoPhoto.AI Nano Banana 2 API.

## Prerequisites

1. Obtain an API key at: https://nanophoto.ai/settings/apikeys
2. Configure `NANOPHOTO_API_KEY` before using the skill.
3. Do not paste the API key into chat; store it in the platform's secure env setting for this skill.

Preferred OpenClaw setup:

- Open the skill settings for this skill
- Add an environment variable named `NANOPHOTO_API_KEY`
- Paste the API key as its value

Equivalent config shape:

```json
{
  "skills": {
    "entries": {
      "nano-banana-2": {
        "enabled": true,
        "env": {
          "NANOPHOTO_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

Other valid ways to provide the key:

- **Shell**: `export NANOPHOTO_API_KEY="your_api_key_here"`
- **Tool-specific env config**: any runtime that injects `NANOPHOTO_API_KEY`
- **OpenClaw config fallback**: the bundled script also falls back to `~/.openclaw/openclaw.json` at `skills.entries.nano-banana-2.env.NANOPHOTO_API_KEY`

Credential declaration summary:

- Primary credential: `NANOPHOTO_API_KEY`
- Resolution order in the bundled script: `--api-key` → `NANOPHOTO_API_KEY` environment variable → `~/.openclaw/openclaw.json` skill env
- No unrelated credentials are required

## Recommended workflow

1. Collect the user's prompt.
2. Decide whether the request is `generate` (text-to-image) or `edit` (image-to-image).
3. Choose `aspectRatio`, `imageQuality`, and whether `googleSearch` should be enabled.
4. For edit mode, require one to fourteen public image URLs.
5. Submit the generation request.
6. If the user wants synchronous progress output in the same process, use `submit --follow`.
7. Poll every 3-5 seconds until `completed` or `failed`.
8. Return the final `imageUrl`, `generationId`, and progress details when available.

## Parameter guidance

- `mode`
  - `generate`: text-to-image
  - `edit`: image-to-image; requires `inputImageUrls`
- `aspectRatio`
  - `16:9`
  - `9:16`
  - `4:3`
  - `3:4`
- `imageQuality`
  - `1K`: default, lowest cost
  - `2K`: higher detail
  - `4K`: highest detail and highest cost
- `googleSearch`
  - Disabled by default
  - Enable only when web context is likely to improve specificity

## Preferred commands

Use the single bundled script with subcommands.

### Submit text-to-image generation

```bash
python3 scripts/nano_banana_2.py submit \
  --prompt "A futuristic cityscape at sunset with flying cars and neon lights" \
  --mode generate \
  --aspect-ratio 16:9 \
  --image-quality 2K
```

### Submit with Google Search enhancement and in-process polling

```bash
python3 scripts/nano_banana_2.py submit \
  --prompt "The latest Tesla Cybertruck in a desert landscape" \
  --mode generate \
  --aspect-ratio 16:9 \
  --image-quality 2K \
  --google-search \
  --follow
```

### Submit image-to-image editing

```bash
python3 scripts/nano_banana_2.py submit \
  --prompt "Transform this photo into a watercolor painting style" \
  --mode edit \
  --aspect-ratio 16:9 \
  --image-quality 1K \
  --input-image-url https://static.nanophoto.ai/demo/nano-banana-pro.webp
```

### Check status of an existing generation

```bash
python3 scripts/nano_banana_2.py status --generation-id abc123xyz
```

## Script behavior

The bundled script resolves credentials in this order: `--api-key`, then `NANOPHOTO_API_KEY` from the environment, then `~/.openclaw/openclaw.json` at `skills.entries.nano-banana-2.env.NANOPHOTO_API_KEY`.

Subcommands:

- `submit`: submit a generation task
- `submit --follow`: submit and keep polling in the same process
- `status`: check an existing `generationId`

Cross-platform note:

- Use `python3` on macOS/Linux.
- Use `python` on Windows unless `python3` is available.
- The script uses Python's standard HTTP client and does not require `curl`.
- Use `--json-only` when another script/tool needs raw JSON output.
- Use `--poll-interval` to override the default 4-second polling interval.
- Default max wait is 180 seconds.

## Manual API calls

### Submit generation

```bash
curl -X POST "https://nanophoto.ai/api/nano-banana-2/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NANOPHOTO_API_KEY" \
  --data-raw '{
    "prompt": "A futuristic cityscape at sunset with flying cars and neon lights",
    "mode": "generate",
    "aspectRatio": "16:9",
    "imageQuality": "2K"
  }'
```

### Check status

```bash
curl -X POST "https://nanophoto.ai/api/nano-banana-2/check-status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NANOPHOTO_API_KEY" \
  --data-raw '{"generationId": "abc123xyz"}'
```

## Error handling

| errorCode | Cause | Action |
|-----------|-------|--------|
| `LOGIN_REQUIRED` | Invalid or missing API key | Verify key at https://nanophoto.ai/settings/apikeys |
| `API_KEY_RATE_LIMIT_EXCEEDED` | Rate limit exceeded | Wait and retry |
| `INSUFFICIENT_CREDITS` | Not enough credits | Top up credits |
| `INVALID_PROMPT` | Missing or invalid prompt | Ask for a valid prompt |
| `MISSING_INPUT_IMAGE` | Edit mode missing images | Ask for public image URLs |
| `TOO_MANY_IMAGES` | Too many images provided | Limit to 14 public image URLs |
| `IMAGE_URLS_REQUIRED` | API needs `inputImageUrls` | Do not send local files or base64 |
| `GENERATION_FAILED` | Server-side generation error | Retry or simplify the prompt |
| `NOT_FOUND` | Unknown generation ID | Re-submit or verify the ID |
| `FORBIDDEN` | Generation not owned by caller | Verify the account |

## Bundled files

- `scripts/nano_banana_2.py`: single entry point for submit, status, and optional in-process polling
- `references/api.md`: condensed API reference, parameters, and error behavior
