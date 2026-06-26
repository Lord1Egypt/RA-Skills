#!/usr/bin/env python3
"""
Amazon KDP 元数据生成器
生成 KDP 出版所需的元数据文件

Usage:
    generate_metadata.py --title "书名" --author "作者" [options]
"""

import argparse
import json
from pathlib import Path
from datetime import datetime


# Amazon KDP 图书分类（部分常用分类）
KDP_CATEGORIES = {
    'fiction': {
        'literature': '文学',
        'scifi': '科幻',
        'fantasy': '奇幻',
        'mystery': '悬疑',
        'romance': ' romance',
        'thriller': '惊悚',
        'horror': '恐怖',
        'historical': '历史小说',
        'contemporary': '当代小说',
        'young_adult': '青少年',
    },
    'nonfiction': {
        'business': '商业与投资',
        'self_help': '自我提升',
        'technology': '计算机与互联网',
        'science': '科学',
        'history': '历史',
        'biography': '传记',
        'health': '健康与健身',
        'cooking': '烹饪',
        'travel': '旅游',
        'education': '教育',
        'parenting': '育儿',
        'politics': '政治与社会科学',
    }
}


def generate_metadata(args) -> dict:
    """生成元数据"""
    
    metadata = {
        'title': args.title,
        'subtitle': args.subtitle or '',
        'author': args.author,
        'contributors': [],
        'description': args.description or '',
        'keywords': args.keywords.split(',') if args.keywords else [],
        'categories': args.categories.split(',') if args.categories else [],
        'language': args.language or 'zh-CN',
        'publication_date': args.date or datetime.now().strftime('%Y-%m-%d'),
        'edition': args.edition or '1',
        'isbn': args.isbn or '',
        'publisher': args.publisher or '自出版',
        'rights': args.rights or '保留所有权利',
        'adult_content': args.adult or False,
        'age_range': args.age_range or '',
        'series': args.series or '',
        'volume': args.volume or '',
    }
    
    # 添加译者/编者
    if args.translator:
        metadata['contributors'].append({
            'role': 'translator',
            'name': args.translator
        })
    
    if args.editor:
        metadata['contributors'].append({
            'role': 'editor',
            'name': args.editor
        })
    
    if args.illustrator:
        metadata['contributors'].append({
            'role': 'illustrator',
            'name': args.illustrator
        })
    
    return metadata


def save_metadata(metadata: dict, output: str, format: str = 'json'):
    """保存元数据"""
    output_path = Path(output)
    
    if format == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    elif format == 'txt':
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"书名: {metadata['title']}\n")
            if metadata['subtitle']:
                f.write(f"副标题: {metadata['subtitle']}\n")
            f.write(f"作者: {metadata['author']}\n")
            f.write(f"语言: {metadata['language']}\n")
            f.write(f"出版日期: {metadata['publication_date']}\n")
            if metadata['description']:
                f.write(f"\n简介:\n{metadata['description']}\n")
            if metadata['keywords']:
                f.write(f"\n关键词: {', '.join(metadata['keywords'])}\n")
            if metadata['categories']:
                f.write(f"分类: {', '.join(metadata['categories'])}\n")
    
    elif format == 'html':
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{metadata['title']} - 元数据</title>
</head>
<body>
    <h1>{metadata['title']}</h1>
    {'<h2>' + metadata['subtitle'] + '</h2>' if metadata['subtitle'] else ''}
    <p><strong>作者:</strong> {metadata['author']}</p>
    <p><strong>语言:</strong> {metadata['language']}</p>
    <p><strong>出版日期:</strong> {metadata['publication_date']}</p>
    {'<p><strong>简介:</strong></p><p>' + metadata['description'] + '</p>' if metadata['description'] else ''}
    {'<p><strong>关键词:</strong> ' + ', '.join(metadata['keywords']) + '</p>' if metadata['keywords'] else ''}
</body>
</html>'''
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    print(f"✅ 元数据保存成功: {output_path}")


def print_category_help():
    """打印分类帮助"""
    print("\n📚 Amazon KDP 图书分类参考:")
    print("\n【小说类】")
    for key, name in KDP_CATEGORIES['fiction'].items():
        print(f"  {key}: {name}")
    
    print("\n【非小说类】")
    for key, name in KDP_CATEGORIES['nonfiction'].items():
        print(f"  {key}: {name}")
    
    print("\n💡 提示: 使用 --categories 参数时，可以用逗号分隔多个分类")
    print("   例如: --categories 'fiction/scifi,technology'")


def main():
    parser = argparse.ArgumentParser(description='Generate Amazon KDP metadata')
    parser.add_argument('--title', '-t', required=True, help='Book title')
    parser.add_argument('--author', '-a', required=True, help='Author name')
    parser.add_argument('--subtitle', '-s', help='Subtitle')
    parser.add_argument('--description', '-d', help='Book description')
    parser.add_argument('--keywords', '-k', help='Keywords (comma-separated, max 7)')
    parser.add_argument('--categories', '-c', help='Categories (comma-separated)')
    parser.add_argument('--language', '-l', default='zh-CN', help='Language code')
    parser.add_argument('--date', help='Publication date (YYYY-MM-DD)')
    parser.add_argument('--edition', '-e', help='Edition number')
    parser.add_argument('--isbn', help='ISBN number')
    parser.add_argument('--publisher', '-p', help='Publisher name')
    parser.add_argument('--rights', help='Copyright notice')
    parser.add_argument('--translator', help='Translator name')
    parser.add_argument('--editor', help='Editor name')
    parser.add_argument('--illustrator', help='Illustrator name')
    parser.add_argument('--series', help='Series name')
    parser.add_argument('--volume', '-v', help='Volume number in series')
    parser.add_argument('--adult', action='store_true', help='Adult content')
    parser.add_argument('--age-range', help='Target age range (e.g., "18+")')
    parser.add_argument('--output', '-o', default='metadata.json', help='Output file')
    parser.add_argument('--format', choices=['json', 'txt', 'html'], default='json',
                       help='Output format')
    parser.add_argument('--categories-help', action='store_true', help='Show category help')
    
    args = parser.parse_args()
    
    if args.categories_help:
        print_category_help()
        return
    
    metadata = generate_metadata(args)
    save_metadata(metadata, args.output, args.format)
    
    print(f"\n📋 元数据摘要:")
    print(f"   书名: {metadata['title']}")
    print(f"   作者: {metadata['author']}")
    print(f"   语言: {metadata['language']}")
    print(f"   出版日期: {metadata['publication_date']}")
    
    if metadata['keywords']:
        print(f"   关键词: {', '.join(metadata['keywords'])}")


if __name__ == '__main__':
    main()
