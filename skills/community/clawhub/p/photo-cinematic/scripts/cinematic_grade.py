#!/usr/bin/env python3
"""
Cinematic film color grading for flower photos.
- S-curve contrast + lifted shadows + compressed highlights
- Teal/orange film grade (subtle)
- Soft glow for "通透" (transparent/airy) feel
- Subtle vignette
- Light film grain
"""

import numpy as np
from PIL import Image, ImageFilter
import sys
import os

def apply_curves(channel, points):
    """Apply a curves adjustment to a single channel.
    points: list of (input, output) tuples defining the curve."""
    x = np.arange(256, dtype=np.float32)
    y_vals = np.interp(x, [p[0]*255 for p in points], [p[1]*255 for p in points])
    return y_vals[channel]

def cinematic_grade(img_path, output_path, strength=1.0):
    print(f"📂 读取图片: {img_path}")
    img = Image.open(img_path).convert("RGB")
    arr = np.array(img, dtype=np.float32)
    h, w, _ = arr.shape
    
    print(f"📐 尺寸: {w}x{h}")
    
    # ========== 1. S-curve contrast ==========
    # Classic film S-curve: lift shadows, compress highlights, increase mid-contrast
    # Normalize to 0-1
    arr_norm = arr / 255.0
    
    # Shadows lift (bring up dark areas slightly)
    shadows_lift = 0.03 * strength
    # Highlights roll-off
    highlights_rolloff = 0.02 * strength
    
    # Apply curve: S-curve
    arr_curved = arr_norm.copy()
    
    # Increase midtone contrast
    contrast_amt = 1.15 * strength
    arr_curved = (arr_curved - 0.5) * contrast_amt + 0.5
    
    # Lift shadows
    shadow_mask = arr_curved < 0.3
    arr_curved[shadow_mask] = arr_curved[shadow_mask] + shadows_lift * (1 - arr_curved[shadow_mask] / 0.3)
    
    # Roll off highlights
    highlight_mask = arr_curved > 0.7
    arr_curved[highlight_mask] = arr_curved[highlight_mask] - highlights_rolloff * ((arr_curved[highlight_mask] - 0.7) / 0.3)
    
    # Clip
    arr_curved = np.clip(arr_curved, 0, 1)
    
    # ========== 2. Color grade - Teal/Orange film look ==========
    # Slight teal in shadows, slight warmth in highlights
    # Split toning effect
    
    # Create luminance mask
    lum = np.dot(arr_curved[...,:3], [0.299, 0.587, 0.114])
    
    # Shadow areas: add slight teal (cyan-blue)
    shadow_weight = np.clip(1.0 - lum * 2, 0, 0.12 * strength)
    arr_curved[..., 0] -= shadow_weight * 0.05   # Reduce red
    arr_curved[..., 1] += shadow_weight * 0.02   # Slight green
    arr_curved[..., 2] += shadow_weight * 0.06   # Add blue
    
    # Highlight areas: add slight warmth (orange-gold)
    highlight_weight = np.clip((lum - 0.5) * 2, 0, 0.10 * strength)
    arr_curved[..., 0] += highlight_weight * 0.04  # Add red
    arr_curved[..., 1] += highlight_weight * 0.01  # Slight green
    arr_curved[..., 2] -= highlight_weight * 0.03  # Reduce blue
    
    arr_curved = np.clip(arr_curved, 0, 1)
    
    # ========== 3. Overall exposure for "通透" feel ==========
    # Brighten midtones while preserving highlights
    exposure_boost = 1.05
    arr_curved = arr_curved * exposure_boost
    arr_curved = np.clip(arr_curved, 0, 1)
    
    # ========== 4. Soft glow/bloom on highlights ==========
    # Creates that dreamy "通透" quality
    # Create a Gaussian-filtered version for the glow
    glow_intensity = 0.08 * strength
    
    # Simple blur using PIL's GaussianBlur
    glow_arr = (arr_curved * 255).astype(np.uint8)
    glow_img = Image.fromarray(glow_arr)
    glow_blurred = np.array(glow_img.filter(ImageFilter.GaussianBlur(radius=8)), dtype=np.float32) / 255.0
    
    # Only apply glow to brighter areas
    glow_mask = np.clip(lum - 0.4, 0, 0.6) / 0.6
    glow_mask = glow_mask[..., np.newaxis]
    arr_curved = arr_curved * (1 - glow_mask * glow_intensity) + glow_blurred * (glow_mask * glow_intensity)
    arr_curved = np.clip(arr_curved, 0, 1)
    
    # ========== 5. Slight desaturation for film look ==========
    desat = 0.08 * strength
    gray = np.dot(arr_curved[...,:3], [0.299, 0.587, 0.114])
    arr_curved = arr_curved * (1 - desat) + gray[..., np.newaxis] * desat
    
    # ========== 6. Subtle vignette ==========
    # Darken corners
    center_x, center_y = w / 2, h / 2
    max_dist = np.sqrt(center_x**2 + center_y**2)
    y_grid, x_grid = np.mgrid[0:h, 0:w]
    dist = np.sqrt((x_grid - center_x)**2 + (y_grid - center_y)**2)
    vignette = 1.0 - 0.20 * strength * (dist / max_dist)**1.5
    vignette = np.clip(vignette, 0.7, 1.0)
    
    for i in range(3):
        arr_curved[..., i] *= vignette
    
    arr_curved = np.clip(arr_curved, 0, 1)
    
    # ========== 7. Subtle film grain ==========
    grain_strength = 0.015 * strength
    grain = np.random.normal(0, grain_strength, arr_curved.shape).astype(np.float32)
    arr_curved += grain
    arr_curved = np.clip(arr_curved, 0, 1)
    
    # ========== 8. Final fine-tune ==========
    # Slight sharpening for clarity
    final_arr = (arr_curved * 255).astype(np.uint8)
    final_img = Image.fromarray(final_arr)
    
    # Slight sharpening
    final_img = final_img.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))
    
    # Save with high quality
    final_img.save(output_path, quality=95, optimize=True)
    
    original_size = os.path.getsize(img_path) / 1024
    new_size = os.path.getsize(output_path) / 1024
    print(f"✅ 处理完成!")
    print(f"  输出: {output_path}")
    print(f"  原图: {original_size:.0f}KB | 处理后: {new_size:.0f}KB")
    
    return output_path

if __name__ == "__main__":
    input_path = "/vol1/@apphome/trim.openclaw/data/home/.openclaw/media/qqbot/downloads/8AED276A79DFD491644565EE273F9058_1778137034062.jpg"
    output_path = "/vol1/@apphome/trim.openclaw/data/workspace/flower_cinematic.jpg"
    
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    
    if not os.path.exists(input_path):
        print(f"❌ 文件不存在: {input_path}")
        sys.exit(1)
    
    strength = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    
    cinematic_grade(input_path, output_path, strength)
