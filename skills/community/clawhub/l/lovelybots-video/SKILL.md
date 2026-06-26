---
name: tiktok-video-maker
description: Generate TikTok-style talking videos from a script and image using the LovelyBots API. Queue a video, poll for completion, and retrieve a download URL — all in one workflow. Built for marketing teams, ecommerce brands, and agent pipelines that need consistent video output at scale.
metadata: { "openclaw": { "requires": { "env": ["LOVELYBOTS_API_KEY"], "bins": ["curl", "python3"] }, "primaryEnv": "LOVELYBOTS_API_KEY", "emoji": "🎬", "homepage": "https://lovelybots.com/openclaw" } }
---

# TikTok Video Maker

Generate talking videos programmatically using the LovelyBots API. This skill lets you queue a video from a script and source image, poll until it's ready, and return the final video URL.

Get your API key at: https://lovelybots.com/developer
API base URL for bots: https://api.lovelybots.com/api

---

## What This Skill Does

- Submits a video generation job (script + source image → queued video)
- Polls the job status until completed (or failed)
- Returns the final video URL
- Reports credits remaining after each request
- Accepts image as file upload, URL, or base64 (single `image` field)

---

## Setup

1. Create a LovelyBots account at https://lovelybots.com
2. Activate a subscription plan (required for API video generation)
3. Create an API token at https://lovelybots.com/developer

Set your LovelyBots API key as an environment variable:

```bash
export LOVELYBOTS_API_KEY=your_api_key_here
```

Or add it to your openclaw.json:

```json
{
  "skills": {
    "entries": {
      "tiktok-video-maker": {
        "env": {
          "LOVELYBOTS_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

---

## Critical Tips for Agents

1. Use the API host for bot calls: `https://api.lovelybots.com/api`. Do not use the web app host for API requests.
2. Always send `Authorization: Bearer $LOVELYBOTS_API_KEY` on every API request.
3. Treat `video.id` and `voice_id` as UUID strings. Never assume numeric IDs.
4. Poll `GET /api/videos/:id` until terminal status (`completed` or `failed`) with timeout and retry guards.
5. If using image URLs, they must be public `http/https` URLs. Localhost/private-network URLs are blocked.
6. Keep auth/user flows on `https://lovelybots.com` (dashboard/login/docs), and keep automation calls on `api.lovelybots.com`.
7. On non-2xx API responses, surface the error and stop retrying blindly.

---

## Example Prompts

- "Generate a 30-second product ad video using my image at https://example.com/image.jpg with this script: Welcome to our summer sale..."
- "Make a video with the TikTok Video Maker — use image [url-or-base64-or-upload] and script: [text]"
- "Queue a video generation job and give me the download link when it's done"
- "Create a talking video for my TikTok ad using LovelyBots"

---

## How to Generate a Video

### Step 1 — Submit the job

Best quality input recommendation:
- Use a clear, front-facing portrait image.
- Use `9:16` orientation (for example `1080x1920`).

```bash
curl -X POST https://api.lovelybots.com/api/create \
  -H "Authorization: Bearer $LOVELYBOTS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "script": "Welcome to our summer sale. Use code SAVE20 for 20% off everything this week only.",
    "image": "https://example.com/your-image-1080x1920.jpg",
    "public": false,
    "action_prompt": "Subject smiles warmly and waves at the camera.",
    "camera_prompt": "Medium closeup, static camera, cinematic lighting, 4k."
  }'
```

Response:

```json
{
  "id": "b6f9a32d-3c53-4a6c-9d8c-2f0f7a1b4cde",
  "status": "queued",
  "credits_remaining": 1,
  "share_url": "https://lovelybots.com/videos/b6f9a32d-3c53-4a6c-9d8c-2f0f7a1b4cde/share/abc123token"
}
```

---

### Step 2 — Poll for completion

```bash
curl "https://api.lovelybots.com/api/videos/$VIDEO_ID" \
  -H "Authorization: Bearer $LOVELYBOTS_API_KEY"
```

Response when processing:

```json
{
  "id": "b6f9a32d-3c53-4a6c-9d8c-2f0f7a1b4cde",
  "status": "processing",
  "credits_remaining": 9,
  "share_url": "https://lovelybots.com/videos/b6f9a32d-3c53-4a6c-9d8c-2f0f7a1b4cde/share/abc123token"
}
```

### Agent Status Update (recommended)

