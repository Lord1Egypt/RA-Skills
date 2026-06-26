"""
pdf_text_replace_v2_ocr.py — Sprint 3: Image-based PDF text replacement (L5)

Pipeline: detect → OCR → inpaint → render → save

Minimum baseline: pytesseract + Pillow
Optional (enhanced): paddleocr, opencv-python, pymupdf (fitz)
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Optional dependency imports — all guarded
# ---------------------------------------------------------------------------

try:
    import fitz  # pymupdf
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False
    print("[pdf_ocr] pymupdf (fitz) not available — will use reportlab fallback for PDF write-back")

try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    print("[pdf_ocr] opencv-python (cv2) not available — inpainting will use solid-color fill fallback")

try:
    from paddleocr import PaddleOCR
    HAS_PADDLE = True
except ImportError:
    HAS_PADDLE = False
    # No message at import time; printed only when engine is actually requested

try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False
    print("[pdf_ocr] pytesseract not available — OCR will fail without at least one OCR engine")

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    raise ImportError("Pillow is required. Install with: pip install Pillow")

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    try:
        from PyPDF2 import PdfReader
        HAS_PYPDF = True
    except ImportError:
        HAS_PYPDF = False
        print("[pdf_ocr] pypdf not available — is_image_based_pdf() will always return True")

try:
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.utils import ImageReader
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
    print("[pdf_ocr] reportlab not available — PDF write-back requires pymupdf or reportlab")


# ---------------------------------------------------------------------------
# CJK font discovery
# ---------------------------------------------------------------------------

_CJK_FONT_SEARCH_PATHS = [
    # macOS system
    "/System/Library/Fonts",
    "/System/Library/AssetsV2/com_apple_MobileAsset_Font7",
    "/System/Library/AssetsV2/com_apple_MobileAsset_Font6",
    "/Library/Fonts",
    os.path.expanduser("~/Library/Fonts"),
    # Linux
    "/usr/share/fonts",
    "/usr/local/share/fonts",
]

_CJK_FONT_NAMES = [
    # macOS built-ins (Simplified Chinese)
    "PingFang SC Regular.ttf",
    "PingFang.ttc",
    "STHeiti Light.ttc",
    "STHeiti Medium.ttc",
    "Hiragino Sans GB.ttc",
    "NotoSansCJK-Regular.ttc",
    # Linux Noto
    "NotoSansCJK-Regular.ttc",
    "NotoSansMonoCJKsc-Regular.otf",
    "WenQuanYiMicroHei.ttf",
    # Fallback Latin
    "Arial.ttf",
    "DejaVuSans.ttf",
]


def _find_cjk_font() -> Optional[str]:
    """Search standard system paths for a CJK-capable font file."""
    for search_root in _CJK_FONT_SEARCH_PATHS:
        if not os.path.isdir(search_root):
            continue
        for dirpath, _dirnames, filenames in os.walk(search_root):
            for fname in filenames:
                if fname in _CJK_FONT_NAMES:
                    return os.path.join(dirpath, fname)
    return None


# ---------------------------------------------------------------------------
# Step 1: Detection
# ---------------------------------------------------------------------------

def is_image_based_pdf(pdf_path: str, page_num: int = 0) -> bool:
    """Detect if a PDF page is image-based (no extractable text).

    Uses pypdf text extraction as primary check.
    Falls back to checking if page has large embedded images when pypdf is
    unavailable.

    Returns True if the page appears to be image-based (scanned).
    """
    if HAS_PYPDF:
        try:
            reader = PdfReader(pdf_path)
            if page_num >= len(reader.pages):
                raise ValueError(f"Page {page_num} out of range (PDF has {len(reader.pages)} pages)")
            text = reader.pages[page_num].extract_text() or ""
            text = text.strip()
            # Heuristic: fewer than 20 non-whitespace chars → image-based
            if len(text.replace(" ", "").replace("\n", "")) < 20:
                return True
            return False
        except Exception as e:
            print(f"[pdf_ocr] pypdf extraction error: {e} — assuming image-based")
            return True

    # Fallback: check via fitz for embedded raster images
    if HAS_FITZ:
        try:
            doc = fitz.open(pdf_path)
            page = doc[page_num]
            image_list = page.get_images(full=True)
            page_area = abs(page.rect.width * page.rect.height)
            for img in image_list:
                xref = img[0]
                img_info = doc.extract_image(xref)
                img_w = img_info.get("width", 0)
                img_h = img_info.get("height", 0)
                # If a single image covers most of the page area → image-based
                if img_w * img_h > page_area * 0.5:
                    doc.close()
                    return True
            doc.close()
            return len(image_list) > 0
        except Exception as e:
            print(f"[pdf_ocr] fitz image check error: {e}")
            return True

    # No detection library available — assume image-based to be safe
    print("[pdf_ocr] No PDF library available; assuming image-based PDF")
    return True


# ---------------------------------------------------------------------------
# Step 2: OCR with positions
# ---------------------------------------------------------------------------

def ocr_page(image: "Image.Image", lang: str = "chi_sim+eng",
             engine: str = "auto") -> list:
    """OCR a page image and return text with bounding boxes.

    engine: "auto" tries PaddleOCR first (better for Chinese), falls back to
            pytesseract.  Pass "tesseract" or "paddle" to force one engine.

    Returns: [{'text': str, 'bbox': (x, y, w, h), 'confidence': float}]
    where bbox is in pixel coordinates: x=left, y=top, w=width, h=height.
    """
    use_paddle = False
    use_tesseract = False

    if engine == "paddle":
        if not HAS_PADDLE:
            print("[pdf_ocr] PaddleOCR requested but not installed. Install with: pip install paddleocr")
            return []
        use_paddle = True
    elif engine == "tesseract":
        if not HAS_TESSERACT:
            print("[pdf_ocr] pytesseract requested but not installed. Install with: pip install pytesseract")
            return []
        use_tesseract = True
    else:  # auto
        if HAS_PADDLE:
            use_paddle = True
        elif HAS_TESSERACT:
            use_tesseract = True
        else:
            print("[pdf_ocr] No OCR engine available. Install paddleocr or pytesseract.")
            return []

    results = []

    if use_paddle:
        try:
            # PaddleOCR accepts numpy array or file path
            if not HAS_CV2:
                import numpy as np_local
                img_array = np_local.array(image.convert("RGB"))
            else:
                img_array = cv2.cvtColor(
                    cv2.UMat(cv2.imdecode(
                        cv2.imencode(".png", __pil_to_cv2(image))[1],
                        cv2.IMREAD_COLOR
                    )).get(),
                    cv2.COLOR_BGR2RGB,
                )

            # Determine language for PaddleOCR
            paddle_lang = "ch" if "chi" in lang else "en"
            ocr = PaddleOCR(use_angle_cls=True, lang=paddle_lang, show_log=False)
            paddle_result = ocr.ocr(img_array, cls=True)

            if paddle_result and paddle_result[0]:
                for line in paddle_result[0]:
                    box_pts, (text, conf) = line
                    # box_pts: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
                    xs = [p[0] for p in box_pts]
                    ys = [p[1] for p in box_pts]
                    x, y = int(min(xs)), int(min(ys))
                    w, h = int(max(xs) - min(xs)), int(max(ys) - min(ys))
                    results.append({
                        "text": text,
                        "bbox": (x, y, w, h),
                        "confidence": float(conf),
                    })
            return results
        except Exception as e:
            print(f"[pdf_ocr] PaddleOCR failed ({e}), falling back to tesseract")
            if not HAS_TESSERACT:
                return []
            use_tesseract = True

    if use_tesseract:
        try:
            data = pytesseract.image_to_data(
                image,
                lang=lang,
                output_type=pytesseract.Output.DICT,
            )
            n = len(data["text"])
            for i in range(n):
                text = data["text"][i].strip()
                if not text:
                    continue
                conf_raw = data["conf"][i]
                conf = float(conf_raw) / 100.0 if conf_raw != -1 else 0.0
                x = int(data["left"][i])
                y = int(data["top"][i])
                w = int(data["width"][i])
                h = int(data["height"][i])
                results.append({
                    "text": text,
                    "bbox": (x, y, w, h),
                    "confidence": conf,
                })
            return results
        except Exception as e:
            print(f"[pdf_ocr] pytesseract failed: {e}")
            return []

    return results


# ---------------------------------------------------------------------------
# Internal helper: PIL ↔ OpenCV
# ---------------------------------------------------------------------------

def __pil_to_cv2(pil_image: "Image.Image"):
    """Convert PIL Image to OpenCV BGR numpy array."""
    import numpy as _np
    rgb = pil_image.convert("RGB")
    arr = _np.array(rgb)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def __cv2_to_pil(cv2_image) -> "Image.Image":
    """Convert OpenCV BGR numpy array to PIL Image."""
    rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


# ---------------------------------------------------------------------------
# Step 3: Background repair (inpainting)
# ---------------------------------------------------------------------------

def inpaint_region(image: "Image.Image", bbox: tuple,
                   method: str = "telea") -> "Image.Image":
    """Remove text from a region and fill with surrounding texture.

    bbox: (x, y, w, h) in pixels.
    method: "telea" (default) or "ns" (Navier-Stokes).
    Uses OpenCV inpainting. Falls back to solid color fill if cv2 unavailable.
    """
    x, y, w, h = bbox

    if not HAS_CV2:
        # Fallback: sample average color from a border strip around the region
        img_copy = image.copy().convert("RGBA")
        draw = ImageDraw.Draw(img_copy)
        # Sample color from a 5px border outside bbox
        border = 5
        sample_region = (
            max(0, x - border), max(0, y - border),
            min(image.width, x + w + border), min(image.height, y + h + border),
        )
        crop = image.crop(sample_region).convert("RGB")
        pixels = list(crop.getdata())
        avg_r = int(sum(p[0] for p in pixels) / len(pixels))
        avg_g = int(sum(p[1] for p in pixels) / len(pixels))
        avg_b = int(sum(p[2] for p in pixels) / len(pixels))
        draw.rectangle([x, y, x + w, y + h], fill=(avg_r, avg_g, avg_b, 255))
        return img_copy.convert("RGB")

    import numpy as np

    cv_img = __pil_to_cv2(image)
    mask = np.zeros(cv_img.shape[:2], dtype=np.uint8)
    # Expand mask slightly so edge pixels of letters are also removed
    pad = max(2, h // 8)
    x1 = max(0, x - pad)
    y1 = max(0, y - pad)
    x2 = min(cv_img.shape[1], x + w + pad)
    y2 = min(cv_img.shape[0], y + h + pad)
    mask[y1:y2, x1:x2] = 255

    inpaint_flag = cv2.INPAINT_TELEA if method == "telea" else cv2.INPAINT_NS
    radius = max(3, h // 4)
    result = cv2.inpaint(cv_img, mask, inpaintRadius=radius, flags=inpaint_flag)
    return __cv2_to_pil(result)


# ---------------------------------------------------------------------------
# Step 4: Render new text
# ---------------------------------------------------------------------------

def render_text_on_image(image: "Image.Image", text: str, bbox: tuple,
                         font_path: str = None, font_size: int = None,
                         color: tuple = (0, 0, 0)) -> "Image.Image":
    """Render text onto image at the given position.

    bbox: (x, y, w, h) in pixels.
    Auto-detects font size from bbox height if font_size not specified.
    Uses system CJK font if font_path not provided.
    Handles both Latin and CJK text.
    """
    x, y, w, h = bbox
    img_copy = image.copy().convert("RGBA")
    draw = ImageDraw.Draw(img_copy)

    # Resolve font
    resolved_font_path = font_path or _find_cjk_font()

    # Auto font size: aim to fill ~80% of bbox height
    if font_size is None:
        font_size = max(8, int(h * 0.80))

    font = None
    if resolved_font_path and os.path.isfile(resolved_font_path):
        try:
            font = ImageFont.truetype(resolved_font_path, font_size)
        except Exception as e:
            print(f"[pdf_ocr] Could not load font {resolved_font_path}: {e}")

    if font is None:
        # Last resort: PIL built-in bitmap font (no CJK, but won't crash)
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None

    # Measure text to center it within bbox
    if font:
        try:
            # Pillow >= 9.2 uses getbbox; older uses getsize
            if hasattr(font, "getbbox"):
                tb = font.getbbox(text)
                text_w = tb[2] - tb[0]
                text_h = tb[3] - tb[1]
            else:
                text_w, text_h = font.getsize(text)  # type: ignore[attr-defined]
        except Exception:
            text_w, text_h = w, h
    else:
        text_w, text_h = w, h

    # Horizontal: left-align within bbox; vertical: center
    text_x = x
    text_y = y + max(0, (h - text_h) // 2)

    draw.text((text_x, text_y), text, fill=color + (255,), font=font)
    return img_copy.convert("RGB")


# ---------------------------------------------------------------------------
# Step 5: Write back to PDF
# ---------------------------------------------------------------------------

def replace_page_image(pdf_path: str, page_num: int,
                       new_image: "Image.Image", output_path: str) -> None:
    """Replace a page's image content in the PDF.

    Uses pymupdf (fitz) if available, falls back to reportlab overlay.
    The new_image should be at the same DPI as the original extraction.
    """
    if HAS_FITZ:
        _replace_page_fitz(pdf_path, page_num, new_image, output_path)
    elif HAS_REPORTLAB:
        _replace_page_reportlab(pdf_path, page_num, new_image, output_path)
    else:
        raise RuntimeError(
            "Neither pymupdf nor reportlab is available. "
            "Install one: pip install pymupdf  OR  pip install reportlab"
        )


def _replace_page_fitz(pdf_path: str, page_num: int,
                       new_image: "Image.Image", output_path: str) -> None:
    """Replace page using pymupdf by inserting image as full-page content."""
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    rect = page.rect  # page dimensions in points

    # Save PIL image to temp PNG
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        new_image.save(tmp_path, format="PNG", dpi=(300, 300))

        # Clear existing content and insert new image
        page.clean_contents()

        # Remove existing images by inserting a white rect then our image
        # Use insert_image which replaces the entire page with the image
        page.insert_image(rect, filename=tmp_path, keep_proportion=False)

        doc.save(output_path, garbage=4, deflate=True)
    finally:
        doc.close()
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def _replace_page_reportlab(pdf_path: str, page_num: int,
                             new_image: "Image.Image", output_path: str) -> None:
    """Replace page using reportlab by creating a new PDF with image overlay.

    Only handles single-page replacement for page_num; other pages are copied
    via pypdf if available.
    """
    if not HAS_REPORTLAB:
        raise RuntimeError("reportlab is not installed")

    # Get page dimensions from source PDF
    page_width_pt = 595.0  # A4 default
    page_height_pt = 842.0

    if HAS_PYPDF:
        reader = PdfReader(pdf_path)
        if page_num < len(reader.pages):
            mb = reader.pages[page_num].mediabox
            page_width_pt = float(mb.width)
            page_height_pt = float(mb.height)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        img_tmp = tmp.name
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp2:
        overlay_pdf = tmp2.name

    try:
        new_image.save(img_tmp, format="PNG")

        c = rl_canvas.Canvas(overlay_pdf, pagesize=(page_width_pt, page_height_pt))
        c.drawImage(
            ImageReader(img_tmp),
            0, 0,
            width=page_width_pt, height=page_height_pt,
            preserveAspectRatio=False,
        )
        c.save()

        # Merge: if pypdf available, copy other pages; else just use overlay
        if HAS_PYPDF:
            try:
                from pypdf import PdfWriter
            except ImportError:
                from PyPDF2 import PdfWriter

            reader_src = PdfReader(pdf_path)
            reader_overlay = PdfReader(overlay_pdf)
            writer = PdfWriter()

            for i, pg in enumerate(reader_src.pages):
                if i == page_num:
                    writer.add_page(reader_overlay.pages[0])
                else:
                    writer.add_page(pg)

            with open(output_path, "wb") as f_out:
                writer.write(f_out)
        else:
            import shutil
            shutil.copy2(overlay_pdf, output_path)

    finally:
        for p in (img_tmp, overlay_pdf):
            try:
                os.unlink(p)
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Helpers: PDF → PIL image
# ---------------------------------------------------------------------------

def _pdf_page_to_image(pdf_path: str, page_num: int, dpi: int = 300) -> "Image.Image":
    """Rasterize a single PDF page to a PIL Image at the given DPI."""
    if HAS_FITZ:
        doc = fitz.open(pdf_path)
        page = doc[page_num]
        zoom = dpi / 72.0  # fitz default is 72 DPI
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        doc.close()
        return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Fallback: pdf2image
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, dpi=dpi, first_page=page_num + 1,
                                   last_page=page_num + 1)
        if images:
            return images[0]
    except ImportError:
        pass

    raise RuntimeError(
        "Cannot rasterize PDF. Install pymupdf (pip install pymupdf) "
        "or pdf2image (pip install pdf2image) plus poppler."
    )


# ---------------------------------------------------------------------------
# Text search helpers
# ---------------------------------------------------------------------------

def _find_text_in_ocr_results(ocr_results: list, target_text: str,
                               fuzzy: bool = True) -> list:
    """Return list of OCR result entries whose text matches target_text.

    fuzzy=True uses case-insensitive substring containment.
    Returns list of dicts with 'text', 'bbox', 'confidence'.
    """
    hits = []
    target_lower = target_text.lower().strip()
    for item in ocr_results:
        item_text = item["text"].strip()
        if fuzzy:
            if target_lower in item_text.lower():
                hits.append(item)
        else:
            if item_text == target_text:
                hits.append(item)
    return hits


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def replace_text_in_image_pdf(
    pdf_path: str,
    old_text: str,
    new_text: str,
    output_path: str = None,
    page_num: int = 0,
    dpi: int = 300,
    lang: str = "chi_sim+eng",
    engine: str = "auto",
    font_path: str = None,
    inpaint_method: str = "telea",
    color: tuple = (0, 0, 0),
) -> bool:
    """Complete pipeline: detect → OCR → inpaint → render → save.

    All operations at consistent DPI (default 300).
    Font size: 1pt ≈ dpi/72 pixels (automatically derived from bbox).

    Returns True if at least one replacement was made, False otherwise.
    """
    pdf_path = str(pdf_path)

    if output_path is None:
        base, ext = os.path.splitext(pdf_path)
        output_path = f"{base}_ocr_replaced{ext}"

    print(f"[pdf_ocr] Processing: {pdf_path}")
    print(f"[pdf_ocr] Replace '{old_text}' → '{new_text}' on page {page_num} at {dpi} DPI")

    # Step 1: Detection
    image_based = is_image_based_pdf(pdf_path, page_num)
    if not image_based:
        print("[pdf_ocr] Page appears to have extractable text. "
              "Consider using the vector-based replacement path instead. "
              "Proceeding with OCR pipeline anyway.")

    # Rasterize page
    print("[pdf_ocr] Rasterizing page...")
    page_image = _pdf_page_to_image(pdf_path, page_num, dpi=dpi)
    print(f"[pdf_ocr] Page image size: {page_image.size[0]}x{page_image.size[1]} px")

    # Step 2: OCR
    print(f"[pdf_ocr] Running OCR (engine={engine}, lang={lang})...")
    ocr_results = ocr_page(page_image, lang=lang, engine=engine)
    print(f"[pdf_ocr] OCR found {len(ocr_results)} text regions")

    if not ocr_results:
        print("[pdf_ocr] No OCR results — cannot proceed")
        return False

    # Find matching regions
    matches = _find_text_in_ocr_results(ocr_results, old_text)
    if not matches:
        print(f"[pdf_ocr] Text '{old_text}' not found in OCR results")
        # Debug: print top-10 OCR results
        print("[pdf_ocr] Top OCR results for debugging:")
        for item in ocr_results[:10]:
            print(f"  conf={item['confidence']:.2f}  bbox={item['bbox']}  text={item['text']!r}")
        return False

    print(f"[pdf_ocr] Found {len(matches)} matching region(s)")

    # Process each match
    working_image = page_image.copy()
    for i, match in enumerate(matches):
        bbox = match["bbox"]
        print(f"[pdf_ocr] Match {i+1}: bbox={bbox}  conf={match['confidence']:.2f}  text={match['text']!r}")

        # Step 3: Inpaint (erase old text)
        working_image = inpaint_region(working_image, bbox, method=inpaint_method)

        # Step 4: Render new text
        working_image = render_text_on_image(
            working_image, new_text, bbox,
            font_path=font_path, color=color
        )

    # Step 5: Write back to PDF
    print(f"[pdf_ocr] Writing output to: {output_path}")
    replace_page_image(pdf_path, page_num, working_image, output_path)
    print("[pdf_ocr] Done.")
    return True


# ---------------------------------------------------------------------------
# Convenience: process all pages
# ---------------------------------------------------------------------------

def replace_text_in_image_pdf_all_pages(
    pdf_path: str,
    old_text: str,
    new_text: str,
    output_path: str = None,
    dpi: int = 300,
    **kwargs,
) -> int:
    """Run replacement on every page of the PDF.

    Returns the number of pages where a replacement was made.
    Internally chains replacements so all pages end up in the final output.
    """
    if not HAS_PYPDF:
        raise RuntimeError("pypdf is required for multi-page processing")

    reader = PdfReader(pdf_path)
    n_pages = len(reader.pages)

    if output_path is None:
        base, ext = os.path.splitext(pdf_path)
        output_path = f"{base}_ocr_replaced{ext}"

    replaced_count = 0
    current_pdf = pdf_path

    with tempfile.TemporaryDirectory() as tmpdir:
        for pg in range(n_pages):
            tmp_out = os.path.join(tmpdir, f"page_{pg:04d}.pdf")
            ok = replace_text_in_image_pdf(
                current_pdf, old_text, new_text,
                output_path=tmp_out, page_num=pg, dpi=dpi, **kwargs
            )
            if ok:
                replaced_count += 1
                current_pdf = tmp_out
            # If not replaced, keep current_pdf unchanged for next iteration

        import shutil
        shutil.copy2(current_pdf, output_path)

    return replaced_count


# ---------------------------------------------------------------------------
# Demo / self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    print("=" * 60)
    print("pdf_text_replace_v2_ocr — self-test / demo")
    print("=" * 60)

    # Capability report
    print(f"\nDependency status:")
    print(f"  Pillow          : {'yes' if HAS_PIL else 'MISSING (required)'}")
    print(f"  pypdf           : {'yes' if HAS_PYPDF else 'no (optional)'}")
    print(f"  pymupdf (fitz)  : {'yes' if HAS_FITZ else 'no (optional)'}")
    print(f"  opencv-python   : {'yes' if HAS_CV2 else 'no (optional)'}")
    print(f"  pytesseract     : {'yes' if HAS_TESSERACT else 'no (optional)'}")
    print(f"  paddleocr       : {'yes' if HAS_PADDLE else 'no (optional)'}")
    print(f"  reportlab       : {'yes' if HAS_REPORTLAB else 'no (optional)'}")

    # Check for CJK font
    cjk_font = _find_cjk_font()
    print(f"  CJK font found  : {cjk_font or 'none (Latin fallback will be used)'}")

    if not (HAS_TESSERACT or HAS_PADDLE):
        print("\n[demo] No OCR engine available — skipping OCR demo.")
        print("Install pytesseract: pip install pytesseract")
        print("Install paddleocr:   pip install paddleocr")
        sys.exit(0)

    print("\n--- Demo: create test image, OCR, replace text ---\n")

    # 1. Create a simple test image with text
    W, H = 800, 200
    test_img = Image.new("RGB", (W, H), color=(255, 255, 255))
    draw = ImageDraw.Draw(test_img)

    # Try to use a real font; fall back to default
    demo_font = None
    demo_font_path = cjk_font or None
    if demo_font_path:
        try:
            demo_font = ImageFont.truetype(demo_font_path, 48)
        except Exception:
            pass
    if demo_font is None:
        demo_font = ImageFont.load_default()

    original_text = "Hello World 测试"
    draw.text((50, 70), original_text, fill=(20, 20, 20), font=demo_font)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
        test_img_path = tf.name
    test_img.save(test_img_path)
    print(f"Created test image: {test_img_path}")

    # 2. OCR the test image
    print("\nRunning OCR on test image...")
    ocr_results = ocr_page(test_img, engine="auto")
    print(f"OCR returned {len(ocr_results)} items:")
    for item in ocr_results:
        print(f"  text={item['text']!r}  bbox={item['bbox']}  conf={item['confidence']:.2f}")

    # 3. Demonstrate inpaint + render on the image
    if ocr_results:
        first = ocr_results[0]
        print(f"\nInpainting region for: {first['text']!r}")
        inpainted = inpaint_region(test_img, first["bbox"])

        replacement = "Replaced!"
        print(f"Rendering replacement text: {replacement!r}")
        final_img = render_text_on_image(
            inpainted, replacement, first["bbox"],
            font_path=demo_font_path, color=(180, 0, 0)
        )

        with tempfile.NamedTemporaryFile(suffix="_replaced.png", delete=False) as tf2:
            out_img_path = tf2.name
        final_img.save(out_img_path)
        print(f"Saved result image: {out_img_path}")

        # 4. Verify: re-OCR the result image
        print("\nVerifying replacement with second OCR pass...")
        verify_results = ocr_page(final_img, engine="auto")
        found_replacement = any(
            "replaced" in r["text"].lower() for r in verify_results
        )
        print(f"Replacement text found in re-OCR: {found_replacement}")
        if verify_results:
            print("Re-OCR results:")
            for item in verify_results:
                print(f"  text={item['text']!r}  conf={item['confidence']:.2f}")
    else:
        print("No OCR results — cannot demonstrate inpaint/render")

    # Clean up temp test image (keep result for inspection)
    try:
        os.unlink(test_img_path)
    except OSError:
        pass

    print("\nDemo complete.")
    if HAS_FITZ or HAS_REPORTLAB:
        print("\nTo process a real PDF:")
        print("  from pdf_text_replace_v2_ocr import replace_text_in_image_pdf")
        print("  replace_text_in_image_pdf('scan.pdf', 'old text', 'new text', 'out.pdf')")
    else:
        print("\nNote: install pymupdf or reportlab to enable PDF write-back.")
