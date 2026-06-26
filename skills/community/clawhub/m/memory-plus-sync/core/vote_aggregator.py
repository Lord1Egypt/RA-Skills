"""
投票聚合逻辑模块

对三个代理的验证结果进行投票聚合，决定是否需要仲裁
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .triple_agent_processor import AgentResponse


class VoteResult(Enum):
    """投票结果类型"""
    UNANIMOUS_PASS = "unanimous_pass"      # 3:0 通过
    MAJORITY_PASS = "majority_pass"        # 2:1 通过
    UNANIMOUS_REJECT = "unanimous_reject"  # 3:0 拒绝
    MAJORITY_REJECT = "majority_reject"    # 2:1 拒绝
    SPLIT_DECISION = "split_decision"      # 1:1:1 或分歧大


@dataclass
class AggregatedResult:
    """聚合结果"""
    vote_result: VoteResult
    vote_counts: Dict[str, int]  # 每种意见的票数
    final_decision: str  # STORE, REVIEW, REJECT, MERGE
    confidence: float  # 0.0-1.0
    reasoning: str
    needs_arbitration: bool
    agent_responses: Dict[str, AgentResponse]
    
    # 详细评分统计
    avg_total_score: Optional[float] = None
    score_variance: Optional[float] = None
    risk_level: Optional[str] = None


class VoteAggregator:
    """投票聚合器"""
    
    def __init__(self, arbitration_threshold: float = 0.6):
        """
        初始化投票聚合器
        
        Args:
            arbitration_threshold: 触发仲裁的置信度阈值
        """
        self.arbitration_threshold = arbitration_threshold
    
    def _extract_decision(self, response: AgentResponse) -> Tuple[str, float]:
        """
        从代理响应中提取决策和置信度
        
        Returns:
            (decision, confidence) 元组
        """
        if not response.success or not response.response_data:
            return "ERROR", 0.0
        
        data = response.response_data
        
        # 从不同代理提取决策
        if "suggested_action" in data:
            return data["suggested_action"], data.get("confidence", 0.5)
        elif "recommended_action" in data:
            return data["recommended_action"], data.get("confidence", 0.5)
        elif "priority_level" in data:
            # Scorer 代理，根据优先级推断
            priority = data.get("priority_level", 3)
            if priority >= 4:
                return "STORE", data.get("confidence", 0.7)
            elif priority >= 2:
                return "REVIEW", data.get("confidence", 0.5)
            else:
                return "REJECT", data.get("confidence", 0.5)
        else:
            return "UNKNOWN", 0.0
    
    def _extract_score(self, response: AgentResponse) -> Optional[float]:
        """从代理响应中提取总分"""
        if not response.success or not response.response_data:
            return None
        
        data = response.response_data
        
        if "total_score" in data:
            return float(data["total_score"])
        elif "quality_score" in data:
            return float(data["quality_score"]) * 5  # 归一化到 0-50
        else:
            return None
    
    def _extract_risk_level(self, response: AgentResponse) -> Optional[str]:
        """从 Reviewer 代理提取风险等级"""
        if not response.success or not response.response_data:
            return None
        
        data = response.response_data
        return data.get("risk_level")
    
    def aggregate(self, responses: Dict[str, AgentResponse]) -> AggregatedResult:
        """
        聚合三个代理的投票结果
        
        Args:
            responses: 三个代理的响应
        
        Returns:
            AggregatedResult: 聚合结果
        """
        # 提取每个代理的决策
        decisions = {}
        confidences = {}
        scores = []
        
        for agent_name, response in responses.items():
            decision, confidence = self._extract_decision(response)
            decisions[agent_name] = decision
            confidences[agent_name] = confidence
            
            score = self._extract_score(response)
            if score is not None:
                scores.append(score)
        
        # 统计投票
        vote_counts = {}
        for decision in decisions.values():
            vote_counts[decision] = vote_counts.get(decision, 0) + 1
        
        # 判断投票结果
        max_votes = max(vote_counts.values())
        majority_decisions = [d for d, c in vote_counts.items() if c == max_votes]
        
        # 计算平均置信度
        avg_confidence = sum(confidences.values()) / len(confidences) if confidences else 0.0
        
        # 判断是否需要仲裁
        needs_arbitration = False
        vote_result = VoteResult.SPLIT_DECISION
        final_decision = "REVIEW"
        reasoning = ""
        
        if len(majority_decisions) == 1:
            majority_decision = majority_decisions[0]
            
            if max_votes == 3:
                # 全票通过或拒绝
                if majority_decision == "STORE" or majority_decision == "APPROVE":
                    vote_result = VoteResult.UNANIMOUS_PASS
                    final_decision = "STORE"
                    reasoning = "三个代理一致同意存储"
                elif majority_decision in ["REJECT", "CRITICAL"]:
                    vote_result = VoteResult.UNANIMOUS_REJECT
                    final_decision = "REJECT"
                    reasoning = "三个代理一致拒绝"
                else:
                    vote_result = VoteResult.UNANIMOUS_PASS
                    final_decision = majority_decision
                    reasoning = f"三个代理一致决定：{majority_decision}"
            
            elif max_votes == 2:
                # 多数决
                if majority_decision in ["STORE", "APPROVE"]:
                    vote_result = VoteResult.MAJORITY_PASS
                    final_decision = "STORE"
                    reasoning = "两个代理同意存储"
                elif majority_decision in ["REJECT", "CRITICAL"]:
                    vote_result = VoteResult.MAJORITY_REJECT
                    final_decision = "REJECT"
                    reasoning = "两个代理拒绝"
                else:
                    vote_result = VoteResult.MAJORITY_PASS
                    final_decision = majority_decision
                    reasoning = f"多数代理决定：{majority_decision}"
                
                # 如果置信度低，需要仲裁
                if avg_confidence < self.arbitration_threshold:
                    needs_arbitration = True
                    reasoning += "，但置信度较低，需要仲裁"
        
        else:
            # 分歧严重 (1:1:1 或 1:1)
            vote_result = VoteResult.SPLIT_DECISION
            needs_arbitration = True
            final_decision = "REVIEW"
            reasoning = f"代理意见分歧：{vote_counts}"
        
        # 检查风险等级
        risk_level = self._extract_risk_level(responses.get("reviewer", AgentResponse("", "", {}, 0, False)))
        if risk_level in ["HIGH", "CRITICAL"]:
            needs_arbitration = True
            reasoning += f"。审查代理标记风险等级：{risk_level}"
            if risk_level == "CRITICAL":
                final_decision = "REJECT"
        
        # 计算评分统计
        avg_score = sum(scores) / len(scores) if scores else None
        score_var = None
        if len(scores) > 1:
            mean = avg_score
            score_var = sum((s - mean) ** 2 for s in scores) / len(scores)
        
        return AggregatedResult(
            vote_result=vote_result,
            vote_counts=vote_counts,
            final_decision=final_decision,
            confidence=avg_confidence,
            reasoning=reasoning,
            needs_arbitration=needs_arbitration,
            agent_responses=responses,
            avg_total_score=avg_score,
            score_variance=score_var,
            risk_level=risk_level
        )
    
    def should_store(self, aggregated_result: AggregatedResult) -> bool:
        """判断是否应该存储"""
        if aggregated_result.needs_arbitration:
            return False  # 需要仲裁，暂不存储
        
        return aggregated_result.final_decision in ["STORE", "APPROVE", "MERGE"]
    
    def format_summary(self, aggregated_result: AggregatedResult) -> str:
        """格式化聚合结果摘要"""
        lines = [
            "=== 投票聚合结果 ===",
            f"投票结果：{aggregated_result.vote_result.value}",
            f"投票分布：{aggregated_result.vote_counts}",
            f"最终决定：{aggregated_result.final_decision}",
            f"置信度：{aggregated_result.confidence:.2f}",
            f"需要仲裁：{'是' if aggregated_result.needs_arbitration else '否'}",
        ]
        
        if aggregated_result.avg_total_score is not None:
            lines.append(f"平均评分：{aggregated_result.avg_total_score:.1f}")
        
        if aggregated_result.risk_level:
            lines.append(f"风险等级：{aggregated_result.risk_level}")
        
        lines.append(f"理由：{aggregated_result.reasoning}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # 测试投票聚合
    print("=== 投票聚合测试 ===\n")
    
    # 模拟三个代理的响应
    from dataclasses import dataclass
    
    responses = {
        "validator": AgentResponse(
            agent_name="validator",
            model_used="moonshot-v1-8k",
            response_data={
                "validation_result": "PASS",
                "total_score": 35,
                "suggested_action": "STORE",
                "confidence": 0.85
            },
            latency_ms=234,
            success=True
        ),
        "scorer": AgentResponse(
            agent_name="scorer",
            model_used="moonshot-v1-8k",
            response_data={
                "memory_type": "EVENT",
                "importance": "IMPORTANT",
                "total_score": 38,
                "priority_level": 4,
                "confidence": 0.78
            },
            latency_ms=256,
            success=True
        ),
        "reviewer": AgentResponse(
            agent_name="reviewer",
            model_used="moonshot-v1-8k",
            response_data={
                "risk_level": "LOW",
                "quality_score": 8.5,
                "recommended_action": "APPROVE",
                "confidence": 0.92
            },
            latency_ms=198,
            success=True
        )
    }
    
    aggregator = VoteAggregator()
    result = aggregator.aggregate(responses)
    
    print(aggregator.format_summary(result))
    print(f"\n是否存储：{aggregator.should_store(result)}")
    
    print("\n=== 测试完成 ===")
