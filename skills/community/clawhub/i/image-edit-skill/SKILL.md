---
name: pillow-skill
description: Expert Pillow (PIL) skill for image processing, manipulation, and analysis. Use this skill for image editing, batch processing, watermarking, format conversion, and extracting image information. Provides executable scripts and comprehensive reference documentation.
---

# Pillow Image Processing Skill

English | [简体中文](SKILL_CN.md)

This skill provides comprehensive image processing capabilities through executable scripts and reference documentation for Pillow (PIL).

## When to Use This Skill

Activate this skill when the user requests:

- Image editing operations (resize, crop, rotate, color adjustments)
- Batch processing multiple images
- Adding watermarks (text or image)
- Image format conversions
- Extracting image metadata or EXIF data
- Applying filters or effects
- Creating thumbnails

## Core Capabilities

### 1. Image Editor (`scripts/image_editor.py`)

Edit single images with various operations:

**Usage:**
```bash
python scripts/image_editor.py input.jpg output.jpg [options]
```

**Options:**
- `--width WIDTH` / `--height HEIGHT`: Resize dimensions
- `--no-aspect`: Ignore aspect ratio when resizing
- `--crop X Y WIDTH HEIGHT`: Crop rectangle
- `--rotate DEGREES`: Rotate image
- `--flip {horizontal,vertical}`: Flip image
- `--brightness FACTOR`: Adjust brightness (0.0-2.0)
- `--contrast FACTOR`: Adjust contrast (0.0-2.0)
- `--color FACTOR`: Adjust color saturation (0.0-2.0)
- `--sharpness FACTOR`: Adjust sharpness (0.0-2.0)
- `--filter {blur,contour,detail,edge_enhance,emboss,sharpen,smooth}`: Apply filter
- `--format FORMAT`: Output format (JPEG, PNG, etc.)
- `--quality QUALITY`: JPEG quality (1-100)

**Examples:**
```bash
# Resize maintaining aspect ratio
python scripts/image_editor.py photo.jpg resized.jpg --width 800

# Multiple operations
python scripts/image_editor.py input.jpg output.jpg \
    --crop 100 100 800 600 \
    --rotate 90 \
    --brightness 1.2 \
    --sharpen 1.5
```

### 2. Batch Processor (`scripts/batch_processor.py`)

Process multiple images in parallel:

**Usage:**
```bash
python scripts/batch_processor.py input_dir output_dir [options]
```

**Options:**
- `--pattern PATTERN`: File pattern (e.g., *.jpg)
- `--resize WIDTH HEIGHT`: Resize all images
- `--thumbnail MAX_W MAX_H`: Create thumbnails (maintains aspect)
- `--grayscale`: Convert to grayscale
- `--brightness FACTOR`: Adjust brightness
- `--format FORMAT`: Convert format
- `--quality QUALITY`: JPEG quality
- `--workers N`: Number of parallel workers (default: 4)

**Examples:**
```bash
# Create thumbnails
python scripts/batch_processor.py ./photos ./thumbs --thumbnail 300 300

# Batch convert and resize
python scripts/batch_processor.py ./raw ./processed \
    --resize 1920 1080 \
    --format JPEG \
    --quality 90
```

### 3. Watermark Tool (`scripts/watermark.py`)

Add text or image watermarks:

**Usage:**
```bash
python scripts/watermark.py input.jpg output.jpg --text "TEXT" [options]
python scripts/watermark.py input.jpg output.jpg --image logo.png [options]
```

**Common Options:**
- `--position {top-left,top-right,bottom-left,bottom-right,center}`: Position
- `--opacity 0-255`: Transparency level
- `--margin PIXELS`: Margin from edge

**Text Options:**
- `--font-size SIZE`: Font size
- `--color COLOR`: Text color (white/black/red/etc)

**Image Options:**
- `--scale RATIO`: Watermark scale (0.0-1.0)

**Examples:**
```bash
# Text watermark
python scripts/watermark.py photo.jpg marked.jpg \
    --text "© 2026 Company" \
    --position bottom-right \
    --opacity 128

# Logo watermark
python scripts/watermark.py image.jpg output.jpg \
    --image logo.png \
    --scale 0.2 \
    --position top-left
```

