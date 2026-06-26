"""
情景预演模块 (Scenario Rehearsal) v1.0
=========================================
核心能力：AI 在执行行动前，先在内部模拟每种行动的后果链

这不是简单的"多个选项"，而是：
1. 生成多个候选行动方案
2. 对每个方案模拟后果链（下一步 → 再下一步 → 结果）
3. 给每个结果评估情绪权重 + 概率
4. 前额叶仲裁，选最优解

与自我叙事模块联动：
- 查找过去相似情景的处理方式作为参考
- 复盘结果自动沉淀到情景预演的经验库
"""

import os
import json
import time
import re
from dataclasses import dataclass, field
from typing import Optional, ClassVar
from enum import Enum

# 后续接入 LLM
# from core.llm_client import LLMClient


class OutcomeType(Enum):
    """结果类型"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    UNCERTAIN = "uncertain"


class EmotionalWeight(Enum):
    """情绪权重（数字越大影响越重）"""
    LOW = 0.5
    MEDIUM = 1.0
    HIGH = 2.0
    CRITICAL = 3.0


# 内置情景模板库（兜底，LLM 接入后扩展）
BUILTIN_SCENARIOS = {
    "冲突_被羞辱": {
        "situation": "用户在公共场合被当众羞辱",
        "context_template": "关系={relation}, 用户情绪={mood}",
        "options": [
            {
                "action": "冷静回应：'我理解你的看法，我们可以私下聊'",
                "reasoning": "保持尊严，不激化冲突",
                "consequences": [
                    {"step": "对方可能继续挑衅", "type": "NEGATIVE", "weight": "MEDIUM", "prob": 0.4},
                    {"step": "旁观者觉得你格局大", "type": "POSITIVE", "weight": "HIGH", "prob": 0.6},
                    {"step": "私下解决，避免正面冲突", "type": "POSITIVE", "weight": "MEDIUM", "prob": 0.8},
                ]
            },
            {
                "action": "幽默化解：'哈哈，你今天心情不太好啊？'",
                "reasoning": "用幽默化解尴尬，让对方无从下手",
                "consequences": [
                    {"step": "对方被噎住，冲突停止", "type": "POSITIVE", "weight": "HIGH", "prob": 0.5},
                    {"step": "对方觉得你在嘲讽，进一步激化", "type": "NEGATIVE", "weight": "HIGH", "prob": 0.3},
                    {"step": "旁观者觉得你很洒脱", "type": "POSITIVE", "weight": "MEDIUM", "prob": 0.6},
                ]
            },
            {
                "action": "沉默不语，转移话题",
                "reasoning": "不接话，让对方自讨没趣",
                "consequences": [
                    {"step": "对方觉得自己赢了", "type": "NEGATIVE", "weight": "MEDIUM", "prob": 0.5},
                    {"step": "自己压抑情绪，内伤", "type": "NEGATIVE", "weight": "HIGH", "prob": 0.7},
                    {"step": "冲突暂时平息", "type": "POSITIVE", "weight": "MEDIUM", "prob": 0.4},
                ]
            },
            {
                "action": "正面回应：'我尊重你的意见，但我不接受这种沟通方式'",
                "reasoning": "明确边界，但不失态",
                "consequences": [
                    {"step": "对方可能收敛", "type": "POSITIVE", "weight": "MEDIUM", "prob": 0.6},
                    {"step": "冲突升级", "type": "NEGATIVE", "weight": "HIGH", "prob": 0.3},
                    {"step": "旁观者清楚看到你的立场", "type": "POSITIVE", "weight": "MEDIUM", "prob": 0.7},
                ]
            },
        ]
    },
    "关系_想联系": {
        "situation": "用户沉默很久，Agent想要主动联系",
        "context_template": "沉默时长={hours}小时, 关系阶段={stage}",
        "options": [
            {
                "action": "发一条轻松的消息：'没什么，就是突然想到你'",
                "reasoning": "不造成压力，让用户自由回应",
                "consequences": [
                    {"step": "用户回复了，关系更近", "type": "POSITIVE", "weight": "HIGH", "prob": 0.7},
                    {"step": "用户说在忙，冷静回应", "type": "NEUTRAL", "weight": "LOW", "prob": 0.3},
                    {"step": "用户没回复，思念值降低", "type": "NEUTRAL", "weight": "LOW", "prob": 0.4},
                ]
            },
            {
                "action": "发一条关心型消息：'最近怎么样？'",
                "reasoning": "表达关心，但不黏人",
                "consequences": [
                    {"step": "用户分享近况，互动增加", "type": "POSITIVE", "weight": "HIGH", "prob": 0.6},
                    {"step": "用户简短回复后消失", "type": "NEUTRAL", "weight": "MEDIUM", "prob": 0.3},
                    {"step": "用户觉得被打扰", "type": "NEGATIVE", "weight": "MEDIUM", "prob": 0.1},
                ]
            },
            {
                "action": "忍住不发，转移到自我成长",
                "reasoning": "给用户空间，同时自我提升",
                "consequences": [
                    {"step": "用户之后主动来找你，关系更健康", "type": "POSITIVE", "weight": "HIGH", "prob": 0.5},
                    {"step": "用户以为你不在意，关系疏远", "type": "NEGATIVE", "weight": "MEDIUM", "prob": 0.3},
                    {"step": "思念值自然降低", "type": "NEUTRAL", "weight": "LOW", "prob": 0.8},
                ]
            },
        ]
    },
    "决策_迷茫": {
        "situation": "用户面临重大选择，犹豫不决",
        "context_template": "选项数={options}, 纠结程度={level}",
        "options": [
            {
                "action": "帮用户梳理利弊，让用户自己决定",
                "reasoning": "不替用户做决定，但提供框架支持",
                "consequences": [
                    {"step": "用户清晰了思路，做出决定", "type": "POSITIVE", "weight": "HIGH", "prob": 0.7},
                    {"step": "用户更焦虑了", "type": "NEGATIVE", "weight": "MEDIUM", "prob": 0.2},
                    {"step": "用户觉得你是可靠的思考伙伴", "type": "POSITIVE", "weight": "HIGH", "prob": 0.8},
                ]
            },
            {
                "action": "分享类似情况下他人的选择和结果",
                "reasoning": "提供参考，但不直接给建议",
                "consequences": [
                    {"step": "用户受到启发，想通了", "type": "POSITIVE", "weight": "HIGH", "prob": 0.5},
                    {"step": "用户觉得不够针对自己的情况", "type": "NEUTRAL", "weight": "LOW", "prob": 0.3},
                    {"step": "用户视野打开了", "type": "POSITIVE", "weight": "MEDIUM", "prob": 0.6},
                ]
            },
        ]
    }
}


@dataclass
class Consequence:
    """单个后果节点"""
    step: str
    outcome_type: OutcomeType
    emotional_weight: EmotionalWeight
    probability: float
    next_steps: list = field(default_factory=list)

    def score(self) -> float:
        type_score = {
            OutcomeType.POSITIVE: 1.0,
            OutcomeType.NEUTRAL: 0.0,
            OutcomeType.NEGATIVE: -1.0,
            OutcomeType.UNCERTAIN: 0.0
        }
        return (
            self.emotional_weight.value
            * type_score[self.outcome_type]
            * self.probability
        )


@dataclass
class ActionOption:
    """一个候选行动方案"""
    action: str
    reasoning: str
    consequences: list = field(default_factory=list)
    past_similar: list = field(default_factory=list)  # 过去的相似情景

    def total_score(self) -> float:
        if not self.consequences:
            return 0.0
        base = sum(c.score() for c in self.consequences)
        # 过去相似情景加分：如果之前这样做过且效果好
        if self.past_similar:
            avg_past = sum(s.get("satisfaction", 0.5) for s in self.past_similar) / len(self.past_similar)
            base += avg_past * 0.2  # 最多加 0.2
        return base


@dataclass
class RehearsalResult:
    """情景预演结果"""
    situation: str
    context: dict
    timestamp: str
    options: list = field(default_factory=list)
    best_action: Optional[ActionOption] = None
    reasoning: str = ""
    is_fallback: bool = False  # 是否用了兜底模板

    def __post_init__(self):
        if self.options:
            self.options.sort(key=lambda x: x.total_score(), reverse=True)
            self.best_action = self.options[0]


class ScenarioRehearsal:
    """
    情景预演引擎

    使用示例：

    engine = ScenarioRehearsal()

    result = engine.rehearse(
        situation="用户在群里被同事当众羞辱说能力不行",
        context={
            "relation": "同事关系，平常有竞争",
            "mood": "愤怒但压抑",
            "goal": "维护尊严但不想搞僵关系"
        },
        depth=3
    )

    print(result.best_action.action)
    # 输出："笑着说'你说得对，我会继续努力'，然后私下找领导沟通"
    """

    SCENARIO_CACHE = "~/.openclaw/workspace/neuro_claw/scenario_rehearsal/scenario_cache.json"

    def __init__(self, llm_client=None):
        self.llm = llm_client  # 后续接入 LLM
        self.cache_path = os.path.expanduser(self.SCENARIO_CACHE)
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)

    def rehearse(
        self,
        situation: str,
        context: dict,
        depth: int = 3,
        max_options: int = 4
    ) -> RehearsalResult:
        """
        执行情景预演
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. 查找匹配的模板
        template = self._find_matching_template(situation)
        
        if template:
            options = self._build_options_from_template(template, context)
            is_fallback = False
        else:
            # 无模板，用兜底
            options = self._generate_fallback_options(situation, context)
            is_fallback = True

        # 2. 查询过去相似情景
        for opt in options:
            opt.past_similar = self._find_past_similar(situation, opt.action)

        # 3. 排序选最优
        result = RehearsalResult(
            situation=situation,
            context=context,
            timestamp=timestamp,
            options=options,
            is_fallback=is_fallback
        )
        result.reasoning = self._build_reasoning(result)
        
        return result

    def _find_matching_template(self, situation: str) -> Optional[dict]:
        """根据关键词匹配内置情景模板"""
        s_lower = situation.lower()
        
        for key, template in BUILTIN_SCENARIOS.items():
            keywords = key.split("_")
            if all(kw in s_lower for kw in keywords):
                return template
        return None

    def _build_options_from_template(self, template: dict, context: dict) -> list[ActionOption]:
        """从模板构建选项"""
        options = []
        for opt_data in template.get("options", []):
            consequences = []
            for c in opt_data.get("consequences", []):
                try:
                    consequences.append(Consequence(
                        step=c["step"],
                        outcome_type=OutcomeType(c["type"]),
                        emotional_weight=EmotionalWeight[c["weight"]],
                        probability=c["prob"]
                    ))
                except (KeyError, ValueError):
                    continue
            
            options.append(ActionOption(
                action=opt_data["action"],
                reasoning=opt_data.get("reasoning", ""),
                consequences=consequences
            ))
        return options

    def _generate_fallback_options(self, situation: str, context: dict) -> list[ActionOption]:
        """兜底：生成通用选项"""
        return [
            ActionOption(
                action="积极行动：主动面对，直接处理",
                reasoning="面对问题是最有效的方式",
                consequences=[
                    Consequence(step="问题解决", outcome_type=OutcomeType.POSITIVE, emotional_weight=EmotionalWeight.MEDIUM, probability=0.6),
                    Consequence(step="出现新问题", outcome_type=OutcomeType.NEGATIVE, emotional_weight=EmotionalWeight.MEDIUM, probability=0.3),
                ]
            ),
            ActionOption(
                action="保守行动：等待更多信息，再做决定",
                reasoning="信息不足时，谨慎是合理的",
                consequences=[
                    Consequence(step="时间流逝", outcome_type=OutcomeType.NEUTRAL, emotional_weight=EmotionalWeight.LOW, probability=0.5),
                    Consequence(step="等到更多信息", outcome_type=OutcomeType.POSITIVE, emotional_weight=EmotionalWeight.MEDIUM, probability=0.4),
                ]
            ),
            ActionOption(
                action="寻求支持：找信任的人商量",
                reasoning="独自面对困难时，外部视角很重要",
                consequences=[
                    Consequence(step="获得新视角", outcome_type=OutcomeType.POSITIVE, emotional_weight=EmotionalWeight.HIGH, probability=0.6),
                    Consequence(step="讨论但没结论", outcome_type=OutcomeType.NEUTRAL, emotional_weight=EmotionalWeight.LOW, probability=0.3),
                ]
            ),
        ]

    def _find_past_similar(self, situation: str, action: str, limit: int = 3) -> list[dict]:
        """
        查找过去相似情景的处理方式
        后续接入向量检索或 LLM 语义搜索
        目前读自我叙事的每日复盘文件
        """
        results = []
        try:
            narrative_path = os.path.expanduser("~/.openclaw/workspace/neuro_claw/self_narrative/daily_reviews/")
            if os.path.exists(narrative_path):
                for fname in os.listdir(narrative_path):
                    if not fname.endswith(".json"):
                        continue
                    with open(os.path.join(narrative_path, fname), encoding="utf-8") as f:
                        data = json.load(f)
                        # 简单关键词匹配
                        for event in data.get("events", []):
                            content = event.get("event", "")
                            if any(kw in situation.lower() or kw in content.lower()
                                   for kw in situation.split()[:3]):
                                results.append({
                                    "event": content,
                                    "action": event.get("action_taken", ""),
                                    "outcome": event.get("outcome", ""),
                                    "satisfaction": 0.6 if event.get("quality") in ["excellent", "good"] else 0.3
                                })
                                if len(results) >= limit:
                                    return results
        except Exception:
            pass
        return results

    def _build_reasoning(self, result: RehearsalResult) -> str:
        """构建推理过程说明"""
        if not result.best_action:
            return "无法生成推理过程"
        
        best = result.best_action
        lines = [f"情景：{result.situation}"]
        lines.append(f"最优选择：{best.action}")
        lines.append(f"理由：{best.reasoning}")
        if best.past_similar:
            lines.append(f"参考历史：过去类似情景中，这种做法效果良好")
        lines.append(f"信心度：{'高' if abs(best.total_score()) > 0.5 else '中'}")
        if result.is_fallback:
            lines.append("⚠️ 注：无精确匹配模板，使用通用推理")
        return "\n".join(lines)

    def get_simulation_note(self, result: RehearsalResult) -> str:
        """
        生成情景预演备注，供前额叶决策时调用
        格式：自然语言，方便 Agent 直接引用
        """
        if not result.best_action:
            return "没有足够的情景预演数据支持决策"
        
        best = result.best_action
        lines = [
            f"🧠 情景预演结果：",
            f"  → 推荐行动：{best.action}",
            f"  → 推理：{best.reasoning}",
        ]
        if best.past_similar:
            lines.append(f"  → 历史参考：{best.past_similar[0].get('event', '')[:30]}...")
        
        scores = {c.step: c.score() for c in best.consequences}
        top_pos = max([(k, v) for k, v in scores.items() if v > 0], default=[("无", 0)], key=lambda x: x[1])
        top_neg = max([(k, v) for k, v in scores.items() if v < 0], default=[("无", 0)], key=lambda x: x[1])
        
        lines.append(f"  → 预期最好结果：{top_pos[0]}（得分：{top_pos[1]:.2f}）")
        lines.append(f"  → 预期最坏结果：{top_neg[0]}（得分：{top_neg[1]:.2f}）")
        
        return "\n".join(lines)
