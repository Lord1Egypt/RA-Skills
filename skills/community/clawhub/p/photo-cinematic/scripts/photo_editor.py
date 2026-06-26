#!/usr/bin/env python3
"""
Photo Cinematic Editor — comprehensive image processing toolkit.

Supports:
- Cinematic film color grading (S-curve, teal/orange split tone)
- Dehaze / clarity enhancement
- Light texture / atmosphere
- Saturation / vibrance adjustment
- Black/white point and levels
- Vignette, grain, glow effects
- HEIC input via pillow-heif
- Auto resize large images for performance
"""

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import os, sys, json, re

# Register HEIC
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

MAX_DIM = 3840  # Max dimension for processing

def load_image(path):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    scale = min(MAX_DIM / w, MAX_DIM / h, 1.0)
    if scale < 1:
        img = img.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
    return img

def save_image(img, path, quality=95):
    img.save(path, quality=quality, optimize=True)

def parse_params(param_str):
    """Parse 'strength=1.2 sat=0.8' style params."""
    params = {'strength': 1.0}
    if not param_str:
        return params
    for p in param_str.split():
        if '=' in p:
            k, v = p.split('=', 1)
            try:
                params[k] = float(v)
            except:
                params[k] = v
    return params

def dehaze(arr, strength=1.0):
    """Local contrast enhancement for dehazing."""
    arr = arr.astype(np.float32) / 255.0
    h, w = arr.shape[:2]
    scale = min(1.0, 2000 / max(h, w))
    small = np.array(Image.fromarray((arr*255).astype(np.uint8)).resize((int(w*scale), int(h*scale))), dtype=np.float32) / 255.0
    blur_r = max(small.shape[1], small.shape[0]) // 20
    blur_img = Image.fromarray((small*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=blur_r))
    small_blur = np.array(blur_img, dtype=np.float32) / 255.0
    blur_resized = np.array(Image.fromarray((small_blur*255).astype(np.uint8)).resize((w, h)), dtype=np.float32) / 255.0
    enhanced = arr + (arr - blur_resized) * 0.25 * strength
    enhanced = np.clip(enhanced, 0, 1)
    # Contrast boost
    enhanced = (enhanced - 0.5) * (1.10 * strength) + 0.5
    # Saturation compensation
    gray = np.dot(enhanced[..., :3], [0.299, 0.587, 0.114])[..., np.newaxis]
    enhanced = gray + (enhanced - gray) * 1.05
    return np.clip(enhanced * 255, 0, 255).astype(np.uint8)

