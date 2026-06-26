#!/usr/bin/env python3
"""
Convert Markdown documentation to Word (docx) using pandoc.
Pandoc properly embeds images when --resource-path is set to the project directory.

Usage:
    python convert_to_docx.py <markdown_file> [output_dir]
    
Example:
    python convert_to_docx.py "D:\Project\myapp_页面文档.md"
"""

import os
import sys
import subprocess
from pathlib import Path


def find_pandoc():
    """Find pandoc executable."""
    locations = [
        "pandoc",
        "C:\\Program Files\\Pandoc\\pandoc.exe",
        "C:\\Program Files (x86)\\Pandoc\\pandoc.exe",
    ]
    
    for loc in locations:
        try:
            result = subprocess.run(
                [loc, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return loc
        except:
            continue
    
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, timeout=5)
        return "pandoc"
    except:
        pass
    
    return None


def convert_to_docx(markdown_path, output_dir=None):
    """Convert Markdown to Word document using pandoc.
    
    Pandoc embeds images when:
    1. Image paths in markdown are relative or absolute paths (not URLs)
    2. --resource-path points to the directory containing the images
    """
    pandoc = find_pandoc()
    if not pandoc:
        return None, "pandoc not found. Please install pandoc from https://pandoc.org/"
    
    md_path = Path(markdown_path)
    if not md_path.exists():
        return None, f"File not found: {markdown_path}"
    
    # Determine output path
    if output_dir:
        output_path = Path(output_dir) / f"{md_path.stem}.docx"
    else:
        output_path = md_path.parent / f"{md_path.stem}.docx"
    
    # Build pandoc command
    # --resource-path tells pandoc where to find images
    cmd = [
        pandoc,
        str(md_path),
        "-o", str(output_path),
        "--resource-path", str(md_path.parent),
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return str(output_path), None
        else:
            return None, result.stderr
    except subprocess.TimeoutExpired:
        return None, "Conversion timed out"
    except Exception as e:
        return None, str(e)


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    if len(sys.argv) < 2:
        print("Usage: python convert_to_docx.py <markdown_file> [output_dir]")
        sys.exit(1)
    
    markdown_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"Converting: {markdown_path}")
    
    output_path, error = convert_to_docx(markdown_path, output_dir)
    
    if error:
        print(f"[ERROR] {error}")
        sys.exit(1)
    else:
        print(f"[OK] Generated: {output_path}")
