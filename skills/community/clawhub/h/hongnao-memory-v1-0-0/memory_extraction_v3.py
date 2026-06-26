#!/usr/bin/env python3
"""
弘脑记忆系统 - 记忆抽取模块 v3
使用关键词匹配而非正则
"""

import uuid
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum


class MemoryType(Enum):
    FACT = "fact"
    PREFERENCE = "preference"
    SKILL = "skill"
    EMOTION = "emotion"
    CONSTRAINT = "constraint"


@dataclass
class MemCell:
    id: str
    content: str
    memory_type: str
    source: str
    created_at: str
    updated_at: str
    importance: int = 5
    access_count: int = 0
    tags: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemCell':
        return cls(**data)


class MemoryExtractor:
    """记忆抽取器 v3 - 基于规则和关键词"""
    
    def __init__(self):
        self.keywords = {
            MemoryType.FACT.value: ['叫', '在', '工作', '职位', '是', '预算', '公司'],
            MemoryType.PREFERENCE.value: ['喜欢', '偏好', '讨厌', '习惯', '爱'],
            MemoryType.CONSTRAINT.value: ['必须', '不能', '禁止', '不要', '务必'],
        }
    
    def extract_from_text(self, text: str, source: str = "conversation") -> List[MemCell]:
        """从文本中抽取记忆 - 基于句子分析"""
        mem_cells = []
        timestamp = datetime.now().isoformat()
        
        # 分句
        sentences = self._split_sentences(text)
        
        for sentence in sentences:
            if not sentence.strip():
                continue
            
            # 判断句子类型
            memory_type = self._classify_sentence(sentence)
            
            if memory_type:
                cell_id = f"mem_{uuid.uuid4().hex[:12]}"
                mem_cell = MemCell(
                    id=cell_id,
                    content=sentence.strip(),
                    memory_type=memory_type,
                    source=source,
                    created_at=timestamp,
                    updated_at=timestamp,
                    importance=self._calc_importance(sentence, memory_type),
                    tags=[memory_type]
                )
                mem_cells.append(mem_cell)
        
        return mem_cells
    
    def _split_sentences(self, text: str) -> List[str]:
        """分句"""
        import re
        # 按句号、分号、换行分割
        sentences = re.split(r'[。；\n]', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _classify_sentence(self, sentence: str) -> str:
        """判断句子类型"""
        # 事实型：包含用户信息、工作、职位等
        if any(kw in sentence for kw in ['用户叫', '用户在', '用户职位', '用户是']):
            return MemoryType.FACT.value
        
        # 偏好型：包含喜欢、偏好、讨厌等
        if any(kw in sentence for kw in ['喜欢', '偏好', '讨厌', '习惯']):
            return MemoryType.PREFERENCE.value
        
        # 约束型：包含必须、不能、禁止等
        if any(kw in sentence for kw in ['必须', '不能', '禁止', '不要', '务必']):
            return MemoryType.CONSTRAINT.value
        
        # 默认：如果包含用户且有动词，可能是事实
        if '用户' in sentence and len(sentence) > 5:
            return MemoryType.FACT.value
        
        return None
    
    def _calc_importance(self, sentence: str, memory_type: str) -> int:
        """计算重要性"""
        base = 5
        
        # 约束型更重要
        if memory_type == MemoryType.CONSTRAINT.value:
            base += 2
        
        # 包含关键词提升重要性
        if any(kw in sentence for kw in ['必须', '一定', '关键', '重要']):
            base += 1
        
        return min(base, 10)


def test_v3():
    """测试 v3"""
    extractor = MemoryExtractor()
    
    test_text = """
    用户叫唐锋，在燧弘华创工作，职位是执行总裁。
    用户喜欢简洁商务风格，偏好使用 PPT 做演示。
    项目预算为 100 万元。
    必须保证数据安全。
    """
    
    print("=" * 60)
    print("弘脑记忆系统 - 记忆抽取模块 v3 测试")
    print("=" * 60)
    print(f"\n输入文本:\n{test_text}\n")
    
    mem_cells = extractor.extract_from_text(test_text, source="test")
    
    print(f"抽取到 {len(mem_cells)} 条记忆:\n")
    
    for i, cell in enumerate(mem_cells, 1):
        print(f"{i}. [{cell.memory_type}] {cell.content}")
        print(f"   重要性：{cell.importance}/10")
        print()
    
    return mem_cells


if __name__ == '__main__':
    test_v3()
