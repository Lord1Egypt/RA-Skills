---
name: keevx-video-translate
description: Translate videos into a specified target language using the Keevx API. Supports audio-only translation, subtitle generation, and dynamic duration adjustment. Use this skill when the user needs to (1) Translate/dub a video (2) Translate a video from one language to another (3) Query the list of supported translation languages (4) Check the status of a video translation task. Keywords video translate, Keevx, dubbing.
---

# Keevx Video Translation Skill

Translate videos into a specified target language via the Keevx API, with support for voice replacement and subtitle generation. Only one target language per translation request.

## Prerequisites

Set the environment variable `KEEVX_API_KEY`, obtained from https://www.keevx.com/main/home.

```bash
export KEEVX_API_KEY="your_api_key_here"
```

## Authentication

- Translation endpoints: `Authorization: Bearer $KEEVX_API_KEY`
- Upload endpoint: `token: $KEEVX_API_KEY`

## API Endpoints

Base URL: `https://api.keevx.com/v1`

- Upload file: `POST /figure-resource/upload/file` (used for local files)
- Query supported languages: `GET /video_translate/target_languages`
- Submit translation task: `POST /video_translate`
- Query task status: `GET /video_translate/{task_id}`

## Video Input Handling

The user's video input may be a URL or a local file path. Handle them differently:

- **If it is a URL** (starts with `http://` or `https://`): Use it directly as `video_url`
- **If it is a local file path**: First call the upload endpoint to get a URL, then use the returned URL for subsequent steps

### Upload Local File

```bash
curl --location 'https://api.keevx.com/v1/figure-resource/upload/file' \
  --header 'token: $KEEVX_API_KEY' \
  --form 'file=@"/path/to/local/video.mp4"'
```

Response format:

```json
{
  "code": 0,
  "success": true,
  "message": { "global": "success" },
  "result": {
    "url": "https://storage.googleapis.com/.../video.mp4",
    "fileId": "c5a4676a-...",
    "fileName": "video.mp4"
  }
}
```

Extract the video URL from `result.url` and use it as the `video_url` value in subsequent requests.

## Core Workflow

### 1. Query Supported Target Languages

```bash
curl -X GET "https://api.keevx.com/v1/video_translate/target_languages" \
  -H "Authorization: Bearer $KEEVX_API_KEY"
```

Response example:

```json
{"code": 0, "msg": "success", "data": ["English", "Chinese", "Japanese", "Korean"]}
```

### 2. Submit Translation Task

```bash
curl -X POST "https://api.keevx.com/v1/video_translate" \
  -H "Authorization: Bearer $KEEVX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "target_languages": ["English"],
    "video_url": "https://example.com/video.mp4",
    "speaker_num": 1,
    "translate_audio_only": true,
    "enable_dynamic_duration": true,
    "enable_caption": false,
    "name": "my-video-translate",
    "callback_url": "https://your-server.com/callback"
  }'
```

Response example: Returns a task_id

```json
{
  "code": 0,
  "msg": "ok",
  "data": [
    {"task_id": "vt-d6b6472bcf724d0399e06d1390cb964e", "language": "English"}
  ]
}
```

**IMPORTANT: After the task is submitted successfully, you MUST immediately display the following message to the user (this must be shown for every task, never omit it):**

> The task has been submitted successfully. Your task_id is `{task_id}`.
> If the task is interrupted later (e.g., network timeout, session disconnected), you can say to me at any time: **"Re-check the status of this video translation task"**, and provide the task_id: `{task_id}`, to resume querying until the task completes or fails, without resubmitting the translation task.

### 3. Poll Task Status

After the translation task is submitted successfully and the task_id message above has been shown to the user, immediately begin polling the task status. When the user later says "Re-check the status of this video translation task" and provides a task_id, use that task_id directly to call the query endpoint to resume polling, without resubmitting the translation task.

```bash
curl -X GET "https://api.keevx.com/v1/video_translate/{task_id}" \
  -H "Authorization: Bearer $KEEVX_API_KEY"
```

