"""
双轨并行架构 - 因果链模块

本模块定义因果链的数据结构和相关类型。
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base_chain import BaseExtractedChain, ChainType


class ProblemNode(BaseModel):
    """问题节点"""
    content: str = Field(description="问题内容")
    severity: str = Field(default="medium", description="严重程度: low/medium/high/critical")
    category: str = Field(default="", description="问题类别")
    metadata: dict = Field(default_factory=dict)


class CauseNode(BaseModel):
    """原因节点"""
    content: str = Field(description="原因内容")
    is_root_cause: bool = Field(default=False, description="是否根本原因")
    cause_type: str = Field(default="direct", description="原因类型: direct/root/contributing")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    metadata: dict = Field(default_factory=dict)


class CausalRelation(BaseModel):
    """因果关系"""
    from_cause: str = Field(description="原因节点ID")
    to_effect: str = Field(description="结果节点ID")
    relation_type: str = Field(default="causes", description="关系类型")
    strength: float = Field(default=0.5, ge=0.0, le=1.0, description="关系强度")


class SolutionNode(BaseModel):
    """解决方案节点"""
    content: str = Field(description="解决方案内容")
    effectiveness: str = Field(default="unknown", description="有效性: unknown/low/medium/high")
    effort: str = Field(default="unknown", description="实施难度: unknown/low/medium/high")
    metadata: dict = Field(default_factory=dict)


class ExtractedCausalChain(BaseExtractedChain):
    """
    因果链：问题→原因→解决方案
    
    用途：提取和表示因果关系
    
    Attributes:
        chain_type: 链类型（固定为CAUSAL）
        problem: 问题节点
        causes: 原因节点列表
        causal_relations: 因果关系列表
        solutions: 解决方案列表
        source_text: 来源文本
    """
    
    chain_type: ChainType = ChainType.CAUSAL
    
    # 因果节点
    problem: ProblemNode = Field(description="问题节点")
    causes: List[CauseNode] = Field(
        default_factory=list,
        description="原因节点列表"
    )
    causal_relations: List[CausalRelation] = Field(
        default_factory=list,
        description="因果关系列表"
    )
    solutions: List[SolutionNode] = Field(
        default_factory=list,
        description="解决方案列表"
    )
    
    # 源信息
    source_text: str = Field(
        default="",
        description="来源文本"
    )
    
    def to_summary(self) -> str:
        """生成因果链摘要"""
        lines = []
        
        # 问题
        lines.append(f"问题: {self.problem.content}")
        
        # 原因
        if self.causes:
            root_causes = [c for c in self.causes if c.is_root_cause]
            if root_causes:
                cause_text = ", ".join(c.content for c in root_causes)
            else:
                cause_text = ", ".join(c.content for c in self.causes)
            lines.append(f"原因: {cause_text}")
        
        # 解决方案
        if self.solutions:
            solution_text = ", ".join(s.content for s in self.solutions)
            lines.append(f"解决方案: {solution_text}")
        
        return "\n".join(lines)
    
    def get_root_causes(self) -> List[CauseNode]:
        """获取根本原因列表"""
        return [c for c in self.causes if c.is_root_cause]
    
    def get_most_effective_solutions(self) -> List[SolutionNode]:
        """获取最有效的解决方案"""
        high_effectiveness = ["high", "medium"]
        return [s for s in self.solutions if s.effectiveness in high_effectiveness]
