---
name: graylog-log-search
version: 1.0.3
author: Pranavj17
description: "Search and debug production logs via Graylog - absolute/relative time queries, stream filtering, system health checks"
triggers:
  - graylog
  - logs
  - log search
  - production debugging
  - error logs
  - debug logs
metadata:
  openclaw:
    requires:
      env: [BASE_URL, API_TOKEN]
    primaryEnv: API_TOKEN
---

# Graylog Log Search Skill

Search Graylog logs directly from your AI agent for production debugging. Query by absolute or relative timestamps, filter by application streams, and check system health.

## Quick Start

### Install

```bash
npm install -g mcp-server-graylog@1.0.3
```

### Configure

Add to your OpenClaw or Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "graylog": {
      "command": "npx",
      "args": ["-y", "mcp-server-graylog@1.0.3"],
      "env": {
        "BASE_URL": "https://your-graylog-instance.example.com",
        "API_TOKEN": "your_graylog_api_token"
      }
    }
  }
}
```

To get your API token: Graylog Web UI > System > Users > Edit your user > Tokens > Create Token.

### Verify

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | BASE_URL=https://your-graylog.example.com API_TOKEN=your_token npx mcp-server-graylog@1.0.3
```

You should see a JSON response with `protocolVersion` and `capabilities`.

## Overview

This skill provides 4 MCP tools for searching and monitoring Graylog:

| Tool | Description |
|------|-------------|
| `search_logs_absolute` | Search logs between specific timestamps (ISO 8601) |
| `search_logs_relative` | Search recent logs (last N seconds, default: 15 min) |
| `list_streams` | Discover available application streams and their IDs |
| `get_system_info` | Check Graylog version, health, and processing status |

## Core Tasks

- "Search for ERROR logs in the last 15 minutes"
- "Find all 500 errors from the payment service between 2pm and 3pm today"
- "List available Graylog streams so I can filter by application"
- "Check if Graylog is healthy and processing logs"
- "Search for timeout errors in the API stream from the last hour"

## Environment Variable Contract

| Variable | Required | Description |
|----------|----------|-------------|
| `BASE_URL` | Yes | Full URL to your Graylog instance (e.g., `https://graylog.example.com`) |
| `API_TOKEN` | Yes | Graylog API token for authentication (Basic Auth) |

## Query Syntax

Uses Elasticsearch query syntax:

- `level:ERROR` - Filter by log level
- `source:api-server` - Filter by source
- `"connection timeout"` - Exact phrase match
- `status:>=500` - Numeric range
- `message:*exception*` - Wildcard match
- `level:ERROR AND source:payment` - Boolean operators

## Security & Guardrails

- **Read-only access**: No write operations to Graylog - only searches and listing
- **Credential isolation**: API token stored in environment variables, never in code or logs
- **Request timeout**: 30-second timeout prevents hanging requests
- **Result limits**: Queries capped at 1000 messages maximum, 50 by default
- **Input validation**: All parameters validated before API calls (query, timestamps, stream IDs, limits)
- **Error sanitization**: Error messages never expose API tokens or sensitive internal details
- **Time range bounds**: Relative searches limited to 24 hours maximum

## Troubleshooting

| Error | Solution |
|-------|----------|
| "Missing environment variables" | Set `BASE_URL` and `API_TOKEN` in your MCP config |
| "Authentication failed" | Verify your API token is valid in Graylog UI |
| "Cannot reach Graylog" | Check BASE_URL and network/VPN connectivity |
| "Invalid query" | Check Elasticsearch query syntax |
| "Endpoint not found" | Verify BASE_URL includes the correct Graylog URL (no trailing `/api`) |

## Release Notes

### v1.0.3 (2026-04-08)
- Extracted shared helpers for testable imports
- Fixed credential leak in git history
- 54 tests passing, all MCP protocol verified

### v1.0.0 (2025-10-23)
- First stable release with 4 tools
- Fixed 5 critical bugs from initial implementation
- Comprehensive test suite and documentation

## Publisher

[@Pranavj17](https://github.com/Pranavj17)