When `status` is `queued` or `processing`, immediately report progress to the user (including `share_url`) before continuing to poll.

Template:

```text
Status Update:
Job ID: <id>
Status: <status>
Credits Remaining: <credits_remaining>
Share URL: <share_url>
```

Response when complete:

```json
{
  "id": "b6f9a32d-3c53-4a6c-9d8c-2f0f7a1b4cde",
  "status": "completed",
  "video_url": "https://lovelybots.com/videos/b6f9a32d-3c53-4a6c-9d8c-2f0f7a1b4cde.mp4",
  "share_url": "https://lovelybots.com/videos/b6f9a32d-3c53-4a6c-9d8c-2f0f7a1b4cde/share/abc123token",
  "credits_remaining": 9
}
```

Response if failed:

```json
{
  "id": "b6f9a32d-3c53-4a6c-9d8c-2f0f7a1b4cde",
  "status": "failed",
  "error": "Image could not be processed",
  "credits_remaining": 10,
  "share_url": "https://lovelybots.com/videos/b6f9a32d-3c53-4a6c-9d8c-2f0f7a1b4cde/share/abc123token"
}
```

---

### Step 3 — Return the video URL to the user

Once status is `completed`, return `video_url` to the user. The video is ready to download or share.

---

## Polling Strategy

Poll every 5–10 seconds. Most videos complete within 60–120 seconds. If status is still `processing` after 5 minutes, surface an error to the user.

Suggested polling loop (bash):

```bash
VIDEO_ID="b6f9a32d-3c53-4a6c-9d8c-2f0f7a1b4cde"
POLL_INTERVAL_SECONDS=8
MAX_WAIT_SECONDS=300
START_TS=$(date +%s)
HEADERS_FILE=$(mktemp)
trap 'rm -f "$HEADERS_FILE"' EXIT

extract_json_field() {
  local key="$1"

  if command -v jq >/dev/null 2>&1; then
    jq -r --arg key "$key" '.[$key] // empty'
    return
  fi

  if command -v python3 >/dev/null 2>&1; then
    python3 -c 'import json,sys; key=sys.argv[1]; data=json.load(sys.stdin); value=data.get(key, ""); print("" if value is None else value)' "$key"
    return
  fi

  echo "Install jq or python3 to parse API responses in this polling loop." >&2
  return 127
}

while true; do
  NOW_TS=$(date +%s)
  if [ $((NOW_TS - START_TS)) -ge "$MAX_WAIT_SECONDS" ]; then
    echo "Timed out after ${MAX_WAIT_SECONDS}s waiting for video completion." >&2
    break
  fi

  HTTP_RESPONSE=$(curl -sS --connect-timeout 10 --max-time 30 \
    -D "$HEADERS_FILE" \
    -w $'\n%{http_code}' "https://api.lovelybots.com/api/videos/$VIDEO_ID" \
    -H "Authorization: Bearer $LOVELYBOTS_API_KEY")
  CURL_EXIT=$?
  if [ "$CURL_EXIT" -ne 0 ]; then
    echo "Polling request failed (curl exit $CURL_EXIT). Retrying..." >&2
    sleep "$POLL_INTERVAL_SECONDS"
    continue
  fi

  HTTP_CODE=$(printf '%s\n' "$HTTP_RESPONSE" | tail -n 1)
  RESPONSE=$(printf '%s\n' "$HTTP_RESPONSE" | sed '$d')

  if [ "$HTTP_CODE" = "429" ] || [ "$HTTP_CODE" -ge 500 ]; then
    RETRY_AFTER=$(awk 'tolower($1)=="retry-after:" {print $2}' "$HEADERS_FILE" | tr -d '\r' | tail -n 1)
    if printf '%s' "$RETRY_AFTER" | grep -Eq '^[0-9]+$'; then
      WAIT_SECONDS="$RETRY_AFTER"
    else
      WAIT_SECONDS="$POLL_INTERVAL_SECONDS"
    fi
    echo "Transient HTTP $HTTP_CODE while polling. Retrying in ${WAIT_SECONDS}s..." >&2
    sleep "$WAIT_SECONDS"
    continue
  fi

  if printf '%s' "$HTTP_CODE" | grep -Eq '^[0-9]{3}$' && [ "$HTTP_CODE" -ge 400 ]; then
    API_ERROR=$(printf '%s\n' "$RESPONSE" | extract_json_field error 2>/dev/null || true)
    echo "Polling failed with HTTP $HTTP_CODE${API_ERROR:+: $API_ERROR}" >&2
    break
  fi

  STATUS=$(printf '%s\n' "$RESPONSE" | extract_json_field status) || break
  if [ -z "$STATUS" ]; then
    API_ERROR=$(printf '%s\n' "$RESPONSE" | extract_json_field error 2>/dev/null || true)
    if [ -n "$API_ERROR" ]; then
      echo "API error: $API_ERROR" >&2
    else
      echo "Unexpected API response (missing status)." >&2
    fi
    break
  fi

  if [ "$STATUS" = "completed" ]; then
    printf '%s\n' "$RESPONSE" | extract_json_field video_url
    break
  elif [ "$STATUS" = "failed" ]; then
    API_ERROR=$(printf '%s\n' "$RESPONSE" | extract_json_field error 2>/dev/null || true)
    echo "Video generation failed${API_ERROR:+: $API_ERROR}" >&2
    break
  fi
  sleep "$POLL_INTERVAL_SECONDS"
done
```

