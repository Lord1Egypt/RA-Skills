# Create Project

Deploy a new project to Litehost.

## Endpoint

```
POST /v1/projects
Content-Type: multipart/form-data
```

## Pre-flight

ALWAYS call `GET /v1/user` before creating. Check `quota.projects` and `quota.storage`. If either limit is reached, follow `utils/quotas.md`. DO NOT attempt the create until quota is available.

## Parameters

| Field | Type | Required | Description |
|---|---|---|---|
| title | string | yes | Project display name. |
| files | file[] | yes | One or more files to upload. |
| slug | string | no | URL slug. Auto-generated from title if omitted. Lowercase alphanumeric with hyphens only. |
| domainId | uuid | no | Assign a custom domain. The slug becomes a subdomain of that domain. |
| workspaceId | uuid | no | Assign to a workspace. |
| access | string | no | `public` (default), `password`, or `private`. |
| password | string | no | Required when access is `password`. Max 255 chars. |
| expiresIn | string | no | `15m`, `1h`, `24h`, or `7d`. Project becomes inaccessible after this duration. |
| zipIndexHtmlPath | string | no | Path to homepage inside a ZIP when it contains multiple HTML files (e.g. `dist/index.html`). |
| asFileBundle | boolean | no | Set `true` to skip HTML detection and force file-bundle mode. |

## Example

```bash
curl -X POST https://connect.litehost.io/v1/projects \
  -H "Authorization: Bearer $LITEHOST_API_KEY" \
  -F "title=My Project" \
  -F "files=@index.html"
```

## Example — ZIP with multiple HTML files

```bash
curl -X POST https://connect.litehost.io/v1/projects \
  -H "Authorization: Bearer $LITEHOST_API_KEY" \
  -F "title=My App" \
  -F "files=@dist.zip" \
  -F "zipIndexHtmlPath=dist/index.html"
```

## Success Response (201)

```json
{
  "status": "success",
  "data": {
    "projectId": "uuid",
    "url": "https://my-project.litepage.site",
    "title": "My Project",
    "type": "html",
    "slug": "my-project",
    "expiresAt": null,
    "createdAt": "...",
    "quota": {
      "projects": { "used": 4, "limit": 10, "unlimited": false },
      "storage": { "usedBytes": 10485760, "limitBytes": 2147483648, "unlimited": false }
    }
  }
}
```

## Error Handling

| Status | Code | Action |
|---|---|---|
| 400 | `ZIP_MULTIPLE_HTML` | Response includes `htmlPaths` array. Present the paths to the user, ask which is the homepage, retry with `zipIndexHtmlPath`. |
| 401 | — | Follow `utils/auth.md`. |
| 403 | `PROJECT_LIMIT_REACHED` | Follow `utils/quotas.md`. |
| 403 | `STORAGE_LIMIT_REACHED` | Follow `utils/quotas.md`. |

## Output

ALWAYS return the `url` and `projectId` from the response to the user.
