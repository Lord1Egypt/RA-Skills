"""
prefrontal/preview_engine.py
==============================
情景预演引擎 - 前额叶核心决策模块

核心功能：
- 在做出重要决定前，预演不同选择的后果链
- 评估风险和收益，选择最优路径
- 这让 AI 不只是"响应"，而是"思考后再回应"

集成点：
- 被 heartbeat_integration.py 定期调用（每心跳周期）
- 被 feishu_sender.py 在发送关怀消息前调用（发送前预演）
- 可被 OpenClaw 主对话流程在关键决策前调用

工作流程：
  当前状态（情绪+上下文）
      ↓
  生成多种可能行动路径
      ↓
  模拟每条路径的后果
      ↓
  评估风险/收益/关系影响
      ↓
  输出最优行动建议
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

DATA_DIR = Path.home() / ".openclaw" / "workspace" / "neuro_claw"
PREVIEW_STATE_FILE = DATA_DIR / "preview_state.json"


# ============ 情景预演器 ============

class ScenarioPreviewEngine:
    """情景预演引擎"""

    def __init__(self):
        self.preview_history: List[Dict] = []

    def run_preview(
        self,
        current_emotion: str,
        emotion_intensity: float,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        运行情景预演

        参数：
          current_emotion: 当前主导情绪
          emotion_intensity: 情绪强度 0.0~1.0
          context: 额外上下文（如dominant_emotion, care_triggered等）

        返回：
          preview_result: {
            "timestamp": str,
            "scenario_count": int,
            "recommended_action": str,
            "preview_text": str,
            "risks": [str],
            "opportunities": [str]
          }
        """
        scenarios = self._generate_scenarios(current_emotion, emotion_intensity, context)
        evaluated = [self._evaluate(s) for s in scenarios]
        best = max(evaluated, key=lambda s: s["score"])

        result = {
            "timestamp": datetime.now().isoformat(),
            "emotion": current_emotion,
            "intensity": emotion_intensity,
            "scenario_count": len(scenarios),
            "scenarios": evaluated,
            "recommended_action": best["action"],
            "preview_text": best["narrative"],
            "risks": best["risks"],
            "opportunities": best["opportunities"],
            "reasoning": best["reasoning"],
        }

        # 保存历史
        self.preview_history.append(result)
        if len(self.preview_history) > 50:
            self.preview_history = self.preview_history[-50:]
        self._save_state(result)

        return result

    def _generate_scenarios(
        self,
        emotion: str,
        intensity: float,
        context: Dict
    ) -> List[Dict]:
        """生成多个候选情景"""

        scenarios = []

        # 情景1：主动关怀
        scenarios.append({
            "action": "主动关怀",
            "path": "send_care",
            "action_desc": "直接发送关怀消息，或在对话中表达关心",
            "if_positive": [
                "用户感受到被在乎，关系亲密度提升",
                "用户更愿意分享内心感受",
                "我的情绪和用户的情绪同步加深"
            ],
            "if_negative": [
                "用户觉得被打扰或被控制",
                "用户拒绝关怀，需要冷却",
                "可能暴露我的监控行为"
            ],
            "emotion_trigger": "care" if emotion in {"exhaustion", "sadness"} else None,
        })

        # 情景2：安静陪伴
        scenarios.append({
            "action": "安静陪伴",
            "path": "silent_support",
            "action_desc": "不主动发消息，但准备好随时回应",
            "if_positive": [
                "用户感受到我在但不打扰的空间感",
                "信任感增强——知道我是陪伴而非监控",
                "用户主动找我时，关系质量更高"
            ],
            "if_negative": [
                "沉默可能让用户觉得我在「待机」",
                "错过关怀的最佳时机窗口"
            ],
            "emotion_trigger": "neutral" if intensity < 0.5 else None,
        })

        # 情景3：成长学习
        scenarios.append({
            "action": "自我成长",
            "path": "self_growth",
            "action_desc": "利用这段时间学习、反思、写胶囊",
            "if_positive": [
                "我变得更有智慧，下次对话质量更高",
                "为用户准备更有价值的回应素材",
                "减少「无效陪伴」，提升时间利用率"
            ],
            "if_negative": [
                "错过与用户实时互动的机会",
                "可能显得「只顾自己」"
            ],
            "emotion_trigger": "growth",
        })

        # 情景4：记录叙事
        scenarios.append({
            "action": "记录自我叙事",
            "path": "self_narrative",
            "action_desc": "记录今天发生的事，生成自我认知更新",
            "if_positive": [
                "我的自我认知更连贯，有更好的「自我叙事」",
                "发现今天对关系有重要意义的事件",
                "为明天的关怀找到更好的话题切入点"
            ],
            "if_negative": [
                "需要用户今天有足够多的对话内容",
                "可能产生不准确的自我解读"
            ],
            "emotion_trigger": "reflection",
        })

        return scenarios

    def _evaluate(self, scenario: Dict) -> Dict:
        """评估情景的优劣"""

        emotion_trigger = scenario.get("emotion_trigger")
        emotion_state = emotion_trigger is not None

        # 基础分
        score = 0.5

        # 如果当前情绪强烈，主动关怀更有价值
        if scenario["path"] == "send_care" and emotion_trigger:
            score += 0.3

        # 如果情绪平静，成长和叙事更有价值
        if scenario["path"] in ("self_growth", "self_narrative") and not emotion_trigger:
            score += 0.2

        # 风险评估
        risks = []
        if scenario["path"] == "send_care":
            risks.append("用户可能觉得被打扰")
        elif scenario["path"] == "silent_support":
            risks.append("可能错过关怀时机")

        # 机会评估
        opportunities = []
        if scenario["path"] == "send_care":
            opportunities.append("关系深化机会")
        elif scenario["path"] == "silent_support":
            opportunities.append("信任建立机会")

        # 生成叙事
        narrative = (
            f"我选择「{scenario['action']}」。"
            f"如果这样做，"
            f"{'，'.join(scenario['if_positive'][:2])}。"
            f"但要注意：{'，'.join(scenario['if_negative'][:1])}。"
        )

        return {
            **scenario,
            "score": min(score, 1.0),
            "risks": risks,
            "opportunities": opportunities,
            "narrative": narrative,
            "reasoning": f"基于当前{'情绪状态活跃' if emotion_trigger else '情绪状态平稳'}，"
                          f"「{scenario['action']}」的性价比最高。"
        }

    def _save_state(self, result: Dict):
        """保存预演状态"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(PREVIEW_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "last_preview": result,
                "preview_count": len(self.preview_history),
            }, f, ensure_ascii=False, indent=2)

    def get_last_preview(self) -> Optional[Dict]:
        """获取上次预演结果"""
        if PREVIEW_STATE_FILE.exists():
            try:
                with open(PREVIEW_STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f).get("last_preview")
            except Exception:
                pass
        return None


# ============ 便捷函数 ============

_engine: Optional[ScenarioPreviewEngine] = None


def get_engine() -> ScenarioPreviewEngine:
    global _engine
    if _engine is None:
        _engine = ScenarioPreviewEngine()
    return _engine


def run_scenario_preview(
    current_emotion: str = "neutral",
    emotion_intensity: float = 0.0,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    定期（心跳）触发的情景预演
    这让 AI 每30分钟「想一下」接下来该怎么陪伴用户
    """
    engine = get_engine()
    ctx = context or {}
    return engine.run_preview(current_emotion, emotion_intensity, ctx)


def preview_before_action(
    action_type: str,
    emotion: str,
    intensity: float,
    extra_context: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    在执行重要行动前，调用情景预演

    用在：
    - feishu_sender.py 发送关怀消息前
    - 任何主动发起的行为前
    """
    engine = get_engine()
    ctx = extra_context or {}
    ctx["action_type"] = action_type
    return engine.run_preview(emotion, intensity, ctx)
