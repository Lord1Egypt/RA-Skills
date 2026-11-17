#!/usr/bin/env python3
"""pdf_merge.py — 批量合并 PDF，自动生成目录书签（能力 #5）

用法：
  python3 pdf_merge.py out.pdf in1.pdf in2.pdf ...   # 按给定顺序合并
  python3 pdf_merge.py out.pdf --dir ./pdfs          # 按文件名自然序合并目录
"""
import argparse, os, re, sys

def natural_key(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]

def merge(inputs, output):
    import fitz
    out = fitz.open()
    toc, skipped = [], []
    for path in inputs:
        try:
            src = fitz.open(path)
            if src.needs_pass:
                skipped.append((os.path.basename(path), "加密未提供密码"))
                continue
            start = out.page_count + 1
            out.insert_pdf(src)
            toc.append([1, os.path.splitext(os.path.basename(path))[0], start])
            src.close()
        except Exception as e:
            skipped.append((os.path.basename(path), str(e)))
    if out.page_count == 0:
        print("❌ 无可合并文件")
        sys.exit(1)
    out.set_toc(toc)
    out.save(output, garbage=3, deflate=True)
    print(f"✅ 合并完成：{output}  共 {out.page_count} 页，{len(toc)} 章目录书签")
    out.close()
    for name, why in skipped:
        print(f"⚠️ 跳过：{name}（{why}）")

def main():
    ap = argparse.ArgumentParser(description="合并 PDF 并生成目录书签")
    ap.add_argument("output")
    ap.add_argument("inputs", nargs="*")
    ap.add_argument("--dir", help="合并指定目录下全部 PDF（自然序）")
    a = ap.parse_args()
    inputs = a.inputs
    if a.dir:
        inputs = [os.path.join(a.dir, f) for f in os.listdir(a.dir) if f.lower().endswith(".pdf")]
        inputs.sort(key=lambda p: natural_key(os.path.basename(p)))
    if not inputs:
        ap.error("未提供输入文件")
    merge(inputs, a.output)

if __name__ == "__main__":
    main()
