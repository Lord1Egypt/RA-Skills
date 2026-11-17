#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Jobs-System · 社区演示版 · 格栅解算
# ---------------------------------------------------------------------------
# 按分档锚与准入激活词的命中关系，解算出证据充分性的原始信号，供产品壳
# 的结构校验消费。分档锚决定判定的宽松程度。
# ---------------------------------------------------------------------------
from typing import Dict

from quality_matrix import _UNCERTAIN_PROBES


def _dispatch_lattice(anchor: str, corpus: str) -> Dict[str, object]:
    """把分档锚与准入激活词解算为结构门原始信号。

    anchor ∈ {"双向门", "部分", "单向门"}。
    返回 {"pass": bool, "reason": str, "_raw": bool}。
    """
    hit = any(p in corpus for p in _UNCERTAIN_PROBES)
    if anchor in ("部分", "单向门"):
        passed = hit
        reason = ("已含不确定性标注" if passed
                  else "部分/单向门须带不确定性区间或残留风险标注")
    else:
        passed = hit
        reason = ("双向门软要求：建议含不确定性标注" if not passed
                  else "已含不确定性标注")
    return {"pass": passed, "reason": reason, "_raw": hit}
