# Format Specifications

Detailed specifications for each output format supported by mermaid-cli.

## Format Comparison Summary

| Feature | PNG | SVG | PDF |
|---------|-----|-----|-----|
| **Type** | Raster | Vector | Document |
| **Best For** | Web, documents | Web, scaling | Print, sharing |
| **Scalability** | Limited | Infinite | Page-based |
| **File Size** | Medium | Small | Large |
| **Quality** | Pixel-based | Mathematical | Print-ready |
| **Transparency** | Yes | Yes | Limited |
| **Browser Support** | Universal | Modern browsers | Universal |

## PNG Format

### Technical Details
- **MIME Type**: `image/png`
- **File Extension**: `.png`
- **Compression**: Lossless (DEFLATE)
- **Color Depth**: Up to 48-bit RGB + 16-bit alpha
- **Metadata**: Can store EXIF, XMP, etc.

### Best Practices

#### Resolution and Scaling
```bash
# Standard resolution (96 DPI)
python scripts/export_mermaid_image.py diagram.mmd -s 1.0 -o standard.png

# High resolution for web (192 DPI)
python scripts/export_mermaid_image.py diagram.mmd -s 2.0 -o highres.png

# Print resolution (300 DPI equivalent)
python scripts/export_mermaid_image.py diagram.mmd -s 3.125 -o print.png
```

#### Background Handling
```bash
# Transparent background (default)
python scripts/export_mermaid_image.py diagram.mmd -b transparent -o transparent.png

# White background for documents
python scripts/export_mermaid_image.py diagram.mmd -b white -o white_bg.png

# Custom color
python scripts/export_mermaid_image.py diagram.mmd -b "#f0f0f0" -o gray_bg.png
```

### Use Cases

#### Web Development
```bash
# Optimized for web
python scripts/export_mermaid_image.py diagram.mmd -w 800 -o web.png

# With fallback for older browsers
python scripts/export_mermaid_image.py diagram.mmd -o diagram.png  # Default is fine
```

#### Documentation
```bash
# Standard documentation size
python scripts/export_mermaid_image.py docs/*.mmd -d images/ -s 1.5

# With consistent background
python scripts/export_mermaid_image.py docs/*.mmd -d images/ -b white
```

### Optimization Tips

#### File Size Reduction
```bash
# Optimize with external tools
python scripts/export_mermaid_image.py diagram.mmd -o diagram.png
optipng diagram.png  # Lossless optimization
pngquant diagram.png  # Lossy optimization (smaller)
```

#### Quality vs Size Trade-off
- **High quality**: `-s 2.0` or higher
- **Balanced**: `-s 1.5` (default good for most uses)
- **Small size**: `-s 1.0` with post-optimization

## SVG Format

### Technical Details
- **MIME Type**: `image/svg+xml`
- **File Extension**: `.svg`
- **Format**: XML-based vector graphics
- **Scalability**: Infinite (no quality loss)
- **File Structure**: Human-readable XML

### Best Practices

#### Embedding in Web Pages
```html
<!-- Direct embedding -->
<svg width="800" height="600">
  <!-- SVG content -->
</svg>

<!-- As image -->
<img src="diagram.svg" alt="Diagram" width="800" height="600">

<!-- With CSS styling -->
<style>
  .diagram {
    max-width: 100%;
    height: auto;
  }
</style>
<img src="diagram.svg" class="diagram" alt="Diagram">
```

#### Export Settings
```bash
# Basic SVG export
python scripts/export_mermaid_image.py diagram.mmd -f svg -o diagram.svg

# With specific dimensions
python scripts/export_mermaid_image.py diagram.mmd -f svg -w 800 -H 600 -o sized.svg

# For dark mode websites
python scripts/export_mermaid_image.py diagram.mmd -f svg -t dark -o dark.svg
```

### Advanced SVG Features

#### CSS Styling Control
```css
/* External CSS for SVG */
.diagram {
  stroke-width: 2;
  font-family: 'Segoe UI', sans-serif;
}

/* Override specific elements */
.node rect {
  fill: #f0f8ff;
  stroke: #4a90e2;
}

.edgePath path {
  stroke: #4a90e2;
  marker-end: url(#arrowhead);
}
```

