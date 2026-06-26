# Nano Banana Pro Image Generation API Reference

## Endpoints

- `POST https://nanophoto.ai/api/nano-banana-pro/generate`
- `POST https://nanophoto.ai/api/nano-banana-pro/check-status`

## Authentication

```text
Authorization: Bearer YOUR_API_KEY
```

For OpenClaw users, the recommended setup is:

- `env.NANOPHOTO_API_KEY=YOUR_API_KEY`

## Modes

- `generate` for text-to-image
- `edit` for image-to-image

## Generate request fields

| Field | Type | Required | Notes |
|------|------|----------|------|
| `prompt` | string | Yes | Main image prompt |
| `mode` | string | Yes | `generate` or `edit` |
| `aspectRatio` | string | No | `16:9`, `9:16`, `4:3`, `3:4` |
| `imageQuality` | string | No | `1K`, `2K`, `4K` |
| `inputImageUrls` | string[] | Conditional | Required for `edit`; max 8 public URLs |

## Important limitations

- API calls accept only `inputImageUrls` for edit mode.
- Base64 image upload is not supported by the API.
- Maximum 8 input images.

## Credits

| Quality | Credits |
|---------|---------|
| `1K` | 4 |
| `2K` | 8 |
| `4K` | 16 |

Credits are pre-deducted and automatically refunded if generation fails.

## Initial generate response

```json
{
  "success": true,
  "generationId": "abc123xyz",
  "taskId": "task-456",
  "status": "pending"
}
```

Poll using `generationId`.

## Completed status

```json
{
  "success": true,
  "status": "completed",
  "imageUrl": "https://static.nanophoto.ai/generations/abc123.jpg",
  "generationId": "abc123xyz",
  "progress": 100
}
```

## Failed status

```json
{
  "success": false,
  "status": "failed",
  "error": "Generation failed",
  "generationId": "abc123xyz",
  "progress": 0
}
```

## Polling guidance

- Poll every 3-5 seconds
- In practice, generation may take roughly 30-300 seconds depending on queue/load and prompt complexity
- Status flow: `pending` → `generating` → `completed` or `failed`
- For Windows compatibility, prefer the bundled Python script over shell-specific curl snippets

## Error codes

| errorCode | Meaning |
|-----------|---------|
| `LOGIN_REQUIRED` | Authentication required |
| `API_KEY_RATE_LIMIT_EXCEEDED` | Rate limit exceeded |
| `INSUFFICIENT_CREDITS` | Not enough credits |
| `INVALID_PROMPT` | Prompt missing or empty |
| `MISSING_INPUT_IMAGE` | Edit mode requires images |
| `TOO_MANY_IMAGES` | More than 8 input images |
| `IMAGE_URLS_REQUIRED` | API requires public `inputImageUrls` |
| `CREDIT_RESERVATION_FAILED` | Failed to reserve credits |
| `GENERATION_FAILED` | Image generation failed |
| `NOT_FOUND` | Generation ID not found |
| `FORBIDDEN` | Access denied |
