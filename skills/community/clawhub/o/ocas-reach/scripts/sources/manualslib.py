"""
ManualsLib source for ocas-reach.

ManualsLib.com is a Vue.js SPA (3M+ manuals, 140K+ brands). Direct access is blocked
from datacenter IPs. This module uses:
- OpenSearch autocomplete for discovery
- Wayback Machine CDX API for URL enumeration
- Direct image URL construction for page content
- Tesseract OCR for text extraction

Also supports ManualZZ (same content, better image quality) via Wayback Machine.
"""

import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request


def query(action, params, auth):
    """Route to the appropriate action handler."""
    handlers = {
        "autocomplete": _autocomplete,
        "search": _search,
        "read_page": _read_page,
        "read_random": _read_random,
    }
    handler = handlers.get(action)
    if not handler:
        return {"error": f"Unknown action: {action}. Supported: {list(handlers.keys())}"}
    return handler(params, auth)


def _autocomplete(params, auth):
    """Use OpenSearch autocomplete endpoint."""
    query_str = params.get("query", "")
    if not query_str:
        return {"error": "Missing required param: query"}

    encoded = urllib.parse.quote(query_str)
    url = f"https://www.manualslib.com/openSearch/action/autocomplete?term={encoded}&open=1"

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        return {"error": f"Autocomplete failed: {e}"}

    results = []
    for item in data[:10]:
        label = re.sub(r"<[^>]+>", "", item["label"])
        results.append({"label": label, "value": item["value"]})

    return {"action": "autocomplete", "query": query_str, "results": results}


def _search(params, auth):
    """Search for manuals via web_search + Wayback CDX enumeration."""
    query_str = params.get("query", "")
    limit = params.get("limit", 5)

    # Use web_search to find manual IDs from search engines
    # This requires the calling agent to have web_search available
    # We provide the search query for the agent to execute
    search_query = f"site:manualslib.com \"{query_str}\" manual"

    return {
        "action": "search",
        "query": query_str,
        "search_query_for_agent": search_query,
        "instruction": (
            "Run web_search with the search_query_for_agent, then extract manual IDs "
            "from results (format: /manual/{ID}/{Slug}.html). Use the Wayback CDX API "
            "to enumerate page images for each manual."
        ),
        "limit": limit,
    }


def _read_page(params, auth):
    """Download and OCR a specific page from a manual."""
    manual_id = params.get("manual_id", "")
    page = params.get("page", 1)
    slug = params.get("slug", "")

    if not manual_id:
        return {"error": "Missing required param: manual_id"}

    # Try to find the image URL via Wayback CDX
    image_urls = _find_page_images(manual_id, page, slug)

    if not image_urls:
        return {
            "error": f"No page images found for manual {manual_id} page {page}",
            "hint": "Try _search first to discover available pages via CDX.",
        }

    # Try each image URL until one works
    for img_url in image_urls:
        result = _download_and_ocr(img_url)
        if result.get("ocr_text"):
            return result

    return {"error": "All image URLs failed or produced no OCR output"}


def _read_random(params, auth):
    """Read a random page from a random manual."""
    # Use Wayback CDX to find a random manual with images
    # Query for recent manuals with page images
    import random

    # Try to find a random manual from the CDX
    # Use a random ID range (manuals go up to ~3M+)
    for _ in range(5):
        manual_id = str(random.randint(100000, 3200000))
        # Check if this manual has images in CDX
        for gen in [7, 10, 51]:
            g1 = manual_id[-3:-1].zfill(2)
            g2 = manual_id[-5:-3].zfill(2)
            cdx_url = (
                f"https://web.archive.org/cdx/search/cdx"
                f"?url=static-data2.manualslib.com/storage/pdf{gen}/{g1}/{g2}/{manual_id}/*"
                f"&output=text&limit=5&fl=original"
            )
            req = urllib.request.Request(cdx_url, headers={"User-Agent": "Mozilla/5.0"})
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    text = resp.read().decode().strip()
                    if text:
                        urls = text.split("\n")
                        # Pick a random page image
                        img_url = random.choice(urls)
                        result = _download_and_ocr(img_url)
                        if result.get("ocr_text"):
                            return result
            except Exception:
                continue

    return {"error": "Could not find a random manual with available images"}


