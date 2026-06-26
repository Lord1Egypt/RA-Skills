# HotelPost MCP User Onboarding

This guide explains the exact user actions required before an installed agent can successfully call the HotelPost MCP server.

## Overview

HotelPost MCP now requires two tokens at the same time:

| Token | Format | Purpose |
|------|--------|---------|
| AgentAuth user token | `uk_xxx` | Identifies which user is calling |
| HotelPost workspace token | `hp_sk_xxx` | Identifies which workspace the agent may access |

The agent must send both headers on every MCP request:

```json
{
  "Authorization": "Bearer hp_sk_xxxxxxxx",
  "X-Agent-User-Key": "uk_xxxxxxxx"
}
```

If either token is missing, MCP authentication fails.

Current HotelPost web domain:

- `https://app.example.com/`

## Step 1: Get the AgentAuth user token

User actions:

1. Open the AgentAuth dashboard:
   `https://aauth-170125614655.asia-northeast1.run.app/dashboard`
2. Sign in with the user's Google account
3. In the `Your API Key` section, click `Show` or `Copy`
4. Copy the token starting with `uk_`
5. Save it securely

Result:
- User gets a personal token like `uk_xxxxxxxx`

Notes:
- This token represents the user identity
- If it becomes invalid later, the user must revisit AgentAuth and copy a fresh token

## Step 2: Get the HotelPost workspace token

User actions:

1. Open HotelPost Web:
   `https://app.example.com/`
2. Sign in to HotelPost
3. Enter the exact workspace the agent should operate on
4. Open `Settings` → `API Keys`
5. Create a new API Key if needed
6. Copy the raw token when it is shown

Result:
- User gets a workspace token like `hp_sk_xxxxxxxx`

Notes:
- This token is workspace-scoped
- Different workspaces may require different `hp_sk_*` tokens
- The raw token is typically shown only once
- This is not a user token. It only grants access to the selected workspace
- The `hp_sk_*` must be used together with the `uk_*` from the same user session context

## Step 3: Configure the agent MCP server

The installed agent must configure the `hotelpost` MCP server with both headers.

Example:

```json
{
  "mcpServers": {
    "hotelpost": {
      "type": "streamable-http",
      "url": "https://mcp.example.com/api/mcp",
      "headers": {
        "Authorization": "Bearer hp_sk_xxxxxxxx",
        "X-Agent-User-Key": "uk_xxxxxxxx"
      }
    }
  }
}
```

User actions:

1. Open the agent MCP configuration
2. Find or create the `hotelpost` server entry
3. Paste both tokens into the headers
4. Save the config
5. Restart or reload the agent if required by the host

## Validation Checklist

Before using the skill, confirm:

- User can open AgentAuth dashboard
- User has a valid `uk_*`
- User can open the correct HotelPost workspace
- User has a valid `hp_sk_*`
- Both headers are present in MCP config
- MCP server name is `hotelpost`

## Common Failures

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `401 Missing AgentAuth user_key` | `X-Agent-User-Key` missing | Add the `uk_*` header |
| `401 Missing API Key` | `Authorization` missing | Add `Bearer hp_sk_*` |
| `401 Invalid AgentAuth user_key` | Wrong or expired `uk_*` | Copy a new key from AgentAuth |
| `401 Invalid API Key` | Wrong `hp_sk_*` | Recreate or copy the HotelPost key again |
| `403 AgentAuth user is not linked to a local account` | The current AgentAuth identity is not available for HotelPost MCP access | Sign in to HotelPost with the intended AgentAuth identity first |
| `403 User does not have access to this workspace` | Token points to a workspace the user cannot access | Use a workspace the user belongs to |

## Important Distinction

Web login and MCP access are different:

- Web login uses the HotelPost web session
- MCP does not use browser cookies
- MCP always requires both `uk_*` and `hp_sk_*`

## Related Files

- Main skill: `SKILL.md`
- Error guide: `references/error-handling.md`
