#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""entry_guard.py — Infoseek 公共入口类型契约守卫原语（纯标准库，零依赖）

设计依据：references/g8-entry-contract-design.md（G8 专项设计 · 方案 C）

约束：
  - 仅使用 collections.abc，无任何第三方依赖；
  - 仅声明类型守卫，绝不修改被守卫入口的函数签名（守卫位于函数体首行）；
  - 失败语义统一为受控 TypeError（带非空消息），替代散落的 AttributeError；
  - 宽容模式 coerce_mapping_list 用于「噪声源」类列表入参（skip_bad=True），
    坏元素跳过 + logging.warning，保留整链存活（与既有降级哲学一致）。

布线清单（G8-apply 接线点）：
  require_text       → extract_entities / get_entities_by_type / compute_trust_bonus /
                       estimate_cost（后三者严格拒绝 None → 受控 TypeError）
  require_mapping    → score_source / identity_aggregator.aggregate
  require_sequence   → detect_conflicts
  coerce_mapping_list→ render_report / detect_conflicts_v3（元素级坏源隔离）
"""
import logging
from collections.abc import Mapping, Sequence

_log = logging.getLogger("infoseek.entry_guard")


def require_text(val, name="value"):
    """None / 非 str（int / float / bool / dict / list ...）→ 受控 TypeError。

    注：None 默认视为非法（严格契约）；若入口需保留「None 透传降级」语义，
    调用方应在入口内联 `if val is not None and not isinstance(val, str): raise` ，
    或本项目在 extract_entities / compute_trust_bonus 中已采用该 None 透传变体。
    """
    if not isinstance(val, str):
        raise TypeError(f"{name} 需为文本(str)，收到 {type(val).__name__}: {val!r}")
    return val


def require_mapping(val, name="value"):
    """非 Mapping（None / str / list / int ...）→ 受控 TypeError。"""
    if not isinstance(val, Mapping):
        raise TypeError(f"{name} 需为映射(Mapping/dict)，收到 {type(val).__name__}: {val!r}")
    return val


def require_sequence(val, name="value"):
    """非 Sequence 或 str → 受控 TypeError（str 视为非法序列，避免误当字符列表）。"""
    if isinstance(val, str) or not isinstance(val, Sequence):
        raise TypeError(f"{name} 需为序列(list/tuple)，收到 {type(val).__name__}: {val!r}")
    return val


def coerce_mapping_list(seq, name="sources", skip_bad=True):
    """元素级隔离：保留 Mapping 元素，跳过（warn）非 Mapping 元素，返回 list[Mapping]。

    设计目的：sources 列表内含坏元素（如 [None]）时，不再中断整条链路（G8 #8 / #10）。
      - None / 空      → []
      - str / 非序列   → 视为结构性非法，raise TypeError（除非 skip_bad 仅跳过顶层）
      - 序列内非 Mapping 元素 → skip_bad=True 时跳过 + warning；False 时 raise
    """
    if seq is None:
        return []
    if isinstance(seq, str):
        raise TypeError(f"{name} 需为映射列表，收到 str: {seq!r}")
    if not isinstance(seq, Sequence):
        raise TypeError(f"{name} 需为序列(list/tuple)，收到 {type(seq).__name__}: {seq!r}")
    out = []
    for i, item in enumerate(seq):
        if isinstance(item, Mapping):
            out.append(item)
        elif skip_bad:
            _log.warning("%s[%d] 非映射已跳过: %r", name, i, item)
        else:
            raise TypeError(f"{name}[{i}] 需为映射，收到 {type(item).__name__}: {item!r}")
    return out
