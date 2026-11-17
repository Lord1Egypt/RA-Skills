#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆无感采集（M2）——从对话文本中提取六类记忆（离线执行）

真实性零容忍（红线 3）：
- **只记录用户自己说出口的事实**，不做任何推断、补全或想象
- 每条记忆都保留 source（原句），注入上下文时可追溯
- 拿不准的一律不记宁缺毋滥

隐私优先（红线 4）：
- 采集前先过 core/privacy.py 脱敏
- 含敏感信息直接放弃该句
"""

import re
import sys
from pathlib import Path
from typing import Any, Dict, List

# 允许 `python scripts/memory/extract.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core.privacy import filter_text, has_sensitive  # noqa: E402

# 六类记忆的触发规则：(类型, 正则, 基础重要度, 情感效价)
# 说明：规则刻意保守，宁可漏记也不误记
PATTERNS: List[tuple] = [
    # 事实：身份、客观信息
    ("事实", re.compile(r"(?:我叫|我的名字是|我是)([^，。！？,.!?]{1,12})"), 0.7, 0.0),
    ("事实", re.compile(r"(?:我住在|我在)([^，。！？,.!?]{1,15})(?:住|工作|上学|生活)?"), 0.6, 0.0),
    ("事实", re.compile(r"我的生日是?\s*([^，。！？,.!?]{1,15})"), 0.8, 0.0),
    ("事实", re.compile(r"我是(?:一个)?([^，。！？,.!?]{1,10})(?:师|生|员|工|设计师|程序员|老师|学生)"), 0.7, 0.0),
    # 偏好
    ("偏好", re.compile(r"我(?:很|最|特别)?(?:喜欢|爱|中意)([^，。！？,.!?]{1,18})"), 0.7, 0.6),
    ("偏好", re.compile(r"我(?:不|不太|最不)(?:喜欢|爱|想|习惯)([^，。！？,.!?]{1,18})"), 0.7, -0.5),
    ("偏好", re.compile(r"我(?:讨厌|受不了|烦)([^，。！？,.!?]{1,18})"), 0.75, -0.7),
    # 里程碑 / 共享事件
    ("里程碑", re.compile(r"(?:纪念日|周年|第一次|我们在一起|交往)([^，。！？,.!?]{0,18})"), 0.85, 0.7),
    ("共享事件", re.compile(r"(?:我们|咱俩|你和我)(?:一起|上次|去过|看过|吃过)([^，。！？,.!?]{1,20})"), 0.7, 0.5),
    # 情绪
    ("情绪", re.compile(r"(?:今天|最近|现在)?(?:好累|很累|累死了|压力大|焦虑|emo|崩溃)"), 0.6, -0.6),
    ("情绪", re.compile(r"(?:今天|最近)?(?:好开心|好高兴|太棒了|很爽|好幸福)"), 0.6, 0.7),
    ("情绪", re.compile(r"(?:难过|伤心|委屈|失落|想哭|心情不好)"), 0.65, -0.7),
    # 人设特征：用户对 Agent 的评价/要求
    ("人设特征", re.compile(r"你(?:总是|很|太|最|特别)([^，。！？,.!?]{1,15})"), 0.6, 0.0),
    ("人设特征", re.compile(r"(?:别|不要|不许)(?:发|说|这么|那么)([^，。！？,.!?]{1,15})"), 0.7, -0.2),
]

# 太短或太泛的内容不记
MIN_CONTENT_LEN = 2
STOPWORDS = ("什么", "怎么", "为什么", "吗")

# v2.1 新增：口语过渡语误捕黑名单——
# 「我是说今天不去」不是自我介绍，「我在想晚饭吃啥」不是住址，
# 命中这些开头的一律不采（真实性零容忍：宁可漏记不可误记）
FALSE_POSITIVE_PREFIXES = (
    "我是说", "我是想", "我是觉得", "我是不是",
    "我在想", "我在做", "我在看", "我在写",
    "我叫它", "我叫他", "我叫她",
)


def _clean(text: str) -> str:
    return (text or "").strip(" ，,。.、；;！!？?~ ").strip()


def extract_memories(text: str, conversation_id: str = "") -> List[Dict[str, Any]]:
    """从一段文本中提取候选记忆

    Args:
        text: 原始对话文本（会先做隐私脱敏）
        conversation_id: 会话标识，便于后续"遗忘某段关系"

    Returns:
        候选记忆列表，每项含 content / type / source / importance / valence
    """
    if not text or not text.strip():
        return []

    safe_text, hits = filter_text(text)
    if hits:
        # 含敏感信息的句子整句放弃，不做部分采集
        return []

    results: List[Dict[str, Any]] = []
    seen = set()

    for mtype, pattern, importance, valence in PATTERNS:
        for match in pattern.finditer(safe_text):
            content = _clean(match.group(0))
            if len(content) < MIN_CONTENT_LEN or content in seen:
                continue
            if any(sw in content for sw in STOPWORDS):
                continue
            if any(content.startswith(p) for p in FALSE_POSITIVE_PREFIXES):
                continue
            if has_sensitive(content):
                continue
            seen.add(content)
            results.append({
                "content": content,
                "type": mtype,
                "source": safe_text[:200],
                "importance": importance,
                "valence": valence,
            })

    return results


if __name__ == "__main__":
    import json
    import sys

    demo = sys.argv[1] if len(sys.argv) > 1 else (
        "我叫小明，我的生日是5月20日，我喜欢三分糖奶茶，我讨厌被敷衍，"
        "今天我们一起去看了电影，最近压力大"
    )
    print(json.dumps(extract_memories(demo), ensure_ascii=False, indent=2))
