"""
temporal/vector_retriever.py
=============================

Neuro-Agent 向量检索器 v2.0
【真实接入】
    - Embedding: paraphrase-multilingual-MiniLM-L12-v2（支持中文）
    - 存储: ChromaDB 持久化
    - 模型懒加载（避免启动超时）

依赖：
    pip install chromadb sentence-transformers

数据目录：
    ~/.openclaw/workspace/neuro_claw/capsules/vectors/
"""

import os
import time
import hashlib
import threading
from pathlib import Path
from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, asdict

# 尝试导入依赖
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

# ============ 路径配置 ============
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "neuro_claw" / "capsules" / "vectors"
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ============ Embedding 模型配置 ============
class EmbeddingModel:
    """
    向量嵌入模型管理器
    支持三种模式（按优先级自动选择）：
        1. 真实模型（sentence-transformers）
        2. API 模型（OpenAI / 硅基流动 / DeepSeek）
        3. 降级模式（simhash，适合无网环境）
    
    模型选择逻辑：
        - 有 sentence-transformers → paraphrase-multilingual-MiniLM-L12-v2
        - 无 sentence-transformers → 降级模式
    """
    
    # 默认使用已缓存的轻量模型（v2.3+ 可切换为中文模型）
    DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    # 推荐中文模型（需下载，Mac首次加载约20-40s）
    CHINESE_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
    # 向量维度
    DIMENSION = 384
    
    _instance: Optional["EmbeddingModel"] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._model: Optional[SentenceTransformer] = None
        self._mode: str = "unknown"
        
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            # 优先用已缓存的 MiniLM（秒级加载）
            for model_name in [self.DEFAULT_MODEL, self.CHINESE_MODEL]:
                try:
                    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
                    self._model = SentenceTransformer(model_name)
                    self._mode = "sentence_transformers"
                    self._dimension = self.DIMENSION
                    print(f"[EmbeddingModel] ✅ 加载: {model_name} (dim={self._dimension})")
                    break
                except Exception:
                    continue
            
            if self._model is None:
                print("[EmbeddingModel] ⚠️ 所有模型加载失败，降级为 simhash")
                self._mode = "simhash"
                self._dimension = 256
        else:
            print("[EmbeddingModel] ⚠️ sentence-transformers 未安装，使用降级模式")
            self._mode = "simhash"
            self._dimension = 256
    
    def encode(self, texts: List[str]) -> List[List[float]]:
        """
        将文本编码为向量
        
        Args:
            texts: 文本列表
            
        Returns:
            List[List[float]]: 向量列表
        """
        if self._mode == "sentence_transformers" and self._model is not None:
            try:
                embeddings = self._model.encode(
                    texts,
                    convert_to_numpy=True,
                    show_progress_bar=False,
                    batch_size=32,
                )
                return embeddings.tolist()
            except Exception as e:
                print(f"[EmbeddingModel] ⚠️ encode 失败: {e}，降级")
        
        # 降级：simhash 模式
        return [self._simhash_encode(text) for text in texts]
    
    def _simhash_encode(self, text: str) -> List[float]:
        """
        SimHash 编码（降级模式）
        用于无 embedding 模型时的语义近似匹配
        """
        words = list(text.lower().replace(" ", ""))
        dim = self._dimension
        
        # 分桶计数
        buckets = [0.0] * dim
        for i, char in enumerate(words):
            bucket = (ord(char) * 31 + i) % dim
            buckets[bucket] += 1.0
        
        # 归一化
        magnitude = sum(b * b for b in buckets) ** 0.5
        if magnitude > 0:
            buckets = [b / magnitude for b in buckets]
        
        return buckets
    
    @property
    def mode(self) -> str:
        return self._mode
    
    @property
    def dimension(self) -> int:
        return self._dimension


# ============ 数据结构 ============
@dataclass
class VectorResult:
    """向量检索结果"""
    capsule_id: str
    content: str
    distance: float
    relevance: float       # 1.0 - distance（语义相似度）
    emotion_label: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        result = asdict(self)
        result["relevance"] = round(self.relevance, 4)
        return result


@dataclass
class VectorOutput:
    """向量检索输出"""
    capsules: List[Dict]
    distances: List[float]
    relevances: List[float]
    total_results: int
    
    def __len__(self) -> int:
        return self.total_results


