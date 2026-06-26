#!/usr/bin/env python3
"""
Memory Cell - 有生命力的记忆细胞
每个记忆都是一个有生命力的细胞，永不死亡，只是沉默
"""

import os
import sys
import json
import time
import uuid
import hashlib
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class CellState(Enum):
    """细胞生命状态"""
    ACTIVE = "active"           # 活跃态 - 能量 > 0.5
    DORMANT = "dormant"         # 休眠态 - 0.1 < 能量 <= 0.5
    HIBERNATE = "hibernate"     # 深度休眠 - 能量 <= 0.1


class SynapseType(Enum):
    """突触连接类型"""
    ASSOCIATIVE = "associative"     # 关联型 - 内容相关
    CAUSAL = "causal"               # 因果型 - 导致/被导致
    TEMPORAL = "temporal"           # 时序型 - 时间相关
    HIERARCHICAL = "hierarchical"   # 层级型 - 父/子
    SEMANTIC = "semantic"           # 语义型 - 含义相近
    CONTRADICTORY = "contradictory" # 矛盾型 - 相反内容


class CellGene(Enum):
    """细胞基因类型"""
    USER = "user"           # 用户画像
    FEEDBACK = "feedback"   # 反馈记忆
    PROJECT = "project"     # 项目记忆
    REFERENCE = "reference" # 引用记忆
    INSIGHT = "insight"     # 洞察记忆（分裂产生）
    PATTERN = "pattern"     # 模式记忆（分裂产生）


