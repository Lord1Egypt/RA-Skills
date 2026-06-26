# Output Schema Reference

This document describes the JSON output schema produced by `scripts/pangolin.py`.

## Envelope Structure

All output follows one of two envelope formats: **success** or **error**.

### Success Envelope

Printed to **stdout** when the API returns a successful response (code 0).

```json
{
  "success": true,
  "task_id": "<string>",
  "results_num": "<int>",
  "ai_overview_count": "<int>",
  "ai_overview": [ ... ],
  "organic_results": [ ... ],
  "screenshot": "<string>"
}
```

### Error Envelope

Printed to **stderr** when any error occurs (network, auth, API, etc.).

```json
{
  "success": false,
  "error": {
    "code": "<string>",
    "message": "<string>",
    "hint": "<string>"
  }
}
```

## Success Fields

| Field | Type | Guaranteed | Description |
|-------|------|------------|-------------|
| `success` | boolean | Yes | Always `true` for successful responses |
| `task_id` | string | Yes | Unique Pangolin task identifier |
| `results_num` | int | Yes | Total number of result items returned |
| `ai_overview_count` | int | Yes | Number of AI overview blocks (0 if none) |
| `ai_overview` | array | No | Present only if AI overviews exist |
| `organic_results` | array | No | Present only if organic results exist |
| `screenshot` | string | No | Screenshot URL; present only if `--screenshot` was passed |

### `ai_overview[]` Item

Each AI overview block contains the AI-generated content and its source references.

| Field | Type | Guaranteed | Description |
|-------|------|------------|-------------|
| `content` | string[] | Yes | Array of AI-generated text paragraphs |
| `references` | array | Yes | Array of source references (may be empty) |

### `ai_overview[].references[]` Item

| Field | Type | Guaranteed | Description |
|-------|------|------------|-------------|
| `title` | string | Yes | Source page title |
| `url` | string | Yes | Source page URL |
| `domain` | string | Yes | Source domain name |

### `organic_results[]` Item

Each organic result represents a traditional Google search result link.

| Field | Type | Guaranteed | Description |
|-------|------|------------|-------------|
| `title` | string | Yes | Result page title |
| `url` | string | Yes | Result page URL |
| `text` | string | No | Result snippet text (may be null) |

## Error Fields

| Field | Type | Guaranteed | Description |
|-------|------|------------|-------------|
| `success` | boolean | Yes | Always `false` for error responses |
| `error.code` | string | Yes | Machine-readable error code |
| `error.message` | string | Yes | Human-readable error description |
| `error.hint` | string | No | Suggested resolution (present for most errors) |

### Error Codes

| Code | Trigger |
|------|---------|
| `MISSING_ENV` | No credentials found in environment or cache |
| `AUTH_FAILED` | Email/password authentication rejected |
| `RATE_LIMIT` | HTTP 429 from the API |
| `NETWORK` | Connection timeout, DNS failure, or other network error |
| `SSL_CERT` | SSL certificate verification failed (common on macOS) |
| `API_ERROR` | Non-zero response code from Pangolin API |

## Mode Differences

### AI Mode (`--mode ai-mode`)

- Typically returns `ai_overview` with rich AI-generated content
- `organic_results` may or may not be present
- Supports `--follow-up` for multi-turn dialogue

### SERP Mode (`--mode serp`)

- Returns `organic_results` with traditional search results
- `ai_overview` may be present if Google generated one for the query
- Does **not** support `--follow-up`

## Auth-Only Output

When using `--auth-only`, the output is a simplified success object:

```json
{
  "success": true,
  "message": "Authentication successful",
  "token_preview": "eyJhbGci...ab1c"
}
```

The `token_preview` shows only the first 8 and last 4 characters -- the full token is never printed.

## Raw Mode

When using `--raw`, the output is the unprocessed Pangolin API response. The structure matches the Pangolin API documentation in `references/ai-mode-api.md` and `references/ai-overview-serp-api.md`. The envelope structure described above does **not** apply in raw mode.

## Example Files

See `references/examples/` for complete example outputs:

- `ai-mode-example.json` -- AI Mode search result
- `serp-example.json` -- Standard SERP search result
