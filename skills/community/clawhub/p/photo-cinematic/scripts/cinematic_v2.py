#!/usr/bin/env python3
"""
Cinematic dehaze + light enhancement for flower photos.
- Dehaze via local contrast enhancement + clarity
- Cinematic film color grading
- Light/glow enhancement for "通透" feel
- Handles HEIC input
"""

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import os
import sys

# Register HEIC support
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

def dehaze_clarity(img_arr, strength=1.0):
    """Simple dehaze via local contrast enhancement and clarity boost."""
    # Convert to float
    arr = img_arr.astype(np.float32) / 255.0
    
    # Create a blurred version (large radius) for local contrast
    h, w = arr.shape[:2]
    # Downscale then upscale for performance on large images
    scale = min(1.0, 2000 / max(h, w))
    small_h, small_w = int(h * scale), int(w * scale)
    
    small = np.array(Image.fromarray((arr * 255).astype(np.uint8)).resize((small_w, small_h)), dtype=np.float32) / 255.0
    
    # Gaussian blur approximation via repeated box blurs
    blur_radius = max(small_w, small_h) // 20
    # Use PIL for blur
    blur_img = Image.fromarray((small * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=blur_radius))
    small_blur = np.array(blur_img, dtype=np.float32) / 255.0
    
    # Resize blur back to original
    blur_resized = np.array(Image.fromarray((small_blur * 255).astype(np.uint8)).resize((w, h)), dtype=np.float32) / 255.0
    
    # Local contrast enhancement (unsharp mask in Lab-like space)
    dehaze_strength = 0.25 * strength
    # Enhance local contrast: detail = original - blur
    detail = arr - blur_resized
    # Boost detail
    enhanced = arr + detail * dehaze_strength
    
    # Global contrast enhancement for dehaze effect
    # Stretch histogram in midtones
    enhanced = np.clip(enhanced, 0, 1)
    
    # S-curve for additional contrast and haze removal
    midtone_contrast = 1.10 * strength
    enhanced = (enhanced - 0.5) * midtone_contrast + 0.5
    enhanced = np.clip(enhanced, 0, 1)
    
    # Slight increase in saturation to compensate
    gray = np.dot(enhanced[..., :3], [0.299, 0.587, 0.114])[..., np.newaxis]
    sat_boost = 1.05
    enhanced = gray + (enhanced - gray) * sat_boost
    
    return np.clip(enhanced * 255, 0, 255).astype(np.uint8)

def cinematic_grade(img_arr, strength=1.0):
    """Apply cinematic film color grading."""
    arr = img_arr.astype(np.float32) / 255.0
    h, w = arr.shape[:2]
    
    # S-curve contrast
    arr_curved = arr.copy()
    contrast_amt = 1.12 * strength
    arr_curved = (arr_curved - 0.5) * contrast_amt + 0.5
    
    # Lift shadows slightly
    shadow_mask = arr_curved < 0.3
    shadows_lift = 0.04 * strength
    arr_curved[shadow_mask] = arr_curved[shadow_mask] + shadows_lift * (1 - arr_curved[shadow_mask] / 0.3)
    
    # Roll off highlights
    highlight_mask = arr_curved > 0.7
    hi_rolloff = 0.03 * strength
    arr_curved[highlight_mask] = arr_curved[highlight_mask] - hi_rolloff * ((arr_curved[highlight_mask] - 0.7) / 0.3)
    
    arr_curved = np.clip(arr_curved, 0, 1)
    
    # Split toning - teal shadows, warm highlights
    lum = np.dot(arr_curved[..., :3], [0.299, 0.587, 0.114])
    
    # Shadow teal
    shadow_w = np.clip(1.0 - lum * 2, 0, 0.10 * strength)
    arr_curved[..., 0] -= shadow_w * 0.04
    arr_curved[..., 1] += shadow_w * 0.01
    arr_curved[..., 2] += shadow_w * 0.05
    
    # Highlight warmth
    hi_w = np.clip((lum - 0.5) * 2, 0, 0.08 * strength)
    arr_curved[..., 0] += hi_w * 0.03
    arr_curved[..., 2] -= hi_w * 0.02
    
    arr_curved = np.clip(arr_curved, 0, 1)
    
    # Exposure boost for "通透"
    arr_curved *= 1.03
    arr_curved = np.clip(arr_curved, 0, 1)
    
    # Soft glow on highlights
    glow_intensity = 0.06 * strength
    glow_arr = (arr_curved * 255).astype(np.uint8)
    glow_img = Image.fromarray(glow_arr)
    # Use smaller blur for performance
    small_h, small_w = h // 4, w // 4
    glow_small = glow_img.resize((small_w, small_h)).filter(ImageFilter.GaussianBlur(radius=12))
    glow_blurred = np.array(glow_small.resize((w, h)), dtype=np.float32) / 255.0
    
    glow_mask = np.clip(lum - 0.35, 0, 0.65) / 0.65
    for c in range(3):
        arr_curved[..., c] = arr_curved[..., c] * (1 - glow_mask * glow_intensity) + glow_blurred[..., c] * (glow_mask * glow_intensity)
    
    arr_curved = np.clip(arr_curved, 0, 1)
    
    # Slight vignette
    cx, cy = w / 2, h / 2
    max_dist = np.sqrt(cx**2 + cy**2)
    yg, xg = np.mgrid[0:h, 0:w]
    dist = np.sqrt((xg - cx)**2 + (yg - cy)**2)
    vignette = 1.0 - 0.15 * strength * (dist / max_dist)**1.6
    vignette = np.clip(vignette, 0.75, 1.0)
    for c in range(3):
        arr_curved[..., c] *= vignette
    
    return np.clip(arr_curved * 255, 0, 255).astype(np.uint8)

