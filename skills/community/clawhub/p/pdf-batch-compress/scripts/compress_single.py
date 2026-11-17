#!/usr/bin/env python3
"""
单文件PDF压缩脚本 - 完整版（pikepdf结构优化 + PyMuPDF渲染）
用法: python3 compress_single.py <filepath> [threshold_mb]
先尝试pikepdf无损结构优化，失败后渲染为图片PDF。
适用于不确定PDF类型时的通用压缩。
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


def compress(filepath):
    orig_size = get_size(filepath)
    orig_mb = orig_size / (1024 * 1024)

    if orig_size <= THRESHOLD:
        print(f"SKIP|{filepath}|{orig_mb:.1f}|{orig_mb:.1f}|already_small")
        return

    import fitz

    # 估算初始DPI
    if orig_mb <= 75:
        start_dpi = 150
    elif orig_mb <= 100:
        start_dpi = 120
    elif orig_mb <= 150:
        start_dpi = 100
    elif orig_mb <= 200:
        start_dpi = 80
    elif orig_mb <= 300:
        start_dpi = 72
    else:
        start_dpi = 50

    tmp_fd, tmp_path = tempfile.mkstemp(suffix='.pdf', dir='/tmp')
    os.close(tmp_fd)

    try:
        # 快速尝试pikepdf（仅对小文件）
        if orig_mb < 80:
            try:
                import pikepdf
                pdf = pikepdf.open(filepath)
                pdf.save(tmp_path,
                         object_stream_mode=pikepdf.ObjectStreamMode.generate,
                         compress_streams=True,
                         stream_decode_level=pikepdf.StreamDecodeLevel.generalized)
                pdf.close()
                if os.path.getsize(tmp_path) <= THRESHOLD:
                    new_mb = os.path.getsize(tmp_path) / (1024*1024)
                    shutil.move(tmp_path, filepath)
                    print(f"OK|{filepath}|{orig_mb:.1f}|{new_mb:.1f}|pikepdf")
                    return
            except Exception:
                pass

        # 渲染为图片PDF
        dpi_configs = []
        d = start_dpi
        while d >= 50:
            q = 70 if d >= 120 else (60 if d >= 100 else (50 if d >= 72 else 40))
            dpi_configs.append((d, q))
            d -= 20

        # 确保包含关键DPI值
        for must_dpi in [150, 120, 100, 72, 50]:
            if not any(dpi == must_dpi for dpi, _ in dpi_configs):
                dpi_configs.append((must_dpi, 50 if must_dpi <= 72 else 60))

        # 按DPI从高到低排序
        dpi_configs.sort(key=lambda x: -x[0])
        seen = set()
        unique = []
        for d, q in dpi_configs:
            if (d, q) not in seen:
                seen.add((d, q))
                unique.append((d, q))

        best_size = orig_size

        for dpi, quality in unique:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

            try:
                doc = fitz.open(filepath)
                new_doc = fitz.open()
                zoom = dpi / 72.0
                mat = fitz.Matrix(zoom, zoom)

                for page_num in range(len(doc)):
                    page = doc[page_num]
                    pix = page.get_pixmap(matrix=mat, alpha=False)
                    img_bytes = pix.tobytes("jpeg", jpg_quality=quality)
                    rect = page.rect
                    new_page = new_doc.new_page(width=rect.width, height=rect.height)
                    new_page.insert_image(rect, stream=img_bytes)

                new_doc.save(tmp_path, garbage=4, deflate=True)
                new_doc.close()
                doc.close()

                new_size = os.path.getsize(tmp_path)
                if new_size <= THRESHOLD:
                    new_mb = new_size / (1024*1024)
                    shutil.move(tmp_path, filepath)
                    print(f"OK|{filepath}|{orig_mb:.1f}|{new_mb:.1f}|render_{dpi}dpi")
                    return

                if new_size < best_size:
                    best_size = new_size

            except Exception:
                continue

        # 最佳努力：如果至少压缩了30%
        if best_size < orig_size * 0.7:
            dpi, quality = unique[-1]
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            doc = fitz.open(filepath)
            new_doc = fitz.open()
            zoom = dpi / 72.0
            mat = fitz.Matrix(zoom, zoom)
            for page_num in range(len(doc)):
                page = doc[page_num]
                pix = page.get_pixmap(matrix=mat, alpha=False)
                img_bytes = pix.tobytes("jpeg", jpg_quality=quality)
                rect = page.rect
                new_page = new_doc.new_page(width=rect.width, height=rect.height)
                new_page.insert_image(rect, stream=img_bytes)
            new_doc.save(tmp_path, garbage=4, deflate=True)
            new_doc.close()
            doc.close()
            new_mb = os.path.getsize(tmp_path) / (1024*1024)
            shutil.move(tmp_path, filepath)
            print(f"PARTIAL|{filepath}|{orig_mb:.1f}|{new_mb:.1f}|best_effort_{dpi}dpi")
        else:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            print(f"FAIL|{filepath}|{orig_mb:.1f}|{orig_mb:.1f}|no_compression")

    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        print(f"ERROR|{filepath}|{orig_mb:.1f}|0|{str(e)[:100]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: compress_single.py <filepath> [threshold_mb]")
        sys.exit(1)
    compress(sys.argv[1])
