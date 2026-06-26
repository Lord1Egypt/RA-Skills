# PDF Export Scripts

This directory only contains the PDF export helper used by `admissions-cv-writing`.

## Files

- `export-pdf/run.py`: single entry point. Creates the venv on first run, then delegates to `export_pdf.py`.
- `export-pdf/export_pdf.py`: reads Markdown, assembles CSS/HTML, and exports PDF.
- `export-pdf/css/offerclaw.css`: main CV stylesheet for typography, headings, body text, and bullet layout.
- `export-pdf/requirements.txt`: Python dependencies for export.

## Setup and Usage

- Python dependencies: `weasyprint`, `markdown`.
- From the `admissions-cv-writing/` skill directory:
  ```bash
  python3 scripts/export-pdf/run.py <input.md> <output.pdf>
  ```
  The venv is created automatically on first run. No manual setup needed.
- Font loading defaults to `--font-source auto`: use packaged fonts when available, otherwise fall back to similar local fonts.
- Optional font-source modes:
  - `--font-source auto`: prefer packaged fonts, then local fonts.
  - `--font-source local-only`: never read packaged font files; useful on platforms that forbid shipping fonts.
  - `--font-source bundled-only`: require packaged font files and fail fast if they are missing.
- Optional watermark mode:
  - `--watermark on`: include the OfferClaw footer watermark.
  - `--watermark off`: omit the footer watermark.