def add_light_texture(img_arr, strength=1.0):
    """Add light rays/texture for cinematic quality."""
    arr = img_arr.astype(np.float32) / 255.0
    h, w = arr.shape[:2]
    
    # Create subtle light streaks from corner
    lum = np.dot(arr[..., :3], [0.299, 0.587, 0.114])
    
    # Subtle warm light overlay from top-left
    yg, xg = np.mgrid[0:h, 0:w]
    light_angle = np.arctan2(yg - h * 0.3, xg - w * 0.2)
    # Only light areas
    light_streak = np.clip(1.0 - np.sqrt((xg - w*0.1)**2 + (yg - h*0.15)**2) / (max(h, w) * 0.6), 0, 1)
    light_streak = light_streak ** 3 * 0.06 * strength
    
    # Apply golden warmth to light areas
    for c in range(3):
        warmth = [0.03, 0.01, -0.02][c]  # warm cast
        arr[..., c] += light_streak * warmth
    
    # Slight boost to highlights for light texture feel
    bright_mask = lum > 0.6
    boost = np.clip((lum[bright_mask] - 0.6) / 0.4, 0, 1) * 0.04 * strength
    for c in range(3):
        arr[bright_mask, c] += boost
    
    return np.clip(arr * 255, 0, 255).astype(np.uint8)

def process_image(input_path, output_path, strength=1.0):
    print(f"📂 读取: {input_path}")
    img = Image.open(input_path).convert("RGB")
    arr = np.array(img, dtype=np.uint8)
    h, w = arr.shape[:2]
    size_mb = os.path.getsize(input_path) / 1024 / 1024
    print(f"📐 尺寸: {w}x{h} ({size_mb:.1f}MB)")
    
    print("1️⃣  去雾处理...")
    dehazed = dehaze_clarity(arr, strength)
    
    print("2️⃣  电影调色...")
    graded = cinematic_grade(dehazed, strength)
    
    print("3️⃣  光线质感增强...")
    final = add_light_texture(graded, strength)
    
    # Final sharpening
    final_img = Image.fromarray(final)
    final_img = final_img.filter(ImageFilter.UnsharpMask(radius=2, percent=20, threshold=3))
    
    # Save as JPEG with high quality
    output_jpg = output_path
    final_img.save(output_jpg, quality=95, optimize=True)
    
    new_size = os.path.getsize(output_jpg) / 1024 / 1024
    print(f"\n✅ 完成! {new_size:.1f}MB -> {output_jpg}")

if __name__ == "__main__":
    default_input = "/vol1/@apphome/trim.openclaw/data/home/.openclaw/media/qqbot/downloads/IMG20260503100028_1778138441669.heic"
    default_output = "/vol1/@apphome/trim.openclaw/data/workspace/flower_cinematic_v2.jpg"
    
    inp = sys.argv[1] if len(sys.argv) > 1 else default_input
    out = sys.argv[2] if len(sys.argv) > 2 else default_output
    st = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    
    if not os.path.exists(inp):
        print(f"❌ 文件不存在: {inp}")
        sys.exit(1)
    
    process_image(inp, out, st)
