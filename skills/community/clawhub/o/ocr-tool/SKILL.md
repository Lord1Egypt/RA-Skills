---
name: ocr-tool
description: "OCR (Optical Character Recognition) tool using Tesseract for extracting text from images. Use when: (1) processing screenshots, charts, or documents in image format, (2) extracting text from financial charts, announcements, or reports, (3) analyzing images containing Chinese/English text. NOT for: simple text files (use read tool), PDF files (use other tools), or when Tesseract is not installed."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["tesseract"] },
        "install":
          [
            {
              "id": "choco",
              "kind": "choco",
              "package": "tesseract",
              "bins": ["tesseract"],
              "label": "Install Tesseract OCR (choco)",
            },
            {
              "id": "winget",
              "kind": "winget",
              "package": "UB-Mannheim.Tesseract",
              "bins": ["tesseract"],
              "label": "Install Tesseract OCR (winget)",
            },
            {
              "id": "apt",
              "kind": "apt",
              "package": "tesseract-ocr",
              "bins": ["tesseract"],
              "label": "Install Tesseract OCR (apt)",
            },
            {
              "id": "brew",
              "kind": "brew",
              "package": "tesseract",
              "bins": ["tesseract"],
              "label": "Install Tesseract OCR (brew)",
            },
          ],
      },
  }
---

# OCR Tool Skill

Use Tesseract OCR to extract text from images, particularly useful for financial charts, announcements, reports, and screenshots containing Chinese and English text.

## When to Use

✅ **USE this skill when:**

- Processing screenshots of financial charts or announcements
- Extracting text from images containing Chinese/English text
- Analyzing "公告全知道" or similar financial announcement images
- Processing images with tabular data or structured information
- Extracting text from charts, reports, or documents in image format

## When NOT to Use

❌ **DON'T use this skill when:**

- Text files are already available (use `read` tool)
- PDF files (use other PDF extraction tools)
- Images without text content
- When Tesseract is not installed

## Setup

```bash
# Verify Tesseract installation
tesseract --version

# Install language packs if needed (for Chinese)
# Windows: Download chi_sim.traineddata from https://github.com/tesseract-ocr/tessdata
# Place in: C:\Program Files\Tesseract-OCR\tessdata\
```

## Basic Usage

### Extract Text from Image

```bash
# Basic OCR (English)
tesseract image.png output.txt

# Chinese OCR
tesseract image.png stdout -l chi_sim

# Chinese + English OCR
tesseract image.png stdout -l chi_sim+eng

# Specify output format
tesseract image.png output -l chi_sim+eng pdf txt
```

### Common Patterns for Financial Analysis

```bash
# Extract text from financial announcement images
tesseract announcement.png stdout -l chi_sim+eng | grep -E "公司|股份|增长|利润"

# Process multiple images
for img in *.png; do
    echo "=== $img ==="
    tesseract "$img" stdout -l chi_sim+eng
done

# Save OCR results
tesseract financial_chart.png financial_analysis.txt -l chi_sim+eng
```

## Integration with OpenClaw

### Example: Process Telegram Image Messages

```bash
# When receiving image messages via Telegram
# 1. Image is automatically downloaded to media directory
# 2. Use OCR to extract text
# 3. Analyze extracted content

# Find latest image
latest_img=$(ls -t "$HOME/.openclaw/media/inbound/"*.png | head -1)

# Extract text
tesseract "$latest_img" stdout -l chi_sim+eng

# Analyze for specific patterns (company names, financial data)
tesseract "$latest_img" stdout -l chi_sim+eng | grep -oE "#[^ ]+|【[^】]+】"
```

### Example: Financial Announcement Analysis

```bash
#!/bin/bash
# analyze_financial_image.sh

IMAGE="$1"
OUTPUT="analysis_$(date +%Y%m%d_%H%M%S).txt"

echo "=== OCR Analysis Report ===" > "$OUTPUT"
echo "Image: $IMAGE" >> "$OUTPUT"
echo "Time: $(date)" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Extract text
echo "=== Extracted Text ===" >> "$OUTPUT"
tesseract "$IMAGE" stdout -l chi_sim+eng >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "=== Key Information ===" >> "$OUTPUT"

# Extract company names
echo "Company Names:" >> "$OUTPUT"
tesseract "$IMAGE" stdout -l chi_sim+eng | grep -oE "[A-Za-z0-9]+股份|[A-Za-z0-9]+科技|[A-Za-z0-9]+集团" | sort -u >> "$OUTPUT"

# Extract stock codes
echo "" >> "$OUTPUT"
echo "Stock Codes:" >> "$OUTPUT"
tesseract "$IMAGE" stdout -l chi_sim+eng | grep -oE "[0-9]{6}\.[A-Z]{2,4}" | sort -u >> "$OUTPUT"

# Extract financial metrics
echo "" >> "$OUTPUT"
echo "Financial Metrics:" >> "$OUTPUT"
tesseract "$IMAGE" stdout -l chi_sim+eng | grep -oE "同比增长[0-9.]+%|利润[0-9.]+亿元|增长[0-9.]+%" | sort -u >> "$OUTPUT"

echo "Analysis saved to: $OUTPUT"
```

## Advanced Usage

### Multiple Language Support

