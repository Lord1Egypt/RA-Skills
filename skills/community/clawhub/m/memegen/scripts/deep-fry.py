#!/usr/bin/env python3
"""
Deep Fry an image — the visual equivalent of turning everything up to 11.

Usage:
    python3 deep-fry.py input.png output.png [--level 1-5] [--emojis] [--flare]

Requires: pip install pillow
"""

import argparse
import io
import os
import random
import sys

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
except ImportError:
    print("Error: Pillow is required. Install with: pip install pillow", file=sys.stderr)
    sys.exit(1)


def add_lens_flare(img, count=1):
    """Add fake lens flare effect(s) to the image."""
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size

    for _ in range(count):
        cx = random.randint(int(w * 0.1), int(w * 0.9))
        cy = random.randint(int(h * 0.1), int(h * 0.9))

        # Outer glow
        for radius in range(60, 5, -5):
            alpha = max(10, 80 - radius)
            draw.ellipse(
                [cx - radius, cy - radius, cx + radius, cy + radius],
                fill=(255, 255, 255, alpha),
            )

        # Hot center
        for radius in range(15, 0, -1):
            alpha = min(255, 150 + (15 - radius) * 7)
            draw.ellipse(
                [cx - radius, cy - radius, cx + radius, cy + radius],
                fill=(255, 255, 200, alpha),
            )

        # Streak lines
        for angle_offset in range(0, 360, 45):
            import math

            length = random.randint(40, 100)
            rad = math.radians(angle_offset + random.randint(-10, 10))
            ex = cx + int(length * math.cos(rad))
            ey = cy + int(length * math.sin(rad))
            draw.line([(cx, cy), (ex, ey)], fill=(255, 255, 255, 60), width=2)

    return img


def add_emoji_overlay(img, count=5):
    """Add random emoji text overlays to the image."""
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    emojis = ["😂", "💯", "🔥", "💀", "😤", "🅱️", "👌", "😩", "⚡", "🤣"]

    # Try to get a font that supports emoji, fall back to default
    font_size = max(w // 10, 30)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", font_size)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except (OSError, IOError):
            font = ImageFont.load_default()

    for _ in range(count):
        emoji = random.choice(emojis)
        x = random.randint(0, max(1, w - font_size))
        y = random.randint(0, max(1, h - font_size))
        # Semi-transparent
        draw.text((x, y), emoji, font=font, fill=(255, 255, 255, 200))

    return img


def deep_fry(img_path, output_path, level=3, emojis=False, flare=False):
    """
    Apply deep fry effect to an image.

    Args:
        img_path: Input image path
        output_path: Output image path
        level: 1-5 intensity
            1 = lightly toasted (subtle saturation + contrast boost)
            2 = golden brown (noticeable but not extreme)
            3 = crispy (standard deep fry — the classic)
            4 = extra crispy (heavy artifacts, red tint)
            5 = charcoal (nuclear — barely recognizable)
        emojis: Add random emoji overlays
        flare: Add lens flare effect
    """
    img = Image.open(img_path).convert("RGBA" if (emojis or flare) else "RGB")

    # --- Saturation boost (the soul of deep frying) ---
    saturation = 1.5 + (level * 0.5)  # 2.0 → 4.0
    img_rgb = img.convert("RGB")
    img_rgb = ImageEnhance.Color(img_rgb).enhance(saturation)

    # --- Contrast boost ---
    contrast = 1.2 + (level * 0.3)  # 1.5 → 2.7
    img_rgb = ImageEnhance.Contrast(img_rgb).enhance(contrast)

    # --- Sharpness (makes it crunchy) ---
    sharpness = 1.0 + (level * 0.8)  # 1.8 → 5.0
    img_rgb = ImageEnhance.Sharpness(img_rgb).enhance(sharpness)

    # --- Brightness bump (slight overexposure) ---
    brightness = 1.0 + (level * 0.05)  # 1.05 → 1.25
    img_rgb = ImageEnhance.Brightness(img_rgb).enhance(brightness)

    # --- Red/orange tint ---
    overlay = Image.new("RGB", img_rgb.size, (255, 60 + level * 15, 0))
    blend_alpha = 0.05 + level * 0.03  # 0.08 → 0.20
    img_rgb = Image.blend(img_rgb, overlay, blend_alpha)

    # --- Edge enhancement at higher levels ---
    if level >= 3:
        for _ in range(level - 2):
            img_rgb = img_rgb.filter(ImageFilter.EDGE_ENHANCE_MORE)

    # --- JPEG artifact pass (the crunch) ---
    num_passes = max(1, level - 1)  # 1 → 4 passes
    for i in range(num_passes):
        buffer = io.BytesIO()
        quality = max(2, 25 - level * 4 - i * 3)
        img_rgb.save(buffer, format="JPEG", quality=quality)
        buffer.seek(0)
        img_rgb = Image.open(buffer).convert("RGB")

    # --- Noise at level 4+ ---
    if level >= 4:
        import numpy as np

        try:
            arr = np.array(img_rgb, dtype=np.int16)
            noise_amount = (level - 3) * 15  # 15 → 30
            noise = np.random.randint(-noise_amount, noise_amount + 1, arr.shape, dtype=np.int16)
            arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
            img_rgb = Image.fromarray(arr)
        except ImportError:
            pass  # numpy not available, skip noise

    # Convert back for overlay effects
    if emojis or flare:
        img_final = img_rgb.convert("RGBA")
        if flare:
            flare_count = max(1, level // 2)
            img_final = add_lens_flare(img_final, count=flare_count)
        if emojis:
            emoji_count = level * 2 + 1  # 3 → 11
            img_final = add_emoji_overlay(img_final, count=emoji_count)
        # Save as PNG to preserve alpha, or convert to RGB for JPEG
        if output_path.lower().endswith((".jpg", ".jpeg")):
            img_final = img_final.convert("RGB")
    else:
        img_final = img_rgb

    # Determine output format
    ext = os.path.splitext(output_path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        img_final.save(output_path, format="JPEG", quality=95)
    else:
        if img_final.mode == "RGBA":
            img_final.save(output_path, format="PNG")
        else:
            img_final.save(output_path, format="PNG")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="🔥 Deep Fry an image — turn it into crispy, oversaturated, JPEG-artifacted glory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.png output.png                    # Default level 3
  %(prog)s input.png fried.png --level 5            # Nuclear fry
  %(prog)s meme.png fried.png --level 4 --emojis    # With emoji spam
  %(prog)s meme.png fried.png --level 3 --flare     # With lens flare
  %(prog)s meme.png glory.png -l 5 --emojis --flare # The full treatment
        """,
    )
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument(
        "-l",
        "--level",
        type=int,
        default=3,
        choices=range(1, 6),
        help="Fry intensity: 1=toasted, 3=crispy (default), 5=charcoal",
    )
    parser.add_argument(
        "--emojis",
        action="store_true",
        help="Add random 😂💯🔥 emoji overlays",
    )
    parser.add_argument(
        "--flare",
        action="store_true",
        help="Add lens flare effect(s)",
    )

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    result = deep_fry(args.input, args.output, level=args.level, emojis=args.emojis, flare=args.flare)
    print(f"🔥 Deep fried (level {args.level}) → {result}")


if __name__ == "__main__":
    main()
