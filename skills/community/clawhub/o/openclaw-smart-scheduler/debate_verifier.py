#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
辩论验证器 - 多模型辩论共识
确保最终共识输出，禁止无限辩论

作者: 海狸 🦫
"""

import json
import requests
from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass
class DebateResult:
    """辩论结果"""
    passed: bool           # 是否通过
    consensus: str         # 共识结论
    confidence: float      # 置信度
    rounds: int            # 辩论轮数
    reason: str            # 判定原因


class DebateVerifier:
    """
    多模型辩论验证器
    
    核心规则：
    1. 最多5轮辩论
    2. 必须输出共识结论
    3. 收敛度≥0.7视为共识
    4. 5轮未收敛则取仲裁者最后结论
    5. 按需触发：仅高价值任务启用
    """
    
    # 辩论服务地址
    DEBATE_URL = "http://127.0.0.1:8002/api/debate"
    DEBATE_WS_URL = "ws://127.0.0.1:8002/ws"
    
    # 阈值
    MAX_ROUNDS = 5           # 最大辩论轮数
    CONSENSUS_THRESHOLD = 0.7  # 共识阈值
    
    # 按需触发关键词（高价值任务）
    HIGH_VALUE_KEYWORDS = [
        '决策', '设计', '分析', '评估', '方案',
        '优化', '改进', '对比', '选择', '确定',
        '验证', '确认', '审核', '复核'
    ]
    
    # 低置信度阈值（低于此值触发辩论）
    LOW_CONFIDENCE_THRESHOLD = 0.8
    
    def __init__(self):
        self.enabled = True
        self.timeout = 180  # 3分钟超时
        self.trigger_policy = "smart"  # always/smart/manual
    
    def should_trigger(self, task_result: str, context: str = "", confidence: float = 1.0) -> bool:
        """
        判断是否需要触发辩论
        
        Args:
            task_result: 任务结果
            context: 背景信息
            confidence: 模型置信度
            
        Returns:
            是否触发辩论
        """
        if self.trigger_policy == "always":
            return True
        
        if self.trigger_policy == "manual":
            return False
        
        # smart策略：按需触发
        # 1. 高价值关键词匹配
        combined_text = f"{task_result} {context}"
        for keyword in self.HIGH_VALUE_KEYWORDS:
            if keyword in combined_text:
                print(f"[DebateVerifier] 触发辩论: 高价值关键词 '{keyword}'")
                return True
        
        # 2. 低置信度
        if confidence < self.LOW_CONFIDENCE_THRESHOLD:
            print(f"[DebateVerifier] 触发辩论: 低置信度 {confidence}")
            return True
        
        # 3. 用户明确要求验证
        if '验证' in combined_text or '确认' in combined_text or '辩论' in combined_text:
            print(f"[DebateVerifier] 触发辩论: 用户明确要求")
            return True
        
        # 默认不触发
        print(f"[DebateVerifier] 不触发辩论: 普通任务")
        return False
    
    def verify(self, task_result: str, context: str = "", confidence: float = 1.0) -> DebateResult:
        """
        验证任务结果
        
        Args:
            task_result: 任务结果描述
            context: 背景信息
            confidence: 模型置信度
            
        Returns:
            DebateResult
        """
        if not self.enabled:
            return DebateResult(
                passed=True,
                consensus=task_result,
                confidence=1.0,
                rounds=0,
                reason="辩论验证已禁用"
            )
        
        # 按需触发判断
        if not self.should_trigger(task_result, context, confidence):
            return DebateResult(
                passed=True,
                consensus=task_result,
                confidence=confidence,
                rounds=0,
                reason="普通任务，无需辩论验证"
            )
        
        # 检查服务可用性
        if not self._check_service():
            return DebateResult(
                passed=True,
                consensus=task_result,
                confidence=0.8,
                rounds=0,
                reason="对抗引擎不可用，默认通过"
            )
        
        # 构建辩论主题
        debate_topic = f"验证以下任务结果的合理性和可信度：\n{task_result[:500]}"
        if context:
            debate_topic = f"背景：{context[:200]}\n\n{debate_topic}"
        
        # 发起辩论
        try:
            debate_response = self._start_debate(debate_topic)
            
            # 解析结果
            return self._parse_debate_result(debate_response)
            
        except Exception as e:
            return DebateResult(
                passed=False,
                consensus="",
                confidence=0.0,
                rounds=0,
                reason=f"辩论失败: {str(e)}"
            )
    
    def _check_service(self) -> bool:
        """检查服务是否可用"""
        try:
            resp = requests.get("http://127.0.0.1:8002/health", timeout=5)
            return resp.status_code == 200
        except:
            return False
    
    def _start_debate(self, topic: str) -> Dict:
        """发起辩论"""
        payload = {
            "topic": topic,
            "max_rounds": self.MAX_ROUNDS
        }
        
        resp = requests.post(
            self.DEBATE_URL,
            json=payload,
            timeout=self.timeout
        )
        
        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception(f"辩论API返回错误: {resp.status_code}")
    
    def _parse_debate_result(self, response: Dict) -> DebateResult:
        """解析辩论结果"""
        status = response.get("status", "unknown")
        convergence = response.get("convergence_score", 0.0)
        total_rounds = response.get("rounds", 0)
        final_consensus = response.get("final_consensus", "")
        
        # 判断是否通过
        if status == "done" and convergence >= self.CONSENSUS_THRESHOLD:
            # 达成共识
            return DebateResult(
                passed=True,
                consensus=final_consensus,
                confidence=convergence,
                rounds=total_rounds,
                reason=f"辩论达成共识，收敛度{convergence*100:.0f}%"
            )
        
        elif status == "partial":
            # 部分收敛，取仲裁者结论
            return DebateResult(
                passed=True,
                consensus=final_consensus,
                confidence=convergence,
                rounds=total_rounds,
                reason=f"辩论部分收敛（{convergence*100:.0f}%），采用仲裁结论"
            )
        
        elif total_rounds >= self.MAX_ROUNDS:
            # 达到最大轮数，强制输出结论
            return DebateResult(
                passed=True,
                consensus=final_consensus or "需人工复核",
                confidence=convergence,
                rounds=total_rounds,
                reason=f"达到最大轮数({self.MAX_ROUNDS}轮)，强制输出结论"
            )
        
        else:
            # 其他情况
            return DebateResult(
                passed=False,
                consensus="",
                confidence=convergence,
                rounds=total_rounds,
                reason="辩论未达成共识"
            )
    
    def quick_verify(self, result: str) -> Tuple[bool, str]:
        """
        快速验证（简化版）
        
        Returns:
            (passed, consensus)
        """
        debate_result = self.verify(result)
        return debate_result.passed, debate_result.consensus


# 测试
if __name__ == "__main__":
    verifier = DebateVerifier()
    
    print("="*50)
    print("🧪 辩论验证器测试")
    print("="*50)
    
    # 测试1：简单结果
    result = "方案设计完成：使用6061铝合金，采用3轴CNC加工，精度±0.05mm，表面阳极氧化，预估成本200元/件"
    
    print(f"\n测试结果: {result[:50]}...")
    print("\n发起辩论验证...")
    
    debate = verifier.verify(result, "CNC零件报价任务")
    
    print(f"\n通过: {debate.passed}")
    print(f"共识: {debate.consensus[:100]}...")
    print(f"置信度: {debate.confidence*100:.0f}%")
    print(f"轮数: {debate.rounds}")
    print(f"原因: {debate.reason}")