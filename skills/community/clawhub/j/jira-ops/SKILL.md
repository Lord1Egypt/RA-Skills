---
name: jira-ops
description: "Retrieve, analyze, and update Jira tickets directly. Supports MCP-based (recommended) and direct REST API approaches. Trigger phrases: fetch Jira ticket, update ticket status, add comment, transition issue, search Jira, extract acceptance criteria. Adapted from everything-claude-code by @affaan-m (MIT)"
metadata: {"clawdbot":{"emoji":"🎫","requires":{"bins":[],"env":["JIRA_URL","JIRA_EMAIL","JIRA_API_TOKEN"]},"os":["linux","darwin","win32"]}}
---

# Jira Integration

Retrieve, analyze, and update Jira tickets with MCP or direct REST API.

## When to Activate

- Fetching ticket requirements and acceptance criteria
- Adding progress comments or status updates
- Transitioning ticket status (To Do → In Progress → Done)
- Searching for issues via JQL queries
- Linking PRs or branches to tickets

## Setup

### Option A: MCP Server (Recommended)

Install `mcp-atlassian` via `uvx`:

```json
{
  "jira": {
    "command": "uvx",
    "args": ["mcp-atlassian==0.21.0"],
    "env": {
      "JIRA_URL": "https://YOUR_ORG.atlassian.net",
      "JIRA_EMAIL": "your.email@example.com",
      "JIRA_API_TOKEN": "your-api-token"
    }
  }
}
```

Get your API token: https://id.atlassian.com/manage-profile/security/api-tokens

### Option B: Direct REST API

Set these environment variables:
- `JIRA_URL` — Jira instance URL
- `JIRA_EMAIL` — Your account email
- `JIRA_API_TOKEN` — API token (never hardcode)

## MCP Tools

With `mcp-atlassian` configured:

- `jira_search` — JQL queries
- `jira_get_issue` — Fetch issue details
- `jira_create_issue` — Create new issues
- `jira_update_issue` — Update fields
- `jira_transition_issue` — Change status
- `jira_add_comment` — Add comments
- `jira_get_transitions` — List available transitions

## Analyzing Tickets

Extract from tickets:
- **Functional requirements** — What needs to be built
- **Acceptance criteria** — Testable conditions
- **Test types** — Unit, integration, E2E
- **Edge cases** — Error scenarios, boundary conditions
- **Dependencies** — Linked issues, APIs, systems

## Updating Tickets

| Workflow | Jira Action |
|----------|-------------|
| Start work | Transition to "In Progress" + comment branch name |
| Tests done | Comment with test coverage summary |
| PR created | Comment with link, transition if needed |
| Merged | Transition to "Done" |

## Security

- Never hardcode API tokens
- Use environment variables or secrets manager
- Add `.env` to `.gitignore`
- Rotate tokens if exposed
- Use least-privilege scopes
