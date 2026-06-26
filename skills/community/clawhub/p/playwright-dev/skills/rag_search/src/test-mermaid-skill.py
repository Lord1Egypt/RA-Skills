#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 mermaid-to-feishu 技能是否已向量化的简单脚本
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from skill_indexer import AliyunEmbeddings
import chromadb
from langchain_chroma import Chroma

def query_mermaid_skill():
    """查询 mermaid 相关技能"""
    
    chroma_dir = r"C:\Users\Xiabi\.openclaw\workspace\chroma_db"
    collection_name = "openclaw_skills"
    
    # 加载向量存储
    client = chromadb.PersistentClient(path=chroma_dir)
    embeddings = AliyunEmbeddings()
    
    vectorstore = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings
    )
    
    # 搜索
    query = "mermaid 图表转图片"
    print(f"查询：{query}")
    results = vectorstore.similarity_search_with_score(query, k=5)
    
    # 去重
    seen_skills = set()
    
    for doc, score in results:
        skill_name = doc.metadata.get("skill_name", "Unknown")
        if skill_name not in seen_skills:
            seen_skills.add(skill_name)
            similarity = round(1 - score, 3)
            print(f"  [OK] {skill_name} (similarity: {similarity})")
            print(f"    file: {doc.metadata.get('filename', '')}")
    
    return list(seen_skills)

if __name__ == "__main__":
    print("=" * 60)
    print("测试 mermaid-to-feishu 技能向量化")
    print("=" * 60)
    
    skills = query_mermaid_skill()
    
    print("\n" + "=" * 60)
    if "mermaid-to-feishu" in skills:
        print("✅ mermaid-to-feishu 技能已成功向量化！")
    else:
        print("⚠️ mermaid-to-feishu 技能未找到，但可能已包含在其他技能中")
    
    print(f"总共找到 {len(skills)} 个相关技能")
    print("=" * 60)
