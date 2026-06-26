---
name: pdf-image-extractor
description: Extract images from PDF files with three modes: original (keep original quality), standard (800x800 square for website), compress (under 50KB for social media). Use when user needs to extract product images from furniture catalogs, marketing materials, or any PDF document. Triggers: "extract PDF images", "PDF to images", "extract from PDF".
---

# PDF Image Extractor

Extract images from PDF files with three output modes.

## Three Modes

| Mode | Command | Best For |
|------|---------|----------|
| Original | `python scripts/extract_original.py` | Printing, high-quality |
| Standard | `python scripts/extract_standard.py` | Website, e-commerce |
| Compress | `python scripts/extract_compress.py` | WeChat, Douyin, social |

## Quick Start

```bash
# Install dependencies
pip install pymupdf pillow

# Configure
# Edit CONFIG section at top of each script:
# - pdf_folder: Path to your PDF folder
# - output_folder: Where to save images

# Run
python scripts/extract_original.py    # Original quality
python scripts/extract_standard.py    # 800x800 square
python scripts/extract_compress.py    # Compressed sharing
```

## Output Structure

```
output_folder/
├── PDF_Name_1/
│   ├── page001_img01.jpg
│   └── ...
└── PDF_Name_2/
    └── ...
```

## Requirements

- Python 3.7+
- PyMuPDF (pymupdf)
- Pillow (PIL)

## Use Cases

- **Furniture manufacturers**: Extract catalog images for printing
- **E-commerce**: Prepare product images for websites  
- **Sales**: Compress images for WeChat Moments, Douyin

---

License: MIT  
Author: 小杰 @ AI家具链
