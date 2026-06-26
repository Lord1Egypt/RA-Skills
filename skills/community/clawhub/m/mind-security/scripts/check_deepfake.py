#!/usr/bin/env python3
"""
check_deepfake.py — Deepfake / AI-generated media detection.

Primary:  BitMind API (Bittensor Subnet 34) — requires BITMIND_API_KEY
Fallback: EXIF / metadata heuristic analysis (no API key needed)

Supports images and videos (including YouTube, Twitter/X, TikTok URLs).

Usage:
    python3 check_deepfake.py photo.jpg
    python3 check_deepfake.py https://example.com/image.png
    python3 check_deepfake.py video.mp4
    python3 check_deepfake.py https://youtube.com/watch?v=... --fps 2
    python3 check_deepfake.py photo.jpg --debug
    python3 check_deepfake.py photo.jpg --method metadata   # force local-only

No pip dependencies — uses Python stdlib only.
"""

import argparse
import json
import os
import struct
import sys
import urllib.error
import urllib.request


# ---------------------------------------------------------------------------
# BitMind API integration
# ---------------------------------------------------------------------------

BITMIND_API_BASE = "https://api.bitmind.ai"
USER_AGENT = "Mozilla/5.0 (compatible; mind-security/1.0; +https://github.com/mind-sec/mind-security)"

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv", ".wmv", ".m4v"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".tif", ".avif"}
VIDEO_URL_PATTERNS = ("youtube.com", "youtu.be", "twitter.com", "x.com", "tiktok.com", "vimeo.com")


def _is_video(target: str) -> bool:
    """Determine if target is a video (by extension or URL pattern)."""
    ext = os.path.splitext(target)[1].lower()
    if ext in VIDEO_EXTENSIONS:
        return True
    target_lower = target.lower()
    return any(pat in target_lower for pat in VIDEO_URL_PATTERNS)


def _detect_image_url(image_url: str, api_key: str, debug: bool = False) -> dict:
    """Send an image URL to BitMind for deepfake detection."""
    endpoint = f"{BITMIND_API_BASE}/detect-image"
    payload_data = {"image": image_url}
    if debug:
        payload_data["debug"] = True
    payload = json.dumps(payload_data).encode()
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode() if exc.fp else ""
        return {"error": f"HTTP {exc.code}", "detail": body}
    except urllib.error.URLError as exc:
        return {"error": "connection_failed", "detail": str(exc.reason)}


def _detect_image_file(file_path: str, api_key: str, debug: bool = False) -> dict:
    """Upload a local image file to BitMind for deepfake detection."""
    endpoint = f"{BITMIND_API_BASE}/detect-image"
    boundary = "----MindSecBoundary9876543210"

    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1].lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
        ".avif": "image/avif",
    }
    content_type = mime_types.get(ext, "application/octet-stream")

    with open(file_path, "rb") as f:
        file_data = f.read()

    body_parts = []
    # Image field
    body_parts.append(
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    )
    body = body_parts[0].encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        endpoint,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode() if exc.fp else ""
        return {"error": f"HTTP {exc.code}", "detail": body_text}
    except urllib.error.URLError as exc:
        return {"error": "connection_failed", "detail": str(exc.reason)}


def _detect_video_url(video_url: str, api_key: str, fps: int = 1, debug: bool = False) -> dict:
    """Send a video URL to BitMind for deepfake detection.

    Supports YouTube, Twitter/X, TikTok, and direct video URLs.
    """
    endpoint = f"{BITMIND_API_BASE}/detect-video"
    payload_data = {"video": video_url, "fps": fps}
    if debug:
        payload_data["debug"] = True
    payload = json.dumps(payload_data).encode()
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode() if exc.fp else ""
        return {"error": f"HTTP {exc.code}", "detail": body}
    except urllib.error.URLError as exc:
        return {"error": "connection_failed", "detail": str(exc.reason)}


def _detect_video_file(file_path: str, api_key: str, fps: int = 1, debug: bool = False) -> dict:
    """Upload a local video file to BitMind for deepfake detection."""
    endpoint = f"{BITMIND_API_BASE}/detect-video"
    boundary = "----MindSecBoundary9876543210"

    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1].lower()
    mime_types = {
        ".mp4": "video/mp4",
        ".mov": "video/quicktime",
        ".avi": "video/x-msvideo",
        ".mkv": "video/x-matroska",
        ".webm": "video/webm",
        ".flv": "video/x-flv",
        ".wmv": "video/x-ms-wmv",
        ".m4v": "video/x-m4v",
    }
    content_type = mime_types.get(ext, "video/mp4")

    with open(file_path, "rb") as f:
        file_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="video"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode() + file_data
    body += f"\r\n--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="fps"\r\n\r\n{fps}\r\n'.encode()
    body += f"--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        endpoint,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode() if exc.fp else ""
        return {"error": f"HTTP {exc.code}", "detail": body_text}
    except urllib.error.URLError as exc:
        return {"error": "connection_failed", "detail": str(exc.reason)}


