#!/usr/bin/env python3
"""
本地向量数据库
基于 ChromaDB 实现，完全离线运行
"""

import os
import yaml
import hashlib
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Chunk:
    """文本块"""
    id: str
    content: str
    metadata: Dict
    embedding: Optional[List[float]] = None


class VectorStore:
    """
    本地向量数据库
    存储文档向量，支持语义检索
    """
    
    def __init__(self, db_path: str = None, config_path: str = None):
        """
        初始化向量数据库
        
        Args:
            db_path: 数据库路径，默认使用本地目录
            config_path: 配置文件路径
        """
        if db_path is None:
            base_dir = Path(__file__).parent.parent
            db_path = base_dir / "data" / "vector_db"
        
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        self.config = self._load_config(config_path)
        self.collection = {}
        self.embedding_model = None
        
        self._init_embedding_model()
    
    def _load_config(self, config_path: str = None) -> Dict:
        """加载配置"""
        if config_path is None:
            base_dir = Path(__file__).parent.parent
            config_path = base_dir / "config" / "model_config.yaml"
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except:
            return {}
    
    def _init_embedding_model(self):
        """初始化嵌入模型"""
        # 模拟初始化，实际应该加载 BGE-M3 等模型
        print(f"[VectorStore] 向量数据库初始化完成 (模拟模式)")
        print(f"[VectorStore] 存储路径: {self.db_path}")
    
    def add_document(self, document: 'Document') -> str:
        """
        添加文档到向量库
        
        Args:
            document: 文档对象
            
        Returns:
            文档 ID
        """
        doc_id = document.id
        
        # 为每个分片生成向量
        for chunk in document.chunks:
            chunk_id = chunk.get("id")
            content = chunk.get("content", "")
            
            # 生成向量（模拟）
            embedding = self._embed_text(content)
            
            # 存储
            self.collection[chunk_id] = Chunk(
                id=chunk_id,
                content=content,
                metadata={
                    "doc_id": doc_id,
                    "doc_title": document.title,
                    "page": chunk.get("page", 1)
                },
                embedding=embedding
            )
        
        print(f"[VectorStore] 添加文档: {document.title}, 分片数: {len(document.chunks)}")
        return doc_id
    
    def search(self, query: str, top_k: int = 5, doc_id: str = None) -> List[Chunk]:
        """
        语义检索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            doc_id: 限制检索范围（可选）
            
        Returns:
            匹配的文本块列表
        """
        query_embedding = self._embed_text(query)
        
        results = []
        for chunk_id, chunk in self.collection.items():
            # 过滤文档
            if doc_id and chunk.metadata.get("doc_id") != doc_id:
                continue
            
            # 计算相似度（模拟）
            score = self._cosine_similarity(query_embedding, chunk.embedding)
            
            results.append((chunk, score))
        
        # 排序并返回前 K 个
        results.sort(key=lambda x: x[1], reverse=True)
        return [chunk for chunk, score in results[:top_k]]
    
    def delete(self, doc_id: str) -> bool:
        """
        删除文档
        
        Args:
            doc_id: 文档 ID
            
        Returns:
            是否成功
        """
        to_delete = []
        for chunk_id, chunk in self.collection.items():
            if chunk.metadata.get("doc_id") == doc_id:
                to_delete.append(chunk_id)
        
        for chunk_id in to_delete:
            del self.collection[chunk_id]
        
        print(f"[VectorStore] 删除文档: {doc_id}, 删除分片: {len(to_delete)}")
        return True
    
    def clear(self):
        """清空数据库"""
        self.collection.clear()
        print("[VectorStore] 数据库已清空")
    
    def list_documents(self) -> List[Dict]:
        """列出所有文档"""
        docs = {}
        for chunk in self.collection.values():
            doc_id = chunk.metadata.get("doc_id")
            if doc_id not in docs:
                docs[doc_id] = {
                    "id": doc_id,
                    "title": chunk.metadata.get("doc_title", ""),
                    "chunk_count": 0
                }
            docs[doc_id]["chunk_count"] += 1
        
        return list(docs.values())
    
    def _embed_text(self, text: str) -> List[float]:
        """
        文本向量化（模拟实现）
        
        实际应该使用 BGE-M3 等模型生成 1024 维向量
        """
        # 模拟向量：基于文本哈希生成固定维度的向量
        import random
        random.seed(hash(text))
        
        # 生成 128 维模拟向量
        dim = 128
        return [random.random() for _ in range(dim)]
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """计算余弦相似度"""
        import math
        
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)


# 单例模式
_store_instance = None


def get_vector_store() -> VectorStore:
    """获取向量数据库单例"""
    global _store_instance
    if _store_instance is None:
        _store_instance = VectorStore()
    return _store_instance
