#!/usr/bin/env python3
"""
使用 markitdown 转换单个文件为 Markdown

要求: Python 3.10+
使用方法: python3.12 scripts/convert.py input.pdf output.md
"""

import argparse
import sys
from pathlib import Path

# 检查 Python 版本
if sys.version_info < (3, 10):
    print(f"错误: 需要 Python 3.10 或更高版本，当前版本: {sys.version}")
    print("请使用 python3.12, python3.11 或 python3.13 运行此脚本")
    print("示例: python3.12 scripts/convert.py input.pdf output.md")
    sys.exit(1)

try:
    from markitdown import MarkItDown
except ImportError:
    print("错误: 未安装 markitdown 库")
    print("请使用虚拟环境安装: python3.12 -m venv markitdown-env")
    print("然后激活虚拟环境并安装 markitdown: source markitdown-env/bin/activate && pip install \"markitdown[all]\"")
    sys.exit(1)


def convert_file(input_path: str, output_path: str = None):
    """
    转换单个文件为 Markdown
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径（可选）
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        print(f"错误: 文件不存在: {input_path}")
        return False
    
    if not input_path.is_file():
        print(f"错误: 不是文件: {input_path}")
        return False
    
    # 如果没有指定输出路径，使用输入文件名 + .md
    if output_path is None:
        output_path = input_path.with_suffix(".md")
    else:
        output_path = Path(output_path)
    
    print(f"正在转换: {input_path} -> {output_path}")
    
    try:
        md = MarkItDown()
        result = md.convert(str(input_path))
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.text_content)
        
        print(f"转换成功: {output_path}")
        return True
        
    except Exception as e:
        print(f"转换失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="使用 markitdown 转换文件为 Markdown"
    )
    parser.add_argument("input_file", help="输入文件路径")
    parser.add_argument("output_file", nargs="?", help="输出文件路径（可选）")
    
    args = parser.parse_args()
    
    success = convert_file(args.input_file, args.output_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
