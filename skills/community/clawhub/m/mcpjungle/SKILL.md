---
name: mcpjungle-management
description: Manage MCPJungle gateway through its CLI. Use when the user needs to list, register, deregister, enable, disable, invoke, or inspect MCP servers, tools, prompts, and tool groups exposed by a running mcpjungle instance. Covers operations like server registration, tool/prompt lifecycle management, configuration export, and direct tool invocation.
---

# MCPJungle Management

## Quick Start

Connect to a running MCPJungle registry with `--registry <url>`. Default is `http://127.0.0.1:8080`.

```bash
# Verify connection and list registered servers
mcpjungle --registry http://localhost:8080 list servers
```

## Registry Connection

Always pass `--registry` if the instance is not on the default port `8080`.

```bash
mcpjungle --registry http://localhost:8080 <command>
```

## Servers

### List registered servers
```bash
mcpjungle --registry <url> list servers
```

### Register a server
```bash
# SSE transport
mcpjungle --registry <url> register <name> --type sse --url <sse-url>

# Streamable HTTP transport
mcpjungle --registry <url> register <name> --type streamable_http --url <http-url>

# STDIO transport
mcpjungle --registry <url> register <name> --type stdio --command <command>
```

### Deregister a server
```bash
mcpjungle --registry <url> deregister <server-name>
```

## Tools

### List available tools
```bash
mcpjungle --registry <url> list tools
mcpjungle --registry <url> list tools --server <server-name>
mcpjungle --registry <url> list tools --group <group-name>
```

### Inspect tool schema and usage
```bash
mcpjungle --registry <url> usage <server-name>__<tool-name>
```

### Invoke a tool
```bash
mcpjungle --registry <url> invoke <server-name>__<tool-name> --input '{"key":"value"}'
```

### Disable a tool
```bash
# Single tool
mcpjungle --registry <url> disable tool <server-name>__<tool-name>

# All tools from a server
mcpjungle --registry <url> disable tool <server-name>
```

### Enable a tool
```bash
mcpjungle --registry <url> enable tool <server-name>__<tool-name>
mcpjungle --registry <url> enable tool <server-name>
```

## Prompts

### List prompts
```bash
mcpjungle --registry <url> list prompts
mcpjungle --registry <url> list prompts --server <server-name>
```

### Retrieve a prompt with arguments
```bash
mcpjungle --registry <url> get prompt "<server-name>__<prompt-name>" --arg key=value
```

### Disable / enable prompts
```bash
mcpjungle --registry <url> disable prompt "<server-name>__<prompt-name>"
mcpjungle --registry <url> enable prompt "<server-name>__<prompt-name>"

# Entire server prompts
mcpjungle --registry <url> disable prompt <server-name>
mcpjungle --registry <url> enable prompt <server-name>
```

## Tool Groups

### List groups
```bash
mcpjungle --registry <url> list groups
```

Groups are logical collections of tools exposed to specific MCP clients.

## Disable / Enable Servers

Disable or re-enable an entire server globally:

```bash
mcpjungle --registry <url> disable server <server-name>
mcpjungle --registry <url> enable server <server-name>
```

Behavior: disabled tools/prompts are hidden from the main `/mcp` gateway but can still be listed and managed via CLI/API.

## Configuration Export

Export all configuration to files:

```bash
mcpjungle --registry <url> export
```

## Prerequisites

- `mcpjungle` CLI must be installed and available in `$PATH`. Verify with `which mcpjungle`.
- A running MCPJungle registry server (default `http://127.0.0.1:8080`).