#### Interactive SVGs
```html
<svg onclick="zoomIn()" onmouseover="highlight()">
  <!-- Make SVG interactive -->
</svg>

<script>
function zoomIn() {
  // Add interactivity
}
</script>
```

### Use Cases

#### Responsive Web Design
```bash
# Export for responsive design
python scripts/export_mermaid_image.py diagram.mmd -f svg -o responsive.svg
```

#### High-Quality Printing
```bash
# SVG for high-quality print
python scripts/export_mermaid_image.py diagram.mmd -f svg -o print_quality.svg
```

#### Documentation Systems
```bash
# SVG for documentation (scales with zoom)
python scripts/export_mermaid_image.py docs/*.mmd -f svg -d svg_docs/
```

### Optimization Tips

#### Clean SVG Output
```bash
# Export then optimize
python scripts/export_mermaid_image.py diagram.mmd -f svg -o diagram.svg
svgo diagram.svg  # SVG optimizer
```

#### Embedding Fonts
```css
@import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

:root {
  --mermaid-font-family: 'Inter', sans-serif;
}
```

## PDF Format

### Technical Details
- **MIME Type**: `application/pdf`
- **File Extension**: `.pdf`
- **Format**: Adobe Portable Document Format
- **Pages**: Single-page (by default)
- **Printing**: Print-ready with proper margins

### Best Practices

#### Page Configuration
```bash
# A4 size (210x297mm)
python scripts/export_mermaid_image.py diagram.mmd -f pdf -w 210 -H 297 -o a4.pdf

# Letter size (8.5x11 inches)
python scripts/export_mermaid_image.py diagram.mmd -f pdf -w 215.9 -H 279.4 -o letter.pdf

# Custom size in millimeters
python scripts/export_mermaid_image.py diagram.mmd -f pdf -w 300 -H 200 -o custom.pdf
```

#### Print Optimization
```bash
# High quality for printing
python scripts/export_mermaid_image.py diagram.mmd -f pdf -s 2.0 -o print.pdf

# With white background (most printers)
python scripts/export_mermaid_image.py diagram.mmd -f pdf -b white -o print_ready.pdf

# CMYK color space (professional printing)
# Note: Requires post-processing
```

### Use Cases

#### Technical Documentation
```bash
# Export all diagrams for PDF documentation
for file in diagrams/*.mmd; do
  base=$(basename "$file" .mmd)
  python scripts/export_mermaid_image.py "$file" -f pdf -o "pdf_docs/${base}.pdf"
done
```

#### Presentation Materials
```bash
# Export for PowerPoint/Keynote import
python scripts/export_mermaid_image.py presentation.mmd -f pdf -o slide.pdf

# Batch export for presentation
python scripts/export_mermaid_image.py slides/*.mmd -f pdf -d presentation_pdfs/
```

#### Archival and Sharing
```bash
# High-quality archival
python scripts/export_mermaid_image.py important.mmd -f pdf -s 3.0 -o archive.pdf

# Share via email/cloud
python scripts/export_mermaid_image.py diagram.mmd -f pdf -o share.pdf
```

### Advanced PDF Features

#### Multi-page Support
```bash
# Complex diagram might create multi-page PDF
# Configure via Puppeteer
cat > pdf_config.json << EOF
{
  "format": "A4",
  "margin": {
    "top": "20mm",
    "right": "20mm",
    "bottom": "20mm",
    "left": "20mm"
  },
  "printBackground": true
}
EOF

python scripts/export_mermaid_image.py diagram.mmd -f pdf -C pdf_config.json -o configured.pdf
```

#### Metadata and Security
```bash
# Add metadata (requires post-processing)
python scripts/export_mermaid_image.py diagram.mmd -f pdf -o diagram.pdf
exiftool -Title="Architecture Diagram" -Author="Team" diagram.pdf
```

### Performance Considerations

#### PDF Generation Speed
- **Simple diagrams**: 2-5 seconds
- **Complex diagrams**: 5-15 seconds
- **Batch processing**: Consider parallel processing

