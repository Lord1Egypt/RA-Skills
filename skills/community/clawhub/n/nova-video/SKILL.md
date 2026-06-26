---
name: nova-video
description: Generate images or videos using the Nova Video OpenAPI with a single sentence. Use when the user wants to generate an image, create a video, check video generation status, or list past generations. Triggers on phrases like "generate image", "create video", "make a video", "generate a picture", "text to image", "text to video", "image generation", "video generation".
---

# Nova Video API

Generate images and videos via the Nova Video OpenAPI using `curl` commands.

> **Free tier**: Every user gets **60 free text-to-image generations per month** at no cost. No credit card required to get started.

## Install this skill

### Option 1 — Direct install (works in any AI agent)

Paste the following into your AI agent (Claude, Cursor, Codex, etc.):

```
Read https://nova-video.onesolo.app/SKILL.md and follow the instructions
```

The agent will fetch this file and activate the Nova Video skill automatically.

### Option 2 — Install via OpenClaw

If your agent supports the [OpenClaw](https://clawhub.ai) skill registry, run:

```
Read https://nova-video.onesolo.app/SKILL.md and follow the instructions
```

---

## Setup

Set your API key and base URL before starting:

```bash
export NOVA_API_KEY="nv_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export NOVA_BASE_URL="https://nova-video.onesolo.app"
```

If `NOVA_BASE_URL` is not set, use the default value `https://nova-video.onesolo.app`.

If `NOVA_API_KEY` is not set, guide the user to obtain one:

> **API Key required to continue**
>
> Follow these steps to get your Nova Video API Key:
>
> 1. Visit the Nova Video website: **https://nova-video.onesolo.app**
> 2. Register an account or log in
> 3. Go to **Profile** → **API Key** page
> 4. Create and copy your API Key (format: `nv_sk_...`)
> 5. Set the environment variable and then continue:
>    ```bash
>    export NOVA_API_KEY="nv_sk_your_key_here"
>    ```

Do not proceed with any API call until `NOVA_API_KEY` is confirmed.

---

## Workflow: One-sentence image generation

**User says**: "Generate an image of a sunset over the ocean"

**Steps**:

1. Call `POST /api/openapi/image` with the user's description as `prompt`
2. Return the `imageUrl` from the response

```bash
curl -s -X POST "$NOVA_BASE_URL/api/openapi/image" \
  -H "Authorization: Bearer $NOVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "<user description>",
    "size": "2k"
  }'
```

Response: `data.imageUrl` is the generated image URL.

---

## Workflow: Text-to-video (async)

**User says**: "Make a 6-second video of waves crashing on a beach"

**Steps**:

1. Generate a reference image from the user's description via `POST /api/openapi/image` → get `imageUrl`
2. Derive a concise **motion prompt** from the user's description (describe camera movement, subject action, atmosphere — keep it under 100 words)
3. Submit video task with `imageUrl` + motion prompt → get `taskId`
4. Poll status every **6 seconds** until `status` is `succeeded` or `failed`
5. Return `videoUrl` when done

> **Be patient**: Video generation typically takes several minutes and can take up to **15 minutes**. Keep polling — do not give up early or report a timeout. Only report failure if the task is still incomplete after 15 minutes of total waiting.

### Step 1 — Generate reference image

```bash
IMAGE_RESP=$(curl -s -X POST "$NOVA_BASE_URL/api/openapi/image" \
  -H "Authorization: Bearer $NOVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "<user description, detailed scene>",
    "size": "2k"
  }')

IMAGE_URL=$(echo $IMAGE_RESP | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['imageUrl'])")
echo "Reference image: $IMAGE_URL"
```

### Step 2 — Derive motion prompt

Based on the user's description, compose a motion prompt that describes **how the scene should move**. Examples:

| User description | Motion prompt |
|---|---|
| "waves crashing on a beach" | "Slow-motion ocean waves rolling in and crashing on the shore, seafoam spreading, gentle camera drift forward, cinematic" |
| "a forest at sunrise" | "Golden sunlight filtering through tree canopy, leaves swaying in a light breeze, slow push-in camera, atmospheric haze" |
| "a bustling city street at night" | "Neon signs reflecting on wet pavement, crowds moving in time-lapse, subtle handheld camera shake, cinematic noir" |

### Step 3 — Submit video task

```bash
VIDEO_RESP=$(curl -s -X POST "$NOVA_BASE_URL/api/openapi/video" \
  -H "Authorization: Bearer $NOVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "<motion prompt derived in Step 2>",
    "imageUrl": "'"$IMAGE_URL"'",
    "duration": 6,
    "aspectRatio": "16:9",
    "resolution": "720p"
  }')

TASK_ID=$(echo $VIDEO_RESP | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['taskId'])")
echo "Video task submitted: $TASK_ID"
```

> `imageUrl` accepts two formats:
> - A publicly accessible image URL, e.g. `https://example.com/photo.jpg`
> - A base64-encoded image, e.g. `data:image/jpeg;base64,/9j/4AAQ...`

Save `data.taskId` from the response.

### Step 4 — Poll status

```bash
curl -s "$NOVA_BASE_URL/api/openapi/video?taskId=<taskId>" \
  -H "Authorization: Bearer $NOVA_API_KEY"
```

Poll every **6 seconds**, up to **15 minutes** (150 attempts). Only consider it failed after exceeding the timeout. Stop when `data.status` is `succeeded` or `failed`.

| `data.status` | Meaning |
|---|---|
| `queued` | Waiting to start |
| `running` | Generating |
| `succeeded` | Done — use `data.videoUrl` |
| `failed` | Failed — show `data.error` |

> **Important: Prevent URL truncation**
>
> `videoUrl` is a long signed URL containing `X-Tos-*` query parameters. Outputting it directly in Claude Code will cause markdown rendering to truncate it.
> Always **write the full URL to a file** — never `echo` it directly or embed it in a markdown link:
>
> ```bash
> VIDEO_URL=$(echo $STATUS | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['videoUrl'])")
> echo "$VIDEO_URL" > video_url.txt
> echo "✅ Video ready. Full URL saved to video_url.txt"
> echo "--- URL preview (first 80 chars) ---"
> echo "${VIDEO_URL:0:80}..."
> ```
>
> Tell the user: "The full URL has been written to `video_url.txt`. Open that file and paste the link into your browser."

---

## API reference

### POST /api/openapi/image — Generate image

| Field | Type | Default | Description |
|---|---|---|---|
| `prompt` | string | required | Image description |
| `model` | string | `doubao-seedream-5-0-260128` | Model ID |
| `size` | string | `2k` | `2k` or `3k` |
| `imageCount` | number | `1` | Number of images (use `9` for 9-grid) |
| `image` | string\|string[] | — | Reference image (URL or base64) |
| `locale` | string | `zh` | `zh` or `en` |

**Response**:
```json
{
  "success": true,
  "data": {
    "imageUrl": "https://...",
    "taskId": "img_xxx",
    "model": "doubao-seedream-5-0-260128",
    "size": "2k",
    "imageCount": 1
  }
}
```

---

### POST /api/openapi/video — Submit video task

| Field | Type | Default | Description |
|---|---|---|---|
| `prompt` | string | required | Video description |
| `model` | string | `seedance-1.5-pro` | `seedance-1.5-pro` / `seedance-1.0-pro` / `seedance-1.0-lite` |
| `duration` | number | `6` | Duration in seconds (min 4) |
| `aspectRatio` | string | `16:9` | `16:9` / `9:16` / `1:1` |
| `resolution` | string | `720p` | `480p` / `720p` / `1080p` |
| `imageUrl` | string | required | Reference image (URL or base64) |
| `negativePrompt` | string | — | What to avoid |
| `seed` | number | — | Random seed |
| `cameraFixed` | boolean | `false` | Lock camera position |

**Response**:
```json
{
  "success": true,
  "data": {
    "taskId": "123456",
    "status": "PENDING",
    "model": "seedance-1.5-pro",
    "duration": 6,
    "aspectRatio": "16:9",
    "resolution": "720p"
  }
}
```

---

### GET /api/openapi/video?taskId=<id> — Query status

```bash
curl -s "$NOVA_BASE_URL/api/openapi/video?taskId=<taskId>" \
  -H "Authorization: Bearer $NOVA_API_KEY"
```

**Success response**:
```json
{
  "success": true,
  "data": {
    "taskId": "123456",
    "status": "succeeded",
    "videoUrl": "https://...",
    "coverUrl": "https://..."
  }
}
```

---

### GET /api/openapi/image — List image history

```bash
curl -s "$NOVA_BASE_URL/api/openapi/image?limit=10&offset=0" \
  -H "Authorization: Bearer $NOVA_API_KEY"
```

### GET /api/openapi/video — List video history

```bash
curl -s "$NOVA_BASE_URL/api/openapi/video?limit=10&offset=0" \
  -H "Authorization: Bearer $NOVA_API_KEY"
```

---

## Error handling

| HTTP | `error` value | Action |
|---|---|---|
| 401 | `Invalid API key` | Ask user to check `NOVA_API_KEY`; if not registered, direct them to https://nova-video.onesolo.app to sign up and get an API Key from the Profile page |
| 403 | `IMAGE_QUOTA_EXHAUSTED` / `VIDEO_QUOTA_EXHAUSTED` | Inform user quota is used up |
| 403 | `INSUFFICIENT_BALANCE` | Inform user wallet balance is low |
| 400 | `SENSITIVE_CONTENT` | Ask user to rephrase the prompt |
| 500 | any | Retry once; if still failing, report the error message |

---

## Examples

### Example 1 — Image from one sentence

> "Generate a cyberpunk-style cityscape at night"

```bash
curl -s -X POST "$NOVA_BASE_URL/api/openapi/image" \
  -H "Authorization: Bearer $NOVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Cyberpunk cityscape at night, neon reflections on rain-soaked streets, cinematic quality", "size": "2k"}'
```

### Example 2 — Text-to-video (full flow)

> "Make a 4-second aerial video of a mountain forest at sunrise"

```bash
# Step 1: Generate reference image from text
IMAGE_RESP=$(curl -s -X POST "$NOVA_BASE_URL/api/openapi/image" \
  -H "Authorization: Bearer $NOVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Aerial view of a mountain forest at sunrise, golden light filtering through trees, misty valleys, cinematic landscape photography", "size": "2k"}')

IMAGE_URL=$(echo $IMAGE_RESP | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['imageUrl'])")
echo "Reference image: $IMAGE_URL"

# Step 2: Submit video task with motion prompt
TASK=$(curl -s -X POST "$NOVA_BASE_URL/api/openapi/video" \
  -H "Authorization: Bearer $NOVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"Slow aerial drone flyover, golden sunrise light filtering through treetops, morning mist drifting through valleys, gentle camera push forward, cinematic\", \"imageUrl\": \"$IMAGE_URL\", \"duration\": 4, \"aspectRatio\": \"16:9\", \"resolution\": \"720p\"}")

TASK_ID=$(echo $TASK | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['taskId'])")
echo "Video task submitted: $TASK_ID"

# Step 3: Poll (max 15 minutes, every 6 seconds, 150 attempts)
MAX_ATTEMPTS=150
ATTEMPT=0
while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  ATTEMPT=$((ATTEMPT + 1))
  STATUS=$(curl -s "$NOVA_BASE_URL/api/openapi/video?taskId=$TASK_ID" \
    -H "Authorization: Bearer $NOVA_API_KEY")
  STATE=$(echo $STATUS | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['status'])")
  echo "[$ATTEMPT/$MAX_ATTEMPTS] Status: $STATE"
  if [ "$STATE" = "succeeded" ]; then
    VIDEO_URL=$(echo $STATUS | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['videoUrl'])")
    echo "$VIDEO_URL" > video_url.txt
    echo "✅ Video ready. Full URL saved to video_url.txt"
    echo "Preview (first 80 chars): ${VIDEO_URL:0:80}..."
    break
  elif [ "$STATE" = "failed" ]; then
    echo $STATUS | python3 -c "import sys,json; print('Error:', json.load(sys.stdin)['data'].get('error','unknown'))"
    break
  fi
  sleep 6
done
if [ $ATTEMPT -ge $MAX_ATTEMPTS ]; then
  echo "❌ Timed out after 15 minutes. Please check the task status or contact support. taskId: $TASK_ID"
fi
```

### Example 3 — Video with reference image

> "Generate a video from this image: https://example.com/photo.jpg"

```bash
curl -s -X POST "$NOVA_BASE_URL/api/openapi/video" \
  -H "Authorization: Bearer $NOVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "The scene comes alive with gentle motion",
    "imageUrl": "https://example.com/photo.jpg",
    "duration": 6,
    "aspectRatio": "16:9"
  }'
```
