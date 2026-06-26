# Mermaid-CLI Image Export Overview

Professional image export solution for Mermaid diagrams using mermaid-cli. Converts Mermaid code into high-quality PNG, SVG, and PDF images suitable for documentation, presentations, and print materials.

## Why Use This Skill?

While the `termaid` skill provides terminal rendering, this skill focuses on **professional image export**:

### Key Differences

| Feature | Termaid (ASCII) | Mermaid-CLI (Images) |
|---------|----------------|---------------------|
| **Output Format** | Terminal text | PNG, SVG, PDF |
| **Quality** | Terminal-friendly | Print-ready |
| **Use Cases** | Development, quick preview | Documentation, presentations |
| **Dependencies** | Pure Python | Node.js + Puppeteer |
| **Rendering** | Text-based | Browser-based |

### When to Use Which

**Use Termaid when:**
- You need quick previews in terminal
- You're working over SSH
- You want zero dependencies
- You need to embed diagrams in terminal documentation

**Use Mermaid-CLI when:**
- You need high-quality images for documents
- You're preparing presentations or print materials
- You need vector graphics (SVG)
- You're publishing to web or documentation sites

## Core Architecture

### 1. Technology Stack
- **mermaid-cli**: Official CLI tool from Mermaid.js team
- **Puppeteer**: Headless Chrome for rendering
- **Node.js**: Runtime environment

### 2. Export Pipeline
```
Mermaid Code (.mmd) → mermaid-cli → Puppeteer/Chrome → Image File
```

### 3. Supported Formats

#### PNG (Portable Network Graphics)
- **Best for**: Web, documents, screenshots
- **Features**: Lossless compression, transparency support
- **Limitations**: Raster format, scaling reduces quality

#### SVG (Scalable Vector Graphics)
- **Best for**: Web, print, scaling
- **Features**: Vector format, infinite scaling, small file size
- **Limitations**: Browser support variations

#### PDF (Portable Document Format)
- **Best for**: Print, sharing, archiving
- **Features**: Multi-page support, high quality
- **Limitations**: Larger file sizes

## Key Features

### 1. Professional Output Quality
- Browser-based rendering ensures consistency with web versions
- Anti-aliasing and sub-pixel rendering
- Support for transparency and alpha channels

### 2. Theme Support
- All Mermaid built-in themes (default, forest, dark, neutral)
- Custom theme configuration
- Dark/light mode switching

### 3. Quality Controls
- Resolution scaling (--scale parameter)
- Custom dimensions (width/height)
- Background color control
- Custom CSS styling

### 4. Batch Processing
- Export multiple diagrams at once
- Consistent settings across batch
- Progress tracking and error handling

## Use Cases

### 1. Technical Documentation
- Embed diagrams in README files
- API documentation with visual workflows
- Architecture documentation

### 2. Presentations
- PowerPoint/Keynote slides
- Conference presentations
- Team meetings and reviews

### 3. Print Materials
- Whitepapers and technical papers
- Books and manuals
- Posters and infographics

### 4. Web Content
- Blog posts and articles
- Documentation websites
- Online tutorials

### 5. Development Workflows
- CI/CD pipeline integration
- Documentation automation
- Version-controlled diagrams

## Integration with Development Workflow

### Development Phase
```bash
# Quick preview with termaid
python termaid_script.py diagram.mmd

# Iterate and refine diagram
```

### Production Phase
```bash
# Export high-quality images
python export_mermaid_image.py diagram.mmd -o diagram.png

# Batch export for documentation
python export_mermaid_image.py docs/*.mmd -d generated/
```

## Performance Considerations

### 1. Export Speed
- **PNG/SVG**: Fast (1-3 seconds per diagram)
- **PDF**: Slower (3-10 seconds, requires Puppeteer initialization)

### 2. Resource Usage
- Requires Chrome/Chromium process
- Memory usage scales with diagram complexity
- Consider batch processing for large volumes

### 3. Optimization Tips
- Use SVG for frequently scaled diagrams
- Lower resolution for draft exports
- Cache exported images when possible

## Security Considerations

### 1. Sandboxing
- Puppeteer runs in sandboxed environment
- Limited system access
- Configurable security policies

### 2. Input Validation
- Validate Mermaid syntax before export
- Sanitize file paths and names
- Limit resource consumption

### 3. Network Access
- Can be configured to run offline
- Optional network access for external resources
- Control through Puppeteer configuration

## Future Enhancements

### Planned Features
1. **Template system**: Pre-configured export templates
2. **Advanced styling**: Programmatic CSS injection
3. **Multi-format export**: Single command for all formats
4. **Cloud rendering**: Optional cloud-based rendering service
5. **Plugin system**: Extensible with custom renderers

### Integration Roadmap
- GitHub Actions integration
- VS Code extension
- Jupyter notebook support
- Docker container distribution

## Getting Started

### Quick Test
```bash
# Check installation
python scripts/install_mermaid_cli.py --check

# Export a test diagram
echo 'graph TD; A-->B-->C' > test.mmd
python scripts/export_mermaid_image.py test.mmd -o test.png
```

### Next Steps
1. Review installation guide for detailed setup
2. Explore format options for your use case
3. Try batch export for multiple diagrams
4. Experiment with themes and styling

---

**Note**: This skill requires Node.js and mermaid-cli. For terminal-only usage without dependencies, use the `termaid` skill instead.