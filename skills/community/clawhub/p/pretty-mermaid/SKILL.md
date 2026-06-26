---
name: pretty-mermaid
description: Generate beautiful Mermaid.js diagrams with custom styling and themes. Create flowcharts, sequence diagrams, Gantt charts, class diagrams, etc. with enhanced visual appeal.
---

Follow these steps to create beautiful Mermaid diagrams with custom styling.

## 1) Check Dependencies
This skill uses Mermaid.js and optionally Puppeteer for image generation.

```bash
# Install Node.js packages if needed
npm install -g @mermaid-js/mermaid-cli
```

## 2) Basic Diagram Generation
Create a simple Mermaid diagram:

```bash
# Create a basic flowchart
cat > diagram.mmd << 'EOF'
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
EOF

# Generate PNG
mmdc -i diagram.mmd -o diagram.png
```

## 3) Using Bundled Scripts
Use the bundled Python script for enhanced diagram generation:

```bash
python3 skills/pretty-mermaid/scripts/mermaid-gen.py --help
```

Quick examples:

```bash
# Generate a flowchart with theme
python3 skills/pretty-mermaid/scripts/mermaid-gen.py --type flowchart --output flowchart.png --theme forest

# Generate a sequence diagram
python3 skills/pretty-mermaid/scripts/mermaid-gen.py --type sequence --output sequence.png --theme dark

# Generate a Gantt chart
python3 skills/pretty-mermaid/scripts/mermaid-gen.py --type gantt --output gantt.png --theme neutral

# Generate a class diagram
python3 skills/pretty-mermaid/scripts/mermaid-gen.py --type class --output class.png --theme default
```

## 4) Custom Styling Options
The script supports:
- **Themes**: default, forest, dark, neutral
- **Background colors**: Custom background colors
- **Font styles**: Custom font families and sizes
- **Node styling**: Custom shapes, colors, borders
- **Edge styling**: Custom line styles, colors, widths

Example with custom styling:

```bash
python3 skills/pretty-mermaid/scripts/mermaid-gen.py \
  --type flowchart \
  --output custom.png \
  --theme custom \
  --background "#f8f9fa" \
  --font-family "Arial, sans-serif" \
  --node-color "#1a73e8" \
  --edge-color "#5f6368"
```

## 5) Diagram Types Supported
1. **Flowchart**: Flow diagrams, process flows
2. **Sequence**: Sequence diagrams, UML sequence
3. **Gantt**: Gantt charts, project timelines
4. **Class**: Class diagrams, UML class
5. **State**: State diagrams, state machines
6. **Entity Relationship**: ER diagrams
7. **User Journey**: User journey maps
8. **Pie**: Pie charts
9. **Quadrant**: Quadrant charts
10. **Requirement**: Requirement diagrams

## 6) Advanced Features
- **Interactive diagrams**: Generate HTML with interactive elements
- **Multiple outputs**: Generate PNG, SVG, PDF, HTML from same source
- **Template system**: Use predefined templates for common diagrams
- **Auto-layout**: Automatic layout optimization
- **Export options**: Multiple export formats and resolutions

## 7) Using mermaid-cli Directly
For advanced usage, use mermaid-cli directly:

```bash
# Generate SVG
mmdc -i input.mmd -o output.svg -t forest -b transparent

# Generate PDF
mmdc -i input.mmd -o output.pdf -t dark

# Generate with custom CSS
mmdc -i input.mmd -o output.png -C custom.css
```

## 8) Templates and Examples
Check the `examples/` directory for:
- Common diagram templates
- Styling examples
- Configuration files
- Sample outputs

## 9) Quick Reference
- **Default theme**: default
- **Default format**: PNG
- **Default size**: 800x600
- **Auto-scaling**: Enabled by default
- **Background**: White (#ffffff)
- **Font**: Arial, sans-serif