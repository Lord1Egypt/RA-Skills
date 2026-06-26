# Local OCR Skill - Detailed Usage Guide

> ⚠️ **macOS Only** - This skill requires macOS 10.15+ (Catalina or later). It will not work on Linux, Windows, or other operating systems.

## Introduction

This document provides comprehensive usage instructions for the local-ocr skill, which uses macOS native Vision framework to perform OCR (Optical Character Recognition) on images and PDFKit for PDF processing.

## Quick Start

### Basic OCR

To extract text from an image:

```bash
swift scripts/ocr_vision_pro.swift /path/to/image.png
```

### Save Results to File (Separated Output)

```bash
swift scripts/ocr_vision_pro.swift /path/to/image.png -o result.txt
```

This will automatically create two files:
- `result.txt` - Complete extracted text
- `result_confidence.txt` - Confidence details

## Output Modes (Mutually Exclusive)

The script supports two output modes that cannot be used simultaneously:

### Text Mode (Default, `-t`)

Outputs only the extracted text. Optionally saves to file with separate confidence file.

**Console output:**
```
[Extracted text content]
```

**With `-o` option:**
Creates two files:
- `result.txt` - Complete extracted text
- `result_confidence.txt` - Confidence details

### JSON Mode (`-j`)

Outputs complete raw information as JSON to stdout. No file output options in JSON mode.

**JSON output structure:**
```json
{
  "imagePath": "/path/to/image.png",
  "totalBlocks": 25,
  "averageConfidence": 0.85,
  "blocks": [
    {
      "index": 1,
      "text": "recognized text",
      "confidence": 0.95,
      "boundingBox": {
        "x": 0.10,
        "y": 0.20,
        "width": 0.30,
        "height": 0.05
      }
    }
  ]
}
```

**JSON fields:**
- `imagePath`: Path to the processed image
- `totalBlocks`: Total number of recognized text blocks
- `averageConfidence`: Average confidence score (0.0 - 1.0)
- `blocks`: Array of recognized text blocks
  - `index`: Block index (1-based)
  - `text`: Recognized text content
  - `confidence`: Confidence score (0.0 - 1.0)
  - `boundingBox`: Normalized bounding box coordinates (0.0 - 1.0)
    - `x`, `y`: Top-left corner position
    - `width`, `height`: Bounding box dimensions

## New Output Format (Text Mode)

## Supported Languages

The OCR script supports the following languages:

| Language Code | Language |
|---------------|----------|
| `zh-Hans` | Simplified Chinese |
| `zh-Hant` | Traditional Chinese |
| `en` | English |
| `ja` | Japanese |
| `ko` | Korean |
| `fr` | French |
| `de` | German |
| `es` | Spanish |
| `it` | Italian |
| `pt` | Portuguese |
| `ru` | Russian |

**Default languages**: `zh-Hans,zh-Hant,en`

## Command-Line Options

### -h, --help

Display help information:

```bash
swift scripts/ocr_vision_pro.swift -h
```

### -l, --language <languages>

Specify recognition language (comma-separated):

```bash
# Chinese and English
swift scripts/ocr_vision_pro.swift image.png -l zh-Hans,en

# Multiple languages
swift scripts/ocr_vision_pro.swift image.png -l zh-Hans,en,ja,ko
```

### -o, --output <file_path>

Output complete text to file, and automatically create a separate confidence file:

```bash
swift scripts/ocr_vision_pro.swift image.png -o result.txt
```

This creates:
- `result.txt` - Complete extracted text
- `result_confidence.txt` - Confidence details

### -t, --text <file_path>

Output only the complete text to specified file (no confidence file):

```bash
swift scripts/ocr_vision_pro.swift image.png -t text_only.txt
```

### -c, --confidence <file_path>

Output only the confidence details to specified file:

```bash
swift scripts/ocr_vision_pro.swift image.png -c confidence.txt
```

### -f, --fast

Use fast mode (lower accuracy, faster processing):

```bash
swift scripts/ocr_vision_pro.swift image.png -f
```

**Default**: Precise mode (higher accuracy, slower processing)

### -j, --json

Output complete raw information as JSON (mutually exclusive with text mode):

```bash
# JSON mode outputs to stdout
swift scripts/ocr_vision_pro.swift image.png -j

# Save JSON output to file
swift scripts/ocr_vision_pro.swift image.png -j > result.json
```

