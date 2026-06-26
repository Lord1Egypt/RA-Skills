# Pillow Skill Usage Examples

English | [简体中文](EXAMPLES_CN.md)

Comprehensive examples for using the Pillow image processing skill.

## Example 1: Basic Image Editing

### Resize Image
```bash
# Resize to specific width (height auto-calculated)
python scripts/image_editor.py portrait.jpg resized.jpg --width 600

# Resize to specific dimensions (ignore aspect ratio)
python scripts/image_editor.py photo.jpg stretched.jpg \
    --width 800 --height 600 --no-aspect
```

### Crop Image
```bash
# Crop square from center
python scripts/image_editor.py photo.jpg cropped.jpg \
    --crop 200 200 800 800

# Extract specific region
python scripts/image_editor.py screenshot.png section.png \
    --crop 0 0 1920 400
```

### Rotate and Flip
```bash
# Rotate 90 degrees
python scripts/image_editor.py photo.jpg rotated.jpg --rotate 90

# Flip horizontally (mirror)
python scripts/image_editor.py selfie.jpg mirrored.jpg --flip horizontal

# Combine rotation and flip
python scripts/image_editor.py input.jpg output.jpg \
    --rotate 45 --flip vertical
```

## Example 2: Color Adjustments

### Brightness and Contrast
```bash
# Brighten dark photo
python scripts/image_editor.py dark.jpg bright.jpg --brightness 1.5

# Increase contrast
python scripts/image_editor.py flat.jpg contrasted.jpg --contrast 1.3

# Reduce brightness and increase contrast
python scripts/image_editor.py overexposed.jpg fixed.jpg \
    --brightness 0.8 --contrast 1.2
```

### Color Saturation
```bash
# Convert to grayscale
python scripts/image_editor.py color.jpg gray.jpg --color 0.0

# Boost colors
python scripts/image_editor.py dull.jpg vivid.jpg --color 1.5

# Subtle saturation reduction
python scripts/image_editor.py saturated.jpg natural.jpg --color 0.9
```

### Sharpness
```bash
# Sharpen image
python scripts/image_editor.py blurry.jpg sharp.jpg --sharpness 2.0

# Slight sharpening
python scripts/image_editor.py photo.jpg enhanced.jpg --sharpness 1.3
```

## Example 3: Filters

### Apply Built-in Filters
```bash
# Blur effect
python scripts/image_editor.py sharp.jpg blurred.jpg --filter blur

# Edge detection
python scripts/image_editor.py photo.jpg edges.jpg --filter edge_enhance

# Artistic emboss effect
python scripts/image_editor.py photo.jpg embossed.jpg --filter emboss

# Sharpen filter
python scripts/image_editor.py soft.jpg sharpened.jpg --filter sharpen
```

## Example 4: Format Conversion

### Convert Between Formats
```bash
# PNG to JPEG
python scripts/image_editor.py image.png image.jpg --format JPEG --quality 95

# JPEG to PNG (lossless)
python scripts/image_editor.py photo.jpg photo.png --format PNG

# Convert to WebP (modern format)
python scripts/image_editor.py image.jpg image.webp --format WEBP --quality 90
```

## Example 5: Batch Processing

### Create Thumbnails for Gallery
```bash
# Generate 300x300 thumbnails for all images
python scripts/batch_processor.py ./photos ./thumbnails \
    --thumbnail 300 300 \
    --workers 8
```

### Batch Resize
```bash
# Resize all images to 1920x1080
python scripts/batch_processor.py ./originals ./resized \
    --resize 1920 1080

# Resize specific file types
python scripts/batch_processor.py ./images ./output \
    --pattern "*.jpg" \
    --resize 800 600
```

### Batch Format Conversion
```bash
# Convert all PNGs to JPEG
python scripts/batch_processor.py ./pngs ./jpegs \
    --format JPEG \
    --quality 90

# Convert to grayscale
python scripts/batch_processor.py ./color ./bw \
    --grayscale
```

### Batch Brightness Adjustment
```bash
# Brighten all images in a directory
python scripts/batch_processor.py ./dark_photos ./brightened \
    --brightness 1.3
```

## Example 6: Watermarking

### Text Watermarks
```bash
# Simple copyright text
python scripts/watermark.py photo.jpg marked.jpg \
    --text "© 2026 John Doe" \
    --position bottom-right

# Centered watermark
python scripts/watermark.py image.jpg output.jpg \
    --text "CONFIDENTIAL" \
    --position center \
    --font-size 72 \
    --opacity 100

# Custom color and position
python scripts/watermark.py photo.jpg branded.jpg \
    --text "MyBrand" \
    --position top-left \
    --color red \
    --font-size 48 \
    --margin 20
```

### Logo Watermarks
```bash
# Company logo in corner
python scripts/watermark.py product.jpg branded.jpg \
    --image logo.png \
    --position bottom-right \
    --scale 0.15 \
    --opacity 180

# Large center watermark
python scripts/watermark.py image.jpg watermarked.jpg \
    --image watermark.png \
    --position center \
    --scale 0.4 \
    --opacity 128

# Subtle top-right logo
python scripts/watermark.py photo.jpg output.jpg \
    --image brand_icon.png \
    --position top-right \
    --scale 0.1 \
    --opacity 200 \
    --margin 15
```