def _find_page_images(manual_id, page, slug):
    """Find page image URLs via Wayback CDX."""
    urls = []
    for gen in [7, 10, 51]:
        g1 = manual_id[-3:-1].zfill(2) if len(manual_id) >= 3 else "00"
        g2 = manual_id[-5:-3].zfill(2) if len(manual_id) >= 5 else "00"

        # Try with slug if provided, otherwise use wildcard
        if slug:
            cdx_url = (
                f"https://web.archive.org/cdx/search/cdx"
                f"?url=static-data2.manualslib.com/storage/pdf{gen}/{g1}/{g2}/{manual_id}-{slug}/images/{slug}_{page}_bg.*"
                f"&output=text&limit=5&fl=original"
            )
        else:
            cdx_url = (
                f"https://web.archive.org/cdx/search/cdx"
                f"?url=static-data2.manualslib.com/storage/pdf{gen}/{g1}/{g2}/{manual_id}/*"
                f"&output=text&limit=10&fl=original"
            )

        req = urllib.request.Request(cdx_url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                text = resp.read().decode().strip()
                if text:
                    for line in text.split("\n"):
                        if f"_{page}_" in line or (not slug and line.endswith((".jpg", ".png"))):
                            if line.startswith("http"):
                                urls.append(line)
                            else:
                                urls.append(f"https:{line}")
        except Exception:
            continue

    # Also try direct URL construction as fallback
    for gen in [7, 10, 51]:
        for ext in ["jpg", "png"]:
            if slug:
                urls.append(
                    f"https://static-data2.manualslib.com/storage/pdf{gen}/{g1}/{g2}/{manual_id}-{slug}/images/{slug}_{page}_bg.{ext}"
                )

    return urls


def _download_and_ocr(image_url):
    """Download an image and OCR it with tesseract."""
    import tempfile

    # Download image
    req = urllib.request.Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            img_data = resp.read()
    except Exception as e:
        return {"error": f"Download failed: {e}", "url": image_url}

    # Check if we got an actual image (not HTML error page)
    if img_data[:20].startswith((b"<!DOCTYPE", b"<html", b"<?xml")):
        return {"error": "Got HTML instead of image (blocked)", "url": image_url}

    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(img_data)
        img_path = f.name

    # Preprocess: upscale 2.5x, sharpen
    ocr_path = img_path.replace(".png", "_ocr.png")
    try:
        from PIL import Image, ImageEnhance

        img = Image.open(img_path).convert("RGB")
        w, h = img.size
        img2 = img.resize((int(w * 2.5), int(h * 2.5)), Image.LANCZOS)
        img2 = ImageEnhance.Sharpness(img2).enhance(1.8)
        img2.save(ocr_path)
    except ImportError:
        # If PIL not available, just use the original
        ocr_path = img_path

    # OCR with tesseract
    try:
        result = subprocess.run(
            ["tesseract", ocr_path, "stdout", "-l", "eng", "--psm", "6"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        ocr_text = result.stdout.strip()
    except Exception as e:
        ocr_text = ""
        result = None

    # Cleanup
    for p in [img_path, ocr_path]:
        try:
            os.unlink(p)
        except Exception:
            pass

    return {
        "action": "read_page",
        "image_url": image_url,
        "ocr_text": ocr_text,
        "ocr_quality": _assess_ocr_quality(ocr_text),
        "page_size": len(img_data),
    }


def _assess_ocr_quality(text):
    """Rough OCR quality assessment."""
    if not text:
        return "none"
    # Count recognizable English words
    words = text.split()
    if len(words) < 5:
        return "low"
    # Check if most tokens are real words (simple heuristic)
    alpha_count = sum(1 for w in words if w.isalpha())
    ratio = alpha_count / len(words) if words else 0
    if ratio > 0.7 and len(words) > 20:
        return "high"
    elif ratio > 0.4:
        return "medium"
    return "low"
