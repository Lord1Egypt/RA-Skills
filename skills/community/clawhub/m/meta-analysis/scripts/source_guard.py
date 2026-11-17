"""source_guard.py — ct- 库共享反幻觉护栏（零依赖，Python 3.8+）。

整合自两个已落地技能的范式：
  - `ct-landscape.scripts.landscape.assert_no_fabrication`：输出实体必须是
    输入已知实体的子集，否则抛 AssertionError（硬拦截静默编造）。
  - `ct-congress.scripts.extract` 的 source_quote 范式：每个吐出的数值 /
    结论必须带逐字 source_quote；缺溯源一律标 `⚠️ 待核实`（落实 ct-base §17.1
    溯源红线）。

对外检索类技能（registry / pipeline / advisor / literature / safety /
congress / landscape）统一调用本模块，不各自重造反幻觉逻辑。

设计原则（与 §17.4 Thin/Thick 一致）：
  - 本模块只做"校验 / 标记"，不调用 LLM、不发网络请求；
  - 纯函数、确定性、可单测；
  - 被编造即硬失败（assert_no_fabrication），缺溯源即标记（require_source）。
"""

from __future__ import annotations

import re
from typing import Dict, Iterable, List, Optional, Sequence, Set

# 缺溯源时的统一标记，渲染层据此显示 ⚠️。
UNVERIFIED_MARKER = "⚠️ 待核实"


# ---------------------------------------------------------------------------
# 1. 硬护栏：禁止编造（整合 ct-landscape.assert_no_fabrication）
# ---------------------------------------------------------------------------
def assert_no_fabrication(
    records: Sequence[Dict],
    known_entities: Iterable[str],
    key: str = "drug",
    entity_label: str = "entity",
    ignore: Optional[Set[str]] = None,
) -> None:
    """输出记录里的 `key` 字段取值必须是 `known_entities` 的白名单子集。

    参数
    ----
    records : 输出记录列表（list[dict]）。
    known_entities : 输入已知实体白名单（如检索命中的药物 / 靶点名）。
    key : 要核查的字段名（默认 "drug"；可传 "target" 等）。
    entity_label : 报错里的实体类别词（用于可读提示）。
    ignore : 视为"未知但合法"的取值集合（如 landscape 的 "unknown"）。

    若输出出现白名单外（且不在 ignore 内）的实体，抛 AssertionError 并列出
    被编造的实体——这是反幻觉的最后一道硬闸，绝不静默放过。
    """
    known: Set[str] = {str(e).strip() for e in (known_entities or [])}
    ignore_set: Set[str] = {str(i).strip() for i in (ignore or set())}
    out = {str(r.get(key, "")).strip() for r in records if r.get(key)}
    unknown = {e for e in out if e not in known and e not in ignore_set}
    assert not unknown, f"fabricated {entity_label}(s): {sorted(unknown)}"


# ---------------------------------------------------------------------------
# 2. 逐字溯源片段截取（整合 ct-congress.source_quote 范式）
# ---------------------------------------------------------------------------
def source_quote_for(
    text: str,
    match_start: int,
    window_before: int = 90,
    window_after: int = 180,
) -> str:
    """从原文 `text` 截取 `match_start` 周围的逐字片段，作为某结论的溯源引用。

    返回单空格归一化的片段；`text` 为空时返回空串。
    """
    if not text:
        return ""
    start = max(0, match_start - window_before)
    end = min(len(text), match_start + window_after)
    return re.sub(r"\s+", " ", text[start:end]).strip()


# ---------------------------------------------------------------------------
# 3. 缺溯源即标记（落实 §17.1 红线：状态断言须带溯源否则 ⚠️ 待核实）
# ---------------------------------------------------------------------------
def require_source(
    rows: Sequence[Dict],
    quote_key: str = "source_quote",
    status_key: str = "status",
) -> tuple[List[Dict], int]:
    """给缺溯源的 row 打 `⚠️ 待核实` 标记（不抛错，只标记）。

    返回 (clean_rows, unverified_count)。
    缺 `quote_key` 或值为空的 row，其 `status_key` 置为 "unverified"，
    并附 `needs_verification=True`；有溯源的 row 附 `needs_verification=False`。
    原始 row 不被原地修改（返回副本）。
    """
    clean: List[Dict] = []
    n_unverified = 0
    for r in rows:
        r = dict(r)
        quote = (r.get(quote_key) or "").strip()
        if not quote:
            r[status_key] = "unverified"
            r["needs_verification"] = True
            n_unverified += 1
        else:
            r["needs_verification"] = False
        clean.append(r)
    return clean, n_unverified


def verify_rate(clean_rows: Sequence[Dict]) -> tuple[float, int]:
    """返回 (验证率, 待核实数)。验证率 = 1 - 待核实/总数。"""
    n = len(clean_rows)
    if n == 0:
        return 1.0, 0
    unverified = sum(1 for r in clean_rows if r.get("needs_verification"))
    return (n - unverified) / n, unverified


# ---------------------------------------------------------------------------
# 4. 一键组合护栏（供对外检索类技能在 emit 前调用）
# ---------------------------------------------------------------------------
def guard_records(
    records: Sequence[Dict],
    known_entities: Iterable[str],
    key: str = "drug",
    entity_label: str = "entity",
    ignore: Optional[Set[str]] = None,
    quote_key: str = "source_quote",
) -> tuple[List[Dict], int]:
    """先 `assert_no_fabrication` 硬拦截编造，再 `require_source` 标记缺溯源。

    返回 (带标记的 records, 待核实数)。任何编造都会在此间抛 AssertionError。
    调用方应捕获该异常并向用户报告，而非吞掉。
    """
    assert_no_fabrication(
        records, known_entities, key=key, entity_label=entity_label, ignore=ignore
    )
    return require_source(records, quote_key=quote_key)
