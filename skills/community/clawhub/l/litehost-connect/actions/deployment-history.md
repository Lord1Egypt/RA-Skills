# Deployment History

Retrieve all deployment versions for a project, newest first.

## Endpoint

```
GET /v1/projects/{projectId}/status
```

## Paid plan required

This endpoint is NOT available on the free tier. If the user is on the `free` plan, the API returns `403 FREE_TIER_RESTRICTED`. Direct them to upgrade at https://litehost.io/dashboard.

## Parameters

| Field | Type | Required | Description |
|---|---|---|---|
| projectId | uuid | yes | Path parameter. |

## Example

```bash
curl https://connect.litehost.io/v1/projects/{projectId}/status \
  -H "Authorization: Bearer $LITEHOST_API_KEY"
```

## Success Response (200)

```json
{
  "status": "success",
  "data": [
    {
      "deploymentId": "dep_v3",
      "version": 3,
      "status": "active",
      "sizeBytes": 204800,
      "createdAt": "..."
    },
    {
      "deploymentId": "dep_v2",
      "version": 2,
      "status": "ready",
      "sizeBytes": 198400,
      "createdAt": "..."
    }
  ]
}
```

`status` values: `active` (currently live), `ready` (previous version, kept in history).

## Error Handling

| Status | Action |
|---|---|
| 401 | Follow `utils/auth.md`. |
| 403 | Free-tier restricted. Requires paid plan. Tell user to upgrade. |
| 404 | Project not found. Verify the ID or list projects. |
