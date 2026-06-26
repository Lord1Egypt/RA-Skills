# One Person Company OS MCP Server

This adapter exposes the canonical repository scripts through a stdio MCP server.

## Run

From the repository root:

```bash
python3 platforms/mcp-server/server.py
```

## Client Config Example

```json
{
  "mcpServers": {
    "one-person-company-os": {
      "command": "python3",
      "args": ["/absolute/path/to/one-person-company-os/platforms/mcp-server/server.py"]
    }
  }
}
```

## Tools

- `preflight_check`
- `init_business`
- `update_focus`
- `generate_artifact_document`
- `validate_release`

## Boundary

The MCP server wraps existing scripts. It does not auto-install system packages and should only be used with founder-approved workspace paths.
