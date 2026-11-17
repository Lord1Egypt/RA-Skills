#!/usr/bin/env python3
"""
text_tokenizer.py — 全仓唯一分词真源（GA5 分词单源化 / mod-v1.1.0）

治理动机
--------
早期版本起同一套「jieba 优先 → 缺失回退纯 Python」分词逻辑存在**两份独立实现**：
  - `anchor_adapter._tokenize_subject`   —— 词级命中率口径（P1#4）
  - `infoseek_pipeline._tokenize_query`  —— 相关性门控多字词硬门槛（P0#2）
中间版本仅做「回退算法对齐」（split → findall，消除中英混合串跨边界 2-gram 噪声），
两份代码仍并存 → ROADMAP **GA5「分词单源化」保持开放**，任一侧口径调整都可能再次漂移
（审计 P1-1「同算法」声明曾被实测证伪：6 样本 3 分叉）。
历史版本演进与各轮 mod-v 见 CHANGELOG。

本模块把该算法收敛为唯一实现 `tokenize_text()`，两侧退化为薄封装委托：
  - `_tokenize_subject(s)`  → `tokenize_text(s)`
  - `_tokenize_query(q)`    → `tokenize_text(q, require_chinese=True)`

保留的唯一差异（有意设计，非漂移）
------------------------------------
`require_chinese=True` 时，纯英文/数字输入返回空集 —— 服务于 `_filter_relevant` 的
「中文多字词硬门槛」语义（纯英文 query 不应触发中文门槛）。subject 侧无门控
（服务通用词级命中率，需处理任意语言 subject）。除此之外**算法完全单源**。

设计约束
--------
- 零第三方硬依赖：jieba 可选（装了更准），缺失自动回退纯 Python；探测结果进程内缓存
  （避免每次调用 try-import —— 见 GA8 教训：import find_spec 在热路径可占 89% 耗时）。
- 无副作用、无模块级可变业务状态（仅探测/告警 flag），可安全被 anchor_adapter 与
  pipeline 双向导入（本模块不 import 任何 infoseek 内部模块 → 天然无循环依赖）。
- 版本维度：mod-v1.0.0（模块内部版本），非 skill 对外版本
  （对外唯一真源见 `mcp_tools_common.SKILL_VERSION`）。
"""

from __future__ import annotations

import logging
import os
import re
import sys
from pathlib import Path

__all__ = ['tokenize_text', 'has_chinese', 'MOD_VERSION']

MOD_VERSION = '1.1.0'

log = logging.getLogger(__name__)

# ── jieba 探测/告警统一经 core/jieba_bridge（2026-09-29 六处裸 import 收敛）──
# 原模块内 _JIEBA/_JIEBA_PROBED/_FALLBACK_WARNED 三套状态删除；bridge 进程内
# 探测一次、降级永不抛错。core 路径在导入期就绪（幂等，不膨胀 sys.path——
# 仅插入一次，且在模块加载期而非热路径，规避 GA8 的 O(n²) 教训）。
_CORE = str(Path(__file__).parent.parent / 'core')
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)
import jieba_bridge as _jb  # noqa: E402  顶层名 ↔ core.jieba_bridge 经 sys.modules 双登记合一

# ── 口径常量（单源；调整此处即全局生效） ────────────────────────────
_CHN = r'[\u4e00-\u9fff]'
# 分段正则：中文连续段 / 英文数字 ≥2 字符整词（v1.8.2 统一口径，禁用 split 防跨边界噪声）
_SEG_RE = re.compile(_CHN + r'+|[A-Za-z0-9]{2,}')
_CHN_RE = re.compile(_CHN)
_MIN_WORD_LEN = 2        # 最短词长（杜绝单字噪音，如「新（汉语汉字）」）
_CHN_WHOLE_SEG_MAX = 4   # 中文连续段 ≤ 此长度整段成词，否则切 2-gram

# ── 进程内探测/告警状态已收口至 jieba_bridge（2026-09-29）────────────
# 探测/初始化/一次性告警全部委托 bridge；本模块仅保留纯 Python 回退算法。


def has_chinese(text: str) -> bool:
    """是否含中文字符（require_chinese 门控判据）。"""
    return bool(text) and bool(_CHN_RE.search(text))


def _probe_jieba():
    """委托 bridge 探测 jieba（保留名字以向后兼容既有调用点/测试）。"""
    return _jb.get_jieba()


def _warn_fallback_once() -> None:
    """委托 bridge：jieba 缺失一次性告警。"""
    _jb.warn_jieba_once()


def _fallback_tokens(text: str) -> set:
    """纯 Python 回退分词（jieba 缺失/异常时）。

    中文连续段：≤4 字整段成词；>4 字滑窗 2-gram。
    英文/数字：≥2 字符整词（不跨中英边界切分）。
    """
    words = set()
    for seg in _SEG_RE.findall(text):
        if _CHN_RE.search(seg):
            if len(seg) <= _CHN_WHOLE_SEG_MAX:
                words.add(seg.lower())
            else:
                for i in range(len(seg) - 1):
                    words.add(seg[i:i + 2].lower())
        else:
            words.add(seg.lower())
    return {w for w in words if len(w) >= _MIN_WORD_LEN}


def tokenize_text(text: str, require_chinese: bool = False,
                  warn_on_fallback: bool = False) -> set:
    """唯一分词入口：提取 ≥2 字符的主体词集合（小写归一）。

    Args:
        text: 待分词文本（query / subject / 任意文本）。
        require_chinese: True 时纯英文/数字输入直接返回空集（中文硬门槛语义）。
        warn_on_fallback: True 时 jieba 缺失发一次性告警（相关性门控侧启用）。

    Returns:
        set[str] —— 词集合；空输入 / 门控不通过 → set()。
    """
    if not text:
        return set()
    if require_chinese and not has_chinese(text):
        return set()

    words = _jb.lcut(text)
    if words is not None:
        return {w.strip().lower() for w in words
                if len(w.strip()) >= _MIN_WORD_LEN}

    if warn_on_fallback:
        _warn_fallback_once()
    return _fallback_tokens(text)
