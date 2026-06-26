---
name: jogg-lip-sync
description: Runs Jogg lip sync using video and audio inputs, reuses tasks when available, and monitors status until completion. Use to generate or check lip sync results.
license: Proprietary
compatibility: Requires curl, jq, a local shell environment, and JOGG_API_KEY to call the Jogg API.
metadata: { "author": "JoggAI", "version": "0.1.0", "openclaw": { "emoji": "🎙️", "requires": { "bins": ["curl", "jq"], "env": ["JOGG_API_KEY"] }, "primaryEnv": "JOGG_API_KEY", "os": ["darwin", "linux"], "install": [ { "id": "brew-jq", "kind": "brew", "formula": "jq", "bins": ["jq"], "label": "Install jq (brew)", "os": ["darwin", "linux"] } ] } }
---

# Jogg Lip Sync

Use this skill to execute lip sync tasks directly, not to generate integration code.

All paths in this document are relative to the current skill root directory.

Runner:

- `sh "run.sh"`

## Trigger

- User asks to run lip sync
- User asks to check lip sync task status
- User provides video and audio and expects the final driven video result

## Required Inputs

- video input: URL or local file path
- audio input: URL or local file path

Optional:

- `JOGG_BASE_URL`, default `https://api.jogg.ai`
- `JOGG_API_PLATFORM`, default `openclaw`
- `playback_type`, default `normal`
- `poll_interval_seconds`, default `10`
- `max_wait_seconds`, default `1800`

If any required input is missing, ask only for the missing item.

Default values used when unset:
- `JOGG_BASE_URL=https://api.jogg.ai`
- `JOGG_API_PLATFORM=openclaw`
- `JOGG_LIP_SYNC_DEFAULT_PLAYBACK_TYPE=normal`
- `JOGG_LIP_SYNC_DEFAULT_POLL_INTERVAL_SECONDS=10`
- `JOGG_LIP_SYNC_DEFAULT_MAX_WAIT_SECONDS=1800`

- `JOGG_API_KEY` is required.
- Other current environment variables are optional.
- If `JOGG_API_KEY` is empty, stop and tell the user to purchase an API plan at `https://www.jogg.ai/api-pricing/` and obtain an API key before continuing.

## Hard Rules

- Execute the existing runner in the current run.
- Prefer the fixed runner over handwritten HTTP calls.
- Use `run.sh` as the only runner entrypoint.
- Do not write scripts, helper files, SDKs, wrappers, or temporary executors.
- Do not replace execution with code generation.
- Do not create duplicate tasks for the same normalized inputs in one run.
- Reuse existing tasks whenever allowed by the decision rules.
- Prefer returning the final video result over producing artifacts.

## Endpoints

- `POST /v2/upload/asset`
- `GET /v2/lip_sync_video`
- `POST /v2/create_lip_sync_video`
- `GET /v2/lip_sync_video/:task_id`

Header:

- `X-Api-Key: $JOGG_API_KEY`
- optional `x-api-platform: $JOGG_API_PLATFORM`

## Procedure

1. Collect missing inputs only.
2. For create or reuse flow, execute the runner with `--no-poll` first.
3. Parse the returned JSON and read `task_id` plus `status`.
4. If status is `pending` or `processing`, call the runner again with `--task-id` to query or poll.
5. Return the execution result directly in the conversation.

Output contract:

- `stdout`: final machine-readable JSON result only
- `stderr`: progress logs during upload, query, create, and polling
- Recommended agent pattern: create with `--no-poll`, then query by `task_id`

## Runner Modes

Create or reuse a task:

```bash
sh "run.sh" \
  --video "<video-url-or-file>" \
  --audio "<audio-url-or-file>" \
  --playback-type "normal" \
  --no-poll
```

Query a task by `task_id`:

```bash
sh "run.sh" \
  --task-id "<task-id>"
```

Useful flags:

- `--force-recreate`: only when the user explicitly asks to regenerate after a terminal task
- `--poll`: wait until terminal state in `task_id` mode
- `--no-poll`: return immediately in create or reuse mode; recommended for the first runner call from the skill
- `--poll-interval-seconds`
- `--max-wait-seconds`

`run.sh` behavior:

- Uses the native shell implementation directly.
- Requires `curl` and `jq`.
- Uses the system default values when optional environment variables are unset.

## Decision Rules

- `playback_type` defaults to `normal` if omitted.
- The query endpoint returns the latest matching task under the current authenticated user and space.
- Reuse `pending`, `processing`, and `success` tasks by default.
- Do not recreate a `failed` task unless the user explicitly requests a retry.
- Query before every create attempt.

Allowed `playback_type` values:

- `normal`
- `normal_reverse`
- `normal_reverse_by_audio`

## Output

Return only execution results:

- `action`
- `reused`
- Whether an existing task was reused or a new one was created
- `task_id`
- Current `status`
- `data.result_url` when successful
- `error.message` when failed
- If still running, return the live `task_id` and `status`
- Never replace the result with a generated script or file
