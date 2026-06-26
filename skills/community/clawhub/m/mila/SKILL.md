---
name: mila
description: >-
  Create, read, update, and delete documents, spreadsheets, and slide
  presentations in Mila via the REST API or MCP tools. Use when the user
  wants to manage collaborative documents with rich HTML content, workbooks
  with tabs and cells in A1 notation, or slide decks with free-form HTML
  on a 960x540 canvas. Supports pagination, server-based organization,
  real-time collaboration, formulas, cell formatting, speaker notes, and
  themes.
version: "1.0.2"
license: MIT
compatibility: Requires network access and a Mila API key (mila_sk_*)
metadata:
  author: mila
  homepage: https://mila.gg
  tags: documents,spreadsheets,slides,presentations,collaboration,productivity,api,mcp,real-time,workbooks,cells
---

# Mila

[Mila](https://mila.gg) is a collaborative platform for documents, spreadsheets, and slide presentations. This skill teaches you how to interact with Mila's REST API and MCP tools to manage content programmatically.

Get started at [https://mila.gg](https://mila.gg) -- create an account, generate an API key, and start building.

## Authentication

All requests require a [Mila](https://mila.gg) API key. Keys use the format `mila_sk_*`.

- Create individual keys at [mila.gg/api-keys](https://mila.gg/api-keys)
- Create team keys at [mila.gg/team-api](https://mila.gg/team-api)

API keys have scopes that control access (e.g. `documents:read`, `documents:write`, `sheets:read`, `sheets:write`, `slides:read`, `slides:write`).

### REST API authentication

Include the API key as a Bearer token:

```
Authorization: Bearer mila_sk_your_key_here
```

Base URL: `https://api.mila.gg/v1`

### MCP authentication

The MCP server uses the same API keys. Include the key in the `Authorization` header when connecting to the MCP endpoint.

MCP endpoint: `https://mcp.mila.gg`

## MCP setup

If the user wants to connect Mila to an AI client via MCP, use these configurations:

**Claude Desktop** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "mila": {
      "url": "https://mcp.mila.gg",
      "headers": {
        "Authorization": "Bearer mila_sk_your_key_here"
      }
    }
  }
}
```

**Cursor** (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "mila": {
      "url": "https://mcp.mila.gg",
      "headers": {
        "Authorization": "Bearer mila_sk_your_key_here"
      }
    }
  }
}
```

**VS Code Copilot** (`.vscode/mcp.json`):

```json
{
  "servers": {
    "mila": {
      "type": "http",
      "url": "https://mcp.mila.gg",
      "headers": {
        "Authorization": "Bearer mila_sk_your_key_here"
      }
    }
  }
}
```

## Quick start

### Create a document

```bash
curl -X POST https://api.mila.gg/v1/documents \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"title": "Meeting Notes", "content": "<h1>Meeting Notes</h1><p>Discussed roadmap.</p>"}'
```

MCP tool: `create_document` with `title` and `content` (HTML string).

### Create a spreadsheet

```bash
curl -X POST https://api.mila.gg/v1/sheets \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"title": "Budget", "cells": {"A1": {"value": "Item"}, "B1": {"value": "Cost"}, "A2": {"value": "Hosting"}, "B2": {"value": 99}}}'
```

MCP tool: `create_sheet` with `title` and `cells` (A1 notation object).

### Create a presentation

```bash
curl -X POST https://api.mila.gg/v1/slides \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"title": "Demo", "data": [{"html": "<div style=\"display:flex;align-items:center;justify-content:center;height:100%\"><h1 style=\"font-size:48px\">Hello</h1></div>", "background": "#ffffff", "notes": "Title slide"}]}'
```

MCP tool: `create_slide_presentation` with `title` and `data` (array of slide objects).

## API conventions

### IDs

All resource IDs are opaque strings (e.g. `"xK9mP2wQ"`). Use them as-is in URLs and parameters.

### Pagination

List endpoints accept `limit` (1-100, default 50) and `offset` (default 0). Responses include a `pagination` object:

```json
{
  "data": [...],
  "pagination": { "total": 42, "limit": 50, "offset": 0 }
}
```

### Sorting

List endpoints accept `sort` (`created_at`, `updated_at`, `last_edited_at`, `title`) and `order` (`asc`, `desc`).

### Server filtering

Content can belong to a **server** (workspace) or to **personal files**.

- Omit `server_id`: returns all content
- `server_id=personal`: returns only personal files
- `server_id=<id>`: returns content in that server

Pass `server_id` in the request body when creating content to place it in a server. Omit for personal files.

### Response format

All responses use this structure:

```json
{
  "success": true,
  "data": { ... }
}
```

Errors return:

```json
{
  "success": false,
  "error": { "message": "Description of the error" }
}
```

### Content formats

- **Documents**: HTML strings (headings, paragraphs, lists, tables, images, links). `<script>` tags are stripped.
- **Sheets**: Cell data in A1 notation (e.g. `{"A1": {"value": "Name"}, "B1": {"value": 42}}`). Formulas start with `=`.
- **Slides**: Free-form HTML on a 960x540px canvas. Each slide has `html`, `background`, and `notes` fields.

## Detailed references

For complete endpoint documentation with all parameters, response shapes, and examples:

- [Documents reference](references/DOCUMENTS.md) -- 6 endpoints, 6 MCP tools
- [Sheets reference](references/SHEETS.md) -- 10 endpoints, 10 MCP tools
- [Slides reference](references/SLIDES.md) -- 6 endpoints, 6 MCP tools
- [Servers reference](references/SERVERS.md) -- 1 endpoint, 1 MCP tool

## Available MCP tools

| Tool | Description |
|---|---|
| `list_servers` | List all servers (workspaces) |
| `list_documents` | List documents with pagination and filtering |
| `get_document` | Get a document with full content |
| `create_document` | Create a document with HTML content |
| `update_document` | Update title and/or content |
| `delete_document` | Delete a document |
| `append_to_document` | Append HTML to a document |
| `list_sheets` | List workbooks with tab metadata |
| `get_sheet` | Get a workbook with all tabs and cells |
| `create_sheet` | Create a workbook with an initial tab |
| `update_sheet` | Update workbook title |
| `delete_sheet` | Delete a workbook and all tabs |
| `get_sheet_tab` | Get a single tab with cell data |
| `create_sheet_tab` | Add a tab to a workbook |
| `update_sheet_tab` | Update cells, name, color, or grid size |
| `delete_sheet_tab` | Remove a tab from a workbook |
| `append_rows` | Append rows of data to a tab |
| `list_slides` | List presentations |
| `get_slide_presentation` | Get a presentation with all slides |
| `create_slide_presentation` | Create a presentation |
| `update_slide_presentation` | Update title, slides, theme, or aspect ratio |
| `delete_slide_presentation` | Delete a presentation |
| `append_slides` | Add slides to a presentation |

## Learn more

- [Mila homepage](https://mila.gg)
- [API documentation](https://mila.gg/docs)
- [MCP integration guide](https://mila.gg/mcp)
