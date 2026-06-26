#!/usr/bin/env python3
"""
PDF Watermark Remover
=====================
Remove image-based watermarks from PDF files by deleting the drawing instructions
from content streams and removing XObject references.

Supports:
- Image watermarks (e.g. "Made with Gamma", Canva, etc.)
- Position-based detection (default: bottom-right corner)
- Custom watermark position/size matching
- Link annotation removal (optional)

Usage:
    python remove_watermark.py <input.pdf> <output.pdf> [--x-threshold 700] [--min-w 100] [--max-w 200] [--min-h 20] [--max-h 50] [--remove-links] [--link-domain gamma.app]

Requirements:
    pip install pymupdf
"""

import argparse
import re
import sys


def find_watermark_xrefs(page, x_threshold=700, min_w=100, max_w=200, min_h=20, max_h=50):
    """Find watermark image xrefs based on position and size."""
    images = page.get_images(full=True)
    watermark_xrefs = set()
    for img in images:
        xref = img[0]
        rects = page.get_image_rects(xref)
        for rect in rects:
            if (rect.x0 > x_threshold and
                min_w <= rect.width <= max_w and
                min_h <= rect.height <= max_h):
                watermark_xrefs.add(xref)
    return watermark_xrefs


def get_xobject_name_mapping(doc, page):
    """Build mapping from XObject names to xrefs for a page."""
    page_xref = page.xref
    page_obj_text = doc.xref_object(page_xref)

    # Find XObject indirect references
    xobject_refs = re.findall(r'/XObject\s+(\d+)\s+\d+\s+R', page_obj_text)

    name_to_xref = {}
    for xobj_ref in xobject_refs:
        xobj_xref = int(xobj_ref)
        xobj_text = doc.xref_object(xobj_xref)
        for m in re.finditer(r'/(\w+)\s+(\d+)\s+\d+\s+R', xobj_text):
            name = m.group(1)
            ref = int(m.group(2))
            name_to_xref[name] = ref

    # Also check page object directly
    for m in re.finditer(r'/(\w+)\s+(\d+)\s+\d+\s+R', page_obj_text):
        name = m.group(1)
        ref = int(m.group(2))
        if ref not in name_to_xref.values():
            name_to_xref[name] = ref

    return name_to_xref, xobject_refs


def remove_watermark_from_content_stream(doc, page, watermark_xrefs):
    """Remove watermark drawing instructions from page content streams."""
    name_to_xref, xobject_refs = get_xobject_name_mapping(doc, page)

    removed_count = 0

    # Remove Do instructions from content streams
    content_xrefs = page.get_contents()
    for cxref in content_xrefs:
        stream = doc.xref_stream(cxref)
        if stream is None:
            continue
        content = stream.decode("latin-1")

        for name, ref_xref in name_to_xref.items():
            if ref_xref in watermark_xrefs:
                # Pattern: q ... cm /Name Do Q (with save/restore and transform)
                pattern = r'q\s*[\d\.\-\s]+cm\s*/' + re.escape(name) + r'\s+Do\s*Q'
                new_content = re.sub(pattern, '', content)

                if new_content != content:
                    content = new_content
                    removed_count += 1
                else:
                    # Try without q/Q wrapper
                    pattern2 = r'/' + re.escape(name) + r'\s+Do'
                    new_content = re.sub(pattern2, '', content)
                    if new_content != content:
                        content = new_content
                        removed_count += 1

        if content != stream.decode("latin-1"):
            doc.update_stream(cxref, content.encode("latin-1"))

    # Remove watermark entries from XObject dictionaries
    for xobj_ref in xobject_refs:
        xobj_xref = int(xobj_ref)
        xobj_text = doc.xref_object(xobj_xref)
        modified = False
        for name, ref_xref in name_to_xref.items():
            if ref_xref in watermark_xrefs:
                pattern = r'\s*/' + re.escape(name) + r'\s+' + str(ref_xref) + r'\s+\d+\s+R'
                new_text = re.sub(pattern, '', xobj_text)
                if new_text != xobj_text:
                    xobj_text = new_text
                    modified = True
        if modified:
            doc.update_object(xobj_xref, xobj_text)

    return removed_count


def remove_link_annotations(page, domain=None):
    """Remove link annotations, optionally filtered by URI domain."""
    removed = 0
    # Access annotations via /Annots
    annots = page.annots()
    if annots is None:
        return 0

    to_remove = []
    for annot in annots:
        uri = annot.info.get("uri", "")
        if domain:
            if domain in uri:
                to_remove.append(annot)
        else:
            if uri:  # Remove all link annotations
                to_remove.append(annot)

    for annot in to_remove:
        page.delete_annot(annot)
        removed += 1

    return removed


def main():
    parser = argparse.ArgumentParser(description="Remove image watermarks from PDF files")
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("output", help="Output PDF file path")
    parser.add_argument("--x-threshold", type=float, default=700,
                        help="X position threshold for watermark detection (default: 700)")
    parser.add_argument("--min-w", type=float, default=100,
                        help="Minimum width for watermark detection (default: 100)")
    parser.add_argument("--max-w", type=float, default=200,
                        help="Maximum width for watermark detection (default: 200)")
    parser.add_argument("--min-h", type=float, default=20,
                        help="Minimum height for watermark detection (default: 20)")
    parser.add_argument("--max-h", type=float, default=50,
                        help="Maximum height for watermark detection (default: 50)")
    parser.add_argument("--remove-links", action="store_true",
                        help="Remove link annotations pointing to watermark domains")
    parser.add_argument("--link-domain", default=None,
                        help="Only remove links containing this domain (e.g. gamma.app)")

    args = parser.parse_args()

    try:
        import fitz  # pymupdf
    except ImportError:
        print("Error: pymupdf is required. Install with: pip install pymupdf")
        sys.exit(1)

    doc = fitz.open(args.input)
    total_watermarks = 0
    total_links = 0

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Find watermark xrefs
        watermark_xrefs = find_watermark_xrefs(
            page, args.x_threshold, args.min_w, args.max_w, args.min_h, args.max_h
        )

        if watermark_xrefs:
            print(f"Page {page_num + 1}: found {len(watermark_xrefs)} watermark(s)")
            removed = remove_watermark_from_content_stream(doc, page, watermark_xrefs)
            total_watermarks += removed
            print(f"  Removed {removed} drawing instruction(s)")

        # Remove link annotations if requested
        if args.remove_links:
            links = remove_link_annotations(page, args.link_domain)
            if links:
                total_links += links
                print(f"  Removed {links} link annotation(s)")

    doc.save(args.output, garbage=4)
    doc.close()

    print(f"\nDone!")
    print(f"  Watermark instructions removed: {total_watermarks}")
    print(f"  Link annotations removed: {total_links}")
    print(f"  Output: {args.output}")


if __name__ == "__main__":
    main()
