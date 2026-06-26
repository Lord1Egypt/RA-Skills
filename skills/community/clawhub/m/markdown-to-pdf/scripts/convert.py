#!/usr/bin/env python3
import argparse
import markdown
import pygments
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
import subprocess
import tempfile
import os
import re

DEFAULT_CSS = """
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
    color: #333;
}
h1, h2, h3, h4, h5, h6 {
    color: #111;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}
code {
    background-color: #f5f5f5;
    padding: 0.2em 0.4em;
    border-radius: 3px;
}
pre {
    background-color: #f5f5f5;
    padding: 1em;
    border-radius: 5px;
    overflow-x: auto;
}
pre code {
    background: none;
    padding: 0;
}
img {
    max-width: 100%;
    height: auto;
}
blockquote {
    border-left: 4px solid #ddd;
    padding-left: 1em;
    color: #666;
    margin-left: 0;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}
table, th, td {
    border: 1px solid #ddd;
}
th, td {
    padding: 0.5em;
    text-align: left;
}
"""

def highlight_code_blocks(html_content):
    """Add syntax highlighting to code blocks using Pygments."""
    # Pattern to find code blocks with language info
    code_block_pattern = re.compile(r'<pre><code(?: class="language-(\w+)")?>(.*?)</code></pre>', re.DOTALL)
    
    def replace_match(match):
        language = match.group(1)
        code = match.group(2)
        # Unescape HTML entities
        code = re.sub(r'&lt;', '<', code)
        code = re.sub(r'&gt;', '>', code)
        code = re.sub(r'&amp;', '&', code)
        
        try:
            if language:
                lexer = get_lexer_by_name(language.lower())
            else:
                lexer = guess_lexer(code)
        except:
            return f'<pre><code>{match.group(2)}</code></pre>'
        
        formatter = HtmlFormatter(style='default')
        highlighted = pygments.highlight(code, lexer, formatter)
        return highlighted
    
    return code_block_pattern.sub(replace_match, html_content)

def convert_markdown_to_pdf(input_path, output_path, custom_css_path=None):
    # Read Markdown
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert Markdown to HTML
    html = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])
    
    # Add syntax highlighting
    html = highlight_code_blocks(html)
    
    # Get CSS
    if custom_css_path and os.path.exists(custom_css_path):
        with open(custom_css_path, 'r', encoding='utf-8') as f:
            css = f.read()
    else:
        css = DEFAULT_CSS
    
    # Add Pygments CSS if we did highlighting
    pygments_css = HtmlFormatter().get_style_defs('.highlight')
    
    # Complete HTML document
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{os.path.basename(input_path)}</title>
    <style>
    {css}
    {pygments_css}
    </style>
</head>
<body>
{html}
</body>
</html>
"""
    
    # Write temporary HTML file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp:
        tmp.write(full_html)
        tmp_path = tmp.name
    
    try:
        # Run wkhtmltopdf
        cmd = [
            'wkhtmltopdf',
            '--enable-local-file-access',
            tmp_path,
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Error generating PDF: {result.stderr}")
            return False
        
        print(f"✅ Successfully converted:")
        print(f"   Input:  {input_path}")
        print(f"   Output: {output_path}")
        return True
    
    finally:
        # Clean up temporary file
        os.unlink(tmp_path)

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown file to PDF")
    parser.add_argument("input", help="Input Markdown file path")
    parser.add_argument("output", help="Output PDF file path")
    parser.add_argument("--css", help="Custom CSS file path (optional)")
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"❌ Input file not found: {args.input}")
        return
    
    convert_markdown_to_pdf(args.input, args.output, args.css)

if __name__ == "__main__":
    main()
