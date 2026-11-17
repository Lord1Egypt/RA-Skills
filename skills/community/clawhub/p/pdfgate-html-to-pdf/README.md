# PDFGate HTML to PDF skill for ClawHub

An OpenClaw / ClawHub skill that converts HTML files or public web page URLs into PDFs through the [PDFGate HTML to PDF API](https://pdfgate.com/api/html-to-pdf).

- **No npm packages:** a single Node.js 18+ script that calls the REST API with `fetch`.
- **Automatic environment selection:** `test_` API keys use the PDFGate sandbox, `live_` keys use production.
- **Features:** HTML to PDF, URL to PDF, page size, orientation, margins, scale, print or screen CSS, header and footer templates, page ranges, waits for dynamic content, and fillable PDF form fields.
- **Output:** writes a real PDF file locally, verifies the PDF header, and prints a one-line JSON result.

## Layout

```
pdfgate-html-to-pdf/
├── SKILL.md                  instructions and metadata read by OpenClaw
├── README.md
├── scripts/generate-pdf.mjs  the helper script
└── examples/
    ├── sample.html           a styled report
    └── form.html             a form for --fillable
```

## Installation

Get a PDFGate API key from [dashboard.pdfgate.com](https://dashboard.pdfgate.com) and make it available as `PDFGATE_API_KEY`, either in the environment of the process that runs the script or through the skill's `apiKey` entry in `openclaw.json`. Never commit or publish API keys.

Install from ClawHub, using the slug shown on the skill's ClawHub page (scoped slugs look like `@handle/pdfgate-html-to-pdf`):

```bash
openclaw skills install pdfgate-html-to-pdf
```

Or run the helper directly:

```bash
node scripts/generate-pdf.mjs --html-file examples/sample.html --output ./sample.pdf --page-size a4
```

From a website:

```bash
node scripts/generate-pdf.mjs --url https://example.com --output ./example.pdf --page-size a4
```

Run `node scripts/generate-pdf.mjs --help` for all flags. Sandbox (`test_`) renders are free and watermarked. HTML and URLs are sent to PDFGate's servers for rendering.

## Publish on ClawHub

From the directory that contains `pdfgate-html-to-pdf/`:

```bash
npm install -g clawhub
clawhub login
clawhub skill publish ./pdfgate-html-to-pdf --slug pdfgate-html-to-pdf --name "PDFGate HTML to PDF" --changelog "Initial release: generate PDFs from HTML and URLs"
```

Add `--dry-run` to preview without uploading. Later publishes of changed content bump the patch version automatically.

Format reference: [ClawHub quickstart](https://docs.openclaw.ai/clawhub/quickstart) and [skill format](https://docs.openclaw.ai/clawhub/skill-format).

## Security notes

- Never put a PDFGate API key in the skill folder or examples. The script reads it from the environment only and never prints it.
- Ask the user before sending sensitive HTML to PDFGate.
- The script refuses localhost, internal hostnames and IP addresses as URLs, and refuses to overwrite files unless `--overwrite` is passed.
- Only run the helper when the user asks for a PDF. Production requests count against the account's plan.
- This skill does not sign, encrypt or edit existing PDFs.

Published ClawHub skills are licensed MIT-0 under ClawHub policy.
