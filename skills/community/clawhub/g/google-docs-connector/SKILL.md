---
name: google-docs-connector
description: "Google Docs Connector: Google Docs: create, edit, format documents. Tables, images, headers, page breaks. Export to PDF/DOCX/HTML. Share and manage permissions. Use when an agent needs google docs connector, document automation, report generation, template creation, collaborative editing, batch update, document id, requests through AgentPMT-hosted remote tool calls. Discovery terms: google docs connector, document automation, report generation, template creation, collaborative editing."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/google-docs-connector
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/google-docs-connector"}}
---
# Google Docs Connector

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Comprehensive Google Docs management tool enabling AI agents to create edit format and share documents through OAuth authentication. Supports rich text formatting with bold italic underline strikethrough and custom fonts paragraph styling with alignment spacing and indentation table creation and manipulation image insertion from URLs headers footers and page breaks named ranges for bookmarking document export to multiple formats including PDF DOCX HTML and EPUB sharing and permission management and natural language document creation. Perfect for document automation report generation collaborative editing template creation and content management workflows.

## Product Instructions
### Google Docs Connector

Create, edit, format, and share Google Docs programmatically. Search for documents, insert text and images, build tables, apply formatting, export to multiple formats, and manage sharing permissions.

#### Actions

##### create_document
Create a new Google Doc.

**Required:** `title`
**Optional:** `text` (initial body content)

```json
{"action": "create_document", "title": "Meeting Notes", "text": "Agenda:\n1. Review\n2. Planning"}
```

##### get_document
Retrieve a document's full content, text, word count, and structure.

**Required:** `document_id`

```json
{"action": "get_document", "document_id": "1a2b3c4d5e"}
```

##### search_documents
Search for Google Docs by name. Returns documents sorted by most recently modified. Omit `query` to list recent documents.

**Optional:** `query` (name contains match), `max_results` (1-100, default 20)

```json
{"action": "search_documents", "query": "Q1 report", "max_results": 5}
```

##### insert_text
Insert text at a specific character position in a document.

**Required:** `document_id`, `text`
**Optional:** `location` (1-based character index; default: 1)

```json
{"action": "insert_text", "document_id": "1a2b3c4d5e", "text": "New paragraph\n", "location": 1}
```

##### replace_text
Find and replace all occurrences of text in a document.

**Required:** `document_id`, `search_text`, `replace_with`
**Optional:** `match_case` (default: false)

```json
{"action": "replace_text", "document_id": "1a2b3c4d5e", "search_text": "draft", "replace_with": "final", "match_case": true}
```

##### format_text
Apply text and/or paragraph styling to a character range.

**Required:** `document_id`, `range_start`, `range_end`, `text_style`
**Optional:** `paragraph_style`

`text_style` options: `bold`, `italic`, `underline`, `strikethrough` (booleans), `font_family` (string), `font_size` (object with `magnitude` and `unit`), `foreground_color`, `background_color` (RGB objects with values 0-1), `link` (URL string)

`paragraph_style` options: `alignment` (START, CENTER, END, JUSTIFIED), `line_spacing` (100=single, 150=1.5x, 200=double), `indent_start`, `indent_end`, `indent_first_line` (objects with `magnitude` and `unit`)

```json
{"action": "format_text", "document_id": "1a2b3c4d5e", "range_start": 1, "range_end": 15, "text_style": {"bold": true, "font_size": {"magnitude": 18, "unit": "PT"}}, "paragraph_style": {"alignment": "CENTER"}}
```

##### update_style
Alias for `format_text`. Accepts the same parameters.

```json
{"action": "update_style", "document_id": "1a2b3c4d5e", "range_start": 1, "range_end": 10, "text_style": {"italic": true}}
```

##### insert_image
Insert an inline image from a publicly accessible URL.

**Required:** `document_id`, `image_url`
**Optional:** `location` (1-based index; default: 1), `width` (pixels), `height` (pixels)

```json
{"action": "insert_image", "document_id": "1a2b3c4d5e", "image_url": "https://example.com/logo.png", "width": 200, "height": 100, "location": 1}
```

##### create_table
Insert a table into a document. If `table_data` is provided, dimensions are inferred from it and cells are populated.

**Required:** `document_id`
**Optional:** `rows` (1-100), `columns` (1-20), `table_data` (2D array of strings), `location` (1-based index; default: 1)

