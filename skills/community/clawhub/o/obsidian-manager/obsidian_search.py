#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian 笔记搜索工具

用法:
    python obsidian_search.py --query "RTHS" --limit 10
    python obsidian_search.py --direction "02-RTHS" --tag "文献"
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def get_research_base_path():
    """获取 research 基础路径"""
    base = Path(__file__).parent.parent / 'research'
    if not base.exists():
        base = Path(r'D:\Personal\OpenClaw\research')
    return base


def search_notes(query, limit=10, direction=None, tag=None):
    """搜索笔记"""
    base = get_research_base_path()
    results = []
    
    # 确定搜索目录
    search_dirs = [base]
    if direction:
        direction_dir = base / direction
        if direction_dir.exists():
            search_dirs = [direction_dir]
        else:
            print(f"警告：研究方向目录不存在：{direction}")
    
    # 遍历所有 markdown 文件
    for search_dir in search_dirs:
        for md_file in search_dir.rglob('*.md'):
            # 跳过模板文件
            if md_file.name == 'template.md':
                continue
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 标签过滤
                if tag:
                    if f'tags:' not in content or tag not in content:
                        continue
                
                # 关键词搜索（标题或内容）
                if query:
                    # 检查标题
                    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    title = title_match.group(1) if title_match else md_file.stem
                    
                    # 检查内容是否包含关键词
                    if query.lower() not in content.lower() and query.lower() not in title.lower():
                        continue
                else:
                    title = md_file.stem
                
                # 提取元数据
                frontmatter = {}
                frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
                if frontmatter_match:
                    fm_text = frontmatter_match.group(1)
                    for line in fm_text.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            frontmatter[key.strip()] = value.strip()
                
                # 创建结果
                result = {
                    'title': title,
                    'file': str(md_file),
                    'relative_path': str(md_file.relative_to(base)),
                    'direction': md_file.parent.name,
                    'created': frontmatter.get('created', frontmatter.get('date', '')),
                    'tags': frontmatter.get('tags', ''),
                    'snippet': get_snippet(content, query)
                }
                results.append(result)
                
            except Exception as e:
                print(f"读取文件失败 {md_file}: {e}")
                continue
    
    # 按创建时间排序（最新的在前）
    results.sort(key=lambda x: x.get('created', ''), reverse=True)
    
    return results[:limit]


def get_snippet(content, query, context=50):
    """获取包含关键词的摘要"""
    if not query:
        return ""
    
    # 查找关键词位置
    content_lower = content.lower()
    query_lower = query.lower()
    pos = content_lower.find(query_lower)
    
    if pos == -1:
        return ""
    
    # 获取上下文
    start = max(0, pos - context)
    end = min(len(content), pos + len(query) + context)
    
    snippet = content[start:end]
    snippet = snippet.replace('\n', ' ').strip()
    
    if start > 0:
        snippet = "..." + snippet
    if end < len(content):
        snippet = snippet + "..."
    
    return snippet


def format_results(results, json_output=False):
    """格式化搜索结果"""
    if json_output:
        return json.dumps(results, ensure_ascii=False, indent=2)
    
    output = []
    for i, item in enumerate(results, 1):
        output.append(f"\n[{i}] **{item['title']}**")
        output.append(f"    路径：{item['relative_path']}")
        if item['created']:
            output.append(f"    创建：{item['created']}")
        if item['tags']:
            output.append(f"    标签：{item['tags']}")
        if item['snippet']:
            output.append(f"    摘要：{item['snippet']}")
    
    return '\n'.join(output)


def list_notes(direction=None):
    """列出指定方向的所有笔记"""
    base = get_research_base_path()
    
    if direction:
        direction_dir = base / direction
        if not direction_dir.exists():
            print(f"错误：研究方向目录不存在：{direction}")
            return []
        
        md_files = list(direction_dir.glob('*.md'))
        return [{'title': f.stem, 'file': str(f), 'direction': direction} for f in md_files]
    else:
        # 列出所有方向的笔记
        all_notes = []
        for direction_name in sorted(os.listdir(base)):
            direction_dir = base / direction_name
            if direction_dir.is_dir():
                md_files = list(direction_dir.glob('*.md'))
                for f in md_files:
                    all_notes.append({
                        'title': f.stem,
                        'file': str(f),
                        'direction': direction_name
                    })
        return all_notes


def main():
    parser = argparse.ArgumentParser(description='Obsidian 笔记搜索工具')
    parser.add_argument('--query', '-q', type=str, help='搜索关键词')
    parser.add_argument('--direction', '-d', type=str, help='研究方向')
    parser.add_argument('--tag', '-t', type=str, help='标签过滤')
    parser.add_argument('--limit', '-l', type=int, default=10, help='返回结果数量')
    parser.add_argument('--list', action='store_true', help='列出笔记（不搜索）')
    parser.add_argument('--json', action='store_true', help='以 JSON 格式输出')
    
    args = parser.parse_args()
    
    if not args.query and not args.list and not args.direction:
        print("错误：请指定 --query、--list 或 --direction")
        parser.print_help()
        sys.exit(1)
    
    print(f"搜索：{args.query or '全部笔记'}")
    if args.direction:
        print(f"研究方向：{args.direction}")
    if args.tag:
        print(f"标签：{args.tag}")
    print("-" * 60)
    
    # 搜索或列出
    if args.list or (not args.query and args.direction):
        results = list_notes(args.direction)
    else:
        results = search_notes(
            query=args.query or '',
            limit=args.limit,
            direction=args.direction,
            tag=args.tag
        )
    
    # 输出结果
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if results:
            print(format_results(results, args.json))
            print(f"\n共找到 {len(results)} 篇笔记")
        else:
            print("未找到匹配的笔记")


if __name__ == '__main__':
    import os
    main()
