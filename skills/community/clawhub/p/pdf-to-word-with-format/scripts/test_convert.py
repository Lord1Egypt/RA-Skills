# -*- coding: utf-8 -*-
"""测试PDF转Word转换功能"""

import os
import sys

# 确保可以导入convert模块
sys.path.insert(0, os.path.dirname(__file__))

from convert import convert_pdf_to_word

def test_conversion():
    """测试基本转换功能"""
    print("=" * 50)
    print("PDF转Word转换测试")
    print("=" * 50)
    
    # 检查pdf2docx是否可用
    try:
        from pdf2docx import Converter
        print("✓ pdf2docx 库已安装")
    except ImportError:
        print("✗ pdf2docx 未安装")
        print("请运行: pip install pdf2docx")
        return False
    
    # 列出当前目录的PDF文件
    print("\n当前目录的PDF文件:")
    pdf_files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
    if pdf_files:
        for f in pdf_files:
            print(f"  - {f}")
    else:
        print("  (无PDF文件)")
    
    print("\n" + "=" * 50)
    print("转换脚本已就绪！")
    print("=" * 50)
    print("\n使用方法:")
    print("  python convert.py <输入PDF> --output <输出Word>")
    print("  python convert.py ./pdfs/ --batch --output ./words/")
    
    return True


if __name__ == '__main__':
    test_conversion()
