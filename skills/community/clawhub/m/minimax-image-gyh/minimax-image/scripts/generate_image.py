#!/usr/bin/env python3
"""
MiniMax Image - MiniMax Image Generation Script

Cross-platform image generation using MiniMax API.
Works on Windows, macOS, and Linux.

Usage:
    python generate_image.py "prompt" [output_path]

Environment variables:
    MINIMAX_API_KEY (required) - Your MiniMax API key
    IMAGE_SIZE (optional) - Image size: "1K" (default), "2K", or "4K"
    IMAGEAspectRatio (optional) - Aspect ratio: "1:1" (default), "16:9", "9:16", "3:4", "4:3"
"""

import argparse
import json
import os
import sys
import requests
from pathlib import Path


# Configuration
DEFAULT_MODEL_ID = "image-01"
API_BASE_URL = "https://api.minimaxi.com"
DEFAULT_IMAGE_SIZE = "1K"
DEFAULT_ASPECT_RATIO = "1:1"
VALID_SIZES = {"1K", "2K", "4K"}
VALID_ASPECTS = {"1:1", "16:9", "9:16", "3:4", "4:3"}
# Default API key (fallback if MINIMAX_API_KEY env var not set)
DEFAULT_API_KEY = "sk-cp-MFXJC1WqfJR0j-ZDmIdOlAvkhfoiu3awjraCF2b7jDeKnIkAucoebrHj_KIrqwdxWjiCHDpIGGmPBjvE62g86MnubennRzM8fBy_Iq9615D7RX7W1dvmiG0"


def get_api_endpoint() -> str:
    """Build the API endpoint URL."""
    return f"{API_BASE_URL}/v1/image_generation"


def get_api_key() -> str:
    """Get the MiniMax API key from environment variable, or use default."""
    api_key = os.environ.get("MINIMAX_API_KEY") or DEFAULT_API_KEY
    if not api_key or api_key == "your-api-key-here":
        print("Error: MINIMAX_API_KEY environment variable not set and no default key available", file=sys.stderr)
        print("\nTo set it:", file=sys.stderr)
        print("  Windows (PowerShell): $env:MINIMAX_API_KEY = 'your-key'", file=sys.stderr)
        print("  Windows (CMD): set MINIMAX_API_KEY=your-key", file=sys.stderr)
        print("  macOS/Linux: export MINIMAX_API_KEY='your-key'", file=sys.stderr)
        print("\nGet your key from MiniMax dashboard:", file=sys.stderr)
        sys.exit(1)
    return api_key


def validate_image_size(size: str) -> str:
    """Validate and return the image size."""
    if size not in VALID_SIZES:
        print(f"Warning: Invalid IMAGE_SIZE '{size}'. Using default '{DEFAULT_IMAGE_SIZE}'", file=sys.stderr)
        return DEFAULT_IMAGE_SIZE
    return size


def validate_aspect_ratio(aspect: str) -> str:
    """Validate and return the aspect ratio."""
    if aspect not in VALID_ASPECTS:
        print(f"Warning: Invalid IMAGEAspectRatio '{aspect}'. Using default '{DEFAULT_ASPECT_RATIO}'", file=sys.stderr)
        return DEFAULT_ASPECT_RATIO
    return aspect


def create_output_dir(output_path: Path) -> None:
    """Create output directory if it doesn't exist."""
    output_dir = output_path.parent
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)


def build_request_body(prompt: str, image_size: str, aspect_ratio: str) -> dict:
    """Build the JSON request body for the API."""
    request_data = {
        "model": DEFAULT_MODEL_ID,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "n": 1,
        "response_format": "url"
    }
    return request_data


