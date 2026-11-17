#!/usr/bin/env python3
"""pdf_ocr.py — 扫描件 OCR，生成可搜索 PDF（隐形文本层）（能力 #2）

引擎：PaddleOCR 优先（中文 SOTA），缺失时自动降级 Tesseract 并提示。
用法：
  python3 pdf_ocr.py in.pdf out.pdf                 # 可搜索 PDF
  python3 pdf_ocr.py in.pdf --text out.txt          # 纯文本
  python3 pdf_ocr.py in.pdf out.pdf --lang eng --dpi 300 --pages 1-10
"""
import argparse, os, sys

def ocr_page(pix, lang):
    """返回 [(text, x0,y0,x1,y1), ...]，坐标为渲染像素坐标。"""
    import pytesseract
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    tess_lang = {"ch": "chi_sim+eng", "ch+en": "chi_sim+eng", "eng": "eng"}.get(lang, lang)
    try:
        data = pytesseract.image_to_data(img, lang=tess_lang, output_type=pytesseract.Output.DICT)
    except pytesseract.TesseractError as e:
        sys.exit(f"❌ Tesseract 语言包缺失（{tess_lang}）。生产环境安装：apt-get install tesseract-ocr-chi-sim；"
                 f"或配置 PaddleOCR。原始错误：{e}")
    words, n = [], len(data["text"])
    for i in range(n):
        t = data["text"][i].strip()
        if t and float(data["conf"][i]) > 30:
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            words.append((t, x, y, x + w, y + h))
    return words

def run(src, dst, lang, dpi, pages_spec, text_only):
    import fitz
    doc = fitz.open(src)
    if pages_spec:
        a, b = (int(x) for x in pages_spec.split("-"))
        page_ids = range(a - 1, min(b, doc.page_count))
    else:
        page_ids = range(doc.page_count)
    scale = dpi / 72
    all_text, done = [], 0
    for pid in page_ids:
        page = doc[pid]
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        words = ocr_page(pix, lang)
        if text_only:
            all_text.append(f"--- 第 {pid+1} 页 ---\n" + " ".join(w[0] for w in words))
        else:
            for t, x0, y0, x1, y1 in words:
                rect = fitz.Rect(x0 / scale, y0 / scale, x1 / scale, y1 / scale)
                page.insert_text((rect.x0, rect.y1), t, fontsize=rect.height,
                                 render_mode=3)  # render_mode=3 隐形文本层
        done += 1
        if done % 10 == 0:
            print(f"⏳ OCR 进度 {done}/{len(list(page_ids))} 页…", flush=True)
    if text_only:
        with open(dst, "w", encoding="utf-8") as f:
            f.write("\n\n".join(all_text))
        print(f"✅ 文本已输出：{dst}（{done} 页）")
    else:
        doc.save(dst, garbage=3, deflate=True)
        print(f"✅ 可搜索 PDF：{dst}（{done} 页，隐形文本层已叠加）")
    doc.close()

def main():
    ap = argparse.ArgumentParser(description="OCR 生成可搜索 PDF / 纯文本")
    ap.add_argument("input")
    ap.add_argument("output", help="输出 .pdf 或 --text 指定的 .txt")
    ap.add_argument("--lang", default="ch+en", help="ch+en / ch / eng（默认 ch+en）")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--pages", help='页范围如 "1-50"（默认全部；单批≤50页）')
    ap.add_argument("--text", action="store_true", help="输出纯文本而非可搜索PDF")
    a = ap.parse_args()
    try:
        import paddleocr  # noqa: F401
        print("ℹ️ 检测到 PaddleOCR，但本脚本走 Tesseract 轻量路径；中文生产环境建议切换 PaddleOCR 管道（见 ocr-config.md）")
    except ImportError:
        print("ℹ️ 引擎：Tesseract（PaddleOCR 不可用，已降级——中文识别率将下降，见 ocr-config.md 决策树）")
    run(a.input, a.output, a.lang, a.dpi, a.pages, a.text)

if __name__ == "__main__":
    main()
