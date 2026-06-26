"""
Vector Knowledge Memory for Enhanced MemCore
向量知识记忆模块 - 支持语义检索
"""

import numpy as np
from typing import List, Dict, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json


@dataclass
class KnowledgeDocument:
    """知识文档"""
    id: str
    content: str
    embedding: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    source: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    
    def touch(self):
        self.access_count += 1


class VectorKnowledgeMemory:
    """
    向量知识记忆
    支持语义相似度检索，无需精确关键词匹配
    """
    
    def __init__(
        self,
        embedding_fn: Optional[Callable[[str], List[float]]] = None,
        backend=None
    ):
        """
        Args:
            embedding_fn: 文本嵌入函数，如果为空则使用简单的词频向量
            backend: 可选的持久化后端
        """
        self.embedding_fn = embedding_fn or self._simple_embedding
        self.backend = backend
        self.documents: Dict[str, KnowledgeDocument] = {}
        self.embeddings: List[np.ndarray] = []
        self.doc_ids: List[str] = []
        
        # 如果有后端，加载已存储的知识
        if backend:
            self._load_from_backend()
    
    def _simple_embedding(self, text: str) -> List[float]:
        """
        简单的词频向量实现（无外部模型时使用）
        """
        # 简化的哈希向量
        hash_val = hashlib.md5(text.encode()).hexdigest()
        # 生成 128 维向量
        vec = [int(hash_val[i:i+2], 16) / 255.0 for i in range(0, 32, 2)]
        return vec
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """计算余弦相似度"""
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(vec1, vec2) / (norm1 * norm2))
    
    def add_knowledge(
        self,
        content: str,
        metadata: Optional[Dict] = None,
        source: str = "",
        doc_id: Optional[str] = None
    ) -> str:
        """
        添加知识
        
        Args:
            content: 知识内容
            metadata: 元数据（如主题、来源等）
            source: 来源标识
            doc_id: 自定义ID（默认生成）
            
        Returns:
            文档ID
        """
        doc_id = doc_id or f"know_{hashlib.md5(content.encode()).hexdigest()[:12]}"
        
        # 生成向量嵌入
        embedding = np.array(self.embedding_fn(content))
        
        doc = KnowledgeDocument(
            id=doc_id,
            content=content,
            embedding=embedding,
            metadata=metadata or {},
            source=source
        )
        
        self.documents[doc_id] = doc
        self.embeddings.append(embedding)
        self.doc_ids.append(doc_id)
        
        # 持久化
        if self.backend:
            self._save_to_backend(doc)
        
        return doc_id
    
    def query(
        self,
        query: str,
        top_k: int = 3,
        threshold: float = 0.0
    ) -> List[Tuple[KnowledgeDocument, float]]:
        """
        语义检索
        
        Args:
            query: 查询文本
            top_k: 返回最相似的k个结果
            threshold: 相似度阈值，低于此值的结果被过滤
            
        Returns:
            [(document, similarity_score), ...]
        """
        if not self.documents:
            return []
        
        # 生成查询向量
        query_vec = np.array(self.embedding_fn(query))
        
        # 计算所有相似度
        similarities = []
        for doc_id, doc in self.documents.items():
            if doc.embedding is not None:
                sim = self._cosine_similarity(query_vec, doc.embedding)
                if sim >= threshold:
                    similarities.append((doc, sim))
        
        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # 返回 top_k
        results = similarities[:top_k]
        
        # 更新访问计数
        for doc, _ in results:
            doc.touch()
        
        return results
    
    def query_with_context(
        self,
        query: str,
        context_topics: List[str] = None,
        top_k: int = 3
    ) -> List[Tuple[KnowledgeDocument, float]]:
        """
        带上下文的检索
        结合语义相似度和主题匹配
        """
        results = self.query(query, top_k=top_k * 2)  # 先获取更多候选
        
        if not context_topics:
            return results[:top_k]
        
        # 增强与上下文主题相关的结果
        boosted_results = []
        for doc, sim in results:
            boost = 0
            doc_topics = doc.metadata.get('topics', [])
            for topic in context_topics:
                if topic in doc_topics:
                    boost += 0.1  # 每匹配一个主题加 0.1 分
            boosted_results.append((doc, min(1.0, sim + boost)))
        
        # 重新排序
        boosted_results.sort(key=lambda x: x[1], reverse=True)
        return boosted_results[:top_k]
    
    def get_document(self, doc_id: str) -> Optional[KnowledgeDocument]:
        """获取特定文档"""
        return self.documents.get(doc_id)
    
    def delete_document(self, doc_id: str) -> bool:
        """删除文档"""
        if doc_id not in self.documents:
            return False
        
        del self.documents[doc_id]
        
        # 更新向量索引
        self.embeddings = []
        self.doc_ids = []
        for did, doc in self.documents.items():
            self.embeddings.append(doc.embedding)
            self.doc_ids.append(did)
        
        return True
    
    def update_metadata(self, doc_id: str, metadata: Dict) -> bool:
        """更新文档元数据"""
        if doc_id not in self.documents:
            return False
        
        self.documents[doc_id].metadata.update(metadata)
        
        if self.backend:
            self._save_to_backend(self.documents[doc_id])
        
        return True
    
    def get_related_documents(
        self,
        doc_id: str,
        top_k: int = 5
    ) -> List[Tuple[KnowledgeDocument, float]]:
        """
        查找与指定文档相关的其他文档
        """
        doc = self.documents.get(doc_id)
        if not doc or doc.embedding is None:
            return []
        
        related = []
        for other_id, other_doc in self.documents.items():
            if other_id != doc_id and other_doc.embedding is not None:
                sim = self._cosine_similarity(doc.embedding, other_doc.embedding)
                related.append((other_doc, sim))
        
        related.sort(key=lambda x: x[1], reverse=True)
        return related[:top_k]
    
    def export_knowledge(self, topic: Optional[str] = None) -> List[Dict]:
        """
        导出知识（用于备份或迁移）
        """
        results = []
        for doc in self.documents.values():
            if topic is None or topic in doc.metadata.get('topics', []):
                results.append({
                    'id': doc.id,
                    'content': doc.content,
                    'metadata': doc.metadata,
                    'source': doc.source,
                    'created_at': doc.created_at.isoformat()
                })
        return results
    
    def import_knowledge(self, knowledge_list: List[Dict]):
        """
        导入知识
        """
        for item in knowledge_list:
            self.add_knowledge(
                content=item['content'],
                metadata=item.get('metadata', {}),
                source=item.get('source', 'imported'),
                doc_id=item.get('id')
            )
    
    def _save_to_backend(self, doc: KnowledgeDocument):
        """保存到后端"""
        if not self.backend:
            return
        
        data = {
            doc.id: {
                'content': doc.content,
                'embedding': doc.embedding.tolist() if doc.embedding is not None else None,
                'metadata': doc.metadata,
                'source': doc.source,
                'created_at': doc.created_at.isoformat(),
                'access_count': doc.access_count
            }
        }
        
        if hasattr(self.backend, 'save'):
            self.backend.save('knowledge', data)
        elif hasattr(self.backend, 'save_knowledge'):
            self.backend.save_knowledge(doc)
    
    def _load_from_backend(self):
        """从后端加载"""
        if not self.backend:
            return
        
        if hasattr(self.backend, 'load'):
            data = self.backend.load('knowledge')
            for doc_id, item in data.items():
                doc = KnowledgeDocument(
                    id=doc_id,
                    content=item['content'],
                    embedding=np.array(item['embedding']) if item.get('embedding') else None,
                    metadata=item.get('metadata', {}),
                    source=item.get('source', ''),
                    created_at=datetime.fromisoformat(item['created_at']),
                    access_count=item.get('access_count', 0)
                )
                self.documents[doc_id] = doc
                self.embeddings.append(doc.embedding)
                self.doc_ids.append(doc_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'total_documents': len(self.documents),
            'total_embeddings': len(self.embeddings),
            'avg_document_length': sum(len(d.content) for d in self.documents.values()) / max(len(self.documents), 1),
            'top_sources': self._count_sources()
        }
    
    def _count_sources(self) -> Dict[str, int]:
        """统计来源分布"""
        sources = {}
        for doc in self.documents.values():
            src = doc.source or 'unknown'
            sources[src] = sources.get(src, 0) + 1
        return sources


