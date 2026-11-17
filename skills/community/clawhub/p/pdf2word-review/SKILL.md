---
name: pdf2word-review
description: Convert PDF to editable Word and automatically verify the conversion quality. Runs a four-way reconciliation (character count, table count, image count, table-cell count) plus a page-count reference after conversion, so content loss or redundancy is surfaced as evidence instead of guesswork. Use when the user asks to convert PDF to Word, convert PDF to docx, check conversion quality, verify a converted document, or worries that PDF-to-Word conversion dropped content.
version: 0.1.0
license: AGPL-3.0
author: hectorlee
tags: [pdf, word, docx, conversion, quality-review, ocr, reconciliation]
---

# PDF → Word Conversion + Automatic Quality Review

## Overview

Convert a PDF into an editable Word document, then **automatically audit the conversion** — reconciling character count, table count, image count, and table-cell count, turning "did the conversion drop anything?" from a feeling into evidence. That is the differentiator versus plain PDF converters: they only convert; this one also tells you *where* the conversion may have gone wrong.

The underlying engine is the standalone open-source project `pdf2word-review` (AGPL-3.0, GitHub: https://github.com/xiyanjun/pdf-to-word-review ). This skill is a **thin wrapper**: it calls the tool and interprets results, and does not vendor any engine code.

## Installation

Check whether the CLI is available first:

```bash
pdf2word --help >/dev/null 2>&1 && echo "installed" || echo "need install"
```

If missing, install (GitHub direct install works even before the PyPI release):

```bash
# Option 1: PyPI (after official release)
pip install pdf2word-review

# Option 2: GitHub direct install (works today, recommended)
pip install git+https://github.com/xiyanjun/pdf-to-word-review.git
```

Only four lightweight core dependencies are pulled in automatically (pdf2docx, PyMuPDF, python-docx, lxml). OCR is optional — see "Scanned PDF OCR".

## Workflow

### Step 1: Confirm the input

- Verify the user's path exists and is a `.pdf`.
- Batch mode: multiple PDFs are supported in one pass.

### Step 2: Convert (auto-routed)

```bash
pdf2word <input.pdf> -o <output.docx> --verify --html
```

The CLI detects the text layer and routes automatically:

| Case | Automatic behavior |
|---|---|
| Has text layer | convert → empty-paragraph cleanup → layout polish |
| No text layer (scanned) | OCR rebuild |

Key flags:

| Flag | Effect |
|---|---|
| `-o <path>` | Output docx path (single file only) |
| `--verify` | **Core**: run the four-way reconciliation after conversion |
| `--html` | Generate a diff-visualization HTML report (`<docx>.report.html`) |
| `--report <json>` | Write the review report to JSON (array in batch mode) |
| `--force-ocr` | Force OCR rebuild |
| `--engine auto/vision/paddle` | OCR backend (default auto: Vision on macOS, else PaddleOCR) |
| `--no-clean` | Skip empty-paragraph cleanup |
| `--no-polish` | Skip layout polish (use on non-macOS, see Notes) |

### Step 3: Quality review (the differentiator)

`--verify` runs a **four-way reconciliation**, each item reporting `PDF value → Word value` delta and a status:

| Item | What it checks |
|---|---|
| Character count | Non-whitespace characters (unified PDF/Word metric) |
| Table count | Tables in source PDF vs target Word |
| Image count | Counted via Word `a:blip` references (avoids media false positives) |
| Table-cell count | row×col reconciliation (catches split/merged tables) |

Page count is reference-only (Word pagination varies with layout).

### Step 4: Interpret and report

Always translate the result into plain language — never dump raw JSON at the user. See "Result Interpretation".

## Result Interpretation

Each item's `status` is one of four values:

| status | Meaning | Severity | How to report |
|---|---|---|---|
| `ok` | Consistent | None | No need to dwell on it |
| `loss` | Content lost (Word < PDF) | 🔴 High | Tell the user exactly what and how much |
| `extra` | Redundant (Word > PDF) | 🟡 Verify | Flag as suspected redundancy; <5% extra chars is normal, not flagged |
| `converted` | Image→text substitution (images down, chars up) | 🟢 Expected | Explain: layout polish turned a banner image into a heading — not loss |

**Report template** (conclusion first, then detail):

```
✅/⚠️ Conversion result: {passed / N items to review}

| Item | PDF | Word | Delta | Verdict |
|------|-----|------|-------|---------|
| Chars | ... | ... | ... | ✅/❌ |
| Tables | ... | ... | ... | ✅/❌ |
| Images | ... | ... | ... | ✅/❌ |
| Table cells | ... | ... | ... | ✅/❌ |

{list each loss/extra with risk note and fix suggestion}
```

Key points:
- Any `loss` or `extra` must be called out by name — never say "might have issues" vaguely.
- When `converted` appears, proactively explain it is expected behavior to avoid false alarm.
- If `--html` was used, give the user the HTML report path (visual diff is clearer than text).

## Scanned PDF OCR

Scanned PDFs (no text layer) are auto-routed to OCR rebuild. OCR has two backends, **both optional, neither installed by default**:

| Backend | Platform | Install |
|---|---|---|
| macOS Vision | macOS only | `pip install pyobjc-framework-Vision pyobjc-framework-Quartz` (lightweight, system framework) |
| PaddleOCR | Cross-platform | `pip install paddleocr paddlepaddle` (heavier; downloads CN/EN models on first run) |

- macOS user processing scans → install Vision.
- Non-macOS → install PaddleOCR.
- Without OCR deps, scanned conversion errors out with an install hint — relay that hint to the user honestly.
- After OCR rebuild, char/image reconciliation does not apply (source has no text layer); rely on the OCR confidence report instead — flag text blocks with confidence < 0.7 for manual review.

## Notes

1. **Layout polish requires macOS**: banner OCR + list-item fixes need system Vision/Quartz. On non-macOS, add `--no-polish`.
2. **AGPL-3.0 boundary**: this skill is a thin wrapper — it only calls the external package and vendors no AGPL code. To change engine logic, open a PR upstream (GitHub) rather than copying code into the skill.
3. **Batch**: `pdf2word a.pdf b.pdf c.pdf --verify --report result.json` writes to each file's directory; `--report` yields a result array.
4. **Char-count tolerance**: <5% extra chars is normal (symbol substitution/formatting); >5% flags redundancy. >2% char loss raises a separate warning.

## License

Thin wrapper. The underlying `pdf2word-review` engine is AGPL-3.0. See https://github.com/xiyanjun/pdf-to-word-review
