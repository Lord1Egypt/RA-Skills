# Troubleshooting

LinkedIn's error messages are famously misleading — "unauthorized" rarely means "bad token." Before guessing, always look at the response body's `serviceErrorCode` and `message` fields, then match against this table.

## Authentication and authorization

### `401 Unauthorized` with `"message": "Not enough permissions"`

The token is valid but lacks `w_organization_social`. Either:
- Community Management API hasn't been approved for your app yet (see `setup.md` step 2), or
- The OAuth flow didn't include `w_organization_social` in the `scope` parameter. Re-run `get_token.py` — it requests that scope explicitly.

### `401 Unauthorized` with `"code": "INVALID_CREDENTIAL"`

Token expired (60-day lifetime) or revoked. Use the refresh token to mint a new one — see `setup.md` for the snippet.

### `403 Forbidden` with `"message": "Not authorized to perform this action"`

The authenticated user is not an admin of the target Company Page. Being a content admin or an employee is not enough — you need the full admin role. Check `https://www.linkedin.com/company/<id>/admin/settings/manage-admins/`.

### `403 Forbidden` when calling a versioned endpoint

Missing the `LinkedIn-Version` or `X-Restli-Protocol-Version` header. The client in this skill always sends them, so if you see this, you're probably calling LinkedIn directly instead of through `LinkedInClient`.

## Content and shape errors

### `400 Bad Request` with `"message": "Invalid content format"`

The `content` field shape doesn't match the expected schema for the post kind. Common culprits:
- Using `content.media.id` (singular) for a carousel — use `content.multiImage.images[].id`.
- Passing a person URN as `author` on an org-scoped post. The token and the author must be consistent.
- Including a `media` block with a URN that's still processing (video) — see below.

### `422 Unprocessable Entity` with a length message

Post commentary exceeded 3,000 characters. The library checks locally before calling, so if you see this, you're bypassing `_envelope`. Trim and retry.

### Post publishes but the image/video is broken in the feed

The media URN wasn't ready when the post was created. For images this is rare but possible; for videos it's common if you skip the poll.

Fix: for videos, always pass `poll=True` to `upload_video` (the default). If you're calling the API directly, `GET /rest/videos/{urn}` until `status == AVAILABLE` before creating the post.

### Article link preview is blank or says "Preview not available"

LinkedIn couldn't scrape the URL's OpenGraph metadata. Check:
- `<meta property="og:title">`, `og:description`, `og:image` are present on the target page.
- The target page is publicly reachable (not behind auth, no aggressive bot-blocking).
- The `og:image` URL is absolute and returns `image/*` content.

You can override `title` and `description` in `post_article`, but `og:image` specifically must come from the target page.

## Media upload errors

### `initializeUpload` returns `400` with `"fileSizeBytes is required"`

Videos always need `fileSizeBytes` in the request. The helper in `lib/media.py` reads this from the file on disk; if you're calling directly, pass the exact `os.path.getsize(path)`.

### Multipart video finalize fails with `"ETag mismatch"`

One of the chunk uploads didn't return an ETag, or the ETags were recorded out of order. The order of `uploadedPartIds` in `finalizeUpload` must match the order of `uploadInstructions` from `initializeUpload`.

### Upload PUT returns `403` with an XML error body

The upload URL expired (15-minute lifetime) or was used twice. Re-run `initializeUpload` to get a fresh one — they're not reusable.

### Image rejected with "pixel count exceeds limit"

LinkedIn caps images at ~36 megapixels. Resize before uploading. Width × height, not file size.

## Rate limiting

### `429 Too Many Requests`

The per-member daily quota is roughly 100 calls. If you're scheduling, queue the posts and spread them out. The response includes a `Retry-After` header — honor it.

## Dev-only: fake/stale tokens

LinkedIn's OAuth tool at https://www.linkedin.com/developers/tools/oauth/token-generator issues tokens that are quick to obtain but miss some scopes. If you grabbed a token there and it behaves oddly, re-run `get_token.py` to get a full 3-legged token instead.

## Last-resort debugging

When nothing in this list matches, gather:

1. The exact request body (from `--dry-run` or by logging the call).
2. The full response body, not just the status code.
3. A fresh `curl` that reproduces the issue, so you can share it without leaking app secrets.

Then compare the request shape against the current LinkedIn docs at:
- Posts: https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api
- Images: https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/images-api
- Videos: https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/videos-api

LinkedIn ships monthly versions; if the docs for your `LINKEDIN_API_VERSION` say something different from what the client expects, the version header is likely out of sync with the docs you're reading.
