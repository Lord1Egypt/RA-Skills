# Errors

## Response Formats

| Code | Body |
|------|------|
| `400` | `{"status": 400, "error": "Bad Request", "message": "..."}` |
| `401` | `{"error": "Invalid API key"}` |
| `404` | `{"error": "Not found"}` |
| `422` | `{"errors": ["Validation error message"]}` |

## Common Status Codes

- `400 Bad Request` — malformed request, e.g. missing `placement_id` on a stats request for a placement network (Facebook/LinkedIn/Telegram).
- `401 Unauthorized` — missing or invalid `POSTPROXY_API_KEY`. Check the `Authorization: Bearer` header.
- `404 Not Found` — resource doesn't exist or belongs to a different profile group.
- `405 Method Not Allowed` — the action isn't supported for this profile's network (e.g. liking a comment on Instagram, replying to profile comments on a non-Google-Business profile).
- `422 Unprocessable Entity` — validation failure. Common cases:
  - "Post cannot be edited" — post is published or within 5 minutes of scheduled publish time
  - "Profile not found for {id}"
  - "Invalid platform params for {network}: {key}"
  - Thread creation with an unsupported platform (only Twitter, Threads, Bluesky)
  - `delete_on_platform` scoped to `instagram` or `tiktok` (not supported)
  - DM API used on an unsupported platform (only Facebook, Instagram, Telegram, Bluesky)
  - More than one `media` attachment on a DM send
  - Missing `parent_id` when replying to a Google Business review

## Async Failure Statuses

Write operations on comments, profile comments, DMs, and platform deletions are asynchronous. Instead of an HTTP error, failures surface as resource statuses:

- `failed_waiting_for_retry` — the platform call failed; Postproxy will retry with backoff. `error_message` is populated.
- `failed` — retries exhausted; the operation failed permanently.
- `inactive_profile_error` — the profile's credentials are no longer valid (e.g. Telegram bot kicked or token revoked); the profile is deactivated and must be reconnected.

Poll the resource or subscribe to the corresponding `*.failed` / `*.failed_waiting_for_retry` webhook events (see [webhooks.md](webhooks.md)).

## Platform Rate Limits

Social networks have rate limits that Postproxy handles automatically. If a post hits a platform rate limit, Postproxy queues it and retries when possible.
