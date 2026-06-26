#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
ModelScope Image Generation Tool

⚠️ SECURITY NOTICE:
This tool ONLY connects to the official ModelScope API endpoint.
There is NO ability to customize or redirect the API endpoint.
The endpoint is hardcoded and immutable.

Official Endpoint: https://api-inference.modelscope.cn/
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image

# ==============================================================================
# SECURITY: Endpoint is hardcoded and cannot be changed
# This prevents any possibility of API key or data being redirected
# ==============================================================================
_API_ENDPOINT = "https://api-inference.modelscope.cn/"

# Timeout settings
_MAX_POLL_ATTEMPTS = 60  # Maximum 5 minutes (60 * 5 seconds)


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("MODELSCOPE_API_KEY")


def image_to_data_url(image_path: str) -> str:
    """Convert image file to data URL format."""
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(image_path, "rb") as f:
        image_data = f.read()

    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type is None or not mime_type.startswith('image/'):
        mime_type = 'image/png'

    base64_encoded = base64.b64encode(image_data).decode('utf-8')
    return f"data:{mime_type};base64,{base64_encoded}"


def parse_lora_config(lora_str: str | None) -> dict | str | None:
    """Parse LoRA configuration string.

    Formats:
        - Single LoRA: "repo-id"
        - Multiple LoRAs: "repo1:0.6,repo2:0.4"
    """
    if not lora_str:
        return None

    # Check if it's multiple LoRAs (contains comma)
    if ',' in lora_str:
        loras = {}
        for item in lora_str.split(','):
            parts = item.strip().split(':')
            if len(parts) == 2:
                repo_id = parts[0].strip()
                weight = float(parts[1].strip())
                loras[repo_id] = weight
            else:
                print(f"Warning: Invalid LoRA format '{item}', skipping.", file=sys.stderr)
        return loras if loras else None
    else:
        # Single LoRA
        return lora_str.strip()


def poll_task_result(
    api_key: str,
    task_id: str,
    max_attempts: int = _MAX_POLL_ATTEMPTS
) -> str | None:
    """Poll for task completion and return output image URL."""
    common_headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    for attempt in range(max_attempts):
        try:
            # SECURITY: Using hardcoded endpoint only
            result = requests.get(
                f"{_API_ENDPOINT}v1/tasks/{task_id}",
                headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
                timeout=30
            )
            result.raise_for_status()
            data = result.json()

            if data["task_status"] == "SUCCEED":
                return data["output_images"][0]
            elif data["task_status"] == "FAILED":
                error_msg = data.get("error", "Unknown error")
                print(f"Error: Image generation failed: {error_msg}", file=sys.stderr)
                return None

            # Wait before next poll
            time.sleep(5)

        except requests.exceptions.RequestException as e:
            print(f"Warning: Request error during polling (attempt {attempt + 1}): {e}", file=sys.stderr)
            time.sleep(5)

    print(f"Error: Task timeout after {max_attempts * 5} seconds.", file=sys.stderr)
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using ModelScope API (fixed endpoint)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
⚠️ SECURITY: This tool ONLY connects to https://api-inference.modelscope.cn/
No custom endpoint configuration is available.

Examples:
  # Text to image
  uv run generate_img.py --prompt "a cute cartoon lobster" --filename output.jpg

  # Image to image
  uv run generate_img.py --prompt "cartoon style" --input-image photo.jpg --filename cartoon.jpg

  # Specify model
  uv run generate_img.py --prompt "sunset" --filename sunset.jpg --model "MusePublic/wukong-1.8B"

  # With LoRA
  uv run generate_img.py --prompt "anime girl" --filename anime.jpg --lora "my-lora-repo:0.8"
        """
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description/prompt"
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output filename (e.g., output.jpg, result.png)"
    )
    parser.add_argument(
        "--input-image", "-i",
        help="Optional input image path for image-to-image generation"
    )
    parser.add_argument(
        "--model", "-m",
        default="Tongyi-MAI/Z-Image-Turbo",
        help="ModelScope model ID (default: Tongyi-MAI/Z-Image-Turbo)"
    )
    parser.add_argument(
        "--lora", "-l",
        help='LoRA configuration. Single: "repo-id". Multiple: "repo1:0.6,repo2:0.4"'
    )
    parser.add_argument(
        "--api-key", "-k",
        help="ModelScope API key (overrides MODELSCOPE_API_KEY env var)"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=_MAX_POLL_ATTEMPTS,
        help=f"Maximum polling attempts (default: {_MAX_POLL_ATTEMPTS}, each attempt is 5 seconds)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set MODELSCOPE_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    # Validate input image if provided
    if args.input_image:
        if not os.path.isfile(args.input_image):
            print(f"Error: Input image not found: {args.input_image}", file=sys.stderr)
            sys.exit(1)
        print(f"Loaded input image: {args.input_image}")

    # Set up output path
    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Parse LoRA configuration
    lora_config = parse_lora_config(args.lora)

    # Build request payload
    payload = {
        "model": args.model,
        "prompt": args.prompt,
    }

    # Add LoRA if specified
    if lora_config:
        payload["loras"] = lora_config

    # Add input image if provided
    if args.input_image:
        payload["image_url"] = [image_to_data_url(args.input_image)]

    # Prepare headers
    common_headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Submit generation task
    print(f"Generating image with model '{args.model}'...")
    print(f"Endpoint: {_API_ENDPOINT} (fixed, non-configurable)")
    if args.input_image:
        print(f"Mode: Image-to-Image")
    else:
        print(f"Mode: Text-to-Image")

    try:
        # SECURITY: Using hardcoded endpoint only - no base-url override possible
        response = requests.post(
            f"{_API_ENDPOINT}v1/images/generations",
            headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
            timeout=30
        )
        response.raise_for_status()
        task_id = response.json()["task_id"]
        print(f"Task submitted: {task_id}")

    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to submit task: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"Response: {error_detail}", file=sys.stderr)
            except:
                print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)

    # Poll for result
    print("Waiting for task completion...", end="", flush=True)
    output_image_url = poll_task_result(api_key, task_id, args.timeout)

    if not output_image_url:
        print()  # New line after dots
        sys.exit(1)

    # Download and save image
    try:
        print("\nDownloading result image...")
        image_response = requests.get(output_image_url, timeout=60)
        image_response.raise_for_status()

        image = Image.open(BytesIO(image_response.content))

        # Save image
        image.save(str(output_path))

        full_path = output_path.resolve()
        print(f"Image saved: {full_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to download image: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to save image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