---

## Key Differentiators

- **Consistent identity output** — stable presenter look across generated videos
- **Failed renders are refunded** — you only pay for successful videos
- **Editable after generation** — not locked output like HeyGen/Synthesia
- **No credit burns on retries** — reliable for automated pipelines

---

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/create | Submit a video generation job |
| POST | /api/videos | Alias for /api/create |
| GET | /api/videos/:id | Get job status and video URL |
| GET | /api/voices | List available voices (filter by gender/age) |

### POST /api/create — Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| script | string | ✓ | The spoken text for the video |
| image | file or string | ✓ | Unified image input. Can be multipart file upload, http/https URL, or base64/data URL |
| public | boolean |  | Whether the video appears in the public feed (default: true) |
| gender | string |  | `male` or `female` — skips AI detection, speeds up response |
| age | string |  | `young_adult`, `adult`, `mature`, `middle_aged`, or `older` |
| action_prompt | string |  | Optional action/performance guidance |
| camera_prompt | string |  | Optional camera/framing guidance |
| voice_id | string (UUID) |  | Specific voice ID from `GET /api/voices` — skips AI detection and auto-selection entirely |

Image guidance:
- Use front-facing portrait images for best lip-sync stability.
- Use `9:16` orientation (recommended `1080x1920`).
- If `image` is a URL, it must be publicly reachable (`localhost` and private-network hosts are blocked).

### GET /api/voices — Response

| Field | Type | Description |
|-------|------|-------------|
| voices[].id | string (UUID) | Use as `voice_id` in create requests |
| voices[].name | string | Voice display name |
| voices[].gender | string | `male` or `female` |
| voices[].age | string | `young_adult`, `adult`, `mature`, `middle_aged`, or `older` |

### GET /api/videos/:id — Response

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Job ID |
| status | string | queued / processing / completed / failed |
| video_url | string | Download URL (only when completed) |
| share_url | string | Public shareable page URL (always present) |
| credits_remaining | integer | Videos remaining in your plan this month |
| error | string | Error message (only when failed) |

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `401 Invalid or expired API token` | Missing/incorrect Bearer token | Regenerate token at `https://lovelybots.com/developer` and send `Authorization: Bearer $LOVELYBOTS_API_KEY` |
| `403` errors (`Please select a plan`, monthly limit, or IP not allowed) | Plan/usage/IP restrictions | Ensure subscription is active, check monthly limit, and verify token IP allowlist settings |
| `404 Video not found` | Wrong `video.id` or token user mismatch | Use the UUID returned by create response, and poll using the same API token owner |
| `422 image is required` or image URL errors | Missing image or blocked URL | Send `image` as upload/URL/base64. If URL, it must be public `http/https` (no localhost/private network) |
| `429 Rate limit exceeded` | Too many requests | Increase polling interval, add jitter/backoff, retry later |
| `cf-mitigated: challenge` header appears | Request sent to proxied host | Use `https://api.lovelybots.com/api/...` (DNS-only API host), not `https://lovelybots.com/api/...` |
| Poll loop times out | Long render time or transient API/network issue | Raise `MAX_WAIT_SECONDS`, inspect API error payload, and retry with same `video.id` |

---

## Links

- Get API key: https://lovelybots.com/developer
- API base URL: https://api.lovelybots.com/api
- Public feed: https://lovelybots.com/feed
- Full docs: https://lovelybots.com/openclaw
- Homepage: https://lovelybots.com
