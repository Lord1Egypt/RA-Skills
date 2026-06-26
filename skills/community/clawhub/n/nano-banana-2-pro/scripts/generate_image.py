#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate images using Google's Nano Banana 2 (Gemini 3.1 Flash Image) API.

Usage:
    uv run generate_image.py --prompt "your image description" --filename "output.png" [options]

Options:
    --resolution 512|1K|2K|4K       Output resolution (default: 1K)
    --aspect-ratio RATIO            Aspect ratio (e.g. 1:1, 16:9, 9:16)
    --input-image PATH [PATH ...]   One or more input images (up to 14)
    --thinking-level minimal|high   Thinking level (default: minimal)
    --model MODEL                   Gemini model name (default: gemini-3.1-flash-image-preview)
    --image-only                    Return image only, no text
    --api-key KEY                   Gemini API key
"""

import argparse
import os
import sys
from pathlib import Path

VALID_ASPECT_RATIOS = [
    "1:1", "1:4", "1:8", "2:3", "3:2", "3:4",
    "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9",
]


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("GEMINI_API_KEY")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Nano Banana 2 (Gemini 3.1 Flash Image)"
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
        nargs="+",
        help="One or more input image paths (up to 14) for editing/composition"
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["512", "1K", "2K", "4K"],
        default="1K",
        help="Output resolution: 512 (0.5K), 1K (default), 2K, or 4K"
    )
    parser.add_argument(
        "--aspect-ratio", "-a",
        choices=VALID_ASPECT_RATIOS,
        default=None,
        help="Aspect ratio (e.g. 1:1, 16:9, 9:16, 1:4, 4:1, 1:8, 8:1)"
    )
    parser.add_argument(
        "--thinking-level", "-t",
        choices=["minimal", "high"],
        default=None,
        help="Thinking level: minimal (default, fastest) or high (best quality)"
    )
    parser.add_argument(
        "--model", "-m",
        default="gemini-3.1-flash-image-preview",
        help="Gemini model name (default: gemini-3.1-flash-image-preview)"
    )
    parser.add_argument(
        "--image-only",
        action="store_true",
        help="Return image only without text in response"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Gemini API key (overrides GEMINI_API_KEY env var)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set GEMINI_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    # Import here after checking API key to avoid slow import on error
    from google import genai
    from google.genai import types
    from PIL import Image as PILImage

    # Initialise client
    client = genai.Client(api_key=api_key)

    # Set up output path
    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load input images if provided
    input_images = []
    output_resolution = args.resolution
    if args.input_image:
        if len(args.input_image) > 14:
            print("Error: Maximum 14 input images supported.", file=sys.stderr)
            sys.exit(1)
        for img_path in args.input_image:
            try:
                img = PILImage.open(img_path)
                input_images.append(img)
                print(f"Loaded input image: {img_path}")
            except Exception as e:
                print(f"Error loading input image '{img_path}': {e}", file=sys.stderr)
                sys.exit(1)

        # Auto-detect resolution from first image if using default
        if args.resolution == "1K" and len(input_images) == 1:
            width, height = input_images[0].size
            max_dim = max(width, height)
            if max_dim >= 3000:
                output_resolution = "4K"
            elif max_dim >= 1500:
                output_resolution = "2K"
            else:
                output_resolution = "1K"
            print(f"Auto-detected resolution: {output_resolution} (from input {width}x{height})")

    # Build contents
    if input_images:
        contents = [*input_images, args.prompt]
        print(f"Processing {len(input_images)} image(s) with resolution {output_resolution}...")
    else:
        contents = args.prompt
        print(f"Generating image with resolution {output_resolution}...")

    # Build image config
    image_config_kwargs = {"image_size": output_resolution}
    if args.aspect_ratio:
        image_config_kwargs["aspect_ratio"] = args.aspect_ratio
        print(f"Aspect ratio: {args.aspect_ratio}")

    # Build generation config
    response_modalities = ["IMAGE"] if args.image_only else ["TEXT", "IMAGE"]
    config_kwargs = {
        "response_modalities": response_modalities,
        "image_config": types.ImageConfig(**image_config_kwargs),
    }

    # Add thinking config if specified
    if args.thinking_level:
        config_kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_level=args.thinking_level.capitalize()
        )
        print(f"Thinking level: {args.thinking_level}")

    try:
        response = client.models.generate_content(
            model=args.model,
            contents=contents,
            config=types.GenerateContentConfig(**config_kwargs),
        )

        # Process response and convert to PNG
        image_saved = False
        for part in response.parts:
            # Skip thought parts
            if hasattr(part, "thought") and part.thought:
                continue
            if part.text is not None:
                print(f"Model response: {part.text}")
            elif part.inline_data is not None:
                from io import BytesIO

                image_data = part.inline_data.data
                if isinstance(image_data, str):
                    import base64
                    image_data = base64.b64decode(image_data)

                image = PILImage.open(BytesIO(image_data))

                # Ensure RGB mode for PNG
                if image.mode == "RGBA":
                    rgb_image = PILImage.new("RGB", image.size, (255, 255, 255))
                    rgb_image.paste(image, mask=image.split()[3])
                    rgb_image.save(str(output_path), "PNG")
                elif image.mode == "RGB":
                    image.save(str(output_path), "PNG")
                else:
                    image.convert("RGB").save(str(output_path), "PNG")
                image_saved = True

        if image_saved:
            full_path = output_path.resolve()
            print(f"\nImage saved: {full_path}")
        else:
            print("Error: No image was generated in the response.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
