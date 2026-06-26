# Nano Banana 2 API Reference

## Endpoints

- `POST https://nanophoto.ai/api/nano-banana-2/generate`
- `POST https://nanophoto.ai/api/nano-banana-2/check-status`

## Authentication

```text
Authorization: Bearer YOUR_API_KEY
```

For OpenClaw users, the recommended setup is:

- `env.NANOPHOTO_API_KEY=YOUR_API_KEY`
- Structured skill metadata should declare `requires.env=["NANOPHOTO_API_KEY"]` and `primaryEnv="NANOPHOTO_API_KEY"`

## Credits

| Quality | Credits |
|---------|---------|
| `1K` | 4 |
| `2K` | 8 |
| `4K` | 16 |

Credits are pre-deducted and refunded automatically if generation fails.

## Generate request fields

| Field | Type | Required | Notes |
|------|------|----------|------|
| `prompt` | string | Yes | Image generation prompt |
| `mode` | string | Yes | `generate` or `edit` |
| `aspectRatio` | string | No | `16:9`, `9:16`, `4:3`, `3:4`; default `16:9` |
| `imageQuality` | string | No | `1K`, `2K`, `4K`; default `1K` |
| `googleSearch` | boolean | No | Prompt enhancement via Google Search; default `false` |
| `inputImageUrls` | string[] | Conditional | Required for `edit`; public URLs only; max 14 |

## Status response behavior

- Generation is asynchronous
- Poll every 3-5 seconds
- Typical generation time is 10-30 seconds
- Status usually moves `pending` → `generating` → `completed` or `failed`

## Error codes

| errorCode | HTTP Status | Description |
|-----------|-------------|-------------|
| `LOGIN_REQUIRED` | 401 | Authentication required |
| `API_KEY_RATE_LIMIT_EXCEEDED` | 429 | Rate limit exceeded |
| `INSUFFICIENT_CREDITS` | 402 | Not enough credits |
| `INVALID_PROMPT` | 400 | Prompt is missing or empty |
| `MISSING_INPUT_IMAGE` | 400 | Edit mode requires input images |
| `TOO_MANY_IMAGES` | 400 | More than 14 input images |
| `IMAGE_URLS_REQUIRED` | 400 | API requires `inputImageUrls` for edit mode |
| `CREDIT_RESERVATION_FAILED` | 500 | Failed to reserve credits |
| `GENERATION_FAILED` | 500 | Image generation failed |
| `NOT_FOUND` | 404 | Generation ID not found |
| `FORBIDDEN` | 403 | Access denied |

## Notes

- API edit mode accepts only public `inputImageUrls`
- Base64 image upload is not supported via API
- Use `googleSearch: true` only when web context is likely to improve the result
