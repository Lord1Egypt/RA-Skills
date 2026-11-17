# PDF PPTX Watermark

> 🔒 PPTX→PDF watermark tool with real-time mobile parameter tuning.

Convert PPT/PPTX to PDF and add custom watermarks — diagonal, grid, or center layout. Tune every parameter live from your phone.

## Mobile Parameter Tuning

Tune every watermark parameter in real-time from your phone — scan QR code, adjust sliders, preview instantly, copy JSON config.

**Live Demo:**

![Mobile Demo](docs/watermark-demo.gif)

**Mobile UI:**

![Mobile UI](docs/watermark-mobile.png)

**Fold View:**

![Fold View](docs/watermark-mobile-fold.png)

## Watermark Effects

**Before (original PDF):**

![Original](images/sample_doc.png)

**Diagonal (default) — 45° rotated "CONFIDENTIAL":**

![Diagonal](images/wm_diagonal.png)

**Grid — uniform "INTERNAL" grid pattern:**

![Grid](images/wm_grid.png)

**Center — large "DRAFT" centered stamp:**

![Center](images/wm_center.png)

## Quick Start

```bash
# PPTX → watermarked PDF (one step)
python3 scripts/pptx_to_pdf_watermark.py input.pptx output.pdf

# PDF → watermarked PDF with custom config
python3 scripts/pptx_to_pdf_watermark.py input.pdf output.pdf config.json
```

## Features

- 📱 **Mobile parameter tuning** — QR code → phone → live preview → copy JSON
- 📐 **3 layout modes** — diagonal / grid / center
- 🎨 **Full customization** — text, size, opacity, rotation, color
- 🌍 **Cross-platform** — auto-detects CJK fonts (macOS/Linux/Windows)
- 📦 **PPTX support** — LibreOffice-powered one-step conversion
- 🔒 **Local & safe** — no network, no credentials, input never modified

## Config

```json
{
  "text": "CONFIDENTIAL",
  "fontSize": 60,
  "opacity": 0.15,
  "rotation": 45,
  "color": [0.5, 0.5, 0.5],
  "pattern": "diagonal"
}
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `text` | `"内部资料 请勿外传"` | Watermark text |
| `fontSize` | `60` | Font size (pt) |
| `opacity` | `0.15` | Transparency (0–1) |
| `rotation` | `45` | Rotation (degrees) |
| `color` | `[0.5, 0.5, 0.5]` | RGB (0–1) |
| `pattern` | `"diagonal"` | `diagonal` / `grid` / `center` |

## Dependencies

- **LibreOffice**: `brew install --cask libreoffice` (macOS) / `apt install libreoffice` (Linux)
- **Python 3**: `pip3 install PyPDF2 reportlab`

## License

MIT-0
