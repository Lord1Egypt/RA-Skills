# Connect PageCrawl

Read this when no PageCrawl tools are available, or when they fail to connect.

## What to connect

- Server URL: `https://mcp.pagecrawl.io/mcp`, exactly as written (no trailing slash, no `/sse`).
- Transport: streamable HTTP. A client set to SSE fails to connect.
- Sign-in: OAuth is the default. The client opens PageCrawl, the user signs in and clicks Approve, and no key is copied.
- Clients without OAuth can send a personal API token instead: `Authorization: Bearer <token>`. The user creates it in PageCrawl under Settings > API > Create Token. Tokens work on every plan.

Never ask the user to paste a token into the conversation. They put it in their client's configuration, or in an environment variable the configuration reads.

## Common clients

Agents with plugin support can install the PageCrawl plugin, which includes this connection and these skills: see https://github.com/pagecrawl/skills.

Command-line agents:

```bash
# Claude Code
claude mcp add --transport http pagecrawl https://mcp.pagecrawl.io/mcp

# Codex: add the server, then sign in with OAuth
codex mcp add pagecrawl --url https://mcp.pagecrawl.io/mcp
codex mcp login pagecrawl

# OpenClaw (API token)
openclaw mcp set pagecrawl --transport streamable-http \
  --url https://mcp.pagecrawl.io/mcp \
  --header "Authorization: Bearer <api-token>"
```

Editors that read an `mcpServers` JSON file (Cursor, Windsurf, Cline and others):

```json
{
  "mcpServers": {
    "pagecrawl": {
      "url": "https://mcp.pagecrawl.io/mcp"
    }
  }
}
```

Add `"headers": {"Authorization": "Bearer YOUR_TOKEN"}` beside `url` when the client does not support OAuth. VS Code's `mcp.json` uses a `servers` key instead of `mcpServers`, with `"type": "http"`.

Chat apps (claude.ai, Claude Desktop, ChatGPT, Microsoft 365 Copilot, Notion) add PageCrawl as a custom connector with the server URL above. Step-by-step instructions for each are at https://pagecrawl.io/help/integrations/article/mcp-server-ai-tools.

## When the connection fails

- **Cannot reach the server**: check the transport is streamable HTTP and the URL is exact.
- **Connected, but the tools are never used**: many clients need the connector turned on per conversation. Naming PageCrawl in the request also helps.
- **Authentication error**: the OAuth grant was revoked or the token deleted. Reconnect, or create a new token under Settings > API.
- **Tools work but return nothing**: the user is probably looking at a different workspace in the web app. Call `list-workspaces` and ask which one they mean.
- **The client warns the server is unverified**: some clients show this for every custom server. It is about the client's own review, not the connection.
