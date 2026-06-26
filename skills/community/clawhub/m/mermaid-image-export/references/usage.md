# Usage Guide

Complete guide to using the mermaid-cli image export skill.

## Quick Start Examples

### Basic Single File Export
```bash
# Export to PNG (default)
python scripts/export_mermaid_image.py diagram.mmd -o output.png

# Export to SVG
python scripts/export_mermaid_image.py diagram.mmd -f svg -o diagram.svg

# Export to PDF
python scripts/export_mermaid_image.py diagram.mmd -f pdf -o document.pdf
```

### Batch Export
```bash
# Export all .mmd files in current directory
python scripts/export_mermaid_image.py *.mmd -d outputs/

# Export specific files
python scripts/export_mermaid_image.py flowchart.mmd sequence.mmd -d diagrams/

# Export with different format
python scripts/export_mermaid_image.py *.mmd -f svg -d svg_outputs/
```

## Command Reference

### Python Script: `export_mermaid_image.py`

#### Basic Arguments
```
positional arguments:
  input                 Input Mermaid file(s) (.mmd) or directory

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file (for single file export)
  -d OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output directory (for batch export)
  -f {png,svg,pdf}, --format {png,svg,pdf}
                        Output format (default: png)
  -t THEME, --theme THEME
                        Mermaid theme (default, forest, dark, neutral)
  -w WIDTH, --width WIDTH
                        Image width in pixels
  -H HEIGHT, --height HEIGHT
                        Image height in pixels
  -s SCALE, --scale SCALE
                        Scale factor (default: 1.0)
  -b BACKGROUND, --background BACKGROUND
                        Background color (default: transparent)
  -c CSS, --css CSS     Custom CSS file for styling
  -C CONFIG, --config CONFIG
                        Mermaid config file
  -q, --quiet           Quiet mode (suppress output)
  --mermaid-cmd MERMAID_CMD
                        mermaid-cli command (default: mmdc, use 'npx mmdc' for local)
```

### Shell Script: `batch_export.sh`

#### Basic Usage
```bash
# Simple batch export
./scripts/batch_export.sh *.mmd

# With options
./scripts/batch_export.sh -f svg -t dark -d exports *.mmd

# Verbose output
./scripts/batch_export.sh -v *.mmd
```

#### Shell Script Options
```
Options:
  -h, --help            Show this help message
  -f, --format FORMAT   Output format: png, svg, pdf (default: png)
  -t, --theme THEME     Mermaid theme (default: default)
  -d, --output-dir DIR  Output directory (default: exports)
  -s, --scale SCALE     Scale factor (default: 1.0)
  -b, --background COLOR Background color (default: transparent)
  -v, --verbose         Verbose output
  --mermaid-cmd CMD     mermaid-cli command (default: mmdc or npx mmdc)
```

## Format-Specific Usage

### PNG Format
```bash
# Basic PNG export
python scripts/export_mermaid_image.py diagram.mmd -o diagram.png

# High resolution PNG
python scripts/export_mermaid_image.py diagram.mmd -s 2.0 -o highres.png

# PNG with specific dimensions
python scripts/export_mermaid_image.py diagram.mmd -w 1200 -H 800 -o sized.png

# PNG with white background (for print)
python scripts/export_mermaid_image.py diagram.mmd -b white -o print.png
```

### SVG Format
```bash
# Basic SVG export
python scripts/export_mermaid_image.py diagram.mmd -f svg -o diagram.svg

# SVG with dark theme
python scripts/export_mermaid_image.py diagram.mmd -f svg -t dark -o dark.svg

# SVG for web embedding
python scripts/export_mermaid_image.py diagram.mmd -f svg -b white -o web.svg
```

### PDF Format
```bash
# Basic PDF export
python scripts/export_mermaid_image.py diagram.mmd -f pdf -o document.pdf

# PDF with A4 size
python scripts/export_mermaid_image.py diagram.mmd -f pdf -w 210 -H 297 -o a4.pdf

# PDF for presentation
python scripts/export_mermaid_image.py diagram.mmd -f pdf -t dark -o presentation.pdf
```

## Theme Configuration

### Built-in Themes
```bash
# Default theme (light)
python scripts/export_mermaid_image.py diagram.mmd -t default -o default.png

# Forest theme (green)
python scripts/export_mermaid_image.py diagram.mmd -t forest -o forest.png

# Dark theme
python scripts/export_mermaid_image.py diagram.mmd -t dark -o dark.png

# Neutral theme
python scripts/export_mermaid_image.py diagram.mmd -t neutral -o neutral.png
```

### Custom Theme via CSS
Create a custom CSS file:
```css
/* custom.css */
:root {
  --mermaid-font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  --mermaid-edge-color: #4a90e2;
  --mermaid-node-bg: #f0f8ff;
  --mermaid-node-border: #4a90e2;
}

.node rect, .node circle, .node ellipse, .node polygon {
  fill: var(--mermaid-node-bg);
  stroke: var(--mermaid-node-border);
  stroke-width: 2px;
}

.edgePath path {
  stroke: var(--mermaid-edge-color);
  stroke-width: 2px;
}
```

Use the custom CSS:
```bash
python scripts/export_mermaid_image.py diagram.mmd -c custom.css -o custom.png
```

### Mermaid Configuration File
Create a config file:
```json
{
  "theme": "forest",
  "themeVariables": {
    "primaryColor": "#BB2528",
    "primaryTextColor": "#fff",
    "primaryBorderColor": "#7C0000",
    "lineColor": "#F8B229",
    "secondaryColor": "#006100",
    "tertiaryColor": "#fff"
  }
}
```

