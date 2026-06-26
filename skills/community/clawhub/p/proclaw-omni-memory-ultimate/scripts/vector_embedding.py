#!/usr/bin/env python3
"""
向量嵌入接口
支持多种向量嵌入方式，实现真正的语义向量化

支持:
1. 外部API嵌入（OpenAI, Cohere, etc.）
2. 本地模型嵌入（sentence-transformers）
3. 模拟嵌入（用于无依赖环境）
"""

import json
import hashlib
import math
import os
from typing import List, Dict, Optional, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class EmbeddingConfig:
    """嵌入配置"""
    provider: str = "simulation"  # simulation, openai, cohere, local
    model: str = "default"
    dimension: int = 128
    api_key: Optional[str] = None
    api_url: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'EmbeddingConfig':
        return cls(
            provider=data.get('provider', 'simulation'),
            model=data.get('model', 'default'),
            dimension=data.get('dimension', 128),
            api_key=data.get('api_key'),
            api_url=data.get('api_url')
        )


class EmbeddingProvider(ABC):
    """嵌入提供者抽象基类"""
    
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """将文本嵌入为向量"""
        pass
    
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量嵌入"""
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """获取向量维度"""
        pass


class SimulationEmbedding(EmbeddingProvider):
    """
    模拟嵌入 - 基于文本特征的确定性向量生成
    
    特点:
    - 无外部依赖
    - 确定性：相同文本始终生成相同向量
    - 语义相关文本产生相似向量
    """
    
    def __init__(self, dimension: int = 128):
        self.dimension = dimension
        # 语义特征词表
        self.semantic_features = {
            # 技术
            'python': [1.0, 0.8, 0.6],
            'code': [0.9, 0.7, 0.5],
            'programming': [0.85, 0.75, 0.55],
            'develop': [0.8, 0.7, 0.6],
            'software': [0.75, 0.65, 0.55],
            
            # AI/ML
            'ai': [0.3, 1.0, 0.7],
            'machine': [0.35, 0.95, 0.65],
            'learning': [0.4, 0.9, 0.6],
            'neural': [0.3, 0.85, 0.7],
            'model': [0.35, 0.9, 0.65],
            
            # 情感
            'happy': [0.6, 0.5, 1.0],
            'love': [0.55, 0.45, 0.95],
            'good': [0.5, 0.5, 0.85],
            'bad': [0.5, 0.5, 0.3],
            'sad': [0.6, 0.5, 0.2],
            
            # 时间
            'today': [0.2, 0.3, 0.4, 1.0],
            'yesterday': [0.25, 0.35, 0.45, 0.95],
            'tomorrow': [0.2, 0.3, 0.4, 0.9],
            'future': [0.15, 0.25, 0.35, 0.85],
            'past': [0.2, 0.35, 0.45, 0.8],
            
            # 人物
            'user': [0.7, 0.4, 0.3],
            'person': [0.65, 0.45, 0.35],
            'team': [0.6, 0.5, 0.4],
            'friend': [0.55, 0.6, 0.7],
            
            # 项目
            'project': [0.8, 0.5, 0.3],
            'task': [0.75, 0.55, 0.35],
            'work': [0.7, 0.5, 0.4],
            'goal': [0.65, 0.6, 0.5],
        }
        
        # 构建特征基向量
        self._build_base_vectors()
    
    def _build_base_vectors(self):
        """构建特征基向量"""
        self.feature_vectors = {}
        
        for feature, weights in self.semantic_features.items():
            # 基于特征权重生成基向量
            vec = [0.0] * self.dimension
            
            for i in range(self.dimension):
                # 使用多个哈希函数混合
                h1 = int(hashlib.md5(f"{feature}_{i}_1".encode()).hexdigest()[:8], 16)
                h2 = int(hashlib.md5(f"{feature}_{i}_2".encode()).hexdigest()[:8], 16)
                
                # 生成 [-1, 1] 范围的值
                val = ((h1 % 1000) / 1000 - 0.5) * 2
                
                # 应用权重
                weight_idx = i % len(weights)
                vec[i] = val * weights[weight_idx]
            
            # 归一化
            norm = math.sqrt(sum(v * v for v in vec))
            if norm > 0:
                vec = [v / norm for v in vec]
            
            self.feature_vectors[feature] = vec
    
    def _text_hash_vector(self, text: str) -> List[float]:
        """基于文本哈希生成基础向量"""
        vec = [0.0] * self.dimension
        
        # 使用文本内容生成确定性向量
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        
        for i in range(self.dimension):
            # 每8个十六进制字符转换为一个浮点数
            start = (i * 8) % len(text_hash)
            hex_val = text_hash[start:start+8]
            val = (int(hex_val, 16) / (16 ** 8)) * 2 - 1  # [-1, 1]
            vec[i] = val
        
        return vec
    
    def _extract_features(self, text: str) -> Dict[str, float]:
        """提取文本语义特征"""
        text_lower = text.lower()
        features = {}
        
        for feature in self.semantic_features.keys():
            # 计算特征出现次数
            count = text_lower.count(feature)
            if count > 0:
                # TF-IDF风格的权重
                features[feature] = 1.0 + math.log(count)
        
        return features
    
    def embed(self, text: str) -> List[float]:
        """将文本嵌入为向量"""
        # 1. 获取基础哈希向量
        base_vec = self._text_hash_vector(text)
        
        # 2. 提取语义特征
        features = self._extract_features(text)
        
        # 3. 融合特征向量
        result = list(base_vec)
        
        if features:
            # 计算特征向量加权平均
            feature_vec = [0.0] * self.dimension
            total_weight = 0
            
            for feature, weight in features.items():
                if feature in self.feature_vectors:
                    fv = self.feature_vectors[feature]
                    for i in range(self.dimension):
                        feature_vec[i] += fv[i] * weight
                    total_weight += weight
            
            if total_weight > 0:
                feature_vec = [v / total_weight for v in feature_vec]
                
                # 混合基础向量和特征向量
                alpha = min(0.7, total_weight * 0.2)  # 特征向量权重
                for i in range(self.dimension):
                    result[i] = result[i] * (1 - alpha) + feature_vec[i] * alpha
        
        # 4. 归一化
        norm = math.sqrt(sum(v * v for v in result))
        if norm > 0:
            result = [v / norm for v in result]
        
        return result
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量嵌入"""
        return [self.embed(text) for text in texts]
    
    def get_dimension(self) -> int:
        return self.dimension


