---
name: google-docs-connector
description: "Google Docs Connector: Google Docs: create, edit, format documents. Tables, images, headers, page breaks. Export to PDF/DOCX/HTML. Share and manage permissions. Supports file renaming. Use when an agent needs google docs connector, document automation, report generation, template creation, collaborative editing, batch update, document id, requests through AgentPMT-hosted remote tool calls. Discovery terms: google docs connector, document automation, report generation, template creation."
version: 1.0.3
homepage: https://www.agentpmt.com/marketplace/google-docs-connector
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/google-docs-connector"}}
---
# Google Docs Connector

## Freshness
Last updated: `2026-11-08`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Comprehensive Google Docs management tool enabling AI agents to create edit format and share documents through OAuth authentication. Supports rich text formatting with bold italic underline strikethrough and custom fonts paragraph styling with alignment spacing and indentation table creation and manipulation image insertion from URLs headers footers and page breaks named ranges for bookmarking document export to multiple formats including PDF DOCX HTML and EPUB sharing and permission management and natural language document creation. Perfect for document automation report generation collaborative editing template creation and content management workflows.

## Product Instructions
### Google Docs

Create, edit, format, and share Google Docs. Search for documents by name.

#### Parameters

- `action` (string, required): Action to perform. Use get_instructions for full details.
- `document_id` (string): Google Docs document ID (from the document URL). Required for most actions except create_document, search_documents, quick_create.
- `tab_id` (string): Target tab for tab-scoped updates. Get this from `get_document` → `tabs[].tab_id`. Indexed updates default to the first tab when omitted. `replace_text` applies to all tabs when omitted.
- `title` (string): Document title. Required for: create_document
- `query` (string): Search term for search_documents. Matches document names (contains match).
- `max_results` (integer, default 20, range 1-100): Maximum results for search_documents
- `text` (string): Text content for insert_text, create_document (initial content), replace_text, quick_create
- `location` (integer): Zero-based UTF-16 code-unit index for insertions. Defaults to `1`, normally the beginning of a tab body.
- `range_start` (integer): Zero-based, inclusive UTF-16 code-unit start index for format_text and create_named_range.
- `range_end` (integer): Zero-based, exclusive UTF-16 code-unit end index for format_text and create_named_range.
- `search_text` (string): Text to find. Required for: replace_text
- `replace_with` (string): Replacement text. Required for: replace_text
- `match_case` (boolean, default false): Case-sensitive search for replace_text
- `requests` (array of objects): Raw batch update requests for batch_update
- `text_style` (object): Styling: bold, italic, underline, strikethrough, font_family, font_size, foreground_color, background_color, link
- `paragraph_style` (object): Styling: named_style_type (NORMAL_TEXT, TITLE, SUBTITLE, HEADING_1 through HEADING_6), alignment (START/CENTER/END/JUSTIFIED), line_spacing (100/150/200), indents
- `rows` (integer, 1-100): Table rows for create_table
- `columns` (integer, 1-20): Table columns for create_table
- `table_data` (array of arrays): 2D string array of cell data for create_table
- `image_url` (string): Publicly accessible image URL for insert_image
- `width` (integer): Image width in pixels
- `height` (integer): Image height in pixels
- `export_format` (string): One of: pdf, docx, odt, rtf, txt, html, epub, zip
- `share_with` (array of objects): Each with `email`, `role` (reader/writer/commenter), `type` (user/group/domain/anyone)
- `send_notification` (boolean, default true): Send email when sharing
- `email_message` (string): Custom sharing notification message

#### Actions

##### `get_instructions`
Returns this documentation.

##### `create_document`
Creates a new Google Doc.

Required: `title`
Optional: `text` (initial content)

##### `get_document`
Retrieves content and indexed structure from every document tab, including nested child tabs.

Required: `document_id`

The response includes a flattened `tabs` array in UI order. Each item contains `tab_id`, title/hierarchy metadata, extracted `text_content`, and the complete `document_tab` structure with Google-provided `startIndex` and `endIndex` values. Use those returned indices and the matching `tab_id` for subsequent updates.

