#!/usr/bin/env python3
"""
pdf2md_figs.py — 把一个 PDF 拆成「正文 Markdown + 图片文件夹」,但**不读图**。

设计目标:文字走 markitdown 转 MD;图片单独抽出来存盘 + 建索引清单,
不送进模型上下文。需要看某张图时,再单独打开那一张,避免 token 浪费在无关图上。

用法:
    python pdf2md_figs.py paper.pdf                 # 输出到 ./paper_out/
    python pdf2md_figs.py paper.pdf -o myout        # 指定输出目录
    python pdf2md_figs.py paper.pdf --min-px 150    # 调整小图过滤阈值(滤 logo/图标)

产物:
    <out>/<stem>.md                正文 Markdown(markitdown)
    <out>/<stem>_figs/p02_img1.png 抽出的图(按页命名)
    <out>/<stem>_figs/MANIFEST.txt 图片索引清单(页码 / 文件 / 尺寸 / 该页 Figure 编号)
"""
import argparse
import re
import sys
from pathlib import Path


def extract_text(pdf_path: Path, md_path: Path) -> None:
    """用 markitdown 把正文转成 Markdown(沿用之前的方式)。"""
    from markitdown import MarkItDown
    md = MarkItDown(enable_plugins=False)
    result = md.convert(str(pdf_path))
    md_path.write_text(result.text_content, encoding="utf-8")


def figure_numbers_on_page(page_text: str):
    """从一页文字里找图注,如 'Figure 1.' / 'Figure 2:' ,返回去重后的编号列表。"""
    nums = re.findall(r"Figure\s+(\d+)\s*[\.\:]", page_text)
    seen, out = set(), []
    for n in nums:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def extract_figures(pdf_path: Path, figs_dir: Path, min_px: int, dpi: int = 200):
    """抽内嵌图。按「该页是否有 Figure 图注」分流:
       有图注 -> 主文件夹(正文图);无图注 -> _misc/ 子文件夹(疑似 logo/广告/TOC)。
       小于 min_px 的直接当 logo/图标跳过。返回清单记录。"""
    import fitz  # PyMuPDF

    figs_dir.mkdir(parents=True, exist_ok=True)
    misc_dir = figs_dir / "_misc"
    doc = fitz.open(str(pdf_path))
    records = []
    seen_xref = set()

    for pno, page in enumerate(doc, start=1):
        page_text = page.get_text()
        fig_nums = figure_numbers_on_page(page_text)
        imgs = page.get_images(full=True)
        idx = 0
        kept_on_page = 0
        for img in imgs:
            xref = img[0]
            if xref in seen_xref:        # 跨页复用的图(页眉logo等)只存一次
                continue
            pix = fitz.Pixmap(doc, xref)
            if pix.width < min_px or pix.height < min_px:
                pix = None               # 太小,判为 logo/图标,跳过
                continue
            if pix.n - pix.alpha >= 4:    # CMYK/分离通道 -> RGB
                pix = fitz.Pixmap(fitz.csRGB, pix)
            idx += 1
            kept_on_page += 1
            is_fig = bool(fig_nums)       # 该页有 Figure 图注 = 正文图
            fname = f"p{pno:02d}_img{idx}.png"
            if is_fig:
                pix.save(str(figs_dir / fname))
                rel = fname
            else:
                misc_dir.mkdir(parents=True, exist_ok=True)
                pix.save(str(misc_dir / fname))
                rel = f"_misc/{fname}"
            records.append({
                "page": pno,
                "file": rel,
                "w": pix.width,
                "h": pix.height,
                "fig_hint": ",".join(fig_nums) if fig_nums else "",
            })
            seen_xref.add(xref)
            pix = None

        # 该页有 "Figure N" 图注、但没抽到任何内嵌大图 -> 多半是矢量图,自动整页栅格化兜底
        if fig_nums and kept_on_page == 0:
            mat = fitz.Matrix(dpi / 72, dpi / 72)
            pix = page.get_pixmap(matrix=mat)
            fname = f"p{pno:02d}_pagerender.png"
            pix.save(str(figs_dir / fname))
            records.append({
                "page": pno,
                "file": fname,
                "w": pix.width,
                "h": pix.height,
                "fig_hint": ",".join(fig_nums),
                "note": "整页栅格化(矢量图)",
            })
            pix = None
    doc.close()
    return records


def write_manifest(records, manifest_path: Path, stem: str):
    main = [r for r in records if not r["file"].startswith("_misc/")]
    misc = [r for r in records if r["file"].startswith("_misc/")]
    lines = [f"# 图片索引 — {stem}", ""]

    lines.append("## 正文图(主文件夹)")
    if not main:
        lines.append("(无)")
    else:
        lines.append(f"{'页':>3}  {'文件':<16}  {'尺寸(px)':<12}  Figure")
        lines.append("-" * 50)
        for r in main:
            size = f"{r['w']}x{r['h']}" if r["w"] else "-"
            hint = f"Fig {r['fig_hint']}" if r["fig_hint"] else ""
            lines.append(f"{r['page']:>3}  {r['file']:<16}  {size:<12}  {hint}")

    if misc:
        lines.append("")
        lines.append("## 疑似非正文图(_misc/ —— logo / 广告 / TOC,所在页无 Figure 图注)")
        lines.append(f"{'页':>3}  {'文件':<22}  {'尺寸(px)':<12}")
        lines.append("-" * 46)
        for r in misc:
            size = f"{r['w']}x{r['h']}"
            lines.append(f"{r['page']:>3}  {r['file']:<22}  {size:<12}")

    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="PDF -> 正文Markdown + 图片(不读图)")
    ap.add_argument("pdf", help="输入 PDF 路径")
    ap.add_argument("-o", "--out", default=None, help="输出目录(默认 <stem>_out)")
    ap.add_argument("--min-px", type=int, default=120,
                    help="小于该像素宽/高的图判为 logo/图标并跳过(默认 120)")
    ap.add_argument("--dpi", type=int, default=200,
                    help="矢量图整页栅格化兜底时的分辨率(默认 200)")
    args = ap.parse_args()

    pdf_path = Path(args.pdf).expanduser()
    if not pdf_path.is_file():
        sys.exit(f"找不到文件: {pdf_path}")

    stem = pdf_path.stem
    out_dir = Path(args.out) if args.out else pdf_path.parent / f"{stem}_out"
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"{stem}.md"
    figs_dir = out_dir / f"{stem}_figs"

    print(f"[1/2] 正文 -> Markdown ...")
    extract_text(pdf_path, md_path)
    nwords = len(md_path.read_text(encoding="utf-8").split())
    print(f"      {md_path}  ({nwords} 词)")

    print(f"[2/2] 提取图片(不读图)...")
    records = extract_figures(pdf_path, figs_dir, args.min_px, args.dpi)
    manifest = write_manifest(records, figs_dir / "MANIFEST.txt", stem)
    n_imgs = sum(1 for r in records if r["w"])
    print(f"      {figs_dir}/  ({n_imgs} 张图)")
    print()
    print(manifest)


if __name__ == "__main__":
    main()