```json
{"action": "create_table", "document_id": "1a2b3c4d5e", "table_data": [["Name", "Role"], ["Alice", "Engineer"], ["Bob", "Designer"]]}
```

```json
{"action": "create_table", "document_id": "1a2b3c4d5e", "rows": 3, "columns": 4, "location": 1}
```

##### insert_page_break
Insert a page break at a specific position.

**Required:** `document_id`
**Optional:** `location` (1-based index; default: 1)

```json
{"action": "insert_page_break", "document_id": "1a2b3c4d5e", "location": 50}
```

##### insert_section_break
Insert a section break at a specific position.

**Required:** `document_id`
**Optional:** `location` (1-based index; default: 1)

```json
{"action": "insert_section_break", "document_id": "1a2b3c4d5e", "location": 100}
```

##### create_header
Add a header to the document.

**Required:** `document_id`
**Optional:** `header_type` (DEFAULT, FIRST_PAGE, EVEN_PAGE, ODD_PAGE; default: DEFAULT), `text` (header content)

```json
{"action": "create_header", "document_id": "1a2b3c4d5e", "header_type": "DEFAULT", "text": "Company Report"}
```

##### create_footer
Add a footer to the document.

**Required:** `document_id`
**Optional:** `footer_type` (DEFAULT, FIRST_PAGE, EVEN_PAGE, ODD_PAGE; default: DEFAULT)

```json
{"action": "create_footer", "document_id": "1a2b3c4d5e", "footer_type": "DEFAULT"}
```

##### create_named_range
Create a named range (bookmark) spanning a character range in the document.

**Required:** `document_id`, `range_name`, `range_start`, `range_end`

```json
{"action": "create_named_range", "document_id": "1a2b3c4d5e", "range_name": "introduction", "range_start": 1, "range_end": 50}
```

##### export_document
Export a document to another format. Text formats (txt, html) return content directly; binary formats (pdf, docx, etc.) return base64-encoded content.

**Required:** `document_id`, `export_format`

Supported formats: `pdf`, `docx`, `odt`, `rtf`, `txt`, `html`, `epub`, `zip`

```json
{"action": "export_document", "document_id": "1a2b3c4d5e", "export_format": "pdf"}
```

##### share_document
Set sharing permissions on a document.

**Required:** `document_id`, `share_with` (array of permission objects)

Each permission object: `email` (for user/group), `role` (reader, writer, commenter), `type` (user, group, domain, anyone), `domain` (for domain-wide sharing)

**Optional:** `send_notification` (default: true), `email_message` (custom notification text)

```json
{"action": "share_document", "document_id": "1a2b3c4d5e", "share_with": [{"email": "colleague@example.com", "role": "writer", "type": "user"}], "send_notification": true, "email_message": "Please review this document."}
```

##### get_permissions
List the current sharing permissions on a document.

**Required:** `document_id`

```json
{"action": "get_permissions", "document_id": "1a2b3c4d5e"}
```

##### batch_update
Execute raw Google Docs API batch update requests for advanced operations not covered by other actions.

**Required:** `document_id`, `requests` (array of Google Docs API request objects)

```json
{"action": "batch_update", "document_id": "1a2b3c4d5e", "requests": [{"insertText": {"location": {"index": 1}, "text": "Hello World\n"}}]}
```

##### quick_create
Create a document from a natural language description. If the description contains a phrase like `titled "..."` or `called "..."`, the title is extracted automatically.

**Required:** `text` (description or content)
**Optional:** `title`

```json
{"action": "quick_create", "text": "Create a project plan titled \"Q2 Launch Plan\" with sections for goals, timeline, and team assignments."}
```

#### Common Workflows

**Create and populate a document:**
1. `create_document` with title and initial text
2. `insert_text` to add more content at specific positions
3. `format_text` to style headings, bold key terms, etc.
4. `share_document` to distribute

**Build a report with a table:**
1. `create_document` with the report title
2. `insert_text` for the report body
3. `create_table` with `table_data` for structured data
4. `export_document` as PDF for distribution

**Find and update a document:**
1. `search_documents` to locate the document by name
2. `get_document` to read current content
3. `replace_text` or `insert_text` to make changes
4. `format_text` to adjust styling

