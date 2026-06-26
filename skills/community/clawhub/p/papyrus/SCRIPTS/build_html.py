#!/usr/bin/env python3
"""
build_html.py — Papyrus HTML Builder

Generates an annotated bilingual HTML from a paper's parsed content.
This script provides the structural skeleton; the LLM fills in translations
and commentary.

Usage:
    python3 build_html.py \
        --template TEMPLATES/paper.html \
        --paper-dir /tmp/papyrus_paper \
        --formula-dir /tmp/papyrus_formulas \
        --output /tmp/papyrus_paper/annotated.html

The actual translation and commentary are done by the LLM (not automated
by this script). This script handles:
1. Loading the HTML template
2. Discovering figure files and generating <img> tags
3. Injecting formula images
4. Setting up the bilingual block structure
"""

import argparse, os, sys, json, re
from pathlib import Path
from typing import Dict, List, Tuple


def discover_figures(paper_dir: str) -> Dict[str, str]:
    """Discover figure files in the paper directory.
    Returns {figure_name: file_path} mapping.
    """
    figures = {}
    figures_dir = os.path.join(paper_dir, "Figures")
    if os.path.isdir(figures_dir):
        for f in sorted(os.listdir(figures_dir)):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
                figures[f] = os.path.join(figures_dir, f)

    # Also check for x*.png files (appendix figures from arXiv HTML)
    for f in sorted(os.listdir(paper_dir)):
        if re.match(r'^x\d+\.png$', f):
            figures[f] = os.path.join(paper_dir, f)

    return figures


def discover_formulas(formula_dir: str) -> Dict[str, str]:
    """Discover formula PNG files in the formula directory."""
    formulas = {}
    if os.path.isdir(formula_dir):
        for f in sorted(os.listdir(formula_dir)):
            if f.endswith('.png'):
                formulas[f] = os.path.join(formula_dir, f)
    return formulas


def load_template(template_path: str) -> str:
    """Load the HTML template."""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def build_bilingual_block(english: str, chinese: str = "",
                          commentary: str = "") -> str:
    """Build a bilingual HTML block."""
    html = '<div class="bilingual-block">\n'
    html += f'  <div class="english-text">\n    {english}\n  </div>\n'
    if chinese:
        html += f'  <div class="chinese-text">\n    {chinese}\n  </div>\n'
    if commentary:
        html += f'  <div class="commentary">\n    {commentary}\n  </div>\n'
    html += '</div>\n'
    return html


def build_formula_block(img_name: str, caption: str = "") -> str:
    """Build a formula block with wireframe styling."""
    html = '<div class="formula-block">\n'
    html += f'  <img src="{img_name}" alt="Formula" style="max-width:100%; height:auto; display:block; margin:0 auto;">\n'
    html += '</div>\n'
    if caption:
        html += f'<div class="formula-caption">{caption}</div>\n'
    return html


def build_figure_block(img_name: str, caption: str = "") -> str:
    """Build a figure block."""
    html = '<div class="figure-container">\n'
    html += f'  <img src="{img_name}" alt="Figure" style="max-width:100%; height:auto; border-radius:4pt;">\n'
    html += '</div>\n'
    if caption:
        html += f'<div class="figure-caption">{caption}</div>\n'
    return html


def main():
    parser = argparse.ArgumentParser(description="Papyrus HTML Builder")
    parser.add_argument("--template", default="TEMPLATES/paper.html",
                        help="Path to HTML template")
    parser.add_argument("--paper-dir", required=True,
                        help="Directory containing paper source")
    parser.add_argument("--formula-dir", default="",
                        help="Directory containing formula PNGs")
    parser.add_argument("--output", default="annotated.html",
                        help="Output HTML file path")
    parser.add_argument("--title", default="Paper Deep-Read",
                        help="Document title")
    parser.add_argument("--authors", default="", help="Paper authors")
    parser.add_argument("--venue", default="", help="Publication venue")
    parser.add_argument("--year", default="", help="Publication year")
    args = parser.parse_args()

    print("📄 Papyrus HTML Builder")
    print(f"   Paper dir:  {args.paper_dir}")
    print(f"   Formula dir: {args.formula_dir}")
    print(f"   Template:   {args.template}")
    print(f"   Output:     {args.output}")
    print()

    # Load template
    template = load_template(args.template)

    # Discover figures
    figures = discover_figures(args.paper_dir)
    print(f"🔍 Found {len(figures)} figure(s):")
    for name, path in figures.items():
        size = os.path.getsize(path)
        print(f"   {name} ({size} bytes)")

    # Discover formulas
    formulas = {}
    if args.formula_dir:
        formulas = discover_formulas(args.formula_dir)
        print(f"\n🔢 Found {len(formulas)} formula(s):")
        for name in sorted(formulas.keys()):
            print(f"   {name}")

    # Fill in metadata
    template = template.replace("{{PAPER_TITLE}}", args.title)
    template = template.replace("{{PAPER_AUTHORS}}", args.authors)
    template = template.replace("{{PAPER_VENUE}}", args.venue)
    template = template.replace("{{PAPER_YEAR}}", args.year)

    # Write skeleton output (LLM fills in {{PAPER_BODY}} and {{PAPER_ABSTRACT}})
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f"\n✅ Skeleton written to: {args.output}")
    print("   Remaining placeholders: {{PAPER_ABSTRACT}}, {{PAPER_BODY}}, {{PAPER_CITATION}}")
    print("   ⚠️  These must be filled in by the LLM following SOP.md")


if __name__ == '__main__':
    main()
