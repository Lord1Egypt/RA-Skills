---
name: grafana
description: |
  Grafana API integration with managed authentication. This is a write-capable integration — it can read, create, update, and delete dashboards, data sources, folders, annotations, alerts, and teams in your Grafana instance.
  Use this skill when users want to interact with Grafana for monitoring, visualization, and observability. All write operations (creating/updating/deleting dashboards, folders, data sources, alerts, or teams) require explicit user approval with specific resource identifiers before execution.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji:
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Grafana

Access Grafana dashboards, data sources, folders, annotations, and alerts via managed API authentication.

## Quick Start

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/grafana/api/search?type=dash-db')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/grafana/{native-api-path}
```

Maton proxies requests to your Grafana instance and automatically injects authentication.

## Authentication

All requests require the Maton API key:

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

Manage your Grafana connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=grafana&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'grafana'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

Open the returned `url` in a browser to complete authentication. You'll need to provide your Grafana service account token. **Use a dedicated, least-privilege service account token** for this integration — limit it to the specific organization, folders, and resources needed for the task. Avoid admin-role tokens unless specifically required. Rotate the token periodically and revoke it immediately when the connection is no longer needed.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

---

## Security & Permissions

- Access is scoped to dashboards, data sources, folders, annotations, alerts, and teams within the connected Grafana instance. The integration inherits the permissions of the service account token used during connection setup — use least-privilege tokens scoped to the needed organization and folders. Prefer a non-production instance for exploratory work. Remove the connection when no longer needed.
- **Default to read-only operations.** Always start by listing or retrieving resources to confirm identifiers before proposing any changes.
- **All write operations require explicit user approval with specific identifiers.** Before executing any POST, PUT, PATCH, or DELETE call:
  1. Retrieve and display the target resource (dashboard title/UID, folder name, data source name, alert rule) so the user can verify.
  2. Clearly describe the intended effect (e.g., "This will delete dashboard 'Production Overview' (UID: abc-123) from the 'Ops' folder").
  3. Wait for explicit user confirmation before proceeding.
- **High-impact operations require extra caution.** Deleting dashboards, modifying alert rules, changing data source configurations, and reorganizing folders can affect monitoring and observability workflows. These actions must include a summary of consequences and require confirmation.

## API Reference

### Organization & User

#### Get Current Organization

```bash
GET /grafana/api/org
```

**Response:**
```json
{
  "id": 1,
  "name": "Main Org.",
  "address": {
    "address1": "",
    "address2": "",
    "city": "",
    "zipCode": "",
    "state": "",
    "country": ""
  }
}
```

#### Get Current User

```bash
GET /grafana/api/user
```

**Response:**
```json
{
  "id": 1,
  "uid": "abc123",
  "email": "user@example.com",
  "name": "User Name",
  "login": "user",
  "orgId": 1,
  "isGrafanaAdmin": false
}
```

---

### Dashboards

#### Search Dashboards

```bash
GET /grafana/api/search?type=dash-db
```

**Query Parameters:**
- `type` - `dash-db` for dashboards, `dash-folder` for folders
- `query` - Search query string
- `tag` - Filter by tag
- `folderIds` - Filter by folder IDs
- `limit` - Max results (default 1000)

**Response:**
```json
[
  {
    "id": 1,
    "uid": "abc123",
    "title": "My Dashboard",
    "uri": "db/my-dashboard",
    "url": "/d/abc123/my-dashboard",
    "type": "dash-db",
    "tags": ["production"],
    "isStarred": false
  }
]
```

#### Get Dashboard by UID

```bash
GET /grafana/api/dashboards/uid/{uid}
```

**Response:**
```json
{
  "meta": {
    "type": "db",
    "canSave": true,
    "canEdit": true,
    "canAdmin": true,
    "canStar": true,
    "slug": "my-dashboard",
    "url": "/d/abc123/my-dashboard",
    "expires": "0001-01-01T00:00:00Z",
    "created": "2024-01-01T00:00:00Z",
    "updated": "2024-01-02T00:00:00Z",
    "version": 1
  },
  "dashboard": {
    "id": 1,
    "uid": "abc123",
    "title": "My Dashboard",
    "tags": ["production"],
    "panels": [...],
    "schemaVersion": 30,
    "version": 1
  }
}
```

#### Create/Update Dashboard

```bash
POST /grafana/api/dashboards/db
Content-Type: application/json

