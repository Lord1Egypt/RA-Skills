---
name: long-image-to-pdf
description: Slices long images/screenshots into overlapping segments and auto-arranges them into a paginated PDF.
license: MIT
metadata:
  author: ByronLeeeee
  version: "1.0"
---

# Long Image to PDF Processor

## When to use this skill
Use this skill when the user provides a very long image (like a long chat screenshot or a full webpage capture) and wants to convert it into a well-formatted PDF document. 

## Prerequisites
Required python packages: `Pillow`, `reportlab`.

## How to use this skill
Execute the python script `scripts/slice_and_pdf.py` via the command line.

### Command Syntax
```bash
python scripts/slice_and_pdf.py --source <path_to_image> --out-dir <output_directory> [OPTIONS]
```

### Required Arguments
* `--source`: Path to the source long image file. **(Always use absolute paths if possible)**
* `--out-dir`: Directory where the final PDF will be saved.

### Optional Arguments
* `--pdf-name`: Name of the output PDF file (default: `output.pdf`).
* `--slice-height`: Height of each slice in pixels (default: `2000`).
* `--overlap`: Overlap height between consecutive slices in pixels (default: `200`).
* `--cols`: Number of columns in the PDF (default: `2`).
* `--rows`: Number of rows in the PDF (default: `2`).
* `--layout`: Arrangement sequence, either `grid` (left-to-right) or `column` (top-to-bottom) (default: `grid`).
* `--cleanup`: Add this flag to automatically delete the intermediate image slices after the PDF is created. (Highly recommended to save disk space unless the user explicitly asks to keep the sliced images).

## ⚠️ Important Instructions for the Agent (Guardrails)
1. **Always apply `--cleanup`** by default, unless the user specifically says "I want the sliced pictures too". Users generally only care about the final PDF.
2. **Absolute Paths**: When constructing the command, resolve any paths (like `~` or relative paths) to absolute paths to prevent execution errors.
3. **DO NOT attempt to read the output PDF**: The resulting file is a visual/binary PDF. Do not try to `cat`, `read`, or use text-extraction tools on the final PDF to verify it. Just read the command line standard output (STDOUT); if it says `STATUS: Success`, tell the user the path where the PDF is saved.

## Examples

**Example 1: Normal conversion (Will auto-cleanup slices, 2x2 grid)**
```bash
python scripts/slice_and_pdf.py --source "/Users/bob/Downloads/long_chat.png" --out-dir "/Users/bob/Desktop/Output" --cleanup
```

**Example 2: Customizing to 1 column, 3 rows, keeping intermediate slices**
```bash
python scripts/slice_and_pdf.py --source "/abs/path/webpage.jpg" --out-dir "./results" --cols 1 --rows 3
```