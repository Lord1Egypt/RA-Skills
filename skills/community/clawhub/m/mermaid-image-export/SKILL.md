---
name: mermaid-image-export
description: Mermaid diagram image export using mermaid-cli. When Claude needs to export Mermaid diagrams as high-quality images (PNG, SVG, PDF) for documentation, presentations, print materials, or web embedding. Uses mermaid-cli with Puppeteer-based rendering for pixel-perfect outputs.
---

# Mermaid CLI Image Export Skill

Professional image export skill for Mermaid diagrams using mermaid-cli. Converts Mermaid code into high-quality PNG, SVG, and PDF images suitable for documentation, presentations, and print materials.

## Quick Start

### Prerequisites
```bash
# Check if Node.js is installed
node --version

# Check if npm is installed
npm --version
```

### Installation Check
```bash
python scripts/install_mermaid_cli.py --check
```

### Basic Usage
Export a Mermaid diagram to PNG:
```bash
python scripts/export_mermaid_image.py diagram.mmd -o output.png
```

Export to SVG:
```bash
python scripts/export_mermaid_image.py diagram.mmd -f svg -o diagram.svg
```

Batch export multiple files:
```bash
python scripts/export_mermaid_image.py *.mmd -d outputs/
```

## Core Features

### Supported Formats
- **PNG**: Raster image, ideal for web and documents
- **SVG**: Vector image, scalable without quality loss  
- **PDF**: Document format for printing and sharing

### Quality Controls
- Resolution scaling (`--scale`)
- Background color (`--background`)
- Width and height constraints (`--width`, `--height`)
- Custom CSS styling (`--css`)

### Theme Support
- All Mermaid built-in themes: `default`, `forest`, `dark`, `neutral`
- Custom theme configuration (`--config`)
- Dark/light mode switching

### Batch Processing
- Export multiple diagrams at once
- Progress tracking and error handling
- Consistent settings across all exports

## Workflow

### 1. Environment Setup
Ensure Node.js and mermaid-cli are installed:
```bash
npm install -g @mermaid-js/mermaid-cli
```

### 2. Diagram Creation
Create Mermaid diagrams using standard syntax.

### 3. Image Export
Use appropriate format based on needs:
- **Web/Docs**: PNG or SVG
- **Print**: PDF or high-resolution PNG
- **Development**: Quick PNG previews

### 4. Integration
Embed exported images in:
- README documentation
- Presentation slides
- Technical papers
- API documentation
- Blog posts

## Comparison with Termaid

| Feature | Termaid | Mermaid-CLI Export |
|---------|---------|-------------------|
| **Output** | ASCII terminal | PNG/SVG/PDF images |
| **Dependencies** | Pure Python | Node.js + Puppeteer |
| **Use Case** | Terminal preview | Professional export |
| **Quality** | Terminal-friendly | Print-ready |
| **Speed** | Instant | Requires browser |

## Advanced Usage

### Custom Configuration
```bash
# Custom CSS
python scripts/export_mermaid_image.py diagram.mmd --css custom.css -o output.png

# Specific theme
python scripts/export_mermaid_image.py diagram.mmd -t dark -o output.png

# High resolution
python scripts/export_mermaid_image.py diagram.mmd --scale 2.0 -o output.png
```

### Automation
```bash
# CI/CD integration
python scripts/export_mermaid_image.py docs/*.mmd -d generated/

# Documentation generation
find . -name "*.mmd" -exec python scripts/export_mermaid_image.py {} -o images/{}.png \;
```

## Troubleshooting

### Common Issues
1. **Node.js not installed**: Install Node.js from nodejs.org
2. **mermaid-cli not found**: Run `npm install -g @mermaid-js/mermaid-cli`
3. **Browser errors**: Ensure Chrome/Chromium is installed
4. **Memory issues**: Reduce image size or resolution

### Performance Tips
- Use lower resolution for quick previews
- Cache frequently used diagrams
- Batch process multiple diagrams
- Consider using SVG for scalability

## Examples

See `assets/examples/` for complete examples:
- Basic export workflow
- Configuration examples
- Template diagrams

## References

Complete documentation in `references/`:
- `overview.md`: Skill overview
- `installation.md`: Installation guide
- `usage.md`: Usage instructions
- `formats.md`: Format specifications
- `troubleshooting.md`: Problem solving

---

**Note**: This skill requires Node.js and mermaid-cli installation. For terminal-only rendering without dependencies, use the `termaid` skill.