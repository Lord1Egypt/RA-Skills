---
name: pdf-report
version: 1.0.1
description: Generate clean A4 PDF reports from structured JSON using Jinja2 and WeasyPrint. Use when the user needs a formatted PDF document — analytical summary, data report, or chart-based export — from workspace data.
metadata: { "openclaw": { "emoji": "PDF", "requires": { "bins": ["python3"] } } }
---

# PDF Report

Generate a clean A4 PDF from structured JSON data.

## Setup

Install system dependencies (WeasyPrint requires these):

```bash
# Ubuntu/Debian
sudo apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev libcairo2
```

Create a virtual environment and install Python dependencies (one-time):

```bash
python3 -m venv ~/.openclaw/workspace/.venv_pdf
~/.openclaw/workspace/.venv_pdf/bin/pip install weasyprint jinja2
```

## Quick start

```bash
~/.openclaw/workspace/.venv_pdf/bin/python skills/pdf-report/scripts/render_pdf.py \
  --input exports/report-data.json \
  --output exports/pdfs/report.pdf
```

## Inputs

- `--input` path to a JSON file inside the workspace
- `--output` path to the PDF output inside the workspace
- Optional: `--template-file` custom Jinja2 template path inside the workspace
- Optional: `--html-out` write the rendered HTML for debugging

## Expected JSON shape

```json
{
  "title": "Monthly Report",
  "subtitle": "Summary by region",
  "generated_at": "2026-03-23 10:00",
  "summary": ["Key point 1", "Key point 2"],
  "sections": [
    {
      "title": "Sales by category",
      "lead": "National overview",
      "items": ["Observation 1", "Observation 2"],
      "table": {
        "headers": ["Category", "Amount", "Share"],
        "rows": [["Electronics", "12 450", "45%"]]
      },
      "charts": [
        {
          "title": "Distribution by category",
          "src": "exports/charts/category.png",
          "caption": "Source: sales database"
        }
      ],
      "note": "Data as of 31/12/2025"
    }
  ],
  "footer": "Company Name — Department"
}
```

## Notes

- All file paths (CLI arguments and `charts[].src` in JSON) must stay inside the workspace. Paths outside the workspace are rejected.
- Missing chart images produce a warning to stderr but do not block PDF generation.
- Use `chart-mpl` first when a section needs chart images, then reference those image paths in `charts[].src`.
- Output directories are created automatically.
- Default template: `skills/pdf-report/templates/report.html`
- Dedicated venv: `~/.openclaw/workspace/.venv_pdf/` (weasyprint + jinja2)
- Pages are numbered automatically (bottom-right: "1 / 3").

## Custom templates

Use `--template-file` to provide your own Jinja2 HTML template. Note that relative asset paths inside custom templates (images, CSS) resolve from the **workspace root**, not the template's directory. Use workspace-root-relative paths for any referenced assets.
