#!/usr/bin/env python3
"""
PDF 转 Word 转换器
接收一个 PDF 文件路径，生成同名的 .docx 文件。
"""

import os
import sys
import argparse
from pdf2docx import Converter

def pdf_to_word(pdf_path, output_path=None):
    """
    将 PDF 转换为 Word
    :param pdf_path: 输入 PDF 文件路径
    :param output_path: 输出 Word 文件路径，如果为 None 则自动生成
    :return: 输出文件路径
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF 文件不存在: {pdf_path}")
    
    if output_path is None:
        output_path = os.path.splitext(pdf_path)[0] + ".docx"
    
    # 执行转换
    cv = Converter(pdf_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()
    return output_path

def main():
    parser = argparse.ArgumentParser(description="PDF 转 Word 工具")
    parser.add_argument("--input", required=True, help="输入 PDF 文件路径")
    parser.add_argument("--output", help="输出 Word 文件路径（可选）")
    args = parser.parse_args()
    
    try:
        out_path = pdf_to_word(args.input, args.output)
        # OpenClaw 会捕获 stdout，我们输出结果文件的路径或内容
        # 这里输出文件路径，OpenClaw 可以根据配置处理文件返回
        print(f"转换成功！输出文件：{out_path}")
        # 如果需要直接返回文件内容，可以打印文件的 base64 编码等，但通常返回路径更方便
    except Exception as e:
        print(f"转换失败：{str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()