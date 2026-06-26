"""
双轨并行架构 - 链感知上下文重构器模块

本模块实现基于链信息的上下文选择和压缩。
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from ..chains.base_chain import BaseExtractedChain, ChainType
from ..type_defs import ScenarioType
from ..context_orchestrator import ContextSource, ContextPriority


class ChainAwareContextBlock(BaseModel):
    """
    链感知的上下文块
    
    在原有上下文块基础上添加链维度信息。
    
    Attributes:
        block_id: 块ID
        source: 来源
        priority: 优先级
        content: 内容
        relevance_score: 相关性
        chain_type: 链类型
        chain_confidence: 链置信度
        chain_completeness: 链完整性
        chain_metadata: 链元数据
        created_at: 创建时间
    """
    
    block_id: str = Field(description="块ID")
    source: ContextSource = Field(description="来源")
    priority: ContextPriority = Field(description="优先级")
    content: str = Field(description="内容")
    relevance_score: float = Field(ge=0.0, le=1.0, description="相关性")
    
    # 链维度
    chain_type: ChainType | None = Field(None, description="链类型")
    chain_confidence: float = Field(default=0.0, description="链置信度")
    chain_completeness: float = Field(default=0.0, description="链完整性")
    chain_metadata: Dict = Field(default_factory=dict, description="链元数据")
    
    created_at: datetime = Field(default_factory=datetime.now)
    
    def calculate_combined_score(
        self,
        task_chain_priority: Dict[ChainType, float]
    ) -> float:
        """
        计算综合得分
        
        Args:
            task_chain_priority: 任务到链类型的优先级映射
        
        Returns:
            综合得分
        """
        if not self.chain_type:
            return self.relevance_score
        
        # 获取链类型的权重
        chain_weight = task_chain_priority.get(self.chain_type, 0.5)
        
        # 综合得分 = 相关性 × 链权重 × 链置信度
        combined_score = (
            self.relevance_score * 
            chain_weight * 
            self.chain_confidence
        )
        
        return combined_score


class ChainAwareContextReconstructor(BaseModel):
    """
    链感知的上下文重构器
    
    根据任务类型和链信息动态选择和压缩上下文。
    """
    
    # 任务类型与链类型的优先级映射
    TASK_CHAIN_PRIORITY: Dict[ScenarioType, Dict[ChainType, float]] = {
        ScenarioType.DEBUGGING: {
            ChainType.CAUSAL: 1.0,      # 调试需要因果关系
            ChainType.OPERATION: 0.9,   # 需要操作步骤
            ChainType.LOGIC: 0.8,      # 需要推理路径
            ChainType.TIME: 0.6,
            ChainType.NARRATIVE: 0.5
        },
        ScenarioType.CODING: {
            ChainType.OPERATION: 1.0,   # 编码需要操作流程
            ChainType.LOGIC: 0.9,       # 需要算法逻辑
            ChainType.CAUSAL: 0.7,
            ChainType.TIME: 0.6,
            ChainType.NARRATIVE: 0.4
        },
        ScenarioType.LEARNING: {
            ChainType.NARRATIVE: 1.0,   # 学习需要完整叙事
            ChainType.LOGIC: 0.9,       # 需要理解逻辑
            ChainType.CAUSAL: 0.8,
            ChainType.OPERATION: 0.7,
            ChainType.TIME: 0.6
        },
        ScenarioType.PLANNING: {
            ChainType.TIME: 1.0,        # 规划需要时间线
            ChainType.OPERATION: 0.9,   # 需要执行步骤
            ChainType.CAUSAL: 0.8,      # 需要预判风险
            ChainType.LOGIC: 0.7,
            ChainType.NARRATIVE: 0.5
        },
        ScenarioType.ANALYSIS: {
            ChainType.LOGIC: 1.0,       # 分析需要逻辑推理
            ChainType.CAUSAL: 0.9,      # 需要因果关系
            ChainType.NARRATIVE: 0.7,   # 需要背景信息
            ChainType.OPERATION: 0.6,
            ChainType.TIME: 0.5
        }
    }
    
    # 压缩策略
    MIN_CHAIN_COMPLETENSS: float = 0.6  # 最低链完整性
    
    def select_context_by_task(
        self,
        available_blocks: List[ChainAwareContextBlock],
        task_type: ScenarioType,
        token_budget: int
    ) -> List[ChainAwareContextBlock]:
        """
        根据任务类型选择上下文
        
        Args:
            available_blocks: 可用的上下文块列表
            task_type: 任务类型
            token_budget: Token预算
        
        Returns:
            选择后的上下文块列表
        """
        if not available_blocks:
            return []
        
        # 获取任务对应的链优先级
        chain_priority = self.TASK_CHAIN_PRIORITY.get(
            task_type,
            {}
        )
        
        # 计算每个块的综合得分
        scored_blocks = []
        for block in available_blocks:
            combined_score = block.calculate_combined_score(chain_priority)
            scored_blocks.append((combined_score, block))
        
        # 按得分排序
        scored_blocks.sort(key=lambda x: x[0], reverse=True)
        
        # 保留完整链（跨块关联）
        selected_blocks = self._preserve_complete_chains(
            [block for score, block in scored_blocks],
            chain_priority
        )
        
        # 压缩到预算内
        compressed = self._compress_by_budget(
            selected_blocks,
            token_budget
        )
        
        return compressed
    
    def _preserve_complete_chains(
        self,
        blocks: List[ChainAwareContextBlock],
        chain_priority: Dict[ChainType, float]
    ) -> List[ChainAwareContextBlock]:
        """
        保留完整链（跨块关联）
        
        Args:
            blocks: 上下文块列表
            chain_priority: 链优先级映射
        
        Returns:
            保留完整链后的块列表
        """
        if not blocks:
            return []
        
        # 按链类型分组
        chains_by_type: Dict[ChainType, List[ChainAwareContextBlock]] = {}
        for block in blocks:
            if block.chain_type:
                chains_by_type.setdefault(block.chain_type, []).append(block)
        
        # 识别关键链（高完整性）
        key_blocks = []
        for block in blocks:
            if block.chain_type and block.chain_completeness >= self.MIN_CHAIN_COMPLETENSS:
                key_blocks.append(block)
        
        # 如果有关键链，优先保留
        if key_blocks:
            # 先添加关键链
            result = key_blocks.copy()
            
            # 再添加其他块（预算内）
            remaining_budget = len(blocks) - len(result)
            for block in blocks:
                if block not in result and remaining_budget > 0:
                    result.append(block)
                    remaining_budget -= 1
            
            return result
        
        return blocks
    
    def _compress_by_budget(
        self,
        blocks: List[ChainAwareContextBlock],
        token_budget: int
    ) -> List[ChainAwareContextBlock]:
        """
        根据Token预算压缩
        
        Args:
            blocks: 上下文块列表
            token_budget: Token预算
        
        Returns:
            压缩后的块列表
        """
        if not blocks:
            return []
        
        # 估算Token使用
        result = []
        total_tokens = 0
        
        for block in blocks:
            block_tokens = self._estimate_tokens(block.content)
            
            if total_tokens + block_tokens <= token_budget:
                result.append(block)
                total_tokens += block_tokens
            else:
                # 尝试截断
                remaining = token_budget - total_tokens
                if remaining > 50:  # 至少50个字符
                    truncated_content = self._truncate_content(
                        block.content,
                        remaining
                    )
                    if truncated_content:
                        result.append(ChainAwareContextBlock(
                            block_id=block.block_id,
                            source=block.source,
                            priority=block.priority,
                            content=truncated_content,
                            relevance_score=block.relevance_score,
                            chain_type=block.chain_type,
                            chain_confidence=block.chain_confidence,
                            chain_completeness=block.chain_completeness,
                            chain_metadata=block.chain_metadata,
                            created_at=block.created_at
                        ))
                break
        
        return result
    
    def _estimate_tokens(self, text: str) -> int:
        """
        估算Token数量（简化版）
        
        Args:
            text: 文本
        
        Returns:
            Token数量
        """
        # 简化估算：1 Token ≈ 4 字符（中文）或 0.75 词（英文）
        return len(text) // 4
    
    def _truncate_content(self, content: str, max_chars: int) -> str:
        """
        截断内容
        
        Args:
            content: 原始内容
            max_chars: 最大字符数
        
        Returns:
            截断后的内容
        """
        if len(content) <= max_chars:
            return content
        
        # 保留前80%，添加省略号
        keep = int(max_chars * 0.8)
        return content[:keep] + "... [截断]"
    
    def create_chain_aware_block(
        self,
        chain: BaseExtractedChain,
        source: ContextSource,
        priority: ContextPriority
    ) -> ChainAwareContextBlock:
        """
        从链创建上下文块
        
        Args:
            chain: 链对象
            source: 来源
            priority: 优先级
        
        Returns:
            上下文块
        """
        return ChainAwareContextBlock(
            block_id=f"block_{chain.chain_id}",
            source=source,
            priority=priority,
            content=chain.to_summary(),
            relevance_score=chain.extraction_confidence,
            chain_type=chain.chain_type,
            chain_confidence=chain.extraction_confidence,
            chain_completeness=0.8,  # 默认完整性
            chain_metadata={
                "chain_id": chain.chain_id,
                "created_at": chain.created_at
            },
            created_at=chain.created_at
        )
    
    def evaluate_context_quality(
        self,
        context_blocks: List[ChainAwareContextBlock],
        task_type: ScenarioType
    ) -> Dict[str, Any]:
        """
        评估上下文质量
        
        Args:
            context_blocks: 上下文块列表
            task_type: 任务类型
        
        Returns:
            质量评估结果
        """
        result = {
            "total_blocks": len(context_blocks),
            "chain_coverage": 0.0,
            "avg_relevance": 0.0,
            "avg_chain_confidence": 0.0,
            "completeness_score": 0.0,
            "missing_chains": []
        }
        
        if not context_blocks:
            return result
        
        # 链覆盖度
        chain_types = set()
        chain_blocks = 0
        for block in context_blocks:
            if block.chain_type:
                chain_types.add(block.chain_type)
                chain_blocks += 1
        
        if context_blocks:
            result["chain_coverage"] = chain_blocks / len(context_blocks)
        
        # 平均相关性
        relevance_scores = [b.relevance_score for b in context_blocks]
        result["avg_relevance"] = sum(relevance_scores) / len(relevance_scores)
        
        # 平均链置信度
        chain_confidences = [
            b.chain_confidence 
            for b in context_blocks 
            if b.chain_type
        ]
        if chain_confidences:
            result["avg_chain_confidence"] = sum(chain_confidences) / len(chain_confidences)
        
        # 完整性评分
        required_chains = self.TASK_CHAIN_PRIORITY.get(task_type, {})
        missing_chains = [
            ct.value 
            for ct in required_chains.keys() 
            if ct not in chain_types
        ]
        result["missing_chains"] = missing_chains
        
        # 计算完整性
        if required_chains:
            completeness = len(chain_types & set(required_chains.keys())) / len(required_chains)
            result["completeness_score"] = completeness
        
        return result
