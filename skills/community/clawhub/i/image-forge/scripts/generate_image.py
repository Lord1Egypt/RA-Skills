#!/usr/bin/env python3
# /// script
# dependencies = [
#   "google-genai>=1.0.0",
#   "pillow>=10.0.0",
# ]
# ///

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from google import genai
from google.genai import types

ALLOWED_ASPECT_RATIOS = ["1:1", "3:4", "4:3", "9:16", "16:9"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an image with Gemini and save it as PNG."
    )
    parser.add_argument(
        "-p",
        "--prompt",
        required=True,
        help="English prompt used for image generation.",
    )
    parser.add_argument(
        "-f",
        "--filename",
        required=True,
        help="Output filename or path for the generated PNG.",
    )
    parser.add_argument(
        "-i",
        "--input-image",
        action="append",
        dest="input_images",
        metavar="IMAGE",
        help="Input image path(s) for editing/composition. Can be specified multiple times (up to 14).",
    )
    parser.add_argument(
        "-a",
        "--aspect-ratio",
        default="1:1",
        choices=ALLOWED_ASPECT_RATIOS,
        help="Aspect ratio for image generation.",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="gemini-3.1-flash-image-preview",
        help="Gemini image model name.",
    )
    parser.add_argument(
        "-k",
        "--api-key",
        default=None,
        help="API key override. Fallback: GEMINI_API_KEY -> NANO_BANANA_API_KEY.",
    )
    return parser.parse_args()


def resolve_api_key(cli_api_key: str | None) -> str:
    api_key = cli_api_key or os.getenv("GEMINI_API_KEY") or os.getenv("NANO_BANANA_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing API key. Provide --api-key or set GEMINI_API_KEY/NANO_BANANA_API_KEY."
        )
    return api_key


def ensure_png_path(filename: str) -> Path:
    path = Path(filename).expanduser()
    if path.suffix.lower() != ".png":
        path = path.with_suffix(".png")

    if path.parent == Path("."):
        sanitized_name = re.sub(r"[^\w\-.\u4e00-\u9fff]", "-", path.name)
        path = Path.cwd() / sanitized_name

    path.parent.mkdir(parents=True, exist_ok=True)
    return path.resolve()


def extract_and_save_image(response, output_path: Path) -> None:
    parts = getattr(response, "parts", None)
    if parts is None and getattr(response, "candidates", None):
        try:
            parts = response.candidates[0].content.parts
        except Exception:
            parts = None

    if not parts:
        raise RuntimeError("Gemini returned no content parts.")

    for part in parts:
        if getattr(part, "inline_data", None):
            image = part.as_image()
            try:
                image.save(output_path, format="PNG")
            except TypeError:
                # google-genai Image.save() may not accept format kwarg
                image.save(str(output_path))
            return

    raise RuntimeError("Gemini response did not include image data.")


def load_input_images(paths: list[str] | None) -> list:
    """Load input images as PIL Image objects for editing/composition."""
    if not paths:
        return []
    if len(paths) > 14:
        raise ValueError(f"Too many input images ({len(paths)}). Maximum is 14.")

    from PIL import Image as PILImage

    images = []
    for img_path in paths:
        try:
            with PILImage.open(img_path) as img:
                images.append(img.copy())
            print(f"Loaded input image: {img_path}")
        except Exception as e:
            raise ValueError(f"Failed to load input image '{img_path}': {e}") from e
    return images


def main() -> int:
    args = parse_args()

    try:
        api_key = resolve_api_key(args.api_key)
        output_path = ensure_png_path(args.filename)

        # Load reference images if provided
        input_images = load_input_images(args.input_images)

        # Build contents: images first (if any), then the text prompt
        if input_images:
            contents = [*input_images, args.prompt]
            print(f"Editing/composing {len(input_images)} image(s) with prompt...")
        else:
            contents = args.prompt
            print(f"Generating image from prompt...")

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=args.model,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio=args.aspect_ratio),
            ),
        )

        extract_and_save_image(response, output_path)

        print(f"MEDIA: {output_path}")
        return 0

    except KeyboardInterrupt:
        print("Error: Generation interrupted by user.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
