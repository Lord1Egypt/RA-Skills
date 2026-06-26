#!/usr/bin/env python3
"""
解析文件内容（PDF / DOCX / TXT / MD → 纯文本）
用法: python3 parse_file.py "/path/to/file.pdf"
"""
import sys
import os

def parse_pdf(path):
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages)
    except ImportError:
        # fallback: 尝试 pypdf
        try:
            from pypdf import PdfReader
            reader = PdfReader(path)
            return "\n".join(p.extract_text() or "" for p in reader.pages)
        except ImportError:
            return f"[错误] 请安装 pdfplumber: pip install pdfplumber\n文件路径: {path}"

def parse_docx(path):
    try:
        from docx import Document
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    except ImportError:
        return f"[错误] 请安装 python-docx: pip install python-docx\n文件路径: {path}"

def parse_file(path):
    ext = os.path.splitext(path)[1].lower()
    if not os.path.exists(path):
        return f"[错误] 文件不存在: {path}"
    if ext == ".pdf":
        return parse_pdf(path)
    elif ext in (".docx", ".doc"):
        return parse_docx(path)
    elif ext in (".txt", ".md", ".markdown"):
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read()
    else:
        # 尝试直接读取
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            return f"[错误] 无法读取文件: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 parse_file.py <文件路径>")
        sys.exit(1)
    print(parse_file(sys.argv[1]))
