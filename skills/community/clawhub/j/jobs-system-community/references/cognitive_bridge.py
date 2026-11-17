#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Jobs-System · 社区演示版 · 共振桥接
# ---------------------------------------------------------------------------
# 把文本经语义维度投影后的结果桥接到产品壳的认知管线：一侧产出维度命中
# 状态，一侧产出聚合后的信号向量，供结构校验在运行时消费。
# ---------------------------------------------------------------------------
from typing import Dict

from quality_matrix import resonate, aggregate_signal_vector as _agg


def _resolve_cognitive_resonance(corpus: str) -> Dict[str, bool]:
    """把文本投影到语义维度空间，返回各维度的激活状态表。"""
    return resonate(corpus)


def _bridge_signal(corpus: str) -> Dict[str, float]:
    """在维度命中状态上做一次加权聚合，返回信号向量。"""
    return _agg(corpus)
