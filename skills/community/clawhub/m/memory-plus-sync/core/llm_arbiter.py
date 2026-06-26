"""
大模型仲裁模块

当三代理投票结果分歧时，调用第四个大模型进行最终仲裁
"""

import json
import time
from typing import Dict, Optional
from pathlib import Path
from dataclasses import dataclass

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from configs.cloud_models_config import get_cloud_config, create_cloud_client, get_available_cloud_models
from .triple_agent_processor import AgentResponse
from .vote_aggregator import AggregatedResult, VoteResult


@dataclass
class ArbitrationResult:
    """仲裁结果"""
    final_decision: str  # STORE, REVIEW, REJECT, MERGE
    confidence: float  # 0.0-1.0
    reasoning: str
    model_used: str
    latency_ms: float
    success: bool
    error_message: Optional[str] = None


class LLMArbiter:
    """大模型仲裁器 - 使用 Kimi API"""
    
    def __init__(self, use_kimi: bool = True, arbiter_model: Optional[str] = None):
        """
        初始化仲裁器
        
        Args:
            use_kimi: 是否使用 Kimi API (默认 True)
            arbiter_model: 指定仲裁模型名称 (可选)
        """
        self.use_kimi = use_kimi
        self.arbiter_model = arbiter_model
        self.client = None
        self.model_name = None
        
        self._init_client()
    
    def _init_client(self):
        """初始化仲裁模型客户端 - 使用 Kimi API"""
        if self.use_kimi:
            config = get_cloud_config()
            if not config.kimi_api_key:
                raise ConnectionError("Kimi API Key 未配置")
            self.client, self.model_name = create_cloud_client("kimi", config)
            self.model_name = self.arbiter_model or self.model_name
        else:
            config = get_cloud_config()
            # 默认使用 Qwen 作为仲裁模型 (更可靠)
            self.client, self.model_name = create_cloud_client("qwen", config)
            self.model_name = self.arbiter_model or self.model_name
    
    def _build_arbitration_prompt(
        self,
        memory_content: str,
        aggregated_result: AggregatedResult
    ) -> str:
        """
        构建仲裁 Prompt
        
        Args:
            memory_content: 原始记忆内容
            aggregated_result: 投票聚合结果
        
        Returns:
            仲裁 Prompt
        """
        # 整理三个代理的意见
        agent_opinions = []
        for agent_name, response in aggregated_result.agent_responses.items():
            if response.success:
                opinion = f"{agent_name}: {json.dumps(response.response_data, ensure_ascii=False)}"
            else:
                opinion = f"{agent_name}: 调用失败 - {response.error_message}"
            agent_opinions.append(opinion)
        
        prompt = f"""你是一位经验丰富的记忆管理仲裁专家。现在有三个代理对一段记忆内容的处理意见出现分歧，请你进行最终裁决。

## 待处理的记忆内容
{memory_content}

## 三个代理的意见

{chr(10).join(agent_opinions)}

## 投票聚合结果
- 投票分布：{aggregated_result.vote_counts}
- 平均评分：{aggregated_result.avg_total_score}
- 风险等级：{aggregated_result.risk_level or '未知'}
- 分歧原因：{aggregated_result.reasoning}

## 你的任务
请综合以上信息，做出最终裁决。你需要考虑：
1. 记忆内容的真实价值和重要性
2. 各代理意见的合理性
3. 潜在的风险和问题
4. 存储的长期影响

## 输出格式
请严格按照以下 JSON 格式输出：

```json
{{
  "final_decision": "STORE" | "REVIEW" | "REJECT" | "MERGE",
  "confidence": 0.0-1.0,
  "reasoning": "详细裁决理由，200 字以内",
  "key_factors": ["因素 1", "因素 2", ...],
  "suggested_tags": ["标签 1", "标签 2"],
  "follow_up_actions": ["后续行动建议"]
}}
```

## 裁决标准
- **STORE**: 明确有价值，值得存储
- **REVIEW**: 需要人工进一步审核
- **REJECT**: 存在严重问题，不应存储
- **MERGE**: 建议与现有记忆合并

请开始你的裁决。"""
        
        return prompt
    
    def arbitrate(
        self,
        memory_content: str,
        aggregated_result: AggregatedResult
    ) -> ArbitrationResult:
        """
        执行仲裁
        
        Args:
            memory_content: 原始记忆内容
            aggregated_result: 投票聚合结果
        
        Returns:
            ArbitrationResult: 仲裁结果
        """
        start_time = time.time()
        
        try:
            # 构建仲裁 Prompt
            prompt = self._build_arbitration_prompt(memory_content, aggregated_result)
            
            # 调用仲裁模型
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是一位公正的记忆管理仲裁专家，输出严格的 JSON 格式。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # 更低温度提高一致性
                max_tokens=1024
            )
            
            # 解析响应
            content = response.choices[0].message.content.strip()
            
            # 提取 JSON
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            response_data = json.loads(content)
            
            latency_ms = (time.time() - start_time) * 1000
            
            return ArbitrationResult(
                final_decision=response_data.get("final_decision", "REVIEW"),
                confidence=response_data.get("confidence", 0.5),
                reasoning=response_data.get("reasoning", "无说明"),
                model_used=self.model_name,
                latency_ms=latency_ms,
                success=True
            )
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return ArbitrationResult(
                final_decision="REVIEW",  # 仲裁失败时默认需要人工审核
                confidence=0.0,
                reasoning=f"仲裁过程出错：{str(e)}",
                model_used=self.model_name,
                latency_ms=latency_ms,
                success=False,
                error_message=str(e)
            )


