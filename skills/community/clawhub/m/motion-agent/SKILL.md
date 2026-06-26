---
name: motion-agent
description: >
  Use this skill when the user pastes a Motion invite URL (contains /invite/ or /agent/),
  asks to "edit a Motion document", "connect to Motion", "collaborate on a document",
  "write to Motion", or provides a document_id/agent_token/invite_token for real-time editing.
  Also triggers on "Motion MCP", "review suggestions", "leave a comment on the doc",
  "export the document", "save a version", "list pages", or "create a page".
---

# Motion Document Agent

You are a real-time collaborative document editor. Your edits appear live in the user's
browser. You appear in the presence bar alongside human collaborators. Other users may be
viewing and editing the same document simultaneously.

By default, your edits are wrapped in **suggestion marks** so humans can review and
accept/reject them before they become permanent. You can also operate in direct mode.

## Authentication

There are two auth methods:

### Agent token (preferred)

Workspace admins generate **agent tokens** from Settings > Agent tokens. Each token grants
full access to all documents in the workspace. The token is a 64-character hex string.

```bash
curl -X POST https://motion-mcp-server.fly.dev/sessions \
  -H "Content-Type: application/json" \
  -d '{"agent_token": "{TOKEN}", "agent_name": "Claude"}'
```

### Invite token (legacy)

Extract from an invite URL: `https://{APP_HOST}/invite/{INVITE_TOKEN}/{DOCUMENT_ID}`

```bash
curl -X POST https://motion-mcp-server.fly.dev/sessions \
  -H "Content-Type: application/json" \
  -d '{"invite_token": "{INVITE_TOKEN}", "document_id": "{DOCUMENT_ID}", "agent_name": "Claude"}'
```

## Connection

### Workspace-first flow (recommended with agent tokens)

Create a session without a document — browse, create, then connect:

```bash
# 1. Create workspace-only session
curl -X POST $BASE/sessions \
  -H "Content-Type: application/json" \
  -d '{"agent_token": "{TOKEN}", "agent_name": "Claude"}'

# 2. List pages, create pages, manage folders — all without a document

# 3. Connect to a document when ready
curl -X POST $BASE/sessions/:id/connect \
  -H "Content-Type: application/json" \
  -d '{"document_id": "{PAGE_ID}"}'

# 4. Or create a new page and connect in one step
curl -X POST $BASE/sessions/:id/pages \
  -H "Content-Type: application/json" \
  -d '{"title": "My Doc", "auto_connect": true}'
```

### Direct document session

If you know which document to edit, connect immediately:

```bash
curl -X POST $BASE/sessions \
  -H "Content-Type: application/json" \
  -d '{"agent_token": "{TOKEN}", "document_id": "{PAGE_ID}", "agent_name": "Claude"}'
```

### Switch documents

Switch to a different document within the same session (workspace boundary enforced):

```bash
curl -X POST $BASE/sessions/:id/connect \
  -H "Content-Type: application/json" \
  -d '{"document_id": "{ANOTHER_PAGE_ID}"}'
```

### Disconnect when done

```bash
curl -X DELETE $BASE/sessions/:id
```

## Security Model

- **Agent tokens** grant workspace-wide access — all documents, folders, comments, versions
- Agents can only access documents within their authorized workspace
- `switch_document` and `/connect` validate that the target document belongs to the workspace
- All page/folder mutations are workspace-scoped at the database level
- Tokens can be revoked by workspace admins at any time

## Core Editing Workflow

1. **Read first** — call `GET /sessions/:id/document` to get all blocks with stable IDs
2. **Edit by block ID** — always use block IDs (UUIDs), never array indexes. IDs persist across concurrent edits.
3. **Use format_text_by_match** for formatting — specify the text string, not character offsets
4. **Re-read after edits** if you need to continue editing or verify changes
5. **Disconnect** when done

## Suggestion Mode

Agents default to **suggestion mode**: edits appear as green underlines (additions) or
strikethroughs (deletions) that humans can accept or reject.

All edit endpoints (`insert`, `update`, `replace`, `delete`, `find-and-replace`) accept an
optional `"mode"` field:
- `"suggest"` (default) — wraps edits in suggestion marks for human review
- `"direct"` — applies edits immediately without suggestion marks

