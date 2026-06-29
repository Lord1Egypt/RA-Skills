---
name: google-tasks
description: |
  Google Tasks API integration with managed OAuth. Manage task lists and tasks with full CRUD operations.
  Use this skill when users want to read, create, update, or delete tasks and task lists in Google Tasks.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Google Tasks

Access the Google Tasks API with managed OAuth authentication. Manage task lists and tasks with full CRUD operations.

## Quick Start

**CLI:**

```bash
maton google-tasks task list -l <tasklistId>
```

```bash
maton api '/google-tasks/tasks/v1/lists/<tasklistId>/tasks'
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/google-tasks/tasks/v1/lists/<tasklistId>/tasks')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/google-tasks/{native-api-path}
```

Maton proxies requests to `tasks.googleapis.com` and automatically injects your OAuth token.

## Installation

**NPM:**
```bash
npm install -g @maton/cli
```

**Homebrew:**
```bash
brew install maton-ai/cli/maton
```

## Authentication

**CLI:**

```bash
maton login                          # Opens browser for API key
maton login --interactive            # Skip browser, paste API key directly
maton whoami                         # Show current auth state
```

**Manual:**

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key
4. Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

## Connection Management

Manage your Google Tasks OAuth connections at `https://api.maton.ai`.

### List Connections

**CLI:**

```bash
maton connection list google-tasks --status ACTIVE
```

```bash
maton api -X GET /connections -f app=google-tasks -f status=ACTIVE
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=google-tasks&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

**CLI:**

```bash
maton connection create google-tasks
```

```bash
maton api /connections -f app=google-tasks
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-tasks'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

**CLI:**

```bash
maton connection view {connection_id}
```

```bash
maton api /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T02:35:51.002199Z",
    "last_updated_time": "2026-02-07T05:32:30.369186Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "google-tasks",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

**CLI:**

```bash
maton connection delete {connection_id}
```

```bash
maton api -X DELETE /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Google Tasks connections, specify which one to use:

**CLI:**

```bash
maton google-tasks tasklist list --connection {connection_id}
```

```bash
maton api /google-tasks/tasks/v1/users/@me/lists --connection {connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/google-tasks/tasks/v1/users/@me/lists')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always specify the connection to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to task lists and tasks with full CRUD operations within the connected Google Tasks account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference

### Task Lists

#### List All Task Lists

```bash
GET /google-tasks/tasks/v1/users/@me/lists
```

**Query Parameters:**
- `maxResults` - Maximum number of task lists to return (default: 20, max: 100)
- `pageToken` - Token for pagination

Example:

```bash
maton google-tasks tasklist list
```

#### Get Task List

```bash
GET /google-tasks/tasks/v1/users/@me/lists/{tasklistId}
```

Example:

```bash
maton google-tasks tasklist view <tasklistId>
```

#### Create Task List

```bash
POST /google-tasks/tasks/v1/users/@me/lists
Content-Type: application/json

{
  "title": "New Task List"
}
```

Example:

```bash
maton google-tasks tasklist create --title 'New Task List'
```

#### Update Task List (PATCH - partial update)

```bash
PATCH /google-tasks/tasks/v1/users/@me/lists/{tasklistId}
Content-Type: application/json

{
  "title": "Updated Title"
}
```

Example:

```bash
maton google-tasks tasklist update <tasklistId> --title 'Updated Title'
```

#### Update Task List (PUT - full replace)

```bash
PUT /google-tasks/tasks/v1/users/@me/lists/{tasklistId}
Content-Type: application/json

{
  "title": "Replaced Title"
}
```

Example:

```bash
maton google-tasks tasklist update <tasklistId> --title 'Replaced Title' --replace
```

#### Delete Task List

```bash
DELETE /google-tasks/tasks/v1/users/@me/lists/{tasklistId}
```

Example:

```bash
maton google-tasks tasklist delete <tasklistId>
```

### Tasks

#### List Tasks

```bash
GET /google-tasks/tasks/v1/lists/{tasklistId}/tasks?showCompleted=true
```

**Query Parameters:**
- `maxResults` - Maximum number of tasks to return (default: 20, max: 100)
- `pageToken` - Token for pagination
- `showCompleted` - Include completed tasks (default: true)
- `showDeleted` - Include deleted tasks (default: false)
- `showHidden` - Include hidden tasks (default: false)
- `dueMin` - Lower bound for due date (RFC 3339 timestamp)
- `dueMax` - Upper bound for due date (RFC 3339 timestamp)
- `completedMin` - Lower bound for completion date (RFC 3339 timestamp)
- `completedMax` - Upper bound for completion date (RFC 3339 timestamp)
- `updatedMin` - Lower bound for last update time (RFC 3339 timestamp)

Example:

```bash
maton google-tasks task list -l <tasklistId> --show-completed
```

#### Get Task

```bash
GET /google-tasks/tasks/v1/lists/{tasklistId}/tasks/{taskId}
```

Example:

```bash
maton google-tasks task view <taskId> -l <tasklistId>
```

#### Create Task

```bash
POST /google-tasks/tasks/v1/lists/{tasklistId}/tasks
Content-Type: application/json

{
  "title": "New Task",
  "notes": "Task description",
  "due": "2026-03-01T00:00:00.000Z"
}
```

**Query Parameters (optional):**
- `parent` - Parent task ID (for subtasks)
- `previous` - Previous sibling task ID (for positioning)

Example:

```bash
maton google-tasks task create -l <tasklistId> --title 'New Task' --notes 'Task description' --due 2026-03-01
```

#### Update Task (PATCH - partial update)

```bash
PATCH /google-tasks/tasks/v1/lists/{tasklistId}/tasks/{taskId}
Content-Type: application/json