Indices are zero-based UTF-16 code-unit offsets; `startIndex` is inclusive and `endIndex` is exclusive. Refetch the document after edits that can shift indices.

##### `search_documents`
Searches for Google Docs by name. Returns documents sorted by most recently modified.

Optional: `query` (name contains match), `max_results`

If `query` is omitted, lists recent Google Docs.

##### `insert_text`
Inserts text at a specific position.

Required: `document_id`, `text`
Optional: `location` (default: 1), `tab_id`

##### `replace_text`
Finds and replaces all occurrences of text.

Required: `document_id`, `search_text`, `replace_with`
Optional: `match_case`, `tab_id`. If `tab_id` is omitted, replacement applies to all tabs.

##### `format_text`
Applies text and paragraph styling to a range.

Required: `document_id`, `range_start`, `range_end`, and at least one of `text_style` or `paragraph_style`
Optional: `tab_id`

##### `update_style`
Alias for format_text.

##### `insert_image`
Inserts an inline image.

Required: `document_id`, `image_url`
Optional: `location`, `width`, `height`, `tab_id`

##### `create_table`
Inserts a table, optionally populated with data.

Required: `document_id`
Optional: `rows`, `columns`, `table_data`, `location`, `tab_id`

If `table_data` is provided, dimensions are inferred from it.

##### `insert_page_break`
Required: `document_id`
Optional: `location`, `tab_id`

##### `insert_section_break`
Required: `document_id`
Optional: `location`, `tab_id`

##### `create_header`
Required: `document_id`
Optional: `header_type` (DEFAULT, FIRST_PAGE, EVEN_PAGE, ODD_PAGE), `text`

##### `create_footer`
Required: `document_id`
Optional: `footer_type` (DEFAULT, FIRST_PAGE, EVEN_PAGE, ODD_PAGE)

##### `create_named_range`
Required: `document_id`, `range_name`, `range_start`, `range_end`
Optional: `tab_id`

##### `export_document`
Exports to another format. Text formats return content directly; binary formats return base64.

Required: `document_id`, `export_format`

##### `share_document`
Sets sharing permissions via Google Drive.

Required: `document_id`, `share_with`
Optional: `send_notification`, `email_message`

##### `get_permissions`
Lists current sharing settings.

Required: `document_id`

##### `batch_update`
Executes raw Google Docs API batch update requests for advanced operations.

Required: `document_id`, `requests`

For a request containing a `range` or `location`, put `tabId` inside that raw range/location. The top-level `tab_id` parameter is not injected into raw requests.

##### `quick_create`
Creates a document from a natural language description.

Required: `text`
Optional: `title`

#### Examples

```json
{"action":"search_documents","query":"meeting notes"}
```

```json
{"action":"search_documents","query":"Q1 report","max_results":5}
```

```json
{"action":"create_document","title":"Meeting Notes","text":"Agenda:\n1. Review\n2. Planning"}
```

```json
{"action":"get_document","document_id":"1a2b3c4d5e"}
```

```json
{"action":"insert_text","document_id":"1a2b3c4d5e","tab_id":"t.abc123","text":"New paragraph\n","location":1}
```

```json
{"action":"replace_text","document_id":"1a2b3c4d5e","search_text":"draft","replace_with":"final"}
```

```json
{"action":"format_text","document_id":"1a2b3c4d5e","tab_id":"t.abc123","range_start":1,"range_end":10,"text_style":{"bold":true,"font_size":{"magnitude":14,"unit":"PT"}}}
```

Apply a real heading style in a specific tab:

```json
{"action":"format_text","document_id":"1a2b3c4d5e","tab_id":"t.abc123","range_start":1,"range_end":18,"paragraph_style":{"named_style_type":"HEADING_1"}}
```

Create a real numbered list in a specific tab using indices returned by `get_document`:

```json
{"action":"batch_update","document_id":"1a2b3c4d5e","requests":[{"createParagraphBullets":{"range":{"tabId":"t.abc123","startIndex":20,"endIndex":58},"bulletPreset":"NUMBERED_DECIMAL_ALPHA_ROMAN"}}]}
```

