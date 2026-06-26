---
name: oo-fuxin
description: "Foxit Cloud API (cloudapi.fuxinsoft.cn). Use this skill for ANY Foxit Cloud API request — reading, creating, updating, and deleting data. Whenever a task involves Foxit Cloud API, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Foxit Cloud API"
  author: "OOMOL"
  version: "1.0.1"
  services: ["fuxin"]
  icon: "https://static.oomol.com/logo/third-party/fuxin.svg"
---

# Foxit Cloud API

Operate **Foxit Cloud API** through your OOMOL-connected account. This skill calls the `fuxin` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Foxit Cloud API. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "fuxin" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "fuxin" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `check_pages_are_scanned` — Submit one PDF for scanned-page detection in Foxit.
- `compare_documents` — Compare two PDF documents with Foxit and submit a diff task.
- `compress_document` — Compress one PDF with a chosen Foxit compression level.
- `convert_document` — Convert one PDF into Word, Excel, PowerPoint, image, or text with Foxit.
- `convert_office_document_to_images` — Convert one Office document into a ZIP of page images with Foxit.
- `create_pdf_from_document` — Create a PDF from a Word, Excel, PowerPoint, image, or text source in Foxit. [write]
- `create_pdf_from_html` — Create a PDF from HTML content, an HTML file, or a webpage URL in Foxit. [write]
- `download_file` — Download one Foxit result document and upload it to connector transit storage.
- `extract_document` — Extract text or embedded images from one PDF with Foxit.
- `flatten_document` — Flatten annotations and form fields into the page content of one PDF with Foxit.
- `get_pages_basic_info` — Submit one PDF for page-size and rotation analysis in Foxit.
- `get_task` — Fetch one Foxit task status and return the normalized task progress details.
- `get_user_stock` — Fetch the remaining Foxit Services API and Embed API quota for the connected credential.
- `linearize_document` — Linearize one PDF to improve incremental web viewing in Foxit.
- `manipulate_document_pages` — Delete, rotate, or move PDF pages with Foxit.
- `merge_documents` — Merge multiple PDF documents into a single PDF with Foxit. [write]
- `ocr_document` — Run OCR on one PDF or image document with Foxit.
- `protect_document` — Protect one PDF with passwords and permissions in Foxit.
- `remove_password_from_document` — Remove the password from one protected PDF with Foxit. [destructive]
- `split_document` — Split one PDF into multiple smaller files with Foxit.
- `upload_file` — Upload one source file to Foxit Cloud API and return the reusable Foxit document ID. [write]
- `watermark_document` — Add a text or image watermark to one PDF with Foxit.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Foxit Cloud API state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Foxit Cloud API is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/app-connections?provider=fuxin
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Foxit Cloud API homepage: https://cloudapi.fuxinsoft.cn
