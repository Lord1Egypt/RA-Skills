---
name: mcp-tool-utils
description: MCP (Model Context Protocol) utilities and helpers. Tools for connecting, configuring, and managing MCP servers with OpenClaw.
---

# MCP Tool Utils

Hilfsmittel für MCP (Model Context Protocol) Integration.

## Was ist MCP?

Model Context Protocol (MCP) ermöglicht:
- Standardisierte Tool-Schnittstellen
- Multi-Server Management
- Kontext-Austausch zwischen Agenten

## Features

### 1. MCP Server Management

```bash
# Server konfigurieren
mcp-tool-utils add-server --name tavily --url https://mcp.tavily.com

# Liste aller Server
mcp-tool-utils list-servers

# Status prüfen
mcp-tool-utils check-health tavily
```

### 2. Tool Discovery

```javascript
// Alle verfügbaren Tools anzeigen
const tools = await mcpUtils.discover({
  server: "tavily"
});

// Ergebnis:
// [
//   { name: "tavily_search", description: "..." },
//   { name: "tavily_extract", description: "..." }
// ]
```

### 3. Konfiguration Sync

```bash
# OpenClaw.json mit MCP-Servern synchronisieren
mcp-tool-utils sync --to openclaw

# Oder zu mcporter
mcp-tool-utils sync --to mcporter
```

## Unterstützte Server

| Server | URL | Tools |
|--------|-----|-------|
| **Tavily** | https://mcp.tavily.com | tavily_search, tavily_extract |
| **Exa** | https://mcp.exa.ai | exa_search |
| **Firecrawl** | https://mcp.firecrawl.dev | firecrawl_scrape, firecrawl_crawl |

## Integration mit OpenClaw

### in openclaw.json
```json
{
  "mcp": {
    "servers": {
      "tavily": {
        "url": "https://mcp.tavily.com/mcp/?tavilyApiKey=..."
      }
    }
  }
}
```

### Verwendung
```javascript
const result = await mcpUtils.call({
  server: "tavily",
  tool: "tavily_search",
  params: {
    query: "API documentation",
    max_results: 5
  }
});
```

## Hilfsfunktionen

| Funktion | Beschreibung |
|----------|--------------|
| `validateConfig()` | Prüft MCP-Konfiguration |
| `generateTypes()` | TypeScript-Definitionen |
| `monitorLatency()` | Server-Performance-Monitoring |
| `backupServers()` | Server-Konfig sichern |

## CLI

```bash
# Server hinzufügen
mcp-tool-utils add tavily --api-key $TAVILY_KEY

# Tool aufrufen
mcp-tool-utils call tavily tavily_search "query=API docs"

# Health-Check
mcp-tool-utils health
```

## Links

- [MCP Spec](https://modelcontextprotocol.io/)
- [OpenClaw MCP Guide](../docs/websearch-mcp/WEBSEARCH_MCP_GUIDE.md)