Use the config:
```bash
python scripts/export_mermaid_image.py diagram.mmd -C config.json -o configured.png
```

## Advanced Usage Patterns

### 1. Integration with Documentation
```bash
# Export all diagrams for documentation
find docs/ -name "*.mmd" -exec python scripts/export_mermaid_image.py {} -d docs/images/ \;

# Update images when diagrams change
python scripts/export_mermaid_image.py docs/*.mmd -d docs/images/ --quiet
```

### 2. CI/CD Pipeline Integration
```yaml
# GitHub Actions example
- name: Export Mermaid Diagrams
  run: |
    python scripts/export_mermaid_image.py docs/*.mmd -d generated/images/
    git add generated/images/
    git commit -m "Update diagram images" || echo "No changes"
```

### 3. Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit
python scripts/export_mermaid_image.py docs/*.mmd -d docs/images/ -q
git add docs/images/
```

### 4. Makefile Integration
```makefile
DIAGRAMS = $(wildcard diagrams/*.mmd)
IMAGES = $(patsubst diagrams/%.mmd, images/%.png, $(DIAGRAMS))

images/%.png: diagrams/%.mmd
	python scripts/export_mermaid_image.py $< -o $@

diagrams: $(IMAGES)

clean:
	rm -f images/*.png images/*.svg images/*.pdf
```

### 5. Dynamic Diagram Generation
```python
#!/usr/bin/env python3
import subprocess
import tempfile

def export_dynamic_diagram(mermaid_code, output_file):
    """Generate and export a dynamic diagram."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
        f.write(mermaid_code)
        temp_file = f.name
    
    try:
        subprocess.run([
            'python', 'scripts/export_mermaid_image.py',
            temp_file, '-o', output_file
        ], check=True)
    finally:
        import os
        os.unlink(temp_file)

# Example usage
diagram_code = """
graph LR
    Client --> LoadBalancer
    LoadBalancer --> Service
    Service --> Database
"""

export_dynamic_diagram(diagram_code, 'architecture.png')
```

## Quality and Performance Optimization

### Resolution and Scaling
```bash
# For web (standard resolution)
python scripts/export_mermaid_image.py diagram.mmd -s 1.0 -o web.png

# For high-DPI displays
python scripts/export_mermaid_image.py diagram.mmd -s 2.0 -o retina.png

# For print (high resolution)
python scripts/export_mermaid_image.py diagram.mmd -s 3.0 -o print.png
```

### Batch Processing Optimization
```bash
# Process in parallel (Linux/macOS)
find . -name "*.mmd" -print0 | xargs -0 -P4 -I{} python scripts/export_mermaid_image.py {} -d outputs/ -q

# Sequential with progress
for file in *.mmd; do
    echo "Processing $file..."
    python scripts/export_mermaid_image.py "$file" -d outputs/ -q
done
```

### Memory Management
```bash
# Increase timeout for complex diagrams
export MMDC_TIMEOUT=60000  # 60 seconds

# Increase memory for Node.js
export NODE_OPTIONS="--max-old-space-size=4096"

# Run export with increased resources
python scripts/export_mermaid_image.py complex.mmd -o complex.png
```

## Error Handling and Debugging

### Verbose Mode
```bash
# See detailed output
python scripts/export_mermaid_image.py diagram.mmd -o output.png  # Default shows progress

# Suppress output
python scripts/export_mermaid_image.py diagram.mmd -o output.png -q

# Shell script verbose
./scripts/batch_export.sh -v *.mmd
```

### Common Errors and Solutions

#### 1. "Timeout exporting"
```bash
# Increase timeout
python scripts/export_mermaid_image.py large.mmd -o large.png  # Script handles timeout

# Or set environment variable
export MMDC_TIMEOUT=120000  # 120 seconds
```

#### 2. "Chrome not found"
```bash
# Specify Chrome path
export PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome
python scripts/export_mermaid_image.py diagram.mmd -o diagram.png
```

#### 3. "Memory error"
```bash
# Reduce complexity or increase memory
python scripts/export_mermaid_image.py diagram.mmd -s 1.0 -o diagram.png  # Lower scale
export NODE_OPTIONS="--max-old-space-size=8192"  # Increase memory
```

## Best Practices

### 1. File Organization
```
project/
├── diagrams/
│   ├── architecture.mmd
│   ├── workflow.mmd
│   └── sequence.mmd
├── scripts/
│   └── export_mermaid_image.py
├── generated/
│   ├── images/
│   │   ├── architecture.png
│   │   ├── workflow.png
│   │   └── sequence.png
│   └── svg/
│       ├── architecture.svg
│       └── workflow.svg
└── docs/
    └── index.md  # References generated images
```

### 2. Version Control
```bash
# Keep Mermaid source files in version control
git add diagrams/*.mmd

# Generated images can be regenerated, but may be cached
git add -f generated/images/*.png

# .gitignore for temporary files
echo "*.tmp" >> .gitignore
echo "temp_*" >> .gitignore
```

### 3. Documentation Integration
```markdown
# In README.md or docs
![Architecture Diagram](generated/images/architecture.png)

![Workflow SVG](generated/svg/workflow.svg)
```

## Next Steps

After mastering basic usage, explore:
1. **Custom Themes**: Create brand-specific styling
2. **Automation**: Integrate with your build process
3. **Advanced Formats**: Explore PDF multi-page exports
4. **Performance**: Optimize for large diagram collections

Refer to the Formats Guide for detailed information about each output format and Troubleshooting Guide for common issues and solutions.