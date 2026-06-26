#!/usr/bin/env python3
"""
OCR processing for scanned PDFs using pytesseract.
Includes image preprocessing to improve recognition accuracy.
"""

import io
import os
from typing import List, Optional

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract


# ─── Language Code Mapping ────────────────────────────────────────────────────
LANG_CODE_MAP = {
    "eng": "eng",
    "chi_sim": "chi_sim",  # Simplified Chinese
    "chi_tra": "chi_tra",  # Traditional Chinese
    "jpn": "jpn",  # Japanese
    "kor": "kor",  # Korean
    "fra": "fra",  # French
    "deu": "deu",  # German
    "spa": "spa",  # Spanish
    "por": "por",  # Portuguese
    "rus": "rus",  # Russian
    "ara": "ara",  # Arabic
    "hin": "hin",  # Hindi
}


def get_tesseract_lang_codes(languages: List[str]) -> str:
    """
    Convert a list of language names to tesseract language codes.

    Args:
        languages: List of language names (e.g., ["eng", "chi_sim"]).

    Returns:
        Tesseract language code string (e.g., "eng+chi_sim").
    """
    codes = []
    for lang in languages:
        code = LANG_CODE_MAP.get(lang, lang)
        if code not in codes:
            codes.append(code)
    return "+".join(codes)


def preprocess_for_ocr(image: Image.Image) -> Image.Image:
    """
    Preprocess an image to improve OCR accuracy.

    Steps:
    1. Convert to grayscale
    2. Increase contrast
    3. Sharpen
    4. Deskew (optional)

    Args:
        image: PIL Image object.

    Returns:
        Preprocessed PIL Image object.
    """
    # Convert to grayscale
    img = image.convert("L")

    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)

    # Sharpen
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.3)

    # Auto-invert if background is dark
    extrema = img.getextrema()
    if extrema[0] < 50:  # Dark background
        img = ImageOps.invert(img)

    return img


def ocr_image(
    image_path: str,
    languages: Optional[List[str]] = None,
    preprocess: bool = True,
    psm: int = 6,
) -> str:
    """
    Perform OCR on an image file.

    Args:
        image_path: Path to the image file.
        languages: List of language codes for OCR (e.g., ["eng", "chi_sim"]).
            Defaults to ["eng"].
        preprocess: Whether to preprocess the image before OCR.
        psm: Page segmentation mode (0-13). Default 6 = fully automatic.

    Returns:
        Recognized text from the image.
    """
    if languages is None:
        languages = ["eng"]

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    img = Image.open(image_path)

    if preprocess:
        img = preprocess_for_ocr(img)

    lang_code = get_tesseract_lang_codes(languages)

    # Configure tesseract
    config = f"--psm {psm}"

    try:
        text = pytesseract.image_to_string(img, lang=lang_code, config=config)
    except Exception as e:
        raise RuntimeError(f"Tesseract OCR failed: {e}")

    return text


def ocr_image_bytes(
    image_bytes: bytes,
    languages: Optional[List[str]] = None,
    preprocess: bool = True,
    psm: int = 6,
) -> str:
    """
    Perform OCR on image bytes.

    Args:
        image_bytes: Image data as bytes.
        languages: List of language codes for OCR.
        preprocess: Whether to preprocess the image.
        psm: Page segmentation mode.

    Returns:
        Recognized text from the image.
    """
    if languages is None:
        languages = ["eng"]

    img = Image.open(io.BytesIO(image_bytes))

    if preprocess:
        img = preprocess_for_ocr(img)

    lang_code = get_tesseract_lang_codes(languages)
    config = f"--psm {psm}"

    try:
        text = pytesseract.image_to_string(img, lang=lang_code, config=config)
    except Exception as e:
        raise RuntimeError(f"Tesseract OCR failed: {e}")

    return text


def ocr_pdf_pages(
    pdf_path: str,
    languages: Optional[List[str]] = None,
    preprocess: bool = True,
    psm: int = 6,
    start_page: int = 0,
    end_page: Optional[int] = None,
) -> List[str]:
    """
    Perform OCR on each page of a PDF (for scanned PDFs).

    Args:
        pdf_path: Path to the scanned PDF file.
        languages: List of language codes for OCR.
        preprocess: Whether to preprocess each page image.
        psm: Page segmentation mode.
        start_page: 0-based start page.
        end_page: 0-based end page (inclusive). None = all pages.

    Returns:
        List of recognized text per page.
    """
    # Import here to avoid circular dependency
    from .pdf_extractor import render_page_as_image

    if languages is None:
        languages = ["eng"]

    try:
        import fitz
    except ImportError:
        raise RuntimeError("PyMuPDF (fitz) is required for PDF OCR. Install with: pip install pymupdf")

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()

    if end_page is None:
        end_page = total_pages - 1

    results = []
    for page_num in range(start_page, min(end_page + 1, total_pages)):
        img_bytes = render_page_as_image(pdf_path, page_num, dpi=300)
        text = ocr_image_bytes(img_bytes, languages=languages, preprocess=preprocess, psm=psm)
        results.append(text)

    return results


def get_ocr_confidence(image_path: str, languages: Optional[List[str]] = None) -> float:
    """
    Get OCR confidence score for an image.

    Args:
        image_path: Path to the image file.
        languages: List of language codes.

    Returns:
        Average confidence score (0.0 - 1.0).
    """
    if languages is None:
        languages = ["eng"]

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    img = Image.open(image_path)
    img = preprocess_for_ocr(img)

    lang_code = get_tesseract_lang_codes(languages)

    try:
        data = pytesseract.image_to_data(img, lang=lang_code, output_type=pytesseract.Output.DICT)
        confidences = [int(conf) for conf in data["conf"] if conf != "-1"]
        if confidences:
            return sum(confidences) / len(confidences) / 100.0
        return 0.0
    except Exception:
        return 0.0
