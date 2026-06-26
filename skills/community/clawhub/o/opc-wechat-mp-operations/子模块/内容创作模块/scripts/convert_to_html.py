#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown转HTML转换工具（增强版）
功能：
1. 将Markdown文件转换为HTML格式
2. 支持表格转换（Markdown表格语法 → HTML表格）
3. 保留样式和图片
4. 确保微信公众号兼容
5. 支持中文字符

使用方法：
python scripts/convert_to_html.py <markdown文件路径> [输出路径]
python scripts/convert_to_html.py 美化文章_睡眠重要性.md
python scripts/convert_to_html.py 美化文章_睡眠重要性.md 输出目录/
"""

import os
import sys
import re
from pathlib import Path
import html


class MarkdownToHTMLConverter:
    """Markdown转HTML转换器（增强版）"""

    def __init__(self, md_content):
        self.md_content = md_content
        self.html_content = ""

    def escape_html(self, text):
        """转义HTML特殊字符"""
        return html.escape(text)

    def convert_tables(self, text):
        """
        转换表格语法
        Markdown表格语法：
        | 列1 | 列2 | 列3 |
        | --- | --- | --- |
        | 数据1 | 数据2 | 数据3 |
        转换为HTML表格
        """
        lines = text.split('\n')
        result = []
        in_table = False
        header_parsed = False
        table_rows = []

        for line in lines:
            # 检测表格开始（包含|符号）
            if '|' in line and line.strip().startswith('|'):
                if not in_table:
                    in_table = True
                    header_parsed = False
                    table_rows = []

                # 清理行内容
                cells = [cell.strip() for cell in line.split('|')]
                # 移除首尾空元素
                if cells and cells[0] == '':
                    cells.pop(0)
                if cells and cells[-1] == '':
                    cells.pop()

                # 检测分隔行（包含---）
                if any('---' in cell for cell in cells):
                    # 这是分隔行，标记表头已解析
                    if table_rows:
                        # 生成表头
                        header_row = table_rows[-1]
                        table_rows.pop()
                        result.append('<table class="data-table">')
                        result.append('<thead>')
                        result.append('<tr>')
                        for cell in header_row:
                            result.append(f'<th>{cell}</th>')
                        result.append('</tr>')
                        result.append('</thead>')
                        result.append('<tbody>')
                        header_parsed = True
                else:
                    # 普通行
                    table_rows.append(cells)
            else:
                # 非表格行
                if in_table:
                    # 结束表格
                    if table_rows:
                        # 生成表格内容
                        for row in table_rows:
                            result.append('<tr>')
                            for cell in row:
                                result.append(f'<td>{cell}</td>')
                            result.append('</tr>')
                    if header_parsed:
                        result.append('</tbody>')
                    else:
                        # 没有分隔行的简单表格
                        if table_rows:
                            result.append('<table class="data-table">')
                            result.append('<tbody>')
                            for row in table_rows:
                                result.append('<tr>')
                                for cell in row:
                                    result.append(f'<td>{cell}</td>')
                                result.append('</tr>')
                            result.append('</tbody>')
                    result.append('</table>')
                    in_table = False
                    table_rows = []
                    header_parsed = False

                result.append(line)

        # 处理文件末尾的表格
        if in_table:
            if table_rows:
                for row in table_rows:
                    result.append('<tr>')
                    for cell in row:
                        result.append(f'<td>{cell}</td>')
                    result.append('</tr>')
            if header_parsed:
                result.append('</tbody>')
            result.append('</table>')

        return '\n'.join(result)

    def convert_images(self, text):
        """转换图片语法"""
        # Markdown图片: ![alt](url)
        # 转换为HTML: <img src="url" alt="alt" />
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

        def replace_image(match):
            alt = match.group(1)
            url = match.group(2).strip()
            # 确保URL不为空
            if not url or '占位符' in url or 'placeholder' in url.lower():
                return f'<div class="image-placeholder">[图片: {alt}]</div>'
            return f'<img src="{url}" alt="{alt}" />'

        return re.sub(pattern, replace_image, text)

    def convert_links(self, text):
        """转换链接语法"""
        # Markdown链接: [text](url)
        # 转换为HTML: <a href="url">text</a>
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'

        def replace_link(match):
            text = match.group(1)
            url = match.group(2).strip()
            return f'<a href="{url}">{text}</a>'

        return re.sub(pattern, replace_link, text)

    def convert_headers(self, text):
        """转换标题"""
        lines = text.split('\n')
        result = []

        for line in lines:
            # 跳过表格内容（已转换为HTML）
            if '<table' in line or '<tr' in line or '<th' in line or '<td' in line:
                result.append(line)
                continue

            # H1: # 标题
            if line.startswith('# '):
                content = line[2:].strip()
                result.append(f'<h1>{content}</h1>')
            # H2: ## 标题
            elif line.startswith('## '):
                content = line[3:].strip()
                result.append(f'<h2>{content}</h2>')
            # H3: ### 标题
            elif line.startswith('### '):
                content = line[4:].strip()
                result.append(f'<h3>{content}</h3>')
            # H4: #### 标题
            elif line.startswith('#### '):
                content = line[5:].strip()
                result.append(f'<h4>{content}</h4>')
            else:
                result.append(line)

        return '\n'.join(result)

    def convert_emphasis(self, text):
        """转换强调语法"""
        # **bold**
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # *italic*
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        return text

    def convert_lists(self, text):
        """转换列表"""
        lines = text.split('\n')
        result = []
        in_ul = False
        in_ol = False

        for line in lines:
            # 跳过表格内容
            if '<table' in line or '</table' in line:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                result.append(line)
                continue

            # 无序列表
            if re.match(r'^[\-\*]\s+', line):
                if not in_ul:
                    if in_ol:
                        result.append('</ol>')
                        in_ol = False
                    result.append('<ul>')
                    in_ul = True
                content = re.sub(r'^[\-\*]\s+', '', line)
                result.append(f'<li>{content}</li>')
            # 有序列表
            elif re.match(r'^\d+\.\s+', line):
                if not in_ol:
                    if in_ul:
                        result.append('</ul>')
                        in_ul = False
                    result.append('<ol>')
                    in_ol = True
                content = re.sub(r'^\d+\.\s+', '', line)
                result.append(f'<li>{content}</li>')
            else:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                result.append(line)

        # 关闭未关闭的标签
        if in_ul:
            result.append('</ul>')
        if in_ol:
            result.append('</ol>')

        return '\n'.join(result)

    def convert_blockquotes(self, text):
        """转换引用块"""
        lines = text.split('\n')
        result = []
        in_quote = False

        for line in lines:
            # 跳过表格内容
            if '<table' in line or '</table' in line:
                if in_quote:
                    result.append('</blockquote>')
                    in_quote = False
                result.append(line)
                continue

            if line.startswith('>'):
                if not in_quote:
                    in_quote = True
                    result.append('<blockquote>')
                content = line[1:].strip()
                if content:
                    result.append(f'<p>{content}</p>')
            else:
                if in_quote:
                    result.append('</blockquote>')
                    in_quote = False
                result.append(line)

        if in_quote:
            result.append('</blockquote>')

        return '\n'.join(result)

    def convert_html_blocks(self, text):
        """保留HTML块（div, style等）"""
        # 不处理已经存在的HTML标签
        return text

    def convert_div_blocks(self, text):
        """处理div块"""
        # 保留现有的div标签
        return text

    def convert_horizontal_rules(self, text):
        """转换分隔线"""
        # --- 或 ***
        text = re.sub(r'^[\-\*]{3,}$', '<hr />', text, flags=re.MULTILINE)
        return text

    def wrap_paragraphs(self, text):
        """包裹段落"""
        lines = text.split('\n')
        result = []
        paragraph_content = []

        for line in lines:
            stripped = line.strip()

            # 跳过空行和特殊标签
            if not stripped:
                if paragraph_content:
                    result.append('<p>' + ''.join(paragraph_content) + '</p>')
                    paragraph_content = []
                continue

            # 跳过自闭合标签和块级元素
            skip_tags = ['<h1', '<h2', '<h3', '<h4', '<ul', '<ol', '<li',
                        '<blockquote', '</blockquote', '<hr', '<img', '<div', '</div', '<p',
                        '<table', '</table', '<thead', '</thead', '<tbody', '</tbody', '<tr', '</tr', '<th', '</th', '<td', '</td']
            if any(stripped.startswith(tag) for tag in skip_tags):
                if paragraph_content:
                    result.append('<p>' + ''.join(paragraph_content) + '</p>')
                    paragraph_content = []
                result.append(stripped)
            else:
                paragraph_content.append(stripped)

        # 处理最后的段落
        if paragraph_content:
            result.append('<p>' + ''.join(paragraph_content) + '</p>')

        return '\n'.join(result)

    def convert(self):
        """执行转换"""
        text = self.md_content

        # 1. 先转换HTML块（不处理）
        text = self.convert_html_blocks(text)

        # 2. 转换表格（在标题之前）
        text = self.convert_tables(text)

        # 3. 转换标题
        text = self.convert_headers(text)

        # 4. 转换分隔线
        text = self.convert_horizontal_rules(text)

        # 5. 转换引用块
        text = self.convert_blockquotes(text)

        # 6. 转换列表
        text = self.convert_lists(text)

        # 7. 转换图片（必须在链接之前）
        text = self.convert_images(text)

        # 8. 转换链接
        text = self.convert_links(text)

        # 9. 转换强调
        text = self.convert_emphasis(text)

        # 10. 包裹段落
        text = self.wrap_paragraphs(text)

        # 11. 处理div块（确保正确闭合）
        text = self.convert_div_blocks(text)

        self.html_content = text
        return text

    def generate_html_document(self, title="微信公众号文章"):
        """生成完整的HTML文档"""
        html_body = self.convert()

        html_doc = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.8;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
        }}
        h1 {{
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            margin: 30px 0;
            color: #1a1a1a;
        }}
        h2 {{
            font-size: 22px;
            font-weight: bold;
            margin: 25px 0 15px 0;
            color: #333;
        }}
        h3 {{
            font-size: 18px;
            font-weight: bold;
            margin: 20px 0 10px 0;
            color: #555;
        }}
        p {{
            margin: 15px 0;
            text-align: justify;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border-radius: 8px;
        }}
        .image-placeholder {{
            background-color: #f5f5f5;
            padding: 30px;
            text-align: center;
            border-radius: 8px;
            color: #999;
            margin: 20px 0;
        }}
        blockquote {{
            background-color: #f9f9f9;
            border-left: 4px solid #ddd;
            padding: 15px 20px;
            margin: 20px 0;
        }}
        blockquote p {{
            margin: 5px 0;
        }}
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 8px 0;
        }}
        hr {{
            border: none;
            height: 1px;
            background: linear-gradient(to right, transparent, #ddd, transparent);
            margin: 30px 0;
        }}
        a {{
            color: #007bff;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        strong {{
            font-weight: bold;
            color: #1a1a1a;
        }}
        em {{
            font-style: italic;
        }}
        .highlight {{
            background-color: #f0f9ff;
            padding: 15px;
            border-left: 4px solid #3b82f6;
            margin: 15px 0;
            border-radius: 0 8px 8px 0;
        }}
        .warning {{
            background-color: #fffbeb;
            padding: 15px;
            border-left: 4px solid #f59e0b;
            margin: 15px 0;
            border-radius: 0 8px 8px 0;
        }}
        .success {{
            background-color: #f0fdf4;
            padding: 15px;
            border-left: 4px solid #10b981;
            margin: 15px 0;
            border-radius: 0 8px 8px 0;
        }}
        .interaction {{
            background-color: #f9fafb;
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
            text-align: center;
        }}
        /* 表格样式 */
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: #fff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .data-table thead {{
            background-color: #f8f9fa;
        }}
        .data-table th {{
            padding: 12px 15px;
            text-align: left;
            font-weight: bold;
            color: #333;
            border-bottom: 2px solid #dee2e6;
        }}
        .data-table td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }}
        .data-table tbody tr:hover {{
            background-color: #f8f9fa;
        }}
        .data-table tbody tr:last-child td {{
            border-bottom: none;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>'''

        return html_doc


def convert_file(input_path, output_path=None):
    """转换文件"""
    input_path = Path(input_path)

    if not input_path.exists():
        print(f"错误: 文件不存在 - {input_path}")
        return False

    # 读取Markdown文件
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception as e:
        print(f"错误: 读取文件失败 - {e}")
        return False

    # 转换
    converter = MarkdownToHTMLConverter(md_content)

    # 确定输出路径
    if output_path is None:
        output_path = input_path.with_suffix('.html')
    else:
        output_path = Path(output_path)
        if output_path.is_dir():
            output_path = output_path / input_path.with_suffix('.html').name

    # 生成HTML
    # 从文件名提取标题
    title = input_path.stem.replace('_', ' ')
    html_content = converter.generate_html_document(title)

    # 写入文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"成功: 已转换为 {output_path}")
        return True
    except Exception as e:
        print(f"错误: 写入文件失败 - {e}")
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python scripts/convert_to_html.py <markdown文件路径> [输出路径]")
        print("示例: python scripts/convert_to_html.py 美化文章_睡眠重要性.md")
        print("示例: python scripts/convert_to_html.py 美化文章_睡眠重要性.md 输出目录/")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    success = convert_file(input_path, output_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
