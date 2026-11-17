#!/usr/bin/env python3
"""Convert images to PDF for printing."""
import argparse
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Pillow not installed. Run: pip install Pillow", file=sys.stderr)
    sys.exit(1)


def img_to_pdf(img_path, pdf_path, resolution=100.0):
    img = Image.open(img_path)
    if img.mode == "RGBA":
        img = img.convert("RGB")
    img.save(pdf_path, "PDF", resolution=resolution)
    img.close()
    return pdf_path


def main():
    parser = argparse.ArgumentParser(description="Convert images to PDF for printing")
    parser.add_argument("images", nargs="+", help="Image file paths")
    parser.add_argument("--resolution", type=float, default=100.0, help="PDF resolution in DPI")
    parser.add_argument("--output-dir", default=None, help="Output directory for PDFs")
    args = parser.parse_args()

    output_dir = args.output_dir or os.path.dirname(args.images[0]) or "."

    for img_path in args.images:
        if not os.path.exists(img_path):
            print(f"File not found: {img_path}", file=sys.stderr)
            continue
        base = os.path.splitext(os.path.basename(img_path))[0]
        pdf_path = os.path.join(output_dir, f"{base}.pdf")
        img_to_pdf(img_path, pdf_path, resolution=args.resolution)
        print(f"Created: {pdf_path}")


if __name__ == "__main__":
    main()