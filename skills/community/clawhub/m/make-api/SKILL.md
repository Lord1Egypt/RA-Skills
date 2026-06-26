---
name: make
description: |
  Make (formerly Integromat) API integration with managed authentication. Manage scenarios, organizations, teams, connections, data stores, hooks, and templates.
  Use this skill when users want to automate workflows, manage scenarios, or integrate apps using Make.
  All write operations (create, update, start, stop, delete) require explicit user approval before executing. Starting or creating scenarios, hooks, and data stores creates persistent resources that continue operating after the conversation ends.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: "🔧"
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Make

Access the Make API with managed authentication. Manage scenarios, organizations, teams, connections, data stores, hooks, and templates.

## Quick Start

```bash
# List organizations
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/make/api/v2/organizations')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/make/api/v2/
```

Only the endpoints listed in the API Reference section below are supported. The gateway proxies requests to your Make zone (e.g., `us2.make.com`) and automatically injects your API token.

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

## Connection Management (Maton Platform)

The following endpoints are Maton platform operations for managing the OAuth connection to Make — they are not part of the Make API itself. Only the endpoints listed in the API Reference section below are proxied to Make.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=make&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'make'}).encode()
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
    "creation_time": "2026-04-07T19:37:17.340922Z",
    "last_updated_time": "2026-04-07T19:40:00.806379Z",
    "url": "https://connect.maton.ai/?session_token=REDACTED",
    "app": "make",
    "metadata": {}
  }
}
```

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

If you have multiple Make connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/make/api/v2/organizations')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to scenarios, organizations, teams, connections, data stores, hooks, and templates within the authenticated Make account.
- **All write operations require explicit user approval.** Before executing any create, update, start, stop, or delete call, confirm the target resource ID and intended effect with the user.
- **Persistent resources**: Creating or modifying scenarios, hooks, data stores, and connections creates resources that continue operating after the conversation ends. Starting a scenario activates ongoing automation.
- **Organizational scope**: Organization and team management operations (create/update/delete organizations, teams) affect shared resources visible to all members. Always confirm before modifying shared resources.

## API Reference

### Users

#### Get Current User

```bash
GET /make/api/v2/users/me
```

**Response:**
```json
{
  "authUser": {
    "id": 2958000,
    "name": "John Doe",
    "email": "john@example.com",
    "language": "en",
    "timezoneId": 301,
    "timezone": "America/New_York",
    "avatar": "https://..."
  }
}
```

#### List Users

```bash
GET /make/api/v2/users?organizationId={organizationId}
GET /make/api/v2/users?teamId={teamId}
```

#### Update User

```bash
PATCH /make/api/v2/users/{userId}
Content-Type: application/json

{
  "name": "Updated Name",
  "language": "en",
  "timezoneId": 301
}
```

### Organizations

#### List Organizations

```bash
GET /make/api/v2/organizations
```

**Response:**
```json
{
  "organizations": [
    {
      "id": 2767268,
      "name": "My Organization",
      "timezoneId": 301,
      "zone": "us2.make.com"
    }
  ],
  "pg": {"sortBy": "name", "limit": 10000, "sortDir": "asc", "offset": 0}
}
```

#### Get Organization

```bash
GET /make/api/v2/organizations/{organizationId}
```

#### Create Organization

```bash
POST /make/api/v2/organizations
Content-Type: application/json

{
  "name": "New Organization",
  "regionId": 2,
  "timezoneId": 301,
  "countryId": 202
}
```

#### Update Organization

```bash
PATCH /make/api/v2/organizations/{organizationId}
Content-Type: application/json

{
  "name": "Updated Name",
  "timezoneId": 301
}
```

#### Delete Organization

```bash
DELETE /make/api/v2/organizations/{organizationId}
```

#### Get Organization Usage

```bash
GET /make/api/v2/organizations/{organizationId}/usage
```

### Teams

#### List Teams

```bash
GET /make/api/v2/teams?organizationId={organizationId}
```

**Response:**
```json
{
  "teams": [
    {
      "id": 388889,
      "name": "My Team",
      "organizationId": 2767268
    }
  ],
  "pg": {"sortBy": "name", "limit": 10000, "sortDir": "asc", "offset": 0}
}
```

#### Get Team

```bash
GET /make/api/v2/teams/{teamId}
```

#### Create Team

```bash
POST /make/api/v2/teams
Content-Type: application/json