{
  "title": "Updated Task Title",
  "status": "completed"
}
```

Example:

```bash
maton google-tasks task update <taskId> -l <tasklistId> --title 'Updated Task Title' --status completed
```

#### Update Task (PUT - full replace)

```bash
PUT /google-tasks/tasks/v1/lists/{tasklistId}/tasks/{taskId}
Content-Type: application/json

{
  "title": "Replaced Task",
  "notes": "New notes",
  "status": "needsAction"
}
```

Example:

```bash
maton google-tasks task update <taskId> -l <tasklistId> --title 'Replaced Task' --notes 'New notes' --status needsAction --replace
```

#### Delete Task

```bash
DELETE /google-tasks/tasks/v1/lists/{tasklistId}/tasks/{taskId}
```

Example:

```bash
maton google-tasks task delete <taskId> -l <tasklistId>
```

#### Move Task

Reposition a task within a task list or change its parent.

```bash
POST /google-tasks/tasks/v1/lists/{tasklistId}/tasks/{taskId}/move
```

**Query Parameters (optional):**
- `parent` - New parent task ID (for making it a subtask)
- `previous` - Previous sibling task ID (for positioning after this task)

Example:

```bash
maton google-tasks task move <taskId> -l <tasklistId> --previous <siblingTaskId>
```

#### Clear Completed Tasks

Delete all completed tasks from a task list.

```bash
POST /google-tasks/tasks/v1/lists/{tasklistId}/clear
```

Example:

```bash
maton google-tasks tasklist clear <tasklistId>
```

## Task Resource Fields

| Field | Type | Description |
|-------|------|-------------|
| `kind` | string | Always "tasks#task" (output only) |
| `id` | string | Task identifier |
| `etag` | string | ETag of the resource |
| `title` | string | Task title (max 1024 characters) |
| `updated` | string | Last modification time (RFC 3339, output only) |
| `selfLink` | string | URL to this task (output only) |
| `parent` | string | Parent task ID (output only) |
| `position` | string | Position among siblings (output only) |
| `notes` | string | Task notes (max 8192 characters) |
| `status` | string | "needsAction" or "completed" |
| `due` | string | Due date (RFC 3339 timestamp) |
| `completed` | string | Completion date (RFC 3339, output only) |
| `deleted` | boolean | Whether task is deleted |
| `hidden` | boolean | Whether task is hidden |
| `links` | array | Collection of links (output only) |
| `webViewLink` | string | Link to task in Google Tasks UI (output only) |

## Task List Resource Fields

| Field | Type | Description |
|-------|------|-------------|
| `kind` | string | Always "tasks#taskList" (output only) |
| `id` | string | Task list identifier |
| `etag` | string | ETag of the resource |
| `title` | string | Task list title (max 1024 characters) |
| `updated` | string | Last modification time (RFC 3339, output only) |
| `selfLink` | string | URL to this task list (output only) |

## Pagination

Google Tasks uses token-based pagination. The CLI automatically paginates with '--paginate'.

Example:

```bash
maton google-tasks task list -l <tasklistId> --paginate
```

## Code Examples

### CLI

```bash
# List all task lists
maton google-tasks tasklist list

# Filter with jq — e.g., extract task list titles
maton google-tasks tasklist list --json --jq '.items[].title'

# Create a task with a due date
maton google-tasks task create -l <tasklistId> --title 'Write spec' --due 2026-12-01
```

### JavaScript

```javascript
// List all task lists
const response = await fetch(
  'https://api.maton.ai/google-tasks/tasks/v1/users/@me/lists',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);

// Create a new task
const createResponse = await fetch(
  `https://api.maton.ai/google-tasks/tasks/v1/lists/${tasklistId}/tasks`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title: 'New Task',
      notes: 'Task description',
      due: '2026-03-01T00:00:00.000Z'
    })
  }
);
```

### Python

```python
import os
import requests

# List all task lists
response = requests.get(
    'https://api.maton.ai/google-tasks/tasks/v1/users/@me/lists',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)

# Create a new task
create_response = requests.post(
    f'https://api.maton.ai/google-tasks/tasks/v1/lists/{tasklist_id}/tasks',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'title': 'New Task',
        'notes': 'Task description',
        'due': '2026-03-01T00:00:00.000Z'
    }
)
```

## Notes

- Task list IDs and task IDs are opaque strings (base64-encoded)
- Status values are "needsAction" or "completed"
- Due dates are RFC 3339 timestamps
- Maximum title length: 1024 characters
- Maximum notes length: 8192 characters
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments. You may get "Invalid API key" errors when piping.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Google Tasks connection |
| 401 | Invalid or missing Maton API key |
| 404 | Task or task list not found |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Google Tasks API |

### Troubleshooting: API Key Issues

**CLI:**

1. Check your auth state:

```bash
maton whoami
```

2. Verify the API key is valid by listing connections:

```bash
maton connection list
```

**Manual:**

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `google-tasks`. For example:

- Correct: `https://api.maton.ai/google-tasks/tasks/v1/users/@me/lists`
- Incorrect: `https://api.maton.ai/tasks/v1/users/@me/lists`

## Resources

- [Google Tasks API Overview](https://developers.google.com/workspace/tasks)
- [Tasks Reference](https://developers.google.com/workspace/tasks/reference/rest/v1/tasks)
- [TaskLists Reference](https://developers.google.com/workspace/tasks/reference/rest/v1/tasklists)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
