---
name: masonry
description: AI-powered image and video generation. Generate images, videos, manage jobs, and explore models via the masonry CLI.
metadata: {"openclaw":{"emoji":"🧱","requires":{"bins":["masonry"],"env":["MASONRY_TOKEN"]},"install":[{"type":"npm","package":"@masonryai/cli"}],"primaryEnv":"MASONRY_TOKEN","homepage":"https://masonry.so"}}
---

# Masonry CLI

Generate AI-powered images and videos from text prompts.

## When to use

- User wants to generate images or videos
- User asks about available AI models
- User wants to check generation job status or download results
- User asks to create visual content, media, or artwork

## Prerequisites

A Masonry subscription is required. Start a free trial at: https://masonry.so/pricing

If the `masonry` command is not found, install it:
```bash
npm install -g @masonryai/cli
```

Or run directly: `npx @masonryai/cli`

## Authentication

If any command returns an auth error:

1. Run: `masonry login --remote`
2. The command prints an auth URL. Send it to the user.
3. User opens the URL in a browser, authenticates, and copies the token.
4. Run: `masonry login --token <TOKEN>`

For environments with `MASONRY_TOKEN` and `MASONRY_WORKSPACE` set, no login is needed.

## Workflow

### 1. Generate content

**Image:**
```bash
masonry image "a sunset over mountains, photorealistic" --aspect 16:9
```

**Video:**
```bash
masonry video "ocean waves crashing on rocks" --duration 4 --aspect 16:9
```

### 2. Handle the response

Commands return JSON immediately:
```json
{
  "success": true,
  "job_id": "abc-123",
  "status": "pending",
  "check_after_seconds": 10,
  "check_command": "masonry job status abc-123"
}
```

### 3. Wait and download

```bash
masonry job wait <job-id>
masonry job download <job-id> -o /tmp/output.png
```

The download command prints a `MEDIA: /path/to/file` line to stderr.
After download completes, output that line so the file is sent to the user:

```
MEDIA: /tmp/output.png
```

## Image flags

| Flag | Short | Description |
|------|-------|-------------|
| `--aspect` | `-a` | Aspect ratio: 16:9, 9:16, 1:1 |
| `--dimension` | `-d` | Exact size: 1920x1080 |
| `--model` | `-m` | Model key |
| `--output` | `-o` | Output file path |
| `--negative-prompt` | | What to avoid |
| `--seed` | | Reproducibility seed |

## Video flags

| Flag | Short | Description |
|------|-------|-------------|
| `--duration` | | Length in seconds: 4, 6, 8 |
| `--aspect` | `-a` | Aspect ratio: 16:9, 9:16 |
| `--model` | `-m` | Model key |
| `--image` | `-i` | First frame image (local file) |
| `--last-image` | | Last frame image (requires --image) |
| `--no-audio` | | Disable audio generation |
| `--seed` | | Reproducibility seed |

## Model discovery

```bash
masonry models list              # All models
masonry models list --type image # Image models only
masonry models list --type video # Video models only
masonry models info <model-key>  # Parameters and usage example
```

## Job management

```bash
masonry job list                          # Recent jobs
masonry job status <job-id>               # Check status
masonry job download <job-id> -o ./file   # Download result
masonry job wait <job-id> --download -o . # Wait then download
masonry history list                      # Local history
masonry history pending --sync            # Sync pending jobs
```

## Error codes

| Code | Meaning | Action |
|------|---------|--------|
| `AUTH_ERROR` | Not authenticated | Run auth flow above |
| `VALIDATION_ERROR` | Invalid parameter | Check flag values |
| `MODEL_NOT_FOUND` | Unknown model key | Run `masonry models list` |

## Guardrails

- Never fabricate job IDs or model keys. Always use values from command output.
- Never run `masonry login` without `--remote` or `--token` (browser login won't work headless).
- If a job is pending, wait `check_after_seconds` before checking again.
- All output is JSON. Parse it, don't guess.

## Feedback

Report issues or suggest improvements at: https://github.com/masonry-so/skills/issues

When filing an issue, include:
- **What was your intent?** What were you trying to accomplish?
- **What worked?** Which parts behaved as expected?
- **What needs improvement?** What went wrong or could be better?
