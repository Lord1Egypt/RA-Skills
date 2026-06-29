---
name: latitude-mcp
description: Connect OpenClaw to the Latitude MCP server so the agent can read and manage your Latitude workspace (projects, traces, spans, issues, annotations, scores, saved searches, datasets, monitors, members). Use when adding Latitude as a remote MCP server in OpenClaw.
version: 1.0.0
tags: mcp, latitude, observability, llm-observability, tracing, monitoring, oauth, integration
homepage: https://docs.latitude.so/getting-started/mcp
emoji: 🔌
---

# Latitude MCP for OpenClaw

[Latitude](https://latitude.so) is an open-source LLM observability and
evaluation platform. Its MCP server is a remote, OAuth-authenticated,
streamable HTTP [Model Context Protocol](https://modelcontextprotocol.io)
server at `https://api.latitude.so/v1/mcp`.

Connecting it lets an OpenClaw agent read and manage your Latitude workspace
directly: projects, members, API keys, traces, spans, issues, annotations,
scores, saved searches, datasets, monitors, and more. The tool catalog is
generated dynamically from the Latitude API, so it stays in sync with the
platform.

There is no API key to copy. Authentication is browser-based OAuth: on first
login you pick which Latitude organization to grant the agent access to, and
you can revoke it any time from your Latitude organization's **Settings → Keys**
under **OAuth Keys**.

## When to use

Use this when you want OpenClaw to query or manage Latitude, or when someone
asks how to add the Latitude MCP server to OpenClaw.

## Add the server

Register Latitude as a user-managed MCP server with OAuth enabled:

```bash
openclaw mcp add latitude \
  --url https://api.latitude.so/v1/mcp \
  --transport streamable-http \
  --auth oauth
```

This is equivalent to adding the following to `~/.openclaw/openclaw.json`:

```json
{
  "mcp": {
    "servers": {
      "latitude": {
        "url": "https://api.latitude.so/v1/mcp",
        "transport": "streamable-http",
        "auth": "oauth"
      }
    }
  }
}
```

## Authenticate

Start the OAuth flow, which prints an authorization URL:

```bash
openclaw mcp login latitude
```

Open the URL, sign in if needed, and pick the organization to authorize. Then
finish the login with the code it gives you:

```bash
openclaw mcp login latitude --code <code>
```

To sign out later, run `openclaw mcp logout latitude`.

## Verify

Probe the connection and list the tools the server exposes:

```bash
openclaw mcp doctor latitude --probe
```

A healthy probe confirms the agent can now call Latitude tools. You can also
manage the server from the Control UI at `/mcp`.

## Notes

- `auth: "oauth"` uses the MCP-native OAuth handshake, so no API key or static
  Authorization header is needed. If you set `auth: "oauth"`, any static headers
  are ignored.
- If you self-host Latitude, use your own MCP URL instead of
  `https://api.latitude.so/v1/mcp`.
- To narrow which tools are exposed, add a `toolFilter` with `include` and
  `exclude` globs to the server entry in `~/.openclaw/openclaw.json`.
