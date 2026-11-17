#!/usr/bin/env python3
"""pdf_convert.py — PDF → Word / Excel（能力 #1）

Word 首选 pdf2docx；复杂版面不达标时按 tech-spec.md 降级链处理。
Excel 走表格提取管道（pdf_extract_tables.py 同等逻辑）。
用法：
  python3 pdf_convert.py in.pdf out.docx
  python3 pdf_convert.py in.pdf out.xlsx
  python3 pdf_convert.py in.pdf out.docx --pages 1-10
"""
import argparse, os, sys

def to_docx(src, dst, pages_spec):
    from pdf2docx import Converter
    cv = Converter(src)
    if pages_spec:
        a, b = (int(x) for x in pages_spec.split("-"))
        cv.convert(dst, start=a - 1, end=b)
    else:
        cv.convert(dst)
    cv.close()

def to_xlsx(src, dst):
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__))
    r = subprocess.run([sys.executable, os.path.join(here, "pdf_extract_tables.py"),
                        src, "--xlsx", dst], capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        sys.exit(r.returncode)

def main():
    ap = argparse.ArgumentParser(description="PDF 转 Word/Excel")
    ap.add_argument("input")
    ap.add_argument("output", help=".docx 或 .xlsx")
    ap.add_argument("--pages", help='页范围 "1-10"')
    a = ap.parse_args()
    ext = os.path.splitext(a.output)[1].lower()
    if ext == ".docx":
        to_docx(a.input, a.output, a.pages)
        print(f"✅ 已转换：{a.output}")
        print("质检项：字体匹配≥90% / 表格原生可编辑 / 图片偏移≤5px / 页眉页脚归位。"
              "不达标走 tech-spec.md 降级链")
    elif ext == ".xlsx":
        to_xlsx(a.input, a.output)
    elif ext == ".pptx":
        sys.exit("PPT 转换按 capabilities-core.md #1 规程执行（一页一幻灯片管道），本脚本不支持")
    else:
        sys.exit(f"❌ 不支持的目标格式：{ext}")

if __name__ == "__main__":
    main()
