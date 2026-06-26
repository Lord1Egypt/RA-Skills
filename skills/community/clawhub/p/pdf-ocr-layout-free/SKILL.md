---
name: pdf-ocr-layout
description: >
  Full OCR pipeline for scanned PDFs with layout preservation. Use this skill whenever
  the user wants to OCR a PDF, convert a scanned document to searchable text, or preserve
  the original layout of a scanned book/document. Triggers on: "OCR this PDF", "用PaddleOCR处理",
  "识别这个PDF", "扫描版PDF转文字", "把这个PDF做OCR", or when a PDF path is provided alongside
  any mention of OCR, text recognition, or layout preservation.
---

# PDF OCR with Layout Preservation

Automated pipeline: **Split → OCR API → Layout PDF → Merge**

Each original page becomes one PDF page, with text placed at exact bounding-box positions
and font sizes calibrated to fill the original block dimensions.

## Quick Start

```bash
python ~/.claude/skills/pdf-ocr-layout/scripts/pipeline.py "/path/to/input.pdf"
```

Output: `input_ocr.pdf` in the same directory. Intermediate files in `input_ocr_work/`.

## Full Options

```bash
python ~/.claude/skills/pdf-ocr-layout/scripts/pipeline.py \
  "/path/to/input.pdf" \
  --output "/path/to/output.pdf" \
  --work-dir "/path/to/workdir" \
  --chunk-size 90
```

## Steps for Claude

1. **Ask for the PDF path** if not already provided in the conversation.
2. **Check dependencies** (install only what's missing):
   ```bash
   pip install pypdf reportlab Pillow requests -q
   ```
3. **Run the pipeline** and stream output to the user:
   ```bash
   python ~/.claude/skills/pdf-ocr-layout/scripts/pipeline.py "{input_pdf}"
   ```
4. **Monitor progress** — the script prints step-by-step progress including API polling.
   API jobs typically take 1–5 minutes per 90-page chunk.
5. **Report the output path** when done.

## Resume / Retry

The pipeline saves state to the work directory and is fully resumable:
- `jobs.json` — API job IDs (prevents re-submitting already-queued chunks)
- `chunk_*_results.jsonl` — cached OCR results (skip re-downloading)
- `chunk_*_ocr.pdf` — completed chunk PDFs (skip re-rendering)

If interrupted, simply re-run the same command. It picks up where it left off.

## Common Issues

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run the pip install command above |
| API 4xx error | Check the PDF isn't password-protected |
| Job stuck in `running` | Normal for large chunks; wait up to 10 min |
| Missing images in output | Images left blank per design (API images are optional) |
| Font too small/large | The font size auto-calibrates — first page may look different if it's a cover |

## Output Quality

- **Block positions**: exact (scaled from 812×1269px OCR space to A4)
- **Font sizes**: auto-calibrated using `fs = min(√(h×w / n×0.65), h×0.72)`
  — verified to recover original ~13–14pt body text
- **Page numbers, headers, footers**: included (all block types preserved)
- **Images**: embedded if URL accessible, blank if not
- **1 OCR page = 1 PDF page**: always maintained