def detect(target: str, api_key: str, fps: int = 1, debug: bool = False) -> dict:
    """Run deepfake detection via BitMind API (images and videos)."""
    is_url = target.startswith("http://") or target.startswith("https://")
    is_video = _is_video(target)

    if is_video:
        media_type = "video"
        if is_url:
            raw = _detect_video_url(target, api_key, fps=fps, debug=debug)
        else:
            if not os.path.isfile(target):
                return {"result": "error", "confidence": 0.0, "error": f"File not found: {target}"}
            raw = _detect_video_file(target, api_key, fps=fps, debug=debug)
    else:
        media_type = "image"
        if is_url:
            raw = _detect_image_url(target, api_key, debug=debug)
        else:
            if not os.path.isfile(target):
                return {"result": "error", "confidence": 0.0, "error": f"File not found: {target}"}
            raw = _detect_image_file(target, api_key, debug=debug)

    if "error" in raw:
        return {
            "result": "error",
            "confidence": 0.0,
            "error": raw.get("error"),
            "detail": raw.get("detail", ""),
        }

    # API response: {isAI: bool, confidence: float, similarity: float, objectKey: str}
    is_ai = raw.get("isAI", False)
    confidence = raw.get("confidence", 0.0)
    similarity = raw.get("similarity")

    if is_ai:
        result = "ai_generated"
    elif confidence >= 0.4:
        result = "uncertain"
    else:
        result = "authentic"

    output = {
        "result": result,
        "isAI": is_ai,
        "confidence": round(confidence, 4),
        "similarity": round(similarity, 4) if similarity is not None else None,
        "media_type": media_type,
        "method": "bitmind",
        "api_response": raw,
    }

    return output


# ---------------------------------------------------------------------------
# EXIF / metadata fallback (no API key)
# ---------------------------------------------------------------------------

# Known AI tool signatures found in EXIF / metadata
AI_SOFTWARE_SIGNATURES = [
    "stable diffusion", "midjourney", "dall-e", "dall·e", "dalle",
    "comfyui", "automatic1111", "invoke ai", "novelai", "artbreeder",
    "deepai", "craiyon", "nightcafe", "leonardo.ai", "runway",
    "pika labs", "kling", "flux", "ideogram", "firefly",
    "adobe firefly", "canva ai", "copilot", "chatgpt", "gemini",
    "sora", "luma", "grok", "imagen",
]


def _read_jpeg_exif(data: bytes) -> dict:
    """Extract basic EXIF fields from JPEG data."""
    info = {}
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        return info

    pos = 2
    while pos < len(data) - 4:
        if data[pos] != 0xFF:
            break
        marker = data[pos + 1]
        if marker == 0xDA:  # Start of scan — stop
            break
        seg_len = struct.unpack(">H", data[pos + 2 : pos + 4])[0]
        segment = data[pos + 4 : pos + 2 + seg_len]

        # APP1 (Exif)
        if marker == 0xE1 and segment[:4] == b"Exif":
            info["has_exif"] = True
            text = segment.decode("latin-1", errors="replace")
            info["exif_raw_snippet"] = text[:500]

        # APP13 (IPTC / Photoshop)
        if marker == 0xED:
            info["has_iptc"] = True

        # Comment
        if marker == 0xFE:
            info["comment"] = segment.decode("utf-8", errors="replace").strip()

        pos += 2 + seg_len

    return info


def _read_png_text(data: bytes) -> dict:
    """Extract tEXt/iTXt chunks from PNG data."""
    info = {}
    if len(data) < 8 or data[:4] != b"\x89PNG":
        return info

    pos = 8
    texts = []
    while pos + 8 < len(data):
        chunk_len = struct.unpack(">I", data[pos : pos + 4])[0]
        chunk_type = data[pos + 4 : pos + 8]
        chunk_data = data[pos + 8 : pos + 8 + chunk_len]

        if chunk_type in (b"tEXt", b"iTXt", b"zTXt"):
            try:
                text = chunk_data.decode("utf-8", errors="replace")
                texts.append(text[:300])
            except Exception:
                pass

        pos += 12 + chunk_len  # 4 len + 4 type + data + 4 crc

    if texts:
        info["png_text_chunks"] = texts

    return info


