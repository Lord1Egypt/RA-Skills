# Nango Provider Reference

This file contains configuration details for popular API providers.

## Authentication Types

| Type | Description | Use Case |
|------|-------------|----------|
| OAuth2 | OAuth 2.0 authorization code flow | Google, Slack, GitHub, etc. |
| API Key | Simple key authentication | Stripe, OpenAI, SendGrid |
| Basic | Username/password | Some internal APIs |
| Custom | Provider-specific auth | Special cases |

## Popular Providers

### Google Workspace

```json
{
  "provider": "google",
  "auth_type": "oauth2",
  "scopes": [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
  ],
  "endpoints": {
    "calendar": "/calendar/v3/calendars/{calendarId}/events",
    "gmail": "/gmail/v1/users/me/messages",
    "drive": "/drive/v3/files"
  }
}
```

### Slack

```json
{
  "provider": "slack",
  "auth_type": "oauth2",
  "scopes": [
    "channels:read",
    "chat:write",
    "users:read"
  ],
  "endpoints": {
    "postMessage": "/api/chat.postMessage",
    "listChannels": "/api/conversations.list",
    "listUsers": "/api/users.list"
  }
}
```

### GitHub

```json
{
  "provider": "github",
  "auth_type": "oauth2",
  "scopes": [
    "repo",
    "user",
    "read:org"
  ],
  "endpoints": {
    "listRepos": "/user/repos",
    "listIssues": "/repos/{owner}/{repo}/issues",
    "createIssue": "/repos/{owner}/{repo}/issues",
    "listPRs": "/repos/{owner}/{repo}/pulls"
  }
}
```

### Notion

```json
{
  "provider": "notion",
  "auth_type": "oauth2",
  "scopes": [],
  "endpoints": {
    "queryDatabase": "/v1/databases/{database_id}/query",
    "createPage": "/v1/pages",
    "listDatabases": "/v1/databases/{database_id}/query"
  }
}
```

### Linear

```json
{
  "provider": "linear",
  "auth_type": "oauth2",
  "scopes": ["read", "write"],
  "endpoints": {
    "graphql": "/graphql"
  }
}
```

### Stripe

```json
{
  "provider": "stripe",
  "auth_type": "api_key",
  "endpoints": {
    "listCustomers": "/v1/customers",
    "createCustomer": "/v1/customers",
    "listCharges": "/v1/charges"
  }
}
```

### Salesforce

```json
{
  "provider": "salesforce",
  "auth_type": "oauth2",
  "scopes": ["api", "refresh_token"],
  "endpoints": {
    "query": "/services/data/v58.0/query",
    "create": "/services/data/v58.0/sobjects/{object}",
    "update": "/services/data/v58.0/sobjects/{object}/{id}"
  }
}
```

### HubSpot

```json
{
  "provider": "hubspot",
  "auth_type": "oauth2",
  "scopes": ["contacts", "content"],
  "endpoints": {
    "listContacts": "/crm/v3/objects/contacts",
    "createContact": "/crm/v3/objects/contacts"
  }
}
```

## Error Handling Reference

### Common Error Codes

| Code | Description | Action |
|------|-------------|--------|
| `auth_expired` | OAuth token expired | Re-authorize |
| `rate_limited` | Too many requests | Wait and retry |
| `invalid_connection` | Connection not found | Create new connection |
| `insufficient_scope` | Missing permissions | Request additional scopes |
| `provider_error` | Upstream API error | Check provider status |

### Rate Limiting

Most providers implement rate limits. Handle them gracefully:

```python
import time
from nango import Nango, NangoError

def call_with_retry(nango, provider, endpoint, connection_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            return nango.proxy(
                provider=provider,
                endpoint=endpoint,
                connection_id=connection_id
            )
        except NangoError as e:
            if e.code == "rate_limited":
                wait_time = e.retry_after or (2 ** attempt)
                time.sleep(wait_time)
                continue
            raise
    raise Exception("Max retries exceeded")
```

## MCP Integration

Model Context Protocol support for AI agents:

```json
{
  "mcp_version": "1.0",
  "server": {
    "name": "nango-github",
    "version": "1.0.0",
    "tools": [
      {
        "name": "create_issue",
        "description": "Create a GitHub issue",
        "input_schema": {
          "type": "object",
          "properties": {
            "owner": {"type": "string"},
            "repo": {"type": "string"},
            "title": {"type": "string"},
            "body": {"type": "string"}
          },
          "required": ["owner", "repo", "title"]
        }
      }
    ]
  }
}
```

## Security Best Practices

1. **Environment Variables**: Never hardcode credentials
2. **Connection IDs**: Use unique IDs per user/context
3. **Scope Minimization**: Request only needed permissions
4. **Token Storage**: Let Nango handle token storage
5. **Audit Logging**: Log API calls for debugging

## Full Provider List

For the complete list of 700+ providers, visit:
- https://nango.dev/integrations
- https://docs.nango.dev/integrations/introduction