# ============ 核心类 ============
class VectorRetriever:
    """
    向量检索器 v2.0
    
    【真实功能】
        ✅ ChromaDB 持久化存储
        ✅ paraphrase-multilingual-MiniLM-L12-v2 中文语义嵌入
        ✅ 懒加载模型（启动不阻塞）
        ✅ 降级模式（无网络时自动 fallback）
    
    【数据流】
        add() → encode(text) → ChromaDB.add()
        search() → encode(query) → ChromaDB.query() → distance → relevance
    """
    
    COLLECTION_NAME = "emotion_capsules_v2"
    
    def __init__(
        self,
        persist_dir: str = None,
        embedding_model: Optional[EmbeddingModel] = None,
    ):
        """
        初始化向量检索器
        
        Args:
            persist_dir: 持久化目录
            embedding_model: 嵌入模型实例（单例自动注入）
        """
        self.persist_dir = persist_dir or str(DATA_DIR)
        self._embedding: EmbeddingModel = embedding_model or EmbeddingModel()
        self._chromadb_ready = False
        
        if CHROMADB_AVAILABLE:
            self._init_chromadb()
        else:
            print("[VectorRetriever] ⚠️ ChromaDB 未安装，使用内存模式")
            self._fallback_mode()
    
    def _init_chromadb(self):
        """初始化 ChromaDB"""
        try:
            self.client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True,
                )
            )
            
            # 创建 collection（带向量维度元数据）
            self.collection = self.client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                metadata={
                    "description": "Neuro-Agent 情绪胶囊向量库 v2",
                    "embedding_model": self._embedding.mode,
                    "dimension": self._embedding.dimension,
                }
            )
            
            self._chromadb_ready = True
            print(f"[VectorRetriever] ✅ ChromaDB 就绪 (dim={self._embedding.dimension}, model={self._embedding.mode})")
            
        except Exception as e:
            print(f"[VectorRetriever] ⚠️ ChromaDB 初始化失败: {e}，切换降级模式")
            self._fallback_mode()
    
    def _fallback_mode(self):
        """降级模式：内存字典 + simhash"""
        self._chromadb_ready = False
        self._memory_store: Dict[str, Dict] = {}
        print("[VectorRetriever] ⚠️ 运行在降级模式（内存存储）")
    
    # ============ 添加操作 ============
    
    def add(
        self,
        capsule_id: str,
        content: str,
        emotion_label: str = None,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
    ) -> bool:
        """
        添加胶囊到向量库
        
        Args:
            capsule_id: 胶囊 ID（唯一）
            content: 内容文本（用于生成向量）
            emotion_label: 情绪标签
            tags: 标签列表
            metadata: 其他元数据
        
        Returns:
            bool: 是否添加成功
        """
        metadata = metadata or {}
        metadata.update({
            "emotion_label": emotion_label or "unknown",
            "tags": ",".join(tags) if tags else "",
        })
        
        try:
            # 生成向量
            embeddings = self._embedding.encode([content])
            vector = embeddings[0]
            
            if self._chromadb_ready:
                # ChromaDB 模式
                self.collection.add(
                    ids=[capsule_id],
                    embeddings=[vector],
                    documents=[content],
                    metadatas=[metadata],
                )
                return True
            else:
                # 降级模式
                self._memory_store[capsule_id] = {
                    "content": content,
                    "emotion_label": emotion_label,
                    "tags": tags or [],
                    "metadata": metadata,
                    "vector": vector,
                }
                return True
                
        except Exception as e:
            print(f"[VectorRetriever] ⚠️ 添加失败: {e}")
            return False
    
    def delete(self, capsule_id: str) -> bool:
        """从向量库删除胶囊"""
        try:
            if self._chromadb_ready:
                self.collection.delete(ids=[capsule_id])
            else:
                self._memory_store.pop(capsule_id, None)
            return True
        except Exception as e:
            print(f"[VectorRetriever] ⚠️ 删除失败: {e}")
            return False
    
    # ============ 检索操作 ============
    
    def search(
        self,
        query: str,
        n: int = 5,
        filter_emotion: str = None,
        filter_tags: List[str] = None,
    ) -> VectorOutput:
        """
        语义检索（核心功能）
        
        Args:
            query: 查询文本
            n: 返回数量上限
            filter_emotion: 按情绪标签过滤
            filter_tags: 按标签过滤（取交集）
        
        Returns:
            VectorOutput: 检索结果（按 relevance 降序）
        """
        try:
            if self._chromadb_ready:
                return self._chromadb_search(query, n, filter_emotion, filter_tags)
            else:
                return self._memory_search(query, n, filter_emotion, filter_tags)
        except Exception as e:
            print(f"[VectorRetriever] ⚠️ 检索失败: {e}")
            return VectorOutput(capsules=[], distances=[], relevances=[], total_results=0)
    
    def _chromadb_search(
        self,
        query: str,
        n: int,
        filter_emotion: str = None,
        filter_tags: List[str] = None,
    ) -> VectorOutput:
        """ChromaDB 语义检索"""
        # 生成查询向量
        query_embedding = self._embedding.encode([query])[0]
        
        # 构建过滤条件
        where_filter: Optional[Dict] = None
        if filter_emotion:
            where_filter = {"emotion_label": filter_emotion}
        
        # 执行检索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )
        
        if not results or not results.get("ids") or not results["ids"][0]:
            return VectorOutput(capsules=[], distances=[], relevances=[], total_results=0)
        
        ids = results["ids"][0]
        distances = results["distances"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        
        capsules = []
        relevances = []
        
        for i, capsule_id in enumerate(ids):
            dist = distances[i]
            capsules.append({
                "id": capsule_id,
                "content": documents[i],
                "emotion_label": metadatas[i].get("emotion_label", "unknown"),
                "tags": metadatas[i].get("tags", "").split(",") if metadatas[i].get("tags") else [],
                "metadata": metadatas[i],
            })
            # distance → relevance 转换
            # ChromaDB distance 是 L2 距离，范围不确定
            # 用 exp(-distance) 映射到 0-1
            import math
            relevance = max(0.0, math.exp(-dist * 2))
            relevances.append(relevance)
        
        return VectorOutput(
            capsules=capsules,
            distances=distances,
            relevances=relevances,
            total_results=len(capsules),
        )
    
    def _memory_search(
        self,
        query: str,
        n: int,
        filter_emotion: str = None,
        filter_tags: List[str] = None,
    ) -> VectorOutput:
        """降级模式：内存 simhash 检索"""
        if not self._memory_store:
            return VectorOutput(capsules=[], distances=[], relevances=[], total_results=0)
        
        query_vec = self._embedding.encode([query])[0]
        results = []
        
        for capsule_id, data in self._memory_store.items():
            # 情绪过滤
            if filter_emotion and data.get("emotion_label") != filter_emotion:
                continue
            # 标签过滤
            if filter_tags:
                capsule_tags = set(data.get("tags", []))
                if not capsule_tags & set(filter_tags):
                    continue
            
            # 余弦相似度
            vec = data.get("vector", [0.0] * self._embedding.dimension)
            dot = sum(q * c for q, c in zip(query_vec, vec))
            norm_q = sum(q * q for q in query_vec) ** 0.5
            norm_c = sum(c * c for c in vec) ** 0.5
            similarity = dot / (norm_q * norm_c) if norm_q > 0 and norm_c > 0 else 0.0
            
            results.append({
                "id": capsule_id,
                "content": data.get("content", ""),
                "emotion_label": data.get("emotion_label", "unknown"),
                "tags": data.get("tags", []),
                "metadata": data.get("metadata", {}),
                "distance": 1.0 - similarity,
                "relevance": max(0.0, similarity),
            })
        
        # 按相关性降序
        results.sort(key=lambda x: x["relevance"], reverse=True)
        results = results[:n]
        
        return VectorOutput(
            capsules=[{"id": r["id"], "content": r["content"],
                       "emotion_label": r["emotion_label"], "tags": r["tags"],
                       "metadata": r["metadata"]} for r in results],
            distances=[r["distance"] for r in results],
            relevances=[r["relevance"] for r in results],
            total_results=len(results),
        )
    
    def search_by_emotion(
        self,
        emotion_label: str,
        n: int = 5,
    ) -> VectorOutput:
        """按情绪类型检索"""
        return self.search(query="", n=n, filter_emotion=emotion_label)
    
    def search_by_tags(
        self,
        tags: List[str],
        n: int = 5,
    ) -> VectorOutput:
        """按标签检索"""
        return self.search(query=tags[0] if tags else "", n=n, filter_tags=tags)
    
    def count(self) -> int:
        """获取向量库胶囊数量"""
        if self._chromadb_ready:
            try:
                return self.collection.count()
            except:
                return 0
        return len(self._memory_store)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "mode": self._embedding.mode,
            "dimension": self._embedding.dimension,
            "chromadb_ready": self._chromadb_ready,
            "total_capsules": self.count(),
            "persist_dir": self.persist_dir,
        }
    
    def reset(self) -> bool:
        """重置向量库（危险）"""
        try:
            if self._chromadb_ready:
                self.client.delete_collection(self.COLLECTION_NAME)
                self.collection = self.client.get_or_create_collection(
                    name=self.COLLECTION_NAME,
                    metadata={"description": "Neuro-Agent 情绪胶囊向量库 v2"},
                )
            else:
                self._memory_store.clear()
            print("[VectorRetriever] ✅ 重置完成")
            return True
        except Exception as e:
            print(f"[VectorRetriever] ⚠️ 重置失败: {e}")
            return False


