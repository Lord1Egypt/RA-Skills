# -*- coding: utf-8 -*-
"""Step 0: 把图纸 PDF 渲染成高分辨率 PNG(坐标基准)。
用法: python render_pdf.py <drawing.pdf> <out.png> [--dpi 400] [--page 0]
说明: 自动应用页面 /Rotate; 输出 PNG 像素尺寸(后续所有坐标以此为准)。
"""
import argparse, sys
import pymupdf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("out")
    ap.add_argument("--dpi", type=int, default=400)
    ap.add_argument("--page", type=int, default=0)
    a = ap.parse_args()
    doc = pymupdf.open(a.pdf)
    pg = doc[a.page]
    zoom = a.dpi / 72.0
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
    pix.save(a.out)
    print(f"OK saved={a.out} size={pix.width}x{pix.height} dpi={a.dpi} "
          f"page_rect={pg.rect} rotation={pg.rotation}")


if __name__ == "__main__":
    main()
