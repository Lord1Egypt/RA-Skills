---
name: google-docs-documents
description: Google Docs API integration with managed OAuth. Search, read, create, and update Google Docs documents. Use this skill when users want to read document text, create drafts from prompts, insert content, or modify document structure.
---

# Google Docs

![Google Docs](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/google-docs.svg)

Access Google Docs via the Google Docs API with managed OAuth authentication. Search, read, create, and update documents stored in Google Drive.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-docs-documents) for hosted connection flows and credentials so you do not need to configure Google Docs API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Google Docs |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Docs |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Google Docs    │
│   (User Chat)   │     │   (OAuth)    │     │   (Docs API)     │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Docs      │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Google  │
   │  File    │           │ Auth     │           │  Drive   │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Docs again."

## Quick Start

```bash
# Search for documents
clawlink_call_tool --tool "googledocs_search_documents" --params '{"query": "report"}'

# Get document plaintext
clawlink_call_tool --tool "googledocs_get_document_plaintext" --params '{"document_id": "YOUR_DOCUMENT_ID"}'

# Create a new document
clawlink_call_tool --tool "googledocs_create_document" --params '{"title": "New Document"}'
```

## Authentication

All Google Docs tool calls are authenticated automatically by ClawLink using the user's connected Google account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Google Docs API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=google-docs and connect Google Docs.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `google-docs` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration google-docs
```

**Response:** Returns the live tool catalog for Google Docs.

### Reconnect

If Google Docs tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=google-docs
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration google-docs`

## Security & Permissions

- Access is scoped to documents within the connected Google account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete content range, delete table row/column) are marked as high-impact and must be confirmed.
- Document sharing permissions can be inspected to understand access levels before making changes.

## Tool Reference

### Document Discovery & Reading

| Tool | Description | Mode |
|------|-------------|------|
| `googledocs_search_documents` | Search for Google Docs by name, content, or date range | Read |
| `googledocs_get_document_by_id` | Retrieve a document's full metadata | Read |
| `googledocs_get_document_plaintext` | Get a best-effort plain-text rendering of a document | Read |
| `googledocs_export_document_as_pdf` | Export a document as PDF (10MB limit) | Read |
| `googledocs_list_spreadsheet_charts` | List charts from a linked Google Sheets spreadsheet | Read |

### Document Creation

| Tool | Description | Mode |
|------|-------------|------|
| `googledocs_create_document` | Create a new empty document with a title | Write |
| `googledocs_create_document_markdown` | Create a document initialized with Markdown content | Write |

### Content Insertion & Updates

| Tool | Description | Mode |
|------|-------------|------|
| `googledocs_insert_text_action` | Insert text at a specific index or append to end | Write |
| `googledocs_replace_all_text` | Replace all occurrences of a string throughout a document | Write |
| `googledocs_update_document_markdown` | Replace entire document content with Markdown | Write |
| `googledocs_update_document_section_markdown` | Insert or replace a section of a document with Markdown | Write |
| `googledocs_update_existing_document` | Apply programmatic edits via batchUpdate API | Write |
| `googledocs_update_document_style` | Update page size, margins, and default text direction | Write |

### Structural Elements

| Tool | Description | Mode |
|------|-------------|------|
| `googledocs_insert_table_action` | Insert a table at a specific location | Write |
| `googledocs_insert_table_column` | Insert a new column into an existing table | Write |
| `googledocs_insert_page_break` | Insert a page break into a document | Write |
| `googledocs_insert_inline_image` | Insert an image from a URI at a specific location | Write |
| `googledocs_create_paragraph_bullets` | Add bullet formatting to paragraphs in a range | Write |
| `googledocs_delete_paragraph_bullets` | Remove bullet formatting from paragraphs | Write |

### Header, Footer & Named Ranges

| Tool | Description | Mode |
|------|-------------|------|
| `googledocs_create_header` | Create a new header with optional text | Write |
| `googledocs_create_footer` | Create a new footer with optional text | Write |
| `googledocs_create_footnote` | Add a footnote at a location or end of document | Write |
| `googledocs_create_named_range` | Assign a name to a specific part of a document | Write |
| `googledocs_delete_header` | Delete a header from a document | Write |
| `googledocs_delete_footer` | Delete a footer from a document | Write |

