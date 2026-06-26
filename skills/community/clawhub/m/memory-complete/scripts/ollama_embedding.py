#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama Embedding Integration
Ollama本地模型嵌入方案
"""

import requests
import json
import numpy as np
from typing import List, Optional, Dict

class OllamaEmbedding:
    """Ollama嵌入生成器"""

    def __init__(self, model: str = "nomic-embed-text",
                 base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/embeddings"
        self.dimension = None

    def check_connection(self) -> bool:
        """检查Ollama服务"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def embed(self, text: str) -> List[float]:
        """生成嵌入"""
        try:
            payload = {"model": self.model, "prompt": text}
            response = requests.post(self.api_url, json=payload, timeout=30)
            result = response.json()
            embedding = result.get('embedding', [])
            if embedding:
                self.dimension = len(embedding)
            return embedding
        except Exception as e:
            print(f"Embedding failed: {e}")
            return []

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量生成"""
        return [self.embed(text) for text in texts if text]

    def similarity(self, emb1: List[float], emb2: List[float]) -> float:
        """计算余弦相似度"""
        try:
            v1, v2 = np.array(emb1), np.array(emb2)
            dot = np.dot(v1, v2)
            norm1, norm2 = np.linalg.norm(v1), np.linalg.norm(v2)
            return dot / (norm1 * norm2) if norm1 and norm2 else 0.0
        except:
            return 0.0


class MemoryWithOllama:
    """集成Ollama的记忆系统"""

    def __init__(self, memory_system, ollama: OllamaEmbedding = None):
        self.memory = memory_system
        self.ollama = ollama or OllamaEmbedding()
        self.cache = {}

    def semantic_search(self, query: str, limit: int = 10) -> List[Dict]:
        """语义搜索"""
        if not self.ollama.check_connection():
            return self.memory.search(query, limit)

        # 生成查询嵌入
        query_emb = self.ollama.embed(query)
        if not query_emb:
            return self.memory.search(query, limit)

        # 获取所有记忆
        memories = self.memory.query(limit=1000)

        # 计算相似度
        results = []
        for mem in memories:
            text = f"{mem.get('title', '')} {mem.get('content', '')}"
            mem_emb = self.ollama.embed(text)
            if mem_emb:
                sim = self.ollama.similarity(query_emb, mem_emb)
                results.append((mem, sim))

        # 排序并返回
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results[:limit]]


# 推荐模型
RECOMMENDED_MODELS = {
    "nomic-embed-text": {"dim": 768, "size": "274MB", "desc": "轻量级"},
    "mxbai-embed-large": {"dim": 1024, "size": "669MB", "desc": "高精度"},
    "all-minilm": {"dim": 384, "size": "120MB", "desc": "超轻量"}
}

if __name__ == "__main__":
    ollama = OllamaEmbedding()
    if ollama.check_connection():
        print("Ollama ready!")
        emb = ollama.embed("test")
        print(f"Dimension: {len(emb)}")
    else:
        print("Ollama not available")
