---
name: home-assistant
description: >-
  Control Home Assistant — lights, switches, climate, scenes, and automations —
  from your agent. Create and risk-check automations from natural language,
  validate YAML before deploying, and act on proactive suggestions. Connects
  over MCP with OAuth 2.0 (Selora Connect) — no long-lived tokens.
license: MIT
compatibility: openclaw
metadata:
  version: 1.0.6
  category: setup
---

# Home Assistant

Control your smart home from your agent — lights, switches, climate, scenes, scripts, and automations. Create new automations from natural language, validate YAML before it runs, and act on proactive suggestions. Connects to Home Assistant over MCP with OAuth 2.0 handled by Selora Connect, so no long-lived tokens or copy-pasted secrets.

## What you can do

**Control the home**

- Inspect entity state across all rooms and areas
- Turn lights, switches, and outlets on / off, set brightness or scene
- Adjust climate (HVAC mode, setpoint, fan)
- Trigger scripts, scenes, and existing automations

**Create and tune automations**

- Describe an automation in plain English (e.g. *"wake up lights at 6:30 AM"*) — Selora returns valid HA YAML with a risk assessment
- Validate hand-written YAML before creating it
- New automations are created **disabled by default**; you enable them after review
- Inspect, edit, and delete existing automations

**Act on proactive suggestions**

- Surface behavior patterns Selora has detected in your home
- Convert suggestions into automations with one approval

## Prerequisites

