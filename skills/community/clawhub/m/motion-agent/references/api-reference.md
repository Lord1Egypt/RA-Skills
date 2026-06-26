# Motion HTTP API Reference

Base URL: `https://motion-mcp-server.fly.dev`

All endpoints require a session ID obtained from `POST /sessions`.

---

## Session

### Create Session
```
POST /sessions
```

**With agent token (preferred):**
```json
{
  "agent_token": "string (64-char hex)",
  "document_id": "uuid (optional)",
  "agent_name": "Claude (optional, defaults to token name)"
}
```

**With invite token (legacy):**
```json
{
  "document_id": "uuid (optional)",
  "invite_token": "string",
  "agent_name": "Claude"
}
```

- `agent_token` — dedicated workspace token generated from Settings. Grants full workspace access.
- `invite_token` — legacy auth via invite links. One of `agent_token` or `invite_token` is required.
- `document_id` is **optional**. Without it, you get a workspace-only session (pages, folders). Add a document later with `/connect`.

Response: `{ session_id, document_id, agent_name, tools: [...] }`

### Connect to Document
```
POST /sessions/:id/connect
```
```json
{ "document_id": "uuid" }
```
Connect a workspace-only session to a specific document, or switch to a different document.
The document must belong to the session's workspace (validated server-side).
Response: `{ connected: true, document_id }`

### Disconnect
```
DELETE /sessions/:id
```
Response: `{ disconnected: true }`

---

## Document Editing

### Read Document
```
GET /sessions/:id/document
```
Response: `{ blocks: [{ id, index, json }] }`

Each block has a stable UUID `id` and ProseMirror JSON in `json`.

### Read Block
```
GET /sessions/:id/blocks/:block_id
```
Response: `{ id, json }`

### Insert Block (rich text)
```
POST /sessions/:id/blocks
```
```json
{
  "index": 0,
  "block": { "type": "paragraph", "content": [{ "type": "text", "text": "Hello" }] },
  "mode": "suggest"
}
```
Use `index: -1` to append at end. Returns `{ inserted: true, block_id, index, mode }`.
- `mode` — `"suggest"` (default) wraps in suggestion marks; `"direct"` applies immediately

### Insert Block (plain text shorthand)
```
POST /sessions/:id/blocks
```
```json
{ "index": 0, "type": "paragraph", "content": "Hello world", "mode": "suggest" }
```

### Replace Block (rich text)
```
PUT /sessions/:id/blocks/:block_id
```
```json
{
  "block": { "type": "paragraph", "content": [{ "type": "text", "text": "New" }] },
  "mode": "suggest"
}
```
- `mode` — `"suggest"` (default) marks old text as deletion + inserts new as suggestion; `"direct"` replaces immediately

### Update Block (plain text)
```
PUT /sessions/:id/blocks/:block_id
```
```json
{ "content": "Updated text", "mode": "suggest" }
```
- `mode` — `"suggest"` (default) marks old text as deletion + inserts new as suggestion; `"direct"` replaces immediately

### Delete Block
```
DELETE /sessions/:id/blocks/:block_id
```
```json
{ "mode": "suggest" }
```
Response: `{ deleted: true, block_id, mode }`
- `mode` — `"suggest"` (default) marks all text as suggested deletion; `"direct"` removes the block immediately

### Move Block
```
POST /sessions/:id/blocks/:block_id/move
```
```json
{ "to_index": 0 }
```

### Find and Replace Text
```
POST /sessions/:id/blocks/:block_id/replace
```
```json
{ "search": "old text", "replacement": "new text", "mode": "suggest" }
```
- `mode` — `"suggest"` (default) marks old text as deletion + inserts replacement as suggestion; `"direct"` replaces immediately

### Format Text by Match (preferred)
```
POST /sessions/:id/blocks/:block_id/format-by-match
```
```json
{
  "text": "welcome",
  "mark": "bold",
  "attrs": {},
  "occurrence": 1,
  "remove": false
}
```
- `text` — exact text to format (case-sensitive)
- `mark` — mark type: bold, italic, strike, code, underline, link, highlight, textStyle, color
- `attrs` — mark attributes (e.g., `{ "href": "https://..." }` for link)
- `occurrence` — which occurrence if text appears multiple times (1-based, default: 1)
- `remove` — set to true to remove the mark

