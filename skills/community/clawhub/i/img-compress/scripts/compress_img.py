#!/usr/bin/env python3
"""
图片批量压缩脚本
用法: python3 compress_img.py [目录路径] [目标大小KB]
默认: 压缩 /www/wwwroot/lovehibachi_demo/public/static/img 下超过100KB的图片，目标是80KB
"""
import os
import sys
from PIL import Image
from pathlib import Path

TARGET_SIZE_KB = 80  # 目标文件大小

def get_file_size_kb(path):
    return os.path.getsize(path) / 1024

def compress_image(src_path, target_size_kb=80):
    """压缩单张图片，返回压缩后大小"""
    img = Image.open(src_path)
    
    # 保存为同名文件（覆盖原文件）
    # 先尝试高压缩率
    if img.mode == 'RGBA':
        img.save(src_path, 'PNG', optimize=True)
    else:
        # 逐步降低质量直到达到目标大小
        quality = 85
        min_quality = 50
        
        img.save(src_path, 'JPEG', quality=quality, optimize=True)
        
        while get_file_size_kb(src_path) > target_size_kb and quality > min_quality:
            quality -= 5
            img.save(src_path, 'JPEG', quality=quality, optimize=True)
    
    return get_file_size_kb(src_path)

def main():
    if len(sys.argv) > 1:
        img_dir = sys.argv[1]
    else:
        img_dir = '/www/wwwroot/lovehibachi_demo/public/static/img'
    
    if len(sys.argv) > 2:
        target_size = int(sys.argv[2])
    else:
        target_size = TARGET_SIZE_KB
    
    extensions = ('.jpg', '.jpeg', '.png')
    
    print(f"📁 扫描目录: {img_dir}")
    print(f"🎯 目标大小: <= {target_size}KB")
    print()
    
    files = []
    for f in Path(img_dir).rglob('*'):
        if f.suffix.lower() in extensions and f.is_file():
            size = get_file_size_kb(f)
            if size > target_size:
                files.append((f, size))
    
    files.sort(key=lambda x: x[1], reverse=True)
    
    if not files:
        print("✅ 没有需要压缩的图片")
        return
    
    print(f"📋 需要压缩的图片 ({len(files)} 张):\n")
    
    total_original = 0
    total_compressed = 0
    
    for i, (path, orig_size) in enumerate(files, 1):
        print(f"[{i}/{len(files)}] 压缩 {path.name} ({orig_size:.0f}KB)...", end=' ', flush=True)
        try:
            new_size = compress_image(path, target_size)
            ratio = (1 - new_size / orig_size) * 100
            print(f"✅ {new_size:.0f}KB (减少 {ratio:.0f}%)")
            total_original += orig_size
            total_compressed += new_size
        except Exception as e:
            print(f"❌ 失败: {e}")
    
    print()
    print(f"📊 总计: {total_original:.0f}KB → {total_compressed:.0f}KB (减少 {(total_original-total_compressed)/total_original*100:.1f}%)")

if __name__ == '__main__':
    main()
