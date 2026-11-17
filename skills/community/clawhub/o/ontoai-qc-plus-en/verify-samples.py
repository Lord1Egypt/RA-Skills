#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ontoAI 质检官 · 样例 PDF 校验脚本
校验 PDF 打印链路不回退到「合成粗体 Type3 位图」（发糊元凶）与「█ 实心黑块」。

硬约束（任一项不为 0 即判失败）：
  - 位图 Type3 计数 = 0   （Type3 内有 /Image|BI|Do 位图标记为失败）
  - emoji 计数       = 0
  - █ (U+2588) 计数  = 0

用法：python verify-samples.py
"""
import fitz
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PDFS = sorted(glob.glob(os.path.join(ROOT, "evals", "samples", "*.pdf")))
PDFS += [os.path.join(ROOT, "evals", "selftest-report.pdf")]

EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF"          # 彩色 emoji 与象形符号（PDF 会变位图、放大发糊）
    "\U0001F1E6-\U0001F1FF"          # 区域指示符（国旗）
    "\U00002B00-\U00002BFF"          # 杂项符号与箭头（如 ⬛⚫，彩色）
    "\u2705\u274c\u2b55\u2757]"       # 特定彩色 emoji 型 dingbat
    # 注意：U+2713（✓ 普通对勾）属正常矢量字形，不计入，以免误报
)

# 英文外壳样例专属：不应残留的中文 UI 标签
ZH_CHROME = ["受检产物", "检验结论", "合计", "必改", "可改", "存疑",
             "已通过", "报告结束", "质检报告", "交付前最后一道关"]
EN_CHROME_OK = ["Product Inspected", "Inspection Conclusion", "Total",
                "Must Fix", "Should Fix", "Unverified", "Passed",
                "End of Report", "Quality Report"]


def classify_type3(doc, xref):
    """返回 'bitmap' 或 'vector'。Type3 内有位图算子即为 bitmap。"""
    try:
        stream = doc.xref_stream(xref)
        if isinstance(stream, bytes):
            stream = stream.decode("latin1", "ignore")
        if re.search(r"\bDo\b|/Image|\bBI\b", stream):
            return "bitmap"
    except Exception:
        pass
    return "vector"


def verify(pdf_path):
    doc = fitz.open(pdf_path)
    bitmap_type3 = 0
    vector_type3 = 0
    font_kind = {}
    alltext = ""
    for pg in doc:
        for fnt in pg.get_fonts(full=True):
            xref = int(fnt[0])
            ftype = fnt[2]
            font_kind[ftype] = font_kind.get(ftype, 0) + 1
            if ftype == "Type3":
                if classify_type3(doc, xref) == "bitmap":
                    bitmap_type3 += 1
                else:
                    vector_type3 += 1
        alltext += pg.get_text()
    doc.close()

    emoji_hits = len(EMOJI_RE.findall(alltext))
    block_hits = alltext.count("\u2588")

    # 英文外壳样例专属校验：不应残留中文 UI 标签；中文样例本就该有中文，不计罚
    is_en = "style-a-en" in pdf_path
    residual_zh = [w for w in ZH_CHROME if w in alltext]
    en_present = [w for w in EN_CHROME_OK if w in alltext]

    ok = (bitmap_type3 == 0 and emoji_hits == 0 and block_hits == 0)
    if is_en:
        ok = ok and (len(residual_zh) == 0)
    return {
        "bitmap_type3": bitmap_type3,
        "vector_type3": vector_type3,
        "font_kind": font_kind,
        "emoji": emoji_hits,
        "block": block_hits,
        "residual_zh": residual_zh if is_en else [],
        "en_present": en_present,
        "ok": ok,
    }


def main():
    print(f"{'文件':52} {'位图T3':>6} {'矢量T3':>6} {'emoji':>6} {'█':>3}  结论")
    print("-" * 92)
    all_ok = True
    for p in PDFS:
        if not os.path.exists(p):
            continue
        r = verify(p)
        name = os.path.relpath(p, ROOT)
        flag = "✅" if r["ok"] else "❌"
        all_ok = all_ok and r["ok"]
        print(f"{name:52} {r['bitmap_type3']:>6} {r['vector_type3']:>6} "
              f"{r['emoji']:>6} {r['block']:>3}  {flag}")
        if r["font_kind"]:
            print("        字体分布: " + ", ".join(f"{k}={v}" for k, v in r["font_kind"].items()))
        if r["residual_zh"]:
            print("        ⚠️ 残留中文 UI 标签: " + " / ".join(r["residual_zh"]))
        if "style-a-en" in name:
            if r["en_present"]:
                print("        ✔ 英文标签就位: " + " / ".join(r["en_present"]))
            else:
                print("        ⚠️ 未检出任何英文 UI 标签")
    print("-" * 92)
    print("全部通过 ✅" if all_ok else "存在失败 ❌")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
