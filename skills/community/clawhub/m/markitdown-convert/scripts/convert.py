#!/usr/bin/env python3
"""
MarkItDown 文档转换脚本
将各种格式文件（PDF/DOCX/XLSX/PPTX/图片等）转换为 Markdown
"""

import argparse
import sys
import os
from pathlib import Path


def check_markitdown():
    """检查 markitdown 是否已安装"""
    try:
        from markitdown import MarkItDown
        return True
    except ImportError:
        return False


def convert_file(input_path: str, output_path: str = None, use_plugins: bool = False) -> str:
    """
    转换文件为 Markdown
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径（可选，默认输出到 stdout）
        use_plugins: 是否启用插件
    
    Returns:
        Markdown 内容
    """
    if not check_markitdown():
        print("Error: markitdown not installed. Run: pip install 'markitdown[all]'", file=sys.stderr)
        sys.exit(1)
    
    from markitdown import MarkItDown
    
    input_file = Path(input_path)
    if not input_file.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        md = MarkItDown(enable_plugins=use_plugins)
        result = md.convert(str(input_file))
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.text_content)
            print(f"Converted: {input_path} -> {output_path}")
        else:
            print(result.text_content)
        
        return result.text_content
    except Exception as e:
        print(f"Error converting {input_path}: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Convert various file formats to Markdown using Microsoft MarkItDown'
    )
    parser.add_argument('input', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path (default: stdout)')
    parser.add_argument('--plugins', action='store_true', help='Enable plugins')
    
    args = parser.parse_args()
    convert_file(args.input, args.output, args.plugins)


if __name__ == '__main__':
    main()
