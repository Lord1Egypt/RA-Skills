#!/usr/bin/env python3
"""
Extract Images from PDF
Extracts embedded images from PDF pages with position metadata.
Used for preserving original images during translation.

Requirements:
    pip install pymupdf pillow

Usage:
    python extract_images.py <input.pdf> [output_dir]

Output:
    Creates images/ directory with extracted images and metadata JSON.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image
    import io
except ImportError:
    print("Error: Pillow not installed. Run: pip install pillow", file=sys.stderr)
    sys.exit(1)


def extract_images(pdf_path: str, output_dir: str) -> Dict[str, Any]:
    """
    Extract images from PDF with position metadata.

    Args:
        pdf_path: Path to the input PDF file
        output_dir: Directory to save extracted images

    Returns:
        Dict containing extraction manifest
    """
    pdf_path = Path(pdf_path).resolve()
    output_dir = Path(output_dir).resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Create output directories
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    # Open PDF
    doc = fitz.open(str(pdf_path))

    manifest = {
        "source_file": str(pdf_path),
        "total_pages": len(doc),
        "total_images": 0,
        "images": [],
    }

    image_counter = 0

    print(f"Extracting images from {len(doc)} pages...")

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Get image list from page
        image_list = page.get_images(full=True)

        for img_index, img_info in enumerate(image_list):
            try:
                # Extract image reference
                xref = img_info[0]

                # Get image data
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # Generate unique filename
                image_counter += 1
                image_name = f"img_{page_num + 1:03d}_{img_index + 1:02d}.{image_ext}"
                image_path = images_dir / image_name

                # Save image
                with open(image_path, "wb") as f:
                    f.write(image_bytes)

                # Get image dimensions
                try:
                    pil_img = Image.open(io.BytesIO(image_bytes))
                    width, height = pil_img.size
                except:
                    width, height = 0, 0

                # Find image position on page
                img_rects = page.get_image_rects(xref)
                positions = []
                for rect in img_rects:
                    positions.append(
                        {
                            "x": rect.x0,
                            "y": rect.y0,
                            "width": rect.width,
                            "height": rect.height,
                        }
                    )

                image_info = {
                    "image_id": image_counter,
                    "filename": image_name,
                    "page_number": page_num + 1,
                    "width_px": width,
                    "height_px": height,
                    "format": image_ext,
                    "xref": xref,
                    "positions": positions,
                }

                manifest["images"].append(image_info)
                manifest["total_images"] = image_counter

                print(
                    f"  Extracted: {image_name} ({width}x{height}px) from page {page_num + 1}"
                )

            except Exception as e:
                print(
                    f"  Warning: Failed to extract image {img_index + 1} from page {page_num + 1}: {e}",
                    file=sys.stderr,
                )

    doc.close()

    # Save manifest
    manifest_path = output_dir / "images_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\nExtraction complete!")
    print(f"Total images extracted: {image_counter}")
    print(f"Images directory: {images_dir}")
    print(f"Manifest saved: {manifest_path}")

    return manifest


def main():
    parser = argparse.ArgumentParser(
        description="Extract embedded images from PDF with metadata"
    )
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=None,
        help="Output directory for extracted images (default: same as PDF name)",
    )

    args = parser.parse_args()

    # Set default output directory
    if args.output_dir is None:
        pdf_path = Path(args.input_pdf)
        args.output_dir = pdf_path.parent / f"{pdf_path.stem}_extracted"

    try:
        manifest = extract_images(args.input_pdf, args.output_dir)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
