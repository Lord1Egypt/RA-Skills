# Nano Banana API Reference

## Base URL

`https://www.nananobanana.com/api/v1`

## Authentication

Authenticated endpoints require:

```http
Authorization: Bearer nb_your_api_key_here
```

The key is shown only once at creation time.

## Endpoints

### `GET /models`

- Authentication: not required.
- Purpose: resolve the current model catalog.
- Recommendation: call this before passing an explicit `selectedModel`.

Live verification on 2026-03-25 returned model IDs including `gemini-2.5-flash-image`, `nanobanan-2`, `nanobanan-2-2k`, `seedream-5.0-2k`, and `nanobanan2&pro`. This differs from the static docs example that uses `nano-banana`, so treat `/models` as authoritative.

### `GET /credits`

- Authentication: required.
- Response shape:

```json
{
  "data": {
    "credits": 100
  }
}
```

### `POST /generate`

- Authentication: required.
- Core request fields:

```json
{
  "prompt": "Required prompt text",
  "selectedModel": "Optional model id from /models",
  "referenceImageUrls": ["Optional image URL"],
  "aspectRatio": "Optional aspect ratio",
  "mode": "sync | stream | async"
}
```

#### Sync

- `mode`: `sync` or omitted.
- Returns when generation completes.
- Best for: one-shot agent tasks and simple server-side integrations.

Common success shape:

```json
{
  "success": true,
  "generationId": "clxx...",
  "imageUrls": ["https://..."],
  "creditsUsed": 1,
  "remainingCredits": 99
}
```

#### Stream

- `mode`: `stream`
- Response content type: `text/event-stream`
- Event examples:

```text
data: {"type":"status","message":"Starting generation...","progress":0}
data: {"type":"status","message":"Processing...","progress":50}
data: {"type":"complete","message":"Generation complete","progress":100,"data":{"success":true,"imageUrls":["https://..."]}}
```

Expect `status`, `complete`, and `error` event types.

#### Async

- `mode`: `async`
- Submission returns immediately with a `generationId`.
- Poll with `GET /generate?id=<generationId>`.

Submission example:

```json
{
  "success": true,
  "async": true,
  "generationId": "clxx...",
  "message": "Generation started. Use GET /api/v1/generate?id={generationId} to poll for results.",
  "creditsUsed": 1,
  "remainingCredits": 99
}
```

### `GET /generate?id=<generationId>`

- Authentication: required.
- Purpose: inspect async job state or result.

Relevant `processingStatus` values:

- `processing`
- `completed`
- `failed`

Completion example:

```json
{
  "data": {
    "id": "clxx...",
    "prompt": "A landscape in ink wash style",
    "outputImageUrls": ["https://..."],
    "modelUsed": "nano-banana",
    "processingStatus": "completed",
    "creditsUsed": 1,
    "createdAt": "2025-01-01T00:00:00.000Z"
  }
}
```

## Request Mode Selection

- Use `sync` for the simplest agent execution path.
- Use `stream` when progress updates need to be surfaced live.
- Use `async` for long-running or queued work, especially when a turn should not block on submission.

## Errors

- `400 Bad Request`: invalid parameters such as missing `prompt` or invalid `mode`.
- `401 Unauthorized`: missing or invalid API key.
- `402 Payment Required`: insufficient credits.
- `403 Forbidden`: API access not enabled on the account.
- `500 Internal Server Error`: server-side failure.
- `503 Service Unavailable`: server busy. Docs note this is specific to async queue saturation.

## Operational Notes

- Generated image URLs expire after 15 days.
- Image-to-image inputs increase credit consumption.
- API access may require account enablement in addition to having a valid key.
- The published docs repo is useful for examples, but live endpoint behavior may change first. Verify unstable values through the API.
- Some CDN-protected image URLs may reject the default Python `urllib` user agent with `403`. The bundled CLI sends an explicit browser-like `User-Agent` for API requests and image downloads to avoid that failure mode.
