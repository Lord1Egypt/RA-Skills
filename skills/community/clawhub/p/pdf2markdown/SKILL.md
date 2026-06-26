---
name: pdf2markdown
description: |
  Convert PDF and image documents to clean Markdown via the PDF2Markdown CLI. Use when the user wants to extract text from PDFs, convert PDFs to markdown, parse document structure, or process images (JPEG, PNG, GIF, WebP, TIFF, BMP) into structured content. Also use when they say "convert this PDF", "parse this document", "extract text from PDF", "parse async", or "large file" (up to 100MB). Must be pre-installed and authenticated.
allowed-tools:
  - Bash(pdf2markdown *)
  - Bash(pdf2md *)
  - Bash(npx pdf2markdown *)
  - Bash(npx pdf2md *)
---

# PDF2Markdown CLI

Convert PDF and image documents to Markdown. Supports both `pdf2markdown` and `pdf2md` commands.

Run `pdf2markdown --help` or `pdf2md <command> --help` for options.

## Prerequisites

Install and authenticate. Check with `pdf2markdown --status`.

```bash
pdf2markdown login
# or set PDF2MARKDOWN_API_KEY
```

If not ready, see [rules/install.md](rules/install.md). For output handling, see [rules/security.md](rules/security.md).

## Workflow

| Need                | Command        | When                                                    |
| ------------------- | -------------- | ------------------------------------------------------- |
| Convert PDF/image   | `parse`        | File under ~30MB, have path or URL                       |
| Large file (async)  | `parse-async`  | File over ~30MB, or sync returns file_too_large error   |

## Quick start

**Parse (sync, ~30MB):**
```bash
pdf2markdown document.pdf -o .pdf2markdown/output.md
pdf2markdown parse --url "https://example.com/doc.pdf" -o .pdf2markdown/doc.md
pdf2markdown parse file1.pdf file2.png -o .pdf2markdown/

# JSON output
pdf2markdown parse document.pdf --format json -o .pdf2markdown/result.json
```

**Parse-async (large files, up to 100MB):**
```bash
# Submit and wait
pdf2markdown parse-async large.pdf --wait -o .pdf2markdown/output.md
pdf2markdown parse-async --url "https://cdn.example.com/big.pdf" --wait -o .pdf2markdown/doc.md

# Submit only (poll later)
pdf2markdown parse-async large.pdf  # returns task_id
pdf2markdown parse-async <task_id> --status
pdf2markdown parse-async <task_id> --result -o .pdf2markdown/output.md
```

## Options

| Command       | Key options                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| `parse`       | `-u, --url`, `-o, --output`, `-f, --format` (markdown, json, all), `--page-images`, `--json`, `--pretty` |
| `parse-async` | `-u, --url`, `-o, --output`, `--wait`, `--status`, `--result`, `--poll-interval`, `--timeout` |

Run `pdf2markdown <command> --help` for full details.

## Output & Organization

Write results to `.pdf2markdown/` with `-o`. Add `.pdf2markdown/` to `.gitignore`.

```bash
pdf2markdown document.pdf -o .pdf2markdown/doc.md
pdf2markdown parse file1.pdf file2.pdf -o .pdf2markdown/
```

Naming: `.pdf2markdown/{name}.md`. For large outputs, use `grep`, `head`, or incremental reads. Always quote URLs — shell interprets `?` and `&` as special characters.

## Documentation

- [PDF2Markdown API Docs](https://pdf2markdown.io/docs)
