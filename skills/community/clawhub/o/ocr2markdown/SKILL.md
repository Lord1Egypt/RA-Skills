---
name: ocr2markdown
description: "Document OCR and parsing — converts PDF/images to Markdown on remote L4 GPU via Modal. Trigger when user says: OCR, PDF to markdown, parse PDF, extract text from PDF, 文档识别, PDF转Markdown, 扫描件识别. Takes local PDF/image files and returns Markdown with layout, tables, formulas, and OCR preserved."
version: v1.0.1
---

# OCR2Markdown

MinerU document parsing pipeline on Modal L4 GPU — PDF/image → Markdown with layout, tables, formulas, and OCR preserved.

**Pipeline code is bundled** at `./src/ocr2markdown.py`. After `npx skills add`, runs from any directory.

## Workflow

### 1. Prepare slug and identify files

**Slug** = task identifier (volume directory name). Use user-provided value, or generate `ocr_YYYYMMDD_HHMMSS` if none given.

**Directory input?** Scan for PDF (`.pdf`), list with index, ask user to confirm selection.

**Specific files?** Use directly, no listing needed.

### 2. Upload to volume

Ensure both volumes exist (idempotent):
```bash
modal volume create speech2srt-data 2>/dev/null || true
modal volume create speech2srt-models 2>/dev/null || true
```

Upload each file:
```bash
modal volume put speech2srt-data <local_file> <slug>/upload/
```

Modal `put` auto-creates remote directories.

### 3. Run pipeline

```bash
modal run ./src/ocr2markdown.py --slug <slug>
```

Pipeline finds all `.pdf` files in `<slug>/upload/` on the volume and processes them one by one.

**Ctrl+C?** Stop cleanly, report progress. Re-run with same slug — already-processed PDFs are skipped automatically.

### 4. Download results

Output directory structure:
```
<slug>/output/<stem>_ocr/
├── <stem>.md              # Main markdown output
├── images/                # Extracted images referenced by markdown
└── *.pdf, *.json          # Auxiliary outputs (layout, model data)
```

Download the entire output folder:
```bash
modal volume get speech2srt-data <slug>/output/ <local_destination>/
```

Preserve original directory tree.

### 5. Report

```
Done. Parsed N PDF(s) in Xs

Results:
  - <output_dir>/<stem>_ocr/<stem>.md
  - <output_dir>/<stem>_ocr/images/
```

## Setup

Before first run, verify:

1. **Python 3.9+** — `python -V`
2. **Modal CLI** — `modal config show`:
   - `token_id` null → `modal setup` to authenticate
   - command not found → `pip install modal` then `modal setup`
3. **Modal free tier** — L4 GPU is $0.80/hr. New accounts get **$30 free credits/month** (~37 hours of L4). No setup needed beyond authentication.

## Performance

| PDF Size | Pages | Time/PDF |
|----------|-------|----------|
| ~40-55 MB | varies | ~110-130s each |

Pipeline auto-skips PDFs with existing output.
