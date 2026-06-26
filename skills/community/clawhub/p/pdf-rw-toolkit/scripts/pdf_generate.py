#!/usr/bin/env python3
"""Generate PDF from HTML, Markdown, or HTML string using WeasyPrint."""

import argparse
import sys
import os


def main():
    parser = argparse.ArgumentParser(description="Generate PDF from HTML/Markdown")
    parser.add_argument("input", nargs="?", help="Input file (HTML or Markdown)")
    parser.add_argument("output", help="Output PDF path")
    parser.add_argument("--html", help="HTML string (instead of input file)")
    parser.add_argument("--css", help="Optional CSS file for styling")
    args = parser.parse_args()

    try:
        from weasyprint import HTML, CSS
    except ImportError:
        print("Error: weasyprint not installed. Run: pip install weasyprint", file=sys.stderr)
        sys.exit(1)

    stylesheets = []
    if args.css:
        stylesheets.append(CSS(filename=args.css))

    if args.html:
        html_content = args.html
    elif args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()

        if args.input.endswith(".md"):
            try:
                import markdown
                html_content = markdown.markdown(content, extensions=["tables", "fenced_code"])
            except ImportError:
                # Fallback: wrap in <pre> if markdown lib not available
                html_content = f"<pre>{content}</pre>"
                print("Warning: 'markdown' package not installed, using raw text", file=sys.stderr)
        else:
            html_content = content
    else:
        print("Error: provide either an input file or --html", file=sys.stderr)
        sys.exit(1)

    # Wrap in basic HTML structure if not already a full document
    if "<html" not in html_content.lower():
        html_content = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
body {{ font-family: sans-serif; margin: 2cm; line-height: 1.5; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
th {{ background: #f5f5f5; }}
pre, code {{ background: #f5f5f5; padding: 2px 6px; border-radius: 3px; }}
</style>
</head><body>{html_content}</body></html>"""

    HTML(string=html_content).write_pdf(args.output, stylesheets=stylesheets or None)
    size = os.path.getsize(args.output)
    print(f"Generated {args.output} ({size:,} bytes)")


if __name__ == "__main__":
    main()
