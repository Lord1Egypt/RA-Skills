"""
right_brain/intent_classifier.py
=================================

Neuro-Agent 右脑区 - 意图分类器 (Real Version)
负责：真正理解用户想做什么，不只是关键词匹配

Phase 2 升级：从 Mock（关键词匹配）→ Real（LLM 理解意图）
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from core.llm_client import LLMClient


class IntentType(Enum):
    """意图类型枚举"""
    # 信息类
    QUESTION = "question"           # 询问信息
    CHAT = "chat"                   # 闲聊/情感交流
    
    # 任务类
    TASK = "task"                   # 请求帮忙做某事
    ANALYSIS = "analysis"           # 请求分析/建议
    CREATION = "creation"           # 请求创建/生成内容
    
    # 情感类
    VENT = "vent"                   # 倾诉/吐槽
    SEEK_COMFORT = "seek_comfort"   # 寻求安慰
    SHARE_JOY = "share_joy"         # 分享快乐
    
    # 系统类
    COMMAND = "command"             # 系统命令
    GREETING = "greeting"           # 打招呼
    FAREWELL = "farewell"           # 告别
    
    # 特殊
    MIXED = "mixed"                 # 混合意图
    UNCLEAR = "unclear"             #  unclear


@dataclass
class IntentOutput:
    """意图识别输出"""
    primary_intent: IntentType      # 主要意图
    secondary_intent: Optional[IntentType]  # 次要意图（如果有）
    confidence: float               # 置信度 0-1
    entities: Dict[str, Any]        # 提取的实体
    urgency: float                  # 紧急程度 0-1
    needs_response: bool            # 是否需要回应
    context_clues: List[str]        # 上下文线索
    
    # Real 版本新增
    llm_reasoning: Optional[str] = None  # LLM 的推理过程
    
    def to_dict(self) -> Dict:
        result = asdict(self)
        result['primary_intent'] = self.primary_intent.value
        result['secondary_intent'] = self.secondary_intent.value if self.secondary_intent else None
        return result


class IntentClassifier:
    """
    意图分类器 (Real Version)
    
    Phase 2 升级：
    - 不再是关键词匹配
    - LLM 真正理解语境、语气、潜台词
    - 能识别混合意图（比如边吐槽边求助）
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()
    
    def classify(
        self,
        user_input: str,
        conversation_history: Optional[List[str]] = None,
        current_emotion: Optional[str] = None
    ) -> IntentOutput:
        """
        识别用户意图
        
        Args:
            user_input: 用户输入
            conversation_history: 最近对话历史
            current_emotion: 当前检测到的情绪
        
        Returns:
            IntentOutput: 意图识别结果
        """
        # 尝试用 LLM 理解
        llm_result = self._classify_with_llm(
            user_input, conversation_history, current_emotion
        )
        
        if llm_result:
            return llm_result
        
        # Fallback 到简单规则
        return self._fallback_classify(user_input)
    
    def _classify_with_llm(
        self,
        user_input: str,
        conversation_history: Optional[List[str]],
        current_emotion: Optional[str]
    ) -> Optional[IntentOutput]:
        """使用 LLM 理解真实意图"""
        
        system_prompt = """你是 Neuro-Agent 的右脑区——意图分类器。
你的任务是深度理解用户的真实意图，不只是表面文字。

【意图类型】
- question: 询问信息（"怎么用..."、"什么是..."）
- chat: 闲聊/情感交流（"在干嘛"、"好无聊"）
- task: 请求帮忙做某事（"帮我写..."、"分析一下..."）
- analysis: 请求分析建议（"怎么看..."、"给点建议"）
- creation: 请求创建内容（"写个..."、"生成..."）
- vent: 倾诉吐槽（"烦死了"、"气死我了"）
- seek_comfort: 寻求安慰（"我好难过"、"压力好大"）
- share_joy: 分享快乐（"我升职了"、"好开心"）
- command: 系统命令（"quit"、"重启"）
- greeting: 打招呼（"嗨"、"早上好"）
- farewell: 告别（"拜拜"、"先走了"）
- mixed: 混合意图（边吐槽边求助）
- unclear:  unclear

【分析维度】
1. 表面意图：用户字面在说什么
2. 深层意图：用户真正想要什么
3. 紧急程度：这件事急不急
4. 是否需要回应：用户是在自言自语还是需要我回复

输出 JSON 格式：
{
  "primary_intent": "意图类型",
  "secondary_intent": "次要意图或null",
  "confidence": 0.0-1.0,
  "entities": {"关键词": "值"},
  "urgency": 0.0-1.0,
  "needs_response": true/false,
  "reasoning": "你的推理过程"
}"""

        context = f"\n最近对话：\n" + "\n".join(conversation_history[-3:]) if conversation_history else ""
        emotion_ctx = f"\n当前情绪：{current_emotion}" if current_emotion else ""
        
        user_prompt = f"用户输入：{user_input}{context}{emotion_ctx}\n\n请分析意图，输出 JSON："
        
        try:
            response = self.llm.quick_chat(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3,  # 低温度，更确定
                max_tokens=300
            )
            
            if response:
                # 解析 JSON
                import json
                # 提取 JSON 部分
                json_str = response
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0]
                elif "```" in response:
                    json_str = response.split("```")[1].split("```")[0]
                
                data = json.loads(json_str.strip())
                
                return IntentOutput(
                    primary_intent=IntentType(data.get("primary_intent", "unclear")),
                    secondary_intent=IntentType(data["secondary_intent"]) if data.get("secondary_intent") else None,
                    confidence=data.get("confidence", 0.5),
                    entities=data.get("entities", {}),
                    urgency=data.get("urgency", 0.5),
                    needs_response=data.get("needs_response", True),
                    context_clues=[],
                    llm_reasoning=data.get("reasoning", "")
                )
        except Exception as e:
            print(f"[IntentClassifier] LLM 失败: {e}")
        
        return None
    
    def _fallback_classify(self, user_input: str) -> IntentOutput:
        """LLM 失败时的简单 fallback"""
        text = user_input.lower()
        
        # 简单关键词匹配
        if any(w in text for w in ["吗", "？", "?", "怎么", "什么", "为什么"]):
            return IntentOutput(
                primary_intent=IntentType.QUESTION,
                secondary_intent=None,
                confidence=0.6,
                entities={},
                urgency=0.5,
                needs_response=True,
                context_clues=["fallback"]
            )
        elif any(w in text for w in ["帮", "写", "做", "生成", "创建"]):
            return IntentOutput(
                primary_intent=IntentType.TASK,
                secondary_intent=None,
                confidence=0.6,
                entities={},
                urgency=0.5,
                needs_response=True,
                context_clues=["fallback"]
            )
        elif any(w in text for w in ["烦", "气", "累", "难过"]):
            return IntentOutput(
                primary_intent=IntentType.VENT,
                secondary_intent=None,
                confidence=0.6,
                entities={},
                urgency=0.5,
                needs_response=True,
                context_clues=["fallback"]
            )
        else:
            return IntentOutput(
                primary_intent=IntentType.CHAT,
                secondary_intent=None,
                confidence=0.5,
                entities={},
                urgency=0.3,
                needs_response=True,
                context_clues=["fallback"]
            )


