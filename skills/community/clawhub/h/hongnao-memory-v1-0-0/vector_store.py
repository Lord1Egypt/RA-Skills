"""
弘脑记忆系统 - 向量存储层模块
HongNao Memory OS - Vector Store Layer

负责语义检索索引，包括：
- ChromaDB 向量数据库集成
- 文本 Embedding 向量化
- 相似度搜索与召回
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass


# ============================================================================
# 向量数据模型
# ============================================================================

@dataclass
class VectorDocument:
    """向量文档"""
    id: str
    text: str  # 原始文本
    embedding: Optional[List[float]]  # 向量表示
    metadata: Dict[str, Any]
    created_at: str
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'text': self.text,
            'embedding': self.embedding,
            'metadata': self.metadata,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'VectorDocument':
        return cls(**data)


# ============================================================================
# ChromaDB 向量存储
# ============================================================================

class ChromaVectorStore:
    """ChromaDB 向量存储"""
    
    def __init__(self, 
                 persist_directory: str = "chroma_db",
                 collection_name: str = "hongnao_memory",
                 embedding_function: Optional[Any] = None):
        """
        初始化 ChromaDB 向量存储
        
        Args:
            persist_directory: 持久化目录
            collection_name: 集合名称
            embedding_function: Embedding 函数（可选，默认使用模拟 Embedding）
        """
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        self._embedding_function = embedding_function or self._default_embedding
        self._client = None
        self._collection = None
        self._init_db()
    
    def _init_db(self):
        """初始化 ChromaDB"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            # 创建持久化客户端
            self._client = chromadb.PersistentClient(
                path=str(self.persist_directory),
                settings=Settings(anonymized_telemetry=False)
            )
            
            # 获取或创建集合
            self._collection = self._client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "弘脑记忆系统向量索引"}
            )
        except ImportError:
            print("⚠️  ChromaDB 未安装，使用内存模式")
            self._memory_store = {}
    
    def _default_embedding(self, text: str) -> List[float]:
        """
        默认 Embedding 函数（模拟）
        
        实际部署时应替换为真实的 Embedding 模型：
        - BGE-M3
        - M3E-Base
        - text2vec
        - 燧弘 MaaS 平台 Embedding 服务
        """
        # 简单的哈希模拟（仅用于测试）
        hash_value = hashlib.md5(text.encode()).hexdigest()
        # 生成 512 维向量
        return [float(ord(c) % 256) / 256.0 for c in hash_value] * 64
    
    def set_embedding_function(self, func):
        """设置自定义 Embedding 函数"""
        self._embedding_function = func
    
    # -------------------- 文档操作 --------------------
    
    def add_document(self, 
                     doc_id: str,
                     text: str,
                     metadata: Optional[Dict] = None,
                     embedding: Optional[List[float]] = None) -> bool:
        """
        添加向量文档
        
        Args:
            doc_id: 文档 ID
            text: 文本内容
            metadata: 元数据
            embedding: 向量（可选，默认自动计算）
        """
        if embedding is None:
            embedding = self._embedding_function(text)
        
        if metadata is None:
            metadata = {}
        
        doc = VectorDocument(
            id=doc_id,
            text=text,
            embedding=embedding,
            metadata=metadata,
            created_at=datetime.now().isoformat()
        )
        
        try:
            if hasattr(self, '_collection') and self._collection:
                self._collection.add(
                    ids=[doc_id],
                    embeddings=[embedding],
                    metadatas=[metadata],
                    documents=[text]
                )
            else:
                self._memory_store[doc_id] = doc.to_dict()
            return True
        except Exception as e:
            print(f"❌ 添加文档失败：{e}")
            return False
    
    def get_document(self, doc_id: str) -> Optional[VectorDocument]:
        """获取向量文档"""
        try:
            if hasattr(self, '_collection') and self._collection:
                result = self._collection.get(ids=[doc_id])
                if result and result['ids']:
                    return VectorDocument(
                        id=result['ids'][0],
                        text=result['documents'][0] if result['documents'] else "",
                        embedding=result['embeddings'][0] if result['embeddings'] else None,
                        metadata=result['metadatas'][0] if result['metadatas'] else {},
                        created_at=""  # ChromaDB 不存储创建时间
                    )
            else:
                doc_data = self._memory_store.get(doc_id)
                if doc_data:
                    return VectorDocument.from_dict(doc_data)
        except Exception as e:
            print(f"❌ 获取文档失败：{e}")
        return None
    
    def delete_document(self, doc_id: str) -> bool:
        """删除向量文档"""
        try:
            if hasattr(self, '_collection') and self._collection:
                self._collection.delete(ids=[doc_id])
            else:
                if doc_id in self._memory_store:
                    del self._memory_store[doc_id]
            return True
        except Exception as e:
            print(f"❌ 删除文档失败：{e}")
            return False
    
    # -------------------- 相似度搜索 --------------------
    
    def search_similar(self,
                       query_text: str,
                       top_k: int = 10,
                       filter_metadata: Optional[Dict] = None,
                       min_similarity: float = 0.5) -> List[Tuple[VectorDocument, float]]:
        """
        相似度搜索
        
        Args:
            query_text: 查询文本
            top_k: 返回数量
            filter_metadata: 元数据过滤条件
            min_similarity: 最小相似度阈值
        
        Returns:
            [(VectorDocument, 相似度分数), ...]
        """
        query_embedding = self._embedding_function(query_text)
        
        try:
            if hasattr(self, '_collection') and self._collection:
                results = self._collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    where=filter_metadata,
                    include=["documents", "metadatas", "embeddings", "distances"]
                )
                
                documents = []
                if results and results['ids'] and results['ids'][0]:
                    for i, doc_id in enumerate(results['ids'][0]):
                        distance = results['distances'][0][i] if results['distances'] else 0
                        similarity = 1.0 - distance  # ChromaDB 返回距离，转换为相似度
                        
                        if similarity >= min_similarity:
                            doc = VectorDocument(
                                id=doc_id,
                                text=results['documents'][0][i] if results['documents'] else "",
                                embedding=results['embeddings'][0][i] if results['embeddings'] else None,
                                metadata=results['metadatas'][0][i] if results['metadatas'] else {},
                                created_at=""
                            )
                            documents.append((doc, similarity))
                
                return documents
            else:
                # 内存模式：简单相似度计算
                return self._memory_search(query_text, query_embedding, top_k, min_similarity)
        
        except Exception as e:
            print(f"❌ 搜索失败：{e}")
            return []
    
    def _memory_search(self,
                       query_text: str,
                       query_embedding: List[float],
                       top_k: int,
                       min_similarity: float) -> List[Tuple[VectorDocument, float]]:
        """内存模式下的相似度搜索"""
        results = []
        
        for doc_id, doc_data in self._memory_store.items():
            # 计算余弦相似度
            doc_embedding = doc_data.get('embedding', [])
            if doc_embedding:
                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                if similarity >= min_similarity:
                    doc = VectorDocument.from_dict(doc_data)
                    results.append((doc, similarity))
        
        # 按相似度排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    # -------------------- 批量操作 --------------------
    
    def add_documents_batch(self, 
                            documents: List[VectorDocument]) -> int:
        """批量添加文档"""
        success_count = 0
        for doc in documents:
            if self.add_document(doc.id, doc.text, doc.metadata, doc.embedding):
                success_count += 1
        return success_count
    
    def upsert_document(self,
                        doc_id: str,
                        text: str,
                        metadata: Optional[Dict] = None,
                        embedding: Optional[List[float]] = None) -> bool:
        """插入或更新文档"""
        if self.get_document(doc_id):
            self.delete_document(doc_id)
        return self.add_document(doc_id, text, metadata, embedding)
    
    # -------------------- 统计与工具 --------------------
    
    def get_stats(self) -> Dict:
        """获取向量存储统计信息"""
        try:
            if hasattr(self, '_collection') and self._collection:
                count = self._collection.count()
                return {
                    'total_documents': count,
                    'collection_name': self.collection_name,
                    'persist_directory': str(self.persist_directory),
                    'mode': 'chromadb'
                }
            else:
                return {
                    'total_documents': len(self._memory_store),
                    'collection_name': self.collection_name,
                    'persist_directory': str(self.persist_directory),
                    'mode': 'memory'
                }
        except Exception as e:
            return {
                'total_documents': 0,
                'error': str(e)
            }
    
    def clear_collection(self):
        """清空集合"""
        try:
            if hasattr(self, '_collection') and self._collection:
                # ChromaDB 不支持直接清空，需要删除重建
                self._client.delete_collection(self.collection_name)
                self._collection = self._client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "弘脑记忆系统向量索引"}
                )
            else:
                self._memory_store = {}
        except Exception as e:
            print(f"❌ 清空集合失败：{e}")


