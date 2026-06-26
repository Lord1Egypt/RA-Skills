---
name: myreels-api
description: >
  Use this skill when the user wants to generate images, videos, speech, or music
  with MyReels, inspect the live model schema, submit a generation task, list
  the authenticated user's tasks, or poll task status. Prefer the bundled shell
  scripts before hand-writing curl/fetch requests. Use this whenever the user
  mentions MyReels generation, model selection, task history, task polling,
  result URLs, or MyReels API integration.
homepage: https://myreels.ai
repository: https://github.com/myreelsai/skills
requires:
  env:
    - MYREELS_ACCESS_TOKEN
    - MYREELS_BASE_URL
  runtime:
    - curl
    - jq
metadata:
  author: myreelsai
---

# MyReels API

This skill is the executable interface to the MyReels public API. Use the bundled scripts first. Fall back to the raw HTTP references only when the scripts do not cover the case.

## Operator Rules

- Always read the live model schema before building a request body.
- Do not invent parameter names. Use `userInputSchema` from the live models endpoint.
- Prefer the bundled scripts over hand-written `curl` or `fetch`.
- Save result URLs on your side. Do not assume MyReels stores them forever.

## Prerequisites

- An active MyReels subscription is required for generation and task query endpoints.
- Create an AccessToken in [myreels.ai/developer](https://myreels.ai/developer).
- `GET https://api.myreels.ai/api/v1/models/api` was verified on March 18, 2026 and currently does not require `Authorization`.

Config file `~/.myreels/config`:

```bash
MYREELS_BASE_URL="https://api.myreels.ai"
MYREELS_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"
```

The scripts in this skill read that file automatically. Environment variables override the file.

First-time setup or config issues:

```bash
scripts/myreels-doctor.sh
```

## Bundled Scripts

- `scripts/myreels-doctor.sh`
  Checks config, dependencies, and live connectivity.
- `scripts/myreels-models.sh`
  Loads live model metadata and can filter by tag or `modelName`.
- `scripts/myreels-generate.sh`
  Submits a generation task for a chosen model.
- `scripts/myreels-tasks-list.sh`
  Lists the authenticated user's tasks with paging and filters.
- `scripts/myreels-task-get.sh`
  Queries a task and derives the next action for the agent.

## Recommended Workflow

### 1. Load live models first

```bash
scripts/myreels-models.sh --summary
```

If you already know the candidate model, inspect its full schema:

```bash
scripts/myreels-models.sh --model MODEL_NAME
```

Priority fields when selecting a model:

- `modelName`
- `name`
- `tags`
- `description`
- `estimatedCost`
- `displayConfig.estimatedTime`
- `userInputSchema`
- `userInputSchema.<param>.label`
- `userInputSchema.<param>.description`
- `userInputSchema.<param>.default`
- `userInputSchema.<param>.options`

For natural-language requests such as "stronger motion" or "disable prompt extension", map user intent from `label` and `description`, not from field names alone.

### 2. List existing tasks when needed

Use this when the user asks for recent tasks, task history, or wants to find tasks by status or date.

```bash
scripts/myreels-tasks-list.sh --page 1 --limit 10
```

Common filters:

```bash
scripts/myreels-tasks-list.sh --status completed --start-date 2026-03-01T00:00:00.000Z
```

For `GET` requests, the public Worker uses query parameters for these filters.

Supported task status values:

- `pending`
- `processing`
- `completed`
- `failed`
- `cancelled`
- `warning`

### 3. Submit a task

Use the real `modelName`, not a display slug.

Example:

```bash
scripts/myreels-generate.sh nano-banana2 '{"prompt":"A cinematic portrait with soft studio lighting"}'
```

Alternative if the request body is large:

```bash
scripts/myreels-generate.sh --model nano-banana2 --file request.json
```

The script returns a normalized JSON acknowledgement with `taskID` and the next polling hint.

### 4. Poll task status

```bash
scripts/myreels-task-get.sh TASK_ID
```

The script returns a simplified action model:

- `WAIT`
  Task is still running. Poll again later.
- `DELIVER`
  Task completed. Deliver `resultUrls` to the user.
- `FAILED`
  Task failed. Explain the failure and retry with a corrected request.
- `REVIEW`
  Unexpected task state. Inspect the raw response before retrying.

Task states from the public API:

- `pending`
- `processing`
- `completed`
- `failed`
- `cancelled`
- `warning`

Polling guidance:

- image generation / image editing: 10 seconds
- video generation: 30 seconds to 1 minute

Query rate limit:

- 60 requests per minute

### 5. Deliver result URLs

When `nextAction=DELIVER`, read `resultUrls` from the output and pass the final URLs to the user. Save them on your side if persistence matters.

## Response Rules

- Check the final HTTP status first.
- If the HTTP status is `2xx`, then inspect the response body `status`.
- For task queries, check `data.status` after `status === "ok"`.
- If the upstream response includes `code`, the Worker uses it as the final HTTP status.
- If the upstream response does not include `code`, the Worker falls back to the upstream HTTP status.

## Public Paths

- `POST /generation/:modelName`
- `GET /generation/tasks`
- `GET /query/task/:taskID`
- `GET|POST /api/v1/*`

## Model Categories

| Category | Tags | Description |
|------|------|------|
| Image and editing | `t2i` / `i2i` / `i2e` | text-to-image, image-to-image, image editing |
| Video | `t2v` / `i2v` | text-to-video, image-to-video, avatar/video motion |
| Speech and music | `t2a` / `m2a` | text-to-speech, music generation |

## Raw API Fallback

If the bundled scripts do not cover the case, use the raw HTTP references:

- [references/models.md](references/models.md)
- [references/code-examples.md](references/code-examples.md)
- [references/errors.md](references/errors.md)

## Install

```bash
npx skills add https://github.com/myreelsai/skills --skill myreels-api -g
```

Remove `-g` for a project-level install.
