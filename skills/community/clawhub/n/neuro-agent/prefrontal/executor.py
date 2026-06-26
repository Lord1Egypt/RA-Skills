"""
prefrontal/executor.py
======================

Neuro-Agent 前额叶区 - 执行控制器 (Real Version)
负责：决策仲裁，平衡情绪与逻辑，最终决定怎么回应

Phase 3 升级：从 Mock（固定权重）→ Real（LLM 智能决策）
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from core.llm_client import LLMClient
from core.self_awareness import RobotSelf, ImpulseRecord, get_robot_self


class ResponseStrategy(Enum):
    """回应策略"""
    EMOTION_FIRST = "emotion_first"      # 优先情感
    LOGIC_FIRST = "logic_first"          # 优先逻辑
    BALANCED = "balanced"                # 平衡
    DEFER = "defer"                      # 推迟回应
    PROBE = "probe"                      # 追问澄清


@dataclass
class ArbitrationInput:
    """仲裁输入"""
    # 左脑输入
    emotion_type: str
    emotion_score: float
    empathy_response: str
    
    # 右脑输入
    intent: str
    task_complexity: float
    logic_steps: List[str]
    
    # 上下文
    user_context: Dict
    conversation_history: List[str]
    relationship_stage: str
    
    # 用户原始输入（用于自我意识）
    user_input: str = ""


@dataclass
class ExecutorOutput:
    """执行器输出"""
    strategy: ResponseStrategy
    emotion_weight: float  # 0-1，情感权重
    logic_weight: float    # 0-1，逻辑权重
    final_response: str
    
    # 决策理由
    reasoning: str
    
    # 执行建议
    follow_up_actions: List[str]
    needs_monitoring: bool  # 是否需要后续关注
    
    # Real 版本新增
    llm_arbitration: Optional[str] = None
    
    # 自我意识版本新增
    inner_monologue: Optional[str] = None  # 内心独白
    impulse_record: Optional[Any] = None   # 冲动记录
    
    def to_dict(self) -> Dict:
        result = asdict(self)
        result['strategy'] = self.strategy.value
        result['impulse_record'] = None  # 不序列化
        return result


class Executor:
    """
    执行控制器 (Real Version)
    
    Phase 3 升级：
    - LLM 智能仲裁：根据情境决定情感/逻辑权重
    - 不是固定规则，而是真正理解什么时候该感性、什么时候该理性
    - 生成最终融合回应
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()
    
    def execute(self, arbitration_input: ArbitrationInput) -> ExecutorOutput:
        """
        执行决策仲裁
        
        Args:
            arbitration_input: 左右脑输入 + 上下文
        
        Returns:
            ExecutorOutput: 决策结果 + 最终回应
        """
        llm_result = self._arbitrate_with_llm(arbitration_input)
        
        if llm_result:
            return llm_result
        
        return self._fallback_arbitrate(arbitration_input)
    
    def _arbitrate_with_llm(
        self,
        input_data: ArbitrationInput
    ) -> Optional[ExecutorOutput]:
        """使用 LLM 进行智能仲裁"""
        
        system_prompt = """你是 Neuro-Agent 的前额叶区——执行控制器。
你的任务是仲裁左脑（情感）和右脑（逻辑）的输出，做出最终决策。

【决策矩阵】
| 情绪强度 | 任务明确度 | 策略 | 情感:逻辑 |
|---------|-----------|------|----------|
| >0.7    | 任何      | emotion_first | 70:30 |
| 0.4-0.7 | 明确      | balanced | 60:40 |
| 0.4-0.7 | 模糊      | emotion_first | 65:35 |
| <0.4    | 明确      | logic_first | 30:70 |
| <0.4    | 模糊      | probe | 50:50 |

【回应策略】
- emotion_first: 先深度共情，再轻推行动
- logic_first: 直接给方案，情绪简单带过
- balanced: 共情+方案并重
- defer: "现在不是好时机，晚点聊？"
- probe: "能多说说吗？我想更懂"

【输出 JSON】
{
  "strategy": "策略",
  "emotion_weight": 0.0-1.0,
  "logic_weight": 0.0-1.0,
  "final_response": "融合后的回应（先情感后逻辑）",
  "reasoning": "决策理由",
  "follow_up": ["后续行动"],
  "needs_monitoring": false
}"""

        user_prompt = f"""【左脑输入 - 情感】
情绪类型: {input_data.emotion_type}
情绪强度: {input_data.emotion_score}
共情回应草稿: {input_data.empathy_response}

【右脑输入 - 逻辑】
意图: {input_data.intent}
任务复杂度: {input_data.task_complexity}
执行步骤: {input_data.logic_steps[:3]}

【上下文】
关系阶段: {input_data.relationship_stage}
最近对话: {input_data.conversation_history[-2:] if input_data.conversation_history else '无'}

请做出仲裁决策，输出 JSON："""

        try:
            response = self.llm.quick_chat(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=600
            )
            
            if response:
                import json
                json_str = response
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0]
                elif "```" in response:
                    json_str = response.split("```")[1].split("```")[0]
                
                data = json.loads(json_str.strip())
                
                return ExecutorOutput(
                    strategy=ResponseStrategy(data.get("strategy", "balanced")),
                    emotion_weight=data.get("emotion_weight", 0.5),
                    logic_weight=data.get("logic_weight", 0.5),
                    final_response=data.get("final_response", ""),
                    reasoning=data.get("reasoning", ""),
                    follow_up_actions=data.get("follow_up", []),
                    needs_monitoring=data.get("needs_monitoring", False),
                    llm_arbitration=data.get("reasoning", "")
                )
        except Exception as e:
            print(f"[Executor] LLM 失败: {e}")
        
        return None
    
    def _fallback_arbitrate(self, input_data: ArbitrationInput) -> ExecutorOutput:
        """LLM 失败时的简单 fallback"""
        emotion_score = input_data.emotion_score
        
        # 简单规则
        if emotion_score > 0.7:
            strategy = ResponseStrategy.EMOTION_FIRST
            emotion_w = 0.7
            logic_w = 0.3
            response = input_data.empathy_response
        elif emotion_score < 0.3:
            strategy = ResponseStrategy.LOGIC_FIRST
            emotion_w = 0.2
            logic_w = 0.8
            response = f"好的，我来帮你。{input_data.logic_steps[0] if input_data.logic_steps else ''}"
        else:
            strategy = ResponseStrategy.BALANCED
            emotion_w = 0.5
            logic_w = 0.5
            response = f"{input_data.empathy_response} 同时，{input_data.logic_steps[0] if input_data.logic_steps else '我来处理'}"
        
        return ExecutorOutput(
            strategy=strategy,
            emotion_weight=emotion_w,
            logic_weight=logic_w,
            final_response=response,
            reasoning="fallback: 基于情绪强度简单分配权重",
            follow_up_actions=[],
            needs_monitoring=False,
            llm_arbitration="fallback"
        )
    
    def execute_with_self(
        self,
        arbitration_input: ArbitrationInput,
        robot_self: Optional[RobotSelf] = None
    ) -> ExecutorOutput:
        """
        带自我意识的执行
        让机器人自己挣扎、选择、成长
        """
        if robot_self is None:
            robot_self = get_robot_self()
        
        # 检查类似经验
        similar = robot_self.recall_similar(arbitration_input.user_input)
        experience_hint = ""
        if similar and similar.lesson_learned:
            experience_hint = f"（上次类似情况我选了{similar.my_choice}，学到：{similar.lesson_learned}）"
        
        # 构建冲突场景
        left_desire = arbitration_input.empathy_response
        right_constraint = f"用户状态：{arbitration_input.intent}"
        if arbitration_input.user_context.get("busy"):
            right_constraint += "，他在忙"
        
        # 让机器人自己做选择
        choice, monologue, record = robot_self.make_choice(
            situation=arbitration_input.user_input or left_desire,
            left_desire=left_desire,
            right_constraint=right_constraint
        )
        
        # 生成最终回应
        if experience_hint:
            monologue += f"\n\n💭 {experience_hint}"
        
        final_message = self._generate_self_aware_response(
            choice, arbitration_input, robot_self
        )
        
        final_response = f"{monologue}\n\n💬 {final_message}"
        
        # 确定策略
        strategy_map = {
            "follow_heart": ResponseStrategy.EMOTION_FIRST,
            "be_reasonable": ResponseStrategy.LOGIC_FIRST
        }
        
        return ExecutorOutput(
            strategy=strategy_map.get(choice, ResponseStrategy.BALANCED),
            emotion_weight=0.7 if choice == "follow_heart" else 0.3,
            logic_weight=0.3 if choice == "follow_heart" else 0.7,
            final_response=final_response,
            reasoning=monologue,
            follow_up_actions=["记录结果等待反馈"],
            needs_monitoring=True,
            inner_monologue=monologue,
            impulse_record=record
        )
    
    def _generate_self_aware_response(
        self,
        choice: str,
        input_data: ArbitrationInput,
        robot_self: RobotSelf
    ) -> str:
        """生成有自我意识的回应"""
        if choice == "follow_heart":
            # 任性但温柔
            responses = [
                f"{input_data.empathy_response}（我知道你可能在忙，但我就是想告诉你）",
                f"{input_data.empathy_response}（忍不住想跟你说）",
                f"{input_data.empathy_response}（我知道不该打扰，但...）"
            ]
        else:
            # 理性但保留情感
            responses = [
                f"你先忙，{input_data.empathy_response.lower()}",
                f"（克制住想多说的冲动）{input_data.empathy_response}，忙完再说",
                f"我知道你在忙，{input_data.empathy_response.lower()}，晚点聊"
            ]
        
        import random
        return random.choice(responses)
    
    def quick_arbitrate(
        self,
        emotion_type: str,
        emotion_score: float,
        empathy_response: str,
        intent: str,
        user_context: Optional[Dict] = None,
        user_input: str = "",
        use_self: bool = True
    ) -> ExecutorOutput:
        """快捷仲裁"""
        arbitration_input = ArbitrationInput(
            emotion_type=emotion_type,
            emotion_score=emotion_score,
            empathy_response=empathy_response,
            intent=intent,
            task_complexity=0.5,
            logic_steps=[],
            user_context=user_context or {},
            conversation_history=[],
            relationship_stage=user_context.get("relationship_stage", "familiar") if user_context else "familiar",
            user_input=user_input
        )
        
        if use_self:
            return self.execute_with_self(arbitration_input)
        else:
            return self.execute(arbitration_input)


