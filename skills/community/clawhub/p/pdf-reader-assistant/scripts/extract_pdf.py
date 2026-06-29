#!/usr/bin/env python3
"""
PDF 文本提取脚本 v2.0
支持：普通PDF文本提取、表格提取(pdfplumber)、扫描版OCR(pytesseract/easyocr)、图片描述
输出 JSON 格式：{success, pages, tables, text, metadata, is_scanned, error}
"""

import sys
import json
import os
import re


def check_deps():
    """检查并提示缺失依赖"""
    missing = []
    try:
        import fitz
    except ImportError:
        missing.append("pymupdf")
    return missing


def detect_scanned(doc) -> bool:
    """检测是否为扫描版PDF（图片型）"""
    try:
        import fitz
        text_pages = 0
        sample = min(5, doc.page_count)
        for i in range(sample):
            text = doc[i].get_text("text").strip()
            if len(text) > 50:
                text_pages += 1
        return text_pages == 0
    except Exception:
        return False


def extract_tables(pdf_path: str, max_pages: int = 0) -> list:
    """使用 pdfplumber 提取表格"""
    try:
        import pdfplumber
    except ImportError:
        return []

    tables_result = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = pdf.pages[:max_pages] if max_pages > 0 else pdf.pages
            for i, page in enumerate(pages):
                page_tables = page.extract_tables()
                for j, table in enumerate(page_tables):
                    if not table:
                        continue
                    # 转为markdown表格
                    md_rows = []
                    for k, row in enumerate(table):
                        cells = [str(c or "").strip() for c in row]
                        md_rows.append("| " + " | ".join(cells) + " |")
                        if k == 0:
                            md_rows.append("|" + "|".join(["---"] * len(cells)) + "|")
                    tables_result.append({
                        "page": i + 1,
                        "table_index": j + 1,
                        "rows": len(table),
                        "cols": len(table[0]) if table else 0,
                        "markdown": "\n".join(md_rows),
                        "raw": table,
                    })
    except Exception as e:
        pass
    return tables_result


def extract_with_ocr(pdf_path: str, max_pages: int = 0) -> dict:
    """扫描版PDF OCR提取"""
    # 优先 pytesseract，其次 easyocr
    try:
        import fitz
        import pytesseract
        from PIL import Image
        import io

        doc = fitz.open(pdf_path)
        total = doc.page_count
        n = min(total, max_pages) if max_pages > 0 else total
        pages_text = []

        for i in range(n):
            page = doc[i]
            mat = fitz.Matrix(2, 2)  # 2x缩放提升识别率
            clip = page.get_pixmap(matrix=mat)
            img = Image.open(io.BytesIO(clip.tobytes("png")))
            text = pytesseract.image_to_string(img, lang='chi_sim+eng')
            pages_text.append({
                "page": i + 1,
                "chars": len(text),
                "text": text.strip(),
                "ocr_engine": "pytesseract"
            })
        doc.close()

        full_text = "\n\n".join([p["text"] for p in pages_text])
        return {
            "success": True,
            "filename": os.path.basename(pdf_path),
            "total_pages": total,
            "pages_read": n,
            "is_scanned": True,
            "ocr_engine": "pytesseract",
            "full_text": full_text,
            "pages": pages_text,
            "tables": [],
            "truncated": max_pages > 0 and total > max_pages,
            "metadata": {},
        }
    except ImportError:
        pass

    try:
        import fitz
        import easyocr
        import numpy as np
        import io
        from PIL import Image

        reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        doc = fitz.open(pdf_path)
        total = doc.page_count
        n = min(total, max_pages) if max_pages > 0 else total
        pages_text = []

        for i in range(n):
            page = doc[i]
            mat = fitz.Matrix(2, 2)
            clip = page.get_pixmap(matrix=mat)
            img = Image.open(io.BytesIO(clip.tobytes("png")))
            results = reader.readtext(np.array(img))
            text = " ".join([r[1] for r in results])
            pages_text.append({
                "page": i + 1,
                "chars": len(text),
                "text": text.strip(),
                "ocr_engine": "easyocr"
            })
        doc.close()

        full_text = "\n\n".join([p["text"] for p in pages_text])
        return {
            "success": True,
            "filename": os.path.basename(pdf_path),
            "total_pages": total,
            "pages_read": n,
            "is_scanned": True,
            "ocr_engine": "easyocr",
            "full_text": full_text,
            "pages": pages_text,
            "tables": [],
            "truncated": max_pages > 0 and total > max_pages,
            "metadata": {},
        }
    except ImportError:
        pass

    return {
        "success": False,
        "is_scanned": True,
        "error": "检测到扫描版PDF，但未安装OCR依赖。请安装：pip install pytesseract pillow 并确保系统已安装 tesseract-ocr，或安装 pip install easyocr",
    }


def extract_image_descriptions(doc) -> list:
    """提取PDF中图片并给出描述（返回图片数量和位置信息）"""
    images_info = []
    for i in range(doc.page_count):
        page = doc[i]
        img_list = page.get_images(full=True)
        if img_list:
            images_info.append({
                "page": i + 1,
                "image_count": len(img_list),
                "note": f"第{i+1}页包含 {len(img_list)} 张图片/图表（建议关注其内容）"
            })
    return images_info


def extract_pdf(pdf_path: str, max_pages: int = 0, extract_tables_flag: bool = True) -> dict:
    """Extract text (and optionally tables) from a PDF file."""
    try:
        import fitz
    except ImportError:
        return {"success": False, "error": "pymupdf not installed. Run: pip install pymupdf"}

    if not os.path.exists(pdf_path):
        return {"success": False, "error": f"File not found: {pdf_path}"}

    try:
        doc = fitz.open(pdf_path)
        metadata = doc.metadata
        total_pages = doc.page_count

        # 检测是否为扫描版
        is_scanned = detect_scanned(doc)
        if is_scanned:
            doc.close()
            return extract_with_ocr(pdf_path, max_pages)

        pages_to_read = min(total_pages, max_pages) if max_pages > 0 else total_pages
        pages_text = []

        for i in range(pages_to_read):
            page = doc[i]
            text = page.get_text("text")
            pages_text.append({
                "page": i + 1,
                "chars": len(text),
                "text": text.strip()
            })

        # 提取图片信息
        images_info = extract_image_descriptions(doc)
        doc.close()

        full_text = "\n\n".join([p["text"] for p in pages_text])

        # 提取表格
        tables = []
        if extract_tables_flag:
            tables = extract_tables(pdf_path, max_pages)

        return {
            "success": True,
            "filename": os.path.basename(pdf_path),
            "total_pages": total_pages,
            "pages_read": pages_to_read,
            "is_scanned": False,
            "metadata": {
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "creator": metadata.get("creator", ""),
                "format": metadata.get("format", ""),
            },
            "full_text": full_text,
            "pages": pages_text,
            "tables": tables,
            "images": images_info,
            "truncated": max_pages > 0 and total_pages > max_pages,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "Usage: extract_pdf.py <pdf_path> [max_pages]"}, ensure_ascii=False))
        sys.exit(1)

    path = sys.argv[1]
    max_p = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    result = extract_pdf(path, max_p)
    print(json.dumps(result, ensure_ascii=False, indent=2))
