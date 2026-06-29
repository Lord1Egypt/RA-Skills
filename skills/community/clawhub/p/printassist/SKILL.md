---
name: print-assist
description: Print any file (PDF, Word, Excel, PowerPoint, photos) with a plain-language instruction. Handles 2-up layout, duplex, page ranges, rotation, watermarks, and photo editing via Adobe CC — without touching a single print dialog.
version: 0.1.0
emoji: 🖨️
homepage: https://github.com/nilsgollub/PrintAssist
metadata:
  openclaw:
    requires:
      bins:
        - python
    os:
      - win32
    install:
      - method: shell
        cmd: pip install -r requirements.txt
---

# Print Assist

Print any file by describing what you want. No more fighting with print dialogs.

## What you can say

```
Print this PDF double-sided, A4, black and white.
Drucke das zweimal nebeneinander auf ein Querformat-Blatt.
Print pages 2-5 of this document, 2 copies.
Rotate all pages 90 degrees and print.
Merge these three PDFs and print the result.
Remove the background from this photo and print it on A4.
Show me a preview before printing.
```

## Tool Routing

| Task | Script | Key function |
|---|---|---|
| Print PDF | `scripts/print.py` | `print_file(path, printer, params)` |
| Print Office file (Word/Excel/PPT) | `scripts/print.py` | auto-converts via LibreOffice, then prints |
| Print image/photo | `scripts/print.py` | Pillow + win32print |
| 2-up (two pages side by side) | `scripts/pdf_tools.py` | `impose_2up(input, output)` |
| Merge PDFs | `scripts/pdf_tools.py` | `merge_pdfs(inputs, output)` |
| Split PDF | `scripts/pdf_tools.py` | `split_pdf(input, output_dir, pages_per_file)` |
| Rotate pages | `scripts/pdf_tools.py` | `rotate_pages(input, output, degrees, pages)` |
| Add watermark | `scripts/pdf_tools.py` | `add_watermark(input, watermark, output)` |
| Encrypt / decrypt PDF | `scripts/pdf_tools.py` | `encrypt_pdf()` / `decrypt_pdf()` |
| Extract pages | `scripts/pdf_tools.py` | `extract_pages(input, output, page_numbers)` |
| Compress PDF | `scripts/pdf_tools.py` | `compress_pdf(input, output)` |
| Edit Word content | `scripts/office_tools.py` | `replace_text_docx()`, `format_paragraph_docx()` |
| Edit Excel cells | `scripts/office_tools.py` | `write_cell_xlsx()`, `replace_value_xlsx()` |
| Edit PowerPoint slides | `scripts/office_tools.py` | `replace_text_pptx()`, `add_slide_pptx()` |
| Preview before printing | `scripts/pdf_tools.py` | `preview_pdf()` → copy to `preview.png` |
| Photo editing (exposure, crop, bg remove) | Adobe CC MCP connector | see Adobe routing table in CLAUDE.md |

## Print parameters

Pass as a dict to `print_file()`:

| Key | Values | Example |
|---|---|---|
| `paper` | `A4`, `A3`, `Letter`, `Legal` | `"A4"` |
| `orientation` | `portrait`, `landscape` | `"landscape"` |
| `duplex` | `duplex`, `duplexshort`, `simplex` | `"duplex"` |
| `color` | `color`, `monochrome` | `"monochrome"` |
| `scale` | `fit`, `shrink`, `noscale` | `"fit"` |
| `pages` | SumatraPDF range string | `"1-3,5"` |
| `copies` | integer | `2` |

## Setup

### First-time (per device)

```powershell
# Windows — run once per machine
powershell -ExecutionPolicy Bypass -File setup.ps1
```

This installs SumatraPDF and LibreOffice via winget, runs pip, and guides you through entering your printer name.

### Printer config

Edit `config/printers.yaml`:

```yaml
default:
  printer_name: "Your Printer Name"   # get via: wmic printer get name
hosts:
  YOUR-HOSTNAME:
    printer_name: "Your Printer Name"
```

### Preview workflow

Always offer a preview for layout-heavy requests (2-up, booklet, rotated):

```python
from scripts.pdf_tools import preview_pdf
import shutil

previews = preview_pdf("output.pdf", dpi=150)
shutil.copy(previews[0], "preview.png")
# Tell user: "Preview saved as preview.png — click it in the file explorer."
```

## What this skill cannot do

- Edit text inside a PDF → direct user to Acrobat
- Upscale images beyond native resolution
- Replace backgrounds generatively (only remove them)
- Wake the PC remotely over WiFi (WoL requires Ethernet)
