#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库统一搜索工具

用法:
    python knowledge_search.py --query "RTHS" --all
    python knowledge_search.py --query "振动台" --zotero --obsidian
"""

import argparse
import json
import sys
from pathlib import Path

# 导入子技能
sys.path.insert(0, str(Path(__file__).parent.parent / 'zotero-manager'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'obsidian-manager'))

try:
    from zotero_search import search_library, get_api_key, get_user_id, format_results as zotero_format
    from obsidian_search import search_notes, format_results as obsidian_format
    ZOTERO_AVAILABLE = True
except ImportError as e:
    print(f"警告：Zotero/Obsidian 模块导入失败：{e}")
    ZOTERO_AVAILABLE = False


def search_ima(query, limit=10):
    """搜索 IMA 知识库（简化版本，待完善）"""
    # TODO: 集成 IMA API
    print(f"[IMA] 搜索：{query}（功能开发中）")
    return []


def search_all(query, limit=10):
    """搜索所有平台"""
    results = {
        'zotero': [],
        'obsidian': [],
        'ima': []
    }
    
    print(f"统一搜索：{query}")
    print("=" * 60)
    
    # 搜索 Zotero
    if ZOTERO_AVAILABLE:
        print("\n【Zotero 文献】")
        try:
            api_key = get_api_key()
            user_id = get_user_id(api_key)
            if user_id:
                items = search_library(query, api_key, user_id, limit)
                results['zotero'] = items
                formatted = zotero_format(items)
                print(formatted)
            else:
                print("无法连接 Zotero（API Key 配置？）")
        except ValueError as e:
            print(f"Zotero 未配置：{e}")
        except Exception as e:
            print(f"Zotero 搜索失败：{e}")
    else:
        print("Zotero 模块不可用")
    
    # 搜索 Obsidian
    print("\n【Obsidian 笔记】")
    obsidian_results = search_notes(query, limit=limit)
    results['obsidian'] = obsidian_results
    if obsidian_results:
        print(obsidian_format(obsidian_results))
    else:
        print("未找到匹配的笔记")
    
    # 搜索 IMA
    print("\n【IMA 云端】")
    ima_results = search_ima(query, limit=limit)
    results['ima'] = ima_results
    if ima_results:
        print(ima_results)
    else:
        print("未找到或功能开发中")
    
    # 统计
    print("\n" + "=" * 60)
    total = len(results['zotero']) + len(results['obsidian']) + len(results['ima'])
    print(f"共找到 {total} 条结果")
    print(f"  - Zotero: {len(results['zotero'])} 篇")
    print(f"  - Obsidian: {len(results['obsidian'])} 篇")
    print(f"  - IMA: {len(results['ima'])} 条")
    
    return results


def main():
    parser = argparse.ArgumentParser(description='知识库统一搜索工具')
    parser.add_argument('--query', '-q', type=str, required=True, help='搜索关键词')
    parser.add_argument('--all', action='store_true', help='搜索所有平台')
    parser.add_argument('--zotero', action='store_true', help='仅搜索 Zotero')
    parser.add_argument('--obsidian', action='store_true', help='仅搜索 Obsidian')
    parser.add_argument('--ima', action='store_true', help='仅搜索 IMA')
    parser.add_argument('--limit', '-l', type=int, default=10, help='返回结果数量')
    parser.add_argument('--json', action='store_true', help='以 JSON 格式输出')
    
    args = parser.parse_args()
    
    # 确定搜索范围
    if args.all or (not args.zotero and not args.obsidian and not args.ima):
        results = search_all(args.query, args.limit)
    else:
        results = {}
        if args.zotero:
            print("【Zotero 文献】")
            # TODO: 实现单独搜索
        if args.obsidian:
            print("【Obsidian 笔记】")
            obs_results = search_notes(args.query, limit=args.limit)
            results['obsidian'] = obs_results
            print(obsidian_format(obs_results))
        if args.ima:
            print("【IMA 云端】")
            results['ima'] = search_ima(args.query, args.limit)
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
