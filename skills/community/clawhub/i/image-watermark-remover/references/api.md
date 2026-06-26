# Image Watermark API Reference

## Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `https://nowatermark.info/api/image/remove-watermark` | Submit image watermark-removal job |
| `POST` | `https://nowatermark.info/api/jobs/query` | Query job status |

## Authentication

Send the API key in the `Authorization` header:

```text
Authorization: Bearer YOUR_API_KEY
```

## Input constraints

- `file_url` must be a valid `http` or `https` URL.
- Use a direct public image URL instead of a page URL.
- Supported formats: `jpg`, `jpeg`, `png`, `webp`, `heic`, `avif`, `bmp`, `tiff`.
- Prefer files at or under 10 MB.
- Query requests accept `request_id` and also tolerate `id`.

## Submit request

```json
{
  "file_url": "https://example.com/input.png"
}
```

Manual call:

```bash
curl -X POST "https://nowatermark.info/api/image/remove-watermark" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NOWATERMARK_API_KEY" \
  --data-raw '{"file_url":"https://example.com/input.png"}'
```

Submit response:

```json
{
  "success": true,
  "status": "processing",
  "request_id": "req_xxx"
}
```

## Query request

```json
{
  "request_id": "req_xxx"
}
```

Manual call:

```bash
curl -X POST "https://nowatermark.info/api/jobs/query" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NOWATERMARK_API_KEY" \
  --data-raw '{"request_id":"req_xxx"}'
```

Completed response:

```json
{
  "success": true,
  "status": "completed",
  "request_id": "req_xxx",
  "url": "https://cdn.nowatermark.info/result/clean-image.png",
  "outputs": [
    "https://cdn.nowatermark.info/result/clean-image.png"
  ]
}
```

Failed response:

```json
{
  "success": false,
  "status": "failed",
  "request_id": "req_xxx",
  "url": null,
  "outputs": []
}
```

## Polling guidance

- Poll every 3-5 seconds.
- Keep the same `request_id` for follow-up queries.
- Prefer the bundled Python script when the task needs submit-plus-poll behavior.

## Error codes

| Code | Meaning | Suggested action |
|------|---------|------------------|
| `LOGIN_REQUIRED` | Missing or invalid API key | Reconfigure `NOWATERMARK_API_KEY` |
| `INSUFFICIENT_CREDITS` | Account has no usable credits | Top up credits |
| `MISSING_FILE_URL` | Submit request omitted `file_url` | Ask for a public image URL |
| `INVALID_FILE_URL` | `file_url` is not a valid `http` or `https` URL | Replace with a direct public URL |
| `MISSING_REQUEST_ID` | Query request omitted `request_id` | Reuse or ask for the existing request id |
| `QUERY_FAILED` | Upstream status lookup failed | Retry with the same `request_id` |
| `GENERATION_FAILED` | Upstream removal request failed | Retry later or use a different image |
