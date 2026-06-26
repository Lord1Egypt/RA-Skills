#!/usr/bin/env python3
"""
图片压缩工具
当图片大小超过指定阈值时，自动压缩图片
"""

import os
import sys
from PIL import Image

def compress_image(input_path, output_path, max_size_mb=1, quality=85):
    """
    压缩图片到指定大小以下

    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        max_size_mb: 最大文件大小（MB）
        quality: 初始压缩质量 (1-100)

    Returns:
        tuple: (输出路径, 原始大小KB, 压缩后大小KB, 是否压缩)
    """
    max_size_bytes = max_size_mb * 1024 * 1024

    # 获取原始文件大小
    original_size = os.path.getsize(input_path)
    original_size_kb = original_size / 1024

    # 如果文件已经小于阈值，直接复制
    if original_size <= max_size_bytes:
        if input_path != output_path:
            import shutil
            shutil.copy(input_path, output_path)
        return (output_path, original_size_kb, original_size_kb, False)

    # 打开图片
    img = Image.open(input_path)

    # 转换为 RGB（如果需要）
    if img.mode in ('RGBA', 'P'):
        # 保留透明度，使用 PNG
        img = img.convert('RGBA')
        format = 'PNG'
    else:
        img = img.convert('RGB')
        format = 'JPEG'

    # 逐步降低质量直到满足大小要求
    current_quality = quality
    while current_quality >= 10:
        # 尝试保存
        img.save(output_path, format=format, quality=current_quality, optimize=True)

        # 检查大小
        compressed_size = os.path.getsize(output_path)
        compressed_size_kb = compressed_size / 1024

        if compressed_size <= max_size_bytes:
            return (output_path, original_size_kb, compressed_size_kb, True)

        # 降低质量继续尝试
        current_quality -= 5

    # 如果质量降到最低仍然太大，尝试缩小尺寸
    scale = 0.9
    while scale >= 0.3:
        new_width = int(img.width * scale)
        new_height = int(img.height * scale)
        resized = img.resize((new_width, new_height), Image.LANCZOS)

        resized.save(output_path, format=format, quality=75, optimize=True)
        compressed_size = os.path.getsize(output_path)
        compressed_size_kb = compressed_size / 1024

        if compressed_size <= max_size_bytes:
            return (output_path, original_size_kb, compressed_size_kb, True)

        scale -= 0.1

    # 最后一次保存（即使超过限制）
    img.save(output_path, format=format, quality=10, optimize=True)
    final_size = os.path.getsize(output_path)
    return (output_path, original_size_kb, final_size / 1024, True)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 compress_image.py <input_image> [output_image] [max_size_mb]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path
    max_size_mb = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

    if not os.path.exists(input_path):
        print(f"错误: 文件不存在 - {input_path}")
        sys.exit(1)

    result = compress_image(input_path, output_path, max_size_mb)
    output, original_kb, compressed_kb, was_compressed = result

    if was_compressed:
        print(f"✅ 已压缩: {original_kb:.1f}KB → {compressed_kb:.1f}KB")
    else:
        print(f"ℹ️ 无需压缩: {original_kb:.1f}KB")

    print(f"输出: {output}")


if __name__ == "__main__":
    main()
