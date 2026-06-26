# Thinking Module Core Data Models
# 神经元和突触的核心数据结构

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Set
from datetime import datetime
import uuid
import json
import sys
import os

# 添加父目录到路径，确保包导入正常
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@dataclass
class Neuron:
    """神经元节点 - 代表一个知识概念"""
    id: str
    type: str  # concept|topic|insight|preference|personality
    name: str
    content: str
    tags: List[str]
    createdAt: str
    lastActivated: Optional[str]
    activationCount: int
    metadata: Dict[str, any]

    @classmethod
    def create(cls, type: str, name: str, content: str, tags: List[str] = None, metadata: Dict = None) -> 'Neuron':
        return cls(
            id=str(uuid.uuid4()),
            type=type,
            name=name,
            content=content,
            tags=tags or [],
            createdAt=datetime.now().isoformat(),
            lastActivated=None,
            activationCount=0,
            metadata=metadata or {}
        )

    def activate(self):
        """激活该神经元"""
        self.lastActivated = datetime.now().isoformat()
        self.activationCount += 1

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Neuron':
        return cls(**data)

@dataclass
class Synapse:
    """突触 - 连接两个神经元，代表知识关联"""
    id: str
    fromNeuron: str
    toNeuron: str
    type: str  # similarity|causality|opposition|example|analogy|...
    weight: float  # 0.0-1.0，突触强度
    confidence: float  # 0.0-1.0，连接置信度
    createdBy: str  # auto|user|reasoning
    createdAt: str
    lastReinforced: Optional[str]
    reinforcementCount: int
    metadata: Dict[str, any]

    @classmethod
    def create(cls, from_neuron: str, to_neuron: str, synapse_type: str,
               weight: float = 0.5, confidence: float = 0.7,
               created_by: str = "auto", metadata: Dict = None) -> 'Synapse':
        return cls(
            id=str(uuid.uuid4()),
            fromNeuron=from_neuron,
            toNeuron=to_neuron,
            type=synapse_type,
            weight=max(0.0, min(1.0, weight)),
            confidence=max(0.0, min(1.0, confidence)),
            createdBy=created_by,
            createdAt=datetime.now().isoformat(),
            lastReinforced=None,
            reinforcementCount=0,
            metadata=metadata or {}
        )

    def reinforce(self, delta: float = 0.1):
        """强化突触"""
        self.weight = min(1.0, self.weight + delta)
        self.lastReinforced = datetime.now().isoformat()
        self.reinforcementCount += 1

    def decay(self, factor: float = 0.95):
        """衰减突触（仅用于非受保护突触）"""
        self.weight = max(0.0, self.weight * factor)

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Synapse':
        # Set defaults for optional/missing fields
        if 'lastReinforced' not in data or data['lastReinforced'] is None:
            data['lastReinforced'] = None
        if 'reinforcementCount' not in data:
            data['reinforcementCount'] = 1
        if 'metadata' not in data:
            data['metadata'] = {}
        return cls(**data)

@dataclass
class ActivationRecord:
    """激活记录 - 记录每次查询的激活路径"""
    queryNeuronId: str
    timestamp: str
    activatedNeurons: Dict[str, float]  # neuron_id -> activation_value
    path: List[Dict]  # 激活传播路径
    parameters: Dict  # 查询参数

    @classmethod
    def create(cls, query_neuron_id: str, activated_neurons: Dict[str, float],
               path: List[Dict], parameters: Dict) -> 'ActivationRecord':
        return cls(
            queryNeuronId=query_neuron_id,
            timestamp=datetime.now().isoformat(),
            activatedNeurons=activated_neurons,
            path=path,
            parameters=parameters
        )

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'ActivationRecord':
        return cls(**data)
