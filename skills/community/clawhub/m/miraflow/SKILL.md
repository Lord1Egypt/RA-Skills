---
name: miraflow
description: Create and manage AI videos and images using the Miraflow API. Use when a user asks to: generate an avatar video with a script, create a cinematic or AI video, generate or edit an AI image, list available avatars or voices, check video generation status, download a completed video, or upload media for use in Miraflow. Requires MIRAFLOW_API_KEY env var.
metadata: {"openclaw":{"config":{"requiredEnv":["MIRAFLOW_API_KEY"]}}}
---

# Miraflow

Miraflow is an AI video/image platform. The API is async — creation endpoints return a `jobId`, then you poll for completion.

**Base URL:** `https://miraflow.ai/api`  
**Auth:** always include `-H "x-api-key: $MIRAFLOW_API_KEY"` on every call. Never hardcode the key.

**Full API reference:** See `references/api.md` for endpoint details, request/response schemas, and the media upload workflow.

## Rules
- Never hardcode the API key. Always read from `$MIRAFLOW_API_KEY`.
- Always use `x-api-key` as the header name, not `Authorization`.
- After creating a video, always clearly state the `jobId` — the user needs it to check status.
- Do not auto-download a video without the user asking.
- Do not poll status in a loop. Check once, report the status, and tell the user to ask again if not ready.
- If an API call returns an error, show the status code and error message clearly.
- **NEVER retry `POST /api/video/create` or `POST /api/image/generate`.** These are expensive, non-idempotent operations. Call each creation endpoint **exactly once** per user request, even if the response is slow or unclear. If the call succeeds (any 2xx), stop — do not call again.
- **Always confirm before creating.** Before calling any creation endpoint, summarize what will be created (avatar, voice, name, script) and wait for the user to confirm. Only proceed after explicit confirmation.

## Core Workflows

### List Avatars
```
GET /api/avatars
```
Present as a numbered list with avatar name and ID.

### List Voices
```
GET /api/voices
```
Present as a numbered list with voice name and ID.

### Create an Avatar Video (voice + script)
1. If no `avatarId` given, list avatars and ask the user to pick one.
2. If no `voiceId` given, list voices and ask the user to pick one.
3. Ask for a video name if not provided.
4. **Before creating:** Confirm with the user — show avatar name, voice name, video name, and script. Wait for explicit approval.
5. Call `POST /api/video/create` **exactly once**:
```json
{
  "avatarId": "<id>",
  "voiceId": "<id>",
  "name": "<name>",
  "text": "<script>",
  "im2vid_full": true
}
```
6. Report the `jobId` clearly — the user needs it to check status later.
7. **Do not call create again** regardless of how long the response takes. If a timeout or error occurs, report it and let the user decide whether to retry.

**Note:** `im2vid_full: true` enables full-body animation on photo avatars. Omit for head-only.

### Check Video Status
```
GET /api/video/{jobId}/status
```
Translate status for the user:
- `inference_started` → "Queued, not started yet"
- `inference_working` → "In progress (X% complete)"
- `inference_complete` → "Ready! Use the jobId to fetch the download link."
- `inference_failed` → "Generation failed"
- `inference_error` → "Unknown error occurred"

### Fetch Video + Download Link
```
GET /api/video/{id}
```
Returns metadata including a signed `downloadUrl` (valid 24h). Share this directly with the user.

### Download a Video
```
GET /api/video/{id}/download
```
Save the response (video/mp4) to the current directory as `{video-name}.mp4`. Confirm the file path when done.

### Generate an AI Image
1. `POST /api/image/generate` with `prompt`, `name`, optional `aspectRatio` (`1:1` | `16:9` | `9:16` | `4:3` | `3:4`)
2. Poll `GET /api/image/{jobId}` until `inference_complete` → includes `downloadUrl`

### Edit an Image
1. Upload image via media upload workflow (see `references/api.md`)
2. `POST /api/image/edit` with `referenceImageMediaId`, `prompt`, `name`
3. Poll until complete

### Upload Media (audio or reference images)
See `references/api.md` → Media Upload Workflow (initialize → PUT to S3 → finalize)

## Error Handling
- `400` — bad request, invalid params, or insufficient credits
- `401` — missing/invalid API key (check `MIRAFLOW_API_KEY`)
- `404` — resource not found

Always show the status code and full error message when an API call fails.

## Credits

**Created by Katie Min** — designed and directed by Katie, built by **Claude Code** (AI coding agent by Anthropic), powered by **[OpenClaw](https://openclaw.ai)**.
