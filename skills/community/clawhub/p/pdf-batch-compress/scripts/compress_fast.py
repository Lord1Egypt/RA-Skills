#!/usr/bin/env python3
"""
单文件PDF压缩脚本 - 优化版（跳过无效步骤，直接渲染）
用法: python3 compress_fast.py <filepath> [threshold_mb]
针对GS无法压缩的Foxit PDF，直接用PyMuPDF渲染，跳过pikepdf/优化步骤。
"""
import os
import sys
import tempfile
import shutil

# 自动检测阈值
THRESHOLD_MB = int(sys.argv[2]) if len(sys.argv) > 2 else 50
THRESHOLD = THRESHOLD_MB * 1024 * 1024


def get_size(path):
    return os.path.getsize(path)


def compress_render(input_path, output_path, dpi=150, jpeg_quality=70):
    try:
        import fitz
        doc = fitz.open(input_path)
        new_doc = fitz.open()
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)
        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img_bytes = pix.tobytes("jpeg", jpg_quality=jpeg_quality)
            rect = page.rect
            new_page = new_doc.new_page(width=rect.width, height=rect.height)
            new_page.insert_image(rect, stream=img_bytes)
        new_doc.save(output_path, garbage=4, deflate=True)
        new_doc.close()
        doc.close()
        return True
    except Exception:
        return False


def compress(filepath):
    orig_size = get_size(filepath)
    orig_mb = orig_size / (1024 * 1024)

    if orig_size <= THRESHOLD:
        print(f"SKIP|{filepath}|{orig_mb:.1f}|{orig_mb:.1f}|already_small")
        return

    # 根据原始大小选择更激进的初始DPI
    # 经验值：渲染压缩比约0.5-0.7x
    if orig_mb <= 65:
        configs = [(120, 65), (100, 55), (80, 50), (72, 45), (60, 40), (50, 40)]
    elif orig_mb <= 80:
        configs = [(100, 60), (80, 50), (72, 45), (60, 40), (50, 40)]
    elif orig_mb <= 100:
        configs = [(80, 55), (72, 50), (60, 40), (50, 40)]
    elif orig_mb <= 150:
        configs = [(72, 50), (60, 40), (50, 40)]
    elif orig_mb <= 200:
        configs = [(72, 45), (60, 40), (50, 40)]
    elif orig_mb <= 300:
        configs = [(60, 40), (50, 35)]
    else:
        configs = [(50, 35), (40, 30)]

    tmp_fd, tmp_path = tempfile.mkstemp(suffix='.pdf', dir='/tmp')
    os.close(tmp_fd)

    try:
        for dpi, quality in configs:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            if compress_render(filepath, tmp_path, dpi, quality):
                new_size = get_size(tmp_path)
                if new_size <= THRESHOLD:
                    new_mb = new_size / (1024 * 1024)
                    shutil.move(tmp_path, filepath)
                    print(f"OK|{filepath}|{orig_mb:.1f}|{new_mb:.1f}|render_{dpi}dpi")
                    return

        # 最佳努力
        if os.path.exists(tmp_path) and get_size(tmp_path) < orig_size * 0.7:
            new_mb = get_size(tmp_path) / (1024 * 1024)
            shutil.move(tmp_path, filepath)
            print(f"PARTIAL|{filepath}|{orig_mb:.1f}|{new_mb:.1f}|best_effort")
        else:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            print(f"FAIL|{filepath}|{orig_mb:.1f}|{orig_mb:.1f}|all_failed")

    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        print(f"ERROR|{filepath}|{orig_mb:.1f}|0|{str(e)[:100]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: compress_fast.py <filepath> [threshold_mb]")
        sys.exit(1)
    compress(sys.argv[1])
