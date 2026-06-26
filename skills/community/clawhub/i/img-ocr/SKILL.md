---
name: img-ocr
description: Image text recognition tool based on Tesseract OCR. Activate when user mentions: image recognition, OCR, text extraction, image to text, recognize text in images.
---

# img-ocr

Image text recognition tool based on Tesseract OCR.

## Dependencies

- Python3
- pytesseract: `pip3 install pytesseract`
- Pillow: `pip3 install Pillow`
- Tesseract OCR: `sudo apt install tesseract-ocr`
- Chinese lang pack: `sudo apt install tesseract-ocr-chi-sim`

## Quick Usage

```bash
python3 skills/img-ocr/scripts/ocr.py /path/to/image.jpg
```

## Typical Scenarios

```bash
# Recognize Chinese + English
python3 skills/img-ocr/scripts/ocr.py screenshot.png

# Extract text from screenshot
python3 skills/img-ocr/scripts/ocr.py /path/to/screenshot.jpg
```