### Table Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googledocs_delete_table_row` | Delete a row from a table | Write |
| `googledocs_delete_table_column` | Delete a column from a table | Write |
| `googledocs_unmerge_table_cells` | Unmerge previously merged cells in a table | Write |
| `googledocs_update_table_row_style` | Update row style (height, header marking) | Write |

### Copying & Duplication

| Tool | Description | Mode |
|------|-------------|------|
| `googledocs_copy_document` | Create a copy of an existing document | Write |

### Deletion

| Tool | Description | Mode |
|------|-------------|------|
| `googledocs_delete_content_range` | Delete a range of content from a document | Write |
| `googledocs_delete_named_range` | Delete a named range from a document | Write |

### Image Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googledocs_replace_image` | Replace an existing image with a new one from a URI | Write |

## Code Examples

### Search for documents

```bash
clawlink_call_tool --tool "googledocs_search_documents" \
  --params '{
    "query": "meeting notes",
    "page_size": 10
  }'
```

### Read document plaintext

```bash
clawlink_call_tool --tool "googledocs_get_document_plaintext" \
  --params '{
    "document_id": "YOUR_DOCUMENT_ID"
  }'
```

### Create a document from Markdown

```bash
clawlink_call_tool --tool "googledocs_create_document_markdown" \
  --params '{
    "title": "Project Brief",
    "markdown": "# Project Brief\n\n## Overview\n\nThis is the project overview section.\n\n## Next Steps\n\n1. Define requirements\n2. Create mockups\n3. Implement feature"
  }'
```

### Insert text at a location

```bash
clawlink_call_tool --tool "googledocs_insert_text_action" \
  --params '{
    "document_id": "YOUR_DOCUMENT_ID",
    "text": "New paragraph content here.",
    "insertion_index": 150
  }'
```

### Replace all text occurrences

```bash
clawlink_call_tool --tool "googledocs_replace_all_text" \
  --params '{
    "document_id": "YOUR_DOCUMENT_ID",
    "replace_text": "New Company Name",
    "search_text": "Old Company Name"
  }'
```

### Copy a document

```bash
clawlink_call_tool --tool "googledocs_copy_document" \
  --params '{
    "document_id": "YOUR_DOCUMENT_ID"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Docs is connected.
2. Call `clawlink_list_tools --integration google-docs` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `google-docs`.
5. If no Google Docs tools appear, direct the user to https://claw-link.dev/dashboard?add=google-docs.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  search → get → export → call                               │
│                                                             │
│  Example: Search docs → Get plaintext → Show results        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer search, read, export, and inspection operations before writes.
4. For document creation, content replacement, Markdown imports, structural edits, or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Document IDs are stable Google Drive file IDs — capture them from search or get responses for subsequent operations.
- `googledocs_insert_text_action`: Use `append_to_end=true` to safely append without index concerns. When using `insertion_index`, it must fall within an existing paragraph's bounds.
- Table operations require knowing the table index within the document structure.
- Every document segment (body, header, footer, footnote) ends with a final newline that cannot be deleted.
- PDF export has a 10MB content limit enforced by Google Drive API.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration google-docs`. |
| Missing connection | Google Docs is not connected. Direct the user to https://claw-link.dev/dashboard?add=google-docs. |
| `RESOURCE_NOT_FOUND` | Document does not exist. Check the document_id. |
| `INVALID_ARGUMENT` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| `FORBIDDEN` | No read or write access to the document. Check sharing permissions. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `google-docs`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Google Docs API Overview](https://developers.google.com/docs/api)
- [Documents Resource](https://developers.google.com/docs/api/reference/rest/v1/documents)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-docs-documents
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Google Drive](https://clawhub.ai/hith3sh/google-drive-files) — For file management, permissions, and Drive-level operations
- [Google Sheets](https://clawhub.ai/hith3sh/google-sheets-spreadsheets) — For spreadsheet operations in Google Workspace

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-docs-documents)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)