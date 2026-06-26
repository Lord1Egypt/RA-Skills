#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成可预览和复制的HTML文件
功能：
1. 生成包含样式的完整HTML文档
2. 可在浏览器中直接预览最终效果
3. 内容可直接复制到微信公众号编辑器
4. 保留所有样式和格式

使用方法：
python scripts/generate_preview_html.py <markdown文件路径>
python scripts/generate_preview_html.py 美化文章_睡眠重要性_男编辑版_20250115.md
"""

import os
import sys
from pathlib import Path


def generate_preview_html(md_path):
    """生成预览HTML文件"""

    md_path = Path(md_path)
    if not md_path.exists():
        print(f"错误: 文件不存在 - {md_path}")
        return False

    # 读取Markdown内容
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception as e:
        print(f"错误: 读取文件失败 - {e}")
        return False

    # 提取标题（第一行#开头的）
    title = "文章预览"
    for line in md_content.split('\n'):
        if line.startswith('#'):
            title = line.lstrip('#').strip()
            break

    # 读取HTML模板
    template_path = Path(__file__).parent / 'html_template.html'
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        print(f"错误: 读取模板失败 - {e}")
        return False

    # 转换Markdown到HTML（使用现有的转换器）
    from convert_to_html import MarkdownToHTMLConverter

    converter = MarkdownToHTMLConverter(md_content)
    html_body = converter.convert()

    # 替换模板中的标题和内容
    html_doc = template.replace('<title>微信公众号文章预览</title>', f'<title>{title}</title>')
    html_doc = html_doc.replace('<!-- 文章内容将在这里生成 -->', html_body)

    # 生成输出文件名
    output_path = md_path.with_suffix('.html')

    # 写入文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_doc)
        print(f"成功: 已生成预览HTML文件 - {output_path}")
        print(f"提示: 可在浏览器中打开查看效果，或直接复制内容到微信公众号编辑器")
        return True
    except Exception as e:
        print(f"错误: 写入文件失败 - {e}")
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python scripts/generate_preview_html.py <markdown文件路径>")
        print("示例: python scripts/generate_preview_html.py 美化文章_睡眠重要性_男编辑版_20250115.md")
        sys.exit(1)

    md_path = sys.argv[1]
    success = generate_preview_html(md_path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
