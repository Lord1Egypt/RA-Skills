# Veo 3.1 API Reference

## Endpoints

- `POST https://nanophoto.ai/api/veo-3/generate`
- `POST https://nanophoto.ai/api/veo-3/check-status`

## Authentication

```text
Authorization: Bearer YOUR_API_KEY
```

For OpenClaw users, the recommended setup is:

- `env.NANOPHOTO_API_KEY=YOUR_API_KEY`
- Structured skill metadata should declare `requires.env=["NANOPHOTO_API_KEY"]` and `primaryEnv="NANOPHOTO_API_KEY"`

## Credits

| Resolution | Scope | Credits |
|------------|-------|---------|
| `720p` | per shot | 10 |
| `1080p` | single-shot only | 14 |
| `4k` | single-shot only | 30 |

Each shot generates an 8-second clip. Multi-shot outputs concatenate shots automatically.

## Generate request fields

| Field | Type | Required | Notes |
|------|------|----------|------|
| `shots` | object[] | Yes | Max 21 shots |
| `shots[].id` | string | Yes | Unique shot identifier |
| `shots[].prompt` | string | Yes | Shot prompt |
| `shots[].generationType` | string | Yes | `TEXT_2_VIDEO`, `FIRST_AND_LAST_FRAMES_2_VIDEO`, or `REFERENCE_2_VIDEO` |
| `shots[].aspectRatio` | string | Yes | `16:9` or `9:16` |
| `shots[].imageUrls` | string[] | Conditional | Public URLs only; required by image-based modes |
| `resolution` | string | No | `720p` default, `1080p`, `4k` |

## Generation type requirements

- `TEXT_2_VIDEO`: no images allowed
- `FIRST_AND_LAST_FRAMES_2_VIDEO`: 1-2 `imageUrls`
- `REFERENCE_2_VIDEO`: 1-3 `imageUrls`

## Status request fields

| Field | Type | Required | Notes |
|------|------|----------|------|
| `taskIds` | object[] | Yes | Array of `{shotId, taskId}` objects |
| `resolution` | string | No | `720p` default, `1080p`, `4k` |

## Polling behavior

- Poll every 5-10 seconds
- Typical generation time is 2-5 minutes per shot
- Multi-shot jobs take longer because shots run sequentially
- Credits are refunded automatically on failure

## Error codes

| errorCode | HTTP Status | Description |
|-----------|-------------|-------------|
| `LOGIN_REQUIRED` | 401 | Authentication required |
| `API_KEY_RATE_LIMIT_EXCEEDED` | 429 | Rate limit exceeded |
| `INSUFFICIENT_CREDITS` | 402 | Not enough credits |
| `SHOTS_REQUIRED` | 400 | Missing shots array |
| `PROMPT_REQUIRED` | 400 | Missing prompt in a shot |
| `INVALID_IMAGE_COUNT` | 400 | Wrong number of images for generation type |
| `IMAGE_URLS_REQUIRED` | 400 | API requires public `imageUrls` |
| `GENERATION_FAILED` | 500 | Video generation failed |
| `TASK_IDS_REQUIRED` | 400 | Missing task IDs |
| `TASK_NOT_FOUND` | 404 | Task not found or not owned by caller |
| `INTERNAL_ERROR` | 500 | Internal server error |

## Notes

- Base64 image upload is not supported via API
- Maximum total duration is 168 seconds (21 shots × 8 seconds)
- Use 1080p or 4k only for single-shot jobs
