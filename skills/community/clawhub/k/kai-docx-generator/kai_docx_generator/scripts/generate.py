#!/usr/bin/env python3
"""CLI: Markdown → .docx 新建模式"""

import argparse
import sys
import os

# Ensure parent directory is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from kai_docx_generator.parser.md_to_ast import parse_markdown_to_docspec
from kai_docx_generator.engine.docx_engine import DocxEngine
from kai_docx_generator.styles.standard import STANDARD_CONFIG

KNOWN_STYLES = {"standard"}


def main():
    parser = argparse.ArgumentParser(
        description="将 Markdown 文件转换为 .docx 文档"
    )
    parser.add_argument("input", help="输入 Markdown 文件路径")
    parser.add_argument("output", help="输出 .docx 文件路径")
    parser.add_argument(
        "--style", default="standard",
        help="Style 预设名称（默认: standard）"
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    output_dir = os.path.dirname(os.path.abspath(args.output))
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(args.input, "r", encoding="utf-8") as f:
        markdown = f.read()

    if args.style not in KNOWN_STYLES:
        print(f"错误: 未知的 Style 预设: {args.style}，支持的有: {', '.join(sorted(KNOWN_STYLES))}", file=sys.stderr)
        sys.exit(1)

    spec = parse_markdown_to_docspec(markdown)
    engine = DocxEngine(style_config=STANDARD_CONFIG)
    doc = engine.generate_from_spec(spec)
    doc.save(args.output)

    print(f"已生成: {args.output}")


if __name__ == "__main__":
    main()