Response format:

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "task_id": "vt-d6b6472bcf724d0399e06d1390cb964e",
    "name": "English-my-video-translate",
    "language": "English",
    "status": "SUCCEEDED",
    "video_url": "https://storage.googleapis.com/.../sample_0.mp4",
    "caption_url": "https://storage.googleapis.com/.../sample_0.ass",
    "error_message": ""
  }
}
```

Status values: `PENDING` (queued) / `PROCESSING` (in progress) / `SUCCEEDED` (completed) / `FAILED` (failed)

Key fields on success:
- `video_url`: Download URL for the translated video
- `caption_url`: Download URL for the subtitle file (.ass format, only available when enable_caption=true)

## Request Parameters

- `target_languages` (required): Target language array, pass only one language, e.g. `["English"]`, value from the supported languages list
- `video_url` (required): URL of the video to translate
- `speaker_num` (optional): Number of speakers in the video, default 1, set to 0 for auto-detection
- `translate_audio_only` (optional): Translate audio track only (ignore face), default true
- `enable_dynamic_duration` (optional): Dynamically adjust video duration to match target language speech rate, default true
- `enable_caption` (optional): Whether to generate subtitles, default false
- `name` (optional): Video name, less than 100 characters. Translated video is named: target_language + "-" + name
- `callback_url` (optional): Callback URL for task completion

## Callback Notification

If a `callback_url` is provided when submitting the task, the system will send a POST request to that URL upon task completion:

```json
{
  "code": 0,
  "msg": "ok",
  "task_type": "video_translate",
  "data": {
    "task_id": "vt-d6b6472bcf724d0399e06d1390cb964e",
    "name": "English-my-video-translate",
    "language": "English",
    "status": "SUCCEEDED",
    "video_url": "https://storage.googleapis.com/.../sample_0.mp4",
    "caption_url": "https://storage.googleapis.com/.../sample_0.ass",
    "error_message": ""
  }
}
```

Callback field descriptions:
- `code`: Status code, 0 means success
- `task_type`: Fixed as `video_translate`
- `data.task_id`: Task ID
- `data.language`: Target language
- `data.status`: `SUCCEEDED` or `FAILED`
- `data.video_url`: Translated video URL (on success)
- `data.caption_url`: Subtitle file URL (on success, if subtitles enabled)
- `data.error_message`: Error message (on failure)

## Error Codes

- `200`: Success
- `400`: Invalid parameters
- `401`: Authentication failed
- `429`: Rate limit exceeded
- `500`: Internal server error

## Full Translation Workflow Script

The following bash script implements the full workflow: submit translation task + poll task status. Requires `jq`.

Usage: `bash translate.sh "https://example.com/video.mp4" "English" [speaker_num]`

Supports local files: `bash translate.sh "/path/to/video.mp4" "English"`

```bash
#!/bin/bash
# Full video translation workflow: submit task + poll status

# Configuration
API_KEY="${KEEVX_API_KEY:?Please set the KEEVX_API_KEY environment variable first}"
API_BASE="https://api.keevx.com/v1"

# Parameters
VIDEO_INPUT="${1:?Usage: bash translate.sh <video_url_or_path> <target_language> [speaker_num]}"
TARGET_LANG="${2:?Usage: bash translate.sh <video_url_or_path> <target_language> [speaker_num] (e.g. English)}"
SPEAKER_NUM="${3:-1}"

