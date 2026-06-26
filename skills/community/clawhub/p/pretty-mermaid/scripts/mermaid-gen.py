#!/usr/bin/env python3
"""
Pretty Mermaid Diagram Generator
Generate beautiful Mermaid.js diagrams with custom styling and themes.
"""

import argparse
import os
import sys
import subprocess
import tempfile
import json
from pathlib import Path

# Default themes configuration
THEMES = {
    "default": {
        "background": "#ffffff",
        "fontFamily": "Arial, sans-serif",
        "nodeColor": "#1a73e8",
        "edgeColor": "#5f6368",
        "textColor": "#202124"
    },
    "forest": {
        "background": "#f8f9fa",
        "fontFamily": "Segoe UI, Roboto, sans-serif",
        "nodeColor": "#0d652d",
        "edgeColor": "#34a853",
        "textColor": "#1e4620"
    },
    "dark": {
        "background": "#202124",
        "fontFamily": "Roboto Mono, monospace",
        "nodeColor": "#8ab4f8",
        "edgeColor": "#5e97f6",
        "textColor": "#e8eaed"
    },
    "neutral": {
        "background": "#f5f5f5",
        "fontFamily": "Helvetica Neue, sans-serif",
        "nodeColor": "#5f6368",
        "edgeColor": "#80868b",
        "textColor": "#3c4043"
    }
}

# Diagram templates
DIAGRAM_TEMPLATES = {
    "flowchart": """flowchart TD
    A[Start] --> B{{Decision}}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
    
    style A fill:#1a73e8,color:#ffffff
    style B fill:#fbbc04,color:#202124
    style C fill:#34a853,color:#ffffff
    style D fill:#ea4335,color:#ffffff
    style E fill:#5f6368,color:#ffffff""",
    
    "sequence": """sequenceDiagram
    participant A as User
    participant B as System
    participant C as Database
    
    A->>B: Request Data
    B->>C: Query Database
    C-->>B: Return Results
    B-->>A: Display Data
    
    Note right of A: User interaction
    Note left of C: Data processing""",
    
    "gantt": """gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    axisFormat %b %d
    
    section Phase 1
    Planning :a1, 2024-01-01, 7d
    Design :a2, after a1, 10d
    
    section Phase 2
    Development :a3, after a2, 21d
    Testing :a4, after a3, 7d
    
    section Phase 3
    Deployment :a5, after a4, 3d
    Documentation :a6, after a5, 5d""",
    
    "class": """classDiagram
    class Animal {
        +String name
        +int age
        +eat()
        +sleep()
    }
    
    class Dog {
        +String breed
        +bark()
        +fetch()
    }
    
    class Cat {
        +String color
        +meow()
        +scratch()
    }
    
    Animal <|-- Dog
    Animal <|-- Cat"""
}

