---
name: pdfgate-html-to-pdf
description: HTML to PDF conversion with the PDFGate PDF API. Generate PDF invoices, reports, receipts and fillable PDF forms from HTML or a web page URL using a dependency-free Node.js script with page size, margin and orientation options.
version: 1.0.0
homepage: https://pdfgate.com/api/html-to-pdf
metadata:
  openclaw:
    emoji: "📄"
    homepage: https://pdfgate.com/api/html-to-pdf
    primaryEnv: PDFGATE_API_KEY
    requires:
      env:
        - PDFGATE_API_KEY
      bins:
        - node
    envVars:
      - name: PDFGATE_API_KEY
        required: true
        description: PDFGate API key. test_ keys use the sandbox, live_ keys use production.
---

# PDFGate HTML to PDF

Convert an HTML document or a publicly accessible web page URL into a PDF with the [PDFGate HTML to PDF API](https://pdfgate.com/api/html-to-pdf). The skill ships a standalone Node.js script with no third-party dependencies.

## When to use

Use this skill when the user wants to:

- Generate a PDF from HTML: an invoice, a report, a receipt, a letter, a certificate.
- Convert a public web page URL to PDF.
- Control the PDF layout: A4 or Letter page size, portrait or landscape, margins, scale, print or screen CSS, header and footer templates, page ranges.
- Create a **fillable** PDF form from HTML inputs (text, number, date, textarea, select, checkbox, radio).

This skill **does not** send documents for electronic signature, fill or flatten existing PDF forms, or edit PDFs that already exist. Those are other PDFGate endpoints.

## Requirements and privacy

- A PDFGate account and API key from [dashboard.pdfgate.com](https://dashboard.pdfgate.com). Keys that start with `test_` use the sandbox at `api-sandbox.pdfgate.com`; keys that start with `live_` use production at `api.pdfgate.com`. The script picks the host from the key prefix.
- The `PDFGATE_API_KEY` environment variable must be visible to the **process that runs the script**. In OpenClaw, set it through the skill's `apiKey` or `env` entry in `openclaw.json` or in the host environment. In sandboxed agent mode, host secrets are not injected into the sandbox, so set the variable inside the sandbox as well.
- Node.js 18 or later. No `npm install`.
- The HTML or the URL is sent to PDFGate's servers for rendering. **Before submitting sensitive, confidential or third-party content, make sure the user authorizes that upload.** Do not describe the PDF as generated locally.
- For URL conversion, render only pages the user intends to submit. The script refuses localhost, internal hostnames and raw IP addresses. Do not attempt to bypass access controls.
- Never print, log, embed in files, or ask the user to paste the API key in chat. The script never prints it.
- Requests count against the account's plan. Sandbox renders are free and watermarked; use a `test_` key to experiment.

## Workflow

1. Confirm the source (HTML in chat, a local HTML file, or a public URL) and the output filename. If the user provides HTML in chat, save it as a UTF-8 `.html` file first.
2. Pick an output path in the agent workspace or a location the user names. The script refuses to overwrite an existing file unless `--overwrite` is passed; ask before using it.
3. Run `{baseDir}/scripts/generate-pdf.mjs` with **separate shell arguments**. Never interpolate HTML, user-supplied URLs or paths into a shell command string; if a shell is unavoidable, quote every argument.
4. On success the script prints one JSON line with `success`, `path`, `bytes` and `environment`. Report the saved path and hand the file to the user where the host supports it.
5. On failure the script exits with code 1 and prints `PDFGate skill error: ...` on stderr. Relay that message, never claim the PDF was generated, and do not retry blindly on HTTP 401 or 429.

## Examples

Generate from a local HTML file:

```bash
node {baseDir}/scripts/generate-pdf.mjs \
  --html-file ./invoice.html \
  --output ./invoice.pdf \
  --page-size a4 \
  --margin 15mm
```

Convert a public URL using the page's screen CSS, landscape Letter:

```bash
node {baseDir}/scripts/generate-pdf.mjs \
  --url https://example.com/report \
  --output ./report.pdf \
  --page-size letter \
  --orientation landscape \
  --media screen
```

Make a PDF with fillable form fields (see `{baseDir}/examples/form.html`):

```bash
node {baseDir}/scripts/generate-pdf.mjs \
  --html-file {baseDir}/examples/form.html \
  --output ./form.pdf \
  --fillable
```

Wait for dynamic content before rendering a JavaScript-heavy page:

```bash
node {baseDir}/scripts/generate-pdf.mjs \
  --url https://example.com/dashboard \
  --output ./dashboard.pdf \
  --wait-for-selector '#report-ready' \
  --wait-for-network-idle \
  --timeout-seconds 300
```

Add a header and footer (templates are HTML files; `--margin` makes room for them):

```bash
node {baseDir}/scripts/generate-pdf.mjs \
  --html-file ./report.html \
  --output ./report.pdf \
  --margin 20mm \
  --header-file ./header.html \
  --footer-file ./footer.html
```

List every option:

```bash
node {baseDir}/scripts/generate-pdf.mjs --help
```

## Option reference

| Option | Meaning |
|---|---|
| `--html-file PATH` | HTML file to convert. `-` reads standard input. Max 10 MiB. |
| `--url URL` | Public http(s) page to convert. Mutually exclusive with `--html-file`. |
| `--output PATH` | Destination `.pdf` path. Parent folders are created. |
| `--page-size` | `a0`..`a6`, `letter`, `legal`, `tabloid`, `ledger`. Default `a4` (the API's own default is `ledger`). |
| `--orientation` | `portrait` (default) or `landscape`. |
| `--margin` | One CSS length for all four sides, e.g. `12mm`, `0.5in`, `20px`. |
| `--scale` | Render scale `0.1`..`2`. |
| `--no-background` | Skip CSS backgrounds. |
| `--media` | `screen` or `print`. PDFGate defaults to `screen` for URLs and `print` for HTML. |
| `--header-file`, `--footer-file` | HTML templates for page header and footer. Require `--margin`. |
| `--page-ranges` | e.g. `1-3,5`. |
| `--fillable` | Turn HTML inputs into interactive PDF form fields. |
| `--wait-for-selector CSS` | Wait for an element before rendering (the API gives it up to 30 s). |
| `--wait-for-network-idle` | Wait until the page has no open network connections. |
| `--delay-ms N` | Extra wait before rendering, up to 20000 ms. |
| `--timeout-seconds N` | Whole request timeout, 15..960. Default 120. Sent to the API as its page-load timeout too (API max 15 min). |
| `--overwrite` | Replace an existing output file. |

## Implementation notes

- The script calls `POST https://api.pdfgate.com/v1/generate/pdf` (or the sandbox host) with the API key in the `X-API-KEY` header and streams the binary PDF response to disk. It does not use `jsonResponse`, so nothing depends on PDFGate file storage settings.
- The PDF is written to a temporary file first, checked for the `%PDF-` signature, then moved into place.
- JavaScript on the page runs in PDFGate's headless Chrome. Use `--wait-for-selector`, `--wait-for-network-idle` or `--delay-ms` when content loads asynchronously.
- The fillable form feature creates real AcroForm fields from HTML inputs. It is not an e-signature workflow.

## Links

- [PDFGate HTML to PDF API](https://pdfgate.com/api/html-to-pdf)
- [Generate PDF endpoint reference](https://pdfgate.com/documentation/generate-pdf)
- [Fillable fields from HTML guide](https://pdfgate.com/guides/html-to-pdf/add-fillable-fields)
- [Authentication and API keys](https://pdfgate.com/documentation/authentication)
- [Dashboard](https://dashboard.pdfgate.com)
