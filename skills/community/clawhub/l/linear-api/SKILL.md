---
name: linear
description: |
  Linear API integration with managed OAuth. Query and manage issues, projects, teams, cycles, and labels using GraphQL.
  Use this skill when users want to create, update, or query Linear issues, search for tasks, manage projects, or track work.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Linear

Access the Linear API with managed OAuth authentication. Query and manage issues, projects, teams, cycles, labels, and comments using GraphQL.

## Quick Start

**CLI:**

```bash
maton linear issue list -c ABC -L 10
```

```bash
maton api '/linear/graphql'
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': '{ viewer { id name email } }'}).encode()
req = urllib.request.Request('https://api.maton.ai/linear/graphql', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/linear/graphql
```

All requests use POST to the GraphQL endpoint. Maton proxies requests to `api.linear.app` and automatically injects your OAuth token.

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

Manage your Linear OAuth connections at `https://api.maton.ai`.

### List Connections

**CLI:**

```bash
maton connection list linear --status ACTIVE
```

```bash
maton api -X GET /connections -f app=linear -f status=ACTIVE
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=linear&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

**CLI:**

```bash
maton connection create linear
```

```bash
maton api /connections -f app=linear
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'linear'}).encode()
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
    "creation_time": "2026-02-04T23:03:22.676001Z",
    "last_updated_time": "2026-02-04T23:03:51.239577Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "linear",
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

If you have multiple Linear connections, specify which one to use:

**CLI:**

```bash
maton linear issue list -c ABC --connection {connection_id}
```

```bash
maton api /linear/graphql --connection {connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': '{ viewer { id name } }'}).encode()
req = urllib.request.Request('https://api.maton.ai/linear/graphql', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always specify the connection to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to issues, projects, teams, cycles, and comments within the connected Linear account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference

Linear uses a GraphQL API. All operations are sent as POST requests with a JSON body containing the `query` field.

### Viewer (Current User)

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ viewer { id name email } }"}
```

Example:

```bash
maton linear whoami
```

### Organization

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ organization { id name urlKey } }"}
```

Example:

```bash
maton linear org view
```

### Teams

#### List Teams

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ teams { nodes { id name key } } }"}
```

Example:

```bash
maton linear team list
```

#### Get Team

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ team(id: \"ABC\") { id name key issues { nodes { id identifier title } } } }"}
```

Example:

```bash
maton linear team view ABC
```

### Issues

#### List Issues

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issues(first: 10, filter: { team: { key: { eq: \"ABC\" } } }) { nodes { id identifier title state { name } priority createdAt } pageInfo { hasNextPage endCursor } } }"}
```

Example:

```bash
maton linear issue list -c ABC -L 10
```

#### Get Issue by ID or Identifier

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issue(id: \"ABC-123\") { id identifier title description state { name } priority assignee { name } team { key name } createdAt updatedAt } }"}
```

Example:

```bash
maton linear issue view ABC-123
```

#### Filter Issues

Filter by state type:

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issues(first: 10, filter: { state: { type: { eq: \"started\" } } }) { nodes { id identifier title state { name type } } } }"}
```

Example:

```bash
maton linear issue list --state started -L 10
```

Filter by title:

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issues(first: 10, filter: { title: { containsIgnoreCase: \"bug\" } }) { nodes { id identifier title } } }"}
```

Example:

```bash
maton linear issue list --title bug -L 10
```

#### Search Issues

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ searchIssues(first: 10, term: \"shopify\") { nodes { id identifier title } } }"}
```

Example:

```bash
maton linear issue search shopify -L 10
```

#### Create Issue

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "mutation { issueCreate(input: { teamId: \"TEAM_ID\", title: \"New issue title\" }) { success issue { id identifier title state { name } } } }"}
```

Example:

```bash
maton linear issue create --team-id TEAM_ID -t 'New issue title'
```

#### Update Issue

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "mutation { issueUpdate(id: \"ABC-123\", input: { title: \"Updated title\", priority: 2 }) { success issue { id identifier title priority } } }"}
```

Example:

```bash
maton linear issue update ABC-123 -t 'Updated title' --priority 2
```

### Projects

#### List Projects

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ projects(first: 10) { nodes { id name state createdAt } } }"}
```

Example:

```bash
maton linear project list
```

### Cycles

#### List Cycles

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ cycles(first: 10) { nodes { id name number startsAt endsAt } } }"}
```

