#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarkItDown backend - Microsoft document converter with OCR fallback.
"""

import platform
import shutil
import subprocess
from pathlib import Path

from utils.deps import (
    is_markitdown_class, is_markitdown_cli, is_pdf2image, is_rapidocr,
    pip_install, find_poppler
)
from utils.images import extract_images_from_docx, extract_images_from_xlsx, append_image_links, rewrite_base64_images
from utils.table import beautify_markdown_tables
from ocr.engine import ocr_fallback


# Image extensions supported for OCR
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff", ".tif"}


def convert_with_markitdown(
    input_path: Path,
    output_path: Path,
    images_dir: Path,
    verbose: bool = False,
    timeout: int = 120
) -> None:
    """Convert file using markitdown with OCR fallback."""
    suf = input_path.suffix.lower()

    # Try markitdown CLI first
    md_cmd = shutil.which("markitdown")
    if not md_cmd and platform.system() == "Windows":
        scripts_dir = Path(__file__).parent.parent.parent / ".venv" / "Scripts"
        if not scripts_dir.exists():
            import sys
            scripts_dir = Path(sys.executable).parent / "Scripts"
        for candidate in [scripts_dir / "markitdown.exe", scripts_dir / "markitdown.cmd"]:
            if candidate.exists():
                md_cmd = str(candidate)
                break

    if md_cmd:
        cmd = [md_cmd, "--format", "text", str(input_path)]
        try:
            result = subprocess.run(
                cmd, capture_output=True, encoding="utf-8", errors="replace", timeout=timeout,
            )
            if result.returncode == 0 and result.stdout.strip():
                output_path.write_text(result.stdout, encoding="utf-8")
                print(f"[markitdown] {input_path.name} -> {output_path}")
                _postprocess_markitdown_output(input_path, output_path, images_dir, verbose)
                return
            else:
                print(f"[markitdown] CLI returned empty or error (rc={result.returncode})")
                if result.stderr and verbose:
                    print(f"[markitdown] stderr: {result.stderr[:300]}")
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"[markitdown] CLI failed: {e}, trying MarkItDown class ...")

    # Try MarkItDown Python class
    if is_markitdown_class():
        try:
            from markitdown import MarkItDown
            md = MarkItDown()
            result = md.convert(str(input_path))
            text = result.text_content or ""
            
            if suf == ".docx":
                extract_images_from_docx(input_path, images_dir)
                text = append_image_links(text, images_dir)
            elif suf in (".xlsx", ".xls"):
                extract_images_from_xlsx(input_path, images_dir)
                text = append_image_links(text, images_dir)
            
            # For images: if markitdown returned empty (no llm_client), fall through to OCR
            if suf in IMAGE_EXTS and not text.strip():
                print("[markitdown] Image returned empty (no LLM configured), trying OCR ...")
                text = ocr_fallback(input_path)
            
            if text.strip():
                output_path.write_text(text, encoding="utf-8")
                print(f"[markitdown] {input_path.name} -> {output_path}")
                return
        except Exception as e:
            print(f"[markitdown] MarkItDown class failed: {e}")

    # For PDFs: try OCR as fallback
    if suf == ".pdf":
        print("[markitdown] Trying PDF OCR (pdf2image + RapidOCR) ...")
        if convert_pdf_with_ocr(input_path, output_path, images_dir, verbose):
            return

    # Final fallback: mammoth
    print("[markitdown] Falling back to mammoth ...")
    from backends.mammoth import convert_with_mammoth
    convert_with_mammoth(input_path, output_path, images_dir)


def _postprocess_markitdown_output(
    input_path: Path,
    output_path: Path,
    images_dir: Path,
    verbose: bool = False
) -> None:
    """Post-process markitdown output."""
    suf = input_path.suffix.lower()
    
    # Extract images
    if suf == ".docx":
        extract_images_from_docx(input_path, images_dir)
    elif suf in (".xlsx", ".xls"):
        extract_images_from_xlsx(input_path, images_dir)
    
    if not output_path.exists():
        return
    
    text = output_path.read_text(encoding="utf-8")
    
    # For image files, if markitdown returned empty, use OCR
    if suf in (".png", ".jpg", ".jpeg", ".gif", ".bmp") and not text.strip():
        text = ocr_fallback(input_path)
    
    # For PDFs with minimal content, try OCR
    if suf == ".pdf" and len(text.strip()) < 100:
        print("[markitdown] PDF has minimal text, trying OCR ...")
        if convert_pdf_with_ocr(input_path, output_path, images_dir, verbose):
            return
    
    text = append_image_links(text, images_dir)
    text = rewrite_base64_images(text, images_dir)
    text = beautify_markdown_tables(text)
    output_path.write_text(text, encoding="utf-8")


def convert_pdf_with_ocr(
    input_path: Path,
    output_path: Path,
    images_dir: Path,
    verbose: bool = False
) -> bool:
    """Convert scanned PDF to Markdown using OCR."""
    if not is_pdf2image():
        try:
            pip_install("pdf2image")
        except Exception:
            print("[pdf-ocr] pdf2image not available")
            return False

    try:
        from pdf2image import convert_from_path
    except Exception as e:
        print(f"[pdf-ocr] Import failed: {e}")
        return False

    poppler_path = find_poppler()

    print(f"[pdf-ocr] Converting PDF pages to images ...")
    if verbose:
        print(f"[pdf-ocr] Poppler: {poppler_path or 'system PATH'}")

    try:
        if poppler_path:
            pages = convert_from_path(str(input_path), dpi=200, poppler_path=poppler_path)
        else:
            pages = convert_from_path(str(input_path), dpi=200)
    except Exception as e:
        print(f"[pdf-ocr] PDF to image failed: {e}")
        print("[pdf-ocr] Hint: Install poppler (Windows: winget install poppler, Mac: brew install poppler)")
        return False

    if not pages:
        print("[pdf-ocr] No pages extracted from PDF")
        return False

    total_pages = len(pages)
    print(f"[pdf-ocr] Extracted {total_pages} page(s), running OCR ...")

    all_text = []
    images_dir.mkdir(parents=True, exist_ok=True)

    for i, page_img in enumerate(pages):
        page_num = i + 1
        if verbose:
            print(f"[pdf-ocr] Processing page {page_num}/{total_pages} ...")

        img_name = f"page_{page_num}.png"
        img_path = images_dir / img_name
        page_img.save(str(img_path), "PNG")

        ocr_text = ocr_fallback(img_path)
        if ocr_text:
            all_text.append(f"## Page {page_num}\n\n{ocr_text}")
            if verbose:
                print(f"[pdf-ocr] Page {page_num}: {len(ocr_text)} chars")
        else:
            all_text.append(f"## Page {page_num}\n\n*[No text recognized]*")
            if verbose:
                print(f"[pdf-ocr] Page {page_num}: no text")

    if all_text:
        output_path.write_text("\n\n".join(all_text), encoding="utf-8")
        print(f"[pdf-ocr] {input_path.name} -> {output_path} ({total_pages} pages)")
        return True
    else:
        print("[pdf-ocr] No text extracted from any page")
        return False