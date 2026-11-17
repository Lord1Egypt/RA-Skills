# Archive Project

Archive a project to free quota without deleting it. Archived projects do NOT count toward project or storage limits. The project data is preserved and can be restored later.

## Endpoint

```
POST /v1/projects/{projectId}/archive
```

## Parameters

| Field | Type | Required | Description |
|---|---|---|---|
| projectId | uuid | yes | Path parameter. |

## Paid plan required

This endpoint is NOT available on the free tier. If the user is on the `free` plan, the API returns `403 FREE_TIER_RESTRICTED`. Direct them to upgrade at https://litehost.io/dashboard.

## When to use

- User hit project or storage limits and needs to free space
- User has unused or old projects they want to deactivate but keep
- As a quota-management step before creating or unarchiving another project

This endpoint is idempotent — calling it on an already-archived project returns success with no changes.

## Example

```bash
curl -X POST https://connect.litehost.io/v1/projects/{projectId}/archive \
  -H "Authorization: Bearer $LITEHOST_API_KEY"
```

## Success Response (200)

```json
{
  "status": "success",
  "data": { "archived": true }
}
```

## Error Handling

| Status | Action |
|---|---|
| 401 | Follow `utils/auth.md`. |
| 403 | Free-tier restricted. Requires paid plan. Tell user to upgrade. |
| 404 | Project not found. List projects and ask user to pick. |
