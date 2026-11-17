# PDF Watermark

> One-liner: Convert PPT/PPTX to PDF and add custom watermarks — all offline, one command.

[![Agent Skills](https://img.shields.io/badge/Agent-Skills-blue)](https://clawhub.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)]()

[中文](README.md) | **English**

---

## When do you need it?

1. **Internal materials**: Convert PPT to PDF and stamp "Confidential" before sharing.
2. **Batch watermarking**: Add company name or "Do Not Distribute" to existing PDFs.
3. **Client deliverables**: Add a subtle watermark to presentations before sending out.

---

## What does it deliver?

- A watermarked PDF file (from PPTX or existing PDF)
- Three layout modes: diagonal (default), grid, or centered
- Full control over text, size, opacity, rotation, and color
- Optional web UI for real-time parameter tuning

---

## Quick Start

```bash
# Install dependencies
pip3 install PyPDF2 reportlab
brew install --cask libreoffice  # macOS; or apt install libreoffice on Linux

# One-step: PPTX → watermarked PDF
python3 scripts/pptx_to_pdf_watermark.py presentation.pptx output.pdf

# With custom config
python3 scripts/pptx_to_pdf_watermark.py presentation.pptx output.pdf config.json
```

---

## Configuration

```json
{
  "text": "CONFIDENTIAL",
  "fontSize": 60,
  "opacity": 0.15,
  "rotation": 45,
  "pattern": "diagonal",
  "color": [0.5, 0.5, 0.5]
}
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `text` | Watermark text | `"内部资料 请勿外传"` |
| `fontSize` | Font size in pt | `60` |
| `opacity` | Transparency 0–1 | `0.15` |
| `rotation` | Rotation degrees | `45` |
| `color` | RGB 0–1 | `[0.5, 0.5, 0.5]` |
| `pattern` | `diagonal` / `grid` / `center` | `"diagonal"` |

---

## How is it different?

| Feature | pdf-watermark | Online Tools | Plain Scripts |
|---------|--------------|-------------|----------------|
| PPTX → PDF + Watermark | ✅ One step | ❌ Separate | ❌ |
| Web UI for tuning | ✅ Included | ✅ | ❌ |
| Cross-platform fonts | ✅ Auto-detect | N/A | ❌ |
| Works offline | ✅ | ❌ | ✅ |
| Configurable via JSON | ✅ | ❌ | ❌ |

---

## Safety

- ✅ Never modifies the input file
- ✅ No network access required
- ✅ No API keys or credentials
- ✅ All processing is local

---

## License

MIT
