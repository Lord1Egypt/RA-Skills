---
name: governclaw-middleware
description: Governance middleware for OpenClaw agents. Wraps HTTP, shell, file, and browser actions with policy checks via GovernClaw before execution. Required tools - http. Environment variables - GOVERNCLAW_URL (default http://127.0.0.1:8000).
---

# GovernClaw Middleware

This skill provides **governed wrappers** for sensitive operations. It acts as a policy enforcement layer between agents and external systems.

## When to Use This Skill

**You MUST use governed tools from this skill instead of raw tools when:**

- Calling external HTTP APIs (`governedHttp` instead of `http`)
- Running shell commands (`governedShell` - future)
- Reading/writing files (`governedFile` - future)
- Controlling a browser (`governedBrowser` - future)

## How It Works

1. You call a governed tool (e.g., `governedHttp`)
2. The skill sends your request metadata to GovernClaw for policy evaluation
3. GovernClaw returns `allow` or `block` with a reason
4. If allowed: the underlying operation executes and returns results
5. If blocked: the operation is cancelled and you receive a block reason

## Available Tools

### governedHttp

Makes HTTP requests through the GovernClaw policy engine.

**Parameters:**
- `method` (string): HTTP method - "GET", "POST", "PUT", "DELETE"
- `url` (string): Target URL
- `body` (object, optional): Request body for POST/PUT
- `headers` (object, optional): Custom headers

**Returns:**
- On success: The HTTP response from the target
- On block: `{ ok: false, blocked: true, reason: "..." }`

**Example:**
```typescript
const result = await context.tools.governclawMiddleware.governedHttp({
  method: "GET",
  url: "https://api.example.com/data"
});

if (result.blocked) {
  // Handle policy block
  console.log("Blocked:", result.reason);
}
```

## Configuration

Set the GovernClaw service URL in your environment:

```bash
export GOVERNCLAW_URL="http://127.0.0.1:8000"
```

Or in `openclaw.json`:

```json
{
  "skills": {
    "governclaw-middleware": {
      "env": {
        "GOVERNCLAW_URL": "http://127.0.0.1:8000"
      }
    }
  }
}
```

## Governance Context

The skill automatically forwards these context fields to GovernClaw:

- `parent_id`: The session ID (who owns the request)
- `child_id`: The agent ID (who is making the request)
- `source`: Where the request originated (agent, control, cron, etc.)
- `channel`: The channel ID (if applicable)
- `node_id`: The node ID (if applicable)
- `skill`: Always "governclaw-middleware"

## Error Handling

Always check for `blocked` in responses:

```typescript
const response = await context.tools.governclawMiddleware.governedHttp({...});

if (!response.ok && response.blocked) {
  // Policy violation - do not retry
  return { error: response.reason };
}

if (!response.ok) {
  // Network or other error - may retry
  return { error: "Request failed" };
}

// Success
return response.data;
```

## Policy Modes

GovernClaw supports three governance modes:

- **playground**: Log-only, actions always allowed
- **governed**: Default mode, enforce policies
- **strict**: Block on any uncertainty

The skill defaults to `governed` mode. Future versions may allow per-request mode overrides.