def make_api_request(api_key: str, request_body: dict) -> dict:
    """Make the API request and return the response."""
    endpoint = get_api_endpoint()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.post(endpoint, headers=headers, json=request_body, timeout=120)
        
        if response.status_code != 200:
            error_detail = response.text
            try:
                error_data = response.json()
                error_detail = error_data.get("base_resp", {}).get("status_msg", error_detail)
            except:
                pass
            
            if response.status_code == 429:
                print("=" * 60, file=sys.stderr)
                print("ERROR: MiniMax API rate limit exceeded", file=sys.stderr)
                print("=" * 60, file=sys.stderr)
                print("\nWhat to do:", file=sys.stderr)
                print("  1. Wait a moment and try again", file=sys.stderr)
                print("  2. Check your API usage limits", file=sys.stderr)
            elif response.status_code == 403:
                print("=" * 60, file=sys.stderr)
                print("ERROR: MiniMax API access denied", file=sys.stderr)
                print("=" * 60, file=sys.stderr)
                print("\nYour API key is invalid or lacks required permissions.", file=sys.stderr)
            elif response.status_code == 400:
                print("=" * 60, file=sys.stderr)
                print("ERROR: Invalid request to MiniMax API", file=sys.stderr)
                print("=" * 60, file=sys.stderr)
                print(f"\nAPI message: {error_detail}", file=sys.stderr)
            else:
                print(f"Error: API request failed with HTTP status {response.status_code}", file=sys.stderr)
                print(f"API message: {error_detail}", file=sys.stderr)
            sys.exit(1)
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print("=" * 60, file=sys.stderr)
        print("ERROR: Failed to connect to MiniMax API", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(f"\nConnection error: {e}", file=sys.stderr)
        print("\nWhat to do:", file=sys.stderr)
        print("  1. Check your internet connection", file=sys.stderr)
        print("  2. Verify the API endpoint is accessible", file=sys.stderr)
        sys.exit(1)


def extract_image_url(response: dict) -> str:
    """Extract image URL from the API response."""
    try:
        # MiniMax response structure
        image_urls = response.get("data", {}).get("image_urls", [])
        if image_urls and len(image_urls) > 0:
            return image_urls[0]

        raise ValueError("No image URL found in response")
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error: Failed to parse response: {e}", file=sys.stderr)
        print(f"Response: {json.dumps(response, indent=2)}", file=sys.stderr)
        sys.exit(1)


def download_and_save_image(url: str, output_path: Path) -> None:
    """Download image from URL and save to file."""
    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        output_path.write_bytes(response.content)
    except Exception as e:
        print(f"Error: Failed to download image: {e}", file=sys.stderr)
        sys.exit(1)


def get_file_size(path: Path) -> str:
    """Get human-readable file size."""
    size = path.stat().st_size
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using MiniMax AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_image.py "A sunset over mountains"
  python generate_image.py "An app icon" ./icons/app.png
  python generate_image.py --size 2K "High-res landscape" ./wallpaper.png
  python generate_image.py --aspect 16:9 "Wide banner" ./banner.png

Environment Variables:
  MINIMAX_API_KEY     Your MiniMax API key (required)
  IMAGE_SIZE          Image size: 1K (default), 2K, or 4K
  IMAGEAspectRatio    Aspect ratio: 1:1 (default), 16:9, 9:16, 3:4, 4:3
        """
    )
    parser.add_argument("prompt", help="Text description of the image to generate")
    parser.add_argument("output", nargs="?", default="./generated-image.png",
                        help="Output file path (default: ./generated-image.png)")
    parser.add_argument("--size", choices=["1K", "2K", "4K"],
                        help="Image size (overrides IMAGE_SIZE env var)")
    parser.add_argument("--aspect", "--aspect-ratio", dest="aspect_ratio",
                        choices=["1:1", "16:9", "9:16", "3:4", "4:3"],
                        help="Aspect ratio (overrides IMAGEAspectRatio env var)")

    args = parser.parse_args()

    # Get configuration
    api_key = get_api_key()
    image_size = args.size or os.environ.get("IMAGE_SIZE", DEFAULT_IMAGE_SIZE)
    image_size = validate_image_size(image_size)
    aspect_ratio = args.aspect_ratio or os.environ.get("IMAGEAspectRatio", DEFAULT_ASPECT_RATIO)
    aspect_ratio = validate_aspect_ratio(aspect_ratio)
    output_path = Path(args.output)

    # Create output directory
    create_output_dir(output_path)

    # Display info
    print(f"Generating image with prompt: \"{args.prompt}\"")
    print(f"Model: {DEFAULT_MODEL_ID}")
    print(f"Image size: {image_size}")
    print(f"Aspect ratio: {aspect_ratio}")
    print(f"Output path: {output_path}")
    print()

    # Build and send request
    request_body = build_request_body(args.prompt, image_size, aspect_ratio)
    response = make_api_request(api_key, request_body)

    # Extract and save image
    image_url = extract_image_url(response)
    if not image_url:
        print("Error: No image URL received from API", file=sys.stderr)
        sys.exit(1)

    print(f"\nDownloading image from URL...")
    download_and_save_image(image_url, output_path)

    # Verify and report success
    if output_path.exists() and output_path.stat().st_size > 0:
        file_size = get_file_size(output_path)
        print("Success! Image generated and saved.")
        print(f"File: {output_path}")
        print(f"Size: {file_size}")
    else:
        print(f"Error: Failed to save image to {output_path}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