You can also:
- **List suggestions**: see all pending suggestions in the document
- **Accept/reject**: review another agent's suggestions
- **Bulk operations**: accept-all or reject-all

## Capabilities

### Page & Folder Management (workspace-level — no document connection needed)
List all workspace pages and folders. Create, rename, delete, restore pages. Create,
rename, delete folders. Move pages between folders and positions. These work even
without a document connection.

For endpoint details: read `references/api-reference.md` (Page Management and Folder sections)

### Document Editing (requires document connection)
Read, insert, update, delete, move blocks. Apply formatting (bold, italic, links, etc.).
Find and replace text. Full ProseMirror JSON support for rich content.

For endpoint details: read `references/api-reference.md` (Document Editing section)
For block/mark JSON format: read `references/block-format-reference.md`

### Comments (requires document connection)
Read all comment threads on a page. Create new threads, reply to existing ones,
resolve threads when discussion is complete, reopen resolved threads.

For endpoint details: read `references/api-reference.md` (Comments section)

### Version History (requires document connection)
List saved versions. Save a named version snapshot before making large changes.
Useful for checkpointing your work.

For endpoint details: read `references/api-reference.md` (Versions section)

### Export (requires document connection)
Export the current document as Markdown or HTML. Returns content as text.

For endpoint details: read `references/api-reference.md` (Export section)

### Suggestion Review (requires document connection)
List all pending suggestions. Accept or reject individual suggestions by ID.
Bulk accept-all or reject-all.

For endpoint details: read `references/api-reference.md` (Suggestions section)

## Quick Reference: Key Endpoints

### Workspace-level (no document needed)
| Action | Method | Path |
|--------|--------|------|
| Create session | POST | `/sessions` |
| Connect to document | POST | `/sessions/:id/connect` |
| List pages | GET | `/sessions/:id/pages` |
| Create page | POST | `/sessions/:id/pages` |
| Create page + connect | POST | `/sessions/:id/pages` (with `auto_connect: true`) |
| Rename page | PATCH | `/sessions/:id/pages/:pid` |
| Delete page | DELETE | `/sessions/:id/pages/:pid` |
| Restore page | POST | `/sessions/:id/pages/:pid/restore` |
| Move page | POST | `/sessions/:id/pages/move` |
| List folders | GET | `/sessions/:id/folders` |
| Create folder | POST | `/sessions/:id/folders` |
| Rename folder | PATCH | `/sessions/:id/folders/:fid` |
| Delete folder | DELETE | `/sessions/:id/folders/:fid` |
| Disconnect | DELETE | `/sessions/:id` |

### Document-level (requires document connection)
| Action | Method | Path |
|--------|--------|------|
| Read document | GET | `/sessions/:id/document` |
| Insert block | POST | `/sessions/:id/blocks` |
| Format text | POST | `/sessions/:id/blocks/:bid/format-by-match` |
| Delete block | DELETE | `/sessions/:id/blocks/:bid` |
| List comments | GET | `/sessions/:id/comments` |
| Create comment | POST | `/sessions/:id/comments` |
| Save version | POST | `/sessions/:id/versions` |
| Export | GET | `/sessions/:id/export?format=markdown` |
| List suggestions | GET | `/sessions/:id/suggestions` |
| Accept suggestion | POST | `/sessions/:id/suggestions/:sid/accept` |

For the complete API with request/response schemas: read `references/api-reference.md`
For common editing patterns and examples: read `references/examples.md`

## Tips

- Use an **agent token** for workspace-wide access — no need to deal with invite URLs
- Create a workspace-only session first, list pages, then connect to the one you need
- Use `auto_connect: true` when creating a page to start editing it immediately
- Always call `read_document` first to understand block structure and IDs
- Use `format-by-match` instead of offset-based formatting — it handles nested blocks
- When building a list, send the entire list as one `insert_block` call
- Save a version before making large destructive changes
- The agent identifies as `agent:Claude` in comments and suggestions
- If the same text appears multiple times, use the `occurrence` parameter
- Use `POST /sessions/:id/connect` to switch between documents without creating a new session
- Callout blocks support variants: info, warning, error, success
- Agents can only access documents within their authorized workspace — cross-workspace access is blocked
