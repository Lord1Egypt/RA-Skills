---
name: oo-ilovepdf
description: "iLovePDF (ilovepdf.com). Use this skill for ANY iLovePDF request — searching and reading data. Whenever a task involves iLovePDF, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "iLovePDF"
  author: "OOMOL"
  version: "1.0.1"
  services: ["ilovepdf"]
  icon: "https://static.oomol.com/logo/third-party/ilovepdf.svg"
---

# iLovePDF

Operate **iLovePDF** through your OOMOL-connected account. This skill calls the `ilovepdf` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected iLovePDF. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ilovepdf" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ilovepdf" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_page_numbers` — Add page numbers to PDFs with page selection, placement, and font options, returning the numbered PDF or ZIP.
- `compress_pdf` — Compress PDF files from public URLs and return the processed PDF or ZIP.
- `convert_to_pdfa` — Convert PDFs to the requested PDF/A conformance level for archiving and return the PDF or ZIP.
- `extract_text` — Extract text from PDFs and return text files or a ZIP, optionally including page, position, and font details.
- `image_to_pdf` — Convert images from public URLs to PDF with page layout and merge options, returning the resulting PDF or ZIP.
- `merge_pdf` — Merge PDF files from public URLs in the supplied order and return a downloadable PDF.
- `ocr_pdf` — Recognize text in scanned PDFs using the selected OCR languages and return searchable PDFs or a ZIP.
- `office_to_pdf` — Convert Office documents from public URLs to PDF and return the resulting PDF or ZIP.
- `pdf_to_image` — Convert PDF pages to JPG images or extract embedded images, returning the resulting image or ZIP.
- `protect_pdf` — Encrypt PDF files with an output password and return the protected PDF or ZIP.
- `repair_pdf` — Attempt to recover damaged PDF files and return the repaired PDF or ZIP.
- `rotate_pdf` — Rotate each PDF by its per-file rotate value and return the processed PDF or ZIP.
- `split_pdf` — Split PDFs by page ranges, fixed page counts, or file size, or remove selected pages, and return the resulting file or ZIP.
- `unlock_pdf` — Remove password protection from PDFs and return the unlocked PDF or ZIP. Supply each source file's opening password when needed.
- `validate_pdfa` — Validate PDFs against the requested PDF/A conformance level and return per-file validation results without downloading a file.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change iLovePDF state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — iLovePDF is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/ilovepdf
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- iLovePDF homepage: https://www.ilovepdf.com/
- API documentation: https://www.iloveapi.com/docs/api-reference
