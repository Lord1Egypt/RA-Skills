---
name: kibana
description: |
  Kibana API integration with managed authentication. This is a write-capable integration — it can read, create, update, and delete saved objects, dashboards, data views, spaces, alerts, fleet resources, connectors/actions, security roles, and cases in your Kibana instance.
  All write operations require explicit user approval with specific resource identifiers before execution. Connector execution triggers external side effects (e.g., sending emails, invoking webhooks) — always confirm the connector ID, target, and payload with the user before executing.
  Use this skill when users want to interact with Kibana for observability, security, and search analytics. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Kibana

Access Kibana saved objects, dashboards, data views, spaces, alerts, and fleet via managed API authentication.

## Quick Start

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/kibana/api/saved_objects/_find?type=dashboard')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('kbn-xsrf', 'true')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/kibana/{native-api-path}
```

Maton proxies requests to your Kibana instance and automatically injects authentication.

## Authentication

All requests require the Maton API key and the `kbn-xsrf` header:

```
Authorization: Bearer $MATON_API_KEY
kbn-xsrf: true
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management (Maton Platform)

The following endpoints are Maton platform operations for managing the connection to Kibana — they are not part of the Kibana API itself. Only the endpoints listed in the API Reference section below are proxied to Kibana.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=kibana&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'kibana'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

Open the returned `url` in a browser to complete authentication. You'll need to provide your Kibana API key. **Use a dedicated, least-privilege Kibana API key** for this integration — avoid admin-level credentials unless specifically required. Scope the key to only the spaces and saved object types needed for the task, and remove the connection when no longer needed.

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

- Access is scoped to saved objects, dashboards, data views, spaces, alerts, fleet, connectors/actions, security roles, and cases within the connected Kibana instance. The integration inherits the permissions of the Kibana API key used during connection setup — use least-privilege keys and avoid admin-level credentials unless required. Prefer a non-production connection for exploratory work. Remove the connection when no longer needed.
- **Default to read-only operations.** Always start by listing or retrieving resources to confirm identifiers before proposing any changes.
- **All write operations require explicit user approval with specific identifiers.** Before executing any POST, PUT, or DELETE call:
  1. Retrieve and display the target resource (dashboard title/ID, saved object type and ID, space name, alert rule name) so the user can verify.
  2. Clearly describe the intended effect (e.g., "This will delete dashboard 'Production Overview' (ID: abc-123) from the default space").
  3. Wait for explicit user confirmation before proceeding.
- **High-impact operations require extra caution.** Deleting dashboards, modifying alert rules, changing space configurations, bulk-importing/exporting saved objects, and fleet agent actions can affect observability and security monitoring. These actions must include a summary of consequences and require confirmation.

## API Reference

**Important:** All Kibana API requests require the `kbn-xsrf: true` header.

### Status & Features

#### Get Status

```bash
GET /kibana/api/status
```

**Response:**
```json
{
  "name": "kibana",
  "uuid": "abc123",
  "version": {
    "number": "8.15.0",
    "build_hash": "..."
  },
  "status": {
    "overall": {"level": "available"}
  }
}
```

#### List Features

```bash
GET /kibana/api/features
```

Returns list of all Kibana features and their capabilities.

---

### Saved Objects

#### Find Saved Objects

```bash
GET /kibana/api/saved_objects/_find?type={type}
```

**Query Parameters:**
- `type` - Object type: `dashboard`, `visualization`, `index-pattern`, `search`, `lens`, `map`
- `search` - Search query
- `page` - Page number
- `per_page` - Results per page (default 20, max 10000)
- `fields` - Fields to return

**Response:**
```json
{
  "page": 1,
  "per_page": 20,
  "total": 5,
  "saved_objects": [
    {
      "id": "abc123",
      "type": "dashboard",
      "attributes": {
        "title": "My Dashboard",
        "description": "Dashboard description"
      },
      "version": "1",
      "updated_at": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

#### Get Saved Object

```bash
GET /kibana/api/saved_objects/{type}/{id}
```

#### Create Saved Object

```bash
POST /kibana/api/saved_objects/{type}/{id}
Content-Type: application/json

{
  "attributes": {
    "title": "My Index Pattern",
    "timeFieldName": "@timestamp"
  }
}
```

#### Update Saved Object

```bash
PUT /kibana/api/saved_objects/{type}/{id}
Content-Type: application/json

{
  "attributes": {
    "title": "Updated Title"
  }
}
```

#### Delete Saved Object

```bash
DELETE /kibana/api/saved_objects/{type}/{id}
```

#### Bulk Operations

```bash
POST /kibana/api/saved_objects/_bulk_get
Content-Type: application/json

[
  {"type": "dashboard", "id": "abc123"},
  {"type": "visualization", "id": "def456"}
]
```

---

### Data Views

#### List Data Views

```bash
GET /kibana/api/data_views
```

**Response:**
```json
{
  "data_view": [
    {
      "id": "abc123",
      "title": "logs-*",
      "timeFieldName": "@timestamp"
    }
  ]
}
```

#### Get Data View

```bash
GET /kibana/api/data_views/data_view/{id}
```

#### Create Data View

```bash
POST /kibana/api/data_views/data_view
Content-Type: application/json

{
  "data_view": {
    "title": "logs-*",
    "timeFieldName": "@timestamp"
  }
}
```

**Response:**
```json
{
  "data_view": {
    "id": "abc123",
    "title": "logs-*",
    "timeFieldName": "@timestamp"
  }
}
```

#### Update Data View

```bash
POST /kibana/api/data_views/data_view/{id}
Content-Type: application/json

