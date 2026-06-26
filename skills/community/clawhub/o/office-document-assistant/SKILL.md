---
name: office-document-assistant
description: Read, extract, summarize, and compare office documents including PDF, Word, Excel, and PowerPoint. Use when a user provides .pdf/.doc/.docx/.xls/.xlsx/.ppt/.pptx files and asks for summaries, key point extraction, page-by-page outlines, field extraction, table explanation, or multi-document comparison. Prefer the bundled extraction script for deterministic text extraction; for PDFs, fall back to OCR when embedded text is missing.
---

# Office Document Assistant

Read, extract, summarize, and compare common office documents:
- PDF
- Word (`.docx`, `.doc`)
- Excel (`.xlsx`, `.xls`)
- PowerPoint (`.pptx`, `.ppt`)

Use this skill when the user wants the contents of a document explained, summarized, searched, or extracted into a simpler structure.

## When to Use

Use this skill when the user:
- uploads a `.pdf` / `.doc` / `.docx` / `.xls` / `.xlsx` / `.ppt` / `.pptx`
- asks to summarize a document
- asks to extract dates, amounts, contacts, conclusions, specifications, risks, or action items
- asks for page-by-page / slide-by-slide structure
- asks what a spreadsheet or slide deck is saying
- asks to compare two or more documents after extracting their text

## When Not to Use

Do **not** position this skill as a high-fidelity layout or visual analysis system.

It is **not** ideal for:
- precise preservation of original layout, formatting, or pagination
- detailed chart / diagram / image interpretation
- password-protected or encrypted files
- OCR-heavy image understanding beyond basic text recovery
- advanced spreadsheet analytics or formula auditing
- tracked-changes / redline reconstruction in Office documents

## Core Workflow

1. Confirm the document path.
2. Run the bundled script:
   - `python3 {skill_dir}/scripts/extract_office_text.py <file> --json`
3. Inspect the JSON fields:
   - `type`
   - `extraction`
   - `warning`
   - `truncated`
   - `text`
4. Separate clearly in your response:
   - **directly extracted content**
   - **your summary / inference based on that content**
5. If extraction is empty or weak:
   - for PDF, check OCR availability first
   - for legacy Office formats, check conversion tools
6. If the user asks for a summary, default to:
   - one-sentence overview
   - 3–8 key points
   - extra sections only when clearly present (dates, people, risks, data, conclusions, contacts)
7. If the user asks for extraction, prefer structured fields over long prose.

## Supported Formats and Strategy

### PDF
- First extract embedded text with `pypdf`.
- If extracted text is too short, fall back to OCR.
- OCR prefers `chi_sim+eng`, then `chi_sim`, then `eng`.
- OCR pipeline requires both `pdftoppm` and `tesseract`.
- If an official first-class PDF tool is exposed in the environment and the task is high-value or multi-PDF, you may prefer that tool; otherwise use this skill's script.

### Word
- `.docx`: extract paragraphs and tables directly.
- `.doc`: try `antiword`, then `catdoc`, then LibreOffice conversion to `.docx`.

### Excel
- Extract sheet names and the first rows of each sheet.
- Best for quickly understanding workbook structure and core fields.
- When explaining, focus on what each sheet represents, key columns, important figures, and obvious anomalies.

### PowerPoint
- Extract slide text from shapes.
- Extract speaker notes when present.
- Summaries should usually be slide-by-slide or theme-based, not a giant raw dump.

## Tools and Dependencies

Document clearly what is required versus optional.

### Required runtime
- `python3`

### Required Python packages
- `pypdf` — embedded text extraction from PDFs
- `python-docx` — `.docx` extraction
- `openpyxl` — `.xlsx` extraction
- `python-pptx` — `.pptx` extraction

### Optional but strongly recommended system tools
- `poppler-utils` — provides `pdftoppm` for PDF → image conversion before OCR
- `tesseract-ocr` — OCR engine
- `tesseract-ocr-chi-sim` — Simplified Chinese OCR language pack
- `libreoffice` — conversion fallback for legacy `.doc`, `.xls`, `.ppt`
- `antiword` — direct `.doc` extraction fallback
- `catdoc` — additional `.doc` extraction fallback

### What each tool is used for
- `pypdf`: try text-layer extraction from PDFs first
- `pdftoppm`: rasterize PDF pages when OCR is needed
- `tesseract`: recover text from scanned/image PDFs
- `python-docx`: read paragraphs and tables from `.docx`
- `openpyxl`: read sheets and rows from `.xlsx`
- `python-pptx`: read slide text and notes from `.pptx`
- `libreoffice`: convert older Office formats into newer parseable formats
- `antiword` / `catdoc`: lightweight extraction options for `.doc`

### Minimum useful setup
If only modern documents matter, the minimum practical setup is:
- `python3`
- Python packages: `pypdf`, `python-docx`, `openpyxl`, `python-pptx`

### Recommended full setup
For the most robust behavior across real-world files, install:
- `python3`
- Python packages: `pypdf`, `python-docx`, `openpyxl`, `python-pptx`
- system tools: `poppler-utils`, `tesseract-ocr`, `tesseract-ocr-chi-sim`, `libreoffice`, `antiword`, `catdoc`

### Dependency check
Use the bundled checker to quickly see what is missing in the current environment:

```bash
python3 {skill_dir}/scripts/check_deps.py
```

## Common Commands

```bash
python3 {skill_dir}/scripts/extract_office_text.py "/path/to/file.pdf" --json
python3 {skill_dir}/scripts/extract_office_text.py "/path/to/file.docx" --json
python3 {skill_dir}/scripts/extract_office_text.py "/path/to/file.xlsx" --json
python3 {skill_dir}/scripts/extract_office_text.py "/path/to/file.pptx" --json
```

Useful flags:

```bash
# limit PDF pages scanned/extracted
python3 {skill_dir}/scripts/extract_office_text.py "/path/to/file.pdf" --page-limit 10 --json

# limit rows per sheet when probing spreadsheets
python3 {skill_dir}/scripts/extract_office_text.py "/path/to/file.xlsx" --row-limit 30 --json

# cap output text size
python3 {skill_dir}/scripts/extract_office_text.py "/path/to/file.pdf" --max-chars 30000 --json
```

## Output Style

Default to a compact answer:
- **one-sentence summary**
- **3–8 key points**
- then expand only if the user asks for:
  - detailed summary
  - page-by-page / slide-by-slide notes
  - field extraction
  - document comparison

## Failure Handling

- If PDF text is empty, suspect scanned pages or missing OCR tools.
- If Chinese OCR is weak, check whether `tesseract-ocr-chi-sim` is installed.
- If `.doc` / `.xls` / `.ppt` extraction fails, check `libreoffice`, `antiword`, and `catdoc`.
- If tables look messy, explain that this is text-first extraction rather than full layout reconstruction.
- If a file is encrypted or unreadable, say so plainly and stop guessing.

## References

Read these only when needed:
- `references/capabilities.md` — capability boundaries and what each format can/can't do well
- `references/troubleshooting.md` — dependency checks and common failure modes
