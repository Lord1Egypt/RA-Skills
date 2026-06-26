#!/usr/bin/env python3
"""
Markdown to PowerPoint converter
Converts markdown files with slide separators (---) to PPTX format
"""

import sys
import os
import re
from pathlib import Path

def get_obsidian_vault_path():
    """Get the active Obsidian vault path from obsidian.json"""
    obsidian_config = Path.home() / "Library/Application Support/obsidian/obsidian.json"
    if obsidian_config.exists():
        import json
        with open(obsidian_config) as f:
            data = json.load(f)
            for vault_id, vault_info in data.get("vaults", {}).items():
                if vault_info.get("open"):
                    return vault_info.get("path")
    return None

def md_to_pptx(input_file, output_file=None):
    """Convert markdown to pptx using LibreOffice or pandoc"""
    input_path = Path(input_file)
    
    if not output_file:
        # Default to Obsidian vault if available
        vault_path = get_obsidian_vault_path()
        if vault_path:
            output_dir = Path(vault_path)
        else:
            output_dir = input_path.parent
        output_file = output_dir / f"{input_path.stem}.pptx"
    
    # Try LibreOffice first (better PPTX output)
    import subprocess
    
    # First convert md to html with slide markers
    html_content = convert_md_to_html(input_file)
    
    # Save intermediate HTML
    html_file = input_path.with_suffix('.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Use LibreOffice to convert HTML to PPTX
    try:
        result = subprocess.run([
            'soffice', '--headless', '--convert-to', 'pptx',
            '--outdir', str(Path(output_file).parent),
            str(html_file)
        ], capture_output=True, text=True, timeout=60)
        
        # Rename to desired output name
        generated = html_file.with_suffix('.pptx')
        if generated.exists():
            if generated != Path(output_file):
                generated.rename(output_file)
            html_file.unlink()  # Clean up HTML
            return str(output_file)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Fallback: try pandoc
    try:
        result = subprocess.run([
            'pandoc', str(input_file), '-o', str(output_file)
        ], capture_output=True, text=True, timeout=30)
        
        if Path(output_file).exists():
            return str(output_file)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Last resort: just copy info
    print(f"Warning: Could not convert to PPTX. Please install LibreOffice or pandoc.")
    print(f"Markdown file available at: {input_file}")
    return None

def convert_md_to_html(md_file):
    """Convert markdown to simple HTML with slide divs"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by slide separators
    slides = re.split(r'\n---\s*\n', content)
    
    html_slides = []
    for i, slide in enumerate(slides):
        # Convert basic markdown to HTML
        slide_html = markdown_to_html(slide.strip())
        html_slides.append(f'<div class="slide" id="slide-{i+1}">\n{slide_html}\n</div>')
    
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Presentation</title>
<style>
.slide {{ page-break-after: always; margin: 40px; }}
h1 {{ color: #333; }}
h2 {{ color: #555; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background-color: #f2f2f2; }}
pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 4px; }}
code {{ font-family: monospace; }}
</style>
</head>
<body>
{chr(10).join(html_slides)}
</body>
</html>"""

def markdown_to_html(text):
    """Simple markdown to HTML conversion"""
    # Headers
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # Bold and italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    
    # Code blocks
    text = re.sub(r'```[\w]*\n(.*?)```', r'<pre><code>\1</code></pre>', text, flags=re.DOTALL)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    
    # Lists
    lines = text.split('\n')
    result = []
    in_list = False
    
    for line in lines:
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            item = line.strip()[2:]
            result.append(f'<li>{item}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
    
    if in_list:
        result.append('</ul>')
    
    text = '\n'.join(result)
    
    # Tables (simple)
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        if '|' in lines[i] and i + 1 < len(lines) and '|---' in lines[i + 1]:
            # Start of table
            headers = [c.strip() for c in lines[i].split('|') if c.strip()]
            result.append('<table><tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr>')
            i += 2  # Skip header separator
            while i < len(lines) and '|' in lines[i]:
                cells = [c.strip() for c in lines[i].split('|') if c.strip()]
                if cells:
                    result.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
                i += 1
            result.append('</table>')
        else:
            result.append(lines[i])
            i += 1
    
    text = '\n'.join(result)
    
    # Paragraphs
    paragraphs = text.split('\n\n')
    new_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<') and not p.startswith('```'):
            p = f'<p>{p}</p>'
        new_paragraphs.append(p)
    
    return '\n\n'.join(new_paragraphs)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: md2pptx.py <input.md> [output.pptx]")
        print("If output not specified, saves to Obsidian vault (if configured)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = md_to_pptx(input_file, output_file)
    if result:
        print(f"Created: {result}")
    else:
        sys.exit(1)
