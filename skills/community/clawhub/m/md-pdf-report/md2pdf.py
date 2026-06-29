"""
md2pdf — Markdown → PDF (CJK-ready, weasyprint)
================================================

Convert a Markdown file to a styled PDF using weasyprint, with macOS-native
Chinese font support. Markdown is the single source of truth; the same .md
file is the editable artifact and the PDF is generated from it.

Usage
-----
    from md2pdf import md_to_pdf
    md_to_pdf("report.md")                    # produces report.pdf
    md_to_pdf("report.md", "out.pdf")         # custom output path
    md_to_pdf("report.md", keep_html=True)    # also save intermediate .html

CLI
---
    python -m md2pdf report.md
    python -m md2pdf report.md -o out.pdf
    python -m md2pdf report.md --keep-html    # debug: also save .html

macOS Setup Notes
-----------------
weasyprint requires pango/cairo/gobject C libraries (not bundled with pip).
On macOS:
    brew install pango
And before running, set:
    export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib
The bootstrap_macos() helper in this module does this automatically when
imported on macOS. On other OSes, install the equivalent dev packages.

Author: Helen Research
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
from typing import Optional

# ============ macOS Bootstrap ============
def bootstrap_macos():
    """
    On macOS, weasyprint needs the homebrew C library path because pango is
    not in the default dyld search path. Call this early (or rely on
    auto-bootstrap on import) to fix the env var.

    Returns True if the bootstrap was applied, False if not macOS.
    """
    if platform.system() != 'Darwin':
        return False
    if os.environ.get('DYLD_FALLBACK_LIBRARY_PATH'):
        return False  # user already set it
    homebrew_lib = '/opt/homebrew/lib'
    if os.path.exists(homebrew_lib):
        os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = homebrew_lib
    return True

# Auto-bootstrap on import. If you want to defer (e.g. for unit tests), set
# MD2PDF_NO_BOOTSTRAP=1 in the environment before importing this module.
if not os.environ.get('MD2PDF_NO_BOOTSTRAP'):
    bootstrap_macos()


# ============ Font Configuration ============
# macOS Chinese fonts. Use the .ttf files in Apple's font asset bundles —
# the .ttc files have PostScript outlines that don't work reliably with
# weasyprint. (Same constraint as reportlab.)
FONT_BODY    = '/System/Library/AssetsV2/com_apple_MobileAsset_Font8/10e7a462a671950b802274fad767b566ff8457d1.asset/AssetData/STXIHEI.ttf'
FONT_HEADING = '/System/Library/AssetsV2/com_apple_MobileAsset_Font8/53fe5be564086fefc7523ccd0a31200acf92e0e5.asset/AssetData/STHEITI.ttf'
FONT_KAITI   = '/System/Library/AssetsV2/com_apple_MobileAsset_Font8/6331c5916c361af1b83fb8b8b76ef2eece20c8eb.asset/AssetData/Kai.ttf'


# ============ CSS Template ============
DEFAULT_CSS = f"""
@page {{
    size: A4;
    margin: 2cm 2cm 2cm 2cm;
    @bottom-center {{
        content: counter(page) " / " counter(pages);
        font-family: 'Body', sans-serif;
        font-size: 9pt;
        color: #94A3B8;
    }}
}}

@font-face {{
    font-family: 'Body';
    src: url('file://{FONT_BODY}');
    font-weight: normal;
}}
@font-face {{
    font-family: 'Headline';
    src: url('file://{FONT_HEADING}');
    font-weight: bold;
}}
@font-face {{
    font-family: 'Kaiti';
    src: url('file://{FONT_KAITI}');
}}

body {{
    font-family: 'Body', 'STHeiti', 'Heiti SC', sans-serif;
    font-size: 10.5pt;
    line-height: 1.65;
    color: #1F2937;
    text-align: justify;
}}

