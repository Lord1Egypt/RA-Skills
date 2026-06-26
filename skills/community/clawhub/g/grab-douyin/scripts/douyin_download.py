#!/usr/bin/env python3
"""
Douyin Video Downloader — powered by TikHub API.

Supports:
  - Short links:  https://v.douyin.com/xxxxx/
  - Full URLs:    https://www.douyin.com/video/<modal_id>
  - Query params: https://www.douyin.com/jingxuan?modal_id=<modal_id>
  - Bare IDs:     7615599455526585067  (16–19 digit number)

Token config: ~/.openclaw/config.json → { "tikhub_api_token": "..." }
"""

import argparse
import json
import os
import re
import sys
import urllib.parse

import requests

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TIKHUB_API_URL = "https://api.tikhub.io/api/v1/douyin/web/fetch_one_video"
DEFAULT_OUTPUT_DIR = os.path.expanduser("~/Downloads/douyin")


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def load_config() -> dict:
    """Load ~/.openclaw/config.json, returning an empty dict if missing."""
    path = os.path.expanduser("~/.openclaw/config.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def get_token() -> str:
    """
    Return the TikHub API token from config.
    Raises ValueError with a friendly message if it's missing.
    """
    token = load_config().get("tikhub_api_token")
    if not token:
        raise ValueError(
            "Missing TikHub API token.\n\n"
            "Add it to ~/.openclaw/config.json:\n"
            '  { "tikhub_api_token": "your-token" }\n\n'
            "Get a free token at: https://user.tikhub.io/register"
        )
    return token


# ---------------------------------------------------------------------------
# Input parsing
# ---------------------------------------------------------------------------

def resolve_short_link(url: str) -> str:
    """
    Follow redirects on a v.douyin.com short link and return the final URL.
    This is needed because short links don't embed the modal_id directly.
    """
    try:
        resp = requests.head(url, allow_redirects=True, timeout=10)
        return resp.url
    except requests.RequestException as e:
        raise ValueError(f"Could not resolve short link '{url}': {e}") from e


def extract_modal_id(user_input: str) -> str:
    """
    Extract a Douyin modal_id (aweme_id) from any of the supported input formats.

    Tries, in order:
      1. Bare 16–19 digit number
      2. modal_id= query param
      3. /video/<id> path segment
      4. Short link resolution (v.douyin.com) → recurse with resolved URL
    """
    text = user_input.strip()

    # 1. Bare numeric ID
    if re.fullmatch(r"\d{16,19}", text):
        return text

    # 2. modal_id query param
    m = re.search(r"[?&]modal_id=(\d{16,19})", text)
    if m:
        return m.group(1)

    # 3. /video/<id> path segment
    m = re.search(r"/video/(\d{16,19})", text)
    if m:
        return m.group(1)

    # 4. Short link — resolve then retry
    if "v.douyin.com" in text:
        resolved = resolve_short_link(text)
        if resolved != text:
            return extract_modal_id(resolved)

    raise ValueError(
        f"Could not find a Douyin modal_id in: {text!r}\n\n"
        "Expected a v.douyin.com short link, a full douyin.com URL, or a 16–19 digit ID."
    )


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def fetch_video_url(modal_id: str, token: str) -> str:
    """
    Call TikHub API and extract the direct video download URL.
    Returns the first matching aweme/v1/play/ URL found in the response.
    """
    params = {"aweme_id": modal_id, "need_anchor_info": "false"}
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(TIKHUB_API_URL, params=params, headers=headers, timeout=30)
    resp.raise_for_status()

    # Unescape any JSON-encoded slashes before searching
    body = resp.text.replace("\\/", "/")

    m = re.search(r"(https://www\.douyin\.com/aweme/v1/play/[^\s\"<>\\]+)", body)
    if not m:
        raise ValueError(
            f"TikHub returned a response but no video URL was found for modal_id={modal_id}. "
            "The video may be private, deleted, or unsupported."
        )
    return m.group(1)


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

def download_video(video_url: str, modal_id: str, output_dir: str) -> str:
    """
    Download a video from video_url and save it to output_dir.
    Returns the path of the saved file.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"douyin_{modal_id}.mp4")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.douyin.com/",
    }

    resp = requests.get(video_url, headers=headers, timeout=120, stream=True)
    resp.raise_for_status()

    total = int(resp.headers.get("content-length", 0))
    downloaded = 0

    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=65536):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded / total * 100
                    print(f"\r  {pct:.1f}%  ({downloaded // 1024} KB / {total // 1024} KB)", end="", flush=True)

    if total:
        print()  # newline after progress

    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="douyin_download.py",
        description="Download a Douyin video via TikHub API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 douyin_download.py "https://v.douyin.com/iABCxyz/"
  python3 douyin_download.py "https://v.douyin.com/iABCxyz/" --download
  python3 douyin_download.py "7615599455526585067" --download
  python3 douyin_download.py "7615599455526585067" --download --output-dir ~/Desktop
        """,
    )
    parser.add_argument(
        "input",
        help="Douyin URL (short or full) or bare modal_id (16–19 digits)",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download the video (default: just print the video URL)",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        metavar="DIR",
        help=f"Directory to save the video (default: {DEFAULT_OUTPUT_DIR})",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        token = get_token()

        print(f"🔍 Extracting modal_id from: {args.input}")
        modal_id = extract_modal_id(args.input)
        print(f"📌 modal_id: {modal_id}")

        print("📡 Fetching video URL from TikHub...")
        video_url = fetch_video_url(modal_id, token)
        print(f"🎬 Video URL: {video_url}")

        if args.download:
            output_dir = os.path.expanduser(args.output_dir)
            print(f"\n⬇️  Downloading to {output_dir} ...")
            saved_path = download_video(video_url, modal_id, output_dir)
            print(f"✅ Saved: {saved_path}")
        else:
            print("\n(Pass --download to save the video to disk.)")

    except ValueError as e:
        print(f"\n❌ {e}", file=sys.stderr)
        sys.exit(1)
    except requests.HTTPError as e:
        print(f"\n❌ HTTP error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Cancelled.")
        sys.exit(130)


if __name__ == "__main__":
    main()
