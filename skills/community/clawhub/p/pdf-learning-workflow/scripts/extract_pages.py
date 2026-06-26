#!/usr/bin/env python3
"""PDF 拆页：提取每一页为高清 PNG"""
import sys, os
import fitz  # PyMuPDF

def extract_pages(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    total = len(doc)
    print(f"📄 总页数: {total}")
    
    for i in range(total):
        page = doc[i]
        # 300 DPI → zoom = 300/72 ≈ 4.17
        zoom = 300 / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        out_path = os.path.join(output_dir, f"page_{i+1:04d}.png")
        pix.save(out_path)
        if (i + 1) % 5 == 0:
            print(f"  ⏳ 已提取 {i+1}/{total} 页")
    
    print(f"✅ 提取完成: {total} 页 → {output_dir}")
    return total

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: extract_pages.py <pdf_path> <output_dir>")
        sys.exit(1)
    extract_pages(sys.argv[1], sys.argv[2])
