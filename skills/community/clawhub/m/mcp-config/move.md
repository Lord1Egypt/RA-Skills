# Move MCP Server (Scope Change)

Change an existing MCP server's scope (e.g., project → local, local → user).

## CRITICAL: Claude Code uses CLI only

Scope change = **remove from old scope** + **add to new scope**. Both steps use `claude mcp` CLI.

## Procedure

### 1. Identify current scope

```bash
claude mcp list
```

Find the server and note its current scope (local/user/project).

### 2. Capture server config

```bash
claude mcp get <server-name>
```

Record: command, args, env vars, transport type.

### 3. Remove from old scope

```bash
claude mcp remove --scope <old-scope> <server-name>
```

### 4. Add to new scope

```bash
# stdio server
claude mcp add --scope <new-scope> <server-name> -- <command> [args...]

# stdio server with env vars
claude mcp add --scope <new-scope> -e KEY=val <server-name> -- <command> [args...]

# HTTP server
claude mcp add --transport http --scope <new-scope> <server-name> <url>
```

### 5. Verify

```bash
claude mcp list
```

Confirm the server appears under the new scope and shows as Connected.

## Scope Reference

| Scope | Flag | Description |
|-------|------|-------------|
| local | `--scope local` | This machine, this project only (default) |
| user | `--scope user` | This machine, all projects |
| project | `--scope project` | `.mcp.json`, committed to repo |

## Special: Project scope (.mcp.json) removal

When removing from **project** scope, `claude mcp remove --scope project` edits `.mcp.json`.
Alternatively, you can manually edit `.mcp.json` to remove the entry (project scope is the only scope where manual edit is acceptable for removal).

## When to Move: Scope Selection Guidelines

| Condition | Recommended Scope | Reason |
|-----------|-------------------|--------|
| Server uses absolute local paths (e.g., `/Users/es6kr/...`) | **local** | Path is machine+project specific, not portable to other machines or projects |
| Server uses relative paths or npx | **project** | Portable, can be committed to git for team sharing |
| Server needed across all projects on this machine | **user** | Global availability without per-project config |
| Server contains secrets in env vars | **local** or **user** | Avoid committing secrets to `.mcp.json` in git |

**Key rule**: If a server config contains machine-specific absolute paths, it should NOT be in project scope (`.mcp.json`) — it will break for other contributors or on other machines.

## Examples

```bash
# Move from project to local
claude mcp remove --scope project my-server
claude mcp add --scope local my-server -- node /path/to/server.js

# Move from local to user (all projects)
claude mcp remove --scope local my-server
claude mcp add --scope user my-server -- npx my-mcp-server
```
