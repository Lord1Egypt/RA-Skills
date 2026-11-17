# List Projects

Retrieve the user's projects with optional filters.

## Endpoint

```
GET /v1/projects
```

## Query Parameters

| Param | Type | Default | Description |
|---|---|---|---|
| workspaceId | uuid | — | Filter by workspace. |
| archived | string | `false` | `true` = only archived. `false` = only active. `all` = both. |
| limit | integer | 50 | Max results per page. Range: 1–100. |
| offset | integer | 0 | Pagination offset. |

## Example — list active projects

```bash
curl https://connect.litehost.io/v1/projects \
  -H "Authorization: Bearer $LITEHOST_API_KEY"
```

## Example — list archived projects

```bash
curl "https://connect.litehost.io/v1/projects?archived=true" \
  -H "Authorization: Bearer $LITEHOST_API_KEY"
```

## Example — filter by workspace

```bash
curl "https://connect.litehost.io/v1/projects?workspaceId={workspaceId}" \
  -H "Authorization: Bearer $LITEHOST_API_KEY"
```

## Success Response (200)

```json
{
  "status": "success",
  "data": {
    "projects": [
      {
        "id": "uuid",
        "title": "My Project",
        "slug": "my-project",
        "type": "html",
        "url": "https://my-project.litepage.site",
        "status": "public",
        "access": "public",
        "createdAt": "...",
        "updatedAt": "..."
      }
    ],
    "limit": 50,
    "offset": 0
  }
}
```

## Pagination

If the returned array length equals `limit`, there may be more results. Increment `offset` by `limit` and call again. Repeat until the array is shorter than `limit`.

## Error Handling

| Status | Action |
|---|---|
| 401 | Follow `utils/auth.md`. |
