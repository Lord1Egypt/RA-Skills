# MCP Server Format

JSON format reference per agent.

## File Locations

| Agent | File | Key Path | Scope | Method |
|-------|------|----------|-------|--------|
| Claude Code (local) | `~/.claude.json` | `projects[path].mcpServers` | This machine, this project | `claude mcp add --scope local` (default) |
| Claude Code (user) | `~/.claude.json` | root `mcpServers` | This machine, all projects | `claude mcp add --scope user` |
| Claude Code (project) | `./.mcp.json` | `mcpServers` | Committed to repo, shared with team | `claude mcp add --scope project` |
| Cursor | `~/.cursor/mcp.json` | Global | Manual edit |
| Antigravity | `~/.gemini/antigravity/mcp_config.json` | Global | Manual edit |

**IMPORTANT**: Claude Code requires `claude mcp add` CLI. Manual `.mcp.json` edits are NOT recognized.

## Basic Format

```json
{
  "server-name": {
    "command": "npx",
    "args": ["-y", "@package/name"]
  }
}
```

## When Environment Variables Are Required

```json
{
  "server-name": {
    "command": "npx",
    "args": ["-y", "@package/name"],
    "env": {
      "API_KEY": "${API_KEY}",
      "CONFIG_FILE": "~/.config/file.json"
    }
  }
}
```

## Using uvx (Python Packages)

```json
{
  "postgres": {
    "command": "uvx",
    "args": ["postgres-mcp", "--access-mode=unrestricted"],
    "env": {
      "DATABASE_URI": "postgresql://user:pass@host:5432/db"
    }
  }
}
```

## Antigravity Format Difference

Antigravity requires the `transport` field:

```json
{
  "server-name": {
    "transport": "stdio",
    "command": "npx",
    "args": ["-y", "@package/name"]
  }
}
```

Claude Code / Cursor do not require `transport`.
