# Kilo CLI Setup and Configuration

## Prerequisites
- **Kilo CLI** must be installed (typically at `/usr/bin/kilo`).
- Access to **npm** or **npx** for loading MCP servers.

## Configuration Directory
Kilo stores its configuration in:
- **`~/.config/kilo/`**

## Main Config File: `kilo.json`
The primary configuration file is `~/.config/kilo/kilo.json`. 

### Schema for MCP Servers
To add an MCP server, use the `"mcp"` key. Each server needs a `type`, `command`, and `args`.

Example `kilo.json`:
```json
{
  "mcp": {
    "puppeteer": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-puppeteer"],
      "enabled": true
    }
  }
}
```

### Auto-Approval Mode
When running Kilo from OpenClaw, use the `--auto` flag to bypass interactive permission prompts.

### Model Selection
Specify the model using the `--model` (or `-m`) flag. 
Format: `provider/model:variant`
Example: `kilo/minimax/minimax-m2.5:free`

## Troubleshooting
If `kilo mcp list` shows "No MCP servers configured" despite a valid `mcp.json` in `~/.kilo/`, it is likely because the CLI expects the configuration in `~/.config/kilo/kilo.json`. Move or link the configuration to the `.config` path.
