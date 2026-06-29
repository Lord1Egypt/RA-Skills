#!/usr/bin/env python3
"""
strip_abstracts.py — 从论文 JSON 中剥离摘要字段，只保留元数据。

用途：当需要 read paper JSON 文件但不想摘要污染上下文时，
      先 pipe 通过此脚本，输出不含 abstract 字段的版本。

用法：
  python strip_abstracts.py -i ranked.json                    # stdout 输出无摘要版
  python strip_abstracts.py -i ranked.json -o safe.json       # 写入文件
  python strip_abstracts.py -i ranked.json --summary          # 只输出统计 + 标题列表

设计原则：
  - 保留所有元数据字段（title, authors, year, venue, citations, doi, link, _scores, _tags, _source_db）
  - 移除 abstract 字段内容（替换为占位符 "[已缓存]"，表示摘要在文件系统中可用）
  - --summary 模式只输出每篇的标题/年份/引用/来源/分数，完全不含摘要
"""

import json
import argparse
import sys
import os

FIELDS_TO_STRIP = [
    'abstract',
    'abstractSnippet',
    'abstract_snippet',
]

# 保留字段：元数据 + 摘要文件引用
FIELDS_TO_KEEP_META = [
    'title', 'authors', 'year', 'venue', 'type', 'citations',
    'doi', 'link', 'isOA', 'openaccess', 'pdfUrl', 'docId',
    '_source_db', '_norm_year', '_norm_citations', '_venue_tier',
    '_scores', '_tags', '_abstract_file',
]


def strip_abstracts(papers: list) -> list:
    """移除每篇论文的 abstract 字段，替换为占位符。保留 _abstract_file 引用。"""
    cleaned = []
    for paper in papers:
        p = {}
        for key, value in paper.items():
            if key in FIELDS_TO_STRIP:
                # 如果有 _abstract_file 引用，标为已缓存
                p[key] = '[已缓存]' if paper.get('_abstract_file') else ''
            elif key == '_abstract_file':
                p[key] = value  # 保留文件引用
            else:
                p[key] = value
        cleaned.append(p)
    return cleaned


def summarize(papers: list) -> list:
    """只输出每篇论文的关键元数据，完全不含摘要。"""
    summaries = []
    for paper in papers:
        scores = paper.get('_scores', {})
        tags = paper.get('_tags', [])
        source = paper.get('_source_db', ['?'])
        has_abstract = bool(paper.get('_abstract_file'))
        summaries.append({
            'title': paper.get('title', ''),
            'year': paper.get('year', ''),
            'citations': paper.get('citations', ''),
            'venue': str(paper.get('venue', ''))[:80],
            'source': source[0] if source else '?',
            'relevance': scores.get('relevance', 0),
            'impact': scores.get('impact', 0),
            'has_abstract': has_abstract,
            'tags': tags,
            'link': paper.get('link', '') or paper.get('doi', ''),
        })
    return summaries


def main():
    parser = argparse.ArgumentParser(
        description='从论文 JSON 剥离摘要字段，防止摘要文本进入 AI 上下文'
    )
    parser.add_argument('-i', '--input', required=True, help='输入 JSON 文件')
    parser.add_argument('-o', '--output', help='输出文件（默认 stdout）')
    parser.add_argument('--summary', action='store_true',
                        help='极简模式：只输出标题/年份/引用/分数，完全不含摘要')
    parser.add_argument('--top', type=int, default=0,
                        help='只输出前 N 篇')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)

    papers = data.get('papers', data if isinstance(data, list) else [])

    if args.top > 0:
        papers = papers[:args.top]

    if args.summary:
        output_papers = summarize(papers)
    else:
        output_papers = strip_abstracts(papers)

    result = {
        'total': len(output_papers),
        'stripped': True,
        'original_file': os.path.basename(args.input),
        'papers': output_papers,
    }

    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f'[Strip] {len(output_papers)} papers → {args.output} (abstracts stripped)',
              file=sys.stderr)
    else:
        print(output_json)


if __name__ == '__main__':
    main()