#### Important Notes
- The `document_id` is the alphanumeric string found in the Google Docs URL between `/d/` and `/edit`.
- Character indices are 1-based. Use `get_document` to inspect the document structure and find the correct indices for insertions and formatting.
- When using `format_text`, you must provide at least `text_style`. The `paragraph_style` is optional and applied to the same range.
- The `update_style` action is identical to `format_text`.
- For `create_table` with `table_data`, the number of rows and columns is inferred from the data array. You do not need to specify `rows` or `columns` separately.
- Export formats `txt` and `html` return plain text content. All other formats return base64-encoded binary data.
- Sharing uses Google Drive permissions. The `anyone` type makes the document publicly accessible with the specified role.

## When To Use
- Use this skill for `Google Docs Connector` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: google docs connector, document automation, report generation, template creation, collaborative editing, batch update, document id, requests.
- Supported action names: `batch_update`, `create_document`, `create_footer`, `create_header`, `create_named_range`, `create_table`, `export_document`, `format_text`, `get_document`, `get_permissions`, `insert_image`, `insert_page_break`, `insert_section_break`, `insert_text`, `quick_create`, `replace_text`, `search_documents`, `share_document`, `update_style`.

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
Supported action count: `19`.
x402 availability: not enabled for this product.

- `batch_update` (action slug: `batch-update`): Execute raw Google Docs API batch update requests for advanced operations not covered by other actions. Price: `5` credits. Parameters: `document_id`, `requests`.
- `create_document` (action slug: `create-document`): Create a new Google Doc. Price: `5` credits. Parameters: `text`, `title`.
- `create_footer` (action slug: `create-footer`): Add a footer to the document. Price: `5` credits. Parameters: `document_id`, `footer_type`.
- `create_header` (action slug: `create-header`): Add a header to the document. Price: `5` credits. Parameters: `document_id`, `header_type`, `text`.
- `create_named_range` (action slug: `create-named-range`): Create a named range (bookmark) spanning a character range in the document. Price: `5` credits. Parameters: `document_id`, `range_end`, `range_name`, `range_start`.
- `create_table` (action slug: `create-table`): Insert a table into a document, optionally populated with data. If table_data is provided, dimensions are inferred from it. Price: `5` credits. Parameters: `columns`, `document_id`, `location`, `rows`, `table_data`.
- `export_document` (action slug: `export-document`): Export a document to another format. Text formats (txt, html) return content directly; binary formats return base64-encoded content. Price: `5` credits. Parameters: `document_id`, `export_format`.
- `format_text` (action slug: `format-text`): Apply text and/or paragraph styling to a character range in a document. Price: `5` credits. Parameters: `document_id`, `paragraph_style`, `range_end`, `range_start`, `text_style`.
- `get_document` (action slug: `get-document`): Retrieve a document's full content, text, word count, and structure. Price: `5` credits. Parameters: `document_id`.
- `get_permissions` (action slug: `get-permissions`): List the current sharing permissions on a document. Price: `5` credits. Parameters: `document_id`.
- `insert_image` (action slug: `insert-image`): Insert an inline image from a publicly accessible URL. Price: `5` credits. Parameters: `document_id`, `height`, `image_url`, `location`, `width`.
- `insert_page_break` (action slug: `insert-page-break`): Insert a page break at a specific position. Price: `5` credits. Parameters: `document_id`, `location`.
- `insert_section_break` (action slug: `insert-section-break`): Insert a section break at a specific position. Price: `5` credits. Parameters: `document_id`, `location`.
- `insert_text` (action slug: `insert-text`): Insert text at a specific character position in a document. Price: `5` credits. Parameters: `document_id`, `location`, `text`.
- `quick_create` (action slug: `quick-create`): Create a document from a natural language description. If the text contains 'titled "..."' or 'called "..."', the title is extracted automatically. Price: `5` credits. Parameters: `text`, `title`.
- `replace_text` (action slug: `replace-text`): Find and replace all occurrences of text in a document. Price: `5` credits. Parameters: `document_id`, `match_case`, `replace_with`, `search_text`.
- `search_documents` (action slug: `search-documents`): Search for Google Docs by name. Returns documents sorted by most recently modified. Omit query to list recent documents. Price: `5` credits. Parameters: `max_results`, `query`.
- `share_document` (action slug: `share-document`): Set sharing permissions on a document via Google Drive. Price: `5` credits. Parameters: `document_id`, `email_message`, `send_notification`, `share_with`.
- `update_style` (action slug: `update-style`): Alias for format_text. Apply text and/or paragraph styling to a character range. Price: `5` credits. Parameters: `document_id`, `paragraph_style`, `range_end`, `range_start`, `text_style`.

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
