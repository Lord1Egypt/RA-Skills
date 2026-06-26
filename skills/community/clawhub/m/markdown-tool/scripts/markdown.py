#!/usr/bin/env python3
"""Markdown Tool - Parse and convert Markdown."""

import argparse
import re
import sys
import html


def parse_inline(text: str) -> str:
    """Parse inline Markdown elements."""
    # Escape HTML first
    text = html.escape(text)
    
    # Code blocks (inline)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', text)
    
    # Italic
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'_([^_]+)_', r'<em>\1</em>', text)
    
    # Strikethrough
    text = re.sub(r'~~([^~]+)~~', r'<del>\1</del>', text)
    
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    
    # Images
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)
    
    return text


def parse_block(lines: list) -> list:
    """Parse block-level Markdown elements."""
    blocks = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Empty line
        if not line.strip():
            i += 1
            continue
        
        # Headers
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if header_match:
            level = len(header_match.group(1))
            content = parse_inline(header_match.group(2))
            blocks.append(f'<h{level}>{content}</h{level}>')
            i += 1
            continue
        
        # Code block
        if line.strip().startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i].rstrip())
                i += 1
            code = '\n'.join(code_lines)
            blocks.append(f'<pre><code>{html.escape(code)}</code></pre>')
            i += 1
            continue
        
        # Blockquote
        if line.strip().startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            content = parse_inline(' '.join(quote_lines))
            blocks.append(f'<blockquote>{content}</blockquote>')
            continue
        
        # Unordered list
        if re.match(r'^[\*\-\+]\s+', line):
            list_items = []
            while i < len(lines) and re.match(r'^[\*\-\+]\s+', lines[i]):
                item = re.sub(r'^[\*\-\+]\s+', '', lines[i])
                list_items.append(f'<li>{parse_inline(item)}</li>')
                i += 1
            blocks.append('<ul>' + ''.join(list_items) + '</ul>')
            continue
        
        # Ordered list
        if re.match(r'^\d+\.\s+', line):
            list_items = []
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i]):
                item = re.sub(r'^\d+\.\s+', '', lines[i])
                list_items.append(f'<li>{parse_inline(item)}</li>')
                i += 1
            blocks.append('<ol>' + ''.join(list_items) + '</ol>')
            continue
        
        # Horizontal rule
        if re.match(r'^[\*\-_]{3,}$', line.strip()):
            blocks.append('<hr>')
            i += 1
            continue
        
        # Paragraph
        para_lines = []
        while i < len(lines) and lines[i].strip() and not re.match(r'^#{1,6}\s+', lines[i]):
            para_lines.append(lines[i].rstrip())
            i += 1
        
        if para_lines:
            content = parse_inline(' '.join(para_lines))
            blocks.append(f'<p>{content}</p>')
    
    return blocks


def markdown_to_html(markdown: str, standalone: bool = False, style: str = 'github') -> str:
    """Convert Markdown to HTML."""
    lines = markdown.split('\n')
    blocks = parse_block(lines)
    html_content = '\n'.join(blocks)
    
    if standalone:
        css = {
            'github': '''body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;max-width:800px;margin:0 auto;padding:20px;line-height:1.6}
h1,h2,h3{margin-top:24px}h1{border-bottom:1px solid #eaecef;padding-bottom:8px}
code{background:#f6f8fa;padding:2px 6px;border-radius:3px}
pre{background:#f6f8fa;padding:16px;border-radius:6px;overflow:auto}
blockquote{border-left:4px solid #dfe2e5;margin:0;padding-left:16px;color:#6a737d}''',
            'minimal': '''body{font-family:sans-serif;max-width:800px;margin:0 auto;padding:20px}''',
            'print': '''body{font-family:Times New Roman,serif;max-width:800px;margin:0 auto;padding:20px}'''
        }
        
        html_content = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Markdown</title>
<style>{css.get(style, css['github'])}</style>
</head>
<body>
{html_content}
</body>
</html>'''
    
    return html_content


def main():
    parser = argparse.ArgumentParser(description='Markdown to HTML converter')
    parser.add_argument('input', nargs='?', help='Input Markdown file')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--to', '-t', choices=['html', 'json'], default='html', help='Output format')
    parser.add_argument('--render', '-r', help='Render inline Markdown')
    parser.add_argument('--standalone', '-s', action='store_true', help='Standalone HTML')
    parser.add_argument('--style', choices=['github', 'minimal', 'print'], default='github', help='CSS style')
    
    args = parser.parse_args()
    
    # Get markdown
    if args.render:
        markdown = args.render
    elif args.input:
        try:
            with open(args.input, 'r') as f:
                markdown = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        markdown = sys.stdin.read()
    
    # Convert
    if args.to == 'html':
        result = markdown_to_html(markdown, args.standalone, args.style)
    else:
        result = "JSON output not implemented"
    
    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        print(f"Saved to: {args.output}")
    else:
        print(result)


if __name__ == '__main__':
    main()
