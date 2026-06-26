#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR engine wrapper - orchestrates multiple OCR engines.
Strategy: PaddleOCR Cloud (primary, if configured) → RapidOCR (fallback) → pix2tex (LaTeX formulas)
"""

import re
import os
from pathlib import Path
from typing import List, Tuple, Optional

from ocr.rapidocr import run_rapidocr, run_latexocr, looks_like_latex
from ocr.paddleocr import run_paddleocr_cloud, is_configured as is_paddleocr_configured

# Image extensions supported for OCR
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff", ".tif"}


def ocr_fallback(input_path: Path, verbose: bool = False) -> str:
    """OCR an image file using a three-engine strategy.
    
    Strategy:
    1. PaddleOCR Cloud - cloud API for enhanced recognition (if configured, used first)
    2. RapidOCR - fast local fallback for general text (Chinese + English)
    3. pix2tex (LaTeX-OCR) - specialized for math formula images -> LaTeX
    
    Engine selection logic:
    - PaddleOCR Cloud runs first if API is configured (env vars set)
    - RapidOCR runs as local fallback
    - LaTeX-OCR only runs when the image appears to be a formula:
      - Both OCRs found no text, OR
      - Result is very short (< 15 chars) AND contains no Chinese chars
    """
    parts = []
    primary_text = None  # Track primary OCR result for comparison
    
    # --- 1. PaddleOCR Cloud (primary, if configured) ---
    if is_paddleocr_configured():
        if verbose:
            print(f"[OCR] Running PaddleOCR Cloud on {input_path.name}...")
        paddle_text = run_paddleocr_cloud(input_path, verbose=verbose)
        if paddle_text:
            primary_text = paddle_text
            parts.append(paddle_text)
            if verbose:
                print(f"[OCR] PaddleOCR Cloud: {len(paddle_text)} chars")
        else:
            if verbose:
                print(f"[OCR] PaddleOCR Cloud returned empty, falling back to RapidOCR...")
    
    # --- 2. RapidOCR fallback (if PaddleOCR failed or not configured) ---
    if not primary_text:  # Only run if primary didn't succeed
        if verbose:
            print(f"[OCR] Running RapidOCR on {input_path.name}...")
        rapid_text = run_rapidocr(input_path)
        if rapid_text:
            primary_text = rapid_text
            parts.append(rapid_text)
            if verbose:
                print(f"[OCR] RapidOCR: {len(rapid_text)} chars")
    
    # --- 3. pix2tex for LaTeX formulas ---
    rapid_clean = (primary_text or "").strip()
    rapid_len = len(rapid_clean)
    
    # Heuristic: if OCR found Chinese chars or long text, it's not a formula image
    has_cjk = bool(re.search(r"[\u4e00-\u9fff]", rapid_clean))
    is_formula_image = (
        rapid_len == 0  # No text found at all
        or (rapid_len < 15 and not has_cjk)  # Short text, no Chinese
    )
    
    if is_formula_image:
        if verbose:
            print(f"[OCR] Running pix2tex on {input_path.name}...")
        latex_text = run_latexocr(input_path)
        if latex_text and looks_like_latex(latex_text):
            parts.append(f"$$\n{latex_text}\n$$")
            if verbose:
                print(f"[OCR] pix2tex: {len(latex_text)} chars (LaTeX)")

    if not parts:
        if verbose:
            print(f"[OCR] No text or formula recognized in {input_path.name}")
        return ""

    return "\n\n".join(parts)


def ocr_with_strategy(input_path: Path, strategy: str = "auto", verbose: bool = False) -> Optional[str]:
    """OCR with specific strategy.
    
    Args:
        input_path: Path to image file
        strategy: "rapidocr", "paddleocr", "latexocr", "all", "auto"
        verbose: Enable verbose output
        
    Returns:
        OCR result text or None
    """
    strategy = strategy.lower()
    
    if strategy == "rapidocr":
        return run_rapidocr(input_path)
    elif strategy == "paddleocr":
        if is_paddleocr_configured():
            return run_paddleocr_cloud(input_path, verbose=verbose)
        return None
    elif strategy == "latexocr":
        latex_text = run_latexocr(input_path)
        if latex_text and looks_like_latex(latex_text):
            return f"$$\n{latex_text}\n$$"
        return None
    elif strategy == "all" or strategy == "auto":
        return ocr_fallback(input_path, verbose=verbose)
    else:
        return None


def ocr_pdf_pages(pages: List, images_dir: Path, verbose: bool = False) -> List[str]:
    """OCR all pages of a PDF and return list of page texts."""
    all_text = []
    total_pages = len(pages)
    
    for i, page_img in enumerate(pages):
        page_num = i + 1
        if verbose:
            print(f"[pdf-ocr] Processing page {page_num}/{total_pages} ...")
        
        # Save page image
        img_name = f"page_{page_num}.png"
        img_path = images_dir / img_name
        page_img.save(str(img_path), "PNG")
        
        # OCR the page
        ocr_text = ocr_fallback(img_path, verbose=verbose)
        if ocr_text:
            all_text.append(f"## Page {page_num}\n\n{ocr_text}")
            if verbose:
                print(f"[pdf-ocr] Page {page_num}: {len(ocr_text)} chars")
        else:
            all_text.append(f"## Page {page_num}\n\n*[No text recognized]*")
            if verbose:
                print(f"[pdf-ocr] Page {page_num}: no text")
    
    return all_text