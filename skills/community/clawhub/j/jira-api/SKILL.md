---
name: jira
description: |
  Jira API integration with managed OAuth. Search issues with JQL, create and update issues, manage projects and transitions. Use this skill when users want to interact with Jira issues, projects, or workflows. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Jira

Access the Jira Cloud API with managed OAuth authentication. Search issues with JQL, create and manage issues, and automate workflows.

## Quick Start

**CLI:**

```bash
maton jira issue search 'project = PROJ AND status = "In Progress"' --cloud-id abc-123
```

```bash
maton api '/jira/ex/jira/{cloudId}/rest/api/3/search/jql?jql=project%3DKEY&maxResults=10'
```

**Python:**

```bash
# First, get your cloud ID
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/jira/oauth/token/accessible-resources')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF

# Then search issues
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/jira/ex/jira/{cloudId}/rest/api/3/search/jql?jql=project%3DKEY&maxResults=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/jira/{native-api-path}
```

Maton proxies requests to `api.atlassian.com` and automatically injects your OAuth token.

## Getting Cloud ID

Jira Cloud requires a cloud ID. Get it first:

```bash
GET /jira/oauth/token/accessible-resources
```

Example:

```bash
maton jira cloud list
```

Response:

```json
[{
  "id": "62909843-b784-4c35-b770-e4e2a26f024b",
  "url": "https://yoursite.atlassian.net",
  "name": "yoursite"
}]
```

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

Manage your Jira OAuth connections at `https://api.maton.ai`.

### List Connections

**CLI:**

```bash
maton connection list jira --status ACTIVE
```

```bash
maton api -X GET /connections -f app=jira -f status=ACTIVE
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=jira&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

**CLI:**

```bash
maton connection create jira
```

```bash
maton api /connections -f app=jira
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'jira'}).encode()
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
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "jira",
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

If you have multiple Jira connections, specify which one to use:

**CLI:**

```bash
maton jira project list --cloud-id abc-123 --connection {connection_id}
```

```bash
maton api /jira/ex/jira/{cloudId}/rest/api/3/project --connection {connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/jira/ex/jira/{cloudId}/rest/api/3/project')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always specify the connection to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to issues, projects, boards, sprints, and users within the connected Jira account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference

### Projects

#### List Projects

```bash
GET /jira/ex/jira/{cloudId}/rest/api/3/project
```

Example:

```bash
maton jira project list --cloud-id abc-123
```

#### Get Project

```bash
GET /jira/ex/jira/{cloudId}/rest/api/3/project/{projectKeyOrId}
```

Example:

```bash
maton jira project view PROJ --cloud-id abc-123
```

### Issues

#### Search Issues (JQL)

```bash
GET /jira/ex/jira/{cloudId}/rest/api/3/search/jql?jql=project%3DPROJ%20order%20by%20created%20DESC&maxResults=20&fields=summary,status,assignee
```

Example:

```bash
maton jira issue search 'project = PROJ order by created DESC' --cloud-id abc-123 --limit 20 --fields summary,status,assignee
```

#### Get Issue

```bash
GET /jira/ex/jira/{cloudId}/rest/api/3/issue/{issueIdOrKey}
```

Example:

```bash
maton jira issue view PROJ-123 --cloud-id abc-123
```

#### Create Issue

```bash
POST /jira/ex/jira/{cloudId}/rest/api/3/issue
Content-Type: application/json

{
  "fields": {
    "project": {"key": "PROJ"},
    "summary": "Fix login",
    "issuetype": {"name": "Task"}
  }
}
```

Example:

```bash
maton jira issue create --cloud-id abc-123 --project PROJ --summary 'Fix login' --type Task
```

#### Update Issue

```bash
PUT /jira/ex/jira/{cloudId}/rest/api/3/issue/{issueIdOrKey}
Content-Type: application/json

{
  "fields": {
    "summary": "Updated summary"
  }
}
```

Example:

```bash
maton jira issue update PROJ-123 --cloud-id abc-123 --summary 'Updated summary'
```

#### Delete Issue

```bash
DELETE /jira/ex/jira/{cloudId}/rest/api/3/issue/{issueIdOrKey}
```

Example:

```bash
maton jira issue delete PROJ-123 --cloud-id abc-123
```

#### Assign Issue

```bash
PUT /jira/ex/jira/{cloudId}/rest/api/3/issue/{issueIdOrKey}/assignee
Content-Type: application/json

{
  "accountId": "712020:5aff718e-6fe0-4548-82f4-f44ec481e5e7"
}
```

Example:

```bash
maton jira issue update PROJ-123 --cloud-id abc-123 --assignee 712020:5aff718e-6fe0-4548-82f4-f44ec481e5e7
```

### Transitions

#### Get Transitions

```bash
GET /jira/ex/jira/{cloudId}/rest/api/3/issue/{issueIdOrKey}/transitions
```

Example:

```bash
maton jira transition list PROJ-123 --cloud-id abc-123
```

#### Transition Issue (change status)

```bash
POST /jira/ex/jira/{cloudId}/rest/api/3/issue/{issueIdOrKey}/transitions
Content-Type: application/json

