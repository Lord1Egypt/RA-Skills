---
name: pdf-to-ppt
description: |
  Convert PDF files to PowerPoint presentations via intermediate image rendering.
  Created collaboratively with 贾维斯 (AI assistant) by Hugo.
  Use when working with PDF documents that are primarily visual (e.g., design drawings, presentations scanned to PDF, etc.) and preserves the visual layout faithfully.
---

# PDF to PPT Conversion Skill

This skill converts PDF files into PowerPoint presentations by first rendering each PDF page as a high-quality image, then assembling those images into a PPT where each image fills a slide. This approach works well for PDFs that are primarily visual (e.g., design drawings, presentations scanned to PDF, etc.) and preserves the visual layout faithfully.

## When to Use

Use this skill when you need to:
- Convert a PDF document into an editable PowerPoint presentation.
- Preserve the exact visual layout of each PDF page (text, images, vectors) as slide backgrounds.
- Work with PDFs that are not easily editable via direct text extraction (e.g., complex layouts, designer files).
- Batch-convert multiple PDFs to PPT format.

## Core Rules

### 1. Input PDF Requirements
- The PDF should be text-based or vector-based for best results. Scanned PDFs will be converted as images (which is still valid for this skill).
- Ensure the PDF is not password-protected, or provide the password via environment variable if supported.

### 2. Image Rendering Quality
- The skill renders PDF pages to images using a configurable zoom factor (default 2.0, which yields ~144 DPI from default 72 DPI).
- Higher zoom values increase image quality and file size but improve text readability in the resulting PPT.
- For text-heavy PDFs where you need selectable text in PPT, consider direct PDF→PPT conversion tools (like LibreOffice) instead.

### 3. Output PPT Characteristics
- Each PDF page becomes one slide.
- Slide size defaults to 16:9 (width=13.33in, height=7.5in) but can be customized.
- Images are stretched to fill the slide; aspect ratio is not locked (to ensure full coverage). If aspect ratio preservation is critical, edit the script to center and crop.
- The generated PPT uses a blank layout for each slide, placing the image as a shape that covers the entire slide.

### 4. Dependencies
- Python packages: `PyMuPDF` (fitz) and `python-pptx`.
- These are installed automatically when the skill is first used via the provided install command, or you can install them manually.

## Installation

To install this skill from a local path (after copying to your skills folder), you can use:

```bash
clawhub install /path/to/pdf-to-ppt
```

Or if you have cloned the skill repository:

```bash
clawhub install pdf-to-ppt
```

## Usage

### Basic Conversion

```bash
python3 scripts/pdf_to_ppt.py input.pdf
```

This will:
- Create an `images/` subdirectory next to the input PDF (or use a specified directory).
- Render each PDF page to a PNG image in that folder.
- Generate a PPT file with the same base name as the input PDF, appended with `.pptx`, in the same directory as the input.

### Advanced Options

```bash
python3 scripts/pdf_to_ppt.py input.pdf \
    --img-dir /path/to/images \
    --output output.pptx \
    --zoom 3.0 \
    --slide-width-in 16 \
    --slide-height-in 9 \
    --format png
```

#### Arguments:
- `input.pdf`: Path to the source PDF file (required).
- `--img-dir DIR`: Directory to store intermediate images. If not provided, defaults to `<pdf_dir>/images/`.
- `--output PPTX`: Path for the output PPT file. If not provided, defaults to `<pdf_basename>.pptx` in the same directory as input PDF.
- `--zoom ZOOM`: Zoom factor for rendering (default 2.0). Higher = higher DPI.
- `--slide-width-in INCHES`: Width of slides in inches (default 13.33 for 16:9 at 7.5in height).
- `--slide-height-in INCHES`: Height of slides in inches (default 7.5).
- `--format {png,jpg}`: Image format for intermediates (default png).

### Example: Convert with Custom Settings

```bash
python3 scripts/pdf_to_ppt.py report.pdf \
    --img-dir ./tmp/imgs \
    --output ./presentation.pptx \
    --zoom 2.5 \
    --format jpg
```

## Workflow Tips

1. **Check Image Quality**: After conversion, open the generated PPT and review a few slides. If text appears blurry, increase `--zoom`.
2. **File Size**: Higher zoom and PNG format increase both image and final PPT size. Use JPG for smaller files if slight compression artifacts are acceptable.
3. **Post-Processing**: The PPT is fully editable in PowerPoint. You can:
   - Add text boxes, shapes, or annotations over the image backgrounds.
   - Replace images with higher-quality versions if needed.
   - Extract individual images via “Save as Picture” if required.
4. **Batch Processing**: Wrap the script in a loop for multiple PDFs:
   ```bash
   for pdf in *.pdf; do
       python3 scripts/pdf_to_ppt.py "$pdf"
   done
   ```

## Troubleshooting

- **ModuleNotFoundError for fitz or pptx**: Ensure dependencies are installed. Run:
  ```bash
  pip install --break-system-packages PyMuPDF python-pptx
  ```
  (Add `--break-system-packages` if using system Python in a restricted environment.)
- **Empty Images**: Verify the PDF is not empty and that PyMuPDF can open it. Try opening the PDF in a viewer to confirm it has content.
- **Memory Issues**: Very large PDFs with high zoom may consume significant RAM. Process in batches or reduce zoom.

## Related Skills

Consider combining with:
- `pdf-tools` — for extracting text, merging, splitting PDFs before conversion.
- `powerpoint-pptx` — for best practices on editing and styling the resulting PPT.
- `images` — if you need to process the intermediate images further.

## Feedback

If you find this skill useful, consider starring it on ClawHub: `clawhub star pdf-to-ppt`

For issues or enhancements, please refer to the skill’s source repository.

---
_This skill was created to automate PDF → image → PPT conversion for visual-rich documents._