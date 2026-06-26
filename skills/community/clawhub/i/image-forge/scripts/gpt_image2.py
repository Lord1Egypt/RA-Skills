#!/usr/bin/env python3
# /// script
# dependencies = ["requests>=2.28.0"]
# ///
"""
GPT Image 2 CLI wrapper for image-forge skill.
Supports: generate (text-to-image) and edit (image-to-image).

Usage:
  # Generate
  python gpt_image2.py generate --prompt "..." --output /path/out.png [--size 1536x1024] [--quality high]

  # Edit (single reference image)
  python gpt_image2.py edit --prompt "..." --image /path/ref.png --output /path/out.png

  # Edit (multiple reference images, up to 4)
  python gpt_image2.py edit --prompt "..." --image ref1.png --image ref2.png --output /path/out.png

Environment:
  CRS_BASE_URL  CRS service base URL (default: http://127.0.0.1:8765)
  CRS_API_KEY   CRS API key (required)
"""
from __future__ import annotations

import argparse
import base64
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("Missing dependency: pip install requests", file=sys.stderr)
    sys.exit(1)

CRS_BASE = os.environ.get("CRS_BASE_URL", "http://127.0.0.1:8765")
CRS_KEY = os.environ.get("CRS_API_KEY", "")

VALID_SIZES = [
    "1024x1024", "1536x1024", "1024x1536",
    "2048x2048", "3840x2160", "2160x3840",
]
DEFAULT_SIZE_GENERATE = "1536x1024"
DEFAULT_SIZE_EDIT     = "1024x1536"


def get_headers() -> dict:
    if not CRS_KEY:
        print("Error: CRS_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    return {"Authorization": f"Bearer {CRS_KEY}"}


def read_image_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def detect_mime(path: str) -> str:
    ext = Path(path).suffix.lower()
    return {"jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(ext, "image/png")


def save_result(data: dict, output: str, fmt: str = "png") -> str:
    out_path = output or f"/tmp/gpt-image2-{int(time.time())}.{fmt}"
    b64 = data.get("b64_json", "")
    if not b64:
        print("Error: no b64_json in response", file=sys.stderr)
        sys.exit(1)
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(b64))
    return out_path


def cmd_generate(args: argparse.Namespace) -> None:
    payload = {
        "model": "gpt-image-2",
        "prompt": args.prompt,
        "size": args.size or DEFAULT_SIZE_GENERATE,
        "quality": args.quality,
        "output_format": args.format,
        "response_format": "b64_json",
    }
    if args.background:
        payload["background"] = args.background

    resp = requests.post(
        f"{CRS_BASE}/openai/v1/images/generations",
        headers=get_headers(),
        json=payload,
        timeout=args.timeout,
    )
    _handle_response(resp, args)


def cmd_edit(args: argparse.Namespace) -> None:
    if not args.image:
        print("Error: --image required for edit", file=sys.stderr)
        sys.exit(1)

    images = []
    for img_path in args.image:
        mime = detect_mime(img_path)
        b64 = read_image_b64(img_path)
        images.append({"image_url": f"data:{mime};base64,{b64}"})

    payload = {
        "model": "gpt-image-2",
        "prompt": args.prompt,
        "images": images,
        "size": args.size or DEFAULT_SIZE_EDIT,
        "quality": args.quality,
        "output_format": args.format,
        "response_format": "b64_json",
    }

    resp = requests.post(
        f"{CRS_BASE}/openai/v1/images/edits",
        headers=get_headers(),
        json=payload,
        timeout=args.timeout,
    )
    _handle_response(resp, args)


def _handle_response(resp: requests.Response, args: argparse.Namespace) -> None:
    try:
        d = resp.json()
    except Exception:
        print(f"Error: non-JSON response (HTTP {resp.status_code})", file=sys.stderr)
        print(resp.text[:500], file=sys.stderr)
        sys.exit(1)

    if "error" in d:
        print(f"API Error: {d['error'].get('message', d['error'])}", file=sys.stderr)
        sys.exit(1)

    if "data" not in d or not d["data"]:
        print(f"Error: unexpected response: {d}", file=sys.stderr)
        sys.exit(1)

    item = d["data"][0]
    out_path = save_result(item, args.output, args.format)
    print(f"MEDIA: {os.path.abspath(out_path)}")

    if item.get("revised_prompt"):
        print(f"# revised_prompt: {item['revised_prompt'][:200]}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="GPT Image 2 CLI for image-forge")
    sub = parser.add_subparsers(dest="command", required=True)

    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("-p", "--prompt", required=True)
    shared.add_argument("-o", "--output", default="")
    shared.add_argument("--size", choices=VALID_SIZES, default="")
    shared.add_argument("--quality", choices=["standard", "high"], default="high")
    shared.add_argument("--format", choices=["png", "webp", "jpeg"], default="png", dest="format")
    shared.add_argument("--timeout", type=int, default=180)

    # generate
    gen = sub.add_parser("generate", parents=[shared])
    gen.add_argument("--background", choices=["transparent", "white", "auto"], default="")

    # edit
    edit = sub.add_parser("edit", parents=[shared])
    edit.add_argument("-i", "--image", action="append", metavar="PATH",
                      help="Reference image path (repeat for multiple, max 4)")

    args = parser.parse_args()

    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "edit":
        cmd_edit(args)


if __name__ == "__main__":
    main()