### 4. Image Info (`scripts/image_info.py`)

Extract image metadata and properties:

**Usage:**
```bash
python scripts/image_info.py image.jpg [options]
```

**Options:**
- `--format {text,json}`: Output format
- `--output FILE`: Save to file

**Provides:**
- File information (size, path)
- Image properties (dimensions, format, mode)
- Color information (bands, palette)
- EXIF data (if available)
- Metadata

**Example:**
```bash
# Display info
python scripts/image_info.py photo.jpg

# Save as JSON
python scripts/image_info.py photo.jpg -o info.json --format json
```

## Reference Documentation

### `references/common_operations.md`

Comprehensive Pillow reference covering:
- Opening and saving images
- Resizing and cropping
- Rotation and flipping
- Color adjustments and enhancements
- Filters and effects
- Drawing on images
- Image composition
- Working with channels
- EXIF data handling
- Performance tips

**When to use:** When Claude needs specific Pillow syntax or operation patterns.

### `references/best_practices.md`

Best practices guide covering:
- Format selection (JPEG vs PNG vs WebP)
- Resizing strategies
- Color mode conversion
- Memory management
- Watermarking strategies
- Filter application
- Optimization techniques
- Error handling patterns
- Common workflows

**When to use:** When designing image processing workflows or optimizing performance.

## Workflow Guidelines

### Step 1: Analyze Requirements
- What format is the input image?
- What operations are needed?
- Is it a single image or batch?
- Are there quality requirements?

### Step 2: Choose the Right Tool
- Single image edit → `image_editor.py`
- Multiple images → `batch_processor.py`
- Add watermark → `watermark.py`
- Need info → `image_info.py`

### Step 3: Plan Operations
- Apply operations in logical order
- Consider quality vs file size tradeoffs
- Validate input requirements

### Step 4: Execute and Validate
- Run the script with appropriate options
- Check output quality
- Verify file sizes and formats

## Common Patterns

### Pattern 1: Web Image Optimization
```bash
# Resize and optimize for web
python scripts/image_editor.py large.jpg web.jpg \
    --width 1200 \
    --quality 85 \
    --format JPEG
```

### Pattern 2: Create Image Gallery
```bash
# Generate thumbnails
python scripts/batch_processor.py ./originals ./gallery \
    --thumbnail 400 400 \
    --format JPEG \
    --quality 90
```

### Pattern 3: Brand Images with Watermark
```bash
# Add company logo
python scripts/watermark.py product.jpg branded.jpg \
    --image company_logo.png \
    --position bottom-right \
    --scale 0.15 \
    --opacity 180
```

### Pattern 4: Batch Format Conversion
```bash
# Convert PNG to JPEG
python scripts/batch_processor.py ./pngs ./jpegs \
    --format JPEG \
    --quality 95
```

## Dependencies

```bash
pip install Pillow
```

## Tips for Effective Use

1. **Preserve originals**: Never overwrite source images
2. **Use appropriate formats**: JPEG for photos, PNG for graphics
3. **Optimize quality**: Balance quality and file size
4. **Batch operations**: Use batch processor for multiple images
5. **Check references**: Consult reference docs for advanced operations
6. **Validate inputs**: Check image format and size before processing
7. **Test first**: Try operations on one image before batch processing

## Limitations

- Limited to 2D image processing (no video)
- Some EXIF data may not be preserved in all formats
- Font availability may vary by system
- Very large images may require significant memory
- Advanced photo editing (layers, masks) requires specialized tools

## Troubleshooting

**Import errors**: Ensure Pillow is installed (`pip install Pillow`)
**Font not found**: Watermark script falls back to default font
**Memory errors**: Process large images in smaller batches
**Format errors**: Check input image format compatibility
**RGBA to JPEG**: Script automatically handles RGBA→RGB conversion

For detailed operations and troubleshooting, always refer to `references/common_operations.md` and `references/best_practices.md`.
