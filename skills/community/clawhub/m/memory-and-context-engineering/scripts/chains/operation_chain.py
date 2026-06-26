"""
双轨并行架构 - 操作链模块

本模块定义操作链的数据结构。
"""

from typing import List
from pydantic import BaseModel, Field
from .base_chain import BaseExtractedChain, ChainType


class ExtractedOperationChain(BaseExtractedChain):
    """
    操作链：动作1→动作2→结果
    
    用途：提取和表示执行步骤
    
    Attributes:
        chain_type: 链类型（固定为OPERATION）
        steps: 操作步骤列表
        expected_outcome: 预期结果
        resources_needed: 所需资源列表
        estimated_duration: 预估耗时
    """
    
    chain_type: ChainType = ChainType.OPERATION
    
    # 操作节点
    steps: List[str] = Field(
        default_factory=list,
        description="操作步骤列表"
    )
    expected_outcome: str = Field(
        default="",
        description="预期结果"
    )
    resources_needed: List[str] = Field(
        default_factory=list,
        description="所需资源列表"
    )
    
    # 操作属性
    estimated_duration: str = Field(
        default="",
        description="预估耗时"
    )
    
    def to_summary(self) -> str:
        """生成操作链摘要"""
        steps_str = " → ".join(self.steps)
        if self.expected_outcome:
            return f"操作链: {steps_str} → {self.expected_outcome}"
        return f"操作链: {steps_str}"
    
    def get_step_count(self) -> int:
        """获取步骤数量"""
        return len(self.steps)
    
    def get_critical_steps(self) -> List[str]:
        """获取关键步骤（包含"关键"、"重要"等关键词）"""
        keywords = ["关键", "重要", "必须", "核心", "critical", "important"]
        critical_steps = []
        for step in self.steps:
            if any(keyword in step for keyword in keywords):
                critical_steps.append(step)
        return critical_steps
