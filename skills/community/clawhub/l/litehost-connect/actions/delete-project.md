# Delete Project

Permanently delete a project and all its associated data. This is irreversible.

## Endpoint

```
DELETE /v1/projects/{projectId}
```

## Parameters

| Field | Type | Required | Description |
|---|---|---|---|
| projectId | uuid | yes | Path parameter. |

## Pre-flight

ALWAYS confirm with the user before executing. Say:
"This will permanently delete the project and all its data. This cannot be undone. Proceed?"

If the user's goal is to free quota rather than destroy data, suggest `archive-project.md` instead — archiving preserves data while freeing project slots and storage.

## Example

```bash
curl -X DELETE https://connect.litehost.io/v1/projects/{projectId} \
  -H "Authorization: Bearer $LITEHOST_API_KEY"
```

## Success Response (200)

```json
{
  "status": "success",
  "data": { "deleted": true }
}
```

## Error Handling

| Status | Action |
|---|---|
| 401 | Follow `utils/auth.md`. |
| 404 | Project not found. List projects and ask user to pick. |
