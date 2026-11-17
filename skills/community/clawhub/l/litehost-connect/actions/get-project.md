# Get Project

Retrieve full details for a single project.

## Endpoint

```
GET /v1/projects/{projectId}
```

## Parameters

| Field | Type | Required | Description |
|---|---|---|---|
| projectId | uuid | yes | Path parameter. |

## Example

```bash
curl https://connect.litehost.io/v1/projects/{projectId} \
  -H "Authorization: Bearer $LITEHOST_API_KEY"
```

## Success Response (200)

Returns the full project object:

```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "title": "My Project",
    "slug": "my-project",
    "type": "html",
    "url": "https://my-project.litepage.site",
    "status": "public",
    "access": "public",
    "domainId": null,
    "workspaceId": null,
    "noIndex": false,
    "disableDownloads": false,
    "pageTitle": null,
    "metaDescription": null,
    "analyticsEnabled": true,
    "expiresAt": null,
    "archivedAt": null,
    "createdAt": "...",
    "updatedAt": "..."
  }
}
```

## Error Handling

| Status | Action |
|---|---|
| 401 | Follow `utils/auth.md`. |
| 404 | Project not found. Verify the ID with the user or call `list-projects.md` to let them pick. |
