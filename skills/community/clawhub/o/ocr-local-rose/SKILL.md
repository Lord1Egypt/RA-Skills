---
name: ocr-local
description: Extract text from images using Tesseract.js OCR (100% local, no API key required). Supports Chinese (simplified/traditional) and English.
homepage: https://github.com/naptha/tesseract.js
metadata: {"openclaw":{"emoji":"📝","requires":{"bins":["node"]},"install":[{"id":"npm","kind":"npm","packages":["tesseract.js"],"label":"Install tesseract.js"}]}}
---

# OCR - Image Text Recognition (Local)

Extract text from images using Tesseract.js. **100% local run, no API key required.** Supports Chinese and English.

## Quick start

```bash
node {baseDir}/scripts/ocr.js /path/to/image.jpg
node {baseDir}/scripts/ocr.js /path/to/image.png --lang chi_sim
node {baseDir}/scripts/ocr.js /path/to/image.jpg --lang chi_tra+eng
```

## Options

- `--lang <langs>`: Language codes (default: chi_sim+eng)
  - `chi_sim` - Simplified Chinese
  - `chi_tra` - Traditional Chinese  
  - `eng` - English
  - Combine with `+`: `chi_sim+eng`

- `--json`: Output as JSON instead of plain text

## Examples

```bash
# Recognize Chinese screenshot
node {baseDir}/scripts/ocr.js screenshot.png

# Recognize English document
node {baseDir}/scripts/ocr.js document.jpg --lang eng

# Mixed Chinese + English
node {baseDir}/scripts/ocr.js mixed.png --lang chi_sim+eng
```

## Notes

- Language data is stored in `{baseDir}/scripts/tessdata/`
- First run downloads language data (~20MB per language)
- Subsequent runs use cached data
- Works best with clear, high-contrast images
- For handwritten text, accuracy may vary

## Language Data

Language model files (`.traineddata.gz`) are automatically downloaded on first use and stored in:
```
{baseDir}/scripts/tessdata/
- chi_sim.traineddata.gz (Simplified Chinese)
- eng.traineddata.gz (English)
```

To manually download or update language data:
```bash
cd {baseDir}/scripts/tessdata
curl -O https://cdn.jsdelivr.net/npm/@tesseract.js-data/chi_sim/4.0.0_best_int/chi_sim.traineddata.gz
curl -O https://cdn.jsdelivr.net/npm/@tesseract.js-data/eng/4.0.0_best_int/eng.traineddata.gz
```
