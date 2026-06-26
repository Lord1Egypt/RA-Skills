---
name: local-ocr
description: "[macOS only] Use this skill when the user requests OCR (Optical Character Recognition), image/PDF text extraction. Uses macOS native Vision/PDFKit frameworks. Triggers: '识别图片', 'OCR', '提取图片文字', '提取PDF文字', '识别PDF', 'extract text from image', 'PDF OCR'."
---

# Local OCR (macOS Only)

## Overview

⚠️ **Platform Requirement**: This skill is **macOS only**. It requires macOS 10.15+ (Catalina or later) and uses macOS native frameworks:

- **Vision framework** - For OCR text recognition
- **PDFKit framework** - For PDF processing
- **Core Graphics** - For image rendering

This skill provides OCR (Optical Character Recognition) capabilities using macOS native Vision framework. It extracts text from images and PDFs without requiring any third-party libraries or internet connection.

## Platform Requirements

⚠️ **macOS Only** - This skill cannot run on Linux, Windows, or other operating systems.

**Required:**
- macOS 10.15+ (Catalina or later)
- Vision framework (pre-installed on macOS)
- PDFKit framework (pre-installed on macOS)

**Why macOS Only?**
- Uses `Vision` framework for OCR (macOS/iOS only)
- Uses `PDFKit` framework for PDF processing (macOS/iOS only)
- Uses `AppKit`/`Core Graphics` for image handling (macOS only)

## When to Use This Skill

Trigger this skill when the user:
- Requests OCR or image text extraction
- Mentions extracting text from images, screenshots, PDF files, or scanned documents
- Uses keywords like: "识别图片", "OCR", "提取文字", "提取PDF文字", "识别PDF", "extract text from image", "PDF OCR"
- Provides an image file or PDF file and asks to read or extract its content

## Core Capabilities

### 1. Text Extraction from Images

Use `scripts/ocr_vision_pro.swift` for comprehensive OCR with the following features:
- Multi-language support (Chinese, English, Japanese, Korean, and more)
- **Two output modes** (mutually exclusive):
  - **Text Mode** (`-t`): Output only extracted text (default)
  - **JSON Mode** (`-j`): Output complete raw info including text, position, and confidence as JSON
- Confidence scores for each detected text block
- Bounding box information (text position in image)
- Output to console or file
- Precise or fast recognition modes

**Basic usage:**
```bash
swift scripts/ocr_vision_pro.swift <image_path>
```

**With options:**
```bash
swift scripts/ocr_vision_pro.swift <image_path> -l zh-Hans,en -o output.txt -f
```

### 2. Text Extraction from PDF Files

Use `scripts/pdf_ocr.swift` to extract text from PDF files with the following features:
- Extract text from specific pages or all pages
- Support page range specification (e.g., `1-5`, `1,3,5`)
- **Two output modes** (mutually exclusive):
  - **Text Mode** (`-t`): Output only extracted text (default)
  - **JSON Mode** (`-j`): Output complete raw info as JSON
- Same multi-language support as image OCR
- Precise or fast recognition modes

**Basic usage (all pages):**
```bash
swift scripts/pdf_ocr.swift <pdf_path>
```

**With page specification:**
```bash
# Single page
swift scripts/pdf_ocr.swift document.pdf -p 1

# Multiple pages
swift scripts/pdf_ocr.swift document.pdf -p 1,3,5

# Page range
swift scripts/pdf_ocr.swift document.pdf -p 1-5

# JSON mode
swift scripts/pdf_ocr.swift document.pdf -p 1 -j
```

### 3. Output Modes (Mutually Exclusive)

The script supports two output modes that cannot be used simultaneously:

#### Text Mode (Default, `-t`)
Outputs only the extracted text:
- Console output: Pure text
- File output (`-o` or `-t`): Saves text to file, optionally with separate confidence file

#### JSON Mode (`-j`)
Outputs complete raw information as JSON:
- Contains: image path, total blocks, average confidence, and per-block details
- Per-block info: index, text, confidence, bounding box (x, y, width, height)
- Outputs to stdout only (no file output options in JSON mode)

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

### 4. Supported File Formats

**Image Formats (ocr_vision_pro.swift):**
- PNG (.png)
- JPEG (.jpg, .jpeg)
- TIFF (.tiff, .tif)
- BMP (.bmp)

**PDF Format (pdf_ocr.swift):**
- PDF (.pdf) - support single page, multiple pages, or page ranges
- Specify pages with `-p` option: `1`, `1,3,5`, or `1-5`

### 4. Command-Line Options

| Option | Description |
|--------|-------------|
| `-h`, `--help` | Show help information |
| `-t`, `--text` | Text mode (default, output only extracted text) |
| `-j`, `--json` | JSON mode (output complete raw info as JSON) |
| `-l`, `--language <lang>` | Specify recognition language (comma-separated) |
| `-o`, `--output <file>` | Output text to file, auto-generate confidence file (`<file>_confidence.txt`) |
| `-t`, `--text <file>` | Output only complete text to specified file (text mode) |
| `-c`, `--confidence <file>` | Output only confidence details to specified file (text mode) |
| `-f`, `--fast` | Use fast mode (default: precise mode) |