# Determine if input is a URL or local file; upload local files first
if [[ "$VIDEO_INPUT" == http://* ]] || [[ "$VIDEO_INPUT" == https://* ]]; then
  VIDEO_URL="$VIDEO_INPUT"
else
  if [ ! -f "$VIDEO_INPUT" ]; then
    echo "File not found: $VIDEO_INPUT"
    exit 1
  fi
  echo "Uploading local video: $VIDEO_INPUT"
  UPLOAD_RESPONSE=$(curl -s --location "$API_BASE/figure-resource/upload/file" \
    --header "token: $API_KEY" \
    --form "file=@\"$VIDEO_INPUT\"")

  UPLOAD_SUCCESS=$(echo "$UPLOAD_RESPONSE" | jq -r '.success')
  if [ "$UPLOAD_SUCCESS" != "true" ]; then
    echo "Upload failed:"
    echo "$UPLOAD_RESPONSE" | jq .
    exit 1
  fi

  VIDEO_URL=$(echo "$UPLOAD_RESPONSE" | jq -r '.result.url')
  echo "Upload succeeded, video URL: $VIDEO_URL"
fi

# Step 1: Submit translation task
echo "Submitting video translation task..."
echo "  Video: $VIDEO_URL"
echo "  Target language: $TARGET_LANG"
echo "  Speaker count: $SPEAKER_NUM"

RESPONSE=$(curl -s -X POST "$API_BASE/video_translate" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"target_languages\": [\"$TARGET_LANG\"],
    \"video_url\": \"$VIDEO_URL\",
    \"speaker_num\": $SPEAKER_NUM,
    \"translate_audio_only\": true,
    \"enable_dynamic_duration\": true,
    \"enable_caption\": false
  }")

CODE=$(echo "$RESPONSE" | jq -r '.code')
if [ "$CODE" != "0" ]; then
  echo "Task submission failed:"
  echo "$RESPONSE" | jq .
  exit 1
fi

TASK_ID=$(echo "$RESPONSE" | jq -r '.data[0].task_id')
echo "Task submitted successfully: $TASK_ID"

# Step 2: Poll task status
MAX_RETRIES=240
INTERVAL=30

echo ""
echo "Starting to poll task status (interval ${INTERVAL}s, max ${MAX_RETRIES} attempts)..."

for i in $(seq 1 $MAX_RETRIES); do
  STATUS_RESPONSE=$(curl -s -X GET "$API_BASE/video_translate/$TASK_ID" \
    -H "Authorization: Bearer $API_KEY")
  STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.data.status')

  if [ "$STATUS" = "SUCCEEDED" ]; then
    VIDEO_RESULT=$(echo "$STATUS_RESPONSE" | jq -r '.data.video_url')
    CAPTION_RESULT=$(echo "$STATUS_RESPONSE" | jq -r '.data.caption_url')
    echo "[$TARGET_LANG] Translation succeeded!"
    echo "  Video: $VIDEO_RESULT"
    [ "$CAPTION_RESULT" != "null" ] && [ -n "$CAPTION_RESULT" ] && echo "  Subtitles: $CAPTION_RESULT"
    exit 0
  elif [ "$STATUS" = "FAILED" ]; then
    ERROR_MSG=$(echo "$STATUS_RESPONSE" | jq -r '.data.error_message')
    echo "[$TARGET_LANG] Translation failed: $ERROR_MSG"
    exit 1
  else
    echo "[$i/$MAX_RETRIES] $TARGET_LANG: $STATUS"
  fi

  sleep $INTERVAL
done

echo ""
echo "Maximum wait time reached (2 hours). The task may still be processing."
echo "Please visit https://www.keevx.com/main/meta/creations to check and retrieve results."
```

## Notes

- Only one target language per request. For multiple languages, submit separate tasks
- Video translation may take up to 2 hours. Recommended polling: 30-second intervals, up to 240 attempts
- If polling times out, direct the user to https://www.keevx.com/main/meta/creations to retrieve results
- After the task is submitted and a task_id is obtained, you MUST immediately and explicitly show the task_id to the user, and inform them that if an interruption occurs they can say "Re-check the status of this video translation task" with the task_id to resume querying. This message must not be omitted for any task
- Generated video/subtitle URLs are retained for only 7 days; download promptly

## Related Links

- [Official API Docs - Supported Languages](https://docs.keevx.com/api-reference/endpoint/ListSupportedLanguages)
- [Official API Docs - Submit Translation](https://docs.keevx.com/api-reference/endpoint/SubmitVideoTranslate)
- [Official API Docs - Check Status](https://docs.keevx.com/api-reference/endpoint/GetTranslationStatus)
