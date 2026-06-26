#!/usr/bin/env python3
"""
OCR engine for pdf-miner: uses a configurable vision API (OpenRouter-compatible) to OCR scanned/image-based PDF pages.
Powered by PyMuPDF for PDF→Image conversion + OpenAI-compatible API for OCR.

No external system dependencies (no Tesseract, no poppler required).

Usage:
    python ocr_engine.py input.pdf [output.md] [options]
    python ocr_engine.py report.pdf                     -- all pages
    python ocr_engine.py report.pdf output.md --pages 1-5 -- specific pages
"""

import sys
import os
import base64
import time
import json
import re
from io import BytesIO
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF required. Install with: python -m pip install pymupdf")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai required. Install with: python -m pip install openai")
    sys.exit(1)


def _load_skill_config():
    """Load skill's own config.json (if exists). Returns (api_key, base_url, model) tuple or None."""
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    config_path = os.path.abspath(config_path)
    try:
        if not os.path.exists(config_path):
            return None
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        api_key = cfg.get("vision_api_key", "").strip()
        base_url = cfg.get("vision_base_url", "").strip()
        model = cfg.get("vision_model", "").strip()
        # Only return if api_key is present (required)
        return (api_key if api_key else None, base_url or None, model or None)
    except Exception:
        return None


_skill_cfg = _load_skill_config() or (None, None, None)

# Config precedence: CLI arg > env var > skill config.json > hardcoded default
DEFAULT_API_KEY = os.environ.get("OCR_API_KEY", os.environ.get("OPENROUTER_API_KEY", _skill_cfg[0] or ""))
DEFAULT_BASE_URL = os.environ.get("OCR_BASE_URL", _skill_cfg[1] or "https://openrouter.ai/api/v1")
DEFAULT_MODEL = os.environ.get("OCR_MODEL", _skill_cfg[2] or "qwen/qwen3.6-plus:free")

MAX_PAGE_DIM = 2048
OCR_PROMPT = (
    "Extract ALL visible text from this PDF page image. "
    "Preserve layout, table structure, numbers and dates exactly as shown. "
    "Return ONLY the extracted text, no explanations."
)

# Known vision-capable model prefixes (non-exhaustive). Keep in sync with extract_pdf.py.
VISION_MODEL_PREFIXES = [
    "qwen/", "stepfun/", "minimax/",
    "anthropic/claude-3",
    "openai/gpt-4o", "openai/gpt-4-turbo", "openai/gpt-4-vision",
    "google/gemini", "microsoft/phi-3",
]

def _is_vision_model(model_id: str) -> bool:
    """Check if a model ID likely supports vision (image input)."""
    model_lower = model_id.lower()
    return any(model_lower.startswith(prefix) for prefix in VISION_MODEL_PREFIXES)


def pdf_page_to_image(doc, page_num: int, dpi: int = 200) -> bytes | None:
    """Convert a PDF page to JPEG bytes via PyMuPDF."""
    try:
        page = doc[page_num - 1]  # 0-based
        zoom = dpi / 72
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), dpi=dpi)

        # Resize if too large
        if pix.width > MAX_PAGE_DIM or pix.height > MAX_PAGE_DIM:
            ratio = MAX_PAGE_DIM / max(pix.width, pix.height)
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom * ratio, zoom * ratio), dpi=int(dpi * ratio))

        return pix.tobytes("jpeg", quality=85)
    except Exception as e:
        print(f"    Error converting page {page_num}: {e}")
        return None