```bash
# Chinese Simplified
tesseract image.png stdout -l chi_sim

# Chinese Traditional
tesseract image.png stdout -l chi_tra

# Japanese
tesseract image.png stdout -l jpn

# Korean
tesseract image.png stdout -l kor

# Multiple languages
tesseract image.png stdout -l chi_sim+eng+jpn
```

### Image Preprocessing (Improve Accuracy)

```bash
# Convert to grayscale (using ImageMagick)
convert image.png -grayscale Rec709Luma grayscale.png
tesseract grayscale.png stdout -l chi_sim+eng

# Increase contrast
convert image.png -contrast -contrast enhanced.png
tesseract enhanced.png stdout -l chi_sim+eng

# Remove noise
convert image.png -despeckle denoised.png
tesseract denoised.png stdout -l chi_sim+eng
```

### Batch Processing

```bash
# Process all PNG images in directory
for img in *.png; do
    base=$(basename "$img" .png)
    tesseract "$img" "output_${base}.txt" -l chi_sim+eng
    echo "Processed: $img -> output_${base}.txt"
done

# Process with parallel (if available)
find . -name "*.png" -print0 | parallel -0 tesseract {} {.}.txt -l chi_sim+eng
```

## Common Use Cases

### 1. Financial Announcements ("公告全知道")

```bash
# Extract key information from financial announcements
tesseract announcement.png stdout -l chi_sim+eng | \
    grep -A2 -B2 -E "公司|股份|增长|利润|合同|中标|收购"

# Find company mentions
tesseract announcement.png stdout -l chi_sim+eng | \
    grep -oE "#[^ ]+|【[^】]+】|([A-Za-z0-9\u4e00-\u9fa5]+股份)"
```

### 2. Stock Charts and Tables

```bash
# Extract stock data from charts
tesseract stock_chart.png stdout -l eng | \
    grep -E "[0-9]+\.[0-9]+|[0-9]+%"

# Process tabular data
tesseract table.png stdout -l chi_sim+eng | \
    awk 'BEGIN {FS="[[:space:]]{2,}"} {for(i=1;i<=NF;i++) printf "|%s", $i; print "|"}'
```

### 3. Document Screenshots

```bash
# Extract structured document content
tesseract document.png stdout -l chi_sim+eng | \
    sed -n '/^[0-9]\+\./p'  # Extract numbered items

# Extract headings
tesseract document.png stdout -l chi_sim+eng | \
    grep -E "^#|^【|^（"
```

## Troubleshooting

### Common Issues

1. **Poor OCR accuracy**
   - Preprocess images (grayscale, contrast enhancement)
   - Use appropriate language packs
   - Ensure image resolution is sufficient (300 DPI recommended)

2. **Missing Chinese characters**
   - Verify chi_sim.traineddata is installed
   - Use `-l chi_sim+eng` for mixed content
   - Check image quality and font clarity

3. **Tesseract not found**
   - Install Tesseract via package manager
   - Add Tesseract to PATH environment variable
   - Verify installation with `tesseract --version`

### Improving Accuracy

```bash
# Use custom configuration
tesseract image.png stdout -l chi_sim+eng --psm 6  # Assume uniform block of text
tesseract image.png stdout -l chi_sim+eng --psm 11  # Sparse text

# PSM modes:
# 3 = Fully automatic page segmentation, but no OSD (default)
# 6 = Assume a single uniform block of text
# 11 = Sparse text. Find as much text as possible in no particular order
# 12 = Sparse text with OSD

# Use OEM (OCR Engine Mode)
tesseract image.png stdout -l chi_sim+eng --oem 1  # LSTM only
tesseract image.png stdout -l chi_sim+eng --oem 2  # Legacy + LSTM
tesseract image.png stdout -l chi_sim+eng --oem 3  # Default
```

## Performance Tips

- For batch processing, consider parallel execution
- Cache OCR results for repeated analysis
- Preprocess images to improve speed and accuracy
- Use appropriate PSM mode for image type

## Integration Examples

### With Python Scripts

```python
import subprocess
import re

def ocr_image(image_path, lang='chi_sim+eng'):
    """Extract text from image using Tesseract"""
    result = subprocess.run(
        ['tesseract', image_path, 'stdout', '-l', lang],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    return result.stdout

# Example usage
text = ocr_image('announcement.png')
companies = re.findall(r'#(\S+)', text)
print(f"Found companies: {companies}")
```

### With Shell Scripts

```bash
#!/bin/bash
# analyze_financial_images.sh

analyze_image() {
    local img="$1"
    echo "Analyzing: $img"
    
    # Extract text
    text=$(tesseract "$img" stdout -l chi_sim+eng)
    
    # Extract key information
    echo "=== Summary ==="
    echo "Companies: $(echo "$text" | grep -oE '#[^ ]+' | tr '\n' ' ')"
    echo "Stock Codes: $(echo "$text" | grep -oE '[0-9]{6}\.[A-Z]{2,4}' | tr '\n' ' ')"
    echo "Financial Terms: $(echo "$text" | grep -oE '同比增长|利润|增长|合同' | sort -u | tr '\n' ' ')"
}

# Process all images
for img in "$@"; do
    analyze_image "$img"
    echo ""
done
```

## Notes

- Tesseract works best with clean, high-contrast images
- Chinese OCR requires chi_sim/chi_tra language data files
- For financial charts with small text, ensure image resolution is sufficient
- Consider image preprocessing for better results with screenshots
- Always verify OCR results, especially for critical financial data
