---
name: oo-googledocs
description: "Google Docs (workspace.google.com). Use this skill for ANY Google Docs request — reading, creating, updating, and deleting data. Whenever a task involves Google Docs, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Google Docs"
  author: "OOMOL"
  version: "1.0.1"
  services: ["googledocs"]
  icon: "https://static.oomol.com/logo/third-party/Google%20Docs.svg"
---

# Google Docs

Operate **Google Docs** through your OOMOL-connected account. This skill calls the `googledocs` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Google Docs. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "googledocs" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "googledocs" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `copy_document` — Copy an existing Google Docs document through Google Drive. If `title` is omitted, Google assigns the default copied-document title. [write]
- `create_document` — Create a Google Docs document and optionally insert initial text at the beginning. Returns document metadata without the full body content. [write]
- `create_document2` — Create a blank Google Docs document. This legacy compatibility action is the no-initial-text variant of `create_document`. [write]
- `create_footer` — Create a footer in a Google Docs document, optionally targeting a specific section break location. [write]
- `create_footnote` — Create a footnote in a Google Docs document at a specific location or at the end of a segment. [write]
- `create_header` — Create a header in a Google Docs document and optionally insert initial text. You can also target a specific section break location. [write]
- `create_named_range` — Create a named range over a specific span in a Google Docs document so it can be referenced later by name or ID. [write]
- `create_paragraph_bullets` — Add bullets to paragraphs within a specified range in a Google Docs document. [write]
- `delete_content_range` — Delete a content range from a Google Docs document. The trailing newline at the end of each segment cannot be removed. [destructive]
- `delete_footer` — Delete a footer from a Google Docs document, including a section-specific footer when applicable. [destructive]
- `delete_header` — Delete a header from a Google Docs document, including a section-specific header when applicable. [destructive]
- `delete_named_range` — Delete a named range from a Google Docs document using a payload that identifies the range by ID or name. [destructive]
- `delete_paragraph_bullets` — Remove bullets from paragraphs within a specified range in a Google Docs document. [destructive]
- `delete_table_column` — Delete one or more table columns from a Google Docs document. [destructive]
- `delete_table_row` — Delete a table row from a Google Docs document. [destructive]
- `export_document_as_pdf` — Export a Google Docs file as a PDF through Google Drive. Google Drive limits export content to roughly 10 MB.
- `get_document_by_id` — Retrieve a Google Docs document by ID. Use `include_tabs_content` when you need tab content in the response.
- `get_document_plaintext` — Retrieve a Google Docs document and render it as best-effort plain text. This flattens paragraphs, lists, tables, and optional headers, footers, or footnotes.
- `insert_inline_image` — Insert an inline image from a URI at a specified location in a Google Docs document. [write]
- `insert_page_break` — Insert a page break at a specified location in a Google Docs document. [write]
- `insert_table_action` — Insert a table at a specific index or at the end of a segment in a Google Docs document. [write]
- `insert_table_column` — Insert one or more table columns at a specified location in a Google Docs document. [write]
- `insert_text_action` — Insert text at a specific index or append it to the end of a Google Docs document. When inserting by index, the position must be inside an existing paragraph. [write]
- `list_spreadsheet_charts` — List chart metadata from a Google Sheets spreadsheet so charts can be referenced or embedded elsewhere, including in Google Docs.
- `replace_all_text` — Replace all matching text in a Google Docs document. Supports case-sensitive and regex-based matching. [write]
- `replace_image` — Replace an existing image in a Google Docs document with a new image from a URI. [write]
- `search_documents` — Search Google Docs files with filters such as query text, dates, starred state, trash state, or shared-drive visibility.
- `unmerge_table_cells` — Unmerge previously merged table cells in a Google Docs document. [write]
- `update_document_batch` — Apply raw Docs `batchUpdate` requests to a Google Docs document. This is the lower-level compatibility action for direct request arrays. [write]
- `update_document_style` — Update global document style settings such as page size, margins, or text direction in a Google Docs document. [write]
- `update_existing_document` — Apply one or more programmatic edits to an existing Google Docs document through `batchUpdate`. Use this for structured insert, delete, or formatting changes. [write]
- `update_table_row_style` — Update the style of a table row in a Google Docs document, such as row height or header formatting. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Google Docs state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Google Docs is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=googledocs
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Google Docs homepage: https://workspace.google.com/products/docs/
