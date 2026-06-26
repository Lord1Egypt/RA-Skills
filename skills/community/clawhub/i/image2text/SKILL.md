---
name: image2text
description: Extract text from any image using tesseract OCR — works with any AI model even if it has no vision capability. Supports local file paths, web URLs (OSS/http/https), and base64 image data pasted directly from clipboard. Use when: user uploads an image and asks what's in it, screenshots or clipboard images need OCR, document images need text extraction, or any image-to-text task. Perfect for text-only AI models that can't "see" images.
---

# image2text

Extract text from images without needing a vision-capable AI model.

## Usage

```
python3 scripts/ocr.py <image path|URL|base64> [--lang <languages>] [--psm <mode>] [--raw]
```

## Parameters

- `--lang`: Language codes, comma-separated, default `chi_sim+eng`
  - `chi_sim` Simplified Chinese | `chi_tra` Traditional | `eng` English | `jpn` Japanese | `kor` Korean | and 30+ more
  - Combine: `chi_sim+eng`
- `--psm`: Page segmentation mode, default `6`
  - `3` Fully automatic | `6` Block-level | `4` Single line | `11` Sparse text
- `--raw`: Output plain text only, no markers

## Auto-Detects Input Type

1. **Local path**: `/Users/xxx/Downloads/xxx.png`
2. **Web URL**: `https://example.com/image.png` — OSS temp links work too
3. **Base64**: Pasted image data from clipboard — just paste directly

## Workflow

1. Receive image input → auto-detect type (local path / URL / base64)
2. URL → curl downloads to temp file
3. Base64 → decode to temp file
4. Run tesseract OCR
5. Output plain text

## Examples

OCR a Chinese receipt:
```bash
python3 scripts/ocr.py ~/Downloads/receipt.png --lang chi_sim
```

English + Chinese mixed:
```bash
python3 scripts/ocr.py https://example.com/doc.jpg --lang chi_sim+eng
```

Plain text only (no markers):
```bash
python3 scripts/ocr.py /path/to/image.png --raw
```

## Requirements

- **tesseract** must be installed: `brew install tesseract`
- Language packs auto-installed with tesseract
- On Mac: binary at `/opt/homebrew/bin/tesseract`
- Temp files auto-deleted after execution
- For best accuracy on receipts/screenshots: try `--psm 3`
