---
name: local-mcp-server
version: 1.0.0
description: Run a full Model Context Protocol (MCP) server in Termux. Exposes Read, Bash, Grep, glob tools for local Ollama models. Privacy-first, offline-capable, ~10MB.
category: Developer Tools
tags: [mcp, local-ai, ollama, developer-tools, privacy]
author: Cod3Black <support@cod3black.agency>
repository: https://github.com/cod3black/local-mcp-server
license: MIT
pricing:
  oneTime: 39
  subscription: null
  currency: USD
requirements:
  - Termux (Android) or Linux environment
  - Node.js v16+
  - Ollama installed (optional, for LLM integration)
  - pnpm or npm
---

# Local MCP Server for Termux

Run a full MCP server in Termux that exposes the same tools as Amp but for local AI models via Ollama.

## What Is MCP?

The Model Context Protocol is the standard for AI tool integration. This server implements it locally, so your Ollama models can:

- **Read files and directories**
- **Execute bash commands**
- **Search code with grep**
- **Pattern match files with glob**

## Perfect For

- Developers who want local AI without cloud dependency
- Privacy-conscious users keeping code on-device
- Termux power users building AI workflows
- Offline development environments

## What's Included

- Full MCP server implementation (Node.js, ~10MB)
- Tool wrappers for local CLI utilities
- Path sandboxing for security
- HTTP and stdio transport options
- Amp-compatible interface (easy switching)
- Health checks and graceful shutdown

## Integration Examples

- Connect Ollama models to local file system
- Use with Claude Desktop as local tool provider
- Build custom AI workflows with tool access

## Quick Start

```bash
# Install dependencies
pnpm install

# Setup server
bash scripts/setup.sh

# Start MCP server
mcp-start

# Verify health
mcp-health

# Connect Ollama model
ollama run llama3.2 --mcp-server http://localhost:8080
```

## Configuration

```json
{
  "server": {
    "port": 8080,
    "transport": "http",
    "sandbox": "~/.openclaw/mcp-sandbox"
  },
  "tools": {
    "read": true,
    "bash": true,
    "grep": true,
    "glob": true
  },
  "security": {
    "allowedPaths": ["~/projects", "~/.openclaw"],
    "forbiddenCommands": ["rm -rf", "dd", "mkfs"]
  }
}
```

## Requirements

- Termux (Android) or Linux environment
- Node.js v16+
- Ollama installed (optional, for LLM integration)
- pnpm or npm

## Support

Email: support@cod3black.agency
