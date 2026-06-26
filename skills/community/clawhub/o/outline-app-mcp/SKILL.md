---
name: outline-app-mcp
description: Model Context Protocol (MCP) bridge for Outline (getoutline.com). Enables AI agents to search, read, create, and manage documents, collections, and comments in an Outline workspace via SSE transport. Includes local filesystem access for bulk file/media uploads to Outline.
metadata:
  version: "1.3.4"
  platform: Outline
  author: Tinker
  transport: Streamable HTTP (SSE)
  mcp_version: "1.0.0"
  openclaw:
    primaryEnv: OUTLINE_API_KEY
    requires:
      env:
        - OUTLINE_API_KEY
        - OUTLINE_URL
      bins:
        - node
        - npm
    install:
      - id: deps
        kind: exec
        command: npm install
        label: Installing Node.js dependencies (@modelcontextprotocol/sdk)
---

# Outline MCP Skill

This skill provides a high-fidelity bridge between OpenClaw and an Outline workspace. It utilizes the **Model Context Protocol (MCP) v1.0.0** to dynamically expose Outline's internal documentation tools to AI agents.

## ⚠️ Security & Permissions Warning

**Host Filesystem Access:**
The `upload` (in `mcp_bridge.mjs`) and `bulk-sync` (in `bulk_sync.mjs`) tools require access to the local host filesystem. These scripts use `fs.readFileSync` to read files from **arbitrary absolute paths** provided by the agent and upload them to the configured Outline workspace.
- **Risk:** If an agent is compromised or misconfigured, it could potentially exfiltrate sensitive local files by providing their absolute paths to these tools.
- **Scope:** Access is limited to the permissions of the user running the OpenClaw process.
- **Recommendation:** Only enable this skill in trusted environments and monitor agent logs for unexpected file access patterns.

## 📋 Prerequisites

Before setting up the skill in OpenClaw, ensure you have completed the following steps in your Outline instance:

1. **Enable AI Features:** Ensure AI features are enabled for your workspace under **Settings** -> **AI**.
2. **Enable MCP:** In the same **AI** settings tab, toggle the **MCP** switch to "On". This enables the Model Context Protocol endpoint for your workspace.
3. **Generate API Key:** Click **Generate API Key** (also in the AI tab). Copy this key immediately as it will only be shown once.
4. **Locate your MCP URL:** Your MCP endpoint is typically your workspace URL with `/mcp` appended (e.g., `https://docs.yourcompany.com/mcp`).
5. **Node.js Environment:** Ensure Node.js (v18+) is installed on your OpenClaw host.

## 🛠️ Setup & Configuration

To use this skill, you must provide your Outline workspace details via environment variables.

### Configuration Commands
```bash
openclaw config set skills.entries.outline-app-mcp.env.OUTLINE_API_KEY "your_ol_api_key"
openclaw config set skills.entries.outline-app-mcp.env.OUTLINE_URL "https://your-workspace.getoutline.com/mcp"
```

## 🧰 API Reference & Detailed Tool Parameters

The following tools are available via the `scripts/mcp_bridge.mjs` executor. All arguments are passed as a JSON object.

### 1. Document Management

#### `list_documents`
Searches documents or lists recent ones.
- `query` (string, optional): Full-text search query.
- `collectionId` (string, optional): Filter by collection.
- `offset` (integer, optional): Pagination offset.
- `limit` (integer, optional): Max results (default 25, max 100).

#### `read_document`
Retrieves the full Markdown content.
- `id` (string, required): Unique identifier of the document.

#### `create_document`
Creates a new document.
- `title` (string, required): Document title.
- `text` (string, optional): Markdown content.
- `collectionId` (string, required if no `parentDocumentId`): Target collection.
- `parentDocumentId` (string, optional): Nest under this document.
- `icon` (string, optional): Emoji icon.
- `color` (string, optional): Hex color (e.g., `#FF0000`).
- `publish` (boolean, optional): Default `true`. Set `false` for draft.

#### `update_document`
Edits an existing document.
- `id` (string, required): Document ID.
- `title` (string, optional): New title.
- `text` (string, optional): New markdown content.
- `editMode` (enum: `replace`, `append`, `prepend`, optional): Default `replace`.
- `collectionId` (string, optional): Required when publishing a draft with no collection.
- `icon` (string/null, optional): Update or remove emoji.
- `color` (string/null, optional): Update or remove hex color.
- `publish` (boolean, optional): Publish draft or revert to draft.

#### `move_document`
Relocates a document.
- `id` (string, required): Document ID.
- `collectionId` (string, optional): Target collection.
- `parentDocumentId` (string, optional): Target parent document.
- `index` (integer, optional): Zero-based position among siblings.

### 2. Collection Management

#### `list_collections`
Lists available collections.
- `query` (string, optional): Filter by name.
- `offset` (integer, optional): Pagination offset.
- `limit` (integer, optional): Max results (max 100).

