---
name: pdf-ocr-extractor
description: Extract text from image-based or scanned PDFs using Tesseract OCR.
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["tesseract", "python3"] },
        "install":
          [
            {
              "id": "tesseract-ocr",
              "kind": "system",
              "package": "tesseract",
              "bins": ["tesseract"],
              "label": "Install Tesseract OCR (requires language packs e.g., tesseract-ocr-chi-sim)"
            },
            {
              "id": "pip-deps",
              "kind": "uv",
              "package": "pypdfium2 pytesseract Pillow",
              "label": "Install Python dependencies (pypdfium2, pytesseract, Pillow)"
            }
          ]
      }
  }
---

# PDF OCR Extractor

Use this skill to extract text from scanned PDFs or image-based PDFs that lack a native text layer. It's completely free, doesn't utilize third-party APIs, and offers unlimited usage. It renders PDF pages to images and runs optical character recognition (OCR).

## Dependencies

This skill requires:
1.  **System Binary**: `tesseract` (along with required language data packs like `chi_sim` or `eng`).
2.  **Python Packages**: `pypdfium2`, `pytesseract`, and `Pillow`.

*Note: Do not run automated `pip install` commands at runtime. Rely on the user or the environment to pre-install the dependencies defined in the metadata block.*

## Quick Start

Create a Python script (e.g., `extract.py`) in a temporary directory to handle the extraction safely:

```python
import pypdfium2 as pdfium
import pytesseract
from PIL import Image
import sys
import os

def extract(pdf_path):
    doc = pdfium.PdfDocument(pdf_path)
    full_text = []
    for i, page in enumerate(doc):
        # Render page to a high-resolution image
        bitmap = page.render(scale=2)
        tmp_img = f"/tmp/page_{i}.png"
        bitmap.to_pil().save(tmp_img)
        
        # Run OCR (assuming English and Simplified Chinese packs are installed)
        text = pytesseract.image_to_string(Image.open(tmp_img), lang='chi_sim+eng')
        full_text.append(text)
        
        # Cleanup temporary file
        os.remove(tmp_img)
        
    return "\n".join(full_text)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(extract(sys.argv[1]))
```

Then execute the script:
```bash
python3 extract.py /path/to/document.pdf
```

## Security & Sandbox Constraints
- Write temporary images only to `/tmp/` and clean them up immediately after extraction.
- Do not attempt to dynamically download or install language packs via shell commands; notify the user if a specific language is missing.