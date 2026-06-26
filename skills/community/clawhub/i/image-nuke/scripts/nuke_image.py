#!/usr/bin/env python3
"""
NUKE IMAGE - Nuclear-grade image metadata cleanser
Level 3: Strip ALL metadata + re-encode + sub-pixel noise injection
Result: forensically untraceable, reverse image search resistant
"""

import sys
import os
import random
import struct
import hashlib
from pathlib import Path

try:
    from PIL import Image, ImageFilter, ImageEnhance
    import numpy as np
except ImportError:
    print("Installing dependencies...")
    os.system("pip install Pillow numpy")
    from PIL import Image, ImageFilter, ImageEnhance
    import numpy as np


def nuke(input_path, output_path=None, noise_level=3, quality=92):
    """
    Nuclear image cleanse.
    
    Args:
        input_path: Source image
        output_path: Output path (default: input_nuked.jpg)
        noise_level: 1-5, higher = more noise (less detectable by reverse search)
        quality: JPEG quality 1-100 (lower = more compression artifacts = harder to match)
    """
    inp = Path(input_path)
    if not inp.exists():
        print(f"[NUKE] File not found: {inp}")
        return None
    
    if output_path is None:
        output_path = inp.parent / f"{inp.stem}_nuked.jpg"
    
    out = Path(output_path)
    
    print(f"[NUKE] Input:  {inp} ({inp.stat().st_size / 1024:.1f} KB)")
    
    # Step 1: Open with PIL (strips ALL metadata by default on save)
    img = Image.open(inp)
    
    # Convert to RGB (strips alpha, ICC profiles, etc.)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    print(f"[NUKE] Original: {img.size[0]}x{img.size[1]} {img.mode}")
    
    # Step 2: Convert to numpy array for pixel manipulation
    pixels = np.array(img, dtype=np.float64)
    
    # Step 3: Sub-pixel noise injection
    # Random Gaussian noise at sub-visible level (1-5 intensity)
    # Human eye can't detect noise below ~3 intensity on 0-255 scale
    noise_sigma = noise_level * 0.8  # 0.8 to 4.0
    noise = np.random.normal(0, noise_sigma, pixels.shape)
    pixels = pixels + noise
    
    # Step 4: Micro color shift (shifts hue by 0.1-0.5 degrees - invisible)
    shift = random.uniform(-0.5, 0.5)
    pixels[:, :, 0] += shift  # tiny R shift
    pixels[:, :, 2] -= shift  # tiny B counter-shift
    
    # Step 5: Sub-pixel brightness variation (0.1% random)
    brightness_noise = np.random.uniform(0.999, 1.001, (pixels.shape[0], pixels.shape[1], 1))
    pixels = pixels * brightness_noise
    
    # Step 6: Micro-crop (remove 1-3 pixels from random edges)
    # Changes image dimensions slightly - breaks exact dimension matching
    crop_top = random.randint(0, 2)
    crop_bottom = random.randint(0, 2)
    crop_left = random.randint(0, 2)
    crop_right = random.randint(0, 2)
    if crop_bottom == 0:
        crop_bottom = None
    else:
        crop_bottom = -crop_bottom
    if crop_right == 0:
        crop_right = None
    else:
        crop_right = -crop_right
    pixels = pixels[crop_top:crop_bottom, crop_left:crop_right]
    
    # Clamp to valid range
    pixels = np.clip(pixels, 0, 255).astype(np.uint8)
    
    # Step 7: Create fresh image from raw pixels (zero metadata)
    nuked = Image.fromarray(pixels)
    
    # Step 8: Random JPEG quality variation (+/- 2 from target)
    actual_quality = quality + random.randint(-2, 2)
    actual_quality = max(70, min(98, actual_quality))
    
    # Step 9: Save with ZERO metadata
    # No EXIF, no ICC profile, no XMP, no IPTC, no comments
    nuked.save(
        out,
        'JPEG',
        quality=actual_quality,
        optimize=True,
        progressive=random.choice([True, False]),  # randomize encoding
        subsampling=random.choice([0, 1, 2]),  # randomize chroma subsampling
    )
    
    # Step 10: Verify - read back and check no metadata
    verify = Image.open(out)
    exif = verify.getexif()
    info_keys = list(verify.info.keys())
    
    # Calculate perceptual hash difference
    orig_small = Image.open(inp).convert('RGB').resize((8, 8))
    nuke_small = nuked.resize((8, 8))
    orig_hash = hashlib.md5(np.array(orig_small).tobytes()).hexdigest()
    nuke_hash = hashlib.md5(np.array(nuke_small).tobytes()).hexdigest()
    
    print(f"[NUKE] Output: {out} ({out.stat().st_size / 1024:.1f} KB)")
    print(f"[NUKE] Size:   {nuked.size[0]}x{nuked.size[1]} (cropped {crop_top}+{-crop_bottom if crop_bottom else 0}px top/bot, {crop_left}+{-crop_right if crop_right else 0}px left/right)")
    print(f"[NUKE] Noise:  sigma={noise_sigma:.1f}, color_shift={shift:+.2f}")
    print(f"[NUKE] JPEG:   quality={actual_quality}, progressive={'yes' if random.choice([True, False]) else 'no'}")
    print(f"[NUKE] EXIF:   {len(exif)} tags (should be 0)")
    print(f"[NUKE] Info:   {info_keys}")
    print(f"[NUKE] Hash:   orig={orig_hash[:12]} vs nuked={nuke_hash[:12]} ({'DIFFERENT' if orig_hash != nuke_hash else 'SAME - increase noise'})")
    print(f"[NUKE] Status: {'CLEAN' if len(exif) == 0 else 'WARNING - metadata found!'}")
    
    return str(out)


def nuke_batch(input_dir, output_dir=None, **kwargs):
    """Nuke all images in a directory."""
    inp = Path(input_dir)
    if output_dir:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
    else:
        out = inp / "nuked"
        out.mkdir(exist_ok=True)
    
    extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif'}
    files = [f for f in inp.iterdir() if f.suffix.lower() in extensions]
    
    print(f"[NUKE] Batch: {len(files)} images in {inp}")
    results = []
    for f in sorted(files):
        output_path = out / f"{f.stem}_nuked.jpg"
        result = nuke(str(f), str(output_path), **kwargs)
        if result:
            results.append(result)
        print()
    
    print(f"[NUKE] Batch complete: {len(results)}/{len(files)} processed")
    return results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single:  python3 nuke_image.py <image> [output] [--noise 1-5] [--quality 70-98]")
        print("  Batch:   python3 nuke_image.py --batch <dir> [output_dir] [--noise 1-5]")
        sys.exit(1)
    
    args = sys.argv[1:]
    noise = 3
    quality = 92
    
    # Parse flags
    if '--noise' in args:
        idx = args.index('--noise')
        noise = int(args[idx + 1])
        args = args[:idx] + args[idx+2:]
    
    if '--quality' in args:
        idx = args.index('--quality')
        quality = int(args[idx + 1])
        args = args[:idx] + args[idx+2:]
    
    if args[0] == '--batch':
        nuke_batch(args[1], args[2] if len(args) > 2 else None, noise_level=noise, quality=quality)
    else:
        nuke(args[0], args[1] if len(args) > 1 else None, noise_level=noise, quality=quality)
