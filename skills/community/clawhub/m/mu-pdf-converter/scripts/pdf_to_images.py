#!/usr/bin/env python3
"""
pdf_to_images.py - 将 PDF 每页渲染为图片
用法：python pdf_to_images.py input.pdf [--dpi 150] [--format png|jpg] [--pages 1-3] [--outdir ./output]
"""

import argparse
import sys
from pathlib import Path

# ── 依赖检查 ──────────────────────────────────
try:
    import fitz  # PyMuPDF
except ImportError:
    print(
        "[错误] 缺少 pymupdf\n请运行：pip install pymupdf",
        file=sys.stderr,
    )
    sys.exit(1)

# 引入公共工具（支持直接运行或作为模块调用）
sys.path.insert(0, str(Path(__file__).parent))
from utils import parse_page_range, generate_output_path, check_scanned_and_warn  # noqa: E402


# ─────────────────────────────────────────────
# 核心逻辑
# ─────────────────────────────────────────────

def pdf_to_images(
    pdf_path: str,
    dpi: int = 150,
    fmt: str = "png",
    pages_str: str = "all",
    outdir: str = None,
) -> list:
    """
    将 PDF 页面渲染为图片文件。

    参数:
        pdf_path: 输入 PDF 路径
        dpi: 渲染分辨率，默认 150
        fmt: 输出格式，'png' 或 'jpg'
        pages_str: 页面范围，如 'all', '1-3', '1,3,5'
        outdir: 输出目录（默认与 PDF 同目录）
    返回:
        生成的图片文件路径列表
    """
    pdf_path = str(Path(pdf_path).resolve())
    if not Path(pdf_path).exists():
        print(f"[错误] 文件不存在：{pdf_path}", file=sys.stderr)
        sys.exit(1)

    # 格式标准化
    fmt = fmt.lower().strip(".")
    if fmt in ("jpeg", "jpg"):
        fmt = "jpeg"
        ext = "jpg"
    else:
        fmt = "png"
        ext = "png"

    # 输出目录
    stem = Path(pdf_path).stem
    if outdir:
        import os
        os.makedirs(outdir, exist_ok=True)
        out_base = Path(outdir)
    else:
        out_base = Path(pdf_path).parent

    # 打开 PDF
    doc = fitz.open(pdf_path)
    total = len(doc)
    print(f"[信息] 共 {total} 页，开始渲染（DPI={dpi}，格式={ext.upper()}）")

    # 解析页面范围
    page_indices = parse_page_range(pages_str, total)
    if not page_indices:
        print("[错误] 页面范围无效，未找到任何页面", file=sys.stderr)
        doc.close()
        sys.exit(1)

    # 渲染矩阵：scale = dpi / 72
    scale = dpi / 72.0
    mat = fitz.Matrix(scale, scale)

    output_files = []
    for idx in page_indices:
        page = doc[idx]
        pix = page.get_pixmap(matrix=mat, alpha=False)

        filename = f"{stem}_page_{idx + 1:03d}.{ext}"
        out_path = str(out_base / filename)

        if fmt == "jpeg":
            pix.save(out_path, output="jpeg", jpg_quality=90)
        else:
            pix.save(out_path)

        output_files.append(out_path)
        print(f"  ✓ 第 {idx + 1} 页 → {out_path}")

    doc.close()
    print(f"\n[完成] 共生成 {len(output_files)} 张图片")
    return output_files


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="将 PDF 每页渲染为图片（PNG/JPG）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python pdf_to_images.py report.pdf
  python pdf_to_images.py report.pdf --dpi 300 --format jpg
  python pdf_to_images.py report.pdf --pages 1-5 --outdir ./images
  python pdf_to_images.py report.pdf --pages 1,3,7 --format png
        """,
    )
    parser.add_argument("input", help="输入 PDF 文件路径")
    parser.add_argument(
        "--dpi", type=int, default=150,
        help="渲染分辨率，默认 150（建议范围 72-300）"
    )
    parser.add_argument(
        "--format", dest="fmt", choices=["png", "jpg", "jpeg"],
        default="png", help="输出图片格式，默认 png"
    )
    parser.add_argument(
        "--pages", default="all",
        help="页面范围，如 'all'、'1-3'、'1,3,5'，默认 all"
    )
    parser.add_argument(
        "--outdir", default=None,
        help="输出目录（默认与 PDF 同目录）"
    )

    args = parser.parse_args()
    check_scanned_and_warn(args.input, allow_continue=True)  # 图片转换对扫描件有效，仅警告
    pdf_to_images(
        pdf_path=args.input,
        dpi=args.dpi,
        fmt=args.fmt,
        pages_str=args.pages,
        outdir=args.outdir,
    )


if __name__ == "__main__":
    main()
