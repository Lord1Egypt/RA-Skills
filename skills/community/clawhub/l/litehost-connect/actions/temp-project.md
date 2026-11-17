# Temporary Project

Upload files and get a live URL instantly — no API key, no sign-in, no code. The project expires in
15 minutes unless the user keeps it with `claimUrl`.

## When to use

- There is no saved key (`scripts/litehost.sh session` returns `NO_SAVED_KEY`) — this is the
  default path, do not start a sign-in first
- The user wants a link fast, a preview, or a one-off share

If a key is saved, use `create-project.md` instead.

---

## Create Temporary Project

```
POST /v1/projects/temp
Content-Type: multipart/form-data
```

No authentication required.

### Limits

- Max 5 files per request
- Total upload size: 2 MB
- Rate limit: 3 uploads/minute, 5 uploads/hour per IP

### Parameters

| Field | Type | Required | Description |
|---|---|---|---|
| files | file[] | yes | One or more files (max 5, total 2 MB). |
| zipIndexHtmlPath | string | no | Homepage path inside a ZIP when it contains multiple HTML files. |
| asFileBundle | boolean | no | Set `true` to force file-bundle mode. |

### Example

```bash
scripts/litehost.sh temp index.html style.css
```

Equivalent curl:

```bash
curl -X POST https://connect.litehost.io/v1/projects/temp \
  -F "files=@index.html" -F "files=@style.css"
```

### Response (200)

```json
{
  "status": "success",
  "data": {
    "projectId": "uuid",
    "slug": "blue-fox-42",
    "url": "https://blue-fox-42.litepage.site",
    "claimToken": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "claimUrl": "https://litehost.io/claim/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "expiresAt": "2026-04-03T01:30:00.000Z"
  }
}
```

After a successful upload, tell the user right away:

> Your link is live: {url}
> It lasts 15 minutes. To keep it, open {claimUrl} and sign in (Google or email) — it moves to your
> Litehost account.

That is all. Do not start a sign-in yourself to claim it: the user claims it in the browser.

---

## Claim Temporary Project (only if a key is already saved)

If `scripts/litehost.sh session` succeeds, you can claim it for the user instead of sending
`claimUrl`. Never sign in just to claim — `claimUrl` does that without a code.

```
POST /v1/projects/claim/{claimToken}
```

Requires authentication (Bearer token).

Permanently transfers the temp project to the user's account.

- The 15-minute expiry is removed on every plan, Free included.
- On Free, the link stays online while it's opened at least once every 90 days.

### Pre-flight

Check quota via `GET /v1/user` before claiming. The API rejects with 403 if project or storage limits would be exceeded.

### Example

```bash
scripts/litehost.sh api POST /v1/projects/claim/{claimToken}
```

### Response (200)

```json
{
  "status": "success",
  "data": {
    "projectId": "uuid",
    "slug": "blue-fox-42",
    "url": "https://blue-fox-42.litepage.site",
    "expiresAt": "2026-04-10T01:15:00.000Z"
  }
}
```

`expiresAt` is `null` after a claim.

### Error Handling

| Status | Code | Action |
|---|---|---|
| 400 | `ZIP_MULTIPLE_HTML` | Present `htmlPaths` to user, retry with `zipIndexHtmlPath`. |
| 401 | `API_KEY_*` | Follow `utils/auth.md`. Or just give the user `claimUrl`. |
| 403 | `PROJECT_LIMIT_REACHED` | Follow `utils/quotas.md`. |
| 403 | `STORAGE_LIMIT_REACHED` | Follow `utils/quotas.md`. |
| 404 | — | Claim token not found or expired. The temp project is gone. |
| 409 | `ALREADY_CLAIMED` | Project was already claimed. No action needed. |
| 429 | `RATE_LIMITED` | Wait `retryAfterSeconds` (5 anonymous uploads per hour per IP). |