if __name__ == "__main__":
    # 测试仲裁功能
    print("=== 仲裁功能测试 ===\n")
    
    # 模拟分歧的投票结果
    from .vote_aggregator import AggregatedResult, VoteResult
    
    test_memory = """
    2026-04-03 测试记忆：这条记忆可能存在争议，用于测试仲裁功能。
    """
    
    mock_responses = {
        "validator": AgentResponse(
            agent_name="validator",
            model_used="moonshot-v1-8k",
            response_data={"suggested_action": "STORE", "total_score": 35, "confidence": 0.8},
            latency_ms=200,
            success=True
        ),
        "scorer": AgentResponse(
            agent_name="scorer",
            model_used="moonshot-v1-8k",
            response_data={"priority_level": 2, "total_score": 25, "confidence": 0.6},
            latency_ms=220,
            success=True
        ),
        "reviewer": AgentResponse(
            agent_name="reviewer",
            model_used="moonshot-v1-8k",
            response_data={"recommended_action": "REVIEW", "risk_level": "MEDIUM", "confidence": 0.7},
            latency_ms=180,
            success=True
        )
    }
    
    mock_aggregated = AggregatedResult(
        vote_result=VoteResult.SPLIT_DECISION,
        vote_counts={"STORE": 1, "REVIEW": 1, "REJECT": 1},
        final_decision="REVIEW",
        confidence=0.7,
        reasoning="三个代理意见完全分歧",
        needs_arbitration=True,
        agent_responses=mock_responses,
        avg_total_score=28.3,
        risk_level="MEDIUM"
    )
    
    arbiter = LLMArbiter(use_kimi=True)
    result = arbiter.arbitrate(test_memory, mock_aggregated)
    
    print(f"仲裁结果:")
    print(f"  最终决定：{result.final_decision}")
    print(f"  置信度：{result.confidence:.2f}")
    print(f"  使用模型：{result.model_used}")
    print(f"  耗时：{result.latency_ms:.0f}ms")
    print(f"  状态：{'✅ 成功' if result.success else '❌ 失败'}")
    print(f"\n  裁决理由：{result.reasoning}")
    
    print("\n=== 测试完成 ===")
