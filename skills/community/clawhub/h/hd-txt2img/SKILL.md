---
name: hd-txt2img-skill
description: Call Hidream txt2img async API with exposed auth and request parameters. Use when users need to generate images from text prompts, build runnable Python command examples, enforce allowed resolution values, or troubleshoot Hidream task polling/results.
---

# HD TXT2IMG Skill

Use Python script `scripts/generate_image.py` to submit txt2img tasks and wait for final images.

## Required Endpoint

- `POST https://www.hidreamai.com/api-pub/gw/v3/image/txt2img/async`
- `GET https://www.hidreamai.com/api-pub/gw/v3/image/txt2img/async/results?task_id=...`

## Auth

- Header: `Authorization: Bearer {USER_Authorization}`
- Header: `Content-Type: application/json`
- Do not hardcode real token in repository files.

## Exposed Parameters

- `authorization` (string): token value only, without `Bearer `
- `prompt` (string): text prompt
- `resolution` (string): must be one of:
  - `1024*1024`
  - `832*1248`
  - `880*1168`
  - `768*1360`
  - `1248*832`
  - `1168*880`
  - `1360*768`

## Execution Example

```bash
python3 hd-txt2img-skill/scripts/generate_image.py \
  --authorization "sk-" \
  --prompt "一个跳舞的小女孩" \
  --resolution "1024*1024"
```

## Script Behavior

1. Build async txt2img request payload.
2. Submit task and get `task_id`.
3. Poll result API until task finishes.
4. Return final structured result object from code and print JSON in CLI mode.

