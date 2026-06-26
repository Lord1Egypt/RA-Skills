---
name: google-tag-manager
description: |
  Google Tag Manager API integration with managed OAuth. Manage GTM accounts, containers, workspaces, tags, triggers, and variables.
  Use this skill when users want to list or manage GTM containers, create or update tags and triggers, manage workspaces, publish container versions, or configure environments.
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

# Google Tag Manager

Access the Google Tag Manager API with managed OAuth authentication. Manage GTM accounts, containers, workspaces, tags, triggers, variables, environments, and container versions.

## Quick Start

```bash
# List all GTM accounts
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/google-tag-manager/tagmanager/v2/accounts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/google-tag-manager/{native-api-path}
```

Maton proxies requests to `tagmanager.googleapis.com` and automatically injects your OAuth token.

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

Manage your Google Tag Manager OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=google-tag-manager&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-tag-manager'}).encode()
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
    "app": "google-tag-manager",
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

If you have multiple Google Tag Manager connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/google-tag-manager/tagmanager/v2/accounts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to the GTM accounts and containers the connected Google account has permissions for.
- **All write operations require explicit user approval.** Before creating, updating, or deleting tags, triggers, variables, or publishing versions, confirm the target resource and intended effect with the user.
- **Publishing a container version makes changes live.** Always confirm with the user before publishing.

## API Reference

### Resource Path Pattern

GTM API v2 uses hierarchical paths:

```
accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/{resource}/{resourceId}
```

### Accounts

#### List Accounts

```bash
GET /google-tag-manager/tagmanager/v2/accounts
```

**Response:**
```json
{
  "account": [
    {
      "path": "accounts/6353461358",
      "accountId": "6353461358",
      "name": "My Company",
      "features": {
        "supportUserPermissions": true,
        "supportMultipleContainers": true
      }
    }
  ]
}
```

#### Get Account

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}
```

### Containers

#### List Containers

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers
```

**Response:**
```json
{
  "container": [
    {
      "path": "accounts/6353461358/containers/251407136",
      "accountId": "6353461358",
      "containerId": "251407136",
      "name": "example.com",
      "publicId": "GTM-XXXXXXX",
      "usageContext": ["web"],
      "tagIds": ["GTM-XXXXXXX"],
      "features": {
        "supportTags": true,
        "supportTriggers": true,
        "supportVariables": true,
        "supportVersions": true,
        "supportEnvironments": true,
        "supportWorkspaces": true,
        "supportFolders": true,
        "supportTemplates": true,
        "supportBuiltInVariables": true,
        "supportZones": true
      }
    }
  ]
}
```

#### Create Container

```bash
POST /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers
Content-Type: application/json

{
  "name": "New Container",
  "usageContext": ["web"]
}
```

**Valid usage contexts:** `web`, `android`, `ios`, `amp`

#### Delete Container

```bash
DELETE /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}
```

### Workspaces

#### List Workspaces

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces
```

**Response:**
```json
{
  "workspace": [
    {
      "path": "accounts/6353461358/containers/251407136/workspaces/2",
      "accountId": "6353461358",
      "containerId": "251407136",
      "workspaceId": "2",
      "name": "Default Workspace"
    }
  ]
}
```

#### Create Workspace

```bash
POST /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces
Content-Type: application/json

{
  "name": "My Feature Workspace",
  "description": "Working on new tracking features"
}
```

#### Get Workspace Status

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/status
```

#### Create Version from Workspace

```bash
POST /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}:create_version
Content-Type: application/json

{
  "name": "v2.0",
  "notes": "Added new tracking tags"
}
```

#### Delete Workspace

```bash
DELETE /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}
```

### Tags

#### List Tags

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/tags
```

#### Get Tag

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/tags/{tagId}
```

#### Create Tag

```bash
POST /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/tags
Content-Type: application/json

{
  "name": "Custom HTML Tag",
  "type": "html",
  "parameter": [
    {
      "type": "template",
      "key": "html",
      "value": "<script>console.log('hello');</script>"
    }
  ],
  "firingTriggerId": ["{triggerId}"]
}
```

**Common tag types:** `html` (Custom HTML), `ua` (Universal Analytics), `gaawc` (GA4 Config), `gaawe` (GA4 Event), `gclidw` (Conversion Linker), `img` (Custom Image)

