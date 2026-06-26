#!/usr/bin/env python3
"""
Reverse image search via SerpAPI Google Lens.

Usage:
  lens_search.py <image_url_or_path> [--query "optional text"] [--type visual_matches] [--limit 5] [--json]

Requires: SERPAPI_KEY environment variable (get one at https://serpapi.com/).
Zero external dependencies — uses only Python stdlib.
"""

import argparse
import json
import os
import sys
import base64
import urllib.parse
import urllib.request

SERPAPI_BASE = "https://serpapi.com/search.json"
MAX_UPLOAD_BYTES = 32 * 1024 * 1024  # 32MB upload limit

# SerpAPI supported hl values (subset — full list at serpapi.com/google-languages)
SUPPORTED_LANGS = {
    "en", "zh-CN", "zh-TW", "ja", "ko", "fr", "de", "es", "pt", "ru",
    "it", "nl", "pl", "tr", "ar", "th", "vi", "id", "hi", "sv",
}


def _validate_lang(hl: str) -> str:
    """Validate and normalize language code. SerpAPI rejects bare 'zh', needs 'zh-CN'."""
    mapping = {"zh": "zh-CN", "tw": "zh-TW"}
    return mapping.get(hl.lower(), hl)


def upload_image_to_url(image_path: str) -> str:
    """Resolve image input to a public URL for SerpAPI.
    
    - URLs are returned as-is.
    - Local files are uploaded to a free image host.
    """
    if image_path.startswith(("http://", "https://")):
        return image_path

    if not os.path.exists(image_path):
        print(f"Error: File not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    file_size = os.path.getsize(image_path)
    if file_size > MAX_UPLOAD_BYTES:
        print(f"Error: File too large ({file_size / 1024 / 1024:.1f}MB > {MAX_UPLOAD_BYTES / 1024 / 1024:.0f}MB limit)", file=sys.stderr)
        sys.exit(1)

    # Prefer imgbb if key is available, otherwise freeimage.host
    imgbb_key = os.environ.get("IMGBB_API_KEY", "")
    if imgbb_key:
        url = _upload_imgbb(image_path, imgbb_key)
        if url:
            return url

    url = _upload_freeimage(image_path)
    if url:
        return url

    print("Error: Cannot upload local image. Provide an image URL or set IMGBB_API_KEY.", file=sys.stderr)
    sys.exit(1)


def _read_as_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _upload_freeimage(image_path: str) -> str | None:
    """Upload to freeimage.host (free, no API key required)."""
    data = urllib.parse.urlencode({
        "key": "6d207e02198a847aa98d0a2a901485a5",  # freeimage public API key
        "action": "upload",
        "source": _read_as_base64(image_path),
        "format": "json",
    }).encode()

    req = urllib.request.Request("https://freeimage.host/api/1/upload", data=data)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            if result.get("status_code") == 200:
                return result["image"]["url"]
    except Exception as e:
        print(f"Warning: freeimage upload failed: {e}", file=sys.stderr)
    return None


def _upload_imgbb(image_path: str, api_key: str) -> str | None:
    """Upload to imgbb.com (requires API key)."""
    data = urllib.parse.urlencode({
        "key": api_key,
        "image": _read_as_base64(image_path),
    }).encode()

    req = urllib.request.Request("https://api.imgbb.com/1/upload", data=data)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            if result.get("success"):
                return result["data"]["url"]
    except Exception as e:
        print(f"Warning: imgbb upload failed: {e}", file=sys.stderr)
    return None


def google_lens_search(
    image_url: str,
    query: str = "",
    search_type: str = "all",
    api_key: str = "",
    hl: str = "en",
    country: str = "",
) -> dict:
    """Call SerpAPI Google Lens endpoint."""
    if not api_key:
        api_key = os.environ.get("SERPAPI_KEY", "")
    if not api_key:
        print("Error: SERPAPI_KEY not set. Get one at https://serpapi.com/", file=sys.stderr)
        sys.exit(1)

    hl = _validate_lang(hl)

    params = {
        "engine": "google_lens",
        "url": image_url,
        "api_key": api_key,
        "hl": hl,
        "type": search_type,
    }
    if query:
        params["q"] = query
    if country:
        params["country"] = country.upper()

    url = f"{SERPAPI_BASE}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "lens-search/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode()
        except Exception:
            pass
        print(f"Error: SerpAPI returned {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def format_results(data: dict, limit: int = 5) -> str:
    """Format Google Lens results into readable markdown."""
    lines = []

    # Check for API-level errors
    if "error" in data and not data.get("visual_matches"):
        return f"No results: {data['error']}"

    # Knowledge graph / related content (entity identification)
    related = data.get("related_content", [])
    if related:
        lines.append("## Identified Entity")
        for item in related[:3]:
            q = item.get("query", "")
            link = item.get("link", "")
            if q:
                lines.append(f"- **{q}**" + (f" — [link]({link})" if link else ""))
        lines.append("")

    # Knowledge graph (sometimes separate from related_content)
    kg = data.get("knowledge_graph", {})
    if kg:
        lines.append("## Knowledge Graph")
        parts = []
        if kg.get("title"):
            parts.append(f"**{kg['title']}**")
        if kg.get("subtitle"):
            parts.append(kg["subtitle"])
        if kg.get("description"):
            parts.append(kg["description"])
        if parts:
            lines.append("- " + " — ".join(parts))
        lines.append("")

    # Visual matches
    matches = data.get("visual_matches", [])
    if matches:
        n = min(limit, len(matches))
        lines.append(f"## Visual Matches (top {n})")
        for m in matches[:limit]:
            title = m.get("title", "No title")
            link = m.get("link", "")
            source = m.get("source", "")
            price = m.get("price", {})
            exact = m.get("exact_matches", False)

            entry = f"- **{title}**"
            if source:
                entry += f" ({source})"
            if price:
                entry += f" — {price.get('value', '')}"
            if exact:
                entry += " ✅ exact match"
            if link:
                entry += f"\n  🔗 {link}"
            # Include matched image URL for visual comparison
            image_url = m.get("image", "")
            if image_url:
                entry += f"\n  🖼️ {image_url}"
            lines.append(entry)
        lines.append("")

    # Detected text (OCR)
    text_results = data.get("text", [])
    if text_results:
        lines.append("## Detected Text")
        for t in text_results[:5]:
            text = t if isinstance(t, str) else t.get("text", "")
            if text:
                lines.append(f"- {text}")
        lines.append("")

    if not lines:
        return "No results found for this image."

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Reverse image search via Google Lens (SerpAPI)",
        epilog="Examples:\n"
               "  %(prog)s https://example.com/photo.jpg\n"
               "  %(prog)s ./local_image.png --type products --country jp\n"
               "  %(prog)s https://example.com/bag.jpg -q 'red' --json\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("image", help="Image URL or local file path")
    parser.add_argument("--query", "-q", default="", help="Optional text query to refine search")
    parser.add_argument("--type", "-t", default="all",
                        choices=["all", "visual_matches", "exact_matches", "products", "about_this_image"],
                        help="Search type (default: all)")
    parser.add_argument("--limit", "-n", type=int, default=5, help="Max results to show (default: 5)")
    parser.add_argument("--lang", default="en", help="Language code, e.g. en, zh-CN, ja (default: en)")
    parser.add_argument("--country", default="", help="Country code for localized results, e.g. us, jp, cn")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of markdown")
    parser.add_argument("--api-key", default="", help="SerpAPI key (default: SERPAPI_KEY env var)")

    args = parser.parse_args()

    # Resolve image to public URL
    image_url = upload_image_to_url(args.image)

    # Search
    results = google_lens_search(
        image_url=image_url,
        query=args.query,
        search_type=args.type,
        api_key=getattr(args, "api_key", ""),
        hl=args.lang,
        country=args.country,
    )

    if args.json:
        json.dump(results, sys.stdout, indent=2, ensure_ascii=False)
        print()  # trailing newline
    else:
        print(format_results(results, limit=args.limit))


if __name__ == "__main__":
    main()