{
  "dashboard": {
    "title": "New Dashboard",
    "panels": [],
    "schemaVersion": 30,
    "version": 0
  },
  "folderUid": "optional-folder-uid",
  "overwrite": false
}
```

**Response:**
```json
{
  "id": 1,
  "uid": "abc123",
  "url": "/d/abc123/new-dashboard",
  "status": "success",
  "version": 1,
  "slug": "new-dashboard"
}
```

#### Delete Dashboard

```bash
DELETE /grafana/api/dashboards/uid/{uid}
```

**Response:**
```json
{
  "title": "My Dashboard",
  "message": "Dashboard My Dashboard deleted",
  "id": 1
}
```

#### Get Home Dashboard

```bash
GET /grafana/api/dashboards/home
```

---

### Folders

#### List Folders

```bash
GET /grafana/api/folders
```

**Response:**
```json
[
  {
    "id": 1,
    "uid": "folder123",
    "title": "My Folder",
    "url": "/dashboards/f/folder123/my-folder",
    "hasAcl": false,
    "canSave": true,
    "canEdit": true,
    "canAdmin": true
  }
]
```

#### Get Folder by UID

```bash
GET /grafana/api/folders/{uid}
```

#### Create Folder

```bash
POST /grafana/api/folders
Content-Type: application/json

{
  "title": "New Folder"
}
```

**Response:**
```json
{
  "id": 1,
  "uid": "folder123",
  "title": "New Folder",
  "url": "/dashboards/f/folder123/new-folder",
  "hasAcl": false,
  "canSave": true,
  "canEdit": true,
  "canAdmin": true,
  "version": 1
}
```

#### Update Folder

```bash
PUT /grafana/api/folders/{uid}
Content-Type: application/json

{
  "title": "Updated Folder Name",
  "version": 1
}
```

#### Delete Folder

```bash
DELETE /grafana/api/folders/{uid}
```

---

### Data Sources

#### List Data Sources

```bash
GET /grafana/api/datasources
```

**Response:**
```json
[
  {
    "id": 1,
    "uid": "ds123",
    "orgId": 1,
    "name": "Prometheus",
    "type": "prometheus",
    "access": "proxy",
    "url": "http://prometheus:9090",
    "isDefault": true,
    "readOnly": false
  }
]
```

#### Get Data Source by ID

```bash
GET /grafana/api/datasources/{id}
```

#### Get Data Source by UID

```bash
GET /grafana/api/datasources/uid/{uid}
```

#### Get Data Source by Name

```bash
GET /grafana/api/datasources/name/{name}
```

#### Create Data Source

```bash
POST /grafana/api/datasources
Content-Type: application/json

{
  "name": "New Prometheus",
  "type": "prometheus",
  "url": "http://prometheus:9090",
  "access": "proxy",
  "isDefault": false
}
```

#### Update Data Source

```bash
PUT /grafana/api/datasources/{id}
Content-Type: application/json

{
  "name": "Updated Prometheus",
  "type": "prometheus",
  "url": "http://prometheus:9090",
  "access": "proxy"
}
```

#### Delete Data Source

```bash
DELETE /grafana/api/datasources/{id}
```

---

### Annotations

#### List Annotations

```bash
GET /grafana/api/annotations
```

**Query Parameters:**
- `from` - Epoch timestamp (ms)
- `to` - Epoch timestamp (ms)
- `dashboardId` - Filter by dashboard ID
- `dashboardUID` - Filter by dashboard UID
- `panelId` - Filter by panel ID
- `tags` - Filter by tags (comma-separated)
- `limit` - Max results

#### Create Annotation

```bash
POST /grafana/api/annotations
Content-Type: application/json