{
  "name": "New Team",
  "organizationId": 2767268
}
```

#### Delete Team

```bash
DELETE /make/api/v2/teams/{teamId}
```

#### Get Team Usage

```bash
GET /make/api/v2/teams/{teamId}/usage
```

### Scenarios

#### List Scenarios

```bash
GET /make/api/v2/scenarios?organizationId={organizationId}
GET /make/api/v2/scenarios?teamId={teamId}
```

**Response:**
```json
{
  "scenarios": [
    {
      "id": 4667499,
      "name": "My Scenario",
      "teamId": 388889,
      "isActive": false,
      "isPaused": false,
      "scheduling": {"type": "indefinitely", "interval": 900},
      "lastEdit": "2026-04-07T19:41:51.801Z"
    }
  ],
  "pg": {"sortBy": "proprietal", "limit": 500, "sortDir": "desc", "offset": 0}
}
```

#### Get Scenario

```bash
GET /make/api/v2/scenarios/{scenarioId}
```

#### Create Scenario

```bash
POST /make/api/v2/scenarios
Content-Type: application/json

{
  "teamId": 388889,
  "name": "New Scenario",
  "blueprint": "{...}"
}
```

#### Update Scenario

```bash
PATCH /make/api/v2/scenarios/{scenarioId}
Content-Type: application/json

{
  "name": "Updated Scenario Name"
}
```

#### Delete Scenario

```bash
DELETE /make/api/v2/scenarios/{scenarioId}
```

#### Start Scenario

```bash
POST /make/api/v2/scenarios/{scenarioId}/start
```

#### Stop Scenario

```bash
POST /make/api/v2/scenarios/{scenarioId}/stop
```

#### Run Scenario

```bash
POST /make/api/v2/scenarios/{scenarioId}/run
Content-Type: application/json

{
  "data": {"key": "value"}
}
```

#### Get Scenario Logs

```bash
GET /make/api/v2/scenarios/{scenarioId}/logs
GET /make/api/v2/scenarios/{scenarioId}/logs?status=3&pg[limit]=10
```

Query parameters:
- `from` / `to` - Timestamp range in milliseconds
- `status` - 1=success, 2=warning, 3=error
- `pg[offset]`, `pg[limit]` - Pagination

### Connections (Make App Connections)

#### List Connections

```bash
GET /make/api/v2/connections?teamId={teamId}
```

**Response:**
```json
{
  "connections": [
    {
      "id": 1353452,
      "name": "My HubSpot CRM connection",
      "accountName": "hubspotcrm",
      "accountLabel": "HubSpot CRM",
      "teamId": 388889,
      "accountType": "oauth",
      "editable": true
    }
  ]
}
```

#### Get Connection

```bash
GET /make/api/v2/connections/{connectionId}
```

#### Create Connection

```bash
POST /make/api/v2/connections
Content-Type: application/json

{
  "accountName": "slack2",
  "accountType": "oauth",
  "teamId": 388889
}
```

#### Update Connection

```bash
PATCH /make/api/v2/connections/{connectionId}
Content-Type: application/json

{
  "name": "Updated Connection Name"
}
```

#### Delete Connection

```bash
DELETE /make/api/v2/connections/{connectionId}
```

#### Test Connection

```bash
POST /make/api/v2/connections/{connectionId}/test
```

### Data Stores

#### List Data Stores

```bash
GET /make/api/v2/data-stores?teamId={teamId}
```

**Response:**
```json
{
  "dataStores": [],
  "pg": {"sortBy": "name", "limit": 10000, "sortDir": "asc", "offset": 0}
}
```

#### Get Data Store

```bash
GET /make/api/v2/data-stores/{dataStoreId}
```

#### Create Data Store

```bash
POST /make/api/v2/data-stores
Content-Type: application/json

{
  "name": "My Data Store",
  "teamId": 388889,
  "datastructureId": 12345,
  "maxSizeMB": 10
}
```

#### Update Data Store

```bash
PATCH /make/api/v2/data-stores/{dataStoreId}
Content-Type: application/json

{
  "name": "Updated Name",
  "maxSizeMB": 20
}
```

#### Delete Data Stores

```bash
DELETE /make/api/v2/data-stores?teamId={teamId}
Content-Type: application/json

{
  "ids": [12345, 67890]
}
```

### Hooks (Webhooks)

#### List Hooks

```bash
GET /make/api/v2/hooks?teamId={teamId}
```

**Response:**
```json
{
  "hooks": [],
  "pg": {"sortBy": "name", "limit": 50, "sortDir": "asc", "offset": 0}
}
```

#### Get Hook

```bash
GET /make/api/v2/hooks/{hookId}
```

#### Create Hook

```bash
POST /make/api/v2/hooks
Content-Type: application/json

