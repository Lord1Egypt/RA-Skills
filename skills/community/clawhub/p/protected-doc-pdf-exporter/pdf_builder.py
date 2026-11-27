"""
PDF Compiler and Image Formatter
Handles page range parsing, multi-engine PDF assembly (PyMuPDF / Pillow),
and format export options.
"""

import os
import re
from typing import List, Set

def parse_page_range(range_str: str, total_pages: int) -> List[int]:
    """
    Parses strings like 'all', '1-5', '1,3,5-8', '-5', '10-'
    Returns 0-based sorted unique page indices within range [0, total_pages - 1].
    """
    if not range_str or range_str.strip().lower() == 'all':
        return list(range(total_pages))

    result_pages: Set[int] = set()
    parts = [p.strip() for p in range_str.split(',') if p.strip()]

    for part in parts:
        if '-' in part:
            sub = part.split('-')
            start_str, end_str = sub[0].strip(), sub[1].strip()
            start = int(start_str) if start_str else 1
            end = int(end_str) if end_str else total_pages
            for p in range(start, end + 1):
                if 1 <= p <= total_pages:
                    result_pages.add(p - 1)
        else:
            p = int(part)
            if 1 <= p <= total_pages:
                result_pages.add(p - 1)

    return sorted(list(result_pages))

def compile_images_to_pdf(image_paths: List[str], output_pdf_path: str, quality: int = 95) -> str:
    """
    Assembles a list of image paths into a single PDF document.
    Uses PyMuPDF (fitz) for lossless vector-sharp page embedding,
    falling back to Pillow if fitz is not installed.
    """
    if not image_paths:
        raise ValueError("No images provided for PDF compilation.")

    output_pdf_path = os.path.abspath(output_pdf_path)
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

    try:
        import fitz  # PyMuPDF
        doc = fitz.open()
        for img_path in image_paths:
            img = fitz.open(img_path)
            rect = img[0].rect
            pdfbytes = img.convert_to_pdf()
            img.close()
            imgPDF = fitz.open('pdf', pdfbytes)
            page = doc.new_page(width=rect.width, height=rect.height)
            page.show_pdf_page(rect, imgPDF, 0)

        doc.save(output_pdf_path, deflate=True)
        doc.close()
    except ImportError:
        from PIL import Image
        pil_images = [Image.open(p).convert('RGB') for p in image_paths]
        pil_images[0].save(
            output_pdf_path,
            save_all=True,
            append_images=pil_images[1:],
            quality=quality
        )

    return output_pdf_path
