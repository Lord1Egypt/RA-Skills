"""
PDF to Image Extractor for pdf-vision-reader skill
Converts PDF pages to high-resolution PNG images using PyMuPDF
"""
import sys
import os

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


def pdf_to_images(pdf_path, output_dir="pdf_extract", zoom=2.0, start_page=0, max_pages=None):
    """
    Convert PDF pages to PNG images.

    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save images
        zoom: Zoom factor (2.0 = 2x resolution for better OCR/visual quality)
        start_page: Page to start from (0-indexed)
        max_pages: Maximum number of pages to extract (None = all)

    Returns:
        List of image file paths
    """
    if not os.path.exists(pdf_path):
        print(f"ERROR: File not found: {pdf_path}")
        return []

    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    total = len(doc)

    if max_pages:
        end = min(start_page + max_pages, total)
    else:
        end = total

    image_paths = []
    for i in range(start_page, end):
        page = doc[i]
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        filename = f"page_{i+1:03d}.png"
        img_path = os.path.join(output_dir, filename)
        pix.save(img_path)
        image_paths.append(img_path)
        print(f"  [{i+1}/{total}] Extracted: {filename}")

    doc.close()
    print(f"\nTotal: {len(image_paths)} pages -> {output_dir}")
    return image_paths


def get_pdf_info(pdf_path):
    """Get basic PDF info without extracting images."""
    try:
        doc = fitz.open(pdf_path)
        info = {
            "pages": len(doc),
            "title": doc.metadata.get("title", ""),
            "author": doc.metadata.get("author", ""),
        }
        doc.close()
        return info
    except Exception as e:
        return {"error": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract.py <pdf_file> [output_dir] [zoom] [start_page] [max_pages]")
        print("  pdf_file     : Path to PDF file")
        print("  output_dir   : Output directory (default: pdf_extract)")
        print("  zoom         : Zoom factor, 2.0=high quality (default: 2.0)")
        print("  start_page   : Start page 0-indexed (default: 0)")
        print("  max_pages    : Max pages to extract (default: all)")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "pdf_extract"
    zoom = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
    start_page = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    max_pages = int(sys.argv[5]) if len(sys.argv) > 5 else None

    print(f"PDF: {pdf_path}")
    print(f"Output: {output_dir}")
    print(f"Zoom: {zoom}x")
    print(f"Pages: {start_page + 1} onwards" + (f", max {max_pages}" if max_pages else ""))
    print()

    # Show PDF info
    info = get_pdf_info(pdf_path)
    print(f"PDF Info: {info}")

    # Extract images
    print("Extracting...")
    paths = pdf_to_images(pdf_path, output_dir, zoom, start_page, max_pages)

    # Print all paths for use by next step
    print("\n=== IMAGE_PATHS ===")
    for p in paths:
        print(p)
    print("=== END_PATHS ===")

    return paths


if __name__ == "__main__":
    main()
