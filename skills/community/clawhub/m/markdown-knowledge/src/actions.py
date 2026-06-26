#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 动作模块
定义知识库检索的 OpenClaw 动作接口
"""

import json
import sys
from pathlib import Path

from .config import load_config
from .knowledge_core import KnowledgeSearcher, IndexBuilder


def action_search(query: str, top_k: int = None) -> dict:
    """
    OpenClaw 搜索动作

    Args:
        query: 搜索查询
        top_k: 返回结果数量

    Returns:
        OpenClaw 格式的结果
    """
    config = load_config()
    if top_k is None:
        top_k = config.get('search_top_k', 3)

    searcher = KnowledgeSearcher(config)
    results = searcher.search(query, top_k)

    if not results:
        return {
            'success': True,
            'found': False,
            'message': '未在知识库中找到相关信息',
            'results': []
        }

    return {
        'success': True,
        'found': True,
        'count': len(results),
        'results': [
            {
                'title': r['document'].get('title', ''),
                'path': r['document'].get('path', ''),
                'relative_path': r['document'].get('relative_path', ''),
                'score': r['score'],
                'summary': r['document'].get('summary', ''),
                'matched_blocks': [
                    {
                        'title': b['title'],
                        'preview': b['preview']
                    }
                    for b in r['matched_blocks']
                ]
            }
            for r in results
        ],
        'formatted': searcher.format_results(results, query)
    }


def action_build() -> dict:
    """OpenClaw 索引构建动作"""
    config = load_config()
    builder = IndexBuilder(config)
    result = builder.build_index()

    return {
        'success': True,
        'total_documents': result['total_documents'],
        'total_blocks': result['total_blocks'],
        'index_path': config['index_path']
    }


def action_stats() -> dict:
    """OpenClaw 统计动作"""
    config = load_config()
    searcher = KnowledgeSearcher(config)

    return {
        'success': True,
        **searcher.get_stats()
    }


def action_check() -> dict:
    """OpenClaw 健康检查动作"""
    config = load_config()
    index_path = Path(config['index_path'])

    status = {
        'config_exists': True,
        'index_exists': index_path.exists(),
        'knowledge_path': config['knowledge_path'],
        'index_path': str(index_path)
    }

    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
            status['document_count'] = index_data.get('total_documents', 0)
            status['last_updated'] = index_data.get('created_at', '')

    return {
        'success': True,
        'status': 'healthy' if status['index_exists'] else 'needs_rebuild',
        **status
    }


# OpenClaw 动作入口
if __name__ == '__main__':
    action = sys.argv[1] if len(sys.argv) > 1 else 'help'
    args = sys.argv[2:] if len(sys.argv) > 2 else []

    if action == 'search':
        query = args[0] if args else ''
        result = action_search(query)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif action == 'build':
        result = action_build()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif action == 'stats':
        result = action_stats()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif action == 'check':
        result = action_check()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print("用法：")
        print("  actions.py search <查询词>  # 搜索")
        print("  actions.py build          # 构建索引")
        print("  actions.py stats          # 统计信息")
        print("  actions.py check           # 健康检查")
