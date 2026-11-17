#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆多路检索（M2）——语义 + 时间 + 重要性 + 关系路径 → Top-3

语义部分用字符二元组重叠度（对中文友好、零依赖），
不做向量化是为了守住"只依赖标准库"的分发约束。
若后续确认可引入轻量向量库，可替换 _semantic_score 而不动其余逻辑。
"""

import math
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

# 允许 `python scripts/memory/retrieve.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.pipeline.injector import estimate_tokens  # noqa: E402

_CJK = re.compile(r"[\u4e00-\u9fff]")
_PUNCT = re.compile(r"[，。！？、；：,.!?;:\s]+")

# 关系类记忆（共享事件 / 里程碑）额外加权 —— 这是"我们的故事"的核心
# v2.1 修正：此前是无条件 ×1.35，导致 importance=1.0 的故事类条目
# 无论问什么都霸占 Top-3，新写入的事实/偏好永远进不了上下文。
# 现在改为 **查询感知**：只有当该条目与当前话题确实有语义重叠时，
# 加权才按重叠度生效——无关的故事条目回归普通打分，不再"躺赢"。
RELATIONAL_TYPES = ("共享事件", "里程碑")
RELATIONAL_BOOST = 1.35
RELATIONAL_MIN_SEMANTIC = 0.05   # 语义重叠低于此值时不享受加权


def _tokens(text: str) -> List[str]:
    """中文按字、英文按词切分"""
    text = (text or "").lower()
    words = [w for w in _PUNCT.split(text) if w]
    out: List[str] = []
    for w in words:
        if _CJK.search(w):
            out.extend(list(w))               # 中文逐字
            out.extend(w[i:i + 2] for i in range(len(w) - 1))  # 二元组
        else:
            out.append(w)
    return out


def _semantic_score(query: str, content: str) -> float:
    """字符级重叠度 0–1"""
    q, c = set(_tokens(query)), set(_tokens(content))
    if not q or not c:
        return 0.0
    overlap = len(q & c)
    return overlap / math.sqrt(len(q) * len(c))


def _recency_score(entry: Dict[str, Any], now: datetime) -> float:
    """时间衰减：越近期权重越高，30 天半衰"""
    stamp = entry.get("last_recalled_at") or entry.get("updated_at") or entry.get("created_at")
    try:
        last = datetime.fromisoformat(str(stamp))
    except (TypeError, ValueError):
        return 0.3
    days = max(0.0, (now - last).total_seconds() / 86400.0)
    return 0.5 ** (days / 30.0)


def score_entry(entry: Dict[str, Any], query: str, now: Optional[datetime] = None) -> float:
    """综合打分：语义 0.5 + 重要性 0.25 + 时间 0.15 + 关系路径 0.10

    关系类（里程碑/共享事件）的额外加权是查询感知的：
    语义完全不相关时不加权，避免高重要度的旧故事霸榜。
    """
    now = now or datetime.now()
    semantic = _semantic_score(query, str(entry.get("content", "")))
    importance = float(entry.get("importance", 0.5))
    recency = _recency_score(entry, now)
    relational = 1.0 if entry.get("type") in RELATIONAL_TYPES else 0.4
    if semantic < RELATIONAL_MIN_SEMANTIC:
        # 与当前话题弱相关/零重叠的记忆：重要度打四折、关系加成归零。
        # 否则 importance=1.0 的旧故事无论聊什么都霸榜（v2.0 实测问题）；
        # 只挡 semantic==0 挡不住单字偶合（如「在」「点」），统一用 0.05 门槛。
        importance *= 0.4
        relational = min(relational, 0.2)
    score = semantic * 0.5 + importance * 0.25 + recency * 0.15 + relational * 0.10
    if entry.get("type") in RELATIONAL_TYPES and semantic >= RELATIONAL_MIN_SEMANTIC:
        # 加权幅度随语义相关度线性放大：完全相关拿满 1.35，刚过门槛约 1.0
        scale = min(1.0, (semantic - RELATIONAL_MIN_SEMANTIC) / (0.5 - RELATIONAL_MIN_SEMANTIC))
        score *= 1.0 + (RELATIONAL_BOOST - 1.0) * scale
    return score


def top_k(entries: Iterable[Dict[str, Any]], query: str, k: int = 3,
          token_budget: int = 150, now: Optional[datetime] = None,
          max_per_type: int = 2) -> List[Dict[str, Any]]:
    """按综合分取 Top-K，并受 Token 预算约束

    Args:
        entries: 候选记忆
        query: 当前用户输入（或当前话题摘要）
        k: 最多取几条（方案要求 Top-3）
        token_budget: 注入预算（方案要求 <150）
        max_per_type: 单一类型在结果里的上限（默认 2）。
            多样性约束：即使故事类分数再高，也给事实/偏好/情绪留至少一个席位。

    Returns:
        命中的记忆条目列表（含 _score 字段，便于调试与可解释面板）
    """
    now = now or datetime.now()
    scored = []
    for e in entries:
        s = score_entry(e, query, now)
        item = dict(e)
        item["_score"] = round(s, 4)
        scored.append(item)
    scored.sort(key=lambda x: x["_score"], reverse=True)

    picked: List[Dict[str, Any]] = []
    type_count: Dict[str, int] = {}
    used = 0
    for item in scored:
        if len(picked) >= k:
            break
        mtype = str(item.get("type", "?"))
        if max_per_type > 0 and type_count.get(mtype, 0) >= max_per_type:
            continue
        cost = estimate_tokens(str(item.get("content", "")))
        if used + cost > token_budget:
            continue
        picked.append(item)
        type_count[mtype] = type_count.get(mtype, 0) + 1
        used += cost
    return picked


def render(memories: List[Dict[str, Any]]) -> str:
    """渲染成可注入的简短文本（每条都带 id，便于追溯）"""
    return "；".join(f"#{m.get('id')} {m.get('content')}" for m in memories)


if __name__ == "__main__":
    import sys
    from scripts.memory.store import MemoryStore

    q = sys.argv[1] if len(sys.argv) > 1 else "今天很累"
    store = MemoryStore()
    hits = top_k(store.all(), q)
    print(render(hits) or "(无匹配记忆)")
    for h in hits:
        print(f"  #{h['id']} [{h['type']}] score={h['_score']} {h['content']}")
