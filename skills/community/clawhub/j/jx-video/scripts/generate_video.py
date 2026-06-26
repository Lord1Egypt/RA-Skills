#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.28.0",
# ]
# ///
"""
Generate videos using SkillBoss API Hub (/v1/pilot).

Usage:
    uv run generate_video.py --prompt "your video description" --filename "output.mp4" [--duration 8] [--aspect-ratio 16:9]
    uv run generate_video.py --prompt "your video description" --filename "output.mp4" --input-image "/path/to/image.png" [--duration 8] [--aspect-ratio 16:9]
    uv run generate_video.py --prompt "your video description" --filename "output.mp4" -i img1.png -i img2.png -i img3.png [--duration 8] [--aspect-ratio 16:9]
"""

import argparse
import base64
import os
import sys
import requests
from pathlib import Path

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.skillbossai.com/v1"


def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=300,
    )
    return r.json()


def main():
    parser = argparse.ArgumentParser(
        description="Generate video using SkillBoss API Hub"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Video description/prompt"
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output filename (e.g., output.mp4)"
    )
    parser.add_argument(
        "--input-image", "-i",
        action="append",
        default=[],
        help="Input image file for image-to-video generation (repeatable, up to 3)"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=8,
        help="Video duration in seconds (default: 8)"
    )
    parser.add_argument(
        "--aspect-ratio", "-a",
        choices=["16:9", "9:16", "1:1"],
        default="16:9",
        help="Aspect ratio (default: 16:9)"
    )
    parser.add_argument(
        "--model", "-m",
        default=None,
        help="Model hint (optional, auto-routed via SkillBoss API Hub)"
    )

    args = parser.parse_args()

    # Set up output path
    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating video via SkillBoss API Hub...")
    print(f"  Prompt: {args.prompt}")
    print(f"  Duration: {args.duration}s")
    print(f"  Aspect ratio: {args.aspect_ratio}")
    for img in args.input_image:
        print(f"  Input image: {img}")

    # Validate input images
    if args.input_image and len(args.input_image) > 3:
        print("Error: Maximum 3 reference images allowed", file=sys.stderr)
        sys.exit(1)

    try:
        inputs = {
            "prompt": args.prompt,
            "duration": args.duration,
            "aspect_ratio": args.aspect_ratio,
        }

        # Encode reference images as base64
        if args.input_image:
            reference_images = []
            for image_path_str in args.input_image:
                image_path = Path(image_path_str)
                if not image_path.exists():
                    print(f"Error: Image file not found: {image_path}", file=sys.stderr)
                    sys.exit(1)

                print(f"Loading image: {image_path}")
                with open(image_path, "rb") as f:
                    image_b64 = base64.b64encode(f.read()).decode()

                mime = "image/png" if image_path.suffix.lower() == ".png" else "image/jpeg"
                reference_images.append({"data": image_b64, "mime_type": mime})

            inputs["reference_images"] = reference_images

        body = {"type": "video", "inputs": inputs, "prefer": "quality"}

        print("Calling SkillBoss API Hub for video generation...")
        result = pilot(body)
        video_url = result["result"]["video_url"]

        # Download the video
        print(f"Downloading video from {video_url}...")
        video_resp = requests.get(video_url, timeout=120)
        video_resp.raise_for_status()
        output_path.write_bytes(video_resp.content)

        # Verify and report
        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"\nVideo saved: {output_path} ({size_mb:.2f} MB)")
            print(f"MEDIA: {output_path}")
        else:
            print("Error: Video file was not saved.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error generating video: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
