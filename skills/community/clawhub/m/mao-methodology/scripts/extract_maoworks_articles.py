#!/usr/bin/env python3
"""Extract articles from Mao Zedong Selected Works docx files.

Works with the人民出版社 docx editions where:
- Article titles end with '*' marker
- Table of contents appears first (skip it)
- Actual article content follows TOC, starting around paragraph 260+

Usage:
    python extract_maoworks_articles.py <path_to.docx> [--list | --article N | --preview N --lines L]

Options:
    --list              List all article titles with paragraph indices
    --article N         Extract full text of article N (1-indexed)
    --preview N --lines L  Show first L lines of article N
"""

import sys
import json
import argparse

try:
    import docx
except ImportError:
    print("ERROR: python-docx not installed. Run: pip install python-docx")
    sys.exit(1)


def find_articles(docx_path):
    """Parse docx and find all articles by * marker."""
    doc = docx.Document(docx_path)
    paragraphs = doc.paragraphs

    articles = []
    current_title = None
    current_start = None
    content_lines = []
    in_article = False

    for i, p in enumerate(paragraphs):
        text = p.text.strip()
        if not text:
            continue

        # Skip TOC and header noise
        if '毛泽东选集' in text and len(text) < 30:
            continue
        if text in ['目录', '目\t录', '第三次国内革命战争时期', '抗日战争时期',
                     '第二次国内革命战争时期', '第一次国内革命战争时期']:
            continue
        if text.isdigit() and len(text) <= 4:
            continue
        if '\t' in text and '—' in text:
            continue

        # Check for title ending with *
        if text.endswith('*'):
            if current_title and in_article:
                articles.append({
                    'title': current_title,
                    'start_para': current_start,
                    'content': content_lines,
                    'word_count': len(''.join(content_lines))
                })

            current_title = text[:-1].strip()
            current_start = i
            content_lines = []
            in_article = True
        elif in_article:
            content_lines.append(text)

    # Don't forget last article
    if current_title and in_article:
        articles.append({
            'title': current_title,
            'start_para': current_start,
            'content': content_lines,
            'word_count': len(''.join(content_lines))
        })

    return articles


def main():
    parser = argparse.ArgumentParser(description='Extract articles from Mao Selected Works docx')
    parser.add_argument('docx_path', help='Path to the .docx file')
    parser.add_argument('--list', action='store_true', help='List all articles')
    parser.add_argument('--article', type=int, help='Extract article N (1-indexed)')
    parser.add_argument('--preview', type=int, help='Preview article N')
    parser.add_argument('--lines', type=int, default=50, help='Number of lines for preview')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    articles = find_articles(args.docx_path)

    if args.list:
        print(f"Found {len(articles)} articles:\n")
        for i, a in enumerate(articles, 1):
            print(f"  [{i}] {a['title']} (段落{a['start_para']}, {a['word_count']}字)")
    elif args.article:
        a = articles[args.article - 1]
        if args.json:
            print(json.dumps({'title': a['title'], 'content': '\n'.join(a['content'])}, ensure_ascii=False))
        else:
            print(f"\n{'='*60}")
            print(f"《{a['title']}》 ({a['word_count']}字)")
            print(f"{'='*60}\n")
            print('\n'.join(a['content']))
    elif args.preview:
        a = articles[args.preview - 1]
        print(f"\n{'='*60}")
        print(f"《{a['title']}》 - 前{args.lines}段")
        print(f"{'='*60}\n")
        for line in a['content'][:args.lines]:
            print(line[:150])
    else:
        # Default: list articles
        print(f"Found {len(articles)} articles:\n")
        for i, a in enumerate(articles, 1):
            print(f"  [{i}] {a['title']} (段落{a['start_para']}, {a['word_count']}字)")


if __name__ == '__main__':
    main()
