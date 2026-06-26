#!/usr/bin/env python3
"""Markdown Tool - Process Markdown files."""

import argparse
import re
import sys
import os
from typing import List, Dict


def parse_markdown(md: str) -> Dict:
    """Parse markdown and extract structure."""
    lines = md.split('\n')
    headings = []
    code_blocks = []
    links = []
    
    in_code = False
    code_lang = ""
    
    for i, line in enumerate(lines):
        # Headings
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            text = line.lstrip('#').strip()
            headings.append({'level': level, 'text': text, 'line': i + 1})
        
        # Code blocks
        if line.startswith('```'):
            if not in_code:
                in_code = True
                code_lang = line[3:].strip()
            else:
                in_code = False
                code_blocks.append({'lang': code_lang, 'start': i})
        
        # Links
        links.extend(re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', line))
    
    return {
        'headings': headings,
        'code_blocks': code_blocks,
        'links': links
    }


def md_to_html(md: str, style: str = 'github') -> str:
    """Convert markdown to HTML."""
    html_lines = []
    
    # Basic conversions
    lines = md.split('\n')
    in_code = False
    in_list = False
    
    for line in lines:
        # Code blocks
        if line.startswith('```'):
            if in_code:
                html_lines.append('</code></pre>')
                in_code = False
            else:
                lang = line[3:].strip()
                html_lines.append(f'<pre><code class="language-{lang}">')
                in_code = True
            continue
        
        if in_code:
            html_lines.append(line)
            continue
        
        # Headings
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            text = line.lstrip('#').strip()
            html_lines.append(f'<h{level}>{text}</h{level}>')
            continue
        
        # Code (inline)
        line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)
        
        # Bold
        line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', line)
        
        # Italic
        line = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', line)
        line = re.sub(r'_([^_]+)_', r'<em>\1</em>', line)
        
        # Links
        line = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', line)
        
        # Images
        line = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1">', line)
        
        # Lists
        if line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{line[2:]}</li>')
            continue
        elif in_list:
            html_lines.append('</ul>')
            in_list = False
        
        # Paragraph
        if line.strip():
            html_lines.append(f'<p>{line}</p>')
        else:
            html_lines.append('')
    
    if in_list:
        html_lines.append('</ul>')
    
    # Wrap in template
    template = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Markdown</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        pre {{ background: #f6f8fa; padding: 16px; border-radius: 6px; overflow-x: auto; }}
        code {{ background: #f6f8fa; padding: 2px 6px; border-radius: 3px; }}
        pre code {{ background: none; padding: 0; }}
        blockquote {{ border-left: 4px solid #dfe2e5; padding-left: 16px; color: #6a737d; margin: 0; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #dfe2e5; padding: 8px; }}
        img {{ max-width: 100%; }}
    </style>
</head>
<body>
{chr(10).join(html_lines)}
</body>
</html>'''
    
    return template


def generate_toc(headings: List[Dict]) -> str:
    """Generate table of contents."""
    if not headings:
        return ""
    
    toc = ["## Table of Contents\n"]
    
    for h in headings:
        indent = "  " * (h['level'] - 1)
        anchor = h['text'].lower().replace(' ', '-')
        anchor = re.sub(r'[^\w\-]', '', anchor)
        toc.append(f'{indent}- [{h["text"]}](#{anchor})')
    
    return '\n'.join(toc)


def main():
    parser = argparse.ArgumentParser(description='Markdown processing tool')
    parser.add_argument('input', nargs='?', help='Input Markdown file')
    parser.add_argument('--to', choices=['html', 'txt'], default='html', help='Output format')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--toc', action='store_true', help='Generate TOC')
    parser.add_argument('--style', default='github', help='CSS style')
    parser.add_argument('--serve', type=int, help='Start server')
    
    args = parser.parse_args()
    
    # Read input
    if args.input:
        if not os.path.exists(args.input):
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        with open(args.input, 'r') as f:
            md = f.read()
    else:
        md = sys.stdin.read()
    
    # Parse
    parsed = parse_markdown(md)
    
    # Generate TOC
    if args.toc:
        toc = generate_toc(parsed['headings'])
        print(toc)
        return
    
    # Convert
    if args.to == 'html':
        html = md_to_html(md, args.style)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(html)
            print(f"Saved to: {args.output}")
        else:
            print(html)
    elif args.to == 'txt':
        # Strip markdown
        txt = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', md)
        txt = re.sub(r'[#*_`]', '', txt)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(txt)
        else:
            print(txt)


if __name__ == '__main__':
    main()
