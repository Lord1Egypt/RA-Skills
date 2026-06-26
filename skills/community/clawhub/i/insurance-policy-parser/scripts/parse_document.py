#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
保险条款文档解析脚本

支持解析PDF、DOCX、TXT格式的文档，提取纯文本内容
"""

import sys
import os
from pathlib import Path


def parse_pdf(file_path: str) -> str:
    """解析PDF文件，提取文本内容"""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        raise ImportError("请先安装 PyPDF2: pip install PyPDF2==3.0.1")
    
    reader = PdfReader(file_path)
    text_content = []
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_content.append(text)
    
    return "\n\n".join(text_content)


def parse_docx(file_path: str) -> str:
    """解析DOCX文件，提取文本内容"""
    try:
        from docx import Document
    except ImportError:
        raise ImportError("请先安装 python-docx: pip install python-docx==1.1.0")
    
    doc = Document(file_path)
    text_content = []
    
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text_content.append(paragraph.text)
    
    return "\n".join(text_content)


def parse_txt(file_path: str) -> str:
    """解析TXT文件，提取文本内容"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    raise ValueError(f"无法解码文件: {file_path}")


def main():
    """主函数：解析文档并输出文本内容"""
    if len(sys.argv) != 2:
        print("用法: python parse_document.py <file_path>", file=sys.stderr)
        print("支持的格式: PDF, DOCX, TXT", file=sys.stderr)
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在 - {file_path}", file=sys.stderr)
        sys.exit(1)
    
    # 获取文件扩展名
    file_ext = Path(file_path).suffix.lower()
    
    try:
        # 根据文件类型选择解析方法
        if file_ext == '.pdf':
            text = parse_pdf(file_path)
        elif file_ext == '.docx':
            text = parse_docx(file_path)
        elif file_ext == '.txt':
            text = parse_txt(file_path)
        else:
            print(f"错误: 不支持的文件格式 - {file_ext}", file=sys.stderr)
            print("支持的格式: .pdf, .docx, .txt", file=sys.stderr)
            sys.exit(1)
        
        # 输出文本内容
        print(text)
        
    except Exception as e:
        print(f"解析失败: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