**Note**: JSON mode outputs to stdout only. No file output options (`-o`, `-t`, `-c`) are used in JSON mode.

**JSON output example:**
```json
{
  "imagePath": "/path/to/image.png",
  "totalBlocks": 25,
  "averageConfidence": 0.85,
  "blocks": [
    {
      "index": 1,
      "text": "recognized text",
      "confidence": 0.95,
      "boundingBox": {
        "x": 0.10,
        "y": 0.20,
        "width": 0.30,
        "height": 0.05
      }
    }
  ]
}
```

## Complete Examples

### Example 1: Console Output with Separated Sections

```bash
swift scripts/ocr_vision_pro.swift ~/Desktop/screenshot.png -l zh-Hans,en
```

Output:
```
=== 完整文本 ===

[Extracted text content here]

=== 置信度详情 ===

总识别块数: 25
平均置信度: 0.85

--- 逐块详情 ---

[1] Text block
    置信度: 0.95
    位置: x=0.10, y=0.20, w=0.30, h=0.05

--- 低置信度警告 (< 0.8) ---
[3] "Some text" - 置信度: 0.50
```

### Example 2: Save to Separate Files

```bash
swift scripts/ocr_vision_pro.swift ~/Documents/document.jpg -o ~/Documents/extracted
```

This creates:
- `~/Documents/extracted.txt` - Complete text
- `~/Documents/extracted_confidence.txt` - Confidence details

### Example 3: Separate Text and Confidence Files

```bash
swift scripts/ocr_vision_pro.swift image.png -t text.txt -c details.txt
```

### Example 4: Fast Mode for Quick Preview

```bash
swift scripts/ocr_vision_pro.swift image.png -f
```

### Example 5: Batch Processing Multiple Images

```bash
for img in *.png; do
    swift scripts/ocr_vision_pro.swift "$img" -o "${img%.png}_ocr"
done
```

This creates for each image:
- `image_ocr.txt` - Complete text
- `image_ocr_confidence.txt` - Confidence details

### Example 6: JSON Mode Output

```bash
# Output JSON to console
swift scripts/ocr_vision_pro.swift image.png -j

# Save JSON to file
swift scripts/ocr_vision_pro.swift image.png -j > result.json

# Parse JSON with jq
swift scripts/ocr_vision_pro.swift image.png -j | jq '.blocks[] | select(.confidence < 0.8)'
```

**Note**: JSON mode and text mode (`-t`) are mutually exclusive. JSON mode outputs to stdout only.

## Output Format

The script supports two mutually exclusive output modes:

### Text Mode (Default, `-t`)

#### Console Output (without `-o` or `-t <file>`)

Outputs only the extracted text:
```
[Extracted text content]
```

When not using `-j`, confidence details are also displayed:
```
=== 置信度详情 ===

总识别块数: 25
平均置信度: 0.85

--- 逐块详情 ---

[1] Text content
    置信度: 0.95
    位置: x=0.10, y=0.20, w=0.30, h=0.05

--- 低置信度警告 (< 0.8) ---
[3] "Some text" - 置信度: 0.50
```

#### File Output (`-o` option)

Creates two separate files:
- `<output>.txt` - Complete extracted text (pure text, no formatting)
- `<output>_confidence.txt` - Confidence details

#### File Output (`-t` and `-c` options)

Creates separate files for text and confidence:
```bash
swift scripts/ocr_vision_pro.swift image.png -t text.txt -c details.txt
```

### JSON Mode (`-j`)

Outputs complete raw information as JSON to stdout (no file output in JSON mode).

**JSON Structure:**
```json
{
  "imagePath": "/path/to/image.png",
  "totalBlocks": 25,
  "averageConfidence": 0.85,
  "blocks": [
    {
      "index": 1,
      "text": "recognized text",
      "confidence": 0.95,
      "boundingBox": {
        "x": 0.10,
        "y": 0.20,
        "width": 0.30,
        "height": 0.05
      }
    }
  ]
}
```

**Note**: JSON mode and text mode are mutually exclusive. JSON mode outputs to stdout only.

## Understanding Confidence Scores

| Confidence Range | Interpretation |
|------------------|----------------|
| 0.9 - 1.0 | Very high confidence |
| 0.7 - 0.9 | High confidence |
| 0.5 - 0.7 | Medium confidence (may need verification) |
| < 0.5 | Low confidence (likely misrecognized) |

