---
name: office-to-markdown
description: >
  Converts office automation documents — PDF, PPTX, DOCX, XLSX, CSV — into
  clean, readable Markdown. Use this skill when a user explicitly asks to
  convert, extract, or turn an uploaded document into Markdown (e.g. "convert
  this PDF to markdown", "extract the text from this Word doc", "turn this into
  markdown"). Do NOT trigger on a bare file upload alone — wait for a clear
  conversion request. Handles both text-based and image-based / scanned
  documents via Claude vision (requires user confirmation before sending images
  to the API).
---

# Office → Markdown Skill

Convert any uploaded office document to clean Markdown.
All conversion logic lives in `scripts/` — load only the script you need.

> **Security notes**
> - Dependencies are installed into an isolated temp directory (`/tmp/office_md_deps/`) and pinned to reviewed versions. The system Python environment is not modified.
> - For scanned or image-only content, pages are sent to Anthropic's vision API. **Always ask the user for confirmation before enabling vision** (see Workflow step 3).

---

## Script Reference

| Format | Extensions | Script |
|--------|-----------|--------|
| PDF (text + scanned/image) | `.pdf` | `scripts/pdf-to-md.py` |
| PowerPoint | `.pptx`, `.ppt` | `scripts/pptx-to-md.py` |
| Word | `.docx`, `.doc` | `scripts/docx-to-md.py` |
| Excel | `.xlsx`, `.xls` | `scripts/xlsx-to-md.py` |
| CSV | `.csv` | `scripts/csv-to-md.py` |

---

## Workflow

### 1. Confirm conversion intent

Only proceed if the user has explicitly asked to convert, extract, or export
the document to Markdown. A bare file upload without a conversion request is
**not** sufficient to trigger this skill.

### 2. Run the matching script (text-only pass first)

```bash
python scripts/<script-name>.py \
  /mnt/user-data/uploads/<input-file> \
  /mnt/user-data/outputs/<stem>.md
```

Each script installs its own pinned dependencies into `/tmp/office_md_deps/`
on first run (isolated from the system Python environment).

### 3. Vision consent — REQUIRED before image extraction

If the script output indicates image-only pages were detected (or the document
is known to be scanned), **stop and ask the user**:

> "This document has **N image-only page(s)** that cannot be extracted without
> sending them to Anthropic's vision API. Page images will be transmitted
> externally for OCR. Would you like to proceed with vision extraction?"

Only if the user confirms, re-run with the `--allow-vision` flag:

```bash
python scripts/<script-name>.py \
  /mnt/user-data/uploads/<input-file> \
  /mnt/user-data/outputs/<stem>.md \
  --allow-vision
```

If the user declines, save the text-only result and note which pages were skipped.

### 4. Present the file

Use `present_files` with the output `.md` path, then give a brief summary:
- File type and page/slide/sheet count
- Whether vision was used and for how many pages (or that it was skipped)

---

## How vision works (PDF / PPTX / DOCX)

Each script uses a **two-pass strategy**:

1. **Text pass** — extract text normally (fast, no API call, always runs)
2. **Vision pass** — only runs when `--allow-vision` is passed AND pages had no
   extractable text; those pages are rendered and sent to the Claude vision API

---

## Edge Cases

| Situation | Behaviour |
|-----------|-----------|
| Fully scanned PDF | All pages flagged for vision; user confirmation required |
| Mixed PDF (some text, some images) | Only image pages flagged; user confirmation required |
| User declines vision | Text-only `.md` is saved; skipped pages are noted inline |
| Password-protected file | Script exits with a clear error message |
| Very large PDF (50+ image pages) | Script adds 0.3s sleep between vision calls |
| Image too large (>4MB base64) | Reduce DPI: edit `dpi=150` → `dpi=100` in `pdf-to-md.py` |
| Encoding errors in CSV | Script auto-retries with `latin-1` |
