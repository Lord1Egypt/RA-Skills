#!/usr/bin/env python3
"""
PDF to Images Converter
Converts each page of a PDF document to high-quality PNG images.
Used for multimodal analysis of PDF layout and formatting.

Requirements:
    pip install pymupdf pillow

Usage:
    python pdf_to_images.py <input.pdf> [output_dir] [--dpi 150]

Output:
    Creates page_001.png, page_002.png, etc. in the output directory.
    Also outputs a JSON manifest with page dimensions.
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow not installed. Run: pip install pillow", file=sys.stderr)
    sys.exit(1)


def pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 150) -> dict:
    """
    Convert PDF pages to PNG images.

    Args:
        pdf_path: Path to the input PDF file
        output_dir: Directory to save output images
        dpi: Resolution for output images (default 150)

    Returns:
        Dict containing manifest with page info
    """
    pdf_path = Path(pdf_path).resolve()
    output_dir = Path(output_dir).resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Open PDF
    doc = fitz.open(str(pdf_path))

    manifest = {
        "source_file": str(pdf_path),
        "total_pages": len(doc),
        "dpi": dpi,
        "pages": [],
    }

    # Calculate zoom factor based on DPI
    zoom = dpi / 72  # 72 is the default PDF DPI

    print(f"Converting {len(doc)} pages at {dpi} DPI...")

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Create transformation matrix for high resolution
        mat = fitz.Matrix(zoom, zoom)

        # Render page to pixmap
        pix = page.get_pixmap(matrix=mat)

        # Generate output filename
        output_name = f"page_{page_num + 1:03d}.png"
        output_path = output_dir / output_name

        # Save as PNG
        pix.save(str(output_path))

        # Get page dimensions
        rect = page.rect

        page_info = {
            "page_number": page_num + 1,
            "image_file": output_name,
            "width_px": pix.width,
            "height_px": pix.height,
            "width_pt": rect.width,
            "height_pt": rect.height,
            "rotation": page.rotation,
        }
        manifest["pages"].append(page_info)

        print(
            f"  Page {page_num + 1}/{len(doc)}: {output_name} ({pix.width}x{pix.height}px)"
        )

    doc.close()

    # Save manifest
    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\nConversion complete!")
    print(f"Output directory: {output_dir}")
    print(f"Manifest saved: {manifest_path}")

    return manifest


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF pages to PNG images for layout analysis"
    )
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=None,
        help="Output directory for images (default: same as PDF name)",
    )
    parser.add_argument(
        "--dpi",
        "-d",
        type=int,
        default=150,
        help="Output image resolution in DPI (default: 150)",
    )

    args = parser.parse_args()

    # Set default output directory
    if args.output_dir is None:
        pdf_path = Path(args.input_pdf)
        args.output_dir = pdf_path.parent / f"{pdf_path.stem}_pages"

    try:
        manifest = pdf_to_images(args.input_pdf, args.output_dir, args.dpi)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
