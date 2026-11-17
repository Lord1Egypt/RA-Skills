# gogcli-mcp-contacts

> [!WARNING]
> **AI-developed project.** This codebase was built and is actively maintained by [Claude Code](https://www.anthropic.com/claude). Review all code and tool permissions before use.

Extended Google Contacts [MCP](https://modelcontextprotocol.io) server via [gogcli](https://github.com/openclaw/gogcli). Includes auth tools plus the base Contacts tools and 5 additional dedicated People API tools for Workspace directory search, profile fields, and relations.

## Requirements

- [gogcli](https://github.com/openclaw/gogcli) installed and authenticated
- Node.js 22+

```bash
brew install gogcli
gog auth add your@gmail.com --services contacts,people
```

## Installation

```bash
npm install -g gogcli-mcp-contacts
```

### Claude Desktop

```json
{
  "mcpServers": {
    "gogcli-contacts": {
      "command": "gogcli-mcp-contacts",
      "env": {
        "GOG_ACCOUNT": "you@gmail.com"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add gogcli-contacts -- gogcli-mcp-contacts
```

## Extra People Tools (5)

Plus 5 auth tools and 5 base Contacts tools (search, list, get, create, run).

| Tool | Description |
|------|-------------|
| `gog_people_me` | Show your own People profile (people/me) |
| `gog_people_get` | Get a People profile by resource name |
| `gog_people_search` | Search the Workspace directory (covers internal users, unlike contacts search) |
| `gog_people_relations` | Get relations (manager, reports) for a user |
| `gog_people_raw` | Dump the raw People API response as JSON |

## License

MIT