{
  "dashboardUID": "abc123",
  "time": 1609459200000,
  "text": "Deployment completed",
  "tags": ["deployment", "production"]
}
```

**Response:**
```json
{
  "message": "Annotation added",
  "id": 1
}
```

#### Update Annotation

```bash
PUT /grafana/api/annotations/{id}
Content-Type: application/json

{
  "text": "Updated annotation text",
  "tags": ["updated"]
}
```

#### Delete Annotation

```bash
DELETE /grafana/api/annotations/{id}
```

---

### Teams

#### Search Teams

```bash
GET /grafana/api/teams/search
```

**Query Parameters:**
- `query` - Search query
- `page` - Page number
- `perpage` - Results per page

**Response:**
```json
{
  "totalCount": 1,
  "teams": [
    {
      "id": 1,
      "orgId": 1,
      "name": "Engineering",
      "email": "engineering@example.com",
      "memberCount": 5
    }
  ],
  "page": 1,
  "perPage": 1000
}
```

#### Get Team by ID

```bash
GET /grafana/api/teams/{id}
```

#### Create Team

```bash
POST /grafana/api/teams
Content-Type: application/json

{
  "name": "New Team",
  "email": "team@example.com"
}
```

#### Update Team

```bash
PUT /grafana/api/teams/{id}
Content-Type: application/json

{
  "name": "Updated Team Name"
}
```

#### Delete Team

```bash
DELETE /grafana/api/teams/{id}
```

---

### Alert Rules (Provisioning API)

#### List Alert Rules

```bash
GET /grafana/api/v1/provisioning/alert-rules
```

#### Get Alert Rule

```bash
GET /grafana/api/v1/provisioning/alert-rules/{uid}
```

#### List Alert Rules by Folder

```bash
GET /grafana/api/ruler/grafana/api/v1/rules
```

---

### Service Accounts

#### Search Service Accounts

```bash
GET /grafana/api/serviceaccounts/search
```

**Response:**
```json
{
  "totalCount": 1,
  "serviceAccounts": [
    {
      "id": 1,
      "name": "api-service",
      "login": "sa-api-service",
      "orgId": 1,
      "isDisabled": false,
      "role": "Editor"
    }
  ],
  "page": 1,
  "perPage": 1000
}
```

---

### Plugins

#### List Plugins

```bash
GET /grafana/api/plugins
```

**Response:**
```json
[
  {
    "name": "Prometheus",
    "type": "datasource",
    "id": "prometheus",
    "enabled": true,
    "pinned": false
  }
]
```

---

## Code Examples

### JavaScript

```javascript
const response = await fetch('https://api.maton.ai/grafana/api/search?type=dash-db', {
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`
  }
});
const dashboards = await response.json();
console.log(dashboards);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://api.maton.ai/grafana/api/search?type=dash-db',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'
    }
)
print(response.json())
```

---

## Notes

- Dashboard UIDs are unique identifiers used in most operations
- Use `/api/search?type=dash-db` to find dashboard UIDs
- Folder operations require folder UIDs
- Some admin operations (list all users, orgs) require elevated permissions
- Alert rules use the provisioning API (`/api/v1/provisioning/...`)
- Annotations require epoch timestamps in milliseconds

## Error Handling

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 400 | Invalid request |
| 401 | Invalid or missing authentication |
| 403 | Permission denied |
| 404 | Resource not found |
| 409 | Conflict (e.g., duplicate name) |
| 412 | Precondition failed (version mismatch) |
| 422 | Unprocessable entity |

## Resources

- [Grafana HTTP API Documentation](https://grafana.com/docs/grafana/latest/developers/http_api/)
- [Dashboard API](https://grafana.com/docs/grafana/latest/developers/http_api/dashboard/)
- [Folder API](https://grafana.com/docs/grafana/latest/developers/http_api/folder/)
- [Data Source API](https://grafana.com/docs/grafana/latest/developers/http_api/data_source/)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
