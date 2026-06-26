"""
双轨并行架构 - 交叉验证模块

本模块实现桶与链之间的一致性验证。
"""

from typing import List, Dict
from pydantic import BaseModel, Field
from ..buckets.topic_cluster import TopicCluster
from ..chains.base_chain import BaseExtractedChain, ChainType
from ..chains.causal_chain import ExtractedCausalChain
from ..chains.logic_chain import ExtractedLogicChain
from ..chains.operation_chain import ExtractedOperationChain


class ValidationResult(BaseModel):
    """
    验证结果
    
    Attributes:
        validation_type: 验证类型
        passed: 是否通过
        confidence: 置信度（0-1）
        issues: 发现的问题列表
        suggestions: 改进建议列表
        metadata: 扩展元数据
    """
    
    validation_type: str = Field(description="验证类型")
    passed: bool = Field(description="是否通过")
    confidence: float = Field(ge=0.0, le=1.0, description="置信度")
    issues: List[str] = Field(default_factory=list, description="发现的问题")
    suggestions: List[str] = Field(default_factory=list, description="改进建议")
    metadata: Dict = Field(default_factory=dict, description="扩展元数据")


class CrossValidator(BaseModel):
    """
    交叉验证器
    
    验证桶与链之间的一致性。
    """
    
    # 配置参数
    MIN_CONFIDENCE_THRESHOLD: float = 0.6
    MAX_ISSUES_COUNT: int = 5
    
    def validate_consistency(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> ValidationResult:
        """
        验证一致性
        
        Args:
            cluster: 话题簇
            chain: 链
        
        Returns:
            验证结果
        """
        issues = []
        
        # 根据链类型选择验证策略
        if chain.chain_type == ChainType.CAUSAL:
            issues.extend(self._validate_causal_consistency(cluster, chain))
        elif chain.chain_type == ChainType.LOGIC:
            issues.extend(self._validate_logic_consistency(cluster, chain))
        elif chain.chain_type == ChainType.OPERATION:
            issues.extend(self._validate_operation_consistency(cluster, chain))
        elif chain.chain_type == ChainType.NARRATIVE:
            issues.extend(self._validate_narrative_consistency(cluster, chain))
        elif chain.chain_type == ChainType.TIME:
            issues.extend(self._validate_time_consistency(cluster, chain))
        
        # 计算置信度
        confidence = self._calculate_confidence(issues)
        
        # 生成建议
        suggestions = self._generate_suggestions(issues, chain.chain_type)
        
        return ValidationResult(
            validation_type=f"{chain.chain_type}_consistency",
            passed=len(issues) == 0,
            confidence=confidence,
            issues=issues[:self.MAX_ISSUES_COUNT],
            suggestions=suggestions,
            metadata={"chain_type": chain.chain_type.value}
        )
    
    def _validate_causal_consistency(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> List[str]:
        """
        验证因果一致性
        
        Args:
            cluster: 话题簇
            chain: 链
        
        Returns:
            问题列表
        """
        issues = []
        
        if not isinstance(chain, ExtractedCausalChain):
            return issues
        
        # 检查1：问题是否在簇中
        problem_keywords = self._extract_keywords(chain.problem.content)
        if problem_keywords and cluster.keywords:
            overlap = problem_keywords & cluster.keywords
            if not overlap:
                issues.append(
                    f"因果链的问题 '{chain.problem.content}' "
                    f"与话题簇关键词 '{', '.join(list(cluster.keywords)[:3])}' 不匹配"
                )
        
        # 检查2：原因是否合理
        for cause in chain.causes:
            cause_keywords = self._extract_keywords(cause.content)
            if cause_keywords and cluster.keywords:
                overlap = cause_keywords & cluster.keywords
                if not overlap:
                    issues.append(
                        f"原因 '{cause.content}' 与话题簇不匹配"
                    )
        
        # 检查3：问题-原因逻辑
        if not chain.causes and chain.solutions:
            issues.append("有解决方案但没有原因，逻辑不完整")
        
        return issues
    
    def _validate_logic_consistency(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> List[str]:
        """
        验证逻辑一致性
        
        Args:
            cluster: 话题簇
            chain: 链
        
        Returns:
            问题列表
        """
        issues = []
        
        if not isinstance(chain, ExtractedLogicChain):
            return issues
        
        # 检查1：前提与话题的一致性
        for premise in chain.premises:
            premise_keywords = self._extract_keywords(premise)
            if premise_keywords and cluster.keywords:
                overlap = premise_keywords & cluster.keywords
                if not overlap:
                    issues.append(
                        f"前提 '{premise}' 与话题簇不一致"
                    )
        
        # 检查2：推理步骤的连贯性
        if len(chain.inference_steps) > 0 and not chain.conclusion:
            issues.append("有推理步骤但没有结论")
        
        # 检查3：逻辑类型合理性
        if chain.logic_type == "deductive" and len(chain.premises) < 2:
            issues.append("演绎推理至少需要2个前提")
        
        return issues
    
    def _validate_operation_consistency(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> List[str]:
        """
        验证操作一致性
        
        Args:
            cluster: 话题簇
            chain: 链
        
        Returns:
            问题列表
        """
        issues = []
        
        if not isinstance(chain, ExtractedOperationChain):
            return issues
        
        # 检查1：操作步骤与话题的一致性
        for step in chain.steps:
            step_keywords = self._extract_keywords(step)
            if step_keywords and cluster.keywords:
                overlap = step_keywords & cluster.keywords
                if not overlap:
                    issues.append(
                        f"操作步骤 '{step}' 与话题簇不匹配"
                    )
        
        # 检查2：操作链的完整性
        if not chain.steps:
            issues.append("操作链没有步骤")
        
        # 检查3：预期结果与操作步骤的一致性
        if chain.expected_outcome and chain.steps:
            outcome_keywords = self._extract_keywords(chain.expected_outcome)
            steps_keywords = set()
            for step in chain.steps:
                steps_keywords.update(self._extract_keywords(step))
            
            if outcome_keywords and steps_keywords:
                overlap = outcome_keywords & steps_keywords
                if not overlap:
                    issues.append("预期结果与操作步骤无明显关联")
        
        return issues
    
    def _validate_narrative_consistency(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> List[str]:
        """
        验证叙事一致性
        
        Args:
            cluster: 话题簇
            chain: 链
        
        Returns:
            问题列表
        """
        issues = []
        
        # 检查1：事件与话题的一致性
        if hasattr(chain, 'events'):
            for event in chain.events:
                event_desc = event.get('description', '')
                event_keywords = self._extract_keywords(event_desc)
                if event_keywords and cluster.keywords:
                    overlap = event_keywords & cluster.keywords
                    if not overlap:
                        issues.append(
                            f"事件 '{event_desc}' 与话题簇不匹配"
                        )
        
        # 检查2：叙事弧的合理性
        if hasattr(chain, 'narrative_arc') and chain.narrative_arc:
            valid_arcs = ['intro', 'rising', 'climax', 'falling', 'resolution']
            if chain.narrative_arc not in valid_arcs:
                issues.append(
                    f"叙事弧 '{chain.narrative_arc}' 不是有效的类型"
                )
        
        return issues
    
    def _validate_time_consistency(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> List[str]:
        """
        验证时间一致性
        
        Args:
            cluster: 话题簇
            chain: 链
        
        Returns:
            问题列表
        """
        issues = []
        
        # 检查1：时间线与话题簇时间的一致性
        cluster_time = cluster.last_updated
        if hasattr(chain, 'created_at'):
            chain_time = chain.created_at
            time_diff = abs((chain_time - cluster_time).total_seconds())
            
            if time_diff > 3600:  # 超过1小时
                issues.append(
                    f"链创建时间与话题簇更新时间相差 {time_diff}秒，可能不一致"
                )
        
        # 检查2：时间线的合理性
        if hasattr(chain, 'timeline'):
            if len(chain.timeline) > 1:
                # 检查时间顺序
                for i in range(1, len(chain.timeline)):
                    prev_time = chain.timeline[i-1].get('time', '')
                    curr_time = chain.timeline[i].get('time', '')
                    # 简单的字符串比较（实际应该解析为datetime）
                    if prev_time and curr_time and prev_time > curr_time:
                        issues.append(
                            f"时间线顺序错误: {prev_time} -> {curr_time}"
                        )
        
        return issues
    
    def _calculate_confidence(self, issues: List[str]) -> float:
        """
        计算置信度
        
        Args:
            issues: 问题列表
        
        Returns:
            置信度（0-1）
        """
        if not issues:
            return 1.0
        
        # 每个问题降低20%置信度
        confidence = 1.0 - len(issues) * 0.2
        return max(0.0, confidence)
    
    def _generate_suggestions(
        self,
        issues: List[str],
        chain_type: ChainType
    ) -> List[str]:
        """
        生成改进建议
        
        Args:
            issues: 问题列表
            chain_type: 链类型
        
        Returns:
            建议列表
        """
        suggestions = []
        
        if not issues:
            return ["验证通过，无需改进"]
        
        # 根据问题生成建议
        if any("不匹配" in issue for issue in issues):
            suggestions.append("检查链的内容与话题簇是否相关")
        
        if any("没有" in issue for issue in issues):
            suggestions.append("补充缺失的信息以增强完整性")
        
        if any("顺序" in issue or "逻辑" in issue for issue in issues):
            suggestions.append("检查链的逻辑顺序是否合理")
        
        # 根据链类型的特定建议
        if chain_type == ChainType.CAUSAL:
            suggestions.append("确保因果关系清晰，根本原因明确")
        elif chain_type == ChainType.LOGIC:
            suggestions.append("确保推理步骤连贯，结论由前提得出")
        elif chain_type == ChainType.OPERATION:
            suggestions.append("确保操作步骤可执行，预期结果合理")
        
        return suggestions
    
    def _extract_keywords(self, text: str) -> set:
        """
        提取关键词
        
        Args:
            text: 文本
        
        Returns:
            关键词集合
        """
        words = text.split()
        stop_words = {'的', '是', '在', '和', '了', '有', '我', '你', '他', 'the', 'is', 'and', 'or', 'of', 'to'}
        keywords = {word for word in words if len(word) > 1 and word not in stop_words}
        return keywords
