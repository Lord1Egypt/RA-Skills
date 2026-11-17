# Workspaces

Create and manage workspaces to organize projects into groups.

**Paid plan required.** All workspace endpoints return `403 FREE_TIER_RESTRICTED` for free-tier users.

---

## List Workspaces

```
GET /v1/workspaces
```

```bash
curl https://connect.litehost.io/v1/workspaces \
  -H "Authorization: Bearer $LITEHOST_API_KEY"
```

### Response (200)

```json
{
  "status": "success",
  "data": {
    "workspaces": [
      {
        "id": "uuid",
        "name": "My Team",
        "projectCount": 5,
        "createdAt": "...",
        "updatedAt": "..."
      }
    ]
  }
}
```

---

## Create Workspace

```
POST /v1/workspaces
Content-Type: application/json
```

| Field | Type | Required | Description |
|---|---|---|---|
| name | string | yes | Display name. 1–255 chars. |

```bash
curl -X POST https://connect.litehost.io/v1/workspaces \
  -H "Authorization: Bearer $LITEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Team"}'
```

---

## Rename Workspace

```
PATCH /v1/workspaces/{workspaceId}
Content-Type: application/json
```

| Field | Type | Required | Description |
|---|---|---|---|
| name | string | yes | New name. 1–255 chars. |

```bash
curl -X PATCH https://connect.litehost.io/v1/workspaces/{workspaceId} \
  -H "Authorization: Bearer $LITEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Name"}'
```

---

## Delete Workspace

```
DELETE /v1/workspaces/{workspaceId}
```

Projects inside the workspace are NOT deleted. They move to the user's personal scope (`workspaceId` becomes `null`).

```bash
curl -X DELETE https://connect.litehost.io/v1/workspaces/{workspaceId} \
  -H "Authorization: Bearer $LITEHOST_API_KEY"
```

---

## Move Project to Workspace

Use `update-project.md` (PATCH) with `workspaceId` set to the workspace UUID. Set `null` to move back to personal scope.

```bash
curl -X PATCH https://connect.litehost.io/v1/projects/{projectId} \
  -H "Authorization: Bearer $LITEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"workspaceId": "workspace-uuid-here"}'
```

---

## Error Handling

| Status | Action |
|---|---|
| 401 | Follow `utils/auth.md`. |
| 403 | Free-tier restricted. Requires paid plan. Tell user to upgrade at https://litehost.io/dashboard. |
| 404 | Workspace not found. List workspaces to verify the ID. |
| 422 | Validation failed. Check name is 1–255 chars. |
