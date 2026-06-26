---
name: netlify
description: |
  Netlify API integration with managed OAuth. View sites, deploys, builds, DNS zones, and environment variables.
  Use this skill when users want to view Netlify site information, check deploy status, or review build logs. Write operations (creating sites, triggering builds, modifying DNS or env vars) require explicit user approval with specific resource identifiers.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: https://maton.ai
    requires:
      env:
        - MATON_API_KEY
---

# Netlify

Access the Netlify API with managed OAuth authentication. View sites, deploys, builds, DNS zones, environment variables, and webhooks. Administrative write operations require explicit approval.

## Quick Start

```bash
# List all sites
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/netlify/api/v1/sites')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/netlify/{native-api-path}
```

The gateway proxies requests to `api.netlify.com` and automatically injects your OAuth token. Only the endpoints documented in this skill are supported — always use specific endpoint paths from the API Reference section below rather than constructing arbitrary paths.

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

Manage your Netlify OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=netlify&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'netlify'}).encode()
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
    "creation_time": "2026-02-12T11:15:33.183756Z",
    "last_updated_time": "2026-02-12T11:15:51.556556Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "netlify",
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

If you have multiple Netlify connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/netlify/api/v1/sites')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to sites, deploys, forms, submissions, and DNS within the connected Netlify account. Only install if you need Netlify administration. Prefer least-privilege OAuth access where available and review scopes before authorizing.
- **Default to read-only operations.** Always start by listing or retrieving resources to confirm account, site, and resource identifiers before proposing any changes.
- **All write operations require explicit user approval with specific identifiers.** Before executing any create, update, or delete call:
  1. Retrieve and display the target resource (site name/ID, deploy ID, DNS zone, env var key) so the user can verify.
  2. Clearly describe the intended effect (e.g., "This will delete site 'my-production-app' (site_id: abc123) and all its deploys").
  3. Wait for explicit user confirmation before proceeding.
- **High-impact operations require extra caution.** Deleting sites, modifying DNS zones/records, changing environment variables, and triggering production builds can affect live websites. These actions must include a summary of consequences and require confirmation.
- **Prefer reversible actions.** Use deploy locking over deletion, and rollback (restore deploy) over redeploying. Always confirm destructive operations like site deletion or DNS zone removal.

## API Reference

### User & Accounts

#### Get Current User

```bash
GET /netlify/api/v1/user
```

#### List Accounts

```bash
GET /netlify/api/v1/accounts
```

#### Get Account

```bash
GET /netlify/api/v1/accounts/{account_id}
```

### Sites

#### List Sites

```bash
GET /netlify/api/v1/sites
```

With filtering:

```bash
GET /netlify/api/v1/sites?filter=all&page=1&per_page=100
```

#### Get Site

```bash
GET /netlify/api/v1/sites/{site_id}
```

#### Create Site

```bash
POST /netlify/api/v1/{account_slug}/sites
Content-Type: application/json

{
  "name": "my-new-site"
}
```

#### Update Site

```bash
PUT /netlify/api/v1/sites/{site_id}
Content-Type: application/json

{
  "name": "updated-site-name"
}
```

#### Delete Site

```bash
DELETE /netlify/api/v1/sites/{site_id}
```

### Deploys

#### List Deploys

```bash
GET /netlify/api/v1/sites/{site_id}/deploys
```

#### Get Deploy

```bash
GET /netlify/api/v1/deploys/{deploy_id}
```

#### Create Deploy

```bash
POST /netlify/api/v1/sites/{site_id}/deploys
Content-Type: application/json

{
  "title": "Deploy from API"
}
```

#### Lock Deploy

```bash
POST /netlify/api/v1/deploys/{deploy_id}/lock
```

#### Unlock Deploy

```bash
POST /netlify/api/v1/deploys/{deploy_id}/unlock
```

#### Restore Deploy (Rollback)

```bash
PUT /netlify/api/v1/deploys/{deploy_id}
```

### Builds

#### List Builds

```bash
GET /netlify/api/v1/sites/{site_id}/builds
```

#### Get Build

```bash
GET /netlify/api/v1/builds/{build_id}
```

#### Trigger Build

```bash
POST /netlify/api/v1/sites/{site_id}/builds
```

### Environment Variables

Environment variables are managed at the account level with optional site scope.

#### List Environment Variables

```bash
GET /netlify/api/v1/accounts/{account_id}/env?site_id={site_id}
```

#### Create Environment Variables

```bash
POST /netlify/api/v1/accounts/{account_id}/env?site_id={site_id}
Content-Type: application/json

[
  {
    "key": "MY_VAR",
    "values": [
      {"value": "my_value", "context": "all"}
    ]
  }
]
```

**Context values:** `all`, `production`, `deploy-preview`, `branch-deploy`, `dev`

#### Update Environment Variable