@dataclass
class Synapse:
    """突触连接 - 细胞间的神经链接"""
    source_id: str
    target_id: str
    synapse_type: SynapseType
    strength: float = 1.0           # 连接强度 (0-1)
    weight: float = 1.0             # 权重（影响脉冲传导）
    bidirectional: bool = True      # 是否双向
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    pulse_count: int = 0            # 通过此突触的脉冲次数
    
    def to_dict(self) -> Dict:
        return {
            'source_id': self.source_id,
            'target_id': self.target_id,
            'type': self.synapse_type.value,
            'strength': self.strength,
            'weight': self.weight,
            'bidirectional': self.bidirectional,
            'created_at': self.created_at,
            'pulse_count': self.pulse_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Synapse':
        return cls(
            source_id=data['source_id'],
            target_id=data['target_id'],
            synapse_type=SynapseType(data['type']),
            strength=data.get('strength', 1.0),
            weight=data.get('weight', 1.0),
            bidirectional=data.get('bidirectional', True),
            created_at=data.get('created_at', datetime.now().isoformat()),
            pulse_count=data.get('pulse_count', 0)
        )


@dataclass
class MemoryCell:
    """
    记忆细胞 - 有生命力的记忆单元
    
    核心特性：
    1. 永不死亡 - 只是沉默
    2. 能量驱动 - 决定活跃度
    3. 突触连接 - 形成神经网络
    4. 分裂能力 - 生发新细胞
    """
    # === 基因（不可变属性）===
    id: str
    gene: CellGene
    content: str                      # 记忆内容
    keywords: List[str] = field(default_factory=list)
    importance: float = 0.7           # 原始重要性
    trust_score: float = 0.5          # 可信度
    
    # === 状态（可变属性）===
    energy: float = 0.7               # 能量值 (0-1)
    state: CellState = CellState.ACTIVE
    age: int = 0                      # 年龄（天）
    access_count: int = 0             # 访问次数
    
    # === 时间戳 ===
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_active: str = field(default_factory=lambda: datetime.now().isoformat())
    last_pulse: str = ""              # 最后接收脉冲时间
    
    # === 突触网络 ===
    synapses: List[Synapse] = field(default_factory=list)
    
    # === 谱系（分裂相关）===
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    generation: int = 0               # 第几代细胞
    
    # === 能量参数 ===
    ENERGY_THRESHOLD_ACTIVE = 0.5
    ENERGY_THRESHOLD_DORMANT = 0.1
    ENERGY_DECAY_DAILY = 0.01         # 每天能量衰减
    ENERGY_BOOST_ACCESS = 0.1         # 访问能量增益
    ENERGY_BOOST_PULSE = 0.05         # 脉冲能量增益
    ENERGY_SPLIT_THRESHOLD = 0.8      # 分裂所需能量
    ENERGY_SPLIT_COST = 0.5           # 分裂能量消耗
    ENERGY_INHERIT_RATE = 0.3         # 子细胞继承比例
    
    def _update_state(self):
        """根据能量更新细胞状态"""
        if self.energy > self.ENERGY_THRESHOLD_ACTIVE:
            self.state = CellState.ACTIVE
        elif self.energy > self.ENERGY_THRESHOLD_DORMANT:
            self.state = CellState.DORMANT
        else:
            self.state = CellState.HIBERNATE
    
    def activate(self, strength: float = 1.0) -> float:
        """
        激活细胞
        
        Args:
            strength: 激活强度
        
        Returns:
            实际激活能量
        """
        # 增加能量
        boost = self.ENERGY_BOOST_ACCESS * strength
        self.energy = min(1.0, self.energy + boost)
        
        # 更新状态
        self._update_state()
        
        # 更新访问记录
        self.access_count += 1
        self.last_active = datetime.now().isoformat()
        
        return boost
    
    def receive_pulse(self, strength: float) -> float:
        """
        接收神经脉冲
        
        Args:
            strength: 脉冲强度
        
        Returns:
            实际接收能量
        """
        # 增加能量
        boost = self.ENERGY_BOOST_PULSE * strength
        self.energy = min(1.0, self.energy + boost)
        
        # 更新状态（可能唤醒）
        old_state = self.state
        self._update_state()
        
        # 记录脉冲
        self.last_pulse = datetime.now().isoformat()
        
        # 如果从休眠唤醒，记录
        if old_state == CellState.HIBERNATE and self.state != CellState.HIBERNATE:
            pass  # 可记录唤醒事件
        
        return boost
    
    def decay(self, days: float = 1.0) -> float:
        """
        能量衰减
        
        Args:
            days: 衰减天数
        
        Returns:
            衰减后的能量
        """
        self.energy = max(0.01, self.energy - self.ENERGY_DECAY_DAILY * days)
        self.age += int(days)
        self._update_state()
        return self.energy
    
    def can_split(self) -> bool:
        """判断是否可以分裂"""
        return (
            self.energy >= self.ENERGY_SPLIT_THRESHOLD and
            self.access_count >= 3 and
            len(self.children_ids) < 5  # 最多5个子细胞
        )
    
    def split(self, new_content: str, new_gene: CellGene = None) -> Optional['MemoryCell']:
        """
        细胞分裂 - 生发新记忆
        
        Args:
            new_content: 新细胞内容
            new_gene: 新细胞基因（默认继承）
        
        Returns:
            新分裂的细胞，如果无法分裂返回None
        """
        if not self.can_split():
            return None
        
        # 创建子细胞
        child_id = f"{self.id}_gen{self.generation + 1}_{uuid.uuid4().hex[:8]}"
        
        child = MemoryCell(
            id=child_id,
            gene=new_gene or self.gene,
            content=new_content,
            keywords=self._extract_keywords(new_content),
            importance=self.importance,
            trust_score=self.trust_score * 0.9,  # 稍降低可信度
            energy=self.energy * self.ENERGY_INHERIT_RATE,
            state=CellState.ACTIVE,
            parent_id=self.id,
            generation=self.generation + 1
        )
        
        # 母细胞能量消耗
        self.energy *= self.ENERGY_SPLIT_COST
        
        # 记录子细胞
        self.children_ids.append(child_id)
        
        # 创建突触连接
        synapse = Synapse(
            source_id=self.id,
            target_id=child_id,
            synapse_type=SynapseType.HIERARCHICAL,
            strength=1.0,
            weight=1.0
        )
        self.synapses.append(synapse)
        
        return child
    
    def connect(self, target_id: str, synapse_type: SynapseType,
                strength: float = 1.0, weight: float = 1.0,
                bidirectional: bool = True) -> Synapse:
        """
        建立突触连接
        
        Args:
            target_id: 目标细胞ID
            synapse_type: 突触类型
            strength: 连接强度
            weight: 权重
            bidirectional: 是否双向
        
        Returns:
            创建的突触
        """
        # 检查是否已存在
        for s in self.synapses:
            if s.target_id == target_id:
                # 更新已有连接
                s.strength = max(s.strength, strength)
                s.weight = max(s.weight, weight)
                return s
        
        synapse = Synapse(
            source_id=self.id,
            target_id=target_id,
            synapse_type=synapse_type,
            strength=strength,
            weight=weight,
            bidirectional=bidirectional
        )
        self.synapses.append(synapse)
        return synapse
    
    def strengthen_synapse(self, target_id: str, delta: float = 0.1):
        """强化突触连接"""
        for s in self.synapses:
            if s.target_id == target_id:
                s.strength = min(1.0, s.strength + delta)
                s.weight = min(2.0, s.weight + delta)
                s.pulse_count += 1
                break
    
    def _extract_keywords(self, content: str) -> List[str]:
        """
        提取关键词
        
        使用简单的中文分词策略，将内容拆分为有意义的词汇单元
        """
        import re
        
        # 提取中文字符和英文单词
        # 中文按常见标点分词，英文按空格分词
        keywords = set()
        
        # 提取英文单词（包括技术术语如FastAPI, PostgreSQL等）
        english_words = re.findall(r'[A-Za-z][A-Za-z0-9]*', content)
        keywords.update(w.lower() for w in english_words if len(w) > 1)
        
        # 提取中文词汇（简化处理：按标点和常用词分词）
        # 移除标点符号和空白
        chinese_text = re.sub(r'[，。！？、；：""''（）【】《» ]+', ' ', content)
        
        # 简单分词：提取2-4字的中文词组
        chinese_words = re.findall(r'[\u4e00-\u9fff]+', chinese_text)
        for word in chinese_words:
            if 2 <= len(word) <= 8:  # 排除单字和过长词
                keywords.add(word)
        
        # 停用词过滤
        stopwords = {'的', '是', '在', '和', '了', '有', '不', '这', '我', '你',
                     '他', '她', '它', '们', '个', '也', '都', '就', '着', '到',
                     'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                     'to', 'of', 'and', 'in', 'on', 'for', 'with', 'at'}
        
        keywords = [w for w in keywords if w not in stopwords]
        
        return list(keywords)[:20]
    
    def get_connected_cells(self) -> List[str]:
        """获取所有连接的细胞ID"""
        return [s.target_id for s in self.synapses]
    
    def is_alive(self) -> bool:
        """细胞是否存活（活跃或休眠）"""
        return self.state != CellState.HIBERNATE
    
    def is_silent(self) -> bool:
        """细胞是否沉默（深度休眠）"""
        return self.state == CellState.HIBERNATE
    
    def to_dict(self) -> Dict:
        """序列化为字典"""
        return {
            'id': self.id,
            'gene': self.gene.value,
            'content': self.content,
            'keywords': self.keywords,
            'importance': self.importance,
            'trust_score': self.trust_score,
            'energy': self.energy,
            'state': self.state.value,
            'age': self.age,
            'access_count': self.access_count,
            'created_at': self.created_at,
            'last_active': self.last_active,
            'last_pulse': self.last_pulse,
            'synapses': [s.to_dict() for s in self.synapses],
            'parent_id': self.parent_id,
            'children_ids': self.children_ids,
            'generation': self.generation
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryCell':
        """从字典反序列化"""
        return cls(
            id=data['id'],
            gene=CellGene(data['gene']),
            content=data['content'],
            keywords=data.get('keywords', []),
            importance=data.get('importance', 0.7),
            trust_score=data.get('trust_score', 0.5),
            energy=data.get('energy', 0.7),
            state=CellState(data.get('state', 'active')),
            age=data.get('age', 0),
            access_count=data.get('access_count', 0),
            created_at=data.get('created_at', datetime.now().isoformat()),
            last_active=data.get('last_active', datetime.now().isoformat()),
            last_pulse=data.get('last_pulse', ''),
            synapses=[Synapse.from_dict(s) for s in data.get('synapses', [])],
            parent_id=data.get('parent_id'),
            children_ids=data.get('children_ids', []),
            generation=data.get('generation', 0)
        )


def create_cell(content: str, gene: CellGene = CellGene.USER,
                importance: float = 0.7) -> MemoryCell:
    """
    创建新的记忆细胞
    
    Args:
        content: 记忆内容
        gene: 细胞基因类型
        importance: 重要性
    
    Returns:
        新创建的记忆细胞
    """
    cell_id = f"cell_{uuid.uuid4().hex[:12]}"
    
    cell = MemoryCell(
        id=cell_id,
        gene=gene,
        content=content,
        importance=importance,
        energy=importance  # 初始能量等于重要性
    )
    
    # 提取关键词
    cell.keywords = cell._extract_keywords(content)
    
    return cell


def main():
    parser = argparse.ArgumentParser(description="Memory Cell - 生命记忆单元")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # create命令
    create_parser = subparsers.add_parser("create", help="创建记忆细胞")
    create_parser.add_argument("--content", required=True, help="记忆内容")
    create_parser.add_argument("--type", default="user", 
                               choices=["user", "feedback", "project", "reference"],
                               help="细胞类型")
    create_parser.add_argument("--importance", type=float, default=0.7, help="重要性")
    
    # activate命令
    activate_parser = subparsers.add_parser("activate", help="激活细胞")
    activate_parser.add_argument("--id", required=True, help="细胞ID")
    activate_parser.add_argument("--strength", type=float, default=1.0, help="激活强度")
    
    # split命令
    split_parser = subparsers.add_parser("split", help="细胞分裂")
    split_parser.add_argument("--id", required=True, help="母细胞ID")
    split_parser.add_argument("--content", required=True, help="新细胞内容")
    
    # connect命令
    connect_parser = subparsers.add_parser("connect", help="建立突触连接")
    connect_parser.add_argument("--from", dest="source", required=True, help="源细胞ID")
    connect_parser.add_argument("--to", dest="target", required=True, help="目标细胞ID")
    connect_parser.add_argument("--type", default="associative", help="突触类型")
    
    args = parser.parse_args()
    
    if args.command == "create":
        gene_map = {
            "user": CellGene.USER,
            "feedback": CellGene.FEEDBACK,
            "project": CellGene.PROJECT,
            "reference": CellGene.REFERENCE
        }
        cell = create_cell(args.content, gene_map[args.type], args.importance)
        print(json.dumps(cell.to_dict(), ensure_ascii=False, indent=2))
        
    elif args.command == "activate":
        # 模拟激活
        print(f"[ACTIVATE] Cell {args.id} activated with strength {args.strength}")
        
    elif args.command == "split":
        print(f"[SPLIT] Creating child cell from {args.id}")
        
    elif args.command == "connect":
        synapse_type = SynapseType(args.type)
        print(f"[CONNECT] {args.source} --[{synapse_type.value}]--> {args.target}")


if __name__ == "__main__":
    main()