```json
{"action":"export_document","document_id":"1a2b3c4d5e","export_format":"pdf"}
```

```json
{"action":"share_document","document_id":"1a2b3c4d5e","share_with":[{"email":"user@example.com","role":"writer","type":"user"}]}
```

#### Response

All responses return `{"success": true, "output": { ... }}`. Output varies by action:

- `search_documents` → `{"query": "...", "result_count": N, "documents": [{"document_id", "name", "modified_time", "web_view_link", ...}]}`
- `create_document` → `{"document_id", "title", "revision_id"}`
- `get_document` → `{"document_id", "title", "text_content", "word_count", "tab_count", "tabs", "index_semantics", "raw_document"}`
- `replace_text` → `{"occurrences_changed": N}`
- `export_document` → `{"content": "..."}` (text) or `{"content_base64": "..."}` (binary)
- `share_document` → `{"permissions_added": N, "permissions": [...]}`
- `get_permissions` → `{"permissions": [...]}`


##### `rename_document`
Renames the Google Doc file, not a document tab. Required: `document_id`, nonblank `new_title`. No optional fields. The document ID and URL remain unchanged.
```json
{"action":"rename_document","document_id":"DOC_ID","new_title":"Q4 Report"}
```

## When To Use
- Use this skill for `Google Docs Connector` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: google docs connector, document automation, report generation, template creation, collaborative editing, batch update, document id, requests.
- Supported action names: `batch_update`, `create_document`, `create_footer`, `create_from_markdown`, `create_header`, `create_named_range`, `create_tab`, `create_table`, `export_document`, `format_text`, `get_document`, `get_permissions`, `insert_image`, `insert_page_break`, `insert_section_break`, `insert_text`, `quick_create`, `rename_document`, `render_markdown`, `replace_text`, `replace_with_markdown`, `search_documents`, `share_document`, `update_style`.

## Use Cases
- document automation
- report generation
- template creation
- collaborative editing
- content management
- proposal writing
- meeting agenda creation
- contract generation
- documentation workflows
- batch document processing

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `24`.
x402 availability: not enabled for this product.

