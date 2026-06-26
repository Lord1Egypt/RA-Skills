---
name: meta-mcp-wizard
description: |
  Use the MCPHero Meta-MCP server inside AI clients (Claude Desktop, Cursor, etc.) to create, deploy, and manage MCP servers through the wizard pipeline. Use this skill when the user wants to connect the Meta-MCP server, build MCP servers interactively via MCP tools, or asks about the meta-mcp endpoint at api.mcphero.app.
---

# Meta-MCP Wizard

The [MCPHero](https://mcphero.app) **Meta-MCP server** lets agents build persistent tools without leaving their MCP client. Instead of re-explaining an API or re-generating SQL on every run, the agent creates a hosted MCP server once and calls it forever — saving 95-99% on token usage for recurring tasks.

Connect it to Claude Desktop, Cursor, or any MCP client, and your agent can build, deploy, and register new MCP servers on the fly.

**Meta-MCP endpoint:** `https://api.mcphero.app/mcp/meta/mcp`

---

## Setup

Add the Meta-MCP server to your MCP client config:

### Claude Desktop

```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "mcphero": {
      "url": "https://api.mcphero.app/mcp/meta/mcp"
    }
  }
}
```

Config file locations:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/claude/claude_desktop_config.json`

### Cursor and other MCP clients

Add the same URL `https://api.mcphero.app/mcp/meta/mcp` to your client's MCP server config. The client handles OAuth 2.1 authentication automatically on first use.

---

## Available Tools

The Meta-MCP server exposes these tools:

| Tool | Purpose |
|------|---------|
| `wizard_create_session` | Start session; returns `server_id` |
| `wizard_chat` | Send requirement message; returns `is_ready` flag |
| `wizard_start` | Transition to tool suggestion (async) |
| `wizard_list_tools` | List suggested tools with IDs, code, params |
| `wizard_refine_tools` | Refine with feedback (async) |
| `wizard_submit_tools` | Confirm selection by tool UUID list |
| `wizard_suggest_env_vars` | Re-trigger env var suggestion (async) |
| `wizard_list_env_vars` | List env vars with IDs and descriptions |
| `wizard_refine_env_vars` | Refine env vars with feedback (async) |
| `wizard_submit_env_vars` | Submit values as `{uuid: value}` dict |
| `wizard_set_auth` | Generate bearer token |
| `wizard_generate_code` | Trigger code gen (async) |
| `wizard_regenerate_tool_code` | Regenerate single tool code (sync) |
| `wizard_deploy` | Deploy and get server URL |
| `wizard_state` | Poll current state — use after all async steps |

---

## Async vs Sync Tools

**Async** (trigger then poll `wizard_state`): `wizard_start`, `wizard_refine_tools`, `wizard_suggest_env_vars`, `wizard_refine_env_vars`, `wizard_generate_code`

**Sync** (wait for result): `wizard_create_session`, `wizard_chat`, `wizard_list_tools`, `wizard_submit_tools`, `wizard_list_env_vars`, `wizard_submit_env_vars`, `wizard_set_auth`, `wizard_regenerate_tool_code`, `wizard_deploy`, `wizard_state`

---

## The Wizard Pipeline

```
1. wizard_create_session    → Returns server_id (save it, needed everywhere)
2. wizard_chat (loop)       → Gather requirements; stop when is_ready: true
3. wizard_start             → Transition to tool suggestion (async → poll)
4. wizard_list_tools        → Review AI-suggested tools
5. wizard_refine_tools      → Iterate on tools until satisfied (optional, async → poll)
6. wizard_submit_tools      → Confirm selection by tool UUID list
7. wizard_list_env_vars     → Review suggested env vars
8. wizard_refine_env_vars   → Iterate on env vars (optional, async → poll)
9. wizard_submit_env_vars   → Provide values as {uuid: value} dict (call even if empty)
10. wizard_set_auth         → Generate bearer token
11. wizard_generate_code    → Trigger code generation (async → poll)
12. wizard_deploy           → Deploy → returns server_url + bearer_token
```

**Always call `wizard_submit_env_vars`**, even when `wizard_list_env_vars` returns `[]`. Pass an empty dict `{}` so the backend transitions to the next state.

---

## State Machine

The `setup_status` field in `wizard_state` tells you where you are:

```
gathering_requirements     → User is chatting about requirements
tools_generating           → LLM is generating tool suggestions (async, poll)
tools_selection            → Tools ready for review/selection
env_vars_generating        → LLM is generating env var suggestions (async, poll)
env_vars_setup             → Env vars ready for review/submission
auth_selection             → Ready for auth setup
code_generating            → LLM is generating code (async, poll)
code_gen                   → Code ready for review
deployment_selection       → Ready to deploy
ready                      → Server deployed and live
```

States ending in `_generating` are transient — poll until they transition. The `processing_status` field is the reliable check: `"idle"` means done, `"processing"` means wait, `"error"` means check `processing_error`.

---

## Polling Pattern

After any async tool, poll `wizard_state` until `processing_status` is `"idle"`:

```
wizard_state(server_id) → check .processing_status
  "processing"  → wait and call again
  "idle"        → ready for next step
  "error"       → check .processing_error
```

---

## Connecting a Deployed Server to MCP Clients

After `wizard_deploy`, construct the full server URL:
```
https://api.mcphero.app{server_url}
```

where `server_url` is the relative path returned (e.g., `/mcp/<server-id>/mcp`).

### Claude Desktop config

```json
{
  "mcpServers": {
    "my-server": {
      "url": "https://api.mcphero.app/mcp/<server-id>/mcp",
      "headers": {
        "Authorization": "Bearer <bearer_token>"
      }
    }
  }
}
```

---

## Key Tips

**Free tier**: Max 5 tools per server. `wizard_submit_tools` will error if more are selected.

**server_id is everything**: Save the UUID returned from `wizard_create_session`. Every subsequent call needs it.

**Empty env vars**: Even if `wizard_list_env_vars` returns `[]`, you must still call `wizard_submit_env_vars` with `{}` so the backend transitions to the next state.

**Regenerate without redeploy**: After using `wizard_regenerate_tool_code`, the code change takes effect immediately for already-deployed servers (the server auto-remounts).