**Note**: `-t` (text mode) and `-j` (JSON mode) are mutually exclusive. JSON mode outputs to stdout only.

**Supported languages:**
- `zh-Hans` - Simplified Chinese
- `zh-Hant` - Traditional Chinese
- `en` - English
- `ja` - Japanese
- `ko` - Korean
- `fr` - French
- `de` - German
- `es` - Spanish
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian

## Workflow

### Step 1: Identify the Image Path

When the user requests OCR:
1. Ask for the image path if not provided
2. Accept common path formats: absolute paths, ~/path, or relative paths
3. Validate that the file exists before proceeding

### Step 2: Determine Recognition Parameters

Based on user request or context:
1. **Language**: Default to `zh-Hans,en` for Chinese users, or `en` for English users
2. **Mode**: Use precise mode (default) for accuracy, fast mode (`-f`) for quick preview
3. **Output**: Ask if user wants results saved to file (`-o` option)

### Step 3: Execute OCR

Run the OCR script with appropriate parameters:

```bash
swift scripts/ocr_vision_pro.swift "<image_path>" -l zh-Hans,en
```

For saving to separate files (recommended):
```bash
swift scripts/ocr_vision_pro.swift "<image_path>" -o "<output>"
```

This automatically creates two files:
- `<output>.txt` - Complete extracted text (pure text, no formatting)
- `<output>_confidence.txt` - Confidence details with statistics and per-block info

For separate text and confidence files with custom names:
```bash
swift scripts/ocr_vision_pro.swift "<image_path>" -t "text.txt" -c "confidence.txt"
```

### Step 4: Present Results

After OCR completes:
1. Display the extracted text to the user
2. If saved to file, inform the user of the output file path
3. Ask if user wants to:
   - Correct misrecognized characters
   - Process another image
   - Save results in a different format

### Step 5: PDF Processing (if PDF file)

When processing a PDF file:
1. **Identify PDF path and pages**:
   - Ask for PDF path if not provided
   - Ask which pages to process (default: all pages)
   - Support formats: `1`, `1,3,5`, or `1-5`

2. **Determine recognition parameters**:
   - Language: Default to `zh-hans,zh-hant,en`
   - Mode: Precise (default) or fast (`-f`)
   - Output: Text mode (default) or JSON mode (`-j`)

3. **Execute PDF OCR**:
```bash
# All pages
swift scripts/pdf_ocr.swift "<pdf_path>"

# Specific pages
swift scripts/pdf_ocr.swift "<pdf_path>" -p 1,3,5

# Page range
swift scripts/pdf_ocr.swift "<pdf_path>" -p 1-5

# JSON mode
swift scripts/pdf_ocr.swift "<pdf_path>" -p 1 -j
```

4. **Present results**:
   - Text mode: Display text by page
   - JSON mode: Output complete JSON to stdout
   - Inform user of output format and options

## Output Format

The script supports two mutually exclusive output modes:

### Text Mode (Default, `-t`)

Outputs only the extracted text.

#### Console Output (without `-o` or `-t <file>`):
```
[Extracted text content]
```

#### File Output (`-o` option):
Creates `<output>.txt` with pure text.

#### With Confidence Details (console, when not using `-j`):
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

#### File Output with Confidence (`-o` option):
- `<output>.txt` - Complete extracted text
- `<output>_confidence.txt` - Confidence details

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

**Fields:**
- `imagePath`: Path to the processed image
- `totalBlocks`: Total number of recognized text blocks
- `averageConfidence`: Average confidence score (0.0 - 1.0)
- `blocks`: Array of recognized text blocks
  - `index`: Block index (1-based)
  - `text`: Recognized text content
  - `confidence`: Confidence score (0.0 - 1.0)
  - `boundingBox`: Normalized bounding box coordinates (0.0 - 1.0)

## Tips and Best Practices

1. **macOS Only**: This skill requires macOS. It will not work on Linux, Windows, or other operating systems.
2. **Image Quality**: Higher resolution images produce better results
3. **Language Specification**: Always specify language for better accuracy
4. **Precise vs Fast**: Use precise mode for final results, fast mode for testing
5. **Batch Processing**: For multiple images, use shell loop:
   ```bash
   for img in *.png; do
       swift scripts/ocr_vision_pro.swift "$img" -o "${img%.png}.txt"
   done
   ```
6. **Confidence Threshold**: Results with confidence < 0.5 may need manual verification

## References

For detailed usage instructions and examples, load `references/usage.md`.

## Resources

### scripts/

- `ocr_vision_pro.swift` - Enhanced OCR script for images with full feature support
- `ocr_vision.swift` - Basic OCR script for simple use cases
- `pdf_ocr.swift` - PDF OCR script for extracting text from PDF files

### references/

- `usage.md` - Comprehensive usage guide with examples
