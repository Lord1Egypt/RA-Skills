---
name: mcp-bridge
description: Use mcp-bridge-openclaw CLI to connect to and manage Model Context Protocol (MCP) servers with auto-reconnection and retry logic. Install via npm install -g mcp-bridge-openclaw.
homepage: https://www.npmjs.com/package/mcp-bridge-openclaw
repository: https://github.com/Jatira-Ltd/OpenClaw-MCP-Bridge
---

# mcp-bridge-openclaw

CLI tool for connecting to MCP servers with built-in resilience.

## Installation

```bash
npm install -g mcp-bridge-openclaw
```

Verified publisher: npm user `jaggu37`

## Commands

### Connect to MCP server
```bash
mcp-bridge --config config.json
```

### List available servers
```bash
mcp-bridge --config config.json --list
```

### Run with verbose logging
```bash
mcp-bridge --verbose --config config.json
```

## Configuration

Create `config.json`:

```json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "env": {}
    }
  }
}
```

**Security tip:** Use environment variables for tokens instead of plaintext in config:

```json
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

Then run: `GITHUB_TOKEN=your_token mcp-bridge --config config.json`

## Programmatic Usage

```typescript
import { MCPBridge } from 'mcp-bridge-openclaw';

const bridge = new MCPBridge({
  configPath: './config.json',
  onServerConnect: (name) => console.log(`Connected to ${name}`),
});

await bridge.connect();
await bridge.disconnect();
```

## Key Features

- Auto-reconnect on disconnect
- Configurable retry logic
- Type-safe JSON config
- CLI + programmatic API
- Multiple server support