**Note**: 
- Bounding box coordinates are normalized (0.0 - 1.0) relative to image dimensions
- Low confidence blocks (< 0.8) are highlighted in the warning section

## Supported Image Formats

- **PNG** (.png)
- **JPEG** (.jpg, .jpeg)
- **TIFF** (.tiff, .tif)
- **BMP** (.bmp)
- **PDF** (.pdf) - first page only

## Troubleshooting

### Issue: "文件不存在" (File does not exist)

**Cause**: Incorrect file path
**Solution**: 
- Use absolute path: `/Users/vector/Desktop/image.png`
- Or expand tilde: `~/Desktop/image.png`
- Verify file exists: `ls -la <path>`

### Issue: "无法加载图片" (Cannot load image)

**Cause**: Unsupported image format or corrupted file
**Solution**:
- Convert to supported format (PNG or JPEG recommended)
- Verify file is not corrupted

### Issue: Low Recognition Accuracy

**Cause**: Incorrect language setting or low image quality
**Solution**:
- Specify correct language: `-l zh-Hans,en`
- Use precise mode (default, do not use `-f`)
- Improve image quality (higher resolution, better lighting)
- Ensure text is not rotated or skewed
- Check low confidence warnings in output

### Issue: Missing Text in Results

**Cause**: Text may be too small, blurry, or in unsupported language
**Solution**:
- Increase image resolution
- Crop image to focus on text area
- Verify language is supported and specified correctly

## Performance Considerations

| Image Size | Precise Mode | Fast Mode |
|------------|--------------|-----------|
| < 1 MB | ~2-5 seconds | ~1-2 seconds |
| 1-5 MB | ~5-10 seconds | ~2-5 seconds |
| > 5 MB | ~10-30 seconds | ~5-10 seconds |

**Tips**:
- Resize large images before OCR for faster processing
- Use fast mode (`-f`) for quick preview
- Process images in batch during off-hours

## System Requirements

> ⚠️ **Platform**: macOS only (not compatible with Linux, Windows, or other OS)

- **Operating System**: macOS 10.15 (Catalina) or later
- **Framework**: Vision + PDFKit + Core Graphics (pre-installed on macOS)
- **Swift**: Pre-installed on macOS (no need to install separately)
- **Disk Space**: Minimal (scripts are < 10 KB each)

## Notes

1. **Privacy**: All processing is done locally on your Mac. No data is sent to the internet.
2. **Language Download**: Some languages may require downloading language data on first use (system will prompt).
3. **Handwriting**: The Vision framework is optimized for printed text. Handwriting recognition may have lower accuracy.
4. **Complex Layouts**: Documents with multiple columns, tables, or unusual layouts may require post-processing to reorder text correctly.
5. **Separated Output**: The new output format separates pure text from metadata, making it easier to use the extracted text directly.

## References

