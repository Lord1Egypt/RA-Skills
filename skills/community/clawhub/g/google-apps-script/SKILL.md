---
name: google-apps-script
description: |
  Google Apps Script API integration with managed OAuth. Manage Apps Script projects, deployments, versions, and execute script functions.
  Use this skill when users want to create or update Apps Script projects, manage deployments and versions, run script functions remotely, or monitor script execution processes.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Google Apps Script

Access the Google Apps Script API with managed OAuth authentication. Create and manage Apps Script projects, update script content, manage deployments and versions, execute functions remotely, and monitor script processes.

## Quick Start

```bash
# Create a new Apps Script project
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"title": "My Script"}).encode()
req = urllib.request.Request('https://api.maton.ai/google-apps-script/v1/projects', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/google-apps-script/{native-api-path}
```

Maton proxies requests to `script.googleapis.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Google Apps Script OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=google-apps-script&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-apps-script'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

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
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "google-apps-script",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Google Apps Script connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/google-apps-script/v1/processes')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to the Apps Script projects owned by or shared with the connected Google account.
- **All write operations require explicit user approval.** Before creating projects, updating content, creating deployments, or executing functions, confirm the target and intended effect with the user.
- **Script execution (`scripts.run`) can have side effects.** Always confirm with the user before running any script function.

## API Reference

### Projects

#### Create Project

```bash
POST /google-apps-script/v1/projects
Content-Type: application/json

{
  "title": "My Script Project",
  "parentId": "{optional_drive_file_id}"
}
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Project name |
| `parentId` | string | No | Drive ID of parent file (Sheet, Doc, Form, Slides). Omit for standalone projects |

**Example:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"title": "Analytics Helper"}).encode()
req = urllib.request.Request('https://api.maton.ai/google-apps-script/v1/projects', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "scriptId": "1e20iskkpOG79nb9sZz53XX6GmqEWwiLFd4GPoGsUL67N0lJXEu1FJud0",
  "title": "Analytics Helper",
  "createTime": "2026-05-05T09:28:57.482Z",
  "updateTime": "2026-05-05T09:28:57.482Z",
  "creator": {
    "email": "user@example.com",
    "name": "User"
  },
  "lastModifyUser": {
    "email": "user@example.com",
    "name": "User"
  }
}
```

#### Get Project

```bash
GET /google-apps-script/v1/projects/{scriptId}
```

#### Get Project Content

```bash
GET /google-apps-script/v1/projects/{scriptId}/content
```

**Optional Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `versionNumber` | integer | Version to retrieve; omit for HEAD (latest) |

**Response:**
```json
{
  "scriptId": "...",
  "files": [
    {
      "name": "appsscript",
      "type": "JSON",
      "source": "{\"timeZone\":\"America/New_York\",\"dependencies\":{},\"exceptionLogging\":\"STACKDRIVER\",\"runtimeVersion\":\"V8\"}",
      "createTime": "2026-05-05T09:28:57.482Z",
      "updateTime": "2026-05-05T09:28:57.482Z",
      "functionSet": {}
    },
    {
      "name": "Code",
      "type": "SERVER_JS",
      "source": "function myFunction() {\n  return 'Hello';\n}",
      "functionSet": {
        "values": [{"name": "myFunction"}]
      }
    }
  ]
}
```

#### Update Project Content

```bash
PUT /google-apps-script/v1/projects/{scriptId}/content
Content-Type: application/json