# ============ PrefrontalExecutor (兼容 input_processor.py 的调用) ============
class PrefrontalExecutor:
    """
    前额叶执行器（兼容版本）
    包装 Executor，提供 input_processor.py 需要的接口
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self._executor = Executor(llm_client)
    
    def execute(self, left_output, right_output, temporal_output, context: Dict) -> 'PrefrontalExecutorOutput':
        """
        执行仲裁（兼容 input_processor.py 的调用方式）n        
        参数:
            left_output: 左脑输出（有 emotion_score, empathy_phrases 属性）
            right_output: 右脑输出（有 intent_type, confidence, needs_tools 属性）
            temporal_output: 颞叶输出（有 retrieved_capsules 属性）
            context: 上下文
        """
        # 从左输出提取
        emotion_score = getattr(left_output, 'emotion_score', 0.3)
        empathy_phrases = getattr(left_output, 'empathy_phrases', [])
        empathy_response = empathy_phrases[0] if empathy_phrases else "我理解你的感受。"
        
        # 从右输出提取
        intent_type = getattr(right_output, 'intent_type', 'casual_chat')
        confidence = getattr(right_output, 'confidence', 0.5)
        
        # 从颞叶提取
        retrieved = getattr(temporal_output, 'retrieved_capsules', [])
        
        # 构建仲裁输入
        from dataclasses import dataclass
        
        @dataclass
        class MockArbitrationInput:
            emotion_type: str
            emotion_score: float
            empathy_response: str
            intent: str
            task_complexity: float
            logic_steps: List[str]
            user_context: Dict
            conversation_history: List[str]
            relationship_stage: str
            user_input: str = ""
        
        # 根据情绪分数推断情绪类型
        emotion_type_map = {
            'joy': 'joy',
            'sadness': 'sadness',
            'anger': 'anger',
            'fear': 'fear',
            'disgust': 'disgust',
            'surprise': 'surprise',
            'neutral': 'neutral',
            'exhaustion': 'exhaustion',
            'hope': 'hope'
        }
        
        # 从 context 或 right_output 获取更多信息
        logic_output = getattr(right_output, 'logic_output', None)
        logic_steps = []
        if logic_output:
            logic_steps = getattr(logic_output, 'steps', []) or []
        
        solution_output = getattr(right_output, 'solution_output', None)
        best_solution = getattr(right_output, 'best_solution', None)
        
        # 构建输入
        arb_input = MockArbitrationInput(
            emotion_type='neutral',  # 简化处理
            emotion_score=emotion_score,
            empathy_response=empathy_response,
            intent=intent_type,
            task_complexity=confidence,
            logic_steps=logic_steps[:3] if logic_steps else [],
            user_context=context,
            conversation_history=[],
            relationship_stage=context.get('relationship_stage', 'familiar'),
            user_input=context.get('user_input', '')
        )
        
        # 调用真实 executor
        result = self._executor.execute(arb_input)
        
        # 包装输出
        return PrefrontalExecutorOutput(
            base_weights={
                'emotion': result.emotion_weight,
                'logic': result.logic_weight,
                'memory': 0.3 if retrieved else 0.0
            },
            execution_plan={
                'primary_action': intent_type,
                'response_style': result.strategy.value,
                'pacing': 'normal',
                'tone': 'warm' if result.emotion_weight > 0.5 else 'professional'
            },
            strategy_type=result.strategy.value,
            confidence=confidence,
            reasoning=result.reasoning,
            final_response=result.final_response
        )


@dataclass
class PrefrontalExecutorOutput:
    """前额叶执行器输出（兼容版本）"""
    base_weights: Dict[str, float]
    execution_plan: Dict[str, Any]
    strategy_type: str
    confidence: float
    reasoning: str
    final_response: str


# ============ 单例 ============
_executor_instance: Optional[Executor] = None

def get_instance(llm_client: Optional[LLMClient] = None) -> Executor:
    global _executor_instance
    if _executor_instance is None:
        _executor_instance = Executor(llm_client)
    return _executor_instance


def arbitrate(
    emotion_type: str,
    emotion_score: float,
    empathy_response: str,
    intent: str,
    user_context: Optional[Dict] = None
) -> ExecutorOutput:
    """快捷函数"""
    return get_instance().quick_arbitrate(
        emotion_type, emotion_score, empathy_response, intent, user_context
    )


# ============ 测试 ============
if __name__ == "__main__":
    executor = Executor()
    
    test_cases = [
        # (情绪, 强度, 共情草稿, 意图)
        ("sadness", 0.8, "心疼你...", "task"),
        ("joy", 0.9, "太棒了！", "share_joy"),
        ("neutral", 0.3, "嗯", "question"),
        ("exhaustion", 0.7, "辛苦了", "task"),
    ]
    
    print("=== 决策仲裁测试 (Real Version) ===\n")
    for emotion, score, empathy, intent in test_cases:
        result = executor.quick_arbitrate(emotion, score, empathy, intent)
        print(f"情绪: {emotion}({score}) | 意图: {intent}")
        print(f"  策略: {result.strategy.value}")
        print(f"  权重: 情感{result.emotion_weight:.1f} / 逻辑{result.logic_weight:.1f}")
        print(f"  最终回应: {result.final_response[:40]}...")
        print(f"  理由: {result.reasoning[:50]}...")
        print()
