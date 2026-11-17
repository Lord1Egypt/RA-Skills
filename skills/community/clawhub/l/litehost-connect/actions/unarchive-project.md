# Unarchive Project

Restore an archived project to active status.

## Endpoint

```
POST /v1/projects/{projectId}/unarchive
```

## Parameters

| Field | Type | Required | Description |
|---|---|---|---|
| projectId | uuid | yes | Path parameter. |

## Paid plan required

This endpoint is NOT available on the free tier. If the user is on the `free` plan, the API returns `403 FREE_TIER_RESTRICTED`. Direct them to upgrade at https://litehost.io/dashboard.

## Pre-flight

ALWAYS call `GET /v1/user` before unarchiving. Verify the user has room in both project count AND storage limits. If either would be exceeded, follow `utils/quotas.md` before attempting. The API rejects with 403 if limits are exceeded.

This endpoint is idempotent — calling it on an already-active project returns success with no changes.

## Example

```bash
curl -X POST https://connect.litehost.io/v1/projects/{projectId}/unarchive \
  -H "Authorization: Bearer $LITEHOST_API_KEY"
```

## Success Response (200)

```json
{
  "status": "success",
  "data": { "archived": false }
}
```

## Error Handling

| Status | Code | Action |
|---|---|---|
| 401 | — | Follow `utils/auth.md`. |
| 403 | `FREE_TIER_RESTRICTED` | Requires paid plan. Tell user to upgrade at https://litehost.io/dashboard. |
| 403 | `PROJECT_LIMIT_REACHED` | Follow `utils/quotas.md`. |
| 403 | `STORAGE_LIMIT_REACHED` | Follow `utils/quotas.md`. |
| 404 | — | Project not found. List archived projects with `?archived=true` and ask user to pick. |
