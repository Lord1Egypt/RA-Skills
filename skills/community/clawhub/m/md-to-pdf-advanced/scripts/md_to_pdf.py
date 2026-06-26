#!/usr/bin/env python3
"""
Markdown to PDF Converter
Supports multiple backends: WeasyPrint (default), Pandoc
"""

import argparse
import sys
import os
import subprocess
import tempfile
import shutil
from pathlib import Path

# Default CSS for nice PDF output
DEFAULT_CSS = """
@page {
    size: A4;
    margin: 25mm;
    @bottom-center {
        content: counter(page);
        font-size: 9pt;
        color: #666;
    }
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
    max-width: 100%;
}

h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    font-weight: 600;
}

h1 { font-size: 2em; border-bottom: 2px solid #eee; padding-bottom: 0.3em; }
h2 { font-size: 1.5em; border-bottom: 1px solid #eee; padding-bottom: 0.3em; }
h3 { font-size: 1.25em; }

p {
    margin: 0.8em 0;
}

a {
    color: #0366d6;
    text-decoration: none;
}

code {
    background-color: #f6f8fa;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 0.9em;
}

pre {
    background-color: #f6f8fa;
    padding: 16px;
    border-radius: 6px;
    overflow-x: auto;
    line-height: 1.45;
}

pre code {
    background: none;
    padding: 0;
}

blockquote {
    border-left: 4px solid #dfe2e5;
    padding-left: 1em;
    margin-left: 0;
    color: #6a737d;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

th, td {
    border: 1px solid #dfe2e5;
    padding: 8px 12px;
    text-align: left;
}

th {
    background-color: #f6f8fa;
    font-weight: 600;
}

tr:nth-child(even) {
    background-color: #f8f9fa;
}

img {
    max-width: 100%;
    height: auto;
}

ul, ol {
    padding-left: 2em;
}

li {
    margin: 0.3em 0;
}

hr {
    border: none;
    border-top: 1px solid #e1e4e8;
    margin: 2em 0;
}
"""


def check_weasyprint():
    """Check if WeasyPrint is available"""
    try:
        import weasyprint
        return True
    except ImportError:
        return False


def check_pandoc():
    """Check if pandoc is available"""
    return shutil.which("pandoc") is not None


def check_wkhtmltopdf():
    """Check if wkhtmltopdf is available"""
    return shutil.which("wkhtmltopdf") is not None


def install_weasyprint():
    """Try to install WeasyPrint automatically"""
    print("WeasyPrint not found. Attempting to install...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--quiet",
            "weasyprint", "markdown", "Pygments"
        ])
        print("Successfully installed WeasyPrint!")
        return True
    except Exception as e:
        print(f"Failed to install WeasyPrint: {e}")
        return False


def convert_with_weasyprint(input_path, output_path, css_content=None, orientation="portrait"):
    """Convert markdown to PDF using WeasyPrint"""
    try:
        import markdown
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
    except ImportError:
        if not install_weasyprint():
            raise RuntimeError("WeasyPrint is required but could not be installed")
        import markdown
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration

    # Read markdown
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=[
        'tables',
        'fenced_code',
        'toc',
        'nl2br'
    ])
    html_body = md.convert(md_content)

    # Wrap in full HTML document
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Document</title>
</head>
<body>
    {html_body}
</body>
</html>"""

    # Add syntax highlighting if Pygments is available
    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name, guess_lexer
        from pygments.formatters import HtmlFormatter
        import re

        def highlight_code(match):
            code = match.group(2)
            lang = match.group(1) or ""
            try:
                if lang:
                    lexer = get_lexer_by_name(lang, stripall=True)
                else:
                    lexer = guess_lexer(code)
                formatter = HtmlFormatter(style='github', noclasses=True)
                return highlight(code, lexer, formatter)
            except:
                return match.group(0)

        html_content = re.sub(
            r'<pre><code(?: class="language-([^"]*)")?>(.*?)</code></pre>',
            highlight_code,
            html_content,
            flags=re.DOTALL
        )
    except ImportError:
        pass

    # Use custom CSS or default
    css_to_use = css_content if css_content else DEFAULT_CSS

    # Adjust page orientation
    if orientation == "landscape":
        css_to_use = css_to_use.replace("size: A4;", "size: A4 landscape;")

    # Convert to PDF
    font_config = FontConfiguration()
    html = HTML(string=html_content, base_url=str(Path(input_path).parent))
    css = CSS(string=css_to_use, font_config=font_config)

    html.write_pdf(output_path, stylesheets=[css], font_config=font_config)
    print(f"✓ PDF created: {output_path}")
    return True


def convert_with_pandoc(input_path, output_path, orientation="portrait"):
    """Convert markdown to PDF using Pandoc + wkhtmltopdf"""
    if not check_pandoc():
        raise RuntimeError("pandoc is not installed. Install it with: apt install pandoc")

    # Pandoc can output PDF directly if wkhtmltopdf or latex is available
    cmd = [
        "pandoc",
        input_path,
        "-o", output_path,
        "--pdf-engine=wkhtmltopdf" if check_wkhtmltopdf() else "--pdf-engine=xelatex",
        "-V", "geometry:margin=1in",
        "--highlight-style=tango"
    ]

    if orientation == "landscape":
        cmd.extend(["-V", "geometry:landscape"])

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ PDF created: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Pandoc error: {e.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF")
    parser.add_argument("input", help="Input markdown file")
    parser.add_argument("output", help="Output PDF file")
    parser.add_argument("--backend", choices=["weasyprint", "pandoc", "auto"],
                        default="auto", help="Conversion backend")
    parser.add_argument("--css", help="Custom CSS file")
    parser.add_argument("--orientation", choices=["portrait", "landscape"],
                        default="portrait", help="Page orientation")
    parser.add_argument("--margin", help="Page margin (e.g., 20mm, 1in)")

    args = parser.parse_args()

    # Validate input
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    # Load custom CSS if provided
    css_content = None
    if args.css:
        if not os.path.exists(args.css):
            print(f"Warning: CSS file not found: {args.css}")
        else:
            with open(args.css, 'r', encoding='utf-8') as f:
                css_content = f.read()

    # Determine backend
    backend = args.backend
    if backend == "auto":
        if check_weasyprint():
            backend = "weasyprint"
        elif check_pandoc():
            backend = "pandoc"
        else:
            print("No backend found. Attempting to install WeasyPrint...")
            backend = "weasyprint"

    # Convert
    try:
        if backend == "weasyprint":
            convert_with_weasyprint(args.input, args.output, css_content, args.orientation)
        elif backend == "pandoc":
            convert_with_pandoc(args.input, args.output, args.orientation)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
