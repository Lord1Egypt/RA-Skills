#!/usr/bin/env python3
"""
PDF 转换工具 - 快速将 PDF 转为 PPTX 或 Word

用法:
    pdf2pptx file.pdf [max_size_mb]  # 转为 PPTX
    pdf2docx file.pdf [max_size_mb]  # 转为 Word
"""

import sys
import os

# 添加技能目录到路径
skill_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, skill_dir)

from scripts.convert import PDFConverter

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print(f"  {sys.argv[0]} file.pdf [max_size_mb]  # 转为 PPTX")
        print(f"  {sys.argv[0]} file.docx [max_size_mb]  # 转为 Word")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    max_size = float(sys.argv[2]) if len(sys.argv) > 2 else 30
    
    # 确定输出格式
    output_format = 'docx' if 'docx' in sys.argv[0] else 'pptx'
    
    converter = PDFConverter(max_size_mb=max_size)
    success = converter.convert(pdf_file, output_format)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
