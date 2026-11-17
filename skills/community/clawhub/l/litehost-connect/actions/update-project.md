# Update Project Settings

Change metadata and configuration of an existing project without re-uploading files.

## Endpoint

```
PATCH /v1/projects/{projectId}
Content-Type: application/json
```

## Paid plan required

This endpoint is NOT available on the free tier. If the user is on the `free` plan, the API returns `403 FREE_TIER_RESTRICTED`. Direct them to upgrade at https://litehost.io/dashboard.

## When to use

Use this when the user wants to change project settings: title, slug, visibility, password, domain, SEO fields, expiry, analytics, or workspace assignment.

DO NOT use this to upload new files. Use `replace-project.md` for that.

## Parameters

Send only the fields you want to change. All fields are optional.

| Field | Type | Description |
|---|---|---|
| title | string | New display name. 1–255 chars. |
| slug | string | New URL slug. Lowercase alphanumeric + hyphens. 1–255 chars. |
| domainId | uuid or null | Assign a custom domain. Set `null` to remove. |
| status | string | `public` or `private`. |
| access | string | `public`, `password`, or `private`. |
| password | string or null | Required when access is `password`. Set `null` to clear. |
| noIndex | boolean | `true` adds a noindex meta tag so search engines skip the page. |
| disableDownloads | boolean | `true` hides the download button on viewer pages. |
| pageTitle | string or null | Custom browser tab title. `null` falls back to project title. |
| metaDescription | string or null | SEO meta description for search engines and link previews. `null` to clear. |
| expiresIn | string | `15m`, `1h`, `24h`, `7d`, or `none`. `none` removes existing expiry. |
| analyticsEnabled | boolean | Enable or disable page view tracking. |
| workspaceId | uuid or null | Move to a workspace. `null` moves to personal scope. |

## Example — make project private

```bash
curl -X PATCH https://connect.litehost.io/v1/projects/{projectId} \
  -H "Authorization: Bearer $LITEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"access": "private"}'
```

## Example — set password protection

```bash
curl -X PATCH https://connect.litehost.io/v1/projects/{projectId} \
  -H "Authorization: Bearer $LITEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"access": "password", "password": "secret123"}'
```

## Example — assign custom domain

```bash
curl -X PATCH https://connect.litehost.io/v1/projects/{projectId} \
  -H "Authorization: Bearer $LITEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domainId": "domain-uuid-here"}'
```

## Example — set SEO fields

```bash
curl -X PATCH https://connect.litehost.io/v1/projects/{projectId} \
  -H "Authorization: Bearer $LITEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"pageTitle": "My Custom Title", "metaDescription": "A brief description for search engines.", "noIndex": false}'
```

## Success Response (200)

```json
{
  "status": "success",
  "data": { "updated": true }
}
```

## Error Handling

| Status | Code | Action |
|---|---|---|
| 401 | — | Follow `utils/auth.md`. |
| 403 | `FREE_TIER_RESTRICTED` | Requires paid plan. Tell user to upgrade at https://litehost.io/dashboard. |
| 404 | — | Project not found. List projects and ask user to pick. |
| 409 | — | Slug already taken. Ask user for a different slug and retry. |
| 422 | — | Validation failed. Check field values against the parameter table and retry. |
