#!/usr/bin/env python3
"""
多模态记忆系统
支持图像、音频等多模态记忆的编码和检索

功能:
- 图像记忆编码
- 音频记忆编码
- 跨模态检索
- 模态融合
"""

import json
import os
import base64
import hashlib
import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class ModalityType(Enum):
    """模态类型"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    MIXED = "mixed"


@dataclass
class MultimodalContent:
    """多模态内容"""
    modality: ModalityType
    content: Any
    embedding: Optional[List[float]] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class MultimodalMemory:
    """多模态记忆"""
    id: str
    modalities: Dict[ModalityType, MultimodalContent]
    created_time: str
    importance: float = 0.5
    access_count: int = 0


class ImageMemoryEncoder:
    """
    图像记忆编码器
    
    将图像编码为可记忆的向量表示
    """
    
    def __init__(self, storage_path: str = "./memory/images"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
    
    def encode(self, image_data: bytes, metadata: Dict = None) -> MultimodalContent:
        """编码图像"""
        # 计算图像哈希作为ID
        image_hash = hashlib.sha256(image_data).hexdigest()[:16]
        
        # 保存图像
        image_path = os.path.join(self.storage_path, f"{image_hash}.bin")
        with open(image_path, 'wb') as f:
            f.write(image_data)
        
        # 生成模拟的图像特征向量
        # 实际应用中应使用CNN等模型提取特征
        embedding = self._extract_features(image_data)
        
        return MultimodalContent(
            modality=ModalityType.IMAGE,
            content=image_hash,
            embedding=embedding,
            metadata={
                'path': image_path,
                'size': len(image_data),
                'hash': image_hash,
                **(metadata or {})
            }
        )
    
    def _extract_features(self, image_data: bytes) -> List[float]:
        """提取图像特征（模拟）"""
        # 使用图像数据的统计特征作为简化表示
        # 实际应使用预训练CNN模型
        
        # 生成确定性特征向量
        dim = 128
        embedding = []
        
        # 使用图像哈希生成基础向量
        hash_bytes = hashlib.sha256(image_data).digest()
        
        for i in range(dim):
            # 每4字节生成一个特征值
            start = (i * 4) % len(hash_bytes)
            val = int.from_bytes(hash_bytes[start:start+4], 'little')
            normalized = (val / (2**32 - 1)) * 2 - 1
            embedding.append(normalized)
        
        # 归一化
        norm = math.sqrt(sum(v * v for v in embedding))
        if norm > 0:
            embedding = [v / norm for v in embedding]
        
        return embedding
    
    def decode(self, content: MultimodalContent) -> Optional[bytes]:
        """解码图像"""
        if content.modality != ModalityType.IMAGE:
            return None
        
        path = content.metadata.get('path')
        if path and os.path.exists(path):
            with open(path, 'rb') as f:
                return f.read()
        
        return None
    
    def encode_from_base64(self, base64_str: str, metadata: Dict = None) -> MultimodalContent:
        """从Base64编码图像"""
        image_data = base64.b64decode(base64_str)
        return self.encode(image_data, metadata)


class AudioMemoryEncoder:
    """
    音频记忆编码器
    
    将音频编码为可记忆的向量表示
    """
    
    def __init__(self, storage_path: str = "./memory/audio"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
    
    def encode(self, audio_data: bytes, metadata: Dict = None) -> MultimodalContent:
        """编码音频"""
        audio_hash = hashlib.sha256(audio_data).hexdigest()[:16]
        
        audio_path = os.path.join(self.storage_path, f"{audio_hash}.bin")
        with open(audio_path, 'wb') as f:
            f.write(audio_data)
        
        embedding = self._extract_features(audio_data)
        
        return MultimodalContent(
            modality=ModalityType.AUDIO,
            content=audio_hash,
            embedding=embedding,
            metadata={
                'path': audio_path,
                'size': len(audio_data),
                'hash': audio_hash,
                **(metadata or {})
            }
        )
    
    def _extract_features(self, audio_data: bytes) -> List[float]:
        """提取音频特征（模拟）"""
        # 实际应使用MFCC、声谱图等特征
        
        dim = 128
        embedding = []
        
        # 使用音频数据的统计特征
        hash_bytes = hashlib.sha256(audio_data).digest()
        
        for i in range(dim):
            start = (i * 4) % len(hash_bytes)
            val = int.from_bytes(hash_bytes[start:start+4], 'little')
            normalized = (val / (2**32 - 1)) * 2 - 1
            embedding.append(normalized)
        
        norm = math.sqrt(sum(v * v for v in embedding))
        if norm > 0:
            embedding = [v / norm for v in embedding]
        
        return embedding
    
    def decode(self, content: MultimodalContent) -> Optional[bytes]:
        """解码音频"""
        if content.modality != ModalityType.AUDIO:
            return None
        
        path = content.metadata.get('path')
        if path and os.path.exists(path):
            with open(path, 'rb') as f:
                return f.read()
        
        return None


class MultimodalMemorySystem:
    """
    多模态记忆系统
    
    整合文本、图像、音频等多种模态的记忆
    """
    
    def __init__(self, memory_path: str = "./memory"):
        self.memory_path = memory_path
        
        # 编码器
        self.image_encoder = ImageMemoryEncoder(os.path.join(memory_path, 'images'))
        self.audio_encoder = AudioMemoryEncoder(os.path.join(memory_path, 'audio'))
        
        # 多模态记忆库
        self.memories: Dict[str, MultimodalMemory] = {}
        
        # 跨模态索引
        self.cross_modal_index: Dict[str, List[str]] = {}
        
        # 统计
        self.stats = {
            'total_memories': 0,
            'by_modality': {m.value: 0 for m in ModalityType},
            'cross_modal_links': 0
        }
        
        self._load_state()
    
    def create_memory(self, 
                      text: str = None,
                      image_data: bytes = None,
                      audio_data: bytes = None,
                      importance: float = 0.5,
                      metadata: Dict = None) -> MultimodalMemory:
        """创建多模态记忆"""
        memory_id = f"mm_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}"
        modalities = {}
        
        # 文本模态
        if text:
            text_embedding = self._encode_text(text)
            modalities[ModalityType.TEXT] = MultimodalContent(
                modality=ModalityType.TEXT,
                content=text,
                embedding=text_embedding,
                metadata=metadata or {}
            )
        
        # 图像模态
        if image_data:
            image_content = self.image_encoder.encode(image_data, metadata)
            modalities[ModalityType.IMAGE] = image_content
        
        # 音频模态
        if audio_data:
            audio_content = self.audio_encoder.encode(audio_data, metadata)
            modalities[ModalityType.AUDIO] = audio_content
        
        memory = MultimodalMemory(
            id=memory_id,
            modalities=modalities,
            created_time=datetime.now().isoformat(),
            importance=importance
        )
        
        self.memories[memory_id] = memory
        
        # 更新统计
        self.stats['total_memories'] += 1
        for modality in modalities.keys():
            self.stats['by_modality'][modality.value] += 1
        
        # 建立跨模态索引
        self._build_cross_modal_index(memory)
        
        self._save_state()
        return memory
    
    def _encode_text(self, text: str) -> List[float]:
        """编码文本（简化版向量）"""
        dim = 128
        embedding = []
        
        hash_bytes = hashlib.sha256(text.encode()).digest()
        
        for i in range(dim):
            start = (i * 4) % len(hash_bytes)
            val = int.from_bytes(hash_bytes[start:start+4], 'little')
            normalized = (val / (2**32 - 1)) * 2 - 1
            embedding.append(normalized)
        
        norm = math.sqrt(sum(v * v for v in embedding))
        if norm > 0:
            embedding = [v / norm for v in embedding]
        
        return embedding
    
    def _build_cross_modal_index(self, memory: MultimodalMemory) -> None:
        """建立跨模态索引"""
        # 相同记忆的不同模态互相关联
        modality_types = list(memory.modalities.keys())
        
        for i, m1 in enumerate(modality_types):
            for m2 in modality_types[i+1:]:
                key = f"{m1.value}_{m2.value}"
                if key not in self.cross_modal_index:
                    self.cross_modal_index[key] = []
                self.cross_modal_index[key].append(memory.id)
                self.stats['cross_modal_links'] += 1
    
    def search_by_text(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """文本检索"""
        query_embedding = self._encode_text(query)
        return self._search_by_embedding(query_embedding, ModalityType.TEXT, top_k)
    
    def search_by_image(self, image_data: bytes, top_k: int = 10) -> List[Tuple[str, float]]:
        """图像检索"""
        content = self.image_encoder.encode(image_data)
        return self._search_by_embedding(content.embedding, ModalityType.IMAGE, top_k)
    
    def search_by_audio(self, audio_data: bytes, top_k: int = 10) -> List[Tuple[str, float]]:
        """音频检索"""
        content = self.audio_encoder.encode(audio_data)
        return self._search_by_embedding(content.embedding, ModalityType.AUDIO, top_k)
    
    def _search_by_embedding(self, query_embedding: List[float],
                             modality: ModalityType,
                             top_k: int) -> List[Tuple[str, float]]:
        """向量检索"""
        results = []
        
        for memory_id, memory in self.memories.items():
            if modality in memory.modalities:
                content = memory.modalities[modality]
                if content.embedding:
                    similarity = self._cosine_similarity(query_embedding, content.embedding)
                    results.append((memory_id, similarity))
        
        results.sort(key=lambda x: -x[1])
        return results[:top_k]
    
    def cross_modal_search(self, 
                          query: str = None,
                          image_data: bytes = None,
                          audio_data: bytes = None,
                          top_k: int = 10) -> List[Tuple[str, float, List[ModalityType]]]:
        """
        跨模态检索
        
        使用一种模态查询，返回所有相关模态的结果
        """
        all_results = {}
        
        if query:
            text_results = self.search_by_text(query, top_k * 2)
            for memory_id, score in text_results:
                if memory_id not in all_results:
                    all_results[memory_id] = {'score': 0, 'modalities': []}
                all_results[memory_id]['score'] += score * 0.4
                all_results[memory_id]['modalities'].append(ModalityType.TEXT)
        
        if image_data:
            image_results = self.search_by_image(image_data, top_k * 2)
            for memory_id, score in image_results:
                if memory_id not in all_results:
                    all_results[memory_id] = {'score': 0, 'modalities': []}
                all_results[memory_id]['score'] += score * 0.4
                all_results[memory_id]['modalities'].append(ModalityType.IMAGE)
        
        if audio_data:
            audio_results = self.search_by_audio(audio_data, top_k * 2)
            for memory_id, score in audio_results:
                if memory_id not in all_results:
                    all_results[memory_id] = {'score': 0, 'modalities': []}
                all_results[memory_id]['score'] += score * 0.4
                all_results[memory_id]['modalities'].append(ModalityType.AUDIO)
        
        # 排序
        sorted_results = sorted(all_results.items(), key=lambda x: -x[1]['score'])
        
        return [(mid, data['score'], data['modalities']) 
                for mid, data in sorted_results[:top_k]]
    
    def get_memory(self, memory_id: str) -> Optional[MultimodalMemory]:
        """获取记忆"""
        return self.memories.get(memory_id)
    
    def get_memory_content(self, memory_id: str, 
                          modality: ModalityType) -> Optional[Any]:
        """获取记忆的特定模态内容"""
        memory = self.memories.get(memory_id)
        if not memory or modality not in memory.modalities:
            return None
        
        content = memory.modalities[modality]
        
        if modality == ModalityType.IMAGE:
            return self.image_encoder.decode(content)
        elif modality == ModalityType.AUDIO:
            return self.audio_encoder.decode(content)
        else:
            return content.content
    
    def fuse_modalities(self, memory_id: str) -> Optional[List[float]]:
        """融合多模态嵌入"""
        memory = self.memories.get(memory_id)
        if not memory:
            return None
        
        embeddings = [c.embedding for c in memory.modalities.values() 
                     if c.embedding]
        
        if not embeddings:
            return None
        
        # 平均融合
        dim = len(embeddings[0])
        fused = [0.0] * dim
        
        for emb in embeddings:
            for i in range(dim):
                fused[i] += emb[i]
        
        fused = [v / len(embeddings) for v in fused]
        
        # 归一化
        norm = math.sqrt(sum(v * v for v in fused))
        if norm > 0:
            fused = [v / norm for v in fused]
        
        return fused
    
    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """余弦相似度"""
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot / (norm1 * norm2)
    
    def _load_state(self) -> None:
        """加载状态"""
        state_file = os.path.join(self.memory_path, 'multimodal_state.json')
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                self.stats = data.get('stats', self.stats)
            except:
                pass
    
    def _save_state(self) -> None:
        """保存状态"""
        state_file = os.path.join(self.memory_path, 'multimodal_state.json')
        
        data = {
            'stats': self.stats
        }
        
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_report(self) -> Dict:
        """获取报告"""
        return {
            'stats': self.stats,
            'cross_modal_links': len(self.cross_modal_index)
        }


def demo_multimodal():
    """演示多模态系统"""
    print("=" * 60)
    print("多模态记忆系统演示")
    print("=" * 60)
    
    system = MultimodalMemorySystem()
    
    # 创建多模态记忆
    print("\n创建多模态记忆...")
    
    # 模拟图像数据
    fake_image = os.urandom(1024)
    # 模拟音频数据
    fake_audio = os.urandom(512)
    
    memory = system.create_memory(
        text="用户上传了一张项目架构图，并录音描述了设计思路",
        image_data=fake_image,
        audio_data=fake_audio,
        importance=0.8
    )
    
    print(f"创建记忆: {memory.id}")
    print(f"模态: {[m.value for m in memory.modalities.keys()]}")
    
    # 文本检索
    print("\n文本检索测试...")
    results = system.search_by_text("项目架构")
    print(f"找到 {len(results)} 条相关记忆")
    
    # 跨模态检索
    print("\n跨模态检索测试...")
    cross_results = system.cross_modal_search(query="项目")
    for mid, score, modalities in cross_results[:3]:
        print(f"  {mid}: 分数={score:.3f}, 模态={[m.value for m in modalities]}")
    
    # 模态融合
    print("\n模态融合测试...")
    fused = system.fuse_modalities(memory.id)
    if fused:
        print(f"融合向量维度: {len(fused)}")
        print(f"融合向量范数: {math.sqrt(sum(v*v for v in fused)):.3f}")
    
    # 报告
    print("\n系统报告:")
    report = system.get_report()
    for k, v in report.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    demo_multimodal()