def detect_with_metadata(file_path: str) -> dict:
    """Analyze image metadata for AI generation signatures."""
    if not os.path.isfile(file_path):
        return {
            "result": "error",
            "confidence": 0.0,
            "method": "metadata",
            "error": f"File not found: {file_path}",
        }

    findings = []
    try:
        with open(file_path, "rb") as f:
            data = f.read(1024 * 1024)  # Read first 1MB
    except OSError as exc:
        return {
            "result": "error",
            "confidence": 0.0,
            "method": "metadata",
            "error": str(exc),
        }

    ext = os.path.splitext(file_path)[1].lower()

    # Extract metadata based on format
    meta = {}
    if ext in (".jpg", ".jpeg"):
        meta = _read_jpeg_exif(data)
    elif ext == ".png":
        meta = _read_png_text(data)

    # Check for AI software signatures
    searchable = json.dumps(meta).lower()
    for sig in AI_SOFTWARE_SIGNATURES:
        if sig in searchable:
            findings.append(f"AI tool signature found: '{sig}'")

    # Check for generation parameters in PNG text chunks
    for chunk in meta.get("png_text_chunks", []):
        chunk_lower = chunk.lower()
        if any(kw in chunk_lower for kw in ("prompt", "negative prompt", "sampler", "cfg scale", "seed", "steps")):
            findings.append("Generation parameters found in PNG metadata")
            break

    # Check comment field
    comment = meta.get("comment", "").lower()
    for sig in AI_SOFTWARE_SIGNATURES:
        if sig in comment:
            findings.append(f"AI tool in comment: '{sig}'")

    # Heuristic: no EXIF in JPEG is suspicious (cameras always add EXIF)
    if ext in (".jpg", ".jpeg") and not meta.get("has_exif"):
        findings.append("JPEG has no EXIF data (unusual for camera photos)")

    # Determine result
    if findings:
        confidence = min(0.3 + 0.2 * len(findings), 0.9)
        result = "ai_generated" if confidence >= 0.6 else "suspicious"
    else:
        confidence = 0.2
        result = "no_indicators"

    return {
        "result": result,
        "confidence": round(confidence, 4),
        "method": "metadata",
        "findings": findings,
        "note": "Metadata analysis is heuristic only. Use BitMind API (set BITMIND_API_KEY) for accurate detection.",
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Detect AI-generated or deepfake images and videos.",
        epilog="Set BITMIND_API_KEY for accurate detection via BitMind API. "
               "Without it, falls back to metadata/EXIF heuristic analysis (images only). "
               "Get your key at https://app.bitmind.ai/api/keys",
    )
    parser.add_argument(
        "target",
        help="Image/video file path or URL to analyze. "
             "Supports YouTube, Twitter/X, TikTok URLs for video.",
    )
    parser.add_argument(
        "--method",
        choices=["auto", "bitmind", "metadata"],
        default="auto",
        help="Detection method. 'auto' uses BitMind if API key is set, "
             "otherwise falls back to metadata analysis. (default: auto)",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=1,
        help="Frames per second for video analysis (1-30). Higher = more accurate "
             "but slower. (default: 1)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Request debug info from API (C2PA, absurdity, timing).",
    )
    args = parser.parse_args()

    api_key = os.environ.get("BITMIND_API_KEY", "").strip()

    if args.method == "bitmind" or (args.method == "auto" and api_key):
        if not api_key:
            print(
                "Error: BITMIND_API_KEY not set.\n\n"
                "Get your API key:\n"
                "  1. Create an account at https://app.bitmind.ai\n"
                "  2. Go to https://app.bitmind.ai/api/keys\n"
                "  3. Generate a new API key\n\n"
                "Then: export BITMIND_API_KEY=your_key_here\n\n"
                "Or use --method metadata for local heuristic analysis.",
                file=sys.stderr,
            )
            sys.exit(1)
        result = detect(args.target, api_key, fps=args.fps, debug=args.debug)
    else:
        # Metadata fallback (images only)
        if _is_video(args.target):
            print(
                "Error: Video analysis requires the BitMind API.\n\n"
                "Set BITMIND_API_KEY to analyze videos.\n"
                "Get your key at https://app.bitmind.ai/api/keys",
                file=sys.stderr,
            )
            sys.exit(1)
        if args.target.startswith("http://") or args.target.startswith("https://"):
            print(
                "Error: Metadata analysis requires a local file, not a URL.\n\n"
                "Set BITMIND_API_KEY to analyze URLs.\n"
                "Get your key at https://app.bitmind.ai/api/keys",
                file=sys.stderr,
            )
            sys.exit(1)
        result = detect_with_metadata(args.target)

    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("result") != "error" else 1)


if __name__ == "__main__":
    main()
