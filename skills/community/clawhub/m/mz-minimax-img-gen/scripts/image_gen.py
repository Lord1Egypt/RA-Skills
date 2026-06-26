#!/usr/bin/env python3
"""
MiniMax Image-01 Generator
Supports both Global and China API endpoints.

Usage:
    python image_gen.py "prompt" --aspect 16:9 --n 1 --region cn
    python image_gen.py "prompt" --region global

Region options:
    --region cn     -> api.minimax.chat (China/MiniMax CN)
    --region global -> api.minimax.io (International)
    If not specified, prompts user to choose.
"""
import os
import sys
import json
import base64
import argparse
import requests

# API endpoints by region
ENDPOINTS = {
    "global": "https://api.minimax.io/v1/image_generation",
    "cn": "https://api.minimax.chat/v1/image_generation",
}

DEFAULT_ENHANCEMENT_PREFIX = (
    "Masterful, highly detailed digital art. "
    "Professional quality, cinematic lighting, "
    "intricate details, sharp focus, 4K resolution. "
)


def enhance_prompt(prompt: str) -> str:
    """Enhance short prompts with professional parameters."""
    if len(prompt.split()) < 8:
        return DEFAULT_ENHANCEMENT_PREFIX + prompt
    return prompt


def get_api_key_and_url(region: str):
    """Get API key and URL. Region must be specified."""
    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        raise RuntimeError(
            "MINIMAX_API_KEY environment variable not set.\n"
            "  macOS/Linux: export MINIMAX_API_KEY=your_key\n"
            "  Windows:     set MINIMAX_API_KEY=your_key (run in same terminal)"
        )
    url = ENDPOINTS.get(region)
    if not url:
        raise ValueError(f"Unknown region: {region}. Use 'global' or 'cn'.")
    return api_key, url


def generate_image(
    prompt: str,
    aspect_ratio: str = "16:9",
    n: int = 1,
    enhance: bool = True,
    region: str = None,
    output_dir: str = ".",
) -> list[str]:
    """Generate image(s) using MiniMax image-01."""
    if region is None:
        print("ERROR: --region is required. Use --region cn or --region global", file=sys.stderr)
        print("  cn     = China endpoint (api.minimax.chat)", file=sys.stderr)
        print("  global = International endpoint (api.minimax.io)", file=sys.stderr)
        sys.exit(1)

    api_key, url = get_api_key_and_url(region)
    final_prompt = enhance_prompt(prompt) if enhance else prompt

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "image-01",
        "prompt": final_prompt,
        "aspect_ratio": aspect_ratio,
        "n": min(n, 9),
        "response_format": "base64",
    }

    print(f"[minimax-image-gen] Region: {region}", file=sys.stderr)
    print(f"[minimax-image-gen] Generating {n} image(s) ({aspect_ratio})...", file=sys.stderr)
    if enhance:
        print(f"[minimax-image-gen] Prompt enhanced: {final_prompt[:60]}...", file=sys.stderr)

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()

    # Check for API errors
    if data.get("base_resp") and data["base_resp"].get("status_code") != 0:
        err = data["base_resp"]
        raise RuntimeError(f"API error {err['status_code']}: {err['status_msg']}")

    images_base64 = data["data"]["image_base64"]

    os.makedirs(output_dir, exist_ok=True)
    output_paths = []
    for i, img_b64 in enumerate(images_base64):
        img_bytes = base64.b64decode(img_b64)
        output_path = os.path.join(output_dir, f"minimax_gen_{i+1}.png")
        with open(output_path, "wb") as f:
            f.write(img_bytes)
        output_paths.append(output_path)
        print(f"[minimax-image-gen] Saved: {output_path} ({len(img_bytes)//1024}KB)", file=sys.stderr)

    return output_paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="MiniMax Image-01 Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Region (--region) is REQUIRED:
  cn     -> China endpoint (api.minimax.chat)
  global -> International endpoint (api.minimax.io)

Examples:
  python image_gen.py "a red sports car" --region cn --aspect 16:9
  python image_gen.py "cyberpunk city" --region global --n 4 --aspect 1:1
  python image_gen.py "simple circle" --region cn --no-enhance
        """
    )
    parser.add_argument("prompt", help="Image description / prompt")
    parser.add_argument("--aspect", "-a", default="16:9",
                        help="Aspect ratio: 16:9, 1:1, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9")
    parser.add_argument("--n", type=int, default=1,
                        help="Number of images (1-9)")
    parser.add_argument("--no-enhance", action="store_true",
                        help="Disable prompt enhancement")
    parser.add_argument("--region", "-r", required=True,
                        choices=["cn", "global"],
                        help="API region: cn (China) or global (International)")
    parser.add_argument("--output", "-o", default=".",
                        help="Output directory")
    args = parser.parse_args()

    try:
        paths = generate_image(
            prompt=args.prompt,
            aspect_ratio=args.aspect,
            n=args.n,
            enhance=not args.no_enhance,
            region=args.region,
            output_dir=args.output,
        )
        print("OUTPUT_PATHS:" + ",".join(paths))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