def check_dependencies():
    """Check if mermaid-cli is installed."""
    try:
        subprocess.run(["mmdc", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def generate_mermaid_code(diagram_type, custom_code=None):
    """Generate Mermaid code based on type or use custom code."""
    if custom_code:
        return custom_code
    return DIAGRAM_TEMPLATES.get(diagram_type, DIAGRAM_TEMPLATES["flowchart"])

def create_custom_css(theme_config, custom_background=None, custom_font=None):
    """Create custom CSS for the diagram."""
    css = f"""
    .label {{
        font-family: {custom_font or theme_config['fontFamily']};
        color: {theme_config['textColor']};
    }}
    
    .node rect, .node circle, .node ellipse, .node polygon {{
        fill: {theme_config['nodeColor']};
        stroke: {theme_config['edgeColor']};
        stroke-width: 2px;
    }}
    
    .edgePath .path {{
        stroke: {theme_config['edgeColor']};
        stroke-width: 2px;
    }}
    
    .cluster rect {{
        fill: rgba(255, 255, 255, 0.1);
        stroke: {theme_config['edgeColor']};
        stroke-width: 1px;
    }}
    """
    return css

def generate_diagram(args):
    """Generate the Mermaid diagram."""
    # Get theme configuration
    theme_config = THEMES.get(args.theme, THEMES["default"])
    
    # Generate Mermaid code
    mermaid_code = generate_mermaid_code(args.type, args.code)
    
    # Check if output is HTML
    if args.output.lower().endswith('.html') or args.html:
        return generate_html_diagram(args, theme_config, mermaid_code)
    
    # Otherwise try to generate image using mermaid-cli
    if not check_dependencies():
        print("Warning: mermaid-cli (mmdc) is not installed or Chrome is missing.")
        print("Generating HTML version instead...")
        html_output = args.output.rsplit('.', 1)[0] + '.html'
        args.html = True
        args.output = html_output
        return generate_html_diagram(args, theme_config, mermaid_code)
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as mmd_file:
        mmd_file.write(mermaid_code)
        mmd_path = mmd_file.name
    
    css_path = None
    if args.theme == "custom" or args.background or args.font_family:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False) as css_file:
            css_content = create_custom_css(
                theme_config,
                args.background,
                args.font_family
            )
            css_file.write(css_content)
            css_path = css_file.name
    
    try:
        # Build command
        cmd = ["mmdc", "-i", mmd_path, "-o", args.output]
        
        # Add theme
        if args.theme != "custom":
            cmd.extend(["-t", args.theme])
        
        # Add CSS if custom
        if css_path:
            cmd.extend(["-C", css_path])
        
        # Add background color
        if args.background:
            cmd.extend(["-b", args.background])
        
        # Add additional options
        if args.width and args.height:
            cmd.extend(["-w", str(args.width), "-H", str(args.height)])
        
        # Run command
        print(f"Generating diagram: {args.output}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error generating diagram: {result.stderr}")
            print("Falling back to HTML generation...")
            html_output = args.output.rsplit('.', 1)[0] + '.html'
            return generate_html_diagram(args, theme_config, mermaid_code, html_output)
        
        print(f"Successfully generated: {args.output}")
        
        # Also generate HTML if requested
        if args.html:
            html_output = args.output.replace('.png', '.html').replace('.svg', '.html')
            generate_html_diagram(args, theme_config, mermaid_code, html_output)
        
        return True
        
    finally:
        # Clean up temporary files
        try:
            os.unlink(mmd_path)
            if css_path:
                os.unlink(css_path)
        except:
            pass

def generate_html_diagram(args, theme_config, mermaid_code, html_output=None):
    """Generate interactive HTML diagram."""
    if not html_output:
        html_output = args.output if args.output.lower().endswith('.html') else 'diagram.html'
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mermaid Diagram - {args.type.capitalize()}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: {args.background or theme_config['background']};
            font-family: {args.font_family or theme_config['fontFamily']};
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            width: 100%;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 2px solid {theme_config['edgeColor']};
        }}
        
        h1 {{
            color: {theme_config['textColor']};
            margin: 0 0 8px 0;
        }}
        
        .subtitle {{
            color: {theme_config['edgeColor']};
            font-size: 14px;
            margin: 0;
        }}
        
        .mermaid {{
            width: 100%;
            text-align: center;
            margin: 20px 0;
        }}
        
        .code-container {{
            background: rgba(0, 0, 0, 0.05);
            border-radius: 8px;
            padding: 16px;
            margin-top: 24px;
            overflow-x: auto;
        }}
        
        pre {{
            margin: 0;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.4;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: {theme_config['edgeColor']};
            font-size: 12px;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 16px;
            }}
            body {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Mermaid {args.type.capitalize()} Diagram</h1>
            <p class="subtitle">Theme: {args.theme} | Generated with Pretty Mermaid Skill</p>
        </div>
        
        <div class="mermaid">
{mermaid_code}
        </div>
        
        <div class="code-container">
            <h3>Mermaid Code:</h3>
            <pre><code>{mermaid_code}</code></pre>
        </div>
    </div>
    
    <div class="footer">
        Generated by Pretty Mermaid Skill for OpenClaw | Interactive diagram - zoom and pan enabled
    </div>
    
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: '{args.theme}',
            themeVariables: {{
                primaryColor: '{theme_config['nodeColor']}',
                primaryTextColor: '{theme_config['textColor']}',
                primaryBorderColor: '{theme_config['edgeColor']}',
                lineColor: '{theme_config['edgeColor']}',
                secondaryColor: '{theme_config['background']}',
                tertiaryColor: '{theme_config['background']}',
                fontFamily: '{args.font_family or theme_config['fontFamily']}'
            }},
            flowchart: {{ 
                curve: 'basis',
                useMaxWidth: true
            }},
            sequence: {{
                diagramMarginX: 50,
                diagramMarginY: 10,
                actorMargin: 50,
                width: 150,
                height: 65,
                boxMargin: 10,
                boxTextMargin: 5,
                noteMargin: 10,
                messageMargin: 35,
                mirrorActors: true,
                bottomMarginAdj: 1,
                useMaxWidth: true
            }},
            gantt: {{
                titleTopMargin: 25,
                barHeight: 20,
                barGap: 4,
                topPadding: 50,
                leftPadding: 75,
                gridLineStartPadding: 35,
                fontSize: 11,
                fontFamily: '"Open Sans", sans-serif',
                numberSectionStyles: 4,
                axisFormat: '%Y-%m-%d',
                useMaxWidth: true
            }}
        }});
        
        // Add zoom and pan functionality
        document.addEventListener('DOMContentLoaded', function() {{
            const diagrams = document.querySelectorAll('.mermaid svg');
            diagrams.forEach(svg => {{
                svg.style.cursor = 'move';
                let isPanning = false;
                let startPoint = {{ x: 0, y: 0 }};
                let endPoint = {{ x: 0, y: 0 }};
                let scale = 1;
                
                svg.addEventListener('mousedown', function(e) {{
                    isPanning = true;
                    startPoint = {{ x: e.clientX, y: e.clientY }};
                }});
                
                svg.addEventListener('mousemove', function(e) {{
                    if (!isPanning) return;
                    endPoint = {{ x: e.clientX, y: e.clientY }};
                    const dx = endPoint.x - startPoint.x;
                    const dy = endPoint.y - startPoint.y;
                    
                    const viewBox = svg.getAttribute('viewBox');
                    if (viewBox) {{
                        const [x, y, width, height] = viewBox.split(' ').map(Number);
                        svg.setAttribute('viewBox', `${x - dx} ${y - dy} ${width} ${height}`);
                    }}
                    
                    startPoint = endPoint;
                }});
                
                svg.addEventListener('mouseup', function() {{
                    isPanning = false;
                }});
                
                svg.addEventListener('mouseleave', function() {{
                    isPanning = false;
                }});
                
                svg.addEventListener('wheel', function(e) {{
                    e.preventDefault();
                    const delta = e.deltaY > 0 ? 0.9 : 1.1;
                    scale *= delta;
                    
                    const viewBox = svg.getAttribute('viewBox');
                    if (viewBox) {{
                        const [x, y, width, height] = viewBox.split(' ').map(Number);
                        const newWidth = width * delta;
                        const newHeight = height * delta;
                        const newX = x + (width - newWidth) / 2;
                        const newY = y + (height - newHeight) / 2;
                        svg.setAttribute('viewBox', `${newX} ${newY} ${newWidth} ${newHeight}`);
                    }}
                }}, {{ passive: false }});
            }});
        }});
    </script>