def cinematic_grade(arr, strength=1.0):
    """Film-style color grading with S-curve + teal/orange split tone."""
    arr = arr.astype(np.float32) / 255.0
    h, w = arr.shape[:2]
    # S-curve
    arr = (arr - 0.5) * (1.12 * strength) + 0.5
    arr[arr < 0.3] += 0.04 * strength * (1 - arr[arr < 0.3] / 0.3)
    hi = arr > 0.7
    arr[hi] -= 0.03 * strength * ((arr[hi] - 0.7) / 0.3)
    arr = np.clip(arr, 0, 1)
    # Split toning
    lum = np.dot(arr[..., :3], [0.299, 0.587, 0.114])
    sw = np.clip(1.0 - lum * 2, 0, 0.10 * strength)
    arr[..., 0] -= sw * 0.04; arr[..., 1] += sw * 0.01; arr[..., 2] += sw * 0.05
    hw = np.clip((lum - 0.5) * 2, 0, 0.08 * strength)
    arr[..., 0] += hw * 0.03; arr[..., 2] -= hw * 0.02
    arr = np.clip(arr, 0, 1)
    # Exposure
    arr *= 1.03; arr = np.clip(arr, 0, 1)
    # Soft glow
    glow = 0.06 * strength
    g_arr = (arr*255).astype(np.uint8)
    g_img = Image.fromarray(g_arr).resize((w//4, h//4)).filter(ImageFilter.GaussianBlur(radius=12))
    g_blur = np.array(g_img.resize((w, h)), dtype=np.float32) / 255.0
    gm = np.clip((lum - 0.35) / 0.65, 0, 1)
    for c in range(3):
        arr[..., c] = arr[..., c] * (1 - gm*glow) + g_blur[..., c] * (gm*glow)
    # Vignette
    cx, cy = w/2, h/2; maxd = np.sqrt(cx**2 + cy**2)
    yg, xg = np.mgrid[0:h, 0:w]
    v = 1.0 - 0.15 * strength * (np.sqrt((xg-cx)**2 + (yg-cy)**2) / maxd)**1.6
    v = np.clip(v, 0.75, 1.0)
    for c in range(3): arr[..., c] *= v
    return np.clip(arr*255, 0, 255).astype(np.uint8)

def adjust_saturation(arr, saturation=1.0):
    """Adjust saturation. 1.0 = original, >1 = more saturated."""
    arr = arr.astype(np.float32) / 255.0
    gray = np.dot(arr[..., :3], [0.299, 0.587, 0.114])[..., np.newaxis]
    result = gray + (arr - gray) * saturation
    return np.clip(result*255, 0, 255).astype(np.uint8)

def adjust_vibrance(arr, vibrance=1.0):
    """Adjust vibrance (smart saturation: less saturated areas boosted more)."""
    arr = arr.astype(np.float32) / 255.0
    gray = np.dot(arr[..., :3], [0.299, 0.587, 0.114])
    # Per-pixel saturation
    sat = np.max(arr, axis=2) - np.min(arr, axis=2)
    # Boost less saturated pixels more
    weight = (1.0 - sat) * (vibrance - 1.0) * 0.5 + 1.0
    weight = np.clip(weight, 0, 2)[..., np.newaxis]
    result = gray[..., np.newaxis] + (arr - gray[..., np.newaxis]) * weight
    return np.clip(result*255, 0, 255).astype(np.uint8)

def adjust_levels(arr, shadows=0, midtones=1.0, highlights=255):
    """Adjust black/white/gamma levels like Photoshop levels tool."""
    arr = arr.astype(np.float32)
    # Input levels
    arr = (arr - shadows) / (highlights - shadows) * 255
    arr = np.clip(arr, 0, 255)
    # Gamma (midtones)
    if midtones != 1.0:
        arr = (arr / 255.0) ** (1.0 / midtones) * 255
    return np.clip(arr, 0, 255).astype(np.uint8)

def add_light_texture(arr, strength=1.0):
    """Add warm light streaks from corner for atmospheric quality."""
    arr = arr.astype(np.float32) / 255.0
    h, w = arr.shape[:2]
    yg, xg = np.mgrid[0:h, 0:w]
    ls = np.clip(1.0 - np.sqrt((xg-w*0.1)**2 + (yg-h*0.15)**2) / (max(h,w)*0.6), 0, 1)**3 * 0.06 * strength
    arr[..., 0] += ls * 0.03; arr[..., 1] += ls * 0.01; arr[..., 2] -= ls * 0.02
    lum = np.dot(arr[..., :3], [0.299, 0.587, 0.114])
    bm = lum > 0.6
    boost = np.clip((lum[bm]-0.6)/0.4, 0, 1) * 0.04 * strength
    for c in range(3): arr[bm, c] += boost
    return np.clip(arr*255, 0, 255).astype(np.uint8)

def process(input_path, output_path, effects, strength=1.0):
    """Apply a pipeline of effects to an image.
    effects: list of strings like ['dehaze', 'grade', 'saturation=1.2']
    """
    img = load_image(input_path)
    arr = np.array(img, dtype=np.uint8)
    h, w = arr.shape[:2]
    print(f"Loaded: {w}x{h}")

    for effect in effects:
        name = effect.split('=')[0]
        params = parse_params(effect)
        s = params.get('strength', strength)
        print(f"  → {effect}")

        if name == 'dehaze':
            arr = dehaze(arr, s)
        elif name == 'grade':
            arr = cinematic_grade(arr, s)
        elif name == 'saturation':
            arr = adjust_saturation(arr, params.get('saturation', s))
        elif name == 'vibrance':
            arr = adjust_vibrance(arr, params.get('vibrance', s))
        elif name == 'levels':
            arr = adjust_levels(arr,
                params.get('shadows', 0),
                params.get('midtones', 1.0),
                params.get('highlights', 255))
        elif name == 'light':
            arr = add_light_texture(arr, s)
        elif name == 'sharpen':
            img = Image.fromarray(arr)
            img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=int(20*s), threshold=3))
            arr = np.array(img, dtype=np.uint8)
        elif name == 'blur':
            arr = np.array(Image.fromarray(arr).filter(ImageFilter.GaussianBlur(radius=int(s))), dtype=np.uint8)

    final = Image.fromarray(arr)
    save_image(final, output_path)
    print(f"Saved: {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: photo_editor.py <input> <output> <effects...>")
        print("  effects: dehaze, grade, saturation=1.2, vibrance=0.8, light, sharpen, levels shadows=10 midtones=1.1, blur=2")
        sys.exit(1)

    inp = sys.argv[1]
    out = sys.argv[2]
    effects = sys.argv[3:] if len(sys.argv) > 3 else ['dehaze', 'grade', 'light', 'sharpen']
    process(inp, out, effects)
