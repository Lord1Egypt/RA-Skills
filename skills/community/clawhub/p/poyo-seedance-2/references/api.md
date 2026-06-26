# PoYo Seedance 2 API Reference

## Endpoint

- Submit task: `https://api.poyo.ai/api/generate/submit`
- Status query: <https://docs.poyo.ai/api-manual/task-management/status>
- Source docs: <https://docs.poyo.ai/api-manual/video-series/seedance-2>
- Model page: <https://poyo.ai/models/seedance-2>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/video-series/seedance-2.json>

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

- `seedance-2` — standard Seedance 2 video generation model; supports `480p`, `720p`, and `1080p`
- `seedance-2-fast` — faster, lower-cost variant; supports `480p` and `720p` only

## Key input fields

- `model` (string, required) — choose `seedance-2` or `seedance-2-fast`
- `callback_url` (string, optional) — Webhook callback URL for result notifications
- `input.prompt` (string, required) — Text prompt describing the target video
- `input.resolution` (string, required) — `480p`, `720p`, `1080p`; use `1080p` only with `seedance-2`
- `input.duration` (integer, required) — Video duration in seconds, any integer from `4` to `15`
- `input.aspect_ratio` (string, optional) — `1:1`, `21:9`, `4:3`, `3:4`, `16:9`, `9:16`
- `input.image_urls` (string[], optional, max 2) — First and last frame images; index `0` is first frame, index `1` is last frame
- `input.reference_image_urls` (string[], optional) — Reference image URLs for multimodal reference-to-video mode
- `input.reference_video_urls` (string[], optional) — Reference video URLs for multimodal reference-to-video mode
- `input.reference_audio_urls` (string[], optional) — Reference audio URLs for multimodal reference-to-video mode
- `input.generate_audio` (boolean, optional) — Whether to generate an audio track
- `input.seed` (integer, optional) — Random seed for reproducible generation

## Important constraints

- `image_urls` and any `reference_*_urls` fields are mutually exclusive.
- `seedance-2-fast` uses the same input schema as `seedance-2`, but do not request `1080p` with it.
- Public media URLs must be directly downloadable by the upstream provider.
- Credits are calculated by duration and resolution; requests with `reference_video_urls` may have different final cost.

## Text-to-video example

```bash
curl -sS https://api.poyo.ai/api/generate/submit \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "seedance-2",
    "callback_url": "https://your-domain.com/callback",
    "input": {
      "prompt": "A cinematic drone shot flying over a neon city after rain, reflections shimmering on the streets",
      "aspect_ratio": "16:9",
      "resolution": "1080p",
      "duration": 5,
      "generate_audio": true,
      "seed": 42
    }
  }'
```

## First and last frame example

```bash
curl -sS https://api.poyo.ai/api/generate/submit \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "seedance-2",
    "callback_url": "https://your-domain.com/callback",
    "input": {
      "prompt": "A smooth transition from sunrise to golden afternoon over a mountain lake",
      "image_urls": [
        "https://example.com/first-frame.jpg",
        "https://example.com/last-frame.jpg"
      ],
      "aspect_ratio": "16:9",
      "resolution": "720p",
      "duration": 10,
      "generate_audio": false,
      "seed": 42
    }
  }'
```

## Multimodal reference example

```bash
curl -sS https://api.poyo.ai/api/generate/submit \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "seedance-2-fast",
    "callback_url": "https://your-domain.com/callback",
    "input": {
      "prompt": "A stylish fashion short with energetic pacing, matching the movement rhythm of the reference clip",
      "reference_image_urls": [
        "https://example.com/reference-image.jpg"
      ],
      "reference_video_urls": [
        "https://example.com/reference-video.mp4"
      ],
      "reference_audio_urls": [
        "https://example.com/reference-audio.mp3"
      ],
      "aspect_ratio": "9:16",
      "resolution": "720p",
      "duration": 5,
      "generate_audio": true,
      "seed": 42
    }
  }'
```

## Polling notes

- PoYo returns a `task_id` after submission.
- If `callback_url` is present, PoYo sends a POST callback when the task reaches `finished` or `failed`.
- Whether or not callbacks are used, the same unified task status docs apply: <https://docs.poyo.ai/api-manual/task-management/status>.

## Practical guidance

- Use `seedance-2` for `1080p`; use `seedance-2-fast` when latency or cost matters and `480p`/`720p` is enough.
- Prefer `image_urls` for exact first/last frame control.
- Prefer `reference_*_urls` for looser multimodal guidance from images, videos, or audio.
- Save the returned `task_id` immediately so status polling is straightforward.
