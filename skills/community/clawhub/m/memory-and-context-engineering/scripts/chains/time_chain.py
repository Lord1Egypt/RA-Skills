"""
双轨并行架构 - 时间链模块

本模块定义时间链的数据结构。
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field
from .base_chain import BaseExtractedChain, ChainType


class ExtractedTimeChain(BaseExtractedChain):
    """
    时间链：时间点A→时间点B→时间点C
    
    用途：提取和表示时序关系
    
    Attributes:
        chain_type: 链类型（固定为TIME）
        timeline: 时间线列表
        duration: 总时长
    """
    
    chain_type: ChainType = ChainType.TIME
    
    # 时间节点
    timeline: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="时间线列表"
    )
    duration: str = Field(
        default="",
        description="总时长"
    )
    
    def to_summary(self) -> str:
        """生成时间链摘要"""
        if not self.timeline:
            return "时间线: 无时间点"
        
        time_str = " → ".join(
            f"{t['time']}: {t['event']}" 
            for t in self.timeline
        )
        return f"时间线: {time_str}"
    
    def get_timepoint_count(self) -> int:
        """获取时间点数量"""
        return len(self.timeline)
    
    def get_start_time(self) -> str:
        """获取起始时间"""
        if self.timeline:
            return self.timeline[0].get("time", "")
        return ""
    
    def get_end_time(self) -> str:
        """获取结束时间"""
        if self.timeline:
            return self.timeline[-1].get("time", "")
        return ""
