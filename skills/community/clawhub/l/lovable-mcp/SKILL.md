---
name: lovable-mcp
description: >
 Use Lovable's MCP server to create, iterate on, and deploy full-stack web apps from natural-language prompts.
 Trigger this skill whenever the user wants to build a web app, dashboard, internal tool, prototype, landing page,
 or any frontend/full-stack project using Lovable — whether they say "Lovable" explicitly or just need a working
 app built and deployed fast. Also trigger when the user wants to manage Lovable projects programmatically:
 listing workspace projects, auditing edit history, reviewing diffs, reading project files, checking deployment
 status, managing databases, or setting AI governance policies. If the user mentions "Lovable," "lovable project,"
 "lovable app," or asks to build/ship/deploy a web app and Lovable is available as a connected MCP, use this skill.
 Even if they just say "make me an app" or "build a dashboard for X" — if the Lovable MCP is connected, this skill
 applies. Covers the full lifecycle: create → iterate → review → deploy.
metadata:
  {
    "openclaw":
      {
        "emoji": "🦞",
        "requires": { "tools": ["curl"] },
        "install":
          [
            {
              "id": "git",
              "kind": "manual",
              "label": "Clone the skill repository and install scripts",
            },
          ],
      },
  }
---

# Lovable MCP Server

Build, iterate, inspect, and deploy full-stack web apps through Lovable's MCP server — without ever opening the Lovable UI.

Lovable's agent handles the heavy lifting: you describe what you want in plain language, and it builds a working app (React + Vite + Tailwind + shadcn/ui + Supabase when needed). The MCP server exposes this capability programmatically, so you can drive the entire workflow from any agent that supports skills.

## What is Lovable MCP?

Lovable provides a Model Context Protocol (MCP) server at `https://mcp.lovable.dev` that gives AI agents direct access to:
- Create, read, update, and delete Lovable projects
- Send prompts to Lovable's AI agent for building/iterating on apps
- Deploy projects to production
- Read source code and review diffs
- Manage workspace-level governance
- Query analytics

**Authentication is OAuth 2.1+PKCE.** The MCP server supports the standard MCP OAuth flow:

1. Contact the server → receive `WWW-Authenticate: Bearer` challenge
2. Fetch OAuth metadata from `https://lovable.dev/oauth/.well-known/oauth-authorization-server`
3. Redirect user to the authorization endpoint with PKCE
4. Exchange the authorization code for tokens at the token endpoint
5. Use the access token as `Authorization: Bearer` in all subsequent calls

## Prerequisites