- [Apple Vision Framework Documentation](https://developer.apple.com/documentation/vision)
- [VNRecognizeTextRequest](https://developer.apple.com/documentation/vision/vnrecognizetextrequest)

## PDF OCR

> ⚠️ **macOS Only** - PDF OCR also requires macOS 10.15+ with PDFKit framework.

This skill also supports extracting text from PDF files using the `pdf_ocr.swift` script, which uses PDFKit to render PDF pages to images and then applies Vision framework OCR.

### Quick Start

**Basic usage (all pages):**
```bash
swift scripts/pdf_ocr.swift document.pdf
```

**Specify pages:**
```bash
# Single page
swift scripts/pdf_ocr.swift document.pdf -p 1

# Multiple pages
swift scripts/pdf_ocr.swift document.pdf -p 1,3,5

# Page range
swift scripts/pdf_ocr.swift document.pdf -p 1-5
```

**JSON mode:**
```bash
swift scripts/pdf_ocr.swift document.pdf -p 1 -j
```

### Page Specification Formats

The `-p` option supports multiple formats:
- **Single page**: `1`
- **Multiple pages**: `1,3,5`
- **Page range**: `1-5`
- **Combination**: `1,3-5,8-10`

### Output Modes (Mutually Exclusive)

#### Text Mode (Default, `-t`)

Outputs extracted text by page:
```
=== 第 1 页 ===

[Extracted text content]

=== 第 2 页 ===

[Extracted text content]
```

#### JSON Mode (`-j`)

Outputs complete raw information as JSON to stdout:
```json
{
  "pdfPath": "/path/to/document.pdf",
  "totalPages": 23,
  "processedPages": 2,
  "pages": [
    {
      "pageNumber": 1,
      "blockCount": 5,
      "averageConfidence": 0.56,
      "text": "page text content",
      "blocks": [...]
    }
  ]
}
```

**PDF JSON Fields:**
- `pdfPath`: Path to the PDF file
- `totalPages`: Total number of pages in PDF
- `processedPages`: Number of pages processed
- `pages`: Array of page results
  - `pageNumber`: Page number (1-based)
  - `blockCount`: Number of text blocks recognized
  - `averageConfidence`: Average confidence score
  - `text`: Full text of the page
  - `blocks`: Array of text blocks with index, text, confidence, boundingBox

### Command-Line Options (PDF OCR)

| Option | Description |
|--------|-------------|
| `-h`, `--help` | Show help information |
| `-t`, `--text` | Text mode (default, output only extracted text) |
| `-j`, `--json` | JSON mode (output complete raw info as JSON) |
| `-p`, `--pages <pages>` | Specify pages to process (default: all pages) |
| `-l`, `--language <lang>` | Specify recognition language (comma-separated) |
| `-f`, `--fast` | Use fast mode (default: precise mode) |

**Note**: `-t` (text mode) and `-j` (JSON mode) are mutually exclusive. JSON mode outputs to stdout only.

### Supported Languages

Same as image OCR: `zh-hans`, `zh-hant`, `en`, `ja`, `ko`, `fr`, `de`, `es`, `it`, `pt`, `ru`

**Default**: `zh-hans,zh-hant,en`

### Examples

#### Example 1: Extract All Pages
```bash
swift scripts/pdf_ocr.swift document.pdf
```

#### Example 2: Extract Specific Pages
```bash
swift scripts/pdf_ocr.swift document.pdf -p 1,3,5
```

#### Example 3: Extract Page Range
```bash
swift scripts/pdf_ocr.swift document.pdf -p 1-5
```

#### Example 4: JSON Mode Output
```bash
# Output JSON to console
swift scripts/pdf_ocr.swift document.pdf -p 1 -j

# Save JSON to file
swift scripts/pdf_ocr.swift document.pdf -j > result.json
```

#### Example 5: Fast Mode for Quick Preview
```bash
swift scripts/pdf_ocr.swift document.pdf -p 1 -f
```

### Troubleshooting (PDF OCR)

#### Issue: "无法加载 PDF 文件"
**Cause**: Incorrect file path or corrupted PDF file
**Solution**:
- Use absolute path: `/Users/vector/Documents/document.pdf`
- Verify file exists: `ls -la <path>`
- Check if PDF is password-protected

#### Issue: Poor Recognition Accuracy on PDF
**Cause**: Low resolution PDF or scanned PDF with poor quality
**Solution**:
- Use precise mode (default, do not use `-f`)
- Specify correct language: `-l zh-hans,en`
- For scanned PDFs, try increasing resolution before OCR

#### Issue: Incorrect Page Numbers
**Cause**: PDF page numbering may not start from 1
**Solution**:
- The script uses actual page indices (1-based)
- Check PDF page count first: `mdls -name kMDItemNumberOfPages document.pdf`

### System Requirements (PDF OCR)

> ⚠️ **Platform**: macOS only

- **Operating System**: macOS 10.15+ (Catalina or later)
- **Framework**: PDFKit + Vision (pre-installed on macOS)
- **Swift**: Pre-installed on macOS

### Notes (PDF OCR)

1. **Platform**: macOS only - requires macOS 10.15+ with PDFKit and Vision frameworks
2. **Privacy**: All processing is done locally on your Mac. No data is sent to the internet.
3. **Page Rendering**: PDF pages are rendered to images at their native resolution before OCR.
4. **Large PDFs**: Processing many pages may take time. Use `-f` (fast mode) for quick preview.
5. **Password-Protected PDFs**: Not currently supported. Remove password protection before OCR.

## References

- [Apple PDFKit Documentation](https://developer.apple.com/documentation/pdfkit)
- [Apple Vision Framework Documentation](https://developer.apple.com/documentation/vision)
