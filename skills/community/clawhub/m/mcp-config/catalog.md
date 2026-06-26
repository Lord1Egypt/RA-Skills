# MCP Server Catalog

List of commonly used MCP servers.

## Server List

| Server | Package | Command | Purpose |
|--------|---------|---------|---------|
| code-mode | `@utcp/code-mode-mcp` | npx | UTCP tool chain |
| context7 | `@upstash/context7-mcp` | npx | Library documentation search |
| playwright | `@anthropics/mcp-playwright` | npx | Browser automation |
| postgres | `postgres-mcp` | uvx | PostgreSQL database |

## Configuration Examples per Server

### code-mode

```json
{
  "code-mode": {
    "command": "npx",
    "args": ["-y", "@utcp/code-mode-mcp"],
    "env": {
      "UTCP_CONFIG_FILE": "~/.utcp_config.json"
    }
  }
}
```

### context7

```json
{
  "context7": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp"]
  }
}
```

### playwright

```json
{
  "playwright": {
    "command": "npx",
    "args": ["-y", "@anthropics/mcp-playwright"]
  }
}
```

### postgres

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
