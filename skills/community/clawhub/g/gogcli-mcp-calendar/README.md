# gogcli-mcp-calendar

> [!WARNING]
> **AI-developed project.** This codebase was built and is actively maintained by [Claude Code](https://www.anthropic.com/claude). Review all code and tool permissions before use.

Extended Google Calendar [MCP](https://modelcontextprotocol.io) server via [gogcli](https://github.com/openclaw/gogcli). Includes auth tools plus the base Calendar tools and 6 additional dedicated Google Meet tools for space management.

## Requirements

- [gogcli](https://github.com/openclaw/gogcli) installed and authenticated
- Node.js 22+

```bash
brew install gogcli
gog auth add your@gmail.com --services calendar,meet
```

## Installation

```bash
npm install -g gogcli-mcp-calendar
```

### Claude Desktop

```json
{
  "mcpServers": {
    "gogcli-calendar": {
      "command": "gogcli-mcp-calendar",
      "env": {
        "GOG_ACCOUNT": "you@gmail.com"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add gogcli-calendar -- gogcli-mcp-calendar
```

## Extra Meet Tools (6)

Plus 5 auth tools and 7 base Calendar tools (events, get, create, update, delete, respond, run).

| Tool | Description |
|------|-------------|
| `gog_meet_create` | Create a Google Meet space |
| `gog_meet_get` | Get a Meet space by meeting code |
| `gog_meet_update` | Update Meet space configuration (access type) |
| `gog_meet_end` | End the active conference in a Meet space |
| `gog_meet_history` | List past calls in a Meet space |
| `gog_meet_participants` | List participants from a Meet call |

## License

MIT
