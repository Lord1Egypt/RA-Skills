#!/usr/bin/env python3
"""
OCR 关键词标注与 Word 格式转换辅助脚本
功能：将提取的文字中的关键词加粗，并生成可用于 Word 的格式
用法：python format_output.py --input input.txt --keywords "关键词1,关键词2" --output output.txt
"""

import argparse
import sys
import re


def parse_arguments():
    parser = argparse.ArgumentParser(description="OCR 文字关键词加粗工具")
    parser.add_argument("--input", "-i", required=True, help="输入的纯文本文件路径")
    parser.add_argument("--keywords", "-k", required=True, help="关键词列表，用逗号或空格分隔")
    parser.add_argument("--output", "-o", required=True, help="输出文件路径")
    return parser.parse_args()


def load_text(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def bold_keywords(text, keywords):
    """将文本中的关键词加粗（Markdown 格式）"""
    # 按长度降序排序，避免短词先匹配导致长词无法匹配
    keywords_sorted = sorted(keywords, key=len, reverse=True)
    
    # 转义特殊字符
    escaped_keywords = [re.escape(kw) for kw in keywords_sorted]
    pattern = "|".join(escaped_keywords)
    
    # 使用正则替换，加粗匹配的关键词
    def replace_with_bold(match):
        return f"**{match.group(0)}**"
    
    result = re.sub(pattern, replace_with_bold, text, flags=re.IGNORECASE)
    return result


def save_text(filepath, content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    args = parse_arguments()
    
    # 解析关键词
    keywords = re.split(r"[,，\s]+", args.keywords.strip())
    keywords = [kw.strip() for kw in keywords if kw.strip()]
    
    print(f"📖 加载文本: {args.input}")
    print(f"🔑 关键词: {', '.join(keywords)}")
    
    text = load_text(args.input)
    
    # 执行加粗
    result = bold_keywords(text, keywords)
    
    # 统计
    count = sum(1 for _ in re.finditer("|".join(map(re.escape, keywords)), text, re.IGNORECASE))
    print(f"✅ 共标注 {count} 个关键词匹配项")
    
    save_text(args.output, result)
    print(f"💾 输出已保存至: {args.output}")
    
    # 提示 Word 转换方法
    print("\n📌 将 Markdown 转换为 Word 的方法：")
    print("  1. 将输出内容粘贴到 Word，使用 'Ctrl+B' 手动加粗")
    print("  2. 或使用 Pandoc: pandoc output.txt -o output.docx")
    print("  3. 或将 Markdown 粘贴到 Typora 等编辑器导出为 Word")


if __name__ == "__main__":
    main()