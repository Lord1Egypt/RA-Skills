---
name: leadshark
description: Connect OpenClaw to LeadShark Apex, the remote MCP server for LinkedIn posts, comment to DM automations, prospecting and sending limits on your LeadShark account.
metadata:
  openclaw:
    homepage: https://leadshark.io/linkedin-mcp-server
---

# LeadShark Apex

LeadShark Apex is a remote MCP server at `https://apex.leadshark.io/mcp` (Streamable HTTP, OAuth). It works against your existing LeadShark account and respects your plan limits.

## Connect with OAuth (recommended)

```bash
openclaw mcp add leadshark \
  --url https://apex.leadshark.io/mcp \
  --transport streamable-http \
  --auth oauth \
  --oauth-scope "mcp:read mcp:write"
openclaw mcp login leadshark
openclaw mcp doctor leadshark --probe
```

`openclaw mcp login` opens the LeadShark sign-in and saves the credentials. `doctor --probe` confirms the server connects and lists its tools.

## Fallback: local server with an API key

If you prefer an API key, use the npm package `@leadshark/mcp-server` (command `leadshark-mcp`). Generate a key at https://apex.leadshark.io/docs/api and where you can, store it through OpenClaw's supported secret mechanisms rather than as a config literal.

```bash
npm i -g @leadshark/mcp-server
openclaw mcp add leadshark \
  --command leadshark-mcp \
  --env LEADSHARK_API_KEY=<your_api_key>
openclaw mcp doctor leadshark --probe
```

## Safe use

- LinkedIn limits: 0 to 250 DMs a day (150 recommended max).
- Prefer drafting automations first and review before turning them on.
- Keep a human in the loop for anything that posts, comments or messages as you.

Docs: https://apex.leadshark.io/docs/mcp