# 集成 OpenAI Embedding 的示例
class OpenAIEmbeddingWrapper:
    """OpenAI Embedding 包装器"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("Please install openai: pip install openai")
    
    def __call__(self, text: str) -> List[float]:
        """生成嵌入向量"""
        response = self.client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding


# 测试代码
if __name__ == "__main__":
    print("🧠 测试 Vector Knowledge Memory...")
    
    # 创建知识库
    knowledge = VectorKnowledgeMemory()
    
    # 添加知识
    knowledge.add_knowledge(
        content="MemCore 是一个五层记忆架构的 AI Agent 记忆系统",
        metadata={"topics": ["MemCore", "AI", "architecture"]},
        source="github"
    )
    
    knowledge.add_knowledge(
        content="遗忘曲线基于艾宾浩斯记忆公式 R = e^(-t/S)",
        metadata={"topics": ["forgetting_curve", "psychology"]},
        source="wikipedia"
    )
    
    knowledge.add_knowledge(
        content="情景记忆可以记录具体事件和结论",
        metadata={"topics": ["episodic_memory", "MemCore"]},
        source="docs"
    )
    
    # 测试查询
    print("\n🔍 测试查询 '记忆架构':")
    results = knowledge.query("记忆架构是什么", top_k=2)
    for doc, score in results:
        print(f"   - {doc.content[:50]}... (相似度: {score:.3f})")
    
    # 测试上下文检索
    print("\n🔍 测试带上下文的查询 '记忆' (上下文: MemCore):")
    results = knowledge.query_with_context(
        "记忆系统",
        context_topics=["MemCore"],
        top_k=2
    )
    for doc, score in results:
        print(f"   - {doc.content[:50]}... (增强后相似度: {score:.3f})")
    
    print("\n📊 统计:", knowledge.get_stats())
    print("✅ 向量知识测试完成!")
