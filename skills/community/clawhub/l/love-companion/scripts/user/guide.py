#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依恋类型识别 + 相处指南编译（M3b）

依恋识别用**规则引擎**（零依赖、可解释、可人工修正），后续若确认可引入本地小模型再替换。
相处指南编译产物必须 < 200 Token（方案 Token 预算表硬约束）。
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

# 允许 `python scripts/user/guide.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.pipeline.injector import estimate_tokens, truncate_to_tokens  # noqa: E402

# 依恋类型判定规则：(类型, 命中关键词/信号权重)
ANXIETY_WORDS = ("在吗", "怎么不回", "是不是", "你还在吗", "不要不理", "为什么不", "你不在乎", "怕你")
AVOIDANT_WORDS = ("别管", "让我静静", "没事", "不用管我", "随便", "我想一个人", "别问")
SECURE_WORDS = ("谢谢", "我们一起", "慢慢来", "没关系", "我理解", "辛苦了")


def infer_attachment(signals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """基于行为信号推断依恋类型

    信号里不含原文，只有情绪/话题/长度等特征，因此这里主要靠：
    - 焦虑型：情绪波动频繁 + 消息偏短促 + 提问率高（反复确认）
    - 回避型：消息极短 + 情绪表达少 + 话题单一
    - 安全型：情绪稳定 + 长度适中 + 有正向表达

    Returns:
        {"判断": str, "候选": [...], "置信度": float}
    """
    if not signals:
        return {"判断": "未知", "候选": ["安全型", "焦虑型", "回避型", "恐惧型"], "置信度": 0.0}

    n = len(signals)
    emotion_rate = sum(1 for s in signals if s.get("emotion")) / n
    question_rate = sum(1 for s in signals if s.get("question")) / n
    avg_len = sum(s.get("length", 0) for s in signals) / n
    negative = sum(1 for s in signals if s.get("emotion") in ("低落", "焦虑", "生气", "疲惫")) / n

    scores = {
        "焦虑型": emotion_rate * 0.4 + question_rate * 0.3 + negative * 0.3,
        "回避型": (1 - min(1.0, avg_len / 20)) * 0.5 + (1 - emotion_rate) * 0.3 + 0.2 * (1 - question_rate),
        "安全型": (1 - negative) * 0.5 + min(1.0, avg_len / 25) * 0.3 + 0.2,
    }
    best = max(scores, key=scores.get)
    ranked = sorted(scores, key=scores.get, reverse=True)
    spread = scores[ranked[0]] - scores[ranked[1]]
    confidence = round(min(1.0, max(0.2, spread * 2 + min(1.0, n / 50) * 0.3)), 2)

    return {"判断": best, "候选": ranked, "置信度": confidence}


def compile_guide(persona: Dict[str, Any], budget: int = 200) -> str:
    """把用户画像编译成可注入的相处指南（<200 Token）

    只输出**策略性短句**，不输出原始画像数据——既省 Token 又保护隐私。
    """
    parts: List[str] = []

    att = (persona.get("依恋类型") or {}).get("判断", "未知")
    ATTACHMENT_STRATEGY = {
        "焦虑型": "多给确定性与回应，避免长时间沉默，主动说明在做什么",
        "回避型": "给足空间，少追问，用行动表达关心而非密集言语",
        "安全型": "自然陪伴，平等交流，可适度深入话题",
        "恐惧型": "温和稳定，节奏放慢，避免忽冷忽热",
        "未知": "保持中性温和，观察用户反应再调整",
    }
    parts.append(f"依恋：{att}（{ATTACHMENT_STRATEGY.get(att, ATTACHMENT_STRATEGY['未知'])}）")

    style = persona.get("沟通风格") or {}
    length_pref = (persona.get("互动偏好") or {}).get("回复长度偏好") or style.get("句式长度")
    if length_pref:
        parts.append(f"回复长度：{'短句为主' if length_pref in ('短', '短句') else length_pref}")

    emotions = (persona.get("情绪模式") or {}).get("常见情绪") or []
    if emotions:
        parts.append(f"近期情绪：{'/'.join(emotions[:3])}")

    topics = (persona.get("互动偏好") or {}).get("喜欢的话题") or []
    if topics:
        parts.append(f"常聊话题：{'/'.join(topics[:3])}")

    active = (persona.get("互动偏好") or {}).get("主动程度偏好")
    if active:
        parts.append(f"主动性：{active}")

    guide = " · ".join(parts)
    if estimate_tokens(guide) > budget:
        guide = truncate_to_tokens(guide, budget)
    return guide


if __name__ == "__main__":
    import json
    from scripts.user.profile import UserProfileStore

    store = UserProfileStore()
    persona = store.get()
    print(compile_guide(persona))
    print(json.dumps(persona.get("依恋类型", {}), ensure_ascii=False))
