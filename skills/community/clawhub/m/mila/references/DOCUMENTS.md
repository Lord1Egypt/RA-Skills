# Documents Reference

Documents store rich text content as HTML. You can create, read, update, append to, and delete documents via the REST API or MCP tools.

## List Documents

**REST API:**

```
GET /v1/documents
```

**Query parameters:**

| Param | Default | Description |
|---|---|---|
| `limit` | 50 | Results per page (1-100) |
| `offset` | 0 | Pagination offset |
| `sort` | `updated_at` | Sort field: `created_at`, `updated_at`, `last_edited_at`, `title` |
| `order` | `desc` | Sort order: `asc` or `desc` |
| `server_id` | *(all)* | Filter: omit for all, `personal` for personal files, or a server ID |

```bash
curl https://api.mila.gg/v1/documents \
  -H "Authorization: Bearer mila_sk_your_key_here"
```

**MCP tool:** `list_documents`

Parameters: `limit`, `offset`, `sort`, `order`, `server_id` (all optional).

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": "aB3kQ9xZwm",
      "title": "Meeting Notes",
      "server_id": null,
      "created_at": "2026-02-26T10:00:00.000Z",
      "updated_at": "2026-02-26T14:30:00.000Z",
      "last_edited_at": "2026-02-26T14:30:00.000Z"
    }
  ],
  "pagination": { "total": 1, "limit": 50, "offset": 0 }
}
```

Note: List responses do not include document content. Use the get endpoint for full content.

---

## Get Document

**REST API:**

```
GET /v1/documents/:id
```

```bash
curl https://api.mila.gg/v1/documents/aB3kQ9xZwm \
  -H "Authorization: Bearer mila_sk_your_key_here"
```

**MCP tool:** `get_document`

Parameters: `id` (required, string).

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "aB3kQ9xZwm",
    "title": "Meeting Notes",
    "content": {
      "blocks": [...],
      "title": "Meeting Notes",
      "version": "v2"
    },
    "server_id": null,
    "created_at": "2026-02-26T10:00:00.000Z",
    "updated_at": "2026-02-26T14:30:00.000Z",
    "last_edited_at": "2026-02-26T14:30:00.000Z"
  }
}
```

The `content` field contains a v2 block format with `blocks`, `title`, and `version` fields. The blocks array represents the document's structured content.

---

## Create Document

**REST API:**

```
POST /v1/documents
```

**Body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | Yes | Document title |
| `content` | string | No | HTML content |
| `server_id` | string or null | No | Server to create in (null = personal files) |

The `content` field accepts HTML. You can use any standard HTML elements: headings, paragraphs, lists, tables, images, links. `<script>` tags are automatically stripped for security.

```bash
curl -X POST https://api.mila.gg/v1/documents \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Project Brief",
    "content": "<h1>Project Brief</h1><p>This project aims to <strong>improve</strong> our onboarding flow.</p><h2>Goals</h2><ul><li>Reduce time-to-value</li><li>Increase activation rate</li></ul><h2>Timeline</h2><p>We plan to ship by <em>Q3 2026</em>.</p>"
  }'
```

**MCP tool:** `create_document`

Parameters: `title` (required), `content` (optional, HTML string), `server_id` (optional).

**Supported HTML elements:**

```html
<!-- Headings -->
<h1>Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>

<!-- Text -->
<p>Regular paragraph with <strong>bold</strong> and <em>italic</em> text.</p>

<!-- Lists -->
<ul>
  <li>Unordered item</li>
</ul>
<ol>
  <li>Ordered item</li>
</ol>

<!-- Tables -->
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Alice</td><td>Engineer</td></tr>
</table>

<!-- Images -->
<img src="https://example.com/photo.png" alt="Description" />

<!-- Links -->
<a href="https://example.com">Link text</a>
```

---

## Update Document

**REST API:**

```
PUT /v1/documents/:id
```

**Body** (all fields optional):

| Field | Type | Description |
|---|---|---|
| `title` | string | New title |
| `content` | string | New HTML content (replaces entire document body) |

```bash
curl -X PUT https://api.mila.gg/v1/documents/aB3kQ9xZwm \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"title": "Renamed Document"}'
```

**MCP tool:** `update_document`

Parameters: `id` (required), `title` (optional), `content` (optional, HTML string).

Note: Updating `content` replaces the entire document body. To add content without replacing, use the append endpoint.

---

## Append to Document

**REST API:**

```
POST /v1/documents/:id/append
```

Appends HTML content to the end of an existing document without replacing existing content.

**Body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `content` | string | Yes | HTML content to append |

`<script>` tags are stripped from the appended content.

```bash
curl -X POST https://api.mila.gg/v1/documents/aB3kQ9xZwm/append \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "<h2>Meeting Notes</h2><p>Discussed roadmap priorities for Q3.</p><ul><li>Feature A - high priority</li><li>Feature B - medium priority</li></ul>"
  }'
```

**MCP tool:** `append_to_document`

Parameters: `id` (required), `content` (required, HTML string).

This is useful for:
- Incrementally building documents
- Logging entries or journal-style additions
- Adding content from automated workflows without reading the full document first

---

## Delete Document

**REST API:**

```
DELETE /v1/documents/:id
```

Permanently deletes the document.

```bash
curl -X DELETE https://api.mila.gg/v1/documents/aB3kQ9xZwm \
  -H "Authorization: Bearer mila_sk_your_key_here"
```

**MCP tool:** `delete_document`

Parameters: `id` (required).
