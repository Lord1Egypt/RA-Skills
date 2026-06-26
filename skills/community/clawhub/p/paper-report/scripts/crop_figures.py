#!/usr/bin/env python3
"""Crop figures/tables from a PDF at specified regions with 3x resolution.

Usage:
    python crop_figures.py <pdf_path> <output_dir> '<json_spec>'

The JSON spec is an array of objects:
    [
      {"page": 3, "rect": [30, 38, 565, 290], "name": "fig1_architecture"},
      {"page": 5, "rect": [30, 50, 565, 200], "name": "table1_metrics"}
    ]

- page: 0-indexed page number
- rect: [x0, y0, x1, y1] in PDF points (original coordinates, NOT pixel coords)
- name: output filename (without extension)
"""

import sys
import os
import json

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF not installed. Run: pip install PyMuPDF", file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <pdf_path> <output_dir> '<json_spec>'", file=sys.stderr)
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]
    spec_json = sys.argv[3]

    if not os.path.isfile(pdf_path):
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    try:
        specs = json.loads(spec_json)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON spec: {e}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    scale = 3  # 3x resolution for high-quality figure crops
    mat = fitz.Matrix(scale, scale)

    for i, spec in enumerate(specs):
        page_idx = spec["page"]
        rect_coords = spec["rect"]
        name = spec.get("name", f"figure_{i + 1}")

        if page_idx < 0 or page_idx >= doc.page_count:
            print(f"WARNING: Page {page_idx} out of range (0-{doc.page_count - 1}), skipping '{name}'")
            continue

        page = doc[page_idx]
        rect = fitz.Rect(*rect_coords)

        # Validate rect is within page bounds
        page_rect = page.rect
        if not page_rect.contains(rect):
            print(f"WARNING: Rect {rect_coords} extends beyond page bounds {list(page_rect)}, clamping.")
            rect = rect & page_rect  # intersection / clamp

        pix = page.get_pixmap(matrix=mat, clip=rect)
        out_path = os.path.join(output_dir, f"{name}.png")
        pix.save(out_path)
        print(f"[{i + 1}/{len(specs)}] {name}: page {page_idx}, {pix.width}x{pix.height} -> {out_path}")

    doc.close()
    print(f"\nDone. {len(specs)} figures cropped to {output_dir}")


if __name__ == "__main__":
    main()
