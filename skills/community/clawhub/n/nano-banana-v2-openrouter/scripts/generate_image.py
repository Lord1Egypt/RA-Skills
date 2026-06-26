#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.28.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate/edit images using Gemini 3.1 Flash Image Preview via OpenRouter.

Usage:
    uv run generate_image.py --prompt "your image description" --filename "output.png" [--resolution 0.5K|1K|2K|4K] [--api-key KEY]
"""

import argparse
import base64
import os
import sys
from io import BytesIO
from pathlib import Path

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "google/gemini-3.1-flash-image-preview"


def get_api_key(provided_key: str | None) -> str | None:
    if provided_key:
        return provided_key
    return os.environ.get("OPENROUTER_API_KEY")


def image_to_data_url(img) -> str:
    """Convert a PIL Image to a base64 data URL."""
    buf = BytesIO()
    img_format = "PNG" if img.mode == "RGBA" else "JPEG"
    img.save(buf, format=img_format)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    mime = f"image/{img_format.lower()}"
    return f"data:{mime};base64,{b64}"


def save_image_from_data_url(data_url: str, output_path: Path) -> bool:
    """Decode a base64 data URL and save as PNG."""
    from PIL import Image as PILImage

    prefix = "data:"
    if not data_url.startswith(prefix):
        return False

    header, b64_data = data_url.split(",", 1)
    image_data = base64.b64decode(b64_data)
    image = PILImage.open(BytesIO(image_data))

    if image.mode == "RGBA":
        rgb_image = PILImage.new("RGB", image.size, (255, 255, 255))
        rgb_image.paste(image, mask=image.split()[3])
        rgb_image.save(str(output_path), "PNG")
    elif image.mode == "RGB":
        image.save(str(output_path), "PNG")
    else:
        image.convert("RGB").save(str(output_path), "PNG")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate/edit images using Gemini 3.1 Flash Image Preview via OpenRouter"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description/prompt",
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output filename (e.g., sunset-mountains.png)",
    )
    parser.add_argument(
        "--input-image", "-i",
        help="Optional input image path for editing/modification",
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["0.5K", "1K", "2K", "4K"],
        default="1K",
        help="Output resolution: 0.5K, 1K (default), 2K, or 4K",
    )
    parser.add_argument(
        "--api-key", "-k",
        help="OpenRouter API key (overrides OPENROUTER_API_KEY env var)",
    )

    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set OPENROUTER_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    import requests
    from PIL import Image as PILImage

    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_resolution = args.resolution

    # Build message content
    if args.input_image:
        try:
            input_image = PILImage.open(args.input_image)
            print(f"Loaded input image: {args.input_image}")

            if args.resolution == "1K":
                width, height = input_image.size
                max_dim = max(width, height)
                if max_dim >= 3000:
                    output_resolution = "4K"
                elif max_dim >= 1500:
                    output_resolution = "2K"
                else:
                    output_resolution = "1K"
                print(f"Auto-detected resolution: {output_resolution} (from input {width}x{height})")

            data_url = image_to_data_url(input_image)
            content = [
                {"type": "image_url", "image_url": {"url": data_url}},
                {"type": "text", "text": args.prompt},
            ]
            print(f"Editing image with resolution {output_resolution}...")
        except Exception as e:
            print(f"Error loading input image: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        content = args.prompt
        print(f"Generating image with resolution {output_resolution}...")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    request_body = {
        "model": MODEL_ID,
        "messages": [
            {"role": "user", "content": content},
        ],
        "modalities": ["image", "text"],
        "image_config": {
            "image_size": output_resolution,
        },
    }

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            json=request_body,
            headers=headers,
            timeout=300,
        )
        response.raise_for_status()
        result = response.json()

        if "error" in result:
            err = result["error"]
            print(
                f"Error from API: [{err.get('code', '?')}] {err.get('message', 'Unknown error')}",
                file=sys.stderr,
            )
            sys.exit(1)

        image_saved = False
        choices = result.get("choices", [])
        if choices:
            message = choices[0].get("message", {})

            text_content = message.get("content")
            if text_content:
                print(f"Model response: {text_content}")

            images = message.get("images", [])
            for img_entry in images:
                img_url = img_entry.get("image_url", {}).get("url", "")
                if img_url and save_image_from_data_url(img_url, output_path):
                    image_saved = True
                    break

        if image_saved:
            full_path = output_path.resolve()
            print(f"\nImage saved: {full_path}")
        else:
            print(
                "Error: No image was generated in the response. "
                "Try adjusting --prompt or simplify the request.",
                file=sys.stderr,
            )
            sys.exit(1)

    except requests.exceptions.HTTPError as e:
        error_body = ""
        if e.response is not None:
            try:
                error_body = e.response.json().get("error", {}).get("message", e.response.text)
            except Exception:
                error_body = e.response.text
        print(f"Error: API request failed: {e}\n{error_body}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(
            "Error: API request timed out (300s). "
            "Try simplifying the prompt or reducing resolution.",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
