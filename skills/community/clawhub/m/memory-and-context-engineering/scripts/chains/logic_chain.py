"""
双轨并行架构 - 逻辑链模块

本模块定义逻辑链的数据结构。
"""

from typing import List
from pydantic import BaseModel, Field
from .base_chain import BaseExtractedChain, ChainType


class ExtractedLogicChain(BaseExtractedChain):
    """
    逻辑链：前提→推理→结论
    
    用途：提取和表示推理过程
    
    Attributes:
        chain_type: 链类型（固定为LOGIC）
        premises: 前提列表
        inference_steps: 推理步骤列表
        conclusion: 结论
        logic_type: 逻辑类型
    """
    
    chain_type: ChainType = ChainType.LOGIC
    
    # 逻辑节点
    premises: List[str] = Field(
        default_factory=list,
        description="前提列表"
    )
    inference_steps: List[str] = Field(
        default_factory=list,
        description="推理步骤列表"
    )
    conclusion: str = Field(
        default="",
        description="结论"
    )
    
    # 逻辑类型
    logic_type: str = Field(
        default="deductive",
        description="逻辑类型: deductive/inductive/abductive"
    )
    
    def to_summary(self) -> str:
        """生成逻辑链摘要"""
        lines = []
        
        # 前提
        if self.premises:
            premises_text = ", ".join(self.premises)
            lines.append(f"前提: {premises_text}")
        
        # 推理
        if self.inference_steps:
            inference_text = " → ".join(self.inference_steps)
            lines.append(f"推理: {inference_text}")
        
        # 结论
        if self.conclusion:
            lines.append(f"结论: {self.conclusion}")
        
        return "\n".join(lines)
    
    def get_premise_count(self) -> int:
        """获取前提数量"""
        return len(self.premises)
    
    def get_inference_depth(self) -> int:
        """获取推理深度"""
        return len(self.inference_steps)
