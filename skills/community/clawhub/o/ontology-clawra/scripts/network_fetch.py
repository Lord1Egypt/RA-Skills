#!/usr/bin/env python3
"""
ontology-clawra 网络获取模块
当本地无数据时，自动从网络获取权威数据
"""

import json
import os
from datetime import datetime

MEMORY_DIR = os.path.expanduser("~/.openclaw/skills/ontology-clawra/memory")
NETWORK_CACHE = os.path.join(MEMORY_DIR, "network_cache.jsonl")


def search_local(keywords):
    """搜索本地记忆/本体"""
    results = []
    keywords = [k.lower() for k in keywords]
    
    # 检查记忆文件
    memory_dir = os.path.expanduser("~/.openclaw/workspace/memory")
    if os.path.exists(memory_dir):
        for root, dirs, files in os.walk(memory_dir):
            for f in files:
                if f.endswith('.md'):
                    path = os.path.join(root, f)
                    with open(path, 'r', encoding='utf-8') as fp:
                        content = fp.read().lower()
                        for kw in keywords:
                            if kw in content:
                                results.append({
                                    "source": "local_memory",
                                    "file": path,
                                    "keyword": kw,
                                    "timestamp": datetime.now().isoformat()
                                })
    
    return results


def search_ontology(keywords):
    """搜索本体数据"""
    results = []
    keywords = [k.lower() for k in keywords]
    
    # 检查ontology-clawra内存
    onto_dir = os.path.expanduser("~/.openclaw/skills/ontology-clawra/memory")
    for fname in ['graph.jsonl', 'laws.yaml', 'rules.yaml', 'concepts.jsonl']:
        path = os.path.join(onto_dir, fname)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as fp:
                content = fp.read().lower()
                for kw in keywords:
                    if kw in content:
                        results.append({
                            "source": "ontology",
                            "file": fname,
                            "keyword": kw,
                            "timestamp": datetime.now().isoformat()
                        })
    
    return results


def fetch_from_network(query):
    """
    从网络获取数据 - ⚠️ 已禁用 ⚠️
    
    为确保安全，本函数现在只返回本地搜索结果。
    如需启用网络功能，请配置 web_search API 并经用户确认。
    """
    # 网络功能已禁用，仅返回本地结果
    # 如需启用，需要：1) 用户明确授权 2) 配置网络API
    # 先检查本地
    local_results = search_local(query.split())
    onto_results = search_ontology(query.split())
    
    all_results = local_results + onto_results
    
    if all_results:
        return {
            "status": "FOUND_LOCAL",
            "confidence": "CONFIRMED" if onto_results else "ASSUMED",
            "results": all_results,
            "message": f"在本地找到{len(all_results)}条相关数据"
        }
    
    # 本地无数据，返回网络获取建议
    return {
        "status": "NOT_FOUND",
        "confidence": "UNKNOWN",
        "results": [],
        "suggestions": [
            f"需要网络搜索: {query}",
            f"建议搜索关键词: {query}",
            "可用的数据源: 燃气工程规范、行业标准、技术手册",
            "注意：获取后应存入本地本体以备后续使用"
        ],
        "network_query": query
    }


def save_to_network_cache(query, results):
    """保存网络获取结果到缓存"""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    
    entry = {
        "query": query,
        "results": results,
        "timestamp": datetime.now().isoformat()
    }
    
    with open(NETWORK_CACHE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def main(query):
    """主函数"""
    print(f"🔍 正在查询: {query}")
    print("-" * 40)
    
    result = fetch_from_network(query)
    
    print(f"📊 状态: {result['status']}")
    print(f"🎯 置信度: {result['confidence']}")
    print()
    
    if result['results']:
        print(f"📁 找到 {len(result['results'])} 条本地数据:")
        for r in result['results']:
            print(f"  - [{r['source']}] {r.get('file', 'unknown')}: {r['keyword']}")
    else:
        print("💡 本地无相关数据")
        if 'suggestions' in result:
            print("\n📋 建议:")
            for s in result['suggestions']:
                print(f"  • {s}")
    
    return result


if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "燃气 调压 选型"
    main(query)
