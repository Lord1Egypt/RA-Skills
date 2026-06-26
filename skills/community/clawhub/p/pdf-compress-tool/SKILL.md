---
name: pdf-compress-tool
description: "Compress PDF files to a target size or by percentage, using a Ghostscript + pikepdf + QPDF multi-stage pipeline."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      bins:
        - python3
    optional:
      - kind: brew
        formula: ghostscript
        bins: [gs]
      - kind: brew
        formula: qpdf
        bins: [qpdf]
    emoji: "📄"
    os: ["macos", "linux", "windows"]
---

# PDF Compress Tool

Performs actual PDF compression, supporting both target size and percentage modes. Unlike existing solutions that only provide guidance, this tool compresses files directly.

## Features

- **Two compression modes**: target size (`--target-size 2MB`) / percentage (`--reduce 30`)
- **Three-stage compression pipeline**: pikepdf structural optimization → Ghostscript progressive compression → QPDF secondary optimization
- **Quality floor protection**: three levels (high / medium / low) to prevent excessive compression from damaging image quality
- **Batch processing**: compress all PDFs in a directory at once
- **Auto dependency detection**: detects available tools at runtime and adapts compression strategy accordingly

## Usage

### Compress to target size

```
"Compress this PDF to under 2MB"
"Compress this PDF to under 5MB"
```

```bash
python compress_pdf.py report.pdf --target-size 2MB
```

### Compress by percentage

```
"Reduce the file size by 30%"
"Reduce the file size by 50%"
```

```bash
python compress_pdf.py report.pdf --reduce 30
```

### Specify output path and quality

```bash
python compress_pdf.py report.pdf --reduce 50 --quality low -o small.pdf
```

### Batch processing

```
"Compress all PDFs in the papers folder to under 2MB"
```

```bash
python compress_pdf.py --batch ./papers --target-size 2MB
python compress_pdf.py --batch ./papers --reduce 40 --quality high
```

## Compression Strategy

### Stage 1: pikepdf structural optimization

Removes redundant objects, compresses streams, and packs object streams. Lossless operation that preserves maximum image quality.

### Stage 2: Ghostscript progressive compression

Tries prepress → printer → ebook → screen progressively, checking at each level and stopping as soon as the target is met.
Also supports custom DPI downsampling (100 → 72 → 50 → 36 dpi), subject to quality floor protection.

### Stage 3: QPDF secondary optimization

Object stream generation and stream recompression, saving an additional 5-15%. Requires qpdf installation (optional).

### Quality floor protection

| Level | Meaning | Minimum compression level | Use case |
|-------|---------|--------------------------|----------|
| `high` | Quality priority | printer (300dpi) | Documents intended for printing |
| `medium` | Balanced (default) | ebook (150dpi) | Everyday use |
| `low` | Size priority | screen (72dpi) and below | Screen viewing only |

## Dependencies

- **python3** (required)
- **ghostscript** (recommended): core compression engine
- **qpdf** (optional): secondary structural optimization, additional 5-15% compression
- **pikepdf** (auto-installed via pip): Python PDF library, fallback when Ghostscript is unavailable

### Install by platform

| Dependency | macOS | Linux (Debian/Ubuntu) | Linux (RHEL/Fedora) | Windows |
|------------|-------|-----------------------|---------------------|---------|
| ghostscript | `brew install ghostscript` | `sudo apt-get install ghostscript` | `sudo dnf install ghostscript` | `choco install ghostscript` or [download](https://ghostscript.com/releases/gsdnld.html) |
| qpdf | `brew install qpdf` | `sudo apt-get install qpdf` | `sudo dnf install qpdf` | `choco install qpdf` or [download](https://github.com/qpdf/qpdf/releases) |
| pikepdf | `pip install pikepdf` (auto) | `pip install pikepdf` (auto) | `pip install pikepdf` (auto) | `pip install pikepdf` (auto) |

The script auto-detects your platform and shows the correct install command when a dependency is missing.
