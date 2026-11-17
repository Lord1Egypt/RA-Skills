# Push New Version

Upload new content to an existing project. Replaces all live files and increments the deployment version. Previous versions are kept in history. The project URL does NOT change.

## Endpoint

```
PUT /v1/projects/{projectId}
Content-Type: multipart/form-data
```

## Paid plan required

This endpoint is NOT available on the free tier. If the user is on the `free` plan, the API returns `403 FREE_TIER_RESTRICTED`. Direct them to upgrade at https://litehost.io/dashboard.

## When to use

Use this when the user wants to update the **files** of an existing project (redeploy, push new build, replace content).

DO NOT use this to change settings (title, slug, visibility, domain). Use `update-project.md` for that.

## Parameters

| Field | Type | Required | Description |
|---|---|---|---|
| projectId | uuid | yes | Path parameter. The project to update. |
| files | file[] | yes | New files to upload. Replaces all existing content. |
| zipIndexHtmlPath | string | no | Homepage path inside a ZIP when it contains multiple HTML files. |
| asFileBundle | boolean | no | Set `true` to force file-bundle mode. |

## Resolving projectId

If the user does not provide a project ID:

1. Call `GET /v1/projects` to list their active projects.
2. Present the list showing titles and URLs.
3. Ask which project to update.
4. Use the selected project's `id`.

## Example

```bash
curl -X PUT https://connect.litehost.io/v1/projects/{projectId} \
  -H "Authorization: Bearer $LITEHOST_API_KEY" \
  -F "files=@dist.zip" \
  -F "zipIndexHtmlPath=dist/index.html"
```

## Success Response (200)

```json
{
  "status": "success",
  "data": {
    "deploymentId": "dep_v2",
    "url": "https://my-project.litepage.site"
  }
}
```

## Error Handling

| Status | Code | Action |
|---|---|---|
| 400 | `ZIP_MULTIPLE_HTML` | Response includes `htmlPaths`. Present paths, ask which is the homepage, retry with `zipIndexHtmlPath`. |
| 401 | — | Follow `utils/auth.md`. |
| 403 | `FREE_TIER_RESTRICTED` | Requires paid plan. Tell user to upgrade at https://litehost.io/dashboard. |
| 404 | — | Project not found. List projects and ask user to pick again. |

## Output

ALWAYS return the `url` and `deploymentId` to the user.
