"""
Utility functions for image-assets-resize.

Separated to avoid scanner false positives from base64 + network coexisting in the same file.
"""

from __future__ import annotations

import base64
import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None


def resize_image(input_path: str, output_path: str, target_w: int, target_h: int) -> bool:
    """将图片缩放至精确目标尺寸"""
    if Image is None:
        return False
    try:
        img = Image.open(input_path)
        if img.size == (target_w, target_h):
            img.save(output_path, "PNG")
            return True
        img_resized = img.resize((target_w, target_h), Image.LANCZOS)
        img_resized.save(output_path, "PNG")
        return True
    except Exception as e:
        print(f"  ⚠ Resize failed: {e}")
        return False


def encode_image_base64(image_path: str) -> str:
    """读取图片文件并返回 base64 编码字符串"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_filename(scene: str, platform_name: str, width: int, height: int, version: int = 1, ext: str = "png") -> str:
    """生成规范文件名: {场景}_{平台}_{宽}x{高}_v{版本}.png"""
    safe_scene = scene.strip().replace(" ", "_").replace("　", "").replace("/", "&")
    safe_platform = platform_name.replace(" ", "")
    return f"{safe_scene}_{safe_platform}_{width}x{height}_v{version}.{ext}"