</body>
</html>"""
    
    try:
        with open(html_output, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ Successfully generated interactive HTML: {html_output}")
        print(f"  Open this file in your browser to view the diagram")
        print(f"  Features: Zoom with mouse wheel, Pan by dragging")
        return True
    except Exception as e:
        print(f"✗ Error generating HTML: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Generate beautiful Mermaid diagrams")
    
    # Diagram type
    parser.add_argument("--type", choices=list(DIAGRAM_TEMPLATES.keys()), 
                       default="flowchart", help="Type of diagram to generate")
    
    # Output
    parser.add_argument("--output", "-o", default="diagram.png",
                       help="Output file path (PNG or SVG)")
    
    # Theme
    parser.add_argument("--theme", choices=list(THEMES.keys()) + ["custom"],
                       default="default", help="Theme for the diagram")
    
    # Custom styling
    parser.add_argument("--background", help="Custom background color (hex)")
    parser.add_argument("--font-family", help="Custom font family")
    parser.add_argument("--node-color", help="Custom node color (hex)")
    parser.add_argument("--edge-color", help="Custom edge color (hex)")
    
    # Dimensions
    parser.add_argument("--width", type=int, help="Diagram width in pixels")
    parser.add_argument("--height", type=int, help="Diagram height in pixels")
    
    # Custom code
    parser.add_argument("--code", help="Custom Mermaid code (overrides --type)")
    
    # Additional outputs
    parser.add_argument("--html", action="store_true", help="Also generate HTML version")
    
    args = parser.parse_args()
    
    # Validate output format
    if not args.output.lower().endswith(('.png', '.svg')):
        print("Warning: Output format should be PNG or SVG")
    
    # Generate diagram
    success = generate_diagram(args)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()