#!/usr/bin/env python3
"""pdf_compress.py — 智能分层压缩，支持目标大小迭代（能力 #15）

策略：文字/矢量无损 → 图片按显示尺寸降采样+JPEG 重编码（迭代降参）→ 对象清理
质量地板：dpi≥96 且 quality≥40；触底仍超标 → 报告极限值退出码 2
用法：
  python3 pdf_compress.py in.pdf out.pdf --target-mb 20
  python3 pdf_compress.py in.pdf out.pdf --dpi 150 --quality 70
"""
import argparse, io, os, sys

def compress(src, dst, dpi, quality):
    """把显示分辨率高于 dpi 的图片降采样到 dpi，并以 JPEG quality 重编码。"""
    import fitz
    from PIL import Image
    doc = fitz.open(src)
    seen = set()
    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            if xref in seen:
                continue
            seen.add(xref)
            try:
                rects = page.get_image_rects(xref)
                if not rects:
                    continue
                disp_w_in = max(r.width for r in rects) / 72  # 显示宽度（英寸）
                base = doc.extract_image(xref)
                im = Image.open(io.BytesIO(base["image"]))
                if im.mode not in ("RGB", "L"):
                    im = im.convert("RGB")
                cur_dpi = im.width / max(disp_w_in, 0.1)
                if cur_dpi <= dpi:  # 已低于目标分辨率，不动
                    continue
                new_w = max(int(disp_w_in * dpi), 50)
                new_h = max(int(im.height * new_w / im.width), 50)
                im = im.resize((new_w, new_h), Image.LANCZOS)
                buf = io.BytesIO()
                im.save(buf, "JPEG", quality=quality, optimize=True)
                page.replace_image(xref, stream=buf.getvalue())
            except Exception:
                continue
    doc.save(dst, garbage=4, deflate=True, deflate_images=True)
    doc.close()
    return os.path.getsize(dst)

def main():
    ap = argparse.ArgumentParser(description="PDF 智能压缩")
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--target-mb", type=float, help="目标大小（迭代降参直至达标或触底）")
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--quality", type=int, default=70)
    a = ap.parse_args()
    src_mb = os.path.getsize(a.input) / 1048576
    if not a.target_mb:
        size = compress(a.input, a.output, a.dpi, a.quality)
        print(f"✅ {src_mb:.1f}MB → {size/1048576:.1f}MB（dpi={a.dpi}, q={a.quality}）")
        return
    target = a.target_mb * 1048576
    if src_mb <= a.target_mb:
        print(f"ℹ️ 原文件 {src_mb:.1f}MB 已达标，无需压缩")
        return
    mb = src_mb
    for dpi, q in [(150, 70), (120, 55), (96, 40)]:
        size = compress(a.input, a.output, dpi, q)
        mb = size / 1048576
        print(f"⏳ 尝试 dpi={dpi} q={q} → {mb:.1f}MB")
        if size <= target:
            print(f"✅ 达标：{src_mb:.1f}MB → {mb:.1f}MB（dpi={dpi}, q={q}）")
            print("质检提示：文字层未参与有损压缩；请抽查公章/签名/二维码区")
            return
    print(f"⚠️ 已到质量地板（dpi≥96,q≥40），极限压缩至 {mb:.1f}MB，仍超目标。"
          f"继续将损伤文字清晰度——请用户裁决是否接受更低画质或拆分文件")
    sys.exit(2)

if __name__ == "__main__":
    main()