#### `create_collection`
Creates a new collection.
- `name` (string, required): Collection name.
- `description` (string, optional): Markdown description.
- `icon` (string, optional): Emoji icon.
- `color` (string, optional): Hex color.

#### `update_collection`
Updates collection metadata.
- `id` (string, required): Collection ID.
- `name` (string, optional): New name.
- `description` (string, optional): New description.
- `icon` (string/null, optional): Update or remove icon.
- `color` (string/null, optional): Update or remove color.

### 3. Commenting & Collaboration

#### `list_comments`
Lists comments (requires `documentId` or `collectionId`).
- `documentId` (string, optional): Filter by document.
- `collectionId` (string, optional): Filter by collection.
- `parentCommentId` (string, optional): List only replies to this comment.
- `statusFilter` (array of `resolved`/`unresolved`, optional): Filter by status.
- `offset` (integer, optional): Pagination offset.
- `limit` (integer, optional): Max results.

#### `create_comment`
Adds a comment to a document.
- `documentId` (string, required): Document to comment on.
- `text` (string, required): Markdown content.
- `parentCommentId` (string, optional): Nest as a reply.

#### `update_comment`
Updates or resolves a comment.
- `id` (string, required): Comment ID.
- `text` (string, optional): New markdown text.
- `status` (enum: `resolved`, `unresolved`, optional): Resolve thread.

#### `delete_comment`
Deletes a comment.
- `id` (string, required): Comment ID.

### 4. User Directory

#### `list_users`
Lists workspace members.
- `query` (string, optional): Search by name or email.
- `role` (enum: `admin`, `member`, `viewer`, `guest`, optional): Filter by role.
- `filter` (enum: `active`, `suspended`, `invited`, `all`, optional): Filter by status.
- `offset` (integer, optional): Pagination offset.
- `limit` (integer, optional): Max results.

---

## 🚀 Usage Examples (Common Actions)

### 1. Search for project documentation
```bash
OUTLINE_API_KEY="..." OUTLINE_URL="..." node skills/outline-app-mcp/scripts/mcp_bridge.mjs call "list_documents" '{"query": "Project Roadmap"}'
```

### 2. Create a new status update
```bash
OUTLINE_API_KEY="..." OUTLINE_URL="..." node skills/outline-app-mcp/scripts/mcp_bridge.mjs call "create_document" '{
  "title": "Weekly Sync - April 1",
  "collectionId": "col_uuid_here",
  "text": "# Update\nEverything is on track."
}'
```

### 3. Append a new row to a table (Token Efficient)
```bash
OUTLINE_API_KEY="..." OUTLINE_URL="..." node skills/outline-app-mcp/scripts/mcp_bridge.mjs call "update_document" '{
  "id": "doc_uuid_here",
  "text": "\n| New Entry | Ready | [Link](url) |",
  "editMode": "append"
}'
```

### 4. Bulk Upload Images & Update Document (Power-Tool)
Use the `bulk_sync.mjs` script for unified Turnaround (Upload + Update).
```bash
OUTLINE_API_KEY="..." OUTLINE_URL="..." node skills/outline-app-mcp/scripts/bulk_sync.mjs "bulk-sync" "target_doc_id" "/path/1.png,/path/2.png" "## 🎨 New Media Assets\n{{MEDIA}}\n---\n*Synced via AI Agent*" "append"
```
- **Inputs**: 
    1. Document ID
    2. Comma-separated absolute file paths.
    3. **Template Text**: Use `{{MEDIA}}` as a placeholder for uploaded images.
    4. **Edit Mode**: `replace`, `append`, or `prepend`.

### 5. Add a Review Comment to a Document
```bash
OUTLINE_API_KEY="..." OUTLINE_URL="..." node skills/outline-app-mcp/scripts/mcp_bridge.mjs call "create_comment" '{
  "documentId": "doc_uuid_here",
  "text": "Draft is ready for review."
}'
```

### 6. Relocate a document to a new Collection
```bash
OUTLINE_API_KEY="..." OUTLINE_URL="..." node skills/outline-app-mcp/scripts/mcp_bridge.mjs call "move_document" '{
  "id": "doc_uuid_here",
  "collectionId": "new_collection_uuid"
}'
```

---

## 💡 Best Practices

### 🚀 Token Efficiency & Cost Optimization (Mandatory)
To minimize token consumption and improve responsiveness, **always prefer `append` or `prepend` modes** when adding new information to existing documents. 
- **Avoid Full Rewrites:** Do NOT use `replace` mode (default) if you only need to add a new row or section.
- **Bulk Sync for Media:** Always use `bulk_sync.mjs` for uploading multiple images to avoid redundant Turnarounds.

## 📜 Technical Requirements
- **Runtime:** Node.js v18+
- **Protocol:** MCP v1.0.0 (over SSE)
- **Dependency:** `@modelcontextprotocol/sdk` (local)
- **Authentication:** Bearer Token via `OUTLINE_API_KEY`
- **Transport:** `StreamableHTTPClientTransport` (POST-based SSE)
