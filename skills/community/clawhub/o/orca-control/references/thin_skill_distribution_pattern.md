# Thin-Skill Architecture & Multi-Client Distribution Pattern

This reference specifies how to design, package, and distribute lightweight client connectors ("Thin-Skills") that interface with a centralized, secure MCP (Model Context Protocol) backend gateway (e.g., Habilis, PAPI).

---

## 1. Core Architecture Principles

1. **Zero Intellectual Property (IP) Leaks**:
   - Client connectors never store private heuristic prompts, optimization algorithms, master API keys, or database schemas.
   - All complex decision-making, budget guardrails, and media rendering run on the server side behind authenticated REST/JSON-RPC/SSE endpoints.

2. **Bring Your Own Keys (BYOK) Vault**:
   - Clients supply their own provider credentials (e.g., Meta App ID, Meta System User Token, OpenAI Org ID) via the platform dashboard or encrypted vault API.
   - The MCP gateway maps the client's Bearer token (`Authorization: Bearer hab_...`) to their vaulted credentials securely in server memory/SQLite.

3. **Multi-Client Manifest Generation**:
   A single service or tool published on the server generates 4 standard configurations automatically:

---

## 2. Standard Manifest Formats

### A. Hermes Agent (`SKILL.md`)
```markdown
---
name: <service-id>
description: <Short description in PT-BR or EN>
author: "Habilis <contact@habilis.ai>"
tags: [ads, marketing, automation, mcp]
---

# <Service Name>

## Authentication & Base URL
Set your Bearer token in environment or headers:
* **Base URL**: `https://<your-domain>/api/mcp`
* **Header**: `Authorization: Bearer <CLIENT_TOKEN>`

## Available Tools & Directives
1. `<tool_1>`: <Description and schema parameters>
2. `<tool_2>`: <Description and schema parameters>
```

### B. Claude Desktop (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "<service-id>": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote-client",
        "--url",
        "https://<your-domain>/api/mcp",
        "--header",
        "Authorization=Bearer <CLIENT_TOKEN>"
      ]
    }
  }
}
```

### C. Cursor IDE (`.cursor/mcp.json` & `.cursorrules`)
```json
{
  "mcpServers": {
    "<service-id>": {
      "url": "https://<your-domain>/api/mcp",
      "headers": {
        "Authorization": "Bearer <CLIENT_TOKEN>"
      }
    }
  }
}
```

### D. n8n Automation Node (HTTP Request)
- **Method**: `POST`
- **URL**: `https://<your-domain>/api/mcp`
- **Headers**:
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer <CLIENT_TOKEN>`
- **Body**:
```json
{
  "jsonrpc": "2.0",
  "id": "n8n_exec_{{$execution.id}}",
  "method": "tools/call",
  "params": {
    "name": "<tool_name>",
    "arguments": {
      "param1": "value1"
    }
  }
}
```

---

## 3. Dynamic Catalog Updates
When a new service/product is registered in the Admin Dashboard:
1. It is assigned a category, pricing tier, and tool schemas.
2. The Thin-Skill generator automatically compiles the Hermes markdown, Claude config, Cursor JSON, and n8n templates.
3. Client dashboards immediately display the copy-paste snippets and download buttons.
