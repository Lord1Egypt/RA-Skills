#!/usr/bin/env python3
"""
多模态数据处理器
支持：PDF/Word/图片/文字输入
"""

import os
import re
import json
from pathlib import Path

# 尝试导入需要的库
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


def extract_from_docx(file_path):
    """从Word文档提取文本"""
    if not DOCX_AVAILABLE:
        return {"success": False, "error": "请安装 python-docx: pip install python-docx"}
    
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return {"success": True, "text": text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def extract_from_image(image_path):
    """从图片提取文字（OCR）"""
    if not PYTESSERACT_AVAILABLE:
        return {"success": False, "error": "请安装 pytesseract 和 tesseract"}
    
    try:
        # 使用pytesseract进行OCR
        text = pytesseract.image_to_string(image_path, lang='chi_sim+eng')
        return {"success": True, "text": text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def extract_from_pdf_images(pdf_path):
    """从PDF提取图片（先转图片再OCR）"""
    if not PDF2IMAGE_AVAILABLE:
        return {"success": False, "error": "请安装 pdf2image: pip install pdf2image"}
    
    if not PYTESSERACT_AVAILABLE:
        return {"success": False, "error": "请安装 pytesseract"}
    
    try:
        # PDF转图片
        images = convert_from_path(pdf_path)
        
        all_text = ""
        for i, image in enumerate(images):
            # 对每页进行OCR
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            all_text += f"\n--- 第{i+1}页 ---\n" + text
        
        return {"success": True, "text": all_text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def detect_file_type(file_path):
    """检测文件类型"""
    ext = os.path.splitext(file_path)[1].lower()
    
    type_mapping = {
        ".pdf": "pdf",
        ".docx": "word",
        ".doc": "word",
        ".jpg": "image",
        ".jpeg": "image",
        ".png": "image",
        ".gif": "image",
        ".bmp": "image"
    }
    
    return type_mapping.get(ext, "unknown")


def process_file(file_path):
    """根据文件类型处理"""
    file_type = detect_file_type(file_path)
    
    if file_type == "pdf":
        # 尝试直接文本提取，失败则用OCR
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            if text.strip():
                return {"success": True, "text": text, "method": "pdf_text"}
        except:
            pass
        
        # 尝试OCR
        return extract_from_pdf_images(file_path)
    
    elif file_type == "word":
        return extract_from_docx(file_path)
    
    elif file_type == "image":
        return extract_from_image(file_path)
    
    else:
        return {"success": False, "error": f"不支持的文件类型: {file_type}"}


if __name__ == "__main__":
    # 测试
    print("=== 多模态数据处理器 ===")
    print(f"PDF转图片: {'可用' if PDF2IMAGE_AVAILABLE else '不可用'}")
    print(f"OCR(pytesseract): {'可用' if PYTESSERACT_AVAILABLE else '不可用'}")
    print(f"Word解析: {'可用' if DOCX_AVAILABLE else '不可用'}")
    
    print("\n支持的文件类型：PDF, Word(.docx), 图片(jpg/png)")