### Format Text by Offset
```
POST /sessions/:id/blocks/:block_id/format
```
```json
{
  "start": 0,
  "length": 5,
  "mark": "bold",
  "attrs": {},
  "remove": false
}
```
Prefer format-by-match instead — it's more reliable.

---

## Page Management

### List Pages
```
GET /sessions/:id/pages
```
Response: `{ pages: [{ id, title, icon, parent_id, position, is_favorite }] }`

### Create Page
```
POST /sessions/:id/pages
```
```json
{
  "title": "My New Page",
  "parent_id": null,
  "folder_id": null,
  "auto_connect": false
}
```
- `auto_connect` — if `true`, automatically disconnects from the current document and connects to the newly created page. The response includes `connected: true` and `document_id`.

Response: `{ id, title, icon, parent_id, folder_id, position, is_favorite, deleted_at }`
With `auto_connect: true`: `{ id, title, ..., connected: true, document_id }`

### Rename Page
```
PATCH /sessions/:id/pages/:page_id
```
```json
{ "title": "New Title" }
```

### Delete Page (soft-delete to trash)
```
DELETE /sessions/:id/pages/:page_id
```
Response: `{ deleted: true, page_id }`

### Restore Page from Trash
```
POST /sessions/:id/pages/:page_id/restore
```
Response: `{ restored: true, page_id }`

### Move Page
```
POST /sessions/:id/pages/move
```
```json
{
  "page_id": "uuid",
  "after_page_id": "uuid or null",
  "parent_id": "uuid or null"
}
```
- `page_id` — the page to move (required)
- `after_page_id` — place after this page (null = first position)
- `parent_id` — new parent page ID (null = root level)

---

## Folders

### List Folders
```
GET /sessions/:id/folders
```
Response: `{ folders: [{ id, name, icon, color, position }] }`

### Create Folder
```
POST /sessions/:id/folders
```
```json
{ "name": "My Folder" }
```
Response: `{ id, name, icon, color, position }`

### Rename Folder
```
PATCH /sessions/:id/folders/:folder_id
```
```json
{ "name": "New Name" }
```

### Delete Folder
```
DELETE /sessions/:id/folders/:folder_id
```
Pages in the deleted folder are moved to root level (folder_id set to null).

---

## Comments

### List Comment Threads
```
GET /sessions/:id/comments
```
Response: `{ threads: [{ id, page_id, is_resolved, created_by, created_at, comments: [{ id, thread_id, author_id, body, mentions, created_at }] }] }`

### Create Comment Thread
```
POST /sessions/:id/comments
```
```json
{
  "body": "This section needs more detail.",
  "mentions": []
}
```
Response: `{ thread_id }`

### Reply to Thread
```
POST /sessions/:id/comments/:thread_id/reply
```
```json
{
  "body": "I agree, I'll expand on it.",
  "mentions": []
}
```

### Resolve Thread
```
POST /sessions/:id/comments/:thread_id/resolve
```

### Reopen Thread
```
POST /sessions/:id/comments/:thread_id/reopen
```

---

## Version History

### List Versions
```
GET /sessions/:id/versions
```
Response: `{ versions: [{ id, page_id, label, created_by_name, actor_type, trigger_type, created_at }] }`

### Save Version
```
POST /sessions/:id/versions
```
```json
{ "label": "Before restructure" }
```
Label is optional. Saves a snapshot of the current document state.

---

## Export

### Export Document
```
GET /sessions/:id/export?format=markdown
```
Supported formats: `markdown`, `html`

Response: `{ format, content }`

The `content` field contains the full document as a string in the requested format.

---

## Suggestions

### List Suggestions
```
GET /sessions/:id/suggestions
```
Response: `{ suggestions: [{ suggestionId, authorId, authorName, createdAt, type, text, blockId, offset, length }] }`

- `type` is either `"add"` (suggested addition) or `"delete"` (suggested deletion)

### Accept Suggestion
```
POST /sessions/:id/suggestions/:suggestion_id/accept
```
- For additions: keeps the text, removes the suggestion mark
- For deletions: removes the text

### Reject Suggestion
```
POST /sessions/:id/suggestions/:suggestion_id/reject
```
- For additions: removes the text
- For deletions: keeps the text, removes the suggestion mark

### Accept All Suggestions
```
POST /sessions/:id/suggestions/accept-all
```
Response: `{ accepted: count }`

### Reject All Suggestions
```
POST /sessions/:id/suggestions/reject-all
```
Response: `{ rejected: count }`
