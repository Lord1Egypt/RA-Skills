---
name: veo-3-1
description: "Generate videos with the NanoPhoto.AI Veo 3.1 API. Use when: (1) User wants Veo 3.1 text-to-video generation, (2) User wants Veo 3.1 generation from reference images or first/last frames, (3) User wants multi-shot long-form Veo video generation, or (4) User wants to check Veo generation status. Supports up to 21 shots, 720p/1080p/4k output rules, status checks, and optional in-process polling from a single bundled script. Prerequisite: Obtain an API key at https://nanophoto.ai/settings/apikeys and configure env.NANOPHOTO_API_KEY."
metadata: {"openclaw":{"homepage":"https://nanophoto.ai","requires":{"env":["NANOPHOTO_API_KEY"]},"primaryEnv":"NANOPHOTO_API_KEY"}}
---

# Veo 3.1

Generate videos through the NanoPhoto.AI Veo 3.1 API.

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
      "veo-3-1": {
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
- **OpenClaw config fallback**: the bundled script also falls back to `~/.openclaw/openclaw.json` at `skills.entries.veo-3-1.env.NANOPHOTO_API_KEY`

Credential declaration summary:

- Primary credential: `NANOPHOTO_API_KEY`
- Resolution order in the bundled script: `--api-key` → `NANOPHOTO_API_KEY` environment variable → `~/.openclaw/openclaw.json` skill env
- No unrelated credentials are required

## Recommended workflow

1. Build a `shots` array.
2. For each shot, set `id`, `prompt`, `generationType`, and `aspectRatio`.
3. Add public `imageUrls` only when the generation type requires them.
4. Choose `resolution`.
   - Use `720p` by default.
   - Use `1080p` or `4k` only for single-shot jobs.
5. Submit the generation request.
6. If the user wants synchronous progress output in the same process, use `submit --follow`.
7. Poll every 5-10 seconds until `completed` or `failed`.
8. Return final shot-level `videoUrl` values and timing information when available.

## Shot rules

- Max 21 shots total
- Each shot is 8 seconds
- Max total runtime is 168 seconds
- `TEXT_2_VIDEO`
  - No `imageUrls`
- `FIRST_AND_LAST_FRAMES_2_VIDEO`
  - Requires 1-2 public `imageUrls`
- `REFERENCE_2_VIDEO`
  - Requires 1-3 public `imageUrls`

## Preferred commands

Use the single bundled script with subcommands.

### Submit a single text-to-video shot

```bash
python3 scripts/veo_3_1.py submit \
  --shots-json '[{"id":"shot-1","prompt":"A golden retriever running on a beach at sunset, cinematic lighting","generationType":"TEXT_2_VIDEO","aspectRatio":"16:9"}]' \
  --resolution 720p
```

### Submit a reference-image shot and keep polling

```bash
python3 scripts/veo_3_1.py submit \
  --shots-json '[{"id":"shot-1","prompt":"The character comes alive, walking through a magical forest","generationType":"REFERENCE_2_VIDEO","aspectRatio":"16:9","imageUrls":["https://static.nanophoto.ai/demo/nano-banana-pro.webp"]}]' \
  --resolution 720p \
  --follow
```

### Check status of an existing job

```bash
python3 scripts/veo_3_1.py status \
  --task-ids-json '[{"shotId":"shot-1","taskId":"task_abc123"}]' \
  --resolution 720p
```

## Script behavior

The bundled script resolves credentials in this order: `--api-key`, then `NANOPHOTO_API_KEY` from the environment, then `~/.openclaw/openclaw.json` at `skills.entries.veo-3-1.env.NANOPHOTO_API_KEY`.

Subcommands:

- `submit`: submit a generation task
- `submit --follow`: submit and keep polling in the same process
- `status`: check an existing Veo generation

Cross-platform note:

- Use `python3` on macOS/Linux.
- Use `python` on Windows unless `python3` is available.
- The script uses Python's standard HTTP client and does not require `curl`.
- Use `--json-only` when another script/tool needs raw JSON output.
- Use `--poll-interval` to override the default 8-second polling interval.
- Default max wait is 1800 seconds.

## Manual API calls

### Submit generation

```bash
curl -X POST "https://nanophoto.ai/api/veo-3/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NANOPHOTO_API_KEY" \
  --data-raw '{
    "shots": [
      {
        "id": "shot-1",
        "prompt": "A golden retriever running on a beach at sunset, cinematic lighting",
        "generationType": "TEXT_2_VIDEO",
        "aspectRatio": "16:9"
      }
    ],
    "resolution": "720p"
  }'
```

### Check status

```bash
curl -X POST "https://nanophoto.ai/api/veo-3/check-status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NANOPHOTO_API_KEY" \
  --data-raw '{
    "taskIds": [
      {"shotId": "shot-1", "taskId": "task_abc123"}
    ],
    "resolution": "720p"
  }'
```

## Error handling

| errorCode | Cause | Action |
|-----------|-------|--------|
| `LOGIN_REQUIRED` | Invalid or missing API key | Verify key at https://nanophoto.ai/settings/apikeys |
| `API_KEY_RATE_LIMIT_EXCEEDED` | Rate limit exceeded | Wait and retry |
| `INSUFFICIENT_CREDITS` | Not enough credits | Top up credits |
| `SHOTS_REQUIRED` | Missing shots array | Build a valid shots payload |
| `PROMPT_REQUIRED` | Missing prompt in a shot | Add prompts to every shot |
| `INVALID_IMAGE_COUNT` | Wrong image count for generation type | Fix `imageUrls` for that shot type |
| `IMAGE_URLS_REQUIRED` | API needs public image URLs | Do not send local files or base64 |
| `GENERATION_FAILED` | Server-side generation error | Retry or simplify the shot prompts |
| `TASK_IDS_REQUIRED` | Missing task IDs | Pass valid `{shotId, taskId}` pairs |
| `TASK_NOT_FOUND` | Task not found or not owned by caller | Re-submit or verify ownership |
| `INTERNAL_ERROR` | Server-side failure | Retry later |

## Bundled files

- `scripts/veo_3_1.py`: single entry point for submit, status, and optional in-process polling
- `references/api.md`: condensed API reference, shot rules, and error behavior
