# MCP Integration - Google Workspace CLI

## Start MCP Server

```bash
# Narrow exposure (recommended)
gws mcp -s drive,gmail,calendar

# Include workflows
gws mcp -s drive,gmail -w
```

## Client Configuration Example

```json
{
  "mcpServers": {
    "gws": {
      "command": "gws",
      "args": ["mcp", "-s", "drive,gmail,calendar"]
    }
  }
}
```

## Tool Budget Discipline

- Each service can add many tools.
- Keep service list limited to current task scope.
- Reconfigure profiles per workflow family instead of exposing all services.

## Operational Guardrails

- Validate service list before starting each MCP session.
- Keep write-capable services disabled in read-only investigations.
- Log MCP profiles in `mcp-profiles.md` for repeatability.
- If tool count grows beyond client limits, split into multiple profiles.
