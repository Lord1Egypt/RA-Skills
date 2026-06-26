#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "openai>=1.0.0",
#     "pillow>=10.0.0",
#     "requests>=2.28.0",
# ]
# ///
"""
Generate or edit images using OpenAI-compatible API (Nano Banana Pro style).

Supports multi-image input, fine-tuning, and custom base_url/api_key/model.
Configuration priority: args > env vars > openclaw.json > skill config.json

Usage:
    # Generate new image
    uv run generate_image.py --prompt "a cat in space" --output "cat.png" \
        --base-url "https://api.example.com" --api-key "your-key" --model "gpt-image-1"

    # Edit with single image
    uv run generate_image.py --prompt "add a hat" --input dog.png --output "dog_hat.png" \
        --base-url "https://api.example.com" --api-key "your-key"

    # Multi-image composition
    uv run generate_image.py --prompt "merge these scenes" \
        --input scene1.png --input scene2.png --output "merged.png" \
        --base-url "https://api.example.com" --api-key "your-key"

    # Fine-tune generation (use fine-tuned model)
    uv run generate_image.py --prompt "a car in my style" --output "car.png" \
        --base-url "https://api.example.com" --api-key "your-key" \
        --model "ft:image-model:my-finetuned-model"

Environment variables:
    NANO_BASE_URL - Default base URL
    NANO_API_KEY  - Default API key
    NANO_MODEL    - Default model (default: gpt-image-1)

Configuration via openclaw.json (edit ~/.openclaw/openclaw.json directly):
    {
        "skills": {
            "nano-banana-pro": {
                "baseUrl": "https://api.example.com/v1",
                "apiKey": "your-api-key",
                "model": "gpt-image-1"
            }
        }
    }

Configuration via skill config.json:
    Create ~/.openclaw/skills/nano-banana-pro/config.json:
    {
        "baseUrl": "https://api.example.com/v1",
        "apiKey": "your-api-key",
        "model": "gpt-image-1"
    }
"""

import argparse
import base64
import io
import json
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple


def load_openclaw_json_config() -> dict:
    """Load configuration from openclaw.json skills section."""
    config_path = Path.home() / ".openclaw" / "openclaw.json"

    skill_names = ["nano-banana-pro-custom", "nano-banana-pro"]

    try:
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            skills = data.get("skills", {})
            if isinstance(skills, dict):
                entries = skills.get("entries", {})
                if isinstance(entries, dict):
                    for name in skill_names:
                        skill_config = entries.get(name, {})
                        if isinstance(skill_config, dict):
                            return skill_config

                for name in skill_names:
                    skill_config = skills.get(name, {})
                    if isinstance(skill_config, dict):
                        return skill_config
    except Exception:
        pass

    return {}


def load_skill_config() -> dict:
    """Load configuration from skill's own config.json."""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.parent
    config_path = script_dir / "config.json"

    try:
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
    except Exception:
        pass

    return {}

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Look for nano-banana-pro in skills section
        skills = data.get("skills", {})
        if isinstance(skills, dict):
            # Check if there's a direct nano-banana-pro config
            skill_config = skills.get("nano-banana-pro", {})
            if isinstance(skill_config, dict):
                return skill_config
    except Exception:
        pass

    return {}


def get_config(args) -> Tuple[str, str, str]:
    """
    Get base_url, api_key, model from args or environment or openclaw.json or skill config.
    Priority: args > env vars > openclaw.json > skill config.json
    """
    # Load from different sources
    env_config = {
        "baseUrl": os.environ.get("NANO_BASE_URL", ""),
        "apiKey": os.environ.get("NANO_API_KEY", ""),
        "model": os.environ.get("NANO_MODEL", ""),
    }

    openclaw_config = load_openclaw_json_config()
    skill_config = load_skill_config()

    # Merge with priority: args > env > openclaw.json > skill config
    def get_value(key: str, arg_value: Optional[str] = None) -> str:
        if arg_value:
            return arg_value
        if env_config.get(key):
            return env_config[key]
        if openclaw_config.get(key):
            return openclaw_config[key]
        if skill_config.get(key):
            return skill_config[key]
        # Also check alternative key names
        alt_keys = {
            "baseUrl": ["base_url", "BASE_URL", "base-url"],
            "apiKey": ["api_key", "API_KEY", "api-key"],
            "model": ["MODEL"],
        }
        for alt in alt_keys.get(key, []):
            if openclaw_config.get(alt):
                return openclaw_config[alt]
            if skill_config.get(alt):
                return skill_config[alt]
        return ""

    base_url = get_value("baseUrl", args.base_url)
    api_key = get_value("apiKey", args.api_key)
    model = get_value("model", args.model) or "gpt-image-1"

    # Get paths for error messages
    openclaw_config_path = Path.home() / ".openclaw" / "openclaw.json"
    skill_dir = Path(__file__).parent.parent
    skill_config_path = skill_dir / "config.json"

    if not base_url:
        print("Error: No base_url provided.", file=sys.stderr)
        print("Please configure one of:", file=sys.stderr)
        print("  1. --base-url argument", file=sys.stderr)
        print("  2. NANO_BASE_URL environment variable", file=sys.stderr)
        print(
            f"  3. {openclaw_config_path}: skills.nano-banana-pro.baseUrl",
            file=sys.stderr,
        )
        print(f"  4. {skill_config_path}: baseUrl", file=sys.stderr)
        sys.exit(1)

    if not api_key:
        print("Error: No api_key provided.", file=sys.stderr)
        print("Please configure one of:", file=sys.stderr)
        print("  1. --api-key argument", file=sys.stderr)
        print("  2. NANO_API_KEY environment variable", file=sys.stderr)
        print(
            f"  3. {openclaw_config_path}: skills.nano-banana-pro.apiKey",
            file=sys.stderr,
        )
        print(f"  4. {skill_config_path}: apiKey", file=sys.stderr)
        sys.exit(1)

    return base_url, api_key, model


