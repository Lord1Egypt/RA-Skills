# Semantic Similarity Engine
# 语义相似度引擎 - 使用嵌入向量计算语义相似度

import os
import json
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import hashlib

# 尝试导入嵌入模型客户端
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


@dataclass
class EmbeddingCache:
    """嵌入向量缓存"""
    text_hash: str
    embedding: List[float]
    model: str
    timestamp: str


class SemanticSimilarityEngine:
    """语义相似度引擎 - 计算文本和神经元的语义相似度"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        
        # 嵌入模型配置
        self.model = self.config.get('embedding_model', 'text-embedding-ada-002')
        self.api_key = self.config.get('api_key') or os.environ.get('OPENAI_API_KEY')
        self.base_url = self.config.get('base_url') or os.environ.get('OPENAI_BASE_URL')
        
        # 缓存
        self._embedding_cache: Dict[str, EmbeddingCache] = {}  # text_hash -> embedding
        self._neuron_embeddings: Dict[str, List[float]] = {}   # neuron_id -> embedding
        
        # 缓存文件路径 - Auto-detect if not provided
        if self.config.get('cache_dir'):
            self.cache_dir = self.config['cache_dir']
        else:
            # Auto-detect cache directory
            from pathlib import Path
            if "NEURAL_MEMORY_PATH" in os.environ:
                base = os.environ["NEURAL_MEMORY_PATH"]
            elif "OPENCLAW_STATE_DIR" in os.environ:
                base = os.path.join(os.environ["OPENCLAW_STATE_DIR"], "neural-memory")
            else:
                base = os.path.join(Path.home(), ".openclaw", "neural-memory")
            self.cache_dir = os.path.join(base, "memory_long_term", "embeddings")
        
        self._ensure_cache_dir()
        self._load_cache()
        
        # 是否使用本地模式（当API不可用时）
        self.local_mode = not (HAS_OPENAI and self.api_key)
        if self.local_mode:
            print("[SemanticEngine] 使用本地模式（关键词相似度）")
        else:
            print(f"[SemanticEngine] 使用嵌入模型: {self.model}")
    
    def _ensure_cache_dir(self):
        """确保缓存目录存在"""
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _load_cache(self):
        """加载缓存"""
        cache_file = os.path.join(self.cache_dir, 'embedding_cache.json')
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data.get('embeddings', []):
                        self._embedding_cache[item['text_hash']] = EmbeddingCache(**item)
                    print(f"[SemanticEngine] 加载了 {len(self._embedding_cache)} 个缓存嵌入")
            except Exception as e:
                print(f"[SemanticEngine] 加载缓存失败: {e}")
        
        # 加载神经元嵌入索引
        neuron_index_file = os.path.join(self.cache_dir, 'neuron_embeddings.json')
        if os.path.exists(neuron_index_file):
            try:
                with open(neuron_index_file, 'r', encoding='utf-8') as f:
                    self._neuron_embeddings = json.load(f)
                    print(f"[SemanticEngine] 加载了 {len(self._neuron_embeddings)} 个神经元嵌入")
            except Exception as e:
                print(f"[SemanticEngine] 加载神经元嵌入失败: {e}")
    
    def _save_cache(self):
        """保存缓存"""
        cache_file = os.path.join(self.cache_dir, 'embedding_cache.json')
        try:
            data = {
                'embeddings': [e.__dict__ for e in self._embedding_cache.values()],
                'lastUpdated': __import__('datetime').datetime.now().isoformat()
            }
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[SemanticEngine] 保存缓存失败: {e}")
    
    def _save_neuron_embeddings(self):
        """保存神经元嵌入索引"""
        neuron_index_file = os.path.join(self.cache_dir, 'neuron_embeddings.json')
        try:
            with open(neuron_index_file, 'w', encoding='utf-8') as f:
                json.dump(self._neuron_embeddings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[SemanticEngine] 保存神经元嵌入失败: {e}")
    
    def _get_text_hash(self, text: str) -> str:
        """获取文本哈希"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """获取文本的嵌入向量"""
        if not text or not text.strip():
            return None
        
        text = text.strip()
        text_hash = self._get_text_hash(text)
        
        # 检查缓存
        if text_hash in self._embedding_cache:
            return self._embedding_cache[text_hash].embedding
        
        # 使用本地模式
        if self.local_mode:
            return None  # 本地模式不生成嵌入
        
        # 调用嵌入API
        try:
            embedding = self._call_embedding_api(text)
            if embedding:
                # 缓存结果
                from datetime import datetime
                self._embedding_cache[text_hash] = EmbeddingCache(
                    text_hash=text_hash,
                    embedding=embedding,
                    model=self.model,
                    timestamp=datetime.now().isoformat()
                )
                self._save_cache()
            return embedding
        except Exception as e:
            print(f"[SemanticEngine] 获取嵌入失败: {e}")
            return None
    
    def _call_embedding_api(self, text: str) -> Optional[List[float]]:
        """调用嵌入API"""
        if not HAS_OPENAI:
            return None
        
        try:
            client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            response = client.embeddings.create(
                model=self.model,
                input=text[:8000]  # 限制长度
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"[SemanticEngine] API调用失败: {e}")
            return None
    
    def compute_similarity(self, embedding_a: List[float], embedding_b: List[float]) -> float:
        """计算两个嵌入向量的余弦相似度"""
        if not embedding_a or not embedding_b:
            return 0.0
        
        vec_a = np.array(embedding_a)
        vec_b = np.array(embedding_b)
        
        dot_product = np.dot(vec_a, vec_b)
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return float(dot_product / (norm_a * norm_b))
    
    def compute_text_similarity(self, text_a: str, text_b: str) -> float:
        """计算两段文本的语义相似度"""
        # 如果是本地模式，使用关键词相似度
        if self.local_mode:
            return self._local_text_similarity(text_a, text_b)
        
        emb_a = self.get_embedding(text_a)
        emb_b = self.get_embedding(text_b)
        
        if emb_a and emb_b:
            return self.compute_similarity(emb_a, emb_b)
        
        # 降级到本地相似度
        return self._local_text_similarity(text_a, text_b)
    
    def _local_text_similarity(self, text_a: str, text_b: str) -> float:
        """本地文本相似度（基于关键词）"""
        if not text_a or not text_b:
            return 0.0
        
        # 简单的关键词重叠相似度
        words_a = set(text_a.lower().split())
        words_b = set(text_b.lower().split())
        
        if not words_a or not words_b:
            return 0.0
        
        intersection = len(words_a & words_b)
        union = len(words_a | words_b)
        
        # Jaccard 相似度
        jaccard = intersection / union if union > 0 else 0
        
        # 包含关系加分
        if text_a.lower() in text_b.lower() or text_b.lower() in text_a.lower():
            jaccard = max(jaccard, 0.7)
        
        return jaccard
    
    def index_neuron(self, neuron_id: str, name: str, content: str, tags: List[str] = None):
        """索引神经元的嵌入向量"""
        # 组合文本用于嵌入
        combined_text = f"{name}\n{content[:500]}"
        if tags:
            combined_text += f"\n{' '.join(tags)}"
        
        embedding = self.get_embedding(combined_text)
        if embedding:
            self._neuron_embeddings[neuron_id] = embedding
            self._save_neuron_embeddings()
            return True
        return False
    
    def search_similar_neurons(self, query: str, top_k: int = 10, 
                               threshold: float = 0.5) -> List[Tuple[str, float]]:
        """搜索与查询相似的神经元"""
        if self.local_mode:
            return self._local_search_similar(query, top_k, threshold)
        
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            return self._local_search_similar(query, top_k, threshold)
        
        results = []
        for neuron_id, neuron_embedding in self._neuron_embeddings.items():
            sim = self.compute_similarity(query_embedding, neuron_embedding)
            if sim >= threshold:
                results.append((neuron_id, sim))
        
        # 按相似度排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def _local_search_similar(self, query: str, top_k: int, threshold: float) -> List[Tuple[str, float]]:
        """本地相似度搜索（降级方案）"""
        # 这个方法需要与存储管理器配合使用
        # 返回空列表，由调用者处理
        return []
    
    def get_neuron_embedding(self, neuron_id: str) -> Optional[List[float]]:
        """获取神经元的嵌入向量"""
        return self._neuron_embeddings.get(neuron_id)
    
    def remove_neuron_embedding(self, neuron_id: str):
        """移除神经元的嵌入索引"""
        if neuron_id in self._neuron_embeddings:
            del self._neuron_embeddings[neuron_id]
            self._save_neuron_embeddings()
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'cached_embeddings': len(self._embedding_cache),
            'indexed_neurons': len(self._neuron_embeddings),
            'model': self.model,
            'local_mode': self.local_mode
        }
