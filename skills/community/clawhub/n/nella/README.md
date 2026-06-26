# @getnella/mcp

CLI and MCP server package for Nella.

## Install

```bash
npm install -g @getnella/mcp
```

The package installs:

- `nella` for the CLI
- `mcp` as the direct stdio MCP entrypoint used by `npx -y @getnella/mcp --workspace /path/to/project`

## Quick Start

```bash
# Show CLI help
nella help

# Configure a supported client
nella connect --client claude

# Claude Code shortcut
nella setup

# Start the local stdio MCP server directly
npx -y @getnella/mcp --workspace /path/to/project
```

If you want to build or refresh the local index yourself:

```bash
nella auth login
nella index --force
```

`nella index` requires either a Nella login or Azure embedding environment variables.

## Commands

| Command | Purpose |
|---------|---------|
| `nella index [--workspace <path>] [--force] [--graph]` | Index a workspace or build a dependency graph from an existing index |
| `nella mcp --workspace <path>` | Start the local stdio MCP server |
| `nella serve [--port <number>] [--host <host>]` | Start the hosted HTTP MCP server |
| `nella connect [--mode <local\|hosted>] [--client <name>]` | Write MCP client config for supported agents |
| `nella auth <login\|logout\|status>` | Manage CLI authentication |
| `nella setup` | Alias for `nella connect --client claude-code --mode local -y` |
| `nella help` | Show top-level help |

Direct stdio/local launches must include `--workspace`, for example `npx -y @getnella/mcp --workspace /path/to/project`.

## MCP Tools

| Tool | Description |
|------|-------------|
| `nella_index` | Index or re-index a workspace |
| `nella_search` | Search indexed code with hybrid, semantic, or lexical mode |
| `nella_get_context` | Read the current session context |
| `nella_add_assumption` | Record an assumption about the codebase |
| `nella_check_assumptions` | Review assumption status |
| `nella_check_dependencies` | Check dependency drift |
| `nella_heartbeat` | Verify trust-chain continuity between tool calls |

## Manual Client Config

Local stdio example:

```json
{
  "mcpServers": {
    "nella": {
      "command": "npx",
      "args": ["-y", "@getnella/mcp", "--workspace", "/absolute/path/to/project"]
    }
  }
}
```

Hosted example:

```json
{
  "mcpServers": {
    "nella": {
      "url": "https://mcp.getnella.dev/mcp",
      "headers": {
        "Authorization": "Bearer nella_your_key_here"
      }
    }
  }
}
```

## Notes

- `nella connect` supports `claude`, `claude-code`, `vscode`, `cursor`, `windsurf`, `cline`, and `roo-code`.
- The local `nella serve` implementation requires `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`, and uses `REDIS_URL` when available.

## Docs

- [CLI Reference](../../docs/cli/commands.md)
- [Installation](../../docs/getting-started/installation.md)
- [Quick Start](../../docs/getting-started/quick-start.md)
- [Claude Desktop](../../docs/integrations/claude-desktop.md)
- [Cursor](../../docs/integrations/cursor.md)
- [VS Code](../../docs/integrations/vscode.md)
