# 🔗 Skill for PicSee URL Shortener

[![Agent Skills](https://img.shields.io/badge/Agent_Skills-Open_Standard-blue.svg)](https://agentskills.io)
[![MCP](https://img.shields.io/badge/MCP-Streamable_HTTP-green.svg)](https://modelcontextprotocol.io)
[![OAuth 2.1](https://img.shields.io/badge/OAuth_2.1-PKCE-orange.svg)](https://modelcontextprotocol.io/specification/draft/basic/authorization)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An **MCP-based [Agent Skill](https://agentskills.io)** for [PicSee](https://picsee.io) — URL shortening, QR code generation, click analytics, and link management.

The skill is just documentation: it points your AI agent at the public PicSee MCP server (`https://api.picsee.io/mcp`) and explains how to use the tools. No Node.js install, no CLI, no local token files — authentication is handled by **OAuth 2.1 + PKCE** via the MCP client.

---

## 🌟 What's new in v3.0.0

- **CLI → MCP**: the entire v2.x CLI (`node cli/dist/cli.js …`) is gone. All functionality is now exposed as MCP tools served from `api.picsee.io/mcp`.
- **OAuth 2.1 + PKCE**: replaces local AES-256 token encryption. Tokens are managed by your MCP client, not by this skill. Dynamic Client Registration means there's no manual app setup.
- **Anonymous mode still works**: `create_short_link` is callable without auth — perfect for one-off shortenings.
- **No Node.js requirement**: works in any MCP-capable client, including ones that can't execute Node (e.g. Cursor, web-based agents).
- **Agent attribution built in**: the server documents the convention of setting `externalId` to the AI agent's name (`Claude Code`, `Cursor`, `Codex`, …) so account owners can see which agent created which link.

Migrating from v2.x? See the [Migration](#migration-from-v2x) section.

---

## ⚙️ Installation by Platform

The skill consists of two parts:

1. **Skill content** (`SKILL.md` + this README) — placed in the platform's skills directory so the agent auto-discovers usage instructions.
2. **MCP server registration** — added to the platform's MCP config so the agent can actually call the tools.

### Claude Code

```bash
# 1. Install the skill
cp -r picsee-short-link ~/.claude/skills/picsee-short-link

# 2. Register the MCP server
claude mcp add --transport http picsee-short-link https://api.picsee.io/mcp
```

Or add manually to `~/.claude.json` (or project `.mcp.json`):

```json
{
  "mcpServers": {
    "picsee-short-link": { "type": "http", "url": "https://api.picsee.io/mcp" }
  }
}
```

### Cursor

Place the skill in `.cursor/skills/picsee-short-link/`, then edit `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project):

```json
{
  "mcpServers": {
    "picsee-short-link": { "url": "https://api.picsee.io/mcp" }
  }
}
```

### Antigravity

Add via Antigravity's MCP settings panel (Settings → MCP Servers → Add), or edit the config file directly:

```json
{
  "mcpServers": {
    "picsee-short-link": { "url": "https://api.picsee.io/mcp" }
  }
}
```

Place `SKILL.md` in Antigravity's skills directory so the agent picks up usage guidance.

### Codex / Codex CLI

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.picsee-short-link]
command = "npx"
args = ["-y", "mcp-remote", "https://api.picsee.io/mcp"]
```

`mcp-remote` bridges stdio ↔ Streamable HTTP and handles OAuth in a browser. (Direct HTTP transport in Codex CLI is improving rapidly — check `codex mcp add --help` on your version.)

Place `SKILL.md` in `.codex/skills/picsee-short-link/` for skill discovery.

### OpenClaw / ClawHub

```bash
clawhub install picsee-short-link
```

Or browse: [https://clawhub.ai/PicSeeInc/picsee-short-link](https://clawhub.ai/PicSeeInc/picsee-short-link)

ClawHub auto-registers the MCP server from the skill's metadata.

### claude.ai (Web)

Upload the skill folder under **Customize → Skills**. Add the MCP server in **Settings → Connectors → Add custom connector** with URL `https://api.picsee.io/mcp`.

### Generic MCP client

Any client that speaks **MCP Streamable HTTP** can register the server directly:

```json
{
  "mcpServers": {
    "picsee-short-link": { "url": "https://api.picsee.io/mcp" }
  }
}
```

For clients that only support stdio, use the `mcp-remote` bridge from npm:

```json
{
  "mcpServers": {
    "picsee-short-link": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.picsee.io/mcp"]
    }
  }
}
```

---

## 🤖 Compatibility Matrix

| Platform | Skill discovery | MCP transport | OAuth flow | Status |
|:---------|:----------------|:--------------|:-----------|:-------|
| Claude Code | `~/.claude/skills/` | HTTP (native) | Browser popup, token in `~/.claude` | ✅ |
| Cursor | `.cursor/skills/` | HTTP (native) | Browser popup, token in Cursor config | ✅ |
| Antigravity | Antigravity skills dir | HTTP (native) | Browser popup | ✅ |
| Codex CLI | `.codex/skills/` | stdio via `mcp-remote` | Browser popup via `mcp-remote` | ✅ |
| OpenClaw / ClawHub | auto (via `clawhub install`) | HTTP | Browser popup | ✅ |
| claude.ai | Customize → Skills | HTTP connector | Browser popup | ✅ |
| Gemini CLI | `.gemini/skills/` | stdio via `mcp-remote` | Browser popup via `mcp-remote` | ✅ |
| VS Code Copilot | `.github/skills/` | HTTP (1.95+) | Browser popup | ✅ |

> Any MCP-compliant client should work — the matrix above is just the integrations we've tested.

---

## 🧩 Tools

`create_short_link` is the only tool callable anonymously. The other 14 require OAuth.

| Group | Tool | Auth |
|:------|:-----|:-----|
| **Create** | `create_short_link` | optional |
| **Account** | `get_api_status` | required |
| | `get_api_usage_by_external_id` | required |
| | `get_my_domains` | required |
| | `get_my_tags` | required |
| | `get_my_tracking_tools` | required |
| **Manage** | `list_short_links` | required |
| | `edit_short_link` | required |
| | `delete_short_link` (covers delete + recover) | required |
| **Analytics** | `get_link_overview` | required |
| | `get_link_daily_clicks` | required |
| | `get_link_platforms` | required |
| | `get_link_referrers` | required |
| | `get_link_regions` | required |
| | `get_link_audience_labels` | required |

> **No QR or chart tool on the server** — those are agent recipes against public services (`api.qrserver.com`, `quickchart.io`). See [SKILL.md → Agent Recipes](SKILL.md#agent-recipes).

Full parameter tables for every tool live in [SKILL.md](SKILL.md). The MCP server is also self-describing via `tools/list` — that is the source of truth.

---

## 🔑 Authentication

1. Register the MCP server in your client (see [Installation](#-installation-by-platform)).
2. Ask the agent to do something that requires auth (e.g. "show me analytics for my last link").
3. The MCP client opens a browser to `https://public-api-oauth.picsee.io/oauth/authorize`.
4. Sign in to PicSee and approve the `user:read` / `user:write` scopes.
5. Done — the client stores the token. Future calls are silent until the refresh token expires.

The skill folder never touches your token. All credential handling lives in your MCP client.

---

## 🔒 Security

| Aspect | v2.x (legacy) | v3.0.0 (current) |
|:-------|:--------------|:-----------------|
| Auth model | Long-lived API token | OAuth 2.1 + PKCE (S256) |
| Token storage | Local file, AES-256-CBC | MCP client (per-client policy) |
| Scopes | All-or-nothing | `user:read`, `user:write` |
| Revocation | Manual via PicSee dashboard | Per-client, revocable from PicSee account |
| Dynamic Client Registration | n/a | ✅ (RFC 7591) |

OAuth metadata is published at [`https://api.picsee.io/.well-known/oauth-protected-resource`](https://api.picsee.io/.well-known/oauth-protected-resource), with the authorization server at [`https://public-api-oauth.picsee.io/.well-known/oauth-authorization-server`](https://public-api-oauth.picsee.io/.well-known/oauth-authorization-server).

---

## 🧭 Agent attribution

The MCP server asks calling agents to set `externalId` to their own product name on `create_short_link`, so PicSee account owners can attribute API usage. The skill tells your agent to default to:

`Claude Code` · `Cursor` · `Codex` · `Antigravity` · `OpenClaw` · `Gemini CLI` · `Copilot` · `ChatGPT`

Users can always override by explicitly passing their own `externalId`.

---

## 📁 Project Structure

```
picsee-short-link/
├── SKILL.md     # Agent Skills definition — read by your agent
├── README.md    # This file — read by humans
└── _meta.json   # ClawHub registry metadata
```

No `cli/` and no `references/` in v3 — the MCP server is self-describing via `tools/list`, and the REST API is now an implementation detail of the server.

---

## Migration from v2.x

```bash
# 1. Remove the old encrypted token + salt files
rm -f ~/.openclaw/.picsee_token ~/.openclaw/.picsee_salt

# 2. Remove the old CLI build artifacts wherever the skill was installed
rm -rf ~/.claude/skills/picsee-short-link/cli
rm -rf ~/.openclaw/workspace/skills/picsee-short-link/cli
rm -rf .cursor/skills/picsee-short-link/cli

# 3. Reinstall the v3 skill (see Installation above) and register the MCP server.
# 4. Ask the agent to do something authenticated — sign in via browser when prompted.
```

No API token migration is needed — OAuth issues fresh credentials from scratch.

---

## 📖 Resources

- **PicSee Website:** [https://picsee.io](https://picsee.io)
- **Developer Docs:** [https://picsee.io/developers](https://picsee.io/developers)
- **MCP Spec:** [https://modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Agent Skills Spec:** [https://agentskills.io](https://agentskills.io)

---

## 📄 License

MIT