**Example:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "name": "GA4 Config Tag",
    "type": "gaawc",
    "parameter": [
        {"type": "template", "key": "measurementId", "value": "G-XXXXXXXXXX"}
    ],
    "firingTriggerId": ["2147479553"]
}).encode()
req = urllib.request.Request('https://api.maton.ai/google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/tags', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### Update Tag

```bash
PUT /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/tags/{tagId}
Content-Type: application/json

{
  "name": "Updated Tag Name",
  "type": "html",
  "parameter": [...],
  "firingTriggerId": ["{triggerId}"],
  "fingerprint": "{current_fingerprint}"
}
```

Include the current `fingerprint` value to ensure you're updating the latest version.

#### Delete Tag

```bash
DELETE /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/tags/{tagId}
```

### Triggers

#### List Triggers

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/triggers
```

#### Create Trigger

```bash
POST /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/triggers
Content-Type: application/json

{
  "name": "All Pages",
  "type": "pageview"
}
```

**Common trigger types:** `pageview`, `domReady`, `windowLoaded`, `customEvent`, `click`, `linkClick`, `formSubmit`, `timer`, `scrollDepth`

**Example with filter:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "name": "Click on CTA Button",
    "type": "click",
    "filter": [
        {
            "type": "equals",
            "parameter": [
                {"type": "template", "key": "arg0", "value": "{{Click Classes}}"},
                {"type": "template", "key": "arg1", "value": "cta-button"}
            ]
        }
    ]
}).encode()
req = urllib.request.Request('https://api.maton.ai/google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/triggers', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### Update Trigger

```bash
PUT /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/triggers/{triggerId}
Content-Type: application/json

{
  "name": "Updated Trigger",
  "type": "pageview",
  "fingerprint": "{current_fingerprint}"
}
```

#### Delete Trigger

```bash
DELETE /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/triggers/{triggerId}
```

### Variables

#### List Variables

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/variables
```

#### Create Variable

```bash
POST /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/variables
Content-Type: application/json

{
  "name": "Data Layer Variable",
  "type": "v",
  "parameter": [
    {"type": "integer", "key": "dataLayerVersion", "value": "2"},
    {"type": "template", "key": "name", "value": "myDataLayerVar"}
  ]
}
```

**Common variable types:** `v` (Data Layer), `j` (JavaScript Variable), `jsm` (Custom JavaScript), `c` (Constant), `k` (Cookie), `u` (URL), `f` (DOM Element)

#### Update Variable

```bash
PUT /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/variables/{variableId}
Content-Type: application/json

{
  "name": "Updated Variable",
  "type": "v",
  "parameter": [...],
  "fingerprint": "{current_fingerprint}"
}
```

#### Delete Variable

```bash
DELETE /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/variables/{variableId}
```

### Built-In Variables

#### List Built-In Variables

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/built_in_variables
```

**Response:**
```json
{
  "builtInVariable": [
    {
      "path": "accounts/6353461358/containers/251407136/workspaces/2/built_in_variables",
      "type": "pageUrl",
      "name": "Page URL"
    },
    {
      "type": "pageHostname",
      "name": "Page Hostname"
    },
    {
      "type": "pagePath",
      "name": "Page Path"
    },
    {
      "type": "referrer",
      "name": "Referrer"
    },
    {
      "type": "event",
      "name": "Event"
    }
  ]
}
```

### Environments

#### List Environments

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/environments
```

#### Create Environment

```bash
POST /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/environments
Content-Type: application/json

{
  "name": "Staging",
  "description": "Staging environment for testing"
}
```

#### Delete Environment

```bash
DELETE /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/environments/{environmentId}
```

### Container Versions

#### List Version Headers

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/version_headers
```

#### Get Version

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/versions/{versionId}
```

#### Get Live Version

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/versions:live
```

#### Publish Version

```bash
POST /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/versions/{versionId}:publish
```

#### Delete Version

```bash
DELETE /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers/{containerId}/versions/{versionId}
```

### User Permissions

#### List User Permissions

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}/user_permissions
```

**Response:**
```json
{
  "userPermission": [
    {
      "path": "accounts/6353461358/user_permissions/05842032124443686272",
      "accountId": "6353461358",
      "emailAddress": "user@example.com",
      "accountAccess": {
        "permission": "admin"
      },
      "containerAccess": [
        {
          "containerId": "251407136",
          "permission": "publish"
        }
      ]
    }
  ]
}
```

#### Create User Permission

```bash
POST /google-tag-manager/tagmanager/v2/accounts/{accountId}/user_permissions
Content-Type: application/json

{
  "emailAddress": "newuser@example.com",
  "accountAccess": {
    "permission": "user"
  },
  "containerAccess": [
    {
      "containerId": "{containerId}",
      "permission": "read"
    }
  ]
}
```

**Permission levels:** `noAccess`, `read`, `edit`, `approve`, `publish` (container); `noAccess`, `user`, `admin` (account)

## Pagination

List endpoints use token-based pagination with `pageToken` parameter:

```bash
GET /google-tag-manager/tagmanager/v2/accounts/{accountId}/containers?pageToken={nextPageToken}
```

Response includes `nextPageToken` when more results exist.

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/google-tag-manager/tagmanager/v2/accounts',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.account);
```

### Python

```python
import os
import requests

# List accounts
response = requests.get(
    'https://api.maton.ai/google-tag-manager/tagmanager/v2/accounts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
accounts = response.json().get('account', [])

# List containers for first account
if accounts:
    account_id = accounts[0]['accountId']
    containers_resp = requests.get(
        f'https://api.maton.ai/google-tag-manager/tagmanager/v2/accounts/{account_id}/containers',
        headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
    )
    print(containers_resp.json())
```

## Notes

- All resources use hierarchical paths: `accounts/{id}/containers/{id}/workspaces/{id}/...`
- The `fingerprint` field is used for optimistic concurrency control; include it in update requests
- Updates (PUT) require the full resource body, not just changed fields
- The `usageContext` for containers can be `web`, `android`, `ios`, or `amp`
- Built-in trigger ID `2147479553` is the "All Pages" trigger available in all containers
- Publishing a version makes it live immediately on all sites using the container
- Workspaces provide draft isolation; changes are committed by creating a version
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Bad request (invalid parameters, malformed resource body) |
| 401 | Invalid or missing Maton API key |
| 403 | Forbidden (insufficient GTM permissions) |
| 404 | Resource not found |
| 409 | Conflict (fingerprint mismatch on update) |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Google Tag Manager API |

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

1. Ensure your URL path starts with `google-tag-manager`. For example:

- Correct: `https://api.maton.ai/google-tag-manager/tagmanager/v2/accounts`
- Incorrect: `https://api.maton.ai/tagmanager/v2/accounts`

## Resources

- [Tag Manager API Overview](https://developers.google.com/tag-platform/tag-manager/api/v2)
- [Tag Manager API Reference](https://developers.google.com/tag-platform/tag-manager/api/reference/rest)
- [Tag Manager Concepts](https://developers.google.com/tag-platform/tag-manager/api/v2/concept)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