{
  "files": [
    {
      "name": "appsscript",
      "type": "JSON",
      "source": "{\"timeZone\":\"America/New_York\",\"dependencies\":{},\"exceptionLogging\":\"STACKDRIVER\",\"runtimeVersion\":\"V8\"}"
    },
    {
      "name": "Code",
      "type": "SERVER_JS",
      "source": "function myFunction() {\n  Logger.log('Hello');\n  return 'Hello';\n}"
    }
  ]
}
```

**File types:** `SERVER_JS` (script code), `HTML` (HTML files), `JSON` (manifest only)

**Important:** This replaces ALL files in the project. Always include the `appsscript` manifest file.

**Example:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "files": [
        {
            "name": "appsscript",
            "type": "JSON",
            "source": json.dumps({
                "timeZone": "America/New_York",
                "dependencies": {},
                "exceptionLogging": "STACKDRIVER",
                "runtimeVersion": "V8"
            })
        },
        {
            "name": "Code",
            "type": "SERVER_JS",
            "source": "function getData() {\n  var sheet = SpreadsheetApp.getActiveSheet();\n  return sheet.getDataRange().getValues();\n}"
        }
    ]
}).encode()
req = urllib.request.Request('https://api.maton.ai/google-apps-script/v1/projects/{scriptId}/content', data=data, method='PUT')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### Get Project Metrics

```bash
GET /google-apps-script/v1/projects/{scriptId}/metrics?metricsGranularity=DAILY
```

**Required Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `metricsGranularity` | string | `DAILY` or `WEEKLY` |

**Response:**
```json
{
  "activeUsers": [
    {"startTime": "2026-05-04T00:00:00Z", "endTime": "2026-05-05T00:00:00Z"}
  ],
  "totalExecutions": [
    {"startTime": "2026-05-04T00:00:00Z", "endTime": "2026-05-05T00:00:00Z"}
  ],
  "failedExecutions": [
    {"startTime": "2026-05-04T00:00:00Z", "endTime": "2026-05-05T00:00:00Z"}
  ]
}
```

### Versions

#### Create Version

```bash
POST /google-apps-script/v1/projects/{scriptId}/versions
Content-Type: application/json

{
  "description": "Release v1.0"
}
```

**Response:**
```json
{
  "scriptId": "...",
  "versionNumber": 1,
  "description": "Release v1.0",
  "createTime": "2026-05-05T09:29:20.755Z"
}
```

#### List Versions

```bash
GET /google-apps-script/v1/projects/{scriptId}/versions
```

**Optional Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageSize` | integer | Max results per page |
| `pageToken` | string | Token for next page |

**Response:**
```json
{
  "versions": [
    {
      "scriptId": "...",
      "versionNumber": 1,
      "description": "Release v1.0",
      "createTime": "2026-05-05T09:29:20.755Z"
    }
  ],
  "nextPageToken": "..."
}
```

#### Get Version

```bash
GET /google-apps-script/v1/projects/{scriptId}/versions/{versionNumber}
```

### Deployments

#### Create Deployment

```bash
POST /google-apps-script/v1/projects/{scriptId}/deployments
Content-Type: application/json

{
  "versionNumber": 1,
  "description": "Production deployment",
  "manifestFileName": "appsscript"
}
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `versionNumber` | integer | No | Version to deploy |
| `description` | string | No | Deployment description |
| `manifestFileName` | string | No | Manifest file name (default: `appsscript`) |

**Response:**
```json
{
  "deploymentId": "AKfycbwcP87Ic2d91w3RqGX73ulArxNtrsJBUScaGZrPe45GztKsUo7b-CPHFr3aEmG9gIJxyg",
  "deploymentConfig": {
    "scriptId": "...",
    "versionNumber": 1,
    "manifestFileName": "appsscript",
    "description": "Production deployment"
  },
  "updateTime": "2026-05-05T09:29:37.688Z"
}
```

#### List Deployments

```bash
GET /google-apps-script/v1/projects/{scriptId}/deployments
```

**Optional Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageSize` | integer | Max results per page |
| `pageToken` | string | Token for next page |

#### Get Deployment

```bash
GET /google-apps-script/v1/projects/{scriptId}/deployments/{deploymentId}
```

#### Update Deployment

```bash
PUT /google-apps-script/v1/projects/{scriptId}/deployments/{deploymentId}
Content-Type: application/json

{
  "deploymentConfig": {
    "scriptId": "{scriptId}",
    "versionNumber": 2,
    "manifestFileName": "appsscript",
    "description": "Updated to v2"
  }
}
```

#### Delete Deployment

```bash
DELETE /google-apps-script/v1/projects/{scriptId}/deployments/{deploymentId}
```

### Processes

#### List User Processes

```bash
GET /google-apps-script/v1/processes
```

