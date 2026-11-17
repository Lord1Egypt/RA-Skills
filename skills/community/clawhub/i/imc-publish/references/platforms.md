# Platform notes

Server-side validation is fail-closed: if a platform rejects the payload or
doesn't support scheduling, the draft/confirm call returns a clear 4xx — relay
it to the user.

| Platform | Required | Notes |
|---|---|---|
| instagram | caption | Feed post by default. Video: mp4. |
| tiktok | caption | Defaults to public visibility. Photo posts and videos supported. |
| facebook | caption | Posts to the account's **default Page** unless a `page_id` is passed in the target: `{"platform":"facebook","account_id":"...","page_id":"1234567890"}`. Pages are listed by `accounts`. |
| youtube | caption + **title** | `--title` is mandatory. |
| linkedin | caption | Personal profile by default. |
| threads | caption | Text-first; media optional. |
| google | caption + media | Google Business Profile post. |
| telegram | caption + explicit target | Must pass a target with the group chat id: `{"platform":"telegram","account_id":"...","platform_data":{"chat_id":"-100123456789"}}`. Telegram publishes immediately (no scheduling) and must be the only platform in its draft. |

## Media

- Images: jpg / png / webp / gif. Videos: mp4.
- Media must be uploaded via the `upload` command first — the API only accepts
  its own hosted URLs.
- Identical files dedupe to the same URL (content-addressed) — re-uploading is
  harmless.

### File size

Large files are uploaded straight to object storage rather than through the
API, so multi-megabyte images and videos are fine. A 3.38MB image was verified
end-to-end on 2026-08-05. `upload` accepts up to 100MB.

Per-platform limits still apply (each platform enforces its own duration,
dimension, and size rules) — a rejection at draft time names the platform and
the reason; relay it to the user.

## Scheduling

- `--schedule` takes RFC3339 UTC (`2026-08-01T09:00:00Z`), at least 5 minutes
  ahead.
- Scheduling support varies by platform; unsupported combinations are rejected
  at draft time with an explanation.

## Limits

- Your workspace plan includes a monthly publishing quota; exceeding it returns
  a clear error.
- There is a daily safety cap per workspace (default 30 posts/day).
