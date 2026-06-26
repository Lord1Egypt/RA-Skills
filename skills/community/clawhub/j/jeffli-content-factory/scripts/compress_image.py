#!/usr/bin/env python3
"""
Compress images for WeChat Official Account upload.

WeChat has a 10MB limit but large files often timeout during upload.
This script compresses images to < 1MB while maintaining good visual quality.

Usage:
    python compress_image.py <input_image> [output_image] [quality]

Examples:
    # Compress with default settings (quality=85)
    python compress_image.py infographic.png

    # Compress with custom quality
    python compress_image.py infographic.png output.jpg 75

    # Compress and specify output path
    python compress_image.py infographic.png compressed.jpg
"""

from PIL import Image
import sys
import os


def compress_for_wechat(input_path, output_path=None, quality=85):
    """
    Compress image for WeChat upload (target < 1MB).

    Args:
        input_path: Path to input image (PNG, JPEG, etc.)
        output_path: Path to output JPEG (default: input_path-compressed.jpg)
        quality: JPEG quality 1-100 (default: 85)

    Returns:
        Path to compressed output file
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}-compressed.jpg"

    # Open and convert image
    img = Image.open(input_path)

    # Convert RGBA/LA/P to RGB for JPEG compatibility
    if img.mode in ('RGBA', 'LA', 'P'):
        # Create white background for transparency
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background

    # Save as optimized JPEG
    img.save(output_path, 'JPEG', quality=quality, optimize=True)

    # Report compression results
    original_mb = os.path.getsize(input_path) / 1024 / 1024
    compressed_mb = os.path.getsize(output_path) / 1024 / 1024
    reduction_pct = 100 * (1 - compressed_mb / original_mb)

    print(f"Original: {original_mb:.2f}MB")
    print(f"Compressed: {compressed_mb:.2f}MB ({reduction_pct:.1f}% reduction)")
    print(f"Output: {output_path}")

    # Warn if still too large
    if compressed_mb > 1.0:
        print(f"\n⚠️  Warning: Compressed file is {compressed_mb:.2f}MB (> 1MB)")
        print(f"   Consider reducing quality or resizing:")
        print(f"   python compress_image.py {input_path} {output_path} 75")

    return output_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    quality = int(sys.argv[3]) if len(sys.argv) > 3 else 85

    try:
        compress_for_wechat(input_path, output_path, quality)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
