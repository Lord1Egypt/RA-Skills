"""
双轨并行架构 - 叙事链模块

本模块定义叙事链的数据结构。
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field
from .base_chain import BaseExtractedChain, ChainType


class ExtractedNarrativeChain(BaseExtractedChain):
    """
    叙事链：事件1→事件2→事件3
    
    用途：提取和表示叙事流程
    
    Attributes:
        chain_type: 链类型（固定为NARRATIVE）
        events: 事件列表
        narrative_arc: 叙事弧
        protagonist: 主角
    """
    
    chain_type: ChainType = ChainType.NARRATIVE
    
    # 叙事节点
    events: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="事件列表"
    )
    narrative_arc: str = Field(
        default="",
        description="叙事弧: intro/rising/climax/falling/resolution"
    )
    
    # 叙事属性
    protagonist: str = Field(
        default="",
        description="主角"
    )
    
    def to_summary(self) -> str:
        """生成叙事链摘要"""
        if not self.events:
            return "叙事链: 无事件"
        
        event_descriptions = [
            e.get("description", "") 
            for e in self.events
        ]
        events_str = " → ".join(event_descriptions)
        return f"叙事: {events_str}"
    
    def get_event_count(self) -> int:
        """获取事件数量"""
        return len(self.events)
    
    def get_key_events(self) -> List[Dict[str, Any]]:
        """获取关键事件"""
        key_events = []
        for event in self.events:
            if event.get("is_key", False):
                key_events.append(event)
        return key_events
