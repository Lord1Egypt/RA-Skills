#!/usr/bin/env python3
"""pdf_split.py — 拆分 PDF（能力 #5）

用法：
  python3 pdf_split.py in.pdf --ranges "1-5,8,10-12" --outdir ./out
  python3 pdf_split.py in.pdf --every 50 --outdir ./out
  python3 pdf_split.py in.pdf --bookmarks --outdir ./out   # 按一级书签拆分
"""
import argparse, os, re, sys

def parse_ranges(spec, npages):
    parts = []
    for seg in spec.split(","):
        seg = seg.strip()
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", seg)
        if not m:
            sys.exit(f"❌ 无法解析页范围：{seg}")
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        if a < 1 or b > npages or a > b:
            sys.exit(f"❌ 页范围越界：{seg}（总页数 {npages}）")
        parts.append((a, b))
    return parts

def split(src_path, chunks, outdir, names=None):
    import fitz
    src = fitz.open(src_path)
    os.makedirs(outdir, exist_ok=True)
    base = os.path.splitext(os.path.basename(src_path))[0]
    made = []
    for i, (a, b) in enumerate(chunks, 1):
        name = names[i - 1] if names else f"{base}_p{a}-{b}.pdf"
        dst = fitz.open()
        dst.insert_pdf(src, from_page=a - 1, to_page=b - 1)
        path = os.path.join(outdir, name)
        dst.save(path, garbage=3, deflate=True)
        dst.close()
        made.append((name, b - a + 1))
    src.close()
    return made

def main():
    ap = argparse.ArgumentParser(description="拆分 PDF")
    ap.add_argument("pdf")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--ranges", help='如 "1-5,8,10-12"')
    g.add_argument("--every", type=int, help="每 N 页一份")
    g.add_argument("--bookmarks", action="store_true", help="按一级书签拆分")
    ap.add_argument("--outdir", default="./split_out")
    a = ap.parse_args()
    import fitz
    doc = fitz.open(a.pdf)
    n = doc.page_count
    names = None
    if a.ranges:
        chunks = parse_ranges(a.ranges, n)
    elif a.every:
        chunks = [(s, min(s + a.every - 1, n)) for s in range(1, n + 1, a.every)]
    else:
        toc = [t for t in doc.get_toc() if t[0] == 1]
        if not toc:
            sys.exit("❌ 无书签可拆（扫描件请走 OCR 标题检测流程）")
        chunks, names = [], []
        for i, (_, title, page) in enumerate(toc):
            end = (toc[i + 1][2] - 1) if i + 1 < len(toc) else n
            chunks.append((page, end))
            safe = re.sub(r'[\\/:*?"<>|]', "-", title)
            names.append(f"{i+1:02d}_{safe}.pdf")
    doc.close()
    made = split(a.pdf, chunks, a.outdir, names)
    print(f"✅ 拆分完成 {len(made)} 份 → {a.outdir}/")
    for name, pages in made:
        print(f"   {name}（{pages} 页）")

if __name__ == "__main__":
    main()
