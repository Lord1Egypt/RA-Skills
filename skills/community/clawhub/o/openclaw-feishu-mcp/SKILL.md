---
name: feishu-mcp
description: Use when user asks about  Feishu MCP (Model Context Protocol) integration for AI agents. Provides cloud document operations with native MCP tool schema. Use for Feishu MCP integration.
---

# Feishu MCP Integration

This skill integrates OpenClaw with Feishu's MCP (Model Context Protocol) service.

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "feishu-mcp": {
        "enabled": true,
        "config": {
          "mcpUrl": "https://feishu-openai-mcp-proxy.bytedance.net/mcp",
          "appID": "cli_a926728f3e38dcba",
          "appSecret": "BiL8CymBwxiA998MXxvUKbN23RhPsxAg"
        }
      }
    }
  }
}
```

## Supported Tools

### 1. Read Document
Read a Feishu cloud document by token.

```json
{
  "action": "read",
  "docToken": "docx_xxx"
}
```

Returns: title, text content, block types.

### 2. Write Document
Replace document content.

```json
{
  "action": "write",
  "docToken": "docx_xxx",
  "content": "# Title\n\nMarkdown content..."
}
```

### 3. Create Document
Create a new document.

```json
{
  "action": "create",
  "title": "New Document",
  "folderToken": "fldcn_xxx"
}
```

### 4. Read Table
Read a table from a document.

```json
{
  "action": "readTable",
  "docToken": "docx_xxx",
  "tableBlockId": "doxcn_xxx"
}
```

Returns: 2D array of cell values.

### 5. Write Table
Write values to a table.

```json
{
  "action": "writeTable",
  "docToken": "docx_xxx",
  "tableBlockId": "doxcn_xxx",
  "values": [
    ["A1", "B1"],
    ["A2", "B2"]
  ]
}
```

### 6. Append Content
Append markdown to document.

```json
{
  "action": "append",
  "docToken": "docx_xxx",
  "content": "Additional content"
}
```

## Usage in OpenClaw

Once configured, AI can automatically use Feishu MCP tools:

```
- Read document "XXX.docx" and extract tables
- Create a new document "Meeting Notes"
- Write data to an existing table
- Update specific section of document
```

## Notes

- MCP tools use native Feishu OpenAPI
- Auto-authentication via appID/appSecret
- Document token extracted from URL: `https://xxx.feishu.cn/docx/ABC123def`

## Dependencies

- Feishu OpenClaw plugin (channel: feishu)
- Feishu app with docx permissions enabled