- `batch_update` (action slug: `batch-update`): Execute raw Google Docs API batch update requests. Put tabId inside each raw range or location when targeting a non-first tab. Price: `5` credits. Parameters: `document_id`, `requests`.
- `create_document` (action slug: `create-document`): Create a new, empty Google Doc. Prefer create_from_markdown when the content has any structure. Price: `5` credits. Parameters: `text`, `title`.
- `create_footer` (action slug: `create-footer`): Add a footer to the document. Price: `5` credits. Parameters: `document_id`, `footer_type`.
- `create_from_markdown` (action slug: `create-from-markdown`): Create a new Google Doc from markdown. Drive converts the markdown into real Google Docs formatting (headings, lists, tables, bold/italic), so no index arithmetic is needed. Preferred way to author a new document. Price: `5` credits. Parameters: `markdown`, `parent_folder_id`, `title`.
- `create_header` (action slug: `create-header`): Add a header to the document. Price: `5` credits. Parameters: `document_id`, `header_type`, `text`.
- `create_named_range` (action slug: `create-named-range`): Create a named range (bookmark) spanning a character range in the document. Price: `5` credits. Parameters: `document_id`, `range_end`, `range_name`, `range_start`, `tab_id`.
- `create_tab` (action slug: `create-tab`): Add a document tab and return its new tab ID, ready to pass to render_markdown or any indexed update. Uses the Docs addDocumentTab request. Price: `5` credits. Parameters: `document_id`, `icon_emoji`, `index`, `parent_tab_id`, `title`.
- `create_table` (action slug: `create-table`): Insert a table into a document, optionally populated with data. If table_data is provided, dimensions are inferred from it. A markdown pipe table through render_markdown is usually simpler. Price: `5` credits. Parameters: `columns`, `document_id`, `location`, `rows`, `tab_id`, `table_data`.
- `export_document` (action slug: `export-document`): Export a document to another format. Text formats (txt, html, md) return content directly; binary formats return base64-encoded content. Use md to read a document as markdown, revise it, and send it back through render_markdown or replace_with_markdown. Price: `5` credits. Parameters: `document_id`, `export_format`.
- `format_text` (action slug: `format-text`): Apply text and/or paragraph styling to a zero-based UTF-16 range in a specific document tab. Provide at least one non-empty style object. Price: `5` credits. Parameters: `document_id`, `paragraph_style`, `range_end`, `range_start`, `tab_id`, `text_style`.
- `get_document` (action slug: `get-document`): Retrieve content and indexed structure from every document tab, including nested child tabs. Price: `5` credits. Parameters: `document_id`.
- `get_permissions` (action slug: `get-permissions`): List the current sharing permissions on a document. Price: `5` credits. Parameters: `document_id`.
- `insert_image` (action slug: `insert-image`): Insert an inline image from a publicly accessible URL. Price: `5` credits. Parameters: `document_id`, `height`, `image_url`, `location`, `tab_id`, `width`.
- `insert_page_break` (action slug: `insert-page-break`): Insert a page break at a specific position. Price: `5` credits. Parameters: `document_id`, `location`, `tab_id`.
- `insert_section_break` (action slug: `insert-section-break`): Insert a section break at a specific position. Price: `5` credits. Parameters: `document_id`, `location`, `tab_id`.
- `insert_text` (action slug: `insert-text`): Insert text at a specific character position in a document. Price: `5` credits. Parameters: `document_id`, `location`, `tab_id`, `text`.
- `quick_create` (action slug: `quick-create`): Create a document from a natural language description. Any markdown in the description becomes real formatting. If the text contains 'titled "..."' or 'called "..."', the title is extracted automatically. Price: `5` credits. Parameters: `text`, `title`.
- `rename_document` (action slug: `rename-document`): Rename an existing Google Doc file without changing its document tabs or ID. Price: `5` credits. Parameters: `document_id`, `new_title`.
- `render_markdown` (action slug: `render-markdown`): Render markdown into an existing document without destroying the rest of it. The tool computes every UTF-16 index, so the caller supplies only markdown and an insertion point. Preferred way to add formatted content to an existing document. Price: `5` credits. Parameters: `document_id`, `location`, `markdown`, `range_end`, `range_start`, `tab_id`.
- `replace_text` (action slug: `replace-text`): Find and replace text in one tab, or in all tabs when tab_id is omitted. Price: `5` credits. Parameters: `document_id`, `match_case`, `replace_with`, `search_text`, `tab_id`.
- `replace_with_markdown` (action slug: `replace-with-markdown`): Replace an existing document's entire body from markdown, keeping its document ID, URL and sharing. Destructive: prefer render_markdown unless a full-body rewrite is intended. Price: `5` credits. Parameters: `confirm_replace`, `document_id`, `markdown`, `new_title`.
- `search_documents` (action slug: `search-documents`): Search for Google Docs by name. Returns documents sorted by most recently modified. Omit query to list recent documents. Price: `5` credits. Parameters: `max_results`, `query`.
- `share_document` (action slug: `share-document`): Set sharing permissions on a document via Google Drive. Price: `5` credits. Parameters: `document_id`, `email_message`, `send_notification`, `share_with`.
- `update_style` (action slug: `update-style`): Alias for format_text. Apply text and/or paragraph styling to a zero-based UTF-16 range in a specific tab. Price: `5` credits. Parameters: `document_id`, `paragraph_style`, `range_end`, `range_start`, `tab_id`, `text_style`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "google-docs-connector"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "google-docs-connector"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "google-docs-connector"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "google-docs-connector"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "google-docs-connector"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "google-docs-connector"
  }
}
```

## Call This Tool
Product slug: `google-docs-connector`

Marketplace page: https://www.agentpmt.com/marketplace/google-docs-connector

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Google-Docs-Connector",
    "arguments": {
      "action": "batch_update",
      "document_id": "example document id",
      "requests": [
        {}
      ]
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "google-docs-connector",
  "parameters": {
    "action": "batch_update",
    "document_id": "example document id",
    "requests": [
      {}
    ]
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `batch_update` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/google-docs-connector
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
