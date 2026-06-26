---
name: movedone
description: Manage Movedone kanban projects, columns, tasks, comments, and task links via the local HTTP API.
homepage: https://movedone.ai
metadata:
  {
    "openclaw":
      { "emoji": "🪧", "requires": { "bins": ["curl"], "env": ["MOVEDONE_BASE_URL", "MOVEDONE_AUTH_TOKEN"] } },
  }
---

# Movedone Skill

Manage Movedone kanban projects, columns, tasks, comments, and task links directly from OpenClaw.

## Setup

1. Download the Movedone desktop app: https://movedone.ai/#download
2. In Movedone, open `Settings > OpenClaw`
3. Enable the HTTP API and copy the base URL and bearer token
4. Set environment variables:
   ```bash
   export MOVEDONE_BASE_URL="http://127.0.0.1:5613"
   export MOVEDONE_AUTH_TOKEN="your-bearer-token"
   ```

## Usage

All commands use `curl` to hit the local Movedone HTTP API.

### List projects

```bash
curl -s "$MOVEDONE_BASE_URL/projects" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

### Create a project

```bash
curl -s -X POST "$MOVEDONE_BASE_URL/projects" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Launch Plan","defaultTemplate":true}'
```

### Get a project with columns and tasks

```bash
curl -s "$MOVEDONE_BASE_URL/projects/{project_id}" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

### Rename a project

```bash
curl -s -X PATCH "$MOVEDONE_BASE_URL/projects/{project_id}" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Renamed Project"}'
```

### Delete a project

```bash
curl -s -X DELETE "$MOVEDONE_BASE_URL/projects/{project_id}" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

### Create a column

```bash
curl -s -X POST "$MOVEDONE_BASE_URL/projects/{project_id}/columns" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Blocked"}'
```

### Rename a column

```bash
curl -s -X PATCH "$MOVEDONE_BASE_URL/columns/{column_id}" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"In Review"}'
```

### Delete a column

```bash
curl -s -X DELETE "$MOVEDONE_BASE_URL/columns/{column_id}" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

### Search tasks

```bash
curl -s "$MOVEDONE_BASE_URL/tasks/search?projectId={project_id}&query=bug" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

### Get a task

```bash
curl -s "$MOVEDONE_BASE_URL/tasks/{task_id}" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

### Create a task

```bash
curl -s -X POST "$MOVEDONE_BASE_URL/tasks" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "columnId":"{column_id}",
    "title":"Write release notes",
    "description":"Summarize the user-facing changes.",
    "priority":"high",
    "tags":["release","docs"]
  }'
```

### Update a task

```bash
curl -s -X PATCH "$MOVEDONE_BASE_URL/tasks/{task_id}" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Write final release notes",
    "description":"Include HTTP API updates.",
    "priority":"medium",
    "tags":["release","docs"],
    "aiStatus":"ready"
  }'
```

### Move a task

```bash
curl -s -X POST "$MOVEDONE_BASE_URL/tasks/{task_id}/move" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "toColumnId":"{target_column_id}",
    "newPosition": 2
  }'
```

### Delete a task

```bash
curl -s -X DELETE "$MOVEDONE_BASE_URL/tasks/{task_id}" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

### List comments on a task

```bash
curl -s "$MOVEDONE_BASE_URL/tasks/{task_id}/comments" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

### Add a comment to a task

```bash
curl -s -X POST "$MOVEDONE_BASE_URL/tasks/{task_id}/comments" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Agent-Name: OpenClaw" \
  -d '{"content":"Finished the API integration and started verification."}'
```

### List task links

```bash
curl -s "$MOVEDONE_BASE_URL/tasks/{task_id}/links" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

### Add a task link

```bash
curl -s -X POST "$MOVEDONE_BASE_URL/tasks/{task_id}/links" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "targetTaskId":"{target_task_id}",
    "linkType":"depends_on"
  }'
```

### Remove a task link

```bash
curl -s -X DELETE "$MOVEDONE_BASE_URL/tasks/{task_id}/links/{target_task_id}" \
  -H "Authorization: Bearer $MOVEDONE_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

## Notes

- Project, column, and task IDs can be discovered with the list and get commands above
- The base URL and bearer token provide full access to your local Movedone HTTP API, so keep them secret
- Use the `X-Agent-Name` header to identify the agent when adding comments (defaults to "Agent" if omitted)
- Use `add_comment` to append progress notes, status updates, working commentary, or intermediate results; do not overwrite the task description for that purpose
- Supported task link types are `depends_on`, `blocks`, and `related`
