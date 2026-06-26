#!/usr/bin/env python3
"""
记忆搜索脚本
支持结构化搜索和向量搜索
"""

import os
import sys
import json
import subprocess

def search_structured(query, category=None):
    """搜索结构化记忆"""
    where = ""
    if category:
        where = f"WHERE category = '{category}'"
    
    cmd = [
        "psql", "-h", "localhost", "-p", "5432",
        "-U", "damien", "-d", "postgres",
        "-c", f"SELECT title, content FROM memory_structured {where};"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def search_vector(query):
    """向量语义搜索"""
    # 获取 embedding
    embed_cmd = [
        "curl", "-s", "http://localhost:11434/api/embeddings",
        "-d", json.dumps({"model": "qllama/bge-large-zh-v1.5", "prompt": query})
    ]
    
    result = subprocess.run(embed_cmd, capture_output=True, text=True)
    try:
        emb = json.loads(result.stdout)["embedding"]
        emb_str = "[" + ",".join(map(str, emb)) + "]"
        
        # 搜索
        search_cmd = [
            "psql", "-h", "localhost", "-p", "5433",
            "-U", "damien", "-d", "postgres",
            "-c", f"SELECT content, (1 - (embedding <=> '{emb_str}')) AS similarity FROM longterm_memory ORDER BY embedding <=> '{emb_str}' LIMIT 3;"
        ]
        
        result = subprocess.run(search_cmd, capture_output=True, text=True)
        return result.stdout
    except:
        return "向量搜索失败"

def main():
    if len(sys.argv) < 2:
        print("Usage: python memory_search.py <query> [--category <category>]")
        print("Example: python memory_search.py '我之前说过我喜欢什么编程语言'")
        sys.exit(1)
    
    query = sys.argv[1]
    category = None
    
    if "--category" in sys.argv:
        idx = sys.argv.index("--category")
        if idx + 1 < len(sys.argv):
            category = sys.argv[idx + 1]
    
    print(f"搜索: {query}")
    print("=" * 50)
    
    print("\n📁 结构化记忆:")
    print(search_structured(query, category))
    
    print("\n🔍 向量搜索:")
    print(search_vector(query))

if __name__ == "__main__":
    main()