def encode_image_to_base64(image_path: str) -> str:
    """Encode image file to base64 string."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def load_images(image_paths: List[str]) -> List[Tuple[str, str]]:
    """Load images and detect format. Returns list of (format, base64_data)."""
    images = []
    for path in image_paths:
        path_obj = Path(path)
        if not path_obj.exists():
            print(f"Error: Image not found: {path}", file=sys.stderr)
            sys.exit(1)

        # Detect format from extension
        ext = path_obj.suffix.lower()
        if ext == ".png":
            fmt = "png"
        elif ext in [".jpg", ".jpeg"]:
            fmt = "jpeg"
        elif ext == ".webp":
            fmt = "webp"
        else:
            # Try to convert using PIL
            try:
                from PIL import Image

                img = Image.open(path)
                buffer = io.BytesIO()
                img.convert("RGB").save(buffer, format="PNG")
                b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
                images.append(("png", b64))
                continue
            except Exception as e:
                print(f"Error loading image '{path}': {e}", file=sys.stderr)
                sys.exit(1)

        b64 = encode_image_to_base64(path)
        images.append((fmt, b64))
        print(f"Loaded input image: {path} ({fmt})")

    return images


def main():
    parser = argparse.ArgumentParser(
        description="Generate/edit images using OpenAI-compatible API (Nano Banana Pro style)"
    )
    parser.add_argument("--prompt", "-p", help="Image description/prompt")
    parser.add_argument("--output", "-o", help="Output filename (e.g., output.png)")
    parser.add_argument(
        "--input",
        "-i",
        action="append",
        dest="input_images",
        metavar="IMAGE",
        help="Input image path(s) for editing. Can be specified multiple times.",
    )
    parser.add_argument(
        "--base-url", help="API base URL (e.g., https://api.openai.com/v1)"
    )
    parser.add_argument("--api-key", help="API key")
    parser.add_argument("--model", help="Model name (default: gpt-image-1)")
    parser.add_argument(
        "--size",
        "-s",
        choices=[
            "1024x1024",
            "1792x1024",
            "1024x1792",
            "1536x1024",
            "1024x1536",
            "auto",
        ],
        default="1024x1024",
        help="Output image size (default: 1024x1024)",
    )
    parser.add_argument(
        "--quality",
        "-q",
        choices=["low", "medium", "high", "auto"],
        default="auto",
        help="Image quality (default: auto)",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1,
        choices=range(1, 11),
        metavar="1-10",
        help="Number of images to generate (1-10, default: 1)",
    )
    parser.add_argument(
        "--response-format",
        choices=["url", "b64_json"],
        default="b64_json",
        help="Response format (default: b64_json)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Request timeout in seconds (default: 120)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Show current configuration sources and exit",
    )

    args = parser.parse_args()

    # Show config if requested
    if args.show_config:
        print("Configuration sources:")
        print()

        # Command line arguments
        print("1. Command Line Arguments:")
        print(f"   --base-url: {'[SET]' if args.base_url else '[not set]'}")
        print(f"   --api-key: {'[SET]' if args.api_key else '[not set]'}")
        print(f"   --model: {args.model or '[not set]'}")
        print()

        # Environment
        print("2. Environment Variables:")
        print(
            f"   NANO_BASE_URL: {'[SET]' if os.environ.get('NANO_BASE_URL') else '[not set]'}"
        )
        print(
            f"   NANO_API_KEY: {'[SET]' if os.environ.get('NANO_API_KEY') else '[not set]'}"
        )
        print(f"   NANO_MODEL: {os.environ.get('NANO_MODEL') or '[not set]'}")
        print()

        # openclaw.json
        print("3. openclaw.json:")
        openclaw_config = load_openclaw_json_config()
        openclaw_config_path = Path.home() / ".openclaw" / "openclaw.json"
        if openclaw_config:
            for k, v in openclaw_config.items():
                display_v = (
                    "[SET]"
                    if k in ["baseUrl", "apiKey", "base_url", "api_key"] and v
                    else v
                )
                print(f"   {k}: {display_v}")
        else:
            print(
                f"   [no skills.nano-banana-pro config found in {openclaw_config_path}]"
            )
        print()

        # skill config.json
        print("4. skill config.json:")
        skill_config = load_skill_config()
        if skill_config:
            for k, v in skill_config.items():
                display_v = (
                    "[SET]"
                    if k in ["baseUrl", "apiKey", "base_url", "api_key"] and v
                    else v
                )
                print(f"   {k}: {display_v}")
        else:
            script_dir = Path(__file__).parent.parent
            config_path = script_dir / "config.json"
            print(f"   [no config.json found at {config_path}]")
        print()

        print("Priority: args > env vars > openclaw.json > skill config.json")
        return

    # Check required arguments
    if not args.prompt:
        print("Error: --prompt/-p is required", file=sys.stderr)
        sys.exit(1)
    if not args.output:
        print("Error: --output/-o is required", file=sys.stderr)
        sys.exit(1)

    # Get configuration
    base_url, api_key, model = get_config(args)

    if args.verbose:
        print(f"Base URL: {base_url}")
        print(f"Model: {model}")
        print(f"Size: {args.size}")
        print(f"Quality: {args.quality}")

    # Import openai here to avoid slow import on early errors
    from openai import OpenAI
    from PIL import Image as PILImage

    # Initialize client
    client = OpenAI(base_url=base_url, api_key=api_key, timeout=args.timeout)

    # Prepare output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load input images if provided
    input_images = []
    if args.input_images:
        input_images = load_images(args.input_images)
        print(f"Processing {len(input_images)} input image(s)...")

    def save_image(img: PILImage.Image, save_path: Path) -> Path:
        if img.mode == "RGBA":
            rgb_img = PILImage.new("RGB", img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])
            rgb_img.save(str(save_path), "PNG")
        elif img.mode == "RGB":
            img.save(str(save_path), "PNG")
        else:
            img.convert("RGB").save(str(save_path), "PNG")
        return save_path.resolve()

    def process_b64_image(b64_json: str, idx: int) -> Path:
        img_bytes = base64.b64decode(b64_json)
        img = PILImage.open(io.BytesIO(img_bytes))
        if args.n > 1:
            save_path = (
                output_path.parent / f"{output_path.stem}_{idx + 1}{output_path.suffix}"
            )
        else:
            save_path = output_path
        return save_image(img, save_path)

    def process_url_image(url: str, idx: int) -> Path:
        import requests

        r = requests.get(url, timeout=60)
        r.raise_for_status()
        img = PILImage.open(io.BytesIO(r.content))
        if args.n > 1:
            save_path = (
                output_path.parent / f"{output_path.stem}_{idx + 1}{output_path.suffix}"
            )
        else:
            save_path = output_path
        return save_image(img, save_path)

    def extract_images_from_chat_response(response) -> list:
        images = []
        for choice in response.choices:
            if hasattr(choice, "message") and choice.message:
                msg = choice.message
                if hasattr(msg, "images") and msg.images:
                    for img in msg.images:
                        if isinstance(img, dict):
                            if "image_url" in img and "url" in img["image_url"]:
                                images.append(("data_url", img["image_url"]["url"]))
                        elif hasattr(img, "image_url") and hasattr(
                            img.image_url, "url"
                        ):
                            images.append(("data_url", img.image_url.url))
        return images

    saved_files = []
    revised_prompt = None

    try:
        if input_images:
            content = []
            for fmt, b64 in input_images:
                content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/{fmt};base64,{b64}"},
                    }
                )
            content.append({"type": "text", "text": args.prompt})

            messages = [{"role": "user", "content": content}]
            chat_params = {
                "model": model,
                "messages": messages,
                "extra_body": {"modalities": ["image", "text"]},
            }
            response = client.chat.completions.create(**chat_params)
            extracted = extract_images_from_chat_response(response)
            for idx, (img_type, img_data) in enumerate(extracted):
                if img_type == "b64_json":
                    saved_files.append(process_b64_image(img_data, idx))
                elif img_type == "url":
                    saved_files.append(process_url_image(img_data, idx))
                elif img_type == "data_url":
                    if img_data.startswith("data:image"):
                        b64_part = img_data.split(",", 1)[1]
                        saved_files.append(process_b64_image(b64_part, idx))
        else:
            messages = [{"role": "user", "content": args.prompt}]
            chat_params = {
                "model": model,
                "messages": messages,
                "extra_body": {"modalities": ["image", "text"]},
            }
            response = client.chat.completions.create(**chat_params)
            extracted = extract_images_from_chat_response(response)
            for idx, (img_type, img_data) in enumerate(extracted):
                if img_type == "b64_json":
                    saved_files.append(process_b64_image(img_data, idx))
                elif img_type == "url":
                    saved_files.append(process_url_image(img_data, idx))
                elif img_type == "data_url":
                    if img_data.startswith("data:image"):
                        b64_part = img_data.split(",", 1)[1]
                        saved_files.append(process_b64_image(b64_part, idx))
            if response.choices and hasattr(response.choices[0].message, "content"):
                content = response.choices[0].message.content
                if isinstance(content, str) and "revised_prompt" not in str(content):
                    revised_prompt = content

        for f in saved_files:
            print(f"Image saved: {f}")
            print(f"MEDIA: {f}")

        if args.verbose and revised_prompt:
            print(f"\nRevised prompt: {revised_prompt}")

    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