## Example 7: Image Information

### Extract Metadata
```bash
# Display all image information
python scripts/image_info.py photo.jpg

# Save info as JSON
python scripts/image_info.py image.jpg -o info.json --format json

# Batch extract info for multiple images
for img in *.jpg; do
    python scripts/image_info.py "$img" -o "${img%.jpg}_info.json" --format json
done
```

## Example 8: Combined Workflows

### Complete Photo Enhancement
```bash
# Step 1: Rotate if needed
python scripts/image_editor.py raw.jpg rotated.jpg --rotate 90

# Step 2: Crop to remove borders
python scripts/image_editor.py rotated.jpg cropped.jpg \
    --crop 50 50 1850 1350

# Step 3: Enhance colors and sharpness
python scripts/image_editor.py cropped.jpg enhanced.jpg \
    --brightness 1.1 \
    --contrast 1.2 \
    --color 1.15 \
    --sharpness 1.3

# Step 4: Add watermark
python scripts/watermark.py enhanced.jpg final.jpg \
    --text "© 2026 Photography Studio" \
    --position bottom-right \
    --opacity 150

# Step 5: Optimize for web
python scripts/image_editor.py final.jpg web_ready.jpg \
    --width 1200 \
    --quality 85
```

### Batch Product Photography Workflow
```bash
# 1. Batch crop all products
python scripts/batch_processor.py ./raw_products ./cropped \
    --resize 2000 2000

# 2. Add watermarks to all
for img in ./cropped/*.jpg; do
    python scripts/watermark.py "$img" "./watermarked/$(basename $img)" \
        --image company_logo.png \
        --position bottom-right \
        --scale 0.12 \
        --opacity 180
done

# 3. Create multiple sizes
python scripts/batch_processor.py ./watermarked ./large \
    --resize 1200 1200 \
    --quality 90

python scripts/batch_processor.py ./watermarked ./medium \
    --thumbnail 600 600 \
    --quality 85

python scripts/batch_processor.py ./watermarked ./small \
    --thumbnail 300 300 \
    --quality 80
```

### Social Media Image Prep
```bash
# Instagram square format (1080x1080)
python scripts/image_editor.py photo.jpg instagram.jpg \
    --crop 0 200 1080 1280 \
    --resize 1080 1080 \
    --brightness 1.1 \
    --color 1.2 \
    --sharpen 1.2 \
    --quality 95

# Facebook cover photo (820x312)
python scripts/image_editor.py wide.jpg fb_cover.jpg \
    --resize 820 312 --no-aspect \
    --quality 90

# Twitter header (1500x500)
python scripts/image_editor.py banner.jpg twitter_header.jpg \
    --resize 1500 500 --no-aspect \
    --quality 92
```

## Example 9: Advanced Techniques

### HDR-like Effect
```bash
# Create pseudo-HDR look
python scripts/image_editor.py photo.jpg hdr_look.jpg \
    --contrast 1.4 \
    --color 1.3 \
    --sharpness 1.5 \
    --filter detail
```

### Vintage Effect
```bash
# Create vintage/faded look
python scripts/image_editor.py modern.jpg vintage.jpg \
    --color 0.7 \
    --contrast 0.9 \
    --brightness 1.1
```

### Create Thumbnail Grid (requires montage or custom script)
```bash
# First create individual thumbnails
python scripts/batch_processor.py ./photos ./grid_thumbs \
    --thumbnail 200 200
```

## Tips and Best Practices

### 1. Always Backup Originals
```bash
# Create backup before processing
cp -r ./originals ./originals_backup
```

### 2. Test on One Image First
```bash
# Test processing on single image
python scripts/image_editor.py test.jpg test_output.jpg --brightness 1.3

# If satisfied, batch process
python scripts/batch_processor.py ./images ./output --brightness 1.3
```

### 3. Use Appropriate Quality Settings
- **Web photos**: quality 80-85
- **Print photos**: quality 95-100
- **Thumbnails**: quality 75-80

### 4. Choose Right Format
- **Photos**: JPEG
- **Graphics/logos**: PNG
- **Transparency needed**: PNG or WebP
- **Modern web**: WebP with JPEG fallback

### 5. Preserve EXIF Data
Extract info before processing if needed:
```bash
python scripts/image_info.py original.jpg -o metadata.json --format json
```

## Troubleshooting

### Issue: Image Quality Degradation
```bash
# Use higher quality setting
--quality 95

# Avoid multiple compressions (process once with all operations)
```

### Issue: Slow Batch Processing
```bash
# Increase worker threads
--workers 8
```

### Issue: Memory Errors with Large Images
```bash
# Process images in smaller batches
# Or resize first before other operations
```

See [SKILL.md](SKILL.md) for complete documentation and [references/](references/) for detailed Pillow guides.
