#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate images using OpenRouter and return the image path for OpenClaw to send to user.

Usage:
    uv run generate_and_return.py --prompt "your image description" [--resolution 1K|2K|4K]

This wrapper script:
1. Generates the image using generate_image.py
2. Saves to output_images/ directory
3. Prints the full path for OpenClaw to return to user
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def generate_filename(prompt: str) -> str:
    """Generate filename from timestamp and prompt."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # Clean prompt for filename (first 3-4 words)
    words = prompt.replace(",", " ").replace(".", " ").split()[:4]
    name = "-".join(words).lower()
    # Remove special characters
    name = "".join(c for c in name if c.isalnum() or c == "-").strip("-")
    if not name:
        name = "generated"
    return f"{timestamp}-{name}.png"


def main():
    parser = argparse.ArgumentParser(
        description="Generate images and return path for OpenClaw"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description/prompt"
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

    args = parser.parse_args()

    # Get script directory
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    output_dir = skill_dir / "output_images"
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    filename = generate_filename(args.prompt)
    output_path = output_dir / filename

    # Build command
    cmd = [
        "uv", "run", str(script_dir / "generate_image.py"),
        "--prompt", args.prompt,
        "--filename", filename,
        "--resolution", args.resolution,
    ]

    if args.input_image:
        cmd.extend(["--input-image", args.input_image])
    
    if args.api_key:
        cmd.extend(["--api-key", args.api_key])

    # Run generation
    try:
        result = subprocess.run(
            cmd,
            cwd=str(skill_dir),
            capture_output=True,
            text=True,
            check=True
        )
        
        # Print the output for debugging
        if result.stdout:
            print(result.stdout)
        
        # Check if file was created
        if output_path.exists():
            print(f"\n✅ Image generated successfully!")
            print(f"📁 Saved to: {output_path}")
            # Print the path in a format OpenClaw can capture
            print(f"OPENCLAW_IMAGE_PATH:{output_path}")
            # Print send command for OpenClaw to use
            print(f"\n💡 To send this image to the user, use:")
            print(f'SEND_IMAGE:{output_path}')
            return 0
        else:
            print("Error: Image file was not created.", file=sys.stderr)
            return 1
            
    except subprocess.CalledProcessError as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