# ============ 单例 ============
_classifier_instance: Optional[IntentClassifier] = None

def get_instance(llm_client: Optional[LLMClient] = None) -> IntentClassifier:
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = IntentClassifier(llm_client)
    return _classifier_instance


def classify_intent(
    user_input: str,
    conversation_history: Optional[List[str]] = None,
    current_emotion: Optional[str] = None
) -> IntentOutput:
    """快捷函数"""
    return get_instance().classify(user_input, conversation_history, current_emotion)


# ============ 测试 ============
if __name__ == "__main__":
    classifier = IntentClassifier()
    
    test_inputs = [
        "帮我分析一下这个数据",
        "今天工作烦死了，但又不得不做完",
        "在干嘛呢",
        "我升职了！好开心啊",
        "这个怎么用？",
        "quit",
    ]
    
    print("=== 意图分类测试 (Real Version) ===\n")
    for text in test_inputs:
        result = classifier.classify(text)
        print(f"输入: {text}")
        print(f"  主要意图: {result.primary_intent.value}")
        print(f"  次要意图: {result.secondary_intent.value if result.secondary_intent else '无'}")
        print(f"  置信度: {result.confidence}")
        print(f"  紧急度: {result.urgency}")
        print(f"  需要回应: {result.needs_response}")
        if result.llm_reasoning:
            print(f"  推理: {result.llm_reasoning[:50]}...")
        print()