{
  "name": "My Webhook",
  "teamId": 388889,
  "typeName": "web",
  "method": "POST",
  "headers": {},
  "stringify": false
}
```

#### Update Hook

```bash
PATCH /make/api/v2/hooks/{hookId}
Content-Type: application/json

{
  "name": "Updated Hook Name"
}
```

#### Delete Hook

```bash
DELETE /make/api/v2/hooks/{hookId}
```

#### Enable/Disable Hook

```bash
POST /make/api/v2/hooks/{hookId}/enable
POST /make/api/v2/hooks/{hookId}/disable
```

#### Ping Hook

```bash
GET /make/api/v2/hooks/{hookId}/ping
```

### Templates

#### List Templates

```bash
GET /make/api/v2/templates?teamId={teamId}
```

**Response:**
```json
{
  "templates": [],
  "pg": {"sortBy": "id", "limit": 10, "sortDir": "asc", "offset": 0}
}
```

#### Get Template

```bash
GET /make/api/v2/templates/{templateId}
```

#### Get Template Blueprint

```bash
GET /make/api/v2/templates/{templateId}/blueprint
```

#### Delete Template

```bash
DELETE /make/api/v2/templates/{templateId}
```

### Incomplete Executions (DLQs)

#### List Incomplete Executions

```bash
GET /make/api/v2/dlqs?scenarioId={scenarioId}
```

**Response:**
```json
{
  "dlqs": [],
  "pg": {"sortBy": "", "limit": 50, "sortDir": "asc", "offset": 0}
}
```

#### Get Incomplete Execution

```bash
GET /make/api/v2/dlqs/{dlqId}
```

#### Retry Incomplete Execution

```bash
POST /make/api/v2/dlqs/{dlqId}/retry
```

#### Delete Incomplete Executions

```bash
DELETE /make/api/v2/dlqs?scenarioId={scenarioId}
Content-Type: application/json

{
  "ids": [12345, 67890]
}
```

## Pagination

Make uses offset-based pagination with `pg` parameters:

```bash
GET /make/api/v2/scenarios?organizationId=123&pg[offset]=0&pg[limit]=50&pg[sortBy]=name&pg[sortDir]=asc
```

**Parameters:**
- `pg[offset]` - Number of items to skip (default: 0)
- `pg[limit]` - Max items per page (varies by endpoint)
- `pg[sortBy]` - Field to sort by
- `pg[sortDir]` - Sort direction: `asc` or `desc`

**Response includes pagination metadata:**
```json
{
  "scenarios": [...],
  "pg": {
    "sortBy": "name",
    "limit": 500,
    "sortDir": "asc",
    "offset": 0,
    "returnTotalCount": false
  }
}
```

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/make/api/v2/organizations',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.organizations);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://api.maton.ai/make/api/v2/scenarios',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'organizationId': 2767268}
)
scenarios = response.json()['scenarios']
```

### List Scenarios and Start One

```python
import os
import requests

headers = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
    'Content-Type': 'application/json'
}

# List scenarios
response = requests.get(
    'https://api.maton.ai/make/api/v2/scenarios',
    headers=headers,
    params={'organizationId': 2767268}
)
scenarios = response.json()['scenarios']

# Display inactive scenarios for user selection
inactive = [s for s in scenarios if not s['isActive']]
for i, s in enumerate(inactive):
    print(f"{i+1}. {s['name']} (ID: {s['id']})")

# Start a specific scenario after user confirms
scenario_id = inactive[0]['id']  # Replace with user-selected ID
requests.post(
    f'https://api.maton.ai/make/api/v2/scenarios/{scenario_id}/start',
    headers=headers
)
print(f"Started scenario: {inactive[0]['name']}")
```

## Notes

- Make uses zone-specific URLs (e.g., `us1.make.com`, `eu1.make.com`) - Maton handles routing automatically
- Most list endpoints require either `organizationId` or `teamId` parameter
- Scenario IDs, team IDs, and organization IDs are integers
- Timestamps use ISO 8601 format
- Some operations (like getting individual scenarios) may require OAuth instead of API key authentication
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq`, environment variables may not expand correctly in some shells

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Make connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 403 | Permission denied or forbidden operation |
| 404 | Resource not found |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Make API |

## Resources

- [Make API Documentation](https://developers.make.com/api-documentation)
- [Make API Reference](https://developers.make.com/api-documentation/api-reference)
- [Make Help Center](https://www.make.com/en/help)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
