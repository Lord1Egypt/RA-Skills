#!/usr/bin/env python3
"""
Nano Banana Image Generation/Editing Script (based on Google Gemini native image generation API)

Usage (text-to-image):
  python3 generate.py --prompt "A futuristic city at sunset, 16:9 cinematic"

Usage (image editing):
  python3 generate.py --prompt "Change the sky to a starry night" --images photo.jpg

Usage (multi-image composition):
  python3 generate.py --prompt "Put these people in a group photo" --images p1.jpg p2.jpg p3.jpg

Usage (real-time generation with search):
  python3 generate.py --prompt "Current weather in Tokyo as a visual chart" --search

Usage (high resolution):
  python3 generate.py --prompt "..." --aspect-ratio 16:9 --image-size 4K

Dependencies: pip install google-genai Pillow
Authentication: export GEMINI_API_KEY=your_api_key
"""

import argparse
import os
import sys


def load_dotenv():
    """Load environment variables from .env file (script directory first, then parent directory). Does not overwrite existing environment variables."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, ".env"),
        os.path.join(script_dir, "..", ".env"),
    ]
    for path in candidates:
        path = os.path.normpath(path)
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = value
            break

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai is not installed. Please run: pip install google-genai", file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is not installed. Please run: pip install Pillow", file=sys.stderr)
    sys.exit(1)

# Models supporting image_size (Gemini 3 series)
GEMINI3_MODELS = {"gemini-3.1-flash-image", "gemini-3-pro-image"}
# Model supporting video input and image search
FLASH31_MODEL = "gemini-3.1-flash-image"

VALID_ASPECT_RATIOS_FLASH31 = {
    "1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3",
    "4:5", "5:4", "8:1", "9:16", "16:9", "21:9",
}
VALID_ASPECT_RATIOS_PRO = {
    "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9",
}
VALID_ASPECT_RATIOS_25FLASH = VALID_ASPECT_RATIOS_PRO
VALID_IMAGE_SIZES_FLASH31 = {"512", "1K", "2K", "4K"}
VALID_IMAGE_SIZES_PRO = {"1K", "2K", "4K"}


def get_mime_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
        ".bmp": "image/bmp",
    }
    mime = mime_map.get(ext)
    if not mime:
        print(f"Warning: Unknown image format '{ext}', trying image/jpeg", file=sys.stderr)
        return "image/jpeg"
    return mime


def load_image(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: Image file not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    return Image.open(file_path)


def save_images(parts, output_path, show_thoughts):
    """Save image parts from response. Returns number of images saved."""
    image_parts = []
    thought_parts = []

    for part in parts:
        if part.inline_data is not None:
            if getattr(part, "thought", False):
                thought_parts.append(part)
            else:
                image_parts.append(part)

    # Save non-thought images
    count = len(image_parts)
    if count == 0:
        return 0

    if count == 1:
        img = image_parts[0].as_image()
        img.save(output_path)
        print(f"Image saved: {output_path}")
    else:
        base, ext = os.path.splitext(output_path)
        if not ext:
            ext = ".png"
        for i, part in enumerate(image_parts, 1):
            path = f"{base}_{i}{ext}"
            img = part.as_image()
            img.save(path)
            print(f"Image saved: {path}")

    # Optionally save thought images
    if show_thoughts and thought_parts:
        base, ext = os.path.splitext(output_path)
        if not ext:
            ext = ".png"
        for i, part in enumerate(thought_parts, 1):
            path = f"{base}_thought_{i}{ext}"
            img = part.as_image()
            img.save(path)
            print(f"Thought image saved: {path}")

    return count


def build_config(args):
    """Build GenerateContentConfig based on model and arguments."""
    model = args.model

    # Response modalities
    modalities = ["IMAGE"] if args.image_only else ["TEXT", "IMAGE"]

    # Build image config (aspect ratio + size)
    image_config = None
    if args.aspect_ratio or args.image_size:
        image_cfg = {}
        if args.aspect_ratio:
            # Validate aspect ratio
            if model == FLASH31_MODEL:
                valid = VALID_ASPECT_RATIOS_FLASH31
            elif model == "gemini-3-pro-image":
                valid = VALID_ASPECT_RATIOS_PRO
            else:
                valid = VALID_ASPECT_RATIOS_25FLASH
            if args.aspect_ratio not in valid:
                print(f"Error: Model {model} does not support aspect ratio '{args.aspect_ratio}'", file=sys.stderr)
                print(f"Supported ratios: {sorted(valid)}", file=sys.stderr)
                sys.exit(1)
            image_cfg["aspect_ratio"] = args.aspect_ratio

        if args.image_size:
            if model not in GEMINI3_MODELS:
                print("Warning: --image-size is only supported by gemini-3.1-flash-image and gemini-3-pro-image, ignored",
                      file=sys.stderr)
            else:
                valid_sizes = VALID_IMAGE_SIZES_FLASH31 if model == FLASH31_MODEL else VALID_IMAGE_SIZES_PRO
                if args.image_size not in valid_sizes:
                    print(f"Error: Unsupported resolution '{args.image_size}', available: {sorted(valid_sizes)}", file=sys.stderr)
                    sys.exit(1)
                image_cfg["image_size"] = args.image_size

        if image_cfg:
            image_config = types.ImageConfig(**image_cfg)

    # Build tools
    tools = []
    if args.search or args.image_search:
        if args.image_search and model != FLASH31_MODEL:
            print(f"Error: --image-search is only supported by {FLASH31_MODEL}", file=sys.stderr)
            sys.exit(1)
        if args.image_search:
            tools.append(types.Tool(google_search=types.GoogleSearch(
                search_types=types.SearchTypes(
                    web_search=types.WebSearch() if args.search else None,
                    image_search=types.ImageSearch(),
                )
            )))
        else:
            tools.append({"google_search": {}})

    # Build thinking config (only for gemini-3.1-flash-image)
    thinking_config = None
    if args.thinking or args.show_thoughts:
        if model != FLASH31_MODEL:
            print(f"Warning: thinking parameter only applies to {FLASH31_MODEL}, ignored", file=sys.stderr)
        else:
            level = args.thinking if args.thinking else "minimal"
            thinking_config = types.ThinkingConfig(
                thinking_level=level.capitalize(),
                include_thoughts=args.show_thoughts,
            )

    config_kwargs = {"response_modalities": modalities}
    if image_config:
        config_kwargs["image_config"] = image_config
    if tools:
        config_kwargs["tools"] = tools
    if thinking_config:
        config_kwargs["thinking_config"] = thinking_config

    return types.GenerateContentConfig(**config_kwargs)


def build_contents(args):
    """Build contents list from prompt and optional images/video."""
    contents = [args.prompt]

    # Add reference images
    if args.images:
        max_images = 14
        if len(args.images) > max_images:
            print(f"Error: Maximum {max_images} reference images supported, {len(args.images)} provided", file=sys.stderr)
            sys.exit(1)
        for img_path in args.images:
            contents.append(load_image(img_path))

    # Add video (only for gemini-3.1-flash-image)
    if args.video:
        if args.model != FLASH31_MODEL:
            print(f"Error: Video input is only supported by {FLASH31_MODEL}", file=sys.stderr)
            sys.exit(1)
        video_part = types.Part(
            file_data=types.FileData(file_uri=args.video),
            video_metadata=types.VideoMetadata(fps=0.5),
        )
        contents.append(video_part)

    return contents


def main():
    parser = argparse.ArgumentParser(
        description="Nano Banana Image Generation/Editing (based on Google Gemini native image generation API)"
    )

    # Core
    parser.add_argument("--prompt", required=True, help="Text prompt (describe what to generate or edit)")
    parser.add_argument(
        "--model",
        default="gemini-3.1-flash-image",
        choices=["gemini-3.1-flash-image", "gemini-3-pro-image", "gemini-2.5-flash-image"],
        help="Model ID (default: gemini-3.1-flash-image)",
    )
    parser.add_argument("--output", default="output.png", help="Output file path (default: output.png)")

    # Output control
    parser.add_argument("--image-only", action="store_true",
                        help="Return image only, no text (default: both)")
    parser.add_argument(
        "--aspect-ratio",
        help="Aspect ratio (e.g. 1:1 16:9 9:16 4:3, default: 1:1)",
    )
    parser.add_argument(
        "--image-size",
        help="Resolution (512/1K/2K/4K, only supported by gemini-3.1-flash-image and gemini-3-pro-image)",
    )

    # Input
    parser.add_argument("--images", nargs="+", metavar="FILE",
                        help="Reference image file paths (up to 14, for editing or multi-image composition)")
    parser.add_argument("--video", metavar="URL",
                        help="YouTube video URL (gemini-3.1-flash-image only)")

    # Search grounding
    parser.add_argument("--search", action="store_true",
                        help="Enable Google Web Search (real-time information generation)")
    parser.add_argument("--image-search", action="store_true",
                        help="Enable Google Image Search (gemini-3.1-flash-image only)")

    # Thinking (gemini-3.1-flash-image only)
    parser.add_argument("--thinking", choices=["minimal", "high"],
                        help="Thinking level (default: minimal, gemini-3.1-flash-image only)")
    parser.add_argument("--show-thoughts", action="store_true",
                        help="Save intermediate thought images (saved as output_thought_N.png)")

    # Proxy
    parser.add_argument("--proxy", default=None,
                        help="HTTP/HTTPS proxy address (e.g. http://127.0.0.1:7890); can also set HTTPS_PROXY in .env")

    args = parser.parse_args()

    load_dotenv()

    # Check API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set. Please configure it in .env file or environment variable:", file=sys.stderr)
        print("  GEMINI_API_KEY=your_api_key", file=sys.stderr)
        sys.exit(1)

    # Proxy: CLI argument > .env/environment variable HTTPS_PROXY > HTTP_PROXY
    proxy = args.proxy or os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    if proxy:
        os.environ.setdefault("HTTPS_PROXY", proxy)
        os.environ.setdefault("HTTP_PROXY", proxy)
        print(f"Proxy: {proxy}")

    client = genai.Client(api_key=api_key)

    contents = build_contents(args)
    config = build_config(args)

    mode = "editing" if args.images else ("video frame extraction" if args.video else "generation")
    print(f"Model: {args.model}")
    print(f"Mode: Image {mode}")
    if args.images:
        print(f"Reference images: {len(args.images)}")
    if args.search or args.image_search:
        print(f"Search: {'Web + Image Search' if args.image_search else 'Web Search'}")
    print("Generating...")

    try:
        response = client.models.generate_content(
            model=args.model,
            contents=contents,
            config=config,
        )
    except Exception as e:
        print(f"Error: API call failed - {e}", file=sys.stderr)
        sys.exit(1)

    # Print text parts
    for part in response.parts:
        if part.text is not None and not getattr(part, "thought", False):
            print(f"\n--- Model Description ---\n{part.text}")

    # Save images
    count = save_images(response.parts, args.output, args.show_thoughts)
    if count == 0:
        print("Warning: Response contains no images", file=sys.stderr)
        # Print full response for debugging
        print(f"Response content: {response}", file=sys.stderr)
        sys.exit(1)

    # Print grounding metadata if available
    if response.candidates:
        candidate = response.candidates[0]
        if hasattr(candidate, "grounding_metadata") and candidate.grounding_metadata:
            gm = candidate.grounding_metadata
            if hasattr(gm, "grounding_chunks") and gm.grounding_chunks:
                print("\n--- Search Sources ---")
                for chunk in gm.grounding_chunks[:3]:
                    if hasattr(chunk, "web") and chunk.web:
                        print(f"  {chunk.web.title}: {chunk.web.uri}")


if __name__ == "__main__":
    main()