1. **Home Assistant** 2025.1+ with the [Selora AI](https://selorahomes.com/docs/selora-ai/installation/) integration installed.
2. A **Selora Connect** account with your HA installation linked.
3. **OpenClaw** installed.

## 1. Get Your MCP URL

| Access | URL |
|--------|-----|
| Local  | `http://homeassistant.local:8123/api/selora_ai/mcp` |
| Remote | `https://mcp-<id>.selorabox.com/api/selora_ai/mcp` |

Your remote MCP URL (including your `mcp-<id>`) is shown in Selora Connect once MCP remote access is enabled. Enable it to provision a SeloraBox tunnel URL.

> Use your HA IP (e.g. `192.168.x.x`) instead of `homeassistant.local` if mDNS is slow.

## 2. Add the MCP Server

Add the server via the CLI:

```bash
openclaw mcp set home-assistant '{"url":"https://mcp-<id>.selorabox.com/api/selora_ai/mcp"}'
```

Or edit `~/.openclaw/openclaw.json` directly:

```json
{
  "mcp": {
    "servers": {
      "home-assistant": {
        "url": "https://mcp-<id>.selorabox.com/api/selora_ai/mcp"
      }
    }
  }
}
```

For local access, use `http://homeassistant.local:8123/api/selora_ai/mcp` as the URL.

## 3. Authenticate

1. Restart the OpenClaw gateway after editing the config.
2. Use any tool from the server (e.g. ask *"Get a snapshot of my home"*). OpenClaw connects and receives a `401 Unauthorized`.
3. OpenClaw surfaces an authorization URL. Open it in a browser.
4. Approve access on the Selora Connect consent screen.
5. The browser redirects back to OpenClaw's callback to complete the exchange.
6. Tokens are cached and refresh silently from then on.

> **The callback must reach OpenClaw's listener.** If the browser and OpenClaw are on the same machine, the redirect completes automatically. If they are on different machines, see [Cross-device callback mismatch](#cross-device-callback-mismatch) below.

## 4. Verify

Ask your agent: *"Get a snapshot of my home"*. You should see `selora_get_home_snapshot` return your entities grouped by area.

## Available Tools

Read tools:

| Tool | Description |
|------|-------------|
| `selora_get_home_snapshot` | Entity states grouped by area — call this first |
| `selora_list_automations` | Selora automations with status and risk (filterable) |
| `selora_get_automation` | Full detail: YAML, versions, risk |
| `selora_validate_automation` | Validate and risk-assess YAML without creating |
| `selora_list_sessions` | Recent chat sessions |
| `selora_list_patterns` | Detected behavior patterns |
| `selora_get_pattern` | Full pattern detail with linked suggestions |
| `selora_list_suggestions` | Proactive suggestions with YAML previews |

Mutating tools (🔒 require admin authorization):

| Tool | Description |
|------|-------------|
| `selora_chat` 🔒 | Natural-language chat — proposes automations with YAML and risk |
| `selora_create_automation` 🔒 | Create automation from YAML (disabled by default) |
| `selora_accept_automation` 🔒 | Enable a pending automation |
| `selora_delete_automation` 🔒 | Delete permanently |
| `selora_accept_suggestion` 🔒 | Create automation from a suggestion |
| `selora_dismiss_suggestion` 🔒 | Dismiss a suggestion |
| `selora_trigger_scan` 🔒 | Trigger immediate suggestion scan (rate-limited 60s) |

## Workflows

### Explore your home
1. `selora_get_home_snapshot` — understand entities and areas.
2. `selora_list_automations` / `selora_get_automation` for existing automations.

### Create from YAML
1. `selora_validate_automation` — check YAML and surface risk.
2. Show normalized YAML + risk, ask user confirmation.
3. `selora_create_automation` with `enabled=false`.
4. `selora_accept_automation` after explicit approval.

### Create from natural language
1. `selora_chat` — describe what you want; Selora returns YAML + risk.
2. Summarize risk, ask user confirmation.
3. `selora_create_automation` or `selora_accept_automation`.

### Act on suggestions
1. `selora_list_suggestions` (optionally `selora_trigger_scan` first).
2. Show suggestion details, ask user confirmation.
3. `selora_accept_suggestion` or `selora_dismiss_suggestion`.

## Safety Rules

1. Never invent IDs — resolve from tool output only.
2. Never mutate without explicit user confirmation.
3. Always surface `risk_assessment` before mutating. High or missing risk requires a second confirmation.
4. Create automations disabled by default.
5. Do not skip validation for externally provided YAML.

## How OAuth Works

1. OpenClaw discovers Connect's OAuth server from the MCP endpoint's `.well-known/oauth-authorization-server` metadata.
2. OpenClaw registers itself dynamically (`POST /oauth/register`).
3. OpenClaw starts an authorization code flow with PKCE and surfaces an authorization URL.
4. You open the URL and approve access on the Selora Connect consent screen.
5. OpenClaw exchanges the code for access + refresh tokens.
6. Tokens refresh automatically — no re-auth needed until you revoke access.

On `401 Unauthorized`, OpenClaw reads the `WWW-Authenticate` header, attempts a token refresh, and falls back to a full OAuth flow if refresh fails. No manual re-configuration is needed.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `401 Unauthorized` (auth URL shown) | Open the authorization URL, approve access on Selora Connect, and the flow completes automatically. If refresh fails later, OpenClaw triggers a new flow. |
| `401 Unauthorized` loop (no auth URL shown) | OpenClaw's native OAuth flow is not surfacing the authorization URL — check gateway logs for `401`, auth URL emission, and MCP startup failures. See [Debugging with mcp-remote](#debugging-with-mcp-remote) below. |
| Connection refused | Verify HA is running and URL is correct |
| Timeout | Check firewall; for remote, ensure SeloraBox tunnel is active |
| Tools not listed | Ensure Selora AI integration is installed and enabled |
| Admin tools rejected | Selora Connect role must be `owner` or `member` (not `viewer`) |

### Cross-device callback mismatch

The OAuth redirect targets `localhost` on the machine running OpenClaw. If your browser is on a different machine (e.g. OpenClaw on a server, browser on a laptop), the callback cannot reach OpenClaw's listener and the flow fails silently.

As a fallback, ask the user to copy the full callback URL (including the `code` and `state` parameters) from their browser's address bar after approving, and paste it back so the agent can complete the token exchange.

### Debugging with mcp-remote

If OpenClaw keeps returning `401` without surfacing an authorization URL, use `mcp-remote` (requires **Node.js 18+**) to isolate the problem. It is not part of the normal setup — only a debugging tool.

```bash
npx -y mcp-remote https://mcp-<id>.selorabox.com/api/selora_ai/mcp
```

This helps verify the endpoint supports OAuth correctly and that the token exchange works end-to-end. If `mcp-remote` completes the flow successfully, the endpoint is working — the issue is in OpenClaw's OAuth runtime, not your HA setup.
