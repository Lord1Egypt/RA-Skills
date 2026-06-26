---
name: happy_img2_direct
version: 1.0.0
description: Generate images with an OpenAI-compatible image provider such as happy/gpt-image-2, with retries and bounded batch concurrency.
metadata:
  openclaw:
    emoji: "🖼️"
    requires:
      bins:
        - python3
        - node
      config:
        - models.providers
---

# Happy IMG2 Direct Skill

Generate real images through an OpenAI-compatible `/images/generations` endpoint configured in OpenClaw.

Default behavior:

- provider: `happy` unless `OPENCLAW_IMAGE_PROVIDER` is set
- model: `gpt-image-2` unless `OPENCLAW_IMAGE_MODEL` is set
- size: `1024x1024`
- timeout: `600000ms` per image
- output: `~/.openclaw/generated-images/`
- no local fake-image fallback
- no built-in message delivery; send or attach files using your normal OpenClaw/channel tools

## Single image

```bash
python3 skills/happy-img2-direct/scripts/run.py \
  --prompt "A realistic photo of an orange cat sitting by a window, no text, no watermark" \
  --task-name "cat-test" \
  --no-send
```

Useful flags:

- `--prompt` required
- `--task-name` output filename prefix
- `--provider` provider key in OpenClaw config, default `happy`
- `--model` image model, default `gpt-image-2`
- `--size` default `1024x1024`
- `--timeout-ms` default `600000`
- `--output-dir` default `~/.openclaw/generated-images`
- `--max-attempts` default `3`, maximum `5`
- `--retry-base-delay`, `--retry-max-delay`, `--retry-jitter`
- `--raw` marker for callers that intentionally keep the user prompt unchanged
- `--no-send` accepted for compatibility; this public skill always leaves delivery to the caller

Successful output is JSON containing `ok:true`, `image_path` or `output`, bytes, model/provider, attempt count, and run directory.

## Batch images

```bash
python3 skills/happy-img2-direct/scripts/batch_run.py @batch.json
```

Example:

```json
{
  "batch_name": "article-covers",
  "max_workers": 4,
  "timeout_ms": 600000,
  "send_to_feishu": false,
  "tasks": [
    {"task_name": "cover-1", "prompt": "Realistic shop counter photo, no readable text"},
    {"task_name": "cover-2", "prompt": "Realistic office desk photo, no readable text"}
  ]
}
```

Batch rules:

- bounded concurrency, current hard maximum `4`
- each item has its own task directory and logs
- one failed image does not prevent other images from finishing
- final `batch_result.json` records success/failure per task
- delivery is disabled in the public version; use OpenClaw/channel tools to send files

## Retry behavior

Retries are limited and only used for retryable failures:

- timeout
- upstream failures
- rate limits
- HTTP `408/429/500/502/503/504`
- wrapper parse errors

Non-retryable errors, such as invalid requests or auth failures, fail fast with redacted diagnostics.

## Safety and publishing notes

This skill intentionally contains no private OpenClaw IDs, no hard-coded user paths, no API keys, and no channel recipient IDs. It reads provider configuration from the local OpenClaw config at runtime.
