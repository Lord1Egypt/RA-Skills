#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恋人式用户理解（M3b）——流式采集 + 两级分析 + 画像持久化

隐私优先（红线 4）：
- 原始输入**不落盘**。只保存脱敏后的结构化信号（情绪/话题/句式/长度），
  以及用于两级分析的计数。方案说"经隐私过滤后进入特征提取队列"，
  这里做得更保守：连脱敏原文都不留，只留特征。

两级分析：
- 轻量：每 5 条消息更新一次（情绪 / 话题 / 句式）
- 深度：每 50 条更新一次画像（沟通风格 / 大五 / 依恋类型 / 情绪模式 / 互动偏好）
"""

import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 允许 `python scripts/user/profile.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core import privacy, schema  # noqa: E402
from scripts.core import settings as core_settings  # noqa: E402
from scripts.core.storage import read_json, write_json  # noqa: E402

LIGHT_INTERVAL = 5
DEEP_INTERVAL = 50

TOPIC_KEYWORDS = {
    "工作": ("加班", "上班", "项目", "同事", "老板", "汇报", "需求", "上线"),
    "学习": ("考试", "考研", "作业", "论文", "上课", "复习", "成绩"),
    "生活": ("吃饭", "睡", "回家", "房租", "做饭", "猫", "狗", "天气"),
    "情绪倾诉": ("累", "烦", "难过", "开心", "焦虑", "压力", "委屈"),
    "关系": ("我们", "在一起", "想你", "喜欢你", "纪念日", "吵架"),
}

EMOTION_WORDS = {
    "疲惫": ("累", "困", "没劲", "撑不住", "压力大"),
    "低落": ("难过", "伤心", "委屈", "失落", "想哭", "emo"),
    "焦虑": ("焦虑", "紧张", "慌", "担心", "怕"),
    "开心": ("开心", "高兴", "哈哈", "太棒", "不错", "爽"),
    "生气": ("气死", "烦死", "生气", "无语", "受不了"),
}


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def signal_from_message(text: str) -> Dict[str, Any]:
    """从一条消息提取轻量信号（不含原文）"""
    safe, _hits = privacy.filter_text(text or "")
    lowered = safe.lower()

    emotion = None
    for name, words in EMOTION_WORDS.items():
        if any(w in safe for w in words):
            emotion = name
            break

    topics = [t for t, kws in TOPIC_KEYWORDS.items() if any(k in safe for k in kws)]

    sentences = [s for s in re.split(r"[。！？!?.；;\n]", safe) if s.strip()]
    avg_len = round(sum(len(s) for s in sentences) / len(sentences), 1) if sentences else 0.0

    return {
        "ts": _now(),
        "length": len(safe),
        "avg_sentence_len": avg_len,
        "emotion": emotion,
        "topics": topics,
        "emoji": len(re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", safe)),
        "question": ("？" in safe) or ("?" in safe),
        "exclaim": safe.count("！") + safe.count("!"),
    }


class UserProfileStore:
    """用户画像存储与两级分析"""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = core_settings.resolve_data_dir(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.persona_file = self.data_dir / "user_persona.json"
        self.stream_file = self.data_dir / "user_signals.json"

    # ---------- 存储 ----------

    def _load_persona(self) -> Dict[str, Any]:
        data = read_json(self.persona_file, None)
        return data if isinstance(data, dict) else schema.user_persona_template()

    def _save_persona(self, persona: Dict[str, Any]) -> None:
        persona["updated_at"] = _now()
        write_json(self.persona_file, persona)

    def _load_signals(self) -> List[Dict[str, Any]]:
        data = read_json(self.stream_file, [])
        return data if isinstance(data, list) else []

    def _save_signals(self, signals: List[Dict[str, Any]], keep: int = 500) -> None:
        write_json(self.stream_file, signals[-keep:])

    # ---------- 采集 ----------

    def ingest(self, text: str) -> Dict[str, Any]:
        """流式采集一条消息，返回本次是否触发了深度更新"""
        signal = signal_from_message(text)
        signals = self._load_signals()
        signals.append(signal)
        self._save_signals(signals)
        self._meta_count = len(signals)

        report = {"signals": len(signals), "light": False, "deep": False}
        if len(signals) % LIGHT_INTERVAL == 0:
            self._light_update(signals)
            report["light"] = True
        if len(signals) % DEEP_INTERVAL == 0:
            self._deep_update(signals)
            report["deep"] = True
        return report

    # ---------- 分析 ----------

    def _light_update(self, signals: List[Dict[str, Any]]) -> None:
        recent = signals[-50:]
        persona = self._load_persona()

        emotions = Counter(s["emotion"] for s in recent if s.get("emotion"))
        topics = Counter(t for s in recent for t in (s.get("topics") or []))
        avg_len = sum(s["avg_sentence_len"] for s in recent) / len(recent)

        persona["情绪模式"]["常见情绪"] = [e for e, _ in emotions.most_common(3)]
        persona["情绪模式"]["置信度"] = round(
            min(1.0, sum(emotions.values()) / max(1, len(recent)) * 1.5), 2
        )
        persona["互动偏好"]["喜欢的话题"] = [t for t, _ in topics.most_common(3)]
        persona["沟通风格"]["句式长度"] = "短句" if avg_len <= 12 else ("中等" if avg_len <= 25 else "长句")
        self._save_persona(persona)

    def _deep_update(self, signals: List[Dict[str, Any]]) -> None:
        recent = signals[-200:]
        persona = self._load_persona()

        # 大五人格：基于行为信号的粗粒度推断（只做相对倾向，不做绝对断言）
        emotion_rate = sum(1 for s in recent if s.get("emotion")) / max(1, len(recent))
        question_rate = sum(1 for s in recent if s.get("question")) / max(1, len(recent))
        avg_len = sum(s["length"] for s in recent) / max(1, len(recent))
        emoji_rate = sum(s["emoji"] for s in recent) / max(1, len(recent))

        persona["大五人格"].update({
            "外向性": round(min(1.0, 0.4 + emoji_rate * 0.3 + (0.2 if avg_len > 20 else 0)), 2),
            "神经质": round(min(1.0, 0.3 + emotion_rate * 0.5), 2),
            "开放性": round(min(1.0, 0.4 + question_rate * 0.4), 2),
            "宜人性": round(min(1.0, 0.5 + (0.2 if emotion_rate < 0.3 else 0)), 2),
            "尽责性": round(min(1.0, 0.5 + (0.2 if avg_len > 15 else 0)), 2),
            "置信度": round(min(1.0, len(recent) / 200), 2),
        })

        # 依恋类型（规则引擎，详见 user/guide.py）
        from scripts.user.guide import infer_attachment
        att = infer_attachment(recent)
        persona["依恋类型"] = att

        self._save_persona(persona)

    # ---------- 反馈闭环 ----------

    def apply_feedback(self, feedback: str) -> Dict[str, Any]:
        """用户纠正即时生效，如「别发这么长」「别用 emoji」"""
        persona = self._load_persona()
        applied = []
        if "长" in feedback:
            persona["互动偏好"]["回复长度偏好"] = "短"
            applied.append("回复长度偏好=短")
        if "emoji" in feedback.lower() or "表情" in feedback:
            persona["沟通风格"]["emoji频率"] = 0.0
            applied.append("emoji 频率归零")
        if "主动" in feedback:
            persona["互动偏好"]["主动程度偏好"] = "高" if "多" in feedback or "更" in feedback else "低"
            applied.append(f"主动程度偏好={persona['互动偏好']['主动程度偏好']}")
        if applied:
            self._save_persona(persona)
        return {"applied": applied}

    def get(self) -> Dict[str, Any]:
        return self._load_persona()

    def clear(self) -> None:
        for f in (self.persona_file, self.stream_file):
            if f.exists():
                f.unlink()


if __name__ == "__main__":
    import sys
    store = UserProfileStore()
    if len(sys.argv) > 1 and sys.argv[1] == "show":
        print(json.dumps(store.get(), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(store.ingest("今天加班好累，压力好大，想你了"), ensure_ascii=False))
