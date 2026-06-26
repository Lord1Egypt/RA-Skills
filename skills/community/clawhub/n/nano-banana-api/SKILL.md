---
name: nano-banana-api
description: Generate images through the Nano Banana REST API and help agents integrate or operate the service safely. Use when a task involves text-to-image, image-to-image, listing models, checking credits, choosing between sync/stream/async generation, polling generation status, or producing reproducible API calls/scripts for Nano Banana.
metadata:
  openclaw:
    homepage: "https://www.nananobanana.com"
    primaryEnv: "NANO_BANANA_API_KEY"
    requires:
      bins: ["python3"]
---

# Nano Banana API

Use this skill when an agent needs to call Nano Banana directly instead of only editing docs.

Official website: `https://www.nananobanana.com`

## Quick Start

Set an API key with `NANO_BANANA_API_KEY` or `NB_API_KEY`.

Use the bundled CLI for repeatable calls:

```bash
python3 scripts/nano_banana_api.py models
python3 scripts/nano_banana_api.py credits
python3 scripts/nano_banana_api.py generate --prompt "A cinematic orange cat on a train" --mode sync
python3 scripts/nano_banana_api.py generate --prompt "Replace the background with a beach" --reference-image-url https://example.com/image.jpg --mode async --wait
python3 scripts/nano_banana_api.py generate --prompt "A cyberpunk skyline at night" --mode stream
```

## Workflow

1. Call `models` first when the model name matters.
2. Omit `--model` unless the user explicitly asks for a specific model.
3. Choose request mode by interaction pattern:
   - `sync`: simplest request/response flow.
   - `stream`: real-time progress via SSE.
   - `async`: immediate submission plus later polling.
4. Use `poll --id <generation_id> --wait` when an async task must be followed to completion.
5. Download images during the same session when the user wants local files. Output URLs expire after 15 days.

## Operational Rules

- Do not print or restate the raw API key.
- Prefer `models` over hardcoding catalog values. The live model list changes and is the source of truth.
- If docs and live API behavior disagree, trust the live endpoints and mention the date of verification.
- Treat `401`, `402`, `403`, and `503` as actionable operational states:
  - `401`: invalid or missing key.
  - `402`: insufficient credits.
  - `403`: account does not have API access enabled.
  - `503`: async queue is busy; retry later.
- For `stream`, expect newline-delimited SSE `data:` events.
- For `async`, only declare success after `processingStatus` becomes `completed`.

## Command Guide

### List models

```bash
python3 scripts/nano_banana_api.py models
```

Use this before selecting `--model`. Live verification on 2026-03-25 showed model names that differ from examples in the docs, so avoid assuming `nano-banana` is the current explicit model ID.

### Check credits

```bash
python3 scripts/nano_banana_api.py credits
```

### Generate synchronously

```bash
python3 scripts/nano_banana_api.py generate \
  --prompt "A watercolor mountain village at sunrise" \
  --mode sync \
  --download-dir ./outputs
```

### Generate asynchronously and wait

```bash
python3 scripts/nano_banana_api.py generate \
  --prompt "A product hero shot of a banana-shaped lamp" \
  --mode async \
  --wait \
  --poll-interval 3 \
  --max-polls 60
```

### Follow an existing job

```bash
python3 scripts/nano_banana_api.py poll --id clxx123 --wait
```

### Generate from a reference image

```bash
python3 scripts/nano_banana_api.py generate \
  --prompt "Keep the subject, turn the room into a brutalist gallery" \
  --reference-image-url https://example.com/source.jpg \
  --mode sync
```

## Fallback Without The Script

If direct shell execution is unavailable, construct HTTP calls from [references/api-reference.md](references/api-reference.md). Use:

- `POST /generate` for sync, stream, or async submission.
- `GET /generate?id=...` for polling.
- `GET /models` to resolve current model names.
- `GET /credits` to inspect balance.

## Resources

- Use [references/api-reference.md](references/api-reference.md) for endpoint shapes, error handling, and live verification notes.
- Use [scripts/nano_banana_api.py](scripts/nano_banana_api.py) for deterministic CLI access without third-party packages.
