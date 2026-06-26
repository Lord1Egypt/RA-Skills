# Installation Guide

## Step 1: Configure the Navifare MCP Server

The Navifare MCP is a hosted service. Add it to your MCP client configuration.

### Claude Code / Claude Desktop

Add to `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "navifare-mcp": {
      "url": "https://mcp.navifare.com/mcp"
    }
  }
}
```

### Other MCP Clients

Add the Navifare MCP endpoint to your client's MCP server configuration:
- **URL**: `https://mcp.navifare.com/mcp`
- **Transport**: Streamable HTTP (SSE)
- **Authentication**: None required

### Local Installation (Alternative)

If you prefer to run the MCP server locally via npm:

```json
{
  "mcpServers": {
    "navifare-mcp": {
      "command": "npx",
      "args": ["-y", "navifare-mcp"],
      "env": {
        "GEMINI_API_KEY": "your-gemini-api-key"
      }
    }
  }
}
```

**Note**: Local installation requires a [Google Gemini API key](https://ai.google.dev/) for the format tool's natural language parsing. The hosted service handles this automatically.

## Step 2: Install the Skill

Copy the skill folder to your agent's skills directory:

```bash
# For Claude Code
cp -r navifare-hidden-flight-deals ~/.claude/skills/

# Or clone from the repository
git clone https://github.com/navifare/navifare-mcp.git
cp -r navifare-mcp/skills/navifare-hidden-flight-deals ~/.claude/skills/
```

## Step 3: Verify

1. Restart your MCP client
2. Check that these tools are available:
   - `mcp__navifare-mcp__flight_pricecheck`
   - `mcp__navifare-mcp__format_flight_pricecheck_request`
3. Test with: "I found a round-trip flight from JFK to LHR for $850. BA553 departing Sep 15 at 6 PM, returning BA554 Sep 22 at 10 AM."

## Troubleshooting

### Tools not appearing

1. Verify `mcp.json` syntax is valid JSON
2. Restart your MCP client completely
3. Check the Navifare MCP endpoint is reachable: `curl -s https://mcp.navifare.com/mcp`

### Connection errors

The hosted MCP server at `mcp.navifare.com` requires internet access. If behind a corporate firewall, you may need to allowlist this domain or use the local npm installation instead.

### Permission errors

Ensure your MCP client has permission to use the Navifare tools. In Claude Code, you may need to approve the tools on first use.

## Support

- **General**: [contact@navifare.com](mailto:contact@navifare.com)
- **Privacy**: [privacy@navifare.com](mailto:privacy@navifare.com)
- **GitHub**: [github.com/navifare/navifare-mcp](https://github.com/navifare/navifare-mcp)