```bash
PUT /netlify/api/v1/accounts/{account_id}/env/{key}?site_id={site_id}
Content-Type: application/json

{
  "key": "MY_VAR",
  "values": [
    {"value": "updated_value", "context": "all"}
  ]
}
```

#### Delete Environment Variable

```bash
DELETE /netlify/api/v1/accounts/{account_id}/env/{key}?site_id={site_id}
```

### DNS Zones

#### List DNS Zones

```bash
GET /netlify/api/v1/dns_zones
```

#### Create DNS Zone

```bash
POST /netlify/api/v1/dns_zones
Content-Type: application/json

{
  "name": "example.com",
  "account_slug": "my-account"
}
```

#### Get DNS Zone

```bash
GET /netlify/api/v1/dns_zones/{zone_id}
```

#### Delete DNS Zone

```bash
DELETE /netlify/api/v1/dns_zones/{zone_id}
```

### DNS Records

#### List DNS Records

```bash
GET /netlify/api/v1/dns_zones/{zone_id}/dns_records
```

#### Create DNS Record

```bash
POST /netlify/api/v1/dns_zones/{zone_id}/dns_records
Content-Type: application/json

{
  "type": "A",
  "hostname": "www",
  "value": "192.0.2.1",
  "ttl": 3600
}
```

#### Delete DNS Record

```bash
DELETE /netlify/api/v1/dns_zones/{zone_id}/dns_records/{record_id}
```

### Build Hooks

#### List Build Hooks

```bash
GET /netlify/api/v1/sites/{site_id}/build_hooks
```

#### Create Build Hook

```bash
POST /netlify/api/v1/sites/{site_id}/build_hooks
Content-Type: application/json

{
  "title": "My Build Hook",
  "branch": "main"
}
```

Response includes a `url` that can be POSTed to trigger a build.

#### Delete Build Hook

```bash
DELETE /netlify/api/v1/sites/{site_id}/build_hooks/{hook_id}
```

### Webhooks

#### List Webhooks

```bash
GET /netlify/api/v1/hooks?site_id={site_id}
```

#### Create Webhook

```bash
POST /netlify/api/v1/hooks?site_id={site_id}
Content-Type: application/json

{
  "type": "url",
  "event": "deploy_created",
  "data": {
    "url": "https://example.com/webhook"
  }
}
```

**Events:** `deploy_created`, `deploy_building`, `deploy_failed`, `deploy_succeeded`, `form_submission`

#### Delete Webhook

```bash
DELETE /netlify/api/v1/hooks/{hook_id}
```

### Forms

#### List Forms

```bash
GET /netlify/api/v1/sites/{site_id}/forms
```

#### List Form Submissions

```bash
GET /netlify/api/v1/sites/{site_id}/submissions
```

#### Delete Form

```bash
DELETE /netlify/api/v1/sites/{site_id}/forms/{form_id}
```

### Functions

#### List Functions

```bash
GET /netlify/api/v1/sites/{site_id}/functions
```

### Services/Add-ons

#### List Available Services

```bash
GET /netlify/api/v1/services
```

#### Get Service Details

```bash
GET /netlify/api/v1/services/{service_id}
```

## Pagination

Use `page` and `per_page` query parameters:

```bash
GET /netlify/api/v1/sites?page=1&per_page=100
```

Default `per_page` varies by endpoint. Check response headers for pagination info.

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/netlify/api/v1/sites',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const sites = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://api.maton.ai/netlify/api/v1/sites',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
sites = response.json()
```

### Create Site and Set Environment Variable

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

# Create site
site = requests.post(
    'https://api.maton.ai/netlify/api/v1/my-account/sites',
    headers=headers,
    json={'name': 'my-new-site'}
).json()

# Add environment variable
requests.post(
    f'https://api.maton.ai/netlify/api/v1/accounts/{site["account_id"]}/env',
    headers=headers,
    params={'site_id': site['id']},
    json=[{'key': 'API_KEY', 'values': [{'value': 'secret', 'context': 'all'}]}]
)
```

## Notes

- Site IDs are UUIDs (e.g., `d37d1ce4-5444-40f5-a4ca-a2c40a8b6835`)
- Account slugs are used for creating sites within a team (e.g., `my-team-slug`)
- Deploy IDs are returned when creating deploys and can be used to track deploy status
- Build hooks return a URL that can be POSTed to externally trigger builds
- Environment variable contexts control where variables are available: `all`, `production`, `deploy-preview`, `branch-deploy`, `dev`
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Netlify connection |
| 401 | Invalid or missing Maton API key |
| 404 | Resource not found |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Netlify API |

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

1. Ensure your URL path starts with `netlify`. For example:

- Correct: `https://api.maton.ai/netlify/api/v1/sites`
- Incorrect: `https://api.maton.ai/api/v1/sites`

## Resources

- [Netlify API Documentation](https://open-api.netlify.com/)
- [Netlify CLI](https://docs.netlify.com/cli/get-started/)
- [Netlify Build Hooks](https://docs.netlify.com/configure-builds/build-hooks/)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