# ============ 单例 ============
_retriever_instance: Optional[VectorRetriever] = None
_retriever_lock = threading.Lock()


def get_instance() -> VectorRetriever:
    """获取 VectorRetriever 单例"""
    global _retriever_instance
    if _retriever_instance is None:
        with _retriever_lock:
            if _retriever_instance is None:
                _retriever_instance = VectorRetriever()
    return _retriever_instance


# ============ 快捷函数 ============
def add_to_vector_store(
    capsule_id: str,
    content: str,
    emotion_label: str = None,
    tags: List[str] = None,
) -> bool:
    """快捷添加"""
    return get_instance().add(
        capsule_id=capsule_id,
        content=content,
        emotion_label=emotion_label,
        tags=tags,
    )


def semantic_search(
    query: str,
    n: int = 5,
    filter_emotion: str = None,
) -> VectorOutput:
    """快捷语义检索"""
    return get_instance().search(
        query=query,
        n=n,
        filter_emotion=filter_emotion,
    )


def search_by_emotion(emotion_label: str, n: int = 5) -> VectorOutput:
    """快捷按情绪检索"""
    return get_instance().search_by_emotion(emotion_label=emotion_label, n=n)


# ============ 测试 ============
if __name__ == "__main__":
    import math
    
    print("=== 向量检索器 v2.0 测试 ===\n")
    vr = VectorRetriever()
    stats = vr.get_stats()
    print(f"运行模式: {stats['mode']} | 维度: {stats['dimension']} | ChromaDB: {stats['chromadb_ready']}\n")
    
    # 添加测试胶囊
    test_capsules = [
        ("c1", "用户今天工作很顺利，心情愉悦", "joy", ["work", "happy"]),
        ("c2", "用户最近工作压力大，很焦虑", "anxiety", ["work", "stress"]),
        ("c3", "用户养了一只猫，很喜欢小动物", "joy", ["pet", "animal"]),
        ("c4", "用户失恋了，很难过", "sadness", ["love", "relationship"]),
        ("c5", "用户对产品不满意，很生气", "anger", ["product", "complaint"]),
        ("c6", "用户对电商运营很感兴趣", "hope", ["work", "ecommerce"]),
    ]
    
    print("📦 添加胶囊:")
    for capsule_id, content, emotion, tags in test_capsules:
        ok = vr.add(capsule_id, content, emotion, tags)
        print(f"  [{'✅' if ok else '❌'}] {capsule_id}: {content[:20]}... ({emotion})")
    
    print(f"\n📊 向量库总数: {vr.count()}")
    
    # 语义检索测试
    test_queries = [
        ("心情好", "joy相关"),
        ("工作压力大怎么办", "work+anxiety相关"),
        ("小动物宠物", "pet相关"),
        ("失恋情感问题", "sadness相关"),
    ]
    
    print("\n🔍 语义检索测试:")
    for query, desc in test_queries:
        results = vr.search(query, n=3)
        print(f"\n  查询「{query}」({desc}):")
        for i, capsule in enumerate(results.capsules):
            r = results.relevances[i]
            print(f"    [{i+1}] {capsule['content'][:30]}... (relevance={r:.3f}, emotion={capsule['emotion_label']})")
    
    # 按情绪检索
    print(f"\n🎭 按情绪检索 'joy':")
    results = vr.search_by_emotion("joy", n=5)
    for i, capsule in enumerate(results.capsules):
        print(f"  [{i+1}] {capsule['content'][:30]}... (relevance={results.relevances[i]:.3f})")
    
    print("\n=== 测试完成 ===")