- A [Lovable](https://lovable.dev) account (Pro or Business plan recommended — needed for API access)
- A CLIENT_ID from Lovable support (email support@lovable.dev and ask for MCP OAuth client credentials)
- `curl` (should be available on any system)
- `python3` (for scripts, should be available on any system)

## Setup

### Step 1: Get credentials from Lovable

Contact Lovable support (`support@lovable.dev`) and request MCP OAuth client credentials. They will provide a **CLIENT_ID** (a hex string like `0123456789abcdef0123456789abcdef`).

This CLIENT_ID is registered with a specific redirect URI. The skill scripts use this redirect URI during the OAuth flow.

### Step 2: Run the OAuth setup

```bash
# Make the scripts executable
chmod +x scripts/*.sh

# Run the OAuth setup — this will generate a PKCE authorization URL for you
bash scripts/lovable-oauth-setup.sh
```

The script will:
1. Generate a cryptographically random PKCE code_verifier + code_challenge
2. Print an authorization URL for you to open in your browser
3. Wait for you to paste back the redirect URL containing the `?code=` parameter
4. Exchange the code for access + refresh tokens
5. Save the tokens to `config/lovable-tokens.json`

### Step 3: Test the connection

```bash
# Get the access token (auto-refreshes if expired)
TOKEN=$(bash scripts/lovable-get-token.sh)

# Test: list your profile and workspaces
curl -s -X POST https://mcp.lovable.dev/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_me","arguments":{}},"id":1}'
```

### Step 4: Configure your MCP server in OpenClaw

Add the Lovable MCP server to your `openclaw.json`:

```json
{
  "mcp": {
    "servers": {
      "lovable": {
        "url": "https://mcp.lovable.dev",
        "type": "http",
        "auth": {
          "CLIENT_ID": "<your-client-id>"
        }
      }
    }
  }
}
```

Then restart the gateway:
```bash
openclaw gateway restart
```

## OAuth Details

The OAuth flow uses **PKCE (Proof Key for Code Exchange)** as required by the MCP OAuth 2.1 specification.

### Authorization URL parameters

| Parameter | Value |
|-----------|-------|
| `response_type` | `code` |
| `client_id` | Your CLIENT_ID |
| `code_challenge_method` | `S256` |
| `code_challenge` | Base64URL(SHA256(code_verifier)) |
| `scope` | `offline projects:read projects:write projects:create workspaces:read workspaces:write` |
| `state` | Random anti-CSRF token |

### Token endpoint

Exchange the authorization code at `https://lovable.dev/oauth/token`:

| Parameter | Value |
|-----------|-------|
| `grant_type` | `authorization_code` |
| `code` | The authorization code from the redirect |
| `redirect_uri` | The registered redirect URI for your client |
| `client_id` | Your CLIENT_ID |
| `code_verifier` | The PKCE verifier you generated |

### Refresh token

When the access token expires (after 8 hours), use the refresh token:

```bash
curl -s -X POST https://lovable.dev/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=<your-refresh-token>" \
  -d "client_id=<your-client-id>" \
  -d "redirect_uri=<your-registered-redirect-uri>"
```

## How to Use

### 1. Find your workspace ID

```bash
TOKEN=$(bash scripts/lovable-get-token.sh)
curl -s -X POST https://mcp.lovable.dev/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"list_workspaces","arguments":{}},"id":1}'
```

### 2. List all projects

```bash
TOKEN=$(bash scripts/lovable-get-token.sh)
WORKSPACE_ID="<your-workspace-id>"

curl -s -X POST https://mcp.lovable.dev/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"tools/call\",\"params\":{\"name\":\"list_projects\",\"arguments\":{\"workspace_id\":\"$WORKSPACE_ID\"}},\"id\":1}"
```

### 3. Deploy a project

```bash
TOKEN=$(bash scripts/lovable-get-token.sh)
PROJECT_ID="<your-project-id>"

curl -s -X POST https://mcp.lovable.dev/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"tools/call\",\"params\":{\"name\":\"deploy_project\",\"arguments\":{\"project_id\":\"$PROJECT_ID\"}},\"id\":1}"
```

### 4. Send a prompt to the Lovable agent

```bash
TOKEN=$(bash scripts/lovable-get-token.sh)
PROJECT_ID="<your-project-id>"

curl -s -X POST https://mcp.lovable.dev/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"tools/call\",\"params\":{\"name\":\"send_message\",\"arguments\":{\"project_id\":\"$PROJECT_ID\",\"message\":\"Add a dark mode toggle to the header\"}},\"id\":1}"
```

## Deploy Workflow

Combine this skill with a CI/CD or agent workflow:

1. Code is reviewed and merged to `main` in your git repo
2. An agent (or CI) checks if the project exists on Lovable using `list_projects`
3. Agent asks the user for deploy approval
4. On approval, agent calls `deploy_project(project_id)`
5. Agent reports the production URL

## Tool Reference

### Project Operations

| Tool | Parameters | Description |
|------|-----------|-------------|
| `create_project` | `workspace_id` (required), `description` (required), `initial_message`, `tech_stack`, `visibility`, `template_project_id`, `selected_libraries` | Create a new Lovable project |
| `send_message` | `project_id` (required), `message` (required), `wait`, `timeout_seconds`, `plan_mode` | Send a prompt to the Lovable agent |
| `get_project` | `project_id` (required) | Get project details (URLs, latest commit, status) |
| `list_projects` | `workspace_id` (required), `query`, `visibility`, `sort_by`, `limit` | List/search all workspace projects |
| `deploy_project` | `project_id` (required), `name` (optional slug) | Publish current build to production |

### Code & History

| Tool | Parameters | Description |
|------|-----------|-------------|
| `list_files` | `project_id`, `ref` | List files at a git ref |
| `read_file` | `project_id`, `ref`, `path` | Read full file contents |
| `get_diff` | `project_id`, `message_id` | View diff for a specific edit |
| `list_edits` | `project_id` | Full edit history (reverse chronological) |
| `get_message` | `project_id`, `message_id` | Check status of a send_message |

### Workspace

| Tool | Parameters | Description |
|------|-----------|-------------|
| `list_workspaces` | (none) | List all workspaces |
| `get_workspace` | `workspace_id` (required) | Workspace details: plan, credits, members |
| `get_me` | (none) | Auth user profile |

### Database (Lovable Cloud)

| Tool | Parameters | Description |
|------|-----------|-------------|
| `get_database_status` | `project_id` (required) | Check if DB is enabled |
| `enable_database` | `project_id` (required) | Provision PostgreSQL |
| `query_database` | `project_id` (required), `query` (required) | Run SQL |

### Analytics

| Tool | Parameters | Description |
|------|-----------|-------------|
| `get_project_analytics` | `project_id`, `start_date`, `end_date` | Historical metrics |
| `get_project_analytics_trend` | `project_id` | Real-time visitors |

### Governance

| Tool | Parameters | Description |
|------|-----------|-------------|
| `get_workspace_knowledge` | `workspace_id` | Read AI governance policies |
| `set_workspace_knowledge` | `workspace_id`, `text` | Set workspace-wide AI rules |

### Connectors

| Tool | Parameters | Description |
|------|-----------|-------------|
| `list_connectors` | `workspace_id` | List connected services |
| `list_available_connectors` | `workspace_id` | Browse available connectors |
| `add_connector` | `connector_id` | Get URL to add a connector via dashboard |
| `remove_connector` | `workspace_id`, `connector_id` | Remove a connector |

## Common Patterns

### Build and deploy in one flow
1. `list_workspaces()` → get workspace_id
2. `create_project(workspace_id, description, initial_message)` → get project_id
3. `get_project(project_id)` → confirm it's built, get preview_url
4. `send_message(project_id, message)` → iterate if needed
5. `get_diff(project_id, message_id)` → review changes
6. `deploy_project(project_id)` → ship it

### Audit a workspace
1. `list_workspaces()` → get workspace_id
2. `list_projects(workspace_id)` → see all projects
3. For each project: `list_edits()`, `read_file()`, `get_database_status()`

## Troubleshooting

### Token expired
Run the token refresh script:
```bash
bash scripts/lovable-refresh-token.sh
```

### Refresh token also expired
If the refresh token no longer works, run the OAuth setup again:
```bash
bash scripts/lovable-oauth-setup.sh
```

### "Invalid API key" error
The Lovable MCP server uses OAuth 2.0 Bearer tokens, NOT the `Lovable-API-Key` header. The API key from Lovable support only works for `tools/list` (discovery). For `tools/call` you MUST use an OAuth Bearer token obtained through the PKCE flow.

### Connection refused / timeout
Verify the MCP server is reachable:
```bash
curl -s -o /dev/null -w "%{http_code}" https://mcp.lovable.dev/.well-known/oauth-protected-resource
```
Should return HTTP 200.

## Security Notes

- **Never commit tokens or credentials to git.** The `config/lovable-tokens.json` file should be in your `.gitignore`.
- The access token is a JWT that expires after 8 hours. The refresh token is a long-lived secret.
- If you suspect a token leak, revoke it by emailing Lovable support.
- The OAuth flow should be initiated interactively by a human — never automate the consent step.
