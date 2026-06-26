# Karadeo — Agent & AI Integration Guide

Karadeo is a karaoke and lyrics tooling platform. This document describes all available
APIs, tools, and agent integration surfaces.

## Authentication

All API endpoints require a Bearer API key from https://karadeo.com/dashboard.

```
Authorization: Bearer kd_<your-api-key>
```

---

## MCP Server

Karadeo exposes a full MCP (Model Context Protocol) server for AI agent tool use.

**Endpoint:** `POST https://karadeo.com/api/mcp`  
**Transport:** Streamable HTTP (JSON-RPC 2.0)  
**Discovery:** `https://karadeo.com/.well-known/mcp/server-card.json`

### Initialize

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
```

### List Tools

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

### Call Tool

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "transcribe",
    "arguments": {
      "audio_url": "https://example.com/song.mp3",
      "format": "lrc"
    }
  }
}
```

---

## REST API

### Transcribe

Convert audio or video to time-synced lyrics or subtitle files.

**Endpoint:** `POST https://karadeo.com/api/transcribe`  
**Docs:** https://karadeo.com/resources/karadeo-lyrics-api  
**OpenAPI:** https://karadeo.com/api/doc

**Request body (JSON):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `fileUrl` | string | yes | Publicly accessible audio/video URL |
| `format` | string | no | `lrc`, `srt`, `ass`, `webvtt`, `ttml`, `txt` (default: `lrc`) |
| `transcriptText` | string | no | Known lyrics to align instead of auto-transcribing |
| `isWordLevel` | boolean | no | Word-level timing (default: false) |

**Example:**

```bash
curl -X POST https://karadeo.com/api/transcribe \
  -H "Authorization: Bearer kd_your_key" \
  -H "Content-Type: application/json" \
  -d '{"fileUrl":"https://example.com/song.mp3","format":"lrc"}'
```

**Response:** Plain text subtitle file with appropriate Content-Type header.

---

## WebMCP (Browser)

Karadeo registers browser tools via `navigator.modelContext.registerTool()` on every page load.

Available tools:
- `list-karaoke-tools` — list all Karadeo tools with URLs
- `navigate-to-tool` — navigate to a specific tool page
- `list-karaoke-templates` — list available karaoke video templates

---

## Discovery Endpoints

| Endpoint | Description |
|----------|-------------|
| `/.well-known/agent-skills/index.json` | Agent Skills Discovery index (RFC v0.2.0) |
| `/.well-known/mcp/server-card.json` | MCP Server Card (SEP-1649) |
| `/.well-known/api-catalog` | API Catalog (RFC 9727) |
| `/.well-known/oauth-authorization-server` | OAuth discovery metadata (RFC 8414) |

---

## Content Policy

```
Content-Signal: ai-train=no, search=yes, ai-input=no
```

AI agents may read this site for tool use. Training on site content is not permitted.
