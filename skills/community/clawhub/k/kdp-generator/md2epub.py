#!/usr/bin/env python3
"""
Amazon KDP E-book Generator
将 Markdown 转换为 Amazon KDP 兼容的 EPUB 格式

Usage:
    md2epub.py <input.md> [options]

Options:
    --title         书名
    --author        作者名
    --output        输出文件名
    --cover         封面图片路径
    --template      使用内置模板 (novel|tech|poetry)
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

try:
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
    import markdown
except ImportError:
    print("❌ 需要安装依赖: pip install ebooklib beautifulsoup4 markdown")
    sys.exit(1)


def create_epub(md_file: Path, output_file: Path, metadata: dict):
    """创建 EPUB 文件"""
    
    # 读取 Markdown 内容
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 转换为 HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc', 'nl2br', 'meta']
    )
    
    # 创建 EPUB 书籍
    book = epub.EpubBook()
    
    # 设置元数据
    book.set_identifier(f"kdp-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    book.set_title(metadata.get('title', md_file.stem))
    book.set_language(metadata.get('language', 'zh-CN'))
    book.add_author(metadata.get('author', 'Unknown'))
    
    if metadata.get('description'):
        book.add_metadata('DC', 'description', metadata['description'])
    
    # 创建章节
    chapter = epub.EpubHtml(
        title='正文',
        file_name='content.xhtml',
        lang=metadata.get('language', 'zh-CN')
    )
    
    # 添加样式
    style_content = get_default_css()
    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style_content
    )
    book.add_item(nav_css)
    
    # 设置章节内容
    chapter.content = f'''
    <?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>{metadata.get('title', 'Book')}</title>
        <link rel="stylesheet" type="text/css" href="style/nav.css"/>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    '''
    
    book.add_item(chapter)
    
    # 添加封面
    if metadata.get('cover'):
        cover_path = Path(metadata['cover'])
        if cover_path.exists():
            with open(cover_path, 'rb') as f:
                cover_data = f.read()
            
            cover_image = epub.EpubImage(
                uid='cover-image',
                file_name=f'images/{cover_path.name}',
                media_type=f'image/{cover_path.suffix[1:]}',
                content=cover_data
            )
            book.add_item(cover_image)
            book.set_cover(cover_path.name, cover_data)
    
    # 创建目录
    book.toc = (epub.Link('content.xhtml', '正文', 'content'),)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # 定义 spine
    book.spine = ['nav', chapter]
    
    # 写入文件
    epub.write_epub(output_file, book, {})
    print(f"✅ EPUB 生成成功: {output_file}")
    return str(output_file)


def get_default_css():
    """返回默认 CSS 样式"""
    return '''
    @namespace epub "http://www.idpf.org/2007/ops";
    
    body {
        font-family: "Noto Serif CJK SC", "Source Han Serif SC", "SimSun", serif;
        font-size: 11pt;
        line-height: 1.8;
        color: #333;
        margin: 0;
        padding: 0;
    }
    
    h1 {
        font-size: 18pt;
        font-weight: bold;
        text-align: center;
        margin-top: 2em;
        margin-bottom: 1em;
        page-break-before: always;
    }
    
    h2 {
        font-size: 14pt;
        font-weight: bold;
        margin-top: 1.5em;
        margin-bottom: 0.8em;
        page-break-after: avoid;
    }
    
    h3 {
        font-size: 12pt;
        font-weight: bold;
        margin-top: 1.2em;
        margin-bottom: 0.6em;
    }
    
    p {
        text-indent: 2em;
        margin: 0.5em 0;
        text-align: justify;
    }
    
    p.no-indent {
        text-indent: 0;
    }
    
    blockquote {
        margin: 1em 2em;
        padding-left: 1em;
        border-left: 3px solid #ccc;
        font-style: italic;
    }
    
    code {
        font-family: "Consolas", "Monaco", monospace;
        font-size: 0.9em;
        background: #f4f4f4;
        padding: 0.2em 0.4em;
    }
    
    pre {
        background: #f8f8f8;
        padding: 1em;
        overflow-x: auto;
        font-size: 0.9em;
        line-height: 1.4;
    }
    
    img {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 1em auto;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1em 0;
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 0.5em;
        text-align: left;
    }
    
    th {
        background: #f5f5f5;
        font-weight: bold;
    }
    
    /* 章节分页 */
    .chapter {
        page-break-before: always;
    }
    
    /* 首字下沉 */
    .drop-cap::first-letter {
        font-size: 3em;
        float: left;
        line-height: 0.8;
        margin-right: 0.1em;
    }
    '''


def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to EPUB for Amazon KDP')
    parser.add_argument('input', help='Input Markdown file')
    parser.add_argument('--output', '-o', help='Output EPUB file')
    parser.add_argument('--title', '-t', help='Book title')
    parser.add_argument('--author', '-a', help='Author name')
    parser.add_argument('--description', '-d', help='Book description')
    parser.add_argument('--cover', '-c', help='Cover image path')
    parser.add_argument('--language', '-l', default='zh-CN', help='Language code')
    
    args = parser.parse_args()
    
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"❌ 文件不存在: {input_file}")
        sys.exit(1)
    
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = input_file.with_suffix('.epub')
    
    metadata = {
        'title': args.title or input_file.stem,
        'author': args.author or 'Unknown',
        'description': args.description,
        'cover': args.cover,
        'language': args.language
    }
    
    create_epub(input_file, output_file, metadata)


if __name__ == '__main__':
    main()
