#!/usr/bin/env python3
"""Convert each page of a PDF to a PNG image at 2x resolution."""

import sys
import os

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF not installed. Run: pip install PyMuPDF", file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <pdf_path> <output_dir>", file=sys.stderr)
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isfile(pdf_path):
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    scale = 2  # 2x resolution for clear reading
    mat = fitz.Matrix(scale, scale)

    for page_num in range(total_pages):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=mat)
        out_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(out_path)
        print(f"Page {page_num + 1}/{total_pages}: {pix.width}x{pix.height} -> {out_path}")

    doc.close()
    print(f"\nDone. {total_pages} pages rendered to {output_dir}")


if __name__ == "__main__":
    main()