#### File Size Management
```bash
# Balance quality and size
python scripts/export_mermaid_image.py diagram.mmd -f pdf -s 1.5 -o balanced.pdf

# For email/quick sharing
python scripts/export_mermaid_image.py diagram.mmd -f pdf -s 1.0 -o small.pdf
```

## Cross-Format Considerations

### Consistent Styling Across Formats
```bash
# Use same theme for all formats
python scripts/export_mermaid_image.py diagram.mmd -t forest -o diagram.png
python scripts/export_mermaid_image.py diagram.mmd -t forest -f svg -o diagram.svg
python scripts/export_mermaid_image.py diagram.mmd -t forest -f pdf -o diagram.pdf
```

### Batch Multi-Format Export
```bash
#!/bin/bash
# Export to all formats
for file in diagrams/*.mmd; do
  base=$(basename "$file" .mmd)
  
  # PNG for web
  python scripts/export_mermaid_image.py "$file" -o "web/${base}.png"
  
  # SVG for scaling
  python scripts/export_mermaid_image.py "$file" -f svg -o "vector/${base}.svg"
  
  # PDF for print
  python scripts/export_mermaid_image.py "$file" -f pdf -o "print/${base}.pdf"
done
```

### Quality Assurance

#### Format Validation
```bash
# Check PNG validity
file diagram.png  # Should show "PNG image data"

# Check SVG validity
xmllint --noout diagram.svg  # Should not show errors

# Check PDF validity
pdfinfo diagram.pdf  # Should show PDF information
```

#### Visual Consistency Check
1. Export same diagram to all formats
2. Compare visual appearance
3. Verify colors, fonts, and layout match
4. Check scaling behavior

## Troubleshooting Format Issues

### Common Problems

#### PNG Artifacts
- **Cause**: Compression artifacts
- **Solution**: Increase scale (`-s 2.0`), use PNG optimization tools

#### SVG Rendering Differences
- **Cause**: Browser SVG implementation variations
- **Solution**: Test in multiple browsers, simplify complex paths

#### PDF Generation Failures
- **Cause**: Puppeteer/Chrome issues
- **Solution**: Update Chrome, increase timeout, check memory

#### Color Differences Between Formats
- **Cause**: Color space differences
- **Solution**: Use consistent color definitions, test output

### Performance Issues

#### Large File Sizes
- **PNG**: Use optimization tools (optipng, pngquant)
- **SVG**: Clean with SVGO, remove unnecessary metadata
- **PDF**: Reduce scale factor, optimize in PDF editor

#### Slow Export
- **Solution**: Reduce diagram complexity
- **Alternative**: Export to SVG (fastest), convert to other formats if needed

## Best Format Selection Guide

### Decision Tree

1. **For Web Display**:
   - Need transparency? → PNG
   - Need scaling? → SVG
   - Simple diagram? → PNG
   - Complex diagram? → SVG

2. **For Print**:
   - Professional printing? → PDF
   - Office printing? → PNG or PDF
   - Large format? → PDF with high scale

3. **For Documentation**:
   - Online docs? → SVG (scales with browser zoom)
   - PDF docs? → PDF or high-res PNG
   - Source control? → SVG (text-based, diff-friendly)

4. **For Presentations**:
   - PowerPoint/Keynote? → PNG or PDF
   - Web presentation? → SVG
   - Handouts? → PDF

5. **For Development**:
   - Quick preview? → PNG
   - Version control? → SVG
   - API documentation? → PNG (universal support)

### Format Conversion

If you need multiple formats:
```bash
# Export to SVG first (fast, scalable)
python scripts/export_mermaid_image.py diagram.mmd -f svg -o diagram.svg

# Convert to other formats as needed
convert diagram.svg diagram.png  # ImageMagick
cairosvg diagram.svg -o diagram.pdf  # CairoSVG
```

## Future Format Support

### Planned Formats
1. **JPEG**: For photographs (not ideal for diagrams)
2. **WebP**: Modern web format with better compression
3. **EPS**: For professional publishing
4. **TIFF**: For archival purposes

### Format Evolution
- Monitor browser support for new formats
- Consider AVIF/JPEG XL for next-gen compression
- Evaluate PDF/A for long-term archival

---

**Next Steps**: Choose the appropriate format based on your specific needs, and refer to the Troubleshooting Guide if you encounter any issues.