def ocr_page(image_bytes: bytes, client, model: str, page_num: int, retries: int = 2) -> str | None:
    """Send page image to vision model for OCR."""
    b64 = base64.b64encode(image_bytes).decode()
    data_uri = f"data:image/jpeg;base64,{b64}"

    for attempt in range(1, retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": OCR_PROMPT},
                        {"type": "image_url", "image_url": {"url": data_uri, "detail": "high"}}
                    ]
                }],
                max_tokens=2000,
                temperature=0,
            )
            text = resp.choices[0].message.content.strip()
            if text.upper() in ("[NO TEXT]", "NO TEXT", "NO TEXT FOUND"):
                return None
            return text
        except Exception as e:
            error_str = str(e)
            if "rate limit" in error_str.lower() or "429" in error_str:
                wait = attempt * 10
                print(f"      Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            if attempt < retries:
                wait = attempt * 5
                print(f"      Retry {attempt}/{retries} after {wait}s... (error: {error_str[:80]})")
                time.sleep(wait)
            else:
                print(f"      OCR failed: {error_str[:120]}")
                return None
    return None


def process_pdf_ocr(pdf_path: str, output_path: str = None, pages: list = None,
                    dpi: int = 200, api_key: str = None, base_url: str = None,
                    model: str = None):
    """OCR a PDF using the configured vision API (OpenRouter-compatible)."""
    api_key = api_key or DEFAULT_API_KEY
    base_url = base_url or DEFAULT_BASE_URL
    model = model or DEFAULT_MODEL

    if not api_key:
        print("Error: No API key. Set OCR_API_KEY env var, configure config.json, or pass --api-key")
        sys.exit(1)

    # Auto-detect vision capability and fallback if needed
    if not _is_vision_model(model):
        fallback = "qwen/qwen3.6-plus:free"
        print(f"Warning: Model '{model}' may not support vision input.")
        print(f"Falling back to default vision model: {fallback}")
        model = fallback

    client = OpenAI(api_key=api_key, base_url=base_url)
    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    if pages is None:
        pages = list(range(1, total_pages + 1))

    print(f"[OCR] {Path(pdf_path).name}")
    print(f"  Pages: {len(pages)}/{total_pages}, DPI: {dpi}, Model: {model}")
    print()

    results = []
    success = 0
    failed = 0

    for pg_num in pages:
        if pg_num > total_pages:
            print(f"  Page {pg_num}: SKIP (beyond {total_pages})")
            results.append((pg_num, f"[Page {pg_num} — beyond total pages]"))
            failed += 1
            continue

        print(f"  Page {pg_num}/{total_pages}... ", end="", flush=True)

        img_bytes = pdf_page_to_image(doc, pg_num, dpi=dpi)
        if img_bytes is None:
            print("SKIP (render failed)")
            results.append((pg_num, f"[Page {pg_num} — render failed]"))
            failed += 1
            continue

        size_kb = len(img_bytes) / 1024
        text = ocr_page(image_bytes=img_bytes, client=client, model=model, page_num=pg_num)

        if text:
            results.append((pg_num, f"--- Page {pg_num} (OCR: {model}, {size_kb:.0f}KB) ---\n{text}"))
            print(f"OK ({len(text)} chars)")
            success += 1
        else:
            results.append((pg_num, f"[Page {pg_num} — no readable text]"))
            print("NO TEXT")
            failed += 1

    doc.close()

    # Write output
    if output_path:
        out = Path(output_path)
    else:
        out = Path(pdf_path).parent / (Path(pdf_path).stem + "-ocr.md")

    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# OCR Results: {Path(pdf_path).name}\n\n")
        f.write(f"PDF: {pdf_path}\n")
        f.write(f"Model: {model}\n")
        f.write(f"Pages: {len(pages)}/{total_pages}\n")
        f.write(f"Success: {success}/{len(pages)} | Failed: {failed}\n\n")
        for pg_num, text in results:
            f.write(text + "\n\n")

    print(f"\n  → {out}")
    print(f"  → Success: {success}/{len(pages)}")
    return out


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="OCR a PDF using vision API (reads skill config by default)")
    parser.add_argument("input", help="Input PDF")
    parser.add_argument("output", nargs="?", default=None, help="Output .md")
    parser.add_argument("--pages", default=None, help="Pages: 1,2,3-5")
    parser.add_argument("--dpi", type=int, default=200, help="DPI (default 200)")
    parser.add_argument("--model", default=None, help="Model ID (overrides config)")
    parser.add_argument("--api-key", default=None, help="API key (overrides config)")
    parser.add_argument("--base-url", default=None, help="API base URL (overrides config)")
    args = parser.parse_args()

    pages = None
    if args.pages:
        pages = []
        for part in args.pages.split(","):
            part = part.strip()
            if "-" in part:
                s, e = part.split("-", 1)
                pages.extend(range(int(s), int(e) + 1))
            else:
                pages.append(int(part))

    process_pdf_ocr(
        args.input, args.output, pages=pages, dpi=args.dpi,
        api_key=args.api_key, base_url=args.base_url, model=args.model
    )