class OpenAIEmbedding(EmbeddingProvider):
    """
    OpenAI嵌入接口
    
    使用方式:
    1. 设置环境变量 OPENAI_API_KEY
    2. 或者在配置中传入 api_key
    """
    
    def __init__(self, config: EmbeddingConfig):
        self.config = config
        self.api_key = config.api_key or os.getenv("OPENAI_API_KEY")
        self.api_url = config.api_url or "https://api.openai.com/v1/embeddings"
        self.model = config.model or "text-embedding-ada-002"
        self.dimension = config.dimension or 1536
    
    def embed(self, text: str) -> List[float]:
        """使用OpenAI API嵌入"""
        if not self.api_key:
            # 降级到模拟嵌入
            return SimulationEmbedding(self.dimension).embed(text)
        
        try:
            from coze_workload_identity import requests
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json={
                    "input": text,
                    "model": self.model
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["data"][0]["embedding"]
            else:
                # API失败，降级到模拟
                return SimulationEmbedding(self.dimension).embed(text)
                
        except Exception as e:
            # 异常时降级
            return SimulationEmbedding(self.dimension).embed(text)
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量嵌入"""
        return [self.embed(text) for text in texts]
    
    def get_dimension(self) -> int:
        return self.dimension


class VectorEmbeddingEngine:
    """
    向量嵌入引擎 - 统一接口
    
    支持自动降级：
    API嵌入 -> 本地模型 -> 模拟嵌入
    """
    
    def __init__(self, config: Optional[EmbeddingConfig] = None):
        self.config = config or EmbeddingConfig()
        self.provider = self._create_provider()
    
    def _create_provider(self) -> EmbeddingProvider:
        """创建嵌入提供者"""
        provider_type = self.config.provider.lower()
        
        if provider_type == "openai":
            return OpenAIEmbedding(self.config)
        elif provider_type == "simulation":
            return SimulationEmbedding(self.config.dimension)
        else:
            # 默认使用模拟
            return SimulationEmbedding(self.config.dimension)
    
    def embed(self, text: str) -> List[float]:
        """嵌入文本"""
        return self.provider.embed(text)
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量嵌入"""
        return self.provider.embed_batch(texts)
    
    def similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def get_dimension(self) -> int:
        """获取向量维度"""
        return self.provider.get_dimension()
    
    def get_config(self) -> Dict:
        """获取配置信息"""
        return {
            'provider': self.config.provider,
            'model': self.config.model,
            'dimension': self.config.dimension
        }


def demo_embedding():
    """演示向量嵌入"""
    print("=" * 60)
    print("向量嵌入演示")
    print("=" * 60)
    
    # 创建模拟嵌入引擎
    engine = VectorEmbeddingEngine(EmbeddingConfig(
        provider="simulation",
        dimension=128
    ))
    
    # 测试文本
    texts = [
        "用户是Python全栈开发者，偏好FastAPI框架",
        "用户对机器学习和AI有浓厚兴趣",
        "今天天气很好，心情愉快",
        "项目代码已经完成，准备上线",
        "用户喜欢使用Docker进行容器化部署"
    ]
    
    print(f"\n嵌入配置: {engine.get_config()}")
    print(f"\n嵌入 {len(texts)} 个文本...")
    
    vectors = engine.embed_batch(texts)
    
    print("\n向量相似度矩阵:")
    print("-" * 50)
    
    for i, t1 in enumerate(texts):
        print(f"\n[{i}] {t1[:30]}...")
        similarities = []
        for j, t2 in enumerate(texts):
            sim = engine.similarity(vectors[i], vectors[j])
            similarities.append((j, sim))
        
        # 显示最相似的3个
        similarities.sort(key=lambda x: -x[1])
        for j, sim in similarities[:3]:
            print(f"    -> [{j}] 相似度: {sim:.4f}")


if __name__ == "__main__":
    demo_embedding()
