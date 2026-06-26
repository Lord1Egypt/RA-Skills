#!/usr/bin/env python3
"""
记忆系统语义检索器
使用 FAISS 索引进行快速语义搜索
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 添加 local-memory 的 venv 到路径
venv_path = Path.home() / ".openclaw" / "workspace" / "skills" / "local-memory" / "venv"
if (venv_path / "bin" / "activate").exists():
    sys.path.insert(0, str(venv_path / "lib" / "python3.11" / "site-packages"))

try:
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
except ImportError as e:
    print(f"❌ 缺少依赖：{e}")
    sys.exit(1)

# 配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
INDEX_DIR = WORKSPACE / "index"
INDEX_FILE = INDEX_DIR / "memory_index.faiss"
METADATA_FILE = INDEX_DIR / "metadata.json"
MODEL_PATH = Path.home() / ".openclaw" / "workspace" / "skills" / "local-memory" / "models" / "all-MiniLM-L6-v2"

def load_index():
    """加载 FAISS 索引和元数据"""
    if not INDEX_FILE.exists():
        print("❌ 索引文件不存在，请先运行 build_memory_index.py")
        sys.exit(1)
    
    index = faiss.read_index(str(INDEX_FILE))
    
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    
    return index, metadata

def search(query, top_k=5):
    """执行语义搜索"""
    index, metadata = load_index()
    model = SentenceTransformer(str(MODEL_PATH))
    
    # 编码查询
    query_embedding = model.encode([query])
    
    # 搜索
    scores, indices = index.search(query_embedding.astype('float32'), min(top_k, len(metadata)))
    
    results = []
    for i, (idx, score) in enumerate(zip(indices[0], scores[0])):
        if idx >= 0 and idx < len(metadata):
            results.append({
                "rank": i + 1,
                "source": metadata[idx]["source"],
                "type": metadata[idx]["type"],
                "score": float(score),
                "similarity": 1 / (1 + score)  # 转换为相似度 (0-1)
            })
    
    return results

def main():
    import argparse
    parser = argparse.ArgumentParser(description="记忆系统语义搜索")
    parser.add_argument("query", help="搜索查询")
    parser.add_argument("-k", "--top-k", type=int, default=5, help="返回结果数量")
    args = parser.parse_args()
    
    print(f"🔍 搜索：{args.query}")
    print("=" * 50)
    
    results = search(args.query, args.top_k)
    
    if not results:
        print("❌ 未找到相关结果")
        return
    
    print(f"✅ 找到 {len(results)} 个相关文档:\n")
    for result in results:
        print(f"{result['rank']}. {result['source']}")
        print(f"   类型：{result['type']}")
        print(f"   相似度：{result['similarity']:.2%}")
        print(f"   分数：{result['score']:.4f}")
        print()

if __name__ == "__main__":
    main()
