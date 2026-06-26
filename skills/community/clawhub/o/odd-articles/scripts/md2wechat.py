#!/usr/bin/env python3
"""
Markdown 转 HTML 工具 (基于 baoyu-markdown-to-html 设计)

功能：将 Markdown 格式转换为微信公众号优化的 HTML 格式
- 支持多种主题（default, grace, simple）
- 支持 frontmatter 元数据
- 支持表格、代码块、脚注、警告框
- ASCII 架构图横向滚动
- 移动端适配
"""

import argparse
import json
import markdown
import re
import sys
from datetime import datetime
from pathlib import Path

# 经典主题（默认）
THEME_DEFAULT = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 16px;
            line-height: 1.8;
            color: #333333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #ffffff;
        }}
        h1 {{
            font-size: 24px;
            font-weight: 600;
            margin: 24px 0 16px;
            color: #1a1a1a;
            text-align: center;
            border-bottom: 2px solid #007aff;
            padding-bottom: 12px;
        }}
        h2 {{
            font-size: 20px;
            font-weight: 600;
            margin: 24px 0 12px;
            color: #ffffff;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 8px 16px;
            border-radius: 4px;
        }}
        h3 {{
            font-size: 18px;
            font-weight: 600;
            margin: 20px 0 10px;
            color: #333333;
        }}
        p {{
            margin: 16px 0;
            line-height: 1.8;
            color: #333333;
        }}
        ul, ol {{
            padding-left: 24px;
            margin: 16px 0;
        }}
        li {{
            margin: 8px 0;
            line-height: 1.7;
        }}
        strong {{
            font-weight: 600;
            color: #1a1a1a;
        }}
        hr {{
            border: none;
            border-top: 1px solid #eeeeee;
            margin: 24px 0;
        }}
        blockquote {{
            border-left: 4px solid #007aff;
            padding: 12px 16px;
            margin: 16px 0;
            background: #f0f7ff;
            color: #333333;
        }}
        pre {{
            background: #f6f8fa;
            padding: 16px;
            border-radius: 4px;
            overflow-x: auto;
            overflow-y: hidden;
            white-space: pre;
            -webkit-overflow-scrolling: touch;
            margin: 16px 0;
            font-family: "Menlo", "Monaco", "Consolas", monospace;
            font-size: 13px;
            line-height: 1.5;
        }}
        code {{
            font-family: "Menlo", "Monaco", "Consolas", monospace;
            font-size: 13px;
            background: #f6f8fa;
            padding: 2px 6px;
            border-radius: 4px;
            color: #d73a49;
        }}
        pre code {{
            background: none;
            padding: 0;
            color: inherit;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 16px auto;
            border-radius: 4px;
        }}
        a {{
            color: #007aff;
            text-decoration: none;
        }}
        .table-wrapper {{
            overflow-x: auto;
            margin: 16px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        th, td {{
            border: 1px solid #eeeeee;
            padding: 10px 12px;
            text-align: left;
        }}
        th {{
            background: #f6f8fa;
            font-weight: 600;
        }}
        /* 警告框 */
        .alert {{
            padding: 12px 16px;
            margin: 16px 0;
            border-radius: 4px;
        }}
        .alert-note {{
            background: #e7f3ff;
            border-left: 4px solid #007aff;
        }}
        .alert-warning {{
            background: #fff8e6;
            border-left: 4px solid #ff9500;
        }}
        .alert-tip {{
            background: #e6fff2;
            border-left: 4px solid #34c759;
        }}
        .alert-important {{
            background: #fff2f2;
            border-left: 4px solid #ff3b30;
        }}
        .author {{
            color: #999999;
            font-size: 14px;
            text-align: center;
            margin-top: 32px;
            padding-top: 16px;
            border-top: 1px solid #eeeeee;
        }}
    </style>
</head>
<body>
{content}
<div class="author">{author}</div>
</body>
</html>"""

# 简洁主题
THEME_SIMPLE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 16px;
            line-height: 1.9;
            color: #2c3e50;
            max-width: 720px;
            margin: 0 auto;
            padding: 32px 20px;
            background: #fafafa;
        }}
        h1 {{
            font-size: 26px;
            font-weight: 700;
            margin: 0 0 24px;
            color: #1a1a1a;
        }}
        h2 {{
            font-size: 20px;
            font-weight: 600;
            margin: 32px 0 16px;
            color: #1a1a1a;
        }}
        p {{
            margin: 16px 0;
            color: #4a4a4a;
        }}
        ul, ol {{
            padding-left: 20px;
            margin: 16px 0;
        }}
        pre {{
            background: #282c34;
            color: #abb2bf;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            white-space: pre;
            margin: 20px 0;
        }}
        blockquote {{
            border-left: 3px solid #3498db;
            padding: 8px 16px;
            margin: 16px 0;
            color: #666;
        }}
        .author {{
            color: #999;
            font-size: 14px;
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
        }}
    </style>
</head>
<body>
{content}
<div class="author">{author}</div>
</body>
</html>"""

# 优雅主题
THEME_GRACE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
            font-size: 16px;
            line-height: 2.0;
            color: #444;
            max-width: 760px;
            margin: 0 auto;
            padding: 24px;
            background: linear-gradient(135deg, #667eea08 0%, #764ba208 100%);
        }}
        .card {{
            background: #ffffff;
            border-radius: 16px;
            padding: 32px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            margin: 16px 0;
        }}
        h1 {{
            font-size: 24px;
            font-weight: 600;
            margin: 0 0 24px;
            text-align: center;
            color: #1a1a1a;
        }}
        h2 {{
            font-size: 18px;
            font-weight: 600;
            margin: 24px 0 12px;
            color: #5e6ad2;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }}
        p {{
            margin: 14px 0;
            color: #555;
        }}
        pre {{
            background: #f8f9fa;
            padding: 16px;
            border-radius: 12px;
            overflow-x: auto;
            white-space: pre;
            margin: 16px 0;
            border: 1px solid #eee;
        }}
        blockquote {{
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
            border-radius: 12px;
            padding: 16px 20px;
            margin: 16px 0;
            border: none;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
        }}
        .author {{
            color: #999;
            font-size: 14px;
            text-align: center;
            margin-top: 32px;
        }}
    </style>
</head>
<body>
<div class="card">
{content}
</div>
<div class="author">{author}</div>
</body>
</html>"""

# oddmeta 主题（墨绿 + 鱼红 + 宣纸底）
THEME_ODD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
            font-size: 16px;
            line-height: 1.9;
            color: #333333;
            max-width: 720px;
            margin: 0 auto;
            padding: 24px 20px;
            background: #F2EDE3;
        }}
        h1 {{
            font-size: 24px;
            font-weight: 700;
            margin: 24px 0 20px;
            text-align: center;
            color: #1A3328;
        }}
        h2 {{
            font-size: 18px;
            font-weight: 600;
            margin: 28px 0 14px;
            color: #1A3328;
            border-left: 4px solid #C44536;
            padding-left: 12px;
        }}
        h3 {{
            font-size: 16px;
            font-weight: 600;
            margin: 20px 0 10px;
            color: #1A3328;
        }}
        p {{
            margin: 14px 0;
            color: #333333;
        }}
        ul, ol {{
            padding-left: 24px;
            margin: 14px 0;
        }}
        li {{
            margin: 8px 0;
            line-height: 1.7;
        }}
        strong {{
            font-weight: 600;
            color: #C44536;
        }}
        hr {{
            border: none;
            border-top: 1px solid #D4DDD7;
            margin: 28px 0;
        }}
        blockquote {{
            border-left: 3px solid #C44536;
            padding: 12px 16px;
            margin: 16px 0;
            background: #ffffff;
            color: #555555;
            border-radius: 0 4px 4px 0;
        }}
        pre {{
            background: #1A3328;
            color: #D4DDD7;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            overflow-y: hidden;
            white-space: pre;
            -webkit-overflow-scrolling: touch;
            margin: 16px 0;
            font-family: "Menlo", "Monaco", "Consolas", monospace;
            font-size: 13px;
            line-height: 1.5;
        }}
        code {{
            font-family: "Menlo", "Monaco", "Consolas", monospace;
            font-size: 13px;
            background: #1A3328;
            color: #D4DDD7;
            padding: 2px 6px;
            border-radius: 4px;
        }}
        pre code {{
            background: none;
            padding: 0;
            color: inherit;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 16px auto;
            border-radius: 4px;
        }}
        a {{
            color: #C44536;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .table-wrapper {{
            overflow-x: auto;
            margin: 16px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        th, td {{
            border: 1px solid #D4DDD7;
            padding: 10px 12px;
            text-align: left;
        }}
        th {{
            background: #1A3328;
            color: #ffffff;
            font-weight: 600;
        }}
        tr:nth-child(even) {{
            background: #ffffff;
        }}
        tr:nth-child(odd) {{
            background: #F2EDE3;
        }}
        .author {{
            color: #7A8C80;
            font-size: 14px;
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #D4DDD7;
        }}
    </style>
</head>
<body>
{content}
<div class="author">{author}</div>
</body>
</html>"""

THEMES = {
    'default': THEME_DEFAULT,
    'simple': THEME_SIMPLE,
    'grace': THEME_GRACE,
    'odd': THEME_ODD
}

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """解析 YAML frontmatter"""
    pattern = r'^---\n(.*?)\n---\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        frontmatter = match.group(1)
        body = match.group(2)
        metadata = {}
        for line in frontmatter.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        return metadata, body
    return {}, content

def extract_title(content: str) -> str:
    """从内容中提取标题"""
    # 尝试 H1
    match = re.match(r'^# (.+)$', content.strip(), re.MULTILINE)
    if match:
        return match.group(1)
    # 尝试 H2
    match = re.match(r'^## (.+)$', content.strip(), re.MULTILINE)
    if match:
        return match.group(1)
    return "Article"

def convert_alerts(html: str) -> str:
    """转换警告框"""
    html = re.sub(
        r'> \[!NOTE\](.*?)',
        r'<div class="alert alert-note"><strong>NOTE:</strong>\1',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'> \[!WARNING\](.*?)',
        r'<div class="alert alert-warning"><strong>WARNING:</strong>\1',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'> \[!TIP\](.*?)',
        r'<div class="alert alert-tip"><strong>TIP:</strong>\1',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'> \[!IMPORTANT\](.*?)',
        r'<div class="alert alert-important"><strong>IMPORTANT:</strong>\1',
        html, flags=re.DOTALL
    )
    # 关闭标签
    html = re.sub(r'(</div>\n?)', r'\1</div>', html)
    return html

def inline_styles_for_wechat(html: str, theme: str = 'default') -> str:
    """将CSS样式转换为内联样式，支持微信公众号"""
    if theme != 'odd':
        return html
    
    # h2样式：左侧边框+墨绿+鱼红强调
    html = re.sub(
        r'<h2([^>]*)>(.*?)</h2>',
        r'<h2\1 style="font-size:18px;font-weight:600;margin:28px 0 14px;color:#1A3328;border-left:4px solid #C44536;padding-left:12px;">\2</h2>',
        html, flags=re.DOTALL
    )
    
    # h3样式
    html = re.sub(
        r'<h3([^>]*)>(.*?)</h3>',
        r'<h3\1 style="font-size:16px;font-weight:600;margin:20px 0 10px;color:#1A3328;">\2</h3>',
        html, flags=re.DOTALL
    )
    
    # 微信公众号对列表支持有限，移除可能导致问题的样式
    
    # strong样式：鱼红强调
    html = re.sub(
        r'<strong>(.*?)</strong>',
        r'<strong style="font-weight:600;color:#C44536;">\1</strong>',
        html, flags=re.DOTALL
    )
    
    # 处理p标签内的列表项（markdown解析可能把列表项解析成p包裹原始文本）
    # 简单替换：所有"- "开头的内容替换为"• "
    html = re.sub(r'<p>\n?\s*-\s+', '<p>• ', html)
    # 处理换行后的列表项
    html = re.sub(r'\n-\s+', '\n• ', html)
    # 处理 <p>• </p><p>xxx</p> 或 <p>• </p>\n<p>xxx</p> 这种被分成两行的情况
    html = re.sub(r'<p>• \s*</p>\s*<p>', '<p>• ', html)
    html = re.sub(r'</p>\n<p>• ', '</p><p>• ', html)
    # 处理div内的连续p标签合并（markdown解析器将列表项解析成两个p的问题）
    html = re.sub(r'(<div[^>]*>)\s*<p>•\s*</p>\s*<p>', r'\1<p>• ', html, flags=re.DOTALL)
    
    # 处理GFM任务列表 [x] 和 [ ]
    html = re.sub(r'\[x\]', '✅', html, flags=re.IGNORECASE)
    html = re.sub(r'\[ \]', '⬜', html)
    
    # 最终修复：合并被分成两行的列表项 <p>• </p><p>xxx</p>
    # 匹配 bullet在第一个p，内容在第二个p，中间可能有换行
    html = re.sub(r'<p>• (\s*)</p>(\n\s*)<p>', r'<p>• ', html)
    html = re.sub(r'<p>• (\s*)</p>\s*<p>', r'<p>• ', html)
    
    # 微信公众号列表支持差，将li转换为p加符号的形式
    html = re.sub(r'<ul>(.*?)</ul>', r'<div>\1</div>', html, flags=re.DOTALL)
    html = re.sub(r'<ol>(.*?)</ol>', r'<div>\1</div>', html, flags=re.DOTALL)
    # 转换li为p，使用中文顿号
    html = re.sub(r'<li>(.*?)</li>', r'<p>• \1</p>', html, flags=re.DOTALL)
    
    # pre样式：墨绿底，使用更可靠的换行方式
    html = re.sub(
        r'<pre([^>]*)>(.*?)</pre>',
        lambda m: '<pre' + m.group(1) + ' style="background:#1A3328;color:#D4DDD7;padding:16px;border-radius:6px;overflow-x:auto;margin:16px;font-family:Menlo,Monaco,Consolas,monospace;font-size:13px;line-height:1.6;display:block;">' + m.group(2).replace('\n', '<br/>') + '</pre>',
        html, flags=re.DOTALL
    )
    
    # code样式（包含在pre内的需要特殊处理）
    html = re.sub(
        r'<code([^>]*)>(.*?)</code>',
        r'<code\1 style="font-family:Menlo,Monaco,Consolas,monospace;font-size:13px;background:#1A3328;color:#D4DDD7;padding:2px 6px;border-radius:4px;white-space:pre-wrap;word-break:break-all;">\2</code>',
        html, flags=re.DOTALL
    )
    
    # blockquote样式
    html = re.sub(
        r'<blockquote([^>]*)>(.*?)</blockquote>',
        r'<blockquote\1 style="border-left:3px solid #C44536;padding:12px 16px;margin:16px 0;background:#ffffff;color:#555555;border-radius:0 4px 4px 0;">\2</blockquote>',
        html, flags=re.DOTALL
    )
    
    # hr样式
    html = re.sub(
        r'<hr\s*/?>',
        r'<hr style="border:none;border-top:1px solid #D4DDD7;margin:28px 0;" />',
        html
    )
    
    # 清理thead及其样式
    html = re.sub(r'<thead[^>]*>(\s*)<tr>', r'<tr>', html)
    html = re.sub(r'</tr>(\s*)</thead>', r'</tr>', html)
    html = re.sub(r'<thead>(\s*)', r'', html)
    html = re.sub(r'(\s*)</thead>', r'', html)
    
    # table样式
    html = re.sub(
        r'<table([^>]*)>(.*?)</table>',
        r'<table\1 style="width:100%;border-collapse:collapse;font-size:14px;">\2</table>',
        html, flags=re.DOTALL
    )
    # 清理重复的style属性
    html = re.sub(r'(style="[^"]*")\s+\1', r'\1', html)
    
    # th样式（先处理没有属性的th，再处理有属性的）
    html = re.sub(
        r'<th>\s*(.*?)\s*</th>',
        r'<th style="background:#1A3328;color:#ffffff;font-weight:600;padding:10px 12px;text-align:left;border:1px solid #D4DDD7;">\1</th>',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'<th([^>]*?)>\s*(.*?)\s*</th>',
        r'<th\1 style="background:#1A3328;color:#ffffff;font-weight:600;padding:10px 12px;text-align:left;border:1px solid #D4DDD7;">\2</th>',
        html, flags=re.DOTALL
    )
    # 再次清理重复的style
    html = re.sub(r'(style="[^"]*")\s+\1', r'\1', html)
    
    # td样式
    html = re.sub(
        r'<td>\s*(.*?)\s*</td>',
        r'<td style="padding:10px 12px;text-align:left;border:1px solid #D4DDD7;">\1</td>',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'<td([^>]*?)>\s*(.*?)\s*</td>',
        r'<td\1 style="padding:10px 12px;text-align:left;border:1px solid #D4DDD7;">\2</td>',
        html, flags=re.DOTALL
    )
    # 再次清理重复的style
    html = re.sub(r'(style="[^"]*")\s+\1', r'\1', html)
    
    return html

def convert_markdown_to_html(markdown_content: str, theme: str = 'default', 
                              title: str = '', author: str = '', 
                              keep_title: bool = False) -> str:
    """将 Markdown 转换为 HTML"""
    # 解析 frontmatter
    metadata, body = parse_frontmatter(markdown_content)
    
    # 获取元数据
    title = title or metadata.get('title', '') or extract_title(body)
    author = author or metadata.get('author', metadata.get('description', ''))
    
    # 是否保留标题
    if not keep_title:
        body = re.sub(r'^# .+\n', '', body, count=1, flags=re.MULTILINE)
    
    # 转换为 HTML
    md = markdown.Markdown(
        extensions=['tables', 'fenced_code', 'footnotes'],
        extension_configs={
            'fenced_code': {'lang_prefix': ''},
        }
    )
    html_content = md.convert(body)
    
    # 转换警告框
    html_content = convert_alerts(html_content)
    
    # odd主题：转换为内联样式（微信公众号支持）
    if theme == 'odd':
        html_content = inline_styles_for_wechat(html_content, theme)
    
    # 选择主题
    template = THEMES.get(theme, THEMES['default'])
    full_html = template.format(title=title, content=html_content, author=author)
    
    return full_html, {'title': title, 'author': author}

def setup_encoding():
    """解决 Windows 下的编码问题"""
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except Exception:
            pass
    import io
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    setup_encoding()
    parser = argparse.ArgumentParser(description='Markdown 转 HTML 工具')
    parser.add_argument('input', nargs='?', default=None, help='输入 Markdown 文件路径或内容')
    parser.add_argument('-o', '--output', default=None, help='输出 HTML 文件路径')
    parser.add_argument('--theme', default='default', choices=['default', 'simple', 'grace', 'odd'],
                        help='主题风格 (default/simple/grace)')
    parser.add_argument('-t', '--title', default='', help='文章标题')
    parser.add_argument('-a', '--author', default='', help='作者名称')
    parser.add_argument('--keep-title', action='store_true', help='保留标题')
    parser.add_argument('--stdin', action='store_true', help='从标准输入读取')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    # 读取输入：优先 stdin，其次文件，最后内容
    if args.stdin or (args.input is None and not Path(args.input or '').exists()):
        markdown_content = sys.stdin.read()
    elif args.input and Path(args.input).exists():
        markdown_content = Path(args.input).read_text(encoding='utf-8')
    else:
        markdown_content = args.input or ''
    
    if not markdown_content:
        print("[ERROR] No content provided")
        sys.exit(1)
    
    # 转换为 HTML
    html, metadata = convert_markdown_to_html(
        markdown_content, args.theme, args.title, args.author, args.keep_title
    )
    
    # 输出
    if args.json:
        result = {
            'title': metadata['title'],
            'author': metadata['author'],
            'htmlPath': args.output or '',
            'theme': args.theme
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.output:
        Path(args.output).write_text(html, encoding='utf-8')
        print(f"[OK] Saved: {args.output}")
        if args.json:
            print(json.dumps({'htmlPath': args.output}, ensure_ascii=False))
    else:
        print(html)

if __name__ == "__main__":
    main()