Example:

```bash
maton linear cycle list
```

### Labels

#### List Labels

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issueLabels(first: 20) { nodes { id name color } } }"}
```

Example:

```bash
maton linear label list
```

### Workflow States

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ workflowStates(first: 20) { nodes { id name type team { key } } } }"}
```

Example:

```bash
maton linear state list
```

### Users

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ users(first: 20) { nodes { id name email active } } }"}
```

Example:

```bash
maton linear user list
```

### Comments

#### List Comments

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issue(id: \"ABC-123\") { comments(first: 10) { nodes { id body createdAt user { name } } } } }"}
```

Example:

```bash
maton linear comment list --issue ABC-123 -L 10
```

#### Create Comment

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "mutation { commentCreate(input: { issueId: \"ABC-123\", body: \"Looking into this\" }) { success comment { id body } } }"}
```

Example:

```bash
maton linear comment create --issue ABC-123 -b 'Looking into this'
```

## Pagination

Linear uses Relay-style cursor-based pagination. The CLI automatically paginates with '--paginate'.

Example:

```bash
maton linear issue list -c ABC --paginate
```

## Code Examples

### CLI

```bash
# List issues for a team
maton linear issue list -c ABC -L 10

# View a specific issue
maton linear issue view ABC-123

# Create a new issue
maton linear issue create --team-id TEAM_ID -t 'Fix login'

# Add a comment
maton linear comment create --issue ABC-123 -b 'Looking into this'
```

### JavaScript

```javascript
const response = await fetch('https://api.maton.ai/linear/graphql', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: `{ issues(first: 10) { nodes { id identifier title state { name } } } }`
  })
});
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.post(
    'https://api.maton.ai/linear/graphql',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'query': '{ issues(first: 10) { nodes { id identifier title state { name } } } }'
    }
)
data = response.json()
```

## Notes

- Linear uses GraphQL exclusively (no REST API)
- Issue identifiers like `ABC-123` can be used in place of UUIDs for the `id` parameter
- Priority values: 0 = No priority, 1 = Urgent, 2 = High, 3 = Medium, 4 = Low
- Workflow state types: `backlog`, `unstarted`, `started`, `completed`, `canceled`
- The GraphQL schema is introspectable at `https://api.linear.app/graphql`
- Use `searchIssues(term: "...")` for full-text search across issues
- Some mutations (delete, create labels/projects) may require additional OAuth scopes. If you receive a scope error, contact Maton support at support@maton.ai with the specific operations/APIs you need and your use-case

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Linear connection or GraphQL validation error |
| 401 | Invalid or missing Maton API key |
| 403 | Insufficient OAuth scope for the operation |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Linear API |

GraphQL errors are returned in the `errors` array:

```json
{
  "errors": [
    {
      "message": "Invalid scope: `write` required",
      "extensions": {
        "type": "forbidden",
        "code": "FORBIDDEN",
        "statusCode": 403
      }
    }
  ]
}
```

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

1. Ensure your URL path starts with `linear`. For example:

- Correct: `https://api.maton.ai/linear/graphql`
- Incorrect: `https://api.maton.ai/graphql`

## Resources

- [Linear API Overview](https://linear.app/developers)
- [Linear GraphQL Getting Started](https://linear.app/developers/graphql)
- [Linear GraphQL Schema (Apollo Studio)](https://studio.apollographql.com/public/Linear-API/schema/reference?variant=current)
- [Linear API and Webhooks](https://linear.app/docs/api-and-webhooks)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
