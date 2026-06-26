---
name: oatda-video-status
description: Check the status of an asynchronous video generation task from OATDA. Triggers when the user wants to check if a video is done generating, retrieve the video URL after completion, or poll the status of a video task by its task ID. Use after oatda-generate-video to get results.
homepage: https://oatda.com
metadata:
  {
    "openclaw":
      {
        "emoji": "📹",
        "requires": { "bins": ["curl", "jq"], "env": ["OATDA_API_KEY"], "config": ["~/.oatda/credentials.json"] },
        "primaryEnv": "OATDA_API_KEY",
      },
  }
---

# OATDA Video Status

Check the status of asynchronous video generation tasks. Companion to `oatda-generate-video`.

## API Key Resolution

All commands need the OATDA API key. Resolve it inline for each `exec` call:

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}"
```

If the key is empty or `null`, tell the user to get one at https://oatda.com and configure it.

**Security**: Never print the full API key. Only verify existence or show first 8 chars.

## Prerequisites

The user must provide a task ID from a previous `oatda-generate-video` call. If they don't have one, tell them to generate a video first.

## API Call

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X GET "https://oatda.com/api/v1/llm/video-status/<TASK_ID>" \
  -H "Authorization: Bearer $OATDA_API_KEY"
```

Replace `<TASK_ID>` with the actual task ID. URL-encode if it contains special characters.

## Response Format

```json
{
  "taskId": "minimax-T2V01-abc123def456",
  "status": "completed",
  "videoUrl": "https://cdn.example.com/video.mp4",
  "directVideoUrl": "https://cdn.example.com/video-direct.mp4",
  "provider": "minimax",
  "model": "T2V-01",
  "createdAt": "2026-01-15T10:30:00Z",
  "completedAt": "2026-01-15T10:32:15Z",
  "costs": {
    "totalCost": 0.05,
    "currency": "USD"
  }
}
```

## Status Handling

| Status | What to tell the user |
|--------|----------------------|
| `pending` | "Your video is queued and hasn't started yet. Check again in a minute." |
| `processing` | "Your video is being generated. Check again in a minute." |
| `completed` | "Your video is ready!" — show `videoUrl` (or `directVideoUrl`). Mention cost if available. |
| `failed` | "Video generation failed." — show `errorMessage` if present. Suggest retrying with different prompt. |

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 401 | Invalid API key | Tell user to check their key |
| 404 | Task not found | Verify task ID is correct. Tasks may expire. |
| 429 | Rate limited | Wait and retry |

## Example

User: "Check status of video task minimax-T2V01-abc123"

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X GET "https://oatda.com/api/v1/llm/video-status/minimax-T2V01-abc123" \
  -H "Authorization: Bearer $OATDA_API_KEY"
```

If completed: "Your video is ready! Download: `<videoUrl>` — Cost: $0.05"
If processing: "Still generating. Try again in about a minute."

## Notes

- This is a GET request — no request body needed
- Video generation typically takes 30 seconds to 5 minutes
- Video URLs may be temporary — recommend downloading promptly
- If `processing`, suggest waiting 30-60 seconds before rechecking
- Use `oatda-generate-video` to start a new video generation