**Optional Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageSize` | integer | Max results per page (default: 50) |
| `pageToken` | string | Token for next page |

**Response:**
```json
{
  "processes": [
    {
      "projectName": "My Script",
      "functionName": "myFunction",
      "processType": "TIME_DRIVEN",
      "processStatus": "COMPLETED",
      "userAccessLevel": "READ",
      "startTime": "2026-05-05T09:05:31.422Z",
      "duration": "4.533s",
      "runtimeVersion": "V8"
    }
  ],
  "nextPageToken": "..."
}
```

**Process types:** `TIME_DRIVEN`, `EDITOR`, `SIMPLE_TRIGGER`, `INSTALLABLE_TRIGGER`, `WEBAPP`, `EXECUTION_API`, `ADD_ON`, `BATCH_TASK`

**Process statuses:** `COMPLETED`, `FAILED`, `TIMED_OUT`, `UNKNOWN`, `DELAYED`, `RUNNING`, `CANCELED`

#### List Script Processes

```bash
GET /google-apps-script/v1/processes:listScriptProcesses?scriptId={scriptId}
```

### Scripts

#### Run Function

```bash
POST /google-apps-script/v1/scripts/{scriptId}:run
Content-Type: application/json

{
  "function": "myFunction",
  "parameters": ["arg1", 42],
  "devMode": false
}
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `function` | string | Yes | Function name to execute |
| `parameters` | array | No | Function arguments (primitives only) |
| `devMode` | boolean | No | If `true`, runs latest saved code instead of deployed version |

**Response:**
```json
{
  "done": true,
  "response": {
    "@type": "type.googleapis.com/google.apps.script.v1.ExecutionResponse",
    "result": "Hello World"
  }
}
```

**Note:** Requires an "API Executable" deployment. The script must be deployed via Apps Script editor with "Deploy > New deployment > API Executable".

## Pagination

All list endpoints use token-based pagination:

```bash
GET /google-apps-script/v1/processes?pageSize=10&pageToken={nextPageToken}
```

Response includes `nextPageToken` when more results exist:

```json
{
  "processes": [...],
  "nextPageToken": "Cg5iDAjLpuHPBhDQ1KO6Ag=="
}
```

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/google-apps-script/v1/projects',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title: 'My Script' })
  }
);
const project = await response.json();
console.log(project.scriptId);
```

### Python

```python
import os
import requests

# Create a project
project = requests.post(
    'https://api.maton.ai/google-apps-script/v1/projects',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'title': 'My Script'}
).json()

# Update its content
requests.put(
    f'https://api.maton.ai/google-apps-script/v1/projects/{project["scriptId"]}/content',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'files': [
            {
                'name': 'appsscript',
                'type': 'JSON',
                'source': '{"timeZone":"America/New_York","dependencies":{},"exceptionLogging":"STACKDRIVER","runtimeVersion":"V8"}'
            },
            {
                'name': 'Code',
                'type': 'SERVER_JS',
                'source': 'function hello() { return "Hello World"; }'
            }
        ]
    }
)
```

## Notes

- The `scriptId` is the Drive file ID of the Apps Script project
- `updateContent` replaces ALL files; always include the `appsscript` manifest file
- Versions are immutable snapshots; create a new version before deploying
- The `scripts.run` endpoint requires an "API Executable" deployment configured in the Apps Script editor
- `devMode: true` in `scripts.run` executes the latest saved HEAD code (owner only)
- Only primitive types (string, number, boolean, array, object) can be passed as parameters to `scripts.run`
- Metrics require the `metricsGranularity` query parameter (`DAILY` or `WEEKLY`)
- Bound scripts (attached to Sheets/Docs/Forms) need the parent file's Drive ID as `parentId` during creation
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Bad request (invalid argument, missing required fields) |
| 401 | Invalid or missing Maton API key |
| 403 | Forbidden (insufficient permissions for the script) |
| 404 | Script project or deployment not found |
| 409 | Conflict (concurrent edit) |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Apps Script API |

### Troubleshooting: API Key Issues

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

1. Ensure your URL path starts with `google-apps-script`. For example:

- Correct: `https://api.maton.ai/google-apps-script/v1/projects`
- Incorrect: `https://api.maton.ai/v1/projects`

## Resources

- [Apps Script API Overview](https://developers.google.com/apps-script/api)
- [Apps Script API Reference](https://developers.google.com/apps-script/api/reference/rest)
- [Projects Resource](https://developers.google.com/apps-script/api/reference/rest/v1/projects)
- [Deployments Guide](https://developers.google.com/apps-script/api/how-tos/manage-deployments)
- [Executing Functions](https://developers.google.com/apps-script/api/how-tos/execute)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
