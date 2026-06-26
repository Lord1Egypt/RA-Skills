#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate images using OpenRouter (Google Gemini 3 Pro Image Preview).

Usage:
    uv run generate_image.py --prompt "your image description" --filename "output.png" [--resolution 1K|2K|4K] [--api-key KEY]
"""

import argparse
import base64
import os
import sys
from pathlib import Path
from typing import Any

def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("OPENROUTER_KEY")

def pil_image_to_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        raw = f.read()
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:image/png;base64,{b64}"

def save_data_url_to_png(data_url: str, output_path: Path) -> None:
    if "," not in data_url:
        raise ValueError("Invalid image data URL")
    _, b64 = data_url.split(",", 1)
    image_bytes = base64.b64decode(b64)

    from io import BytesIO
    from PIL import Image as PILImage

    image = PILImage.open(BytesIO(image_bytes))
    if image.mode == "RGBA":
        rgb_image = PILImage.new("RGB", image.size, (255, 255, 255))
        rgb_image.paste(image, mask=image.split()[3])
        rgb_image.save(str(output_path), "PNG")
    elif image.mode == "RGB":
        image.save(str(output_path), "PNG")
    else:
        image.convert("RGB").save(str(output_path), "PNG")

def post_openrouter(payload: dict[str, Any], api_key: str) -> dict[str, Any]:
    import requests

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=180)
    if not resp.ok:
        raise RuntimeError(f"OpenRouter API error: HTTP {resp.status_code}: {resp.text}")
    return resp.json()

def get_default_output_dir() -> Path:
    """Get default output directory: skill_dir/output_images"""
    script_dir = Path(__file__).parent.parent  # scripts/../ = skill root
    output_dir = script_dir / "output_images"
    return output_dir


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using OpenRouter (Google Gemini 3 Pro Image Preview)"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description/prompt"
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output filename (e.g., sunset-mountains.png)"
    )
    parser.add_argument(
        "--input-image", "-i",
        help="Optional input image path for editing/modification"
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["1K", "2K", "4K"],
        default="1K",
        help="Output resolution: 1K (default), 2K, or 4K"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="OpenRouter API key (overrides OPENROUTER_KEY env var)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        help="Output directory (default: skill_dir/output_images)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set OPENROUTER_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    from PIL import Image as PILImage

    # Set up output path
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = get_default_output_dir()
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / args.filename

    # Load input image if provided
    input_image = None
    output_resolution = args.resolution
    if args.input_image:
        try:
            input_image = PILImage.open(args.input_image)
            print(f"Loaded input image: {args.input_image}")

            # Auto-detect resolution if not explicitly set by user
            if args.resolution == "1K":  # Default value
                # Map input image size to resolution
                width, height = input_image.size
                max_dim = max(width, height)
                if max_dim >= 3000:
                    output_resolution = "4K"
                elif max_dim >= 1500:
                    output_resolution = "2K"
                else:
                    output_resolution = "1K"
                print(f"Auto-detected resolution: {output_resolution} (from input {width}x{height})")
        except Exception as e:
            print(f"Error loading input image: {e}", file=sys.stderr)
            sys.exit(1)

    # Build contents (image first if editing, prompt only if generating)
    if input_image:
        contents = [
            {
                "type": "image_url",
                "image_url": {
                    "url": pil_image_to_data_url(args.input_image),
                },
            },
            {"type": "text", "text": args.prompt},
        ]
        print(f"Editing image with resolution {output_resolution}...")
    else:
        contents = args.prompt
        print(f"Generating image with resolution {output_resolution}...")

    try:
        payload: dict[str, Any] = {
            "model": "google/gemini-3-pro-image-preview",
            "messages": [
                {
                    "role": "user",
                    "content": contents,
                }
            ],
            "modalities": ["image", "text"],
            "image_config": {
                "image_size": output_resolution,
            },
        }

        result = post_openrouter(payload=payload, api_key=api_key)
        choices = result.get("choices")
        if not choices:
            print("Error: No choices returned from API.", file=sys.stderr)
            sys.exit(1)

        message = choices[0].get("message") or {}
        content_text = message.get("content")
        if content_text:
            print(f"Model response: {content_text}")

        images = message.get("images") or []
        if not images:
            print("Error: No image was generated in the response.", file=sys.stderr)
            sys.exit(1)

        image_url = images[0].get("image_url", {}).get("url")
        if not image_url:
            print("Error: Image URL missing in response.", file=sys.stderr)
            sys.exit(1)

        save_data_url_to_png(image_url, output_path)
        full_path = output_path.resolve()
        print(f"\nImage saved: {full_path}")

    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
