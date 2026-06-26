# Mermaid Image Export Skill for Claude

![Mermaid Logo](https://mermaid.js.org/img/logo.svg)

Professional image export skill for Mermaid diagrams using mermaid-cli. Convert Mermaid code into high-quality PNG, SVG, and PDF images for documentation, presentations, and print materials.

## 🎯 Features

- **Multiple Formats**: Export to PNG, SVG, and PDF
- **High Quality**: Browser-based rendering for pixel-perfect outputs
- **Batch Processing**: Export multiple diagrams at once
- **Theme Support**: Built-in themes (default, forest, dark, neutral) + custom CSS
- **Quality Controls**: Resolution scaling, custom dimensions, background colors
- **Complete Documentation**: From installation to advanced usage

## 📋 Prerequisites

- Node.js (v14 or later)
- npm or yarn
- Chrome/Chromium browser
- mermaid-cli (`npm install -g @mermaid-js/mermaid-cli`)

## 🚀 Quick Start

### 1. Installation Check
```bash
python scripts/install_mermaid_cli.py --check
```

### 2. Basic Export
```bash
# Export to PNG
python scripts/export_mermaid_image.py diagram.mmd -o output.png

# Export to SVG
python scripts/export_mermaid_image.py diagram.mmd -f svg -o diagram.svg

# Export to PDF
python scripts/export_mermaid_image.py diagram.mmd -f pdf -o document.pdf
```

### 3. Batch Export
```bash
# Export all .mmd files
python scripts/export_mermaid_image.py *.mmd -d exports/

# Or use shell script
./scripts/batch_export.sh -f svg -t dark -d svg_exports *.mmd
```

## 📁 Skill Structure

```
mermaid-image-export/
├── SKILL.md                    # Skill documentation
├── package.json               # Clawhub metadata
├── scripts/                   # Core scripts
│   ├── export_mermaid_image.py  # Main export script
│   ├── install_mermaid_cli.py   # Installation checker
│   └── batch_export.sh          # Batch export wrapper
├── references/                # Complete documentation
│   ├── overview.md           # Skill overview
│   ├── installation.md       # Installation guide
│   ├── usage.md             # Usage instructions
│   ├── formats.md           # Format specifications
│   └── troubleshooting.md   # Problem solving
└── assets/examples/         # Example files
    ├── export_example.mmd   # Mermaid example diagrams
    └── config_example.json  # Configuration example
```

## 🔄 Complementary with Termaid Skill

This skill works perfectly with the **termaid** skill:

| Use Case | Termaid (ASCII) | Mermaid-CLI (Images) |
|----------|-----------------|---------------------|
| **Development** | Quick preview, debugging | Final export |
| **Output** | Terminal text | PNG/SVG/PDF images |
| **Speed** | Instant | Slower (browser rendering) |
| **Quality** | Terminal-friendly | Print-ready |

**Workflow**: Use termaid for development → Use mermaid-cli for final export.

## 🎨 Examples

### Export with Theme
```bash
python scripts/export_mermaid_image.py diagram.mmd -t dark -o dark_theme.png
```

### High Resolution Export
```bash
python scripts/export_mermaid_image.py diagram.mmd -s 2.0 -o highres.png
```

### Custom CSS Styling
```bash
python scripts/export_mermaid_image.py diagram.mmd -c custom.css -o styled.png
```

### Multi-Format Batch
```bash
# Export to all formats
for file in diagrams/*.mmd; do
  base=$(basename "$file" .mmd)
  python scripts/export_mermaid_image.py "$file" -o "png/${base}.png"
  python scripts/export_mermaid_image.py "$file" -f svg -o "svg/${base}.svg"
  python scripts/export_mermaid_image.py "$file" -f pdf -o "pdf/${base}.pdf"
done
```

## 📚 Documentation

Complete documentation is available in the `references/` directory:

- **Overview**: Skill architecture and use cases
- **Installation**: Step-by-step setup for all platforms
- **Usage**: Complete command reference and examples
- **Formats**: Detailed specifications for PNG, SVG, PDF
- **Troubleshooting**: Comprehensive problem-solving guide

## 🔧 Advanced Usage

### Integration with Documentation Systems
```bash
# Auto-export diagrams for docs
find docs/ -name "*.mmd" -exec python scripts/export_mermaid_image.py {} -d docs/images/ \;
```

### CI/CD Pipeline Integration
```yaml
# GitHub Actions example
- name: Export Mermaid Diagrams
  run: |
    python scripts/export_mermaid_image.py docs/*.mmd -d generated/images/
    git add generated/images/
```

### Makefile Integration
```makefile
DIAGRAMS = $(wildcard diagrams/*.mmd)
IMAGES = $(patsubst diagrams/%.mmd, images/%.png, $(DIAGRAMS))

images/%.png: diagrams/%.mmd
	python scripts/export_mermaid_image.py $< -o $@

diagrams: $(IMAGES)
```

## 🐛 Troubleshooting

Common issues and solutions:

1. **"mmdc: command not found"**: Install mermaid-cli with `npm install -g @mermaid-js/mermaid-cli`
2. **Chrome not found**: Install Chrome/Chromium or set `PUPPETEER_EXECUTABLE_PATH`
3. **Timeout errors**: Increase timeout with `export MMDC_TIMEOUT=120000`
4. **Memory errors**: Increase memory with `export NODE_OPTIONS="--max-old-space-size=4096"`

See `references/troubleshooting.md` for complete troubleshooting guide.

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🔗 Links

- **Mermaid.js**: https://mermaid.js.org/
- **mermaid-cli**: https://github.com/mermaid-js/mermaid-cli
- **Termaid Skill**: Complementary terminal rendering skill
- **Clawhub**: https://clawhub.com

## 📊 Stats

- **Skill Size**: 36KB (compressed)
- **Files**: 11 core files
- **Documentation**: 38KB of comprehensive guides
- **Scripts**: 23KB of production-ready code
- **Examples**: 10KB of ready-to-use examples

---

**Ready to export professional diagrams? Install this skill and start creating!**