{
  "data_view": {
    "title": "updated-logs-*"
  }
}
```

#### Delete Data View

```bash
DELETE /kibana/api/data_views/data_view/{id}
```

---

### Spaces

#### List Spaces

```bash
GET /kibana/api/spaces/space
```

**Response:**
```json
[
  {
    "id": "default",
    "name": "Default",
    "description": "Default space",
    "disabledFeatures": []
  }
]
```

#### Get Space

```bash
GET /kibana/api/spaces/space/{id}
```

#### Create Space

```bash
POST /kibana/api/spaces/space
Content-Type: application/json

{
  "id": "marketing",
  "name": "Marketing",
  "description": "Marketing team space",
  "disabledFeatures": []
}
```

#### Update Space

```bash
PUT /kibana/api/spaces/space/{id}
Content-Type: application/json

{
  "id": "marketing",
  "name": "Marketing Team",
  "description": "Updated description"
}
```

#### Delete Space

```bash
DELETE /kibana/api/spaces/space/{id}
```

---

### Alerting

#### Find Alert Rules

```bash
GET /kibana/api/alerting/rules/_find
```

**Query Parameters:**
- `search` - Search query
- `page` - Page number
- `per_page` - Results per page

**Response:**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 5,
  "data": [
    {
      "id": "abc123",
      "name": "CPU Alert",
      "consumer": "alerts",
      "enabled": true,
      "rule_type_id": "metrics.alert.threshold"
    }
  ]
}
```

#### Get Alert Rule

```bash
GET /kibana/api/alerting/rule/{id}
```

#### Enable/Disable Rule

```bash
POST /kibana/api/alerting/rule/{id}/_enable
POST /kibana/api/alerting/rule/{id}/_disable
```

#### Mute/Unmute Rule

```bash
POST /kibana/api/alerting/rule/{id}/_mute_all
POST /kibana/api/alerting/rule/{id}/_unmute_all
```

#### Get Alerting Health

```bash
GET /kibana/api/alerting/_health
```

---

### Connectors (Actions)

> **External side effects.** Executing a connector triggers actions outside Kibana (sending emails, posting to Slack, invoking webhooks, etc.). Always confirm the connector ID, action type, and full payload with the user before executing. Do not execute connectors proactively.

#### List Connectors

```bash
GET /kibana/api/actions/connectors
```

**Response:**
```json
[
  {
    "id": "abc123",
    "name": "Email Connector",
    "connector_type_id": ".email",
    "is_preconfigured": false,
    "is_deprecated": false
  }
]
```

#### Get Connector

```bash
GET /kibana/api/actions/connector/{id}
```

#### List Connector Types

```bash
GET /kibana/api/actions/connector_types
```

#### Execute Connector

```bash
POST /kibana/api/actions/connector/{id}/_execute
Content-Type: application/json

{
  "params": {
    "to": ["user@example.com"],
    "subject": "Alert",
    "message": "Alert triggered"
  }
}
```

---

### Fleet

#### List Agent Policies

```bash
GET /kibana/api/fleet/agent_policies
```

**Response:**
```json
{
  "items": [
    {
      "id": "abc123",
      "name": "Default policy",
      "namespace": "default",
      "status": "active"
    }
  ],
  "total": 1,
  "page": 1,
  "perPage": 20
}
```

#### List Agents

```bash
GET /kibana/api/fleet/agents
```

#### List Packages

```bash
GET /kibana/api/fleet/epm/packages
```

Returns all available integrations/packages.

---

### Security

> **Admin scope.** Security role inspection reveals privilege configurations across the Kibana instance. This is read-only but exposes access control details.

#### List Roles

```bash
GET /kibana/api/security/role
```

**Response:**
```json
[
  {
    "name": "admin",
    "metadata": {},
    "elasticsearch": {
      "cluster": ["all"],
      "indices": [...]
    },
    "kibana": [...]
  }
]
```

#### Get Role

```bash
GET /kibana/api/security/role/{name}
```

---

### Cases

#### Find Cases

```bash
GET /kibana/api/cases/_find
```

**Query Parameters:**
- `status` - `open`, `in-progress`, `closed`
- `severity` - `low`, `medium`, `high`, `critical`
- `page` - Page number
- `perPage` - Results per page

**Response:**
```json
{
  "cases": [],
  "page": 1,
  "per_page": 20,
  "total": 0
}
```

---

## Code Examples

### JavaScript

```javascript
const response = await fetch('https://api.maton.ai/kibana/api/saved_objects/_find?type=dashboard', {
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'kbn-xsrf': 'true'
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
    'https://api.maton.ai/kibana/api/saved_objects/_find?type=dashboard',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'kbn-xsrf': 'true'
    }
)
print(response.json())
```

---

## Notes

- All requests require `kbn-xsrf: true` header
- Saved object types: `dashboard`, `visualization`, `index-pattern`, `search`, `lens`, `map`
- Data views are the modern replacement for index patterns
- Spaces provide multi-tenancy support
- Fleet manages Elastic Agents and integrations
- Some operations require specific Kibana privileges

## Error Handling

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 204 | No content (successful delete) |
| 400 | Invalid request |
| 401 | Invalid or missing authentication |
| 403 | Permission denied |
| 404 | Resource not found |
| 409 | Conflict (e.g., object already exists) |

## Resources

- [Kibana REST API Documentation](https://www.elastic.co/docs/api/doc/kibana/)
- [Saved Objects API](https://www.elastic.co/guide/en/kibana/current/saved-objects-api.html)
- [Alerting API](https://www.elastic.co/guide/en/kibana/current/alerting-apis.html)
- [Fleet API](https://www.elastic.co/guide/en/fleet/current/fleet-apis.html)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