# ============================================================================
# MaaS 平台 Embedding 服务集成
# ============================================================================

class MaaSEmbeddingService:
    """
    燧弘 MaaS 平台 Embedding 服务
    
    支持：
    - 火山方舟豆包 Embedding
    - DeepSeek Embedding
    - Qwen Embedding
    - BGE-M3 本地部署
    """
    
    def __init__(self, 
                 provider: str = "volcano",
                 api_key: Optional[str] = None,
                 model: str = "bge-m3"):
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self._client = None
    
    def embed(self, text: str) -> List[float]:
        """
        获取文本 Embedding 向量
        
        Returns:
            向量表示（维度取决于模型）
        """
        # TODO: 实现真实 MaaS 平台调用
        # 目前返回模拟向量
        return [0.1] * 1024
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量获取 Embedding"""
        return [self.embed(text) for text in texts]


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    # 测试向量存储
    vector_store = ChromaVectorStore(
        persist_directory="test_chroma_db",
        collection_name="test_memory"
    )
    
    # 添加测试文档
    test_docs = [
        VectorDocument(
            id="doc_001",
            text="燧弘华创采用 1+N+X 架构",
            metadata={"type": "fact", "project": "燧弘"},
            embedding=None,
            created_at=datetime.now().isoformat()
        ),
        VectorDocument(
            id="doc_002",
            text="弘脑记忆系统包含四层架构",
            metadata={"type": "fact", "project": "弘脑"},
            embedding=None,
            created_at=datetime.now().isoformat()
        ),
        VectorDocument(
            id="doc_003",
            text="用户偏好使用简洁的表达方式",
            metadata={"type": "preference", "user": "唐锋"},
            embedding=None,
            created_at=datetime.now().isoformat()
        )
    ]
    
    for doc in test_docs:
        vector_store.add_document(doc.id, doc.text, doc.metadata)
    
    # 测试相似度搜索
    query = "燧弘的架构是什么"
    results = vector_store.search_similar(query, top_k=2)
    
    print(f"查询：{query}")
    print(f"找到 {len(results)} 条相关记忆：\n")
    
    for doc, similarity in results:
        print(f"  相似度：{similarity:.3f}")
        print(f"  内容：{doc.text}")
        print(f"  元数据：{doc.metadata}")
        print()
    
    # 统计信息
    stats = vector_store.get_stats()
    print(f"向量存储统计：{json.dumps(stats, ensure_ascii=False, indent=2)}")
    
    print("\n✅ 向量存储层测试完成")