h1 {{
    font-family: 'Headline', sans-serif;
    color: #0F172A;
    font-size: 22pt;
    text-align: center;
    margin: 0 0 8pt 0;
    font-weight: bold;
}}
h1 + p {{ text-align: center; color: #475569; font-size: 11pt; margin-top: 0; }}

h2 {{
    font-family: 'Headline', sans-serif;
    color: #0F172A;
    font-size: 15pt;
    margin: 20pt 0 10pt 0;
    padding-bottom: 4pt;
    border-bottom: 2px solid #1E293B;
    font-weight: bold;
}}
h3 {{
    font-family: 'Headline', sans-serif;
    color: #1E293B;
    font-size: 12pt;
    margin: 14pt 0 6pt 0;
    font-weight: bold;
}}
h4 {{
    font-family: 'Headline', sans-serif;
    color: #334155;
    font-size: 11pt;
    margin: 10pt 0 4pt 0;
    font-weight: bold;
}}

p {{ margin: 0 0 8pt 0; }}

ul, ol {{ margin: 0 0 8pt 0; padding-left: 22pt; }}
li {{ margin-bottom: 3pt; }}

a {{ color: #1D4ED8; text-decoration: none; border-bottom: 1px dotted #1D4ED8; }}
code {{
    font-family: 'Menlo', 'Monaco', monospace;
    background: #F1F5F9;
    padding: 1pt 4pt;
    border-radius: 3px;
    font-size: 9.5pt;
}}
pre {{
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 4pt;
    padding: 10pt;
    overflow-x: auto;
    font-size: 9.5pt;
    line-height: 1.5;
}}
pre code {{ background: none; padding: 0; }}

blockquote {{
    border-left: 3px solid #CBD5E1;
    padding: 4pt 12pt;
    margin: 8pt 0;
    color: #475569;
    font-family: 'Kaiti', 'Body', sans-serif;
}}

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 10pt 0 12pt 0;
    font-size: 9.5pt;
}}
th {{
    background: #1E293B;
    color: white;
    padding: 7pt 8pt;
    text-align: left;
    font-family: 'Headline', sans-serif;
    font-weight: bold;
}}
td {{
    padding: 6pt 8pt;
    border-bottom: 1px solid #E2E8F0;
    vertical-align: top;
}}
tr:nth-child(even) td {{ background: #F8FAFC; }}

hr {{
    border: none;
    border-top: 1px solid #E2E8F0;
    margin: 16pt 0;
}}

/* Custom classes (set via <div class="..."> in MD) */
.callout {{
    background: #FEF2F2;
    border: 1px solid #FCA5A5;
    border-radius: 4pt;
    padding: 10pt 14pt;
    margin: 10pt 0;
    color: #7F1D1D;
    font-family: 'Kaiti', 'Body', sans-serif;
}}
.note {{
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 4pt;
    padding: 10pt 14pt;
    margin: 10pt 0;
    color: #64748B;
    font-size: 9.5pt;
}}
.warn {{
    background: #FFFBEB;
    border: 1px solid #FCD34D;
    border-radius: 4pt;
    padding: 10pt 14pt;
    margin: 10pt 0;
    color: #78350F;
}}
"""


# ============ Markdown → HTML ============
def md_to_html(md_text: str, css: Optional[str] = None, title: str = "Report") -> str:
    """Convert Markdown text to a full HTML document with embedded CSS."""
    import markdown
    md = markdown.Markdown(extensions=[
        'extra',      # tables, fenced code, footnotes, abbr, def_list
        'sane_lists', # better list handling
        'toc',        # TOC support
        'meta',       # metadata support
    ])
    body_html = md.convert(md_text)
    css_str = css or DEFAULT_CSS
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>{css_str}</style>
</head>
<body>
{body_html}
</body>
</html>
"""


# ============ HTML → PDF ============
def html_to_pdf(html: str, pdf_path: str):
    """Render HTML to PDF using weasyprint."""
    from weasyprint import HTML
    HTML(string=html).write_pdf(pdf_path)


# ============ Main entry point ============
def md_to_pdf(
    md_path: str,
    pdf_path: Optional[str] = None,
    *,
    keep_html: bool = False,
    css: Optional[str] = None,
    base_url: Optional[str] = None,
) -> str:
    """
    Convert a Markdown file to a styled PDF.

    Args:
        md_path: Path to the input .md file
        pdf_path: Output .pdf path. Defaults to same path with .pdf extension
        keep_html: If True, also save intermediate .html for debugging
        css: Custom CSS to override DEFAULT_CSS
        base_url: Base URL for resolving relative paths in MD (e.g. images)

    Returns:
        Absolute path to the generated PDF
    """
    md_path = Path(md_path).resolve()
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    if pdf_path is None:
        pdf_path = md_path.with_suffix('.pdf')
    else:
        pdf_path = Path(pdf_path).resolve()

    md_text = md_path.read_text(encoding='utf-8')
    title = md_path.stem

    html = md_to_html(md_text, css=css, title=title)
    html_to_pdf(html, str(pdf_path))

    if keep_html:
        html_path = pdf_path.with_suffix('.html')
        html_path.write_text(html, encoding='utf-8')

    return str(pdf_path)


# ============ CLI ============
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Convert Markdown to a styled PDF (CJK-ready).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m md2pdf report.md
  python -m md2pdf report.md -o final.pdf
  python -m md2pdf report.md --keep-html   # also save report.html for debug
        """
    )
    parser.add_argument('md_file', help='Input Markdown file')
    parser.add_argument('-o', '--output', help='Output PDF path (default: same name .pdf)')
    parser.add_argument('--keep-html', action='store_true',
                        help='Also save intermediate HTML for debugging')
    args = parser.parse_args()

    out = md_to_pdf(args.md_file, args.output, keep_html=args.keep_html)
    size = Path(out).stat().st_size
    print(f"✓ PDF generated: {out} ({size:,} bytes = {size/1024:.1f} KB)")


if __name__ == '__main__':
    main()
