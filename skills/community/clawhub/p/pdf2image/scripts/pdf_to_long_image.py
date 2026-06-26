#!/usr/bin/env python3
"""
PDF to Long Image Converter

Converts a multi-page PDF into a single vertical long image by concatenating all pages.

Usage:
    uv run python pdf_to_long_image.py <input.pdf> [output.png] [--scale 2]

Dependencies:
    uv pip install pymupdf pillow

Examples:
    uv run python pdf_to_long_image.py document.pdf
    uv run python pdf_to_long_image.py document.pdf output.png
    uv run python pdf_to_long_image.py document.pdf output.png --scale 3
"""

import argparse
import sys
from pathlib import Path

import fitz  # pymupdf
from PIL import Image


def pdf_to_long_image(pdf_path: str, output_path: str | None = None, scale: float = 2.0) -> str:
    """
    Convert a PDF to a single vertical long image.
    
    Args:
        pdf_path: Path to the input PDF file
        output_path: Path for the output image (default: input_long.png)
        scale: Scale factor for rendering (default: 2.0 for higher resolution)
    
    Returns:
        Path to the generated long image
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    if output_path is None:
        output_path = str(pdf_path.with_suffix("")) + "_long.png"
    
    # Open PDF
    doc = fitz.open(str(pdf_path))
    page_count = len(doc)
    
    if page_count == 0:
        raise ValueError("PDF has no pages")
    
    print(f"Converting {page_count} pages from {pdf_path.name}...")
    
    # Render each page to image
    images = []
    max_width = 0
    total_height = 0
    
    for page_num in range(page_count):
        page = doc[page_num]
        
        # Get page dimensions and apply scale
        mat = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
        
        max_width = max(max_width, img.width)
        total_height += img.height
        
        print(f"  Page {page_num + 1}/{page_count}: {img.width}x{img.height}")
    
    # Create combined image
    print(f"Creating long image: {max_width}x{total_height} pixels...")
    result = Image.new("RGB", (max_width, total_height), "white")
    
    y_offset = 0
    for img in images:
        # Center images that are narrower than max width
        x_offset = (max_width - img.width) // 2
        result.paste(img, (x_offset, y_offset))
        y_offset += img.height
    
    # Save result
    result.save(output_path, "PNG", optimize=True)
    
    # Get file size
    file_size = Path(output_path).stat().st_size
    size_mb = file_size / (1024 * 1024)
    
    print(f"Done! Saved to: {output_path}")
    print(f"  Dimensions: {max_width}x{total_height} pixels")
    print(f"  File size: {size_mb:.2f} MB")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF to vertical long image",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("output", nargs="?", help="Output image file (default: input_long.png)")
    parser.add_argument("--scale", type=float, default=2.0, 
                       help="Scale factor for rendering (default: 2.0)")
    
    args = parser.parse_args()
    
    try:
        pdf_to_long_image(args.input, args.output, args.scale)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()