{
  "transition": {"id": "31"}
}
```

Example:

```bash
maton jira transition apply PROJ-123 --cloud-id abc-123 --id 31
```

### Comments

#### Get Comments

```bash
GET /jira/ex/jira/{cloudId}/rest/api/3/issue/{issueIdOrKey}/comment
```

Example:

```bash
maton jira comment list PROJ-123 --cloud-id abc-123
```

#### Add Comment

```bash
POST /jira/ex/jira/{cloudId}/rest/api/3/issue/{issueIdOrKey}/comment
Content-Type: application/json

{
  "body": {
    "type": "doc",
    "version": 1,
    "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Comment text"}]}]
  }
}
```

Example:

```bash
maton jira comment add PROJ-123 --cloud-id abc-123 --body 'Comment text'
```

### Users

#### Get Current User

```bash
GET /jira/ex/jira/{cloudId}/rest/api/3/myself
```

Example:

```bash
maton jira whoami --cloud-id abc-123
```

#### Search Users

```bash
GET /jira/ex/jira/{cloudId}/rest/api/3/user/search?query=john
```

Example:

```bash
maton jira user search john --cloud-id abc-123
```

### Metadata

#### List Issue Types

```bash
GET /jira/ex/jira/{cloudId}/rest/api/3/issuetype
```

Example:

```bash
maton jira issuetype list --cloud-id abc-123
```

#### List Priorities

```bash
GET /jira/ex/jira/{cloudId}/rest/api/3/priority
```

Example:

```bash
maton jira priority list --cloud-id abc-123
```

#### List Statuses

```bash
GET /jira/ex/jira/{cloudId}/rest/api/3/status
```

Example:

```bash
maton jira status list --cloud-id abc-123
```

## Code Examples

### CLI

```bash
# Discover accessible Jira Cloud resources
maton jira cloud list

# Search issues with JQL
maton jira issue search 'project = PROJ AND status = "In Progress"' --cloud-id abc-123

# Filter with jq
maton jira issue search 'project = PROJ' --cloud-id abc-123 \
  --json --jq '.issues | map(select(.fields.status.name == "In Progress"))'

# Create an issue
maton jira issue create --cloud-id abc-123 --project PROJ --summary 'Fix login'
```

### JavaScript

```javascript
// Get cloud ID first
const resources = await fetch(
  'https://api.maton.ai/jira/oauth/token/accessible-resources',
  { headers: { 'Authorization': `Bearer ${process.env.MATON_API_KEY}` } }
).then(r => r.json());

const cloudId = resources[0].id;

// Search issues
const issues = await fetch(
  `https://api.maton.ai/jira/ex/jira/${cloudId}/rest/api/3/search/jql?jql=project=KEY`,
  { headers: { 'Authorization': `Bearer ${process.env.MATON_API_KEY}` } }
).then(r => r.json());
```

### Python

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

# Get cloud ID
resources = requests.get(
    'https://api.maton.ai/jira/oauth/token/accessible-resources',
    headers=headers
).json()

cloud_id = resources[0]['id']

# Search issues
issues = requests.get(
    f'https://api.maton.ai/jira/ex/jira/{cloud_id}/rest/api/3/search/jql',
    headers=headers,
    params={'jql': 'project=KEY', 'maxResults': 10}
).json()
```

## Notes

- Always fetch cloud ID first using `/oauth/token/accessible-resources`
- JQL queries must be bounded (e.g., `project=KEY`)
- Use URL encoding for JQL query parameters
- Update, Delete, Transition return HTTP 204 on success
- Agile API requires additional OAuth scopes. If you receive a scope error, contact Maton support at support@maton.ai with the specific operations/APIs you need and your use-case
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets (`fields[]`, `sort[]`, `records[]`) to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments. You may get "Invalid API key" errors when piping.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Jira connection or invalid JQL |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Jira API |

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

1. Ensure your URL path starts with `jira`. For example:

- Correct: `https://api.maton.ai/jira/ex/jira/{cloudId}/rest/api/3/project`
- Incorrect: `https://api.maton.ai/ex/jira/{cloudId}/rest/api/3/project`

## Resources

- [Jira API Introduction](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [Search Issues (JQL)](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-jql-get)
- [Get Issue](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-get)
- [Create Issue](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-post)
- [Transition Issue](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-transitions-post)
- [JQL Reference](https://support.atlassian.com/jira-service-management-cloud/docs/use-advanced-search-with-jira-query-language-jql/)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
