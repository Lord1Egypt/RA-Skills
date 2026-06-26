#!/usr/bin/env python3
"""md2pdf — Convert Markdown files to PDF using Pandoc.

Usage:
    python md2pdf.py <input.md> [output.pdf] [--css <style.css>]

Requires: pandoc (with a LaTeX engine), XeLaTeX recommended for CJK support.
"""

import argparse
import os
import subprocess
import sys
import shutil
from pathlib import Path


def check_dependencies():
    """Check if pandoc is available."""
    if not shutil.which("pandoc"):
        print("Error: pandoc is not installed or not in PATH.", file=sys.stderr)
        print("Install it from: https://pandoc.org/installing.html", file=sys.stderr)
        print("Or on Windows: choco install pandoc / winget install pandoc", file=sys.stderr)
        sys.exit(1)


def find_latex_engine():
    """Find an available LaTeX engine. Prefer XeLaTeX for CJK support."""
    engines = ["xelatex", "lualatex", "pdflatex"]
    for engine in engines:
        if shutil.which(engine):
            return engine
    return None


def convert_md_to_pdf(
    input_path: str,
    output_path: str = None,
    css_path: str = None,
    toc: bool = False,
    highlight_style: str = "tango",
) -> str:
    """Convert a Markdown file to PDF via Pandoc + LaTeX."""
    check_dependencies()

    input_file = Path(input_path).resolve()
    if not input_file.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    if output_path is None:
        output_path = str(input_file.with_suffix(".pdf"))
    output_file = Path(output_path).resolve()

    engine = find_latex_engine()
    if engine is None:
        print("Warning: No LaTeX engine found. PDF generation may fail.", file=sys.stderr)
        print("Install a LaTeX distribution: https://www.latex-project.org/get/", file=sys.stderr)
        print("Recommended: TeX Live (full) or MiKTeX", file=sys.stderr)
        engine = "xelatex"

    cmd = [
        "pandoc",
        str(input_file),
        "-o", str(output_file),
        "--pdf-engine", engine,
        "--highlight-style", highlight_style,
    ]

    if engine in ("xelatex", "lualatex"):
        cmd.extend([
            "-V", "mainfont=SimSun",
            "-V", "sansfont=SimHei",
            "-V", "monofont=Microsoft YaHei",
            "-V", "CJKmainfont=SimSun",
            "-V", "geometry:margin=1in",
        ])

    if toc:
        cmd.append("--toc")

    if css_path and Path(css_path).exists():
        cmd.extend(["--css", str(Path(css_path).resolve())])

    print(f"Converting: {input_file} -> {output_file}")
    print(f"Engine: {engine}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"Pandoc error:\n{result.stderr}", file=sys.stderr)
            sys.exit(1)
        print(f"Done: {output_file}")
        return str(output_file)
    except subprocess.TimeoutExpired:
        print("Error: Conversion timed out (120s).", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF using Pandoc")
    parser.add_argument("input", help="Input Markdown file path")
    parser.add_argument("output", nargs="?", help="Output PDF path (default: same name as input)")
    parser.add_argument("--css", help="Optional CSS file for styling")
    parser.add_argument("--toc", action="store_true", help="Include table of contents")
    parser.add_argument("--highlight", default="tango", help="Code highlight style (default: tango)")
    args = parser.parse_args()

    convert_md_to_pdf(
        input_path=args.input,
        output_path=args.output,
        css_path=args.css,
        toc=args.toc,
        highlight_style=args.highlight,
    )


if __name__ == "__main__":
    main()
