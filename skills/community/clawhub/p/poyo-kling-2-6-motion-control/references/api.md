# PoYo Kling 2 6 Motion Control API Reference

## Endpoint

- Submit task: `https://api.poyo.ai/api/generate/submit`
- Status query: <https://docs.poyo.ai/api-manual/task-management/status>
- Source docs: <https://docs.poyo.ai/api-manual/video-series/kling-2.6-motion-control>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/video-series/kling-2.6-motion-control.json>

## Auth

Send:

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Get API keys from <https://poyo.ai/dashboard/api-key>.

Recommended skill env var:

- `POYO_API_KEY`

## Models

- `kling-2.6-motion-control` — motion transfer and character animation

## Key input fields

- `model` (string, required) — choose one of the documented model ids
- `callback_url` (string, optional) — Webhook callback URL for result notifications
- `character_orientation` (string, required) — Character orientation mode: 'image' matches the person's orientation in the photograph (max 10 seconds output), 'video' maintains consistency with character orientation from the reference video (max 30 seconds output) options: image, video
- `video_urls` (string[], required) — Single reference video URL for motion transfer (MP4, MOV, MKV, max 100MB, 3-30 seconds). Must clearly show the subject's head, shoulders, and torso
- `prompt` (string, optional) — Text description of the desired output scene (optional)
- `image_urls` (string[], required) — Single character image URL (JPEG, PNG, WEBP, max 10MB). Must clearly show the subject's head, shoulders, and torso
- `resolution` (string, required) — Output video resolution. 720p for standard quality, 1080p for higher visual quality options: 720p, 1080p

## Submission example

```bash
curl -sS https://api.poyo.ai/api/generate/submit   -H 'Authorization: Bearer YOUR_API_KEY'   -H 'Content-Type: application/json'   -d '{
  "model": "kling-2.6-motion-control",
  "callback_url": "https://your-domain.com/callback",
  "input": {
    "prompt": "The cartoon character is dancing gracefully in a studio",
    "image_urls": [
      "https://example.com/character-image.jpg"
    ],
    "video_urls": [
      "https://example.com/dance-reference.mp4"
    ],
    "character_orientation": "video",
    "resolution": "1080p"
  }
}'
```

## Polling notes

- PoYo returns a `task_id` after submission.
- If `callback_url` is present, PoYo sends a POST callback when the task reaches `finished` or `failed`.
- Whether or not callbacks are used, the same unified task status docs apply: <https://docs.poyo.ai/api-manual/task-management/status>.

## Practical guidance

- Respect the documented image count limit: `image_urls` allows up to 1 item(s).
- Use a supported `resolution`: 720p, 1080p.
- Save the returned `task_id` immediately so status polling is straightforward.
