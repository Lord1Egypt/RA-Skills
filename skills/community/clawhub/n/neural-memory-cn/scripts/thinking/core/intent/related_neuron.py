# Related Neuron Data Model
# 相关神经元数据模型 - 表示查询结果中的相关神经元

from dataclasses import dataclass, asdict
from typing import Optional, Dict

@dataclass
class RelatedNeuron:
    """相关神经元 - 表示与查询相关的神经元"""
    neuron_id: str
    relevance_score: float  # 相关性分数 0.0-1.0
    matched_concept: Optional[str] = None  # 匹配的概念名称
    match_type: str = 'semantic'  # semantic|name|tag|hybrid
    confidence: float = 0.7  # 置信度
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'RelatedNeuron':
        return cls(**data)
    
    def __lt__(self, other):
        """用于排序，按相关性分数降序"""
        return self.relevance_score < other.relevance_score
