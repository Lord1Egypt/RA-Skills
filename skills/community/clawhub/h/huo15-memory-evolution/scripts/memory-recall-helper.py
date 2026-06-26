#!/usr/bin/env python3
"""memory-recall-helper.py - 记忆检索辅助脚本"""

import os
import json
import sys
import re
from pathlib import Path
from datetime import datetime


def scan_memories(memory_dir):
    """扫描所有记忆文件"""
    memories = []
    for type_dir in ['user', 'feedback', 'project', 'reference']:
        type_path = os.path.join(memory_dir, type_dir)
        if not os.path.isdir(type_path):
            continue
        for f in Path(type_path).glob('*.md'):
            if f.name in ['MEMORY.md', 'index.md']:
                continue
            try:
                stat = f.stat()
                with open(f, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                
                # 解析 frontmatter
                frontmatter = {}
                body = content
                if content.startswith('---'):
                    parts = content[3:].split('---', 1)
                    if len(parts) > 1:
                        fp_text, body = parts
                        for line in fp_text.strip().split('\n'):
                            if ':' in line:
                                k, v = line.split(':', 1)
                                frontmatter[k.strip()] = v.strip()
                
                # 提取描述
                desc_lines = [l.strip() for l in body.strip().split('\n') 
                             if l.strip() and not l.strip().startswith('#')]
                description = ' '.join(desc_lines[:3])[:300]
                
                mtime = datetime.fromtimestamp(stat.st_mtime)
                age_days = (datetime.now() - mtime).days
                
                memories.append({
                    'filename': f.name,
                    'filePath': str(f),
                    'type': type_dir,
                    'name': frontmatter.get('name', f.stem.replace('_', ' ')),
                    'description': description,
                    'mtimeMs': stat.st_mtime * 1000,
                    'ageDays': age_days
                })
            except Exception as e:
                pass
    
    memories.sort(key=lambda x: x['mtimeMs'], reverse=True)
    return memories


def build_manifest(memories):
    """构建记忆清单"""
    by_type = {}
    for m in memories:
        t = m['type']
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(m)
    
    type_icons = {'user': '👤', 'feedback': '🔧', 'project': '📋', 'reference': '🔗'}
    type_names = {'user': '用户画像', 'feedback': '反馈纠正', 'project': '项目进展', 'reference': '外部引用'}
    
    lines = []
    for t in ['user', 'feedback', 'project', 'reference']:
        if t not in by_type:
            continue
        lines.append(f"\n## {type_icons[t]} {type_names[t]}")
        for m in by_type[t][:10]:
            age = f"({m['ageDays']}天前)" if m['ageDays'] > 0 else "(今天)"
            lines.append(f"- [{m['filename']}] {m['name']} {age}")
            if m['description']:
                lines.append(f"  {m['description'][:100]}")
    return '\n'.join(lines)


def keyword_match(query, memories):
    """关键词匹配"""
    query = query.lower()
    query_nospace = re.sub(r'\s+', '', query)
    selected = []
    for m in memories:
        text = (m['name'] + ' ' + m.get('description', '')).lower()
        if query_nospace and query_nospace in text:
            selected.append(m['filename'])
        else:
            words = re.findall(r'[a-zA-Z]{3,}', query)
            for w in words:
                if w in text:
                    selected.append(m['filename'])
                    break
    return selected[:5]


def format_results(filenames, memories):
    """格式化结果"""
    type_icons = {'user': '👤', 'feedback': '🔧', 'project': '📋', 'reference': '🔗'}
    lines = []
    for filename in filenames:
        for m in memories:
            if m['filename'] == filename:
                icon = type_icons.get(m['type'], '📄')
                age = f"({m['ageDays']}天前)" if m['ageDays'] > 0 else '(今天)'
                lines.append(f"{icon} [{m['type']}] {m['name']} {age}")
                lines.append(f"   路径: {m['filePath']}")
                if m['description']:
                    lines.append(f"   {m['description'][:100]}")
                lines.append("")
                break
    return '\n'.join(lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: memory-recall-helper.py <action> <memory_dir> [query]")
        sys.exit(1)
    
    action = sys.argv[1]
    memory_dir = sys.argv[2]
    query = sys.argv[3] if len(sys.argv) > 3 else ''
    
    memories = scan_memories(memory_dir)
    
    if action == 'scan':
        print(json.dumps(memories, ensure_ascii=False))
    elif action == 'list':
        type_icons = {'user': '👤', 'feedback': '🔧', 'project': '📋', 'reference': '🔗'}
        type_names = {'user': '用户', 'feedback': '反馈', 'project': '项目', 'reference': '引用'}
        print(f"共 {len(memories)} 个记忆:\n")
        for m in memories[:20]:
            icon = type_icons.get(m['type'], '📄')
            name = m['name'][:35]
            desc = (m.get('description') or '')[:50]
            age_days = m['ageDays']
            age_str = '今天' if age_days == 0 else f'{age_days}天前'
            print(f"{icon} [{type_names.get(m['type'], m['type'])}] {name}")
            print(f"   {age_str} | {desc}")
            print()
    elif action == 'count':
        print(len(memories))
    elif action == 'recall':
        filenames = keyword_match(query, memories)
        if filenames:
            print(format_results(filenames, memories))
        else:
            print("没有找到与查询相关的记忆")
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)


if __name__ == '__main__':
    main()
