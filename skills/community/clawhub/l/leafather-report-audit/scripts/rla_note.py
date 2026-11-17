#!/usr/bin/env python3
"""rla_note.py — 让 pandas / numpy / 纯 Python 算出来的数字也能入账

为什么需要它：
    录像钩子只看得见 SQL（duckdb / sqlite / pandas.read_sql）。
    `pd.read_parquet(...)` 之后做 groupby / merge / apply 算出来的数，
    一条都录不到 → 账本为空 → 覆盖率恒为 0。
    这不是"没入账"，是"整条通道不存在"（星仔 2026-11-13 反馈）。

用法（在你的出报告脚本里）：

    from rla_note import note

    pool = len(df[df.tag == "高血压"])
    note("htn.pool", pool, expr="len(df[df.tag=='高血压'])",
         caliber="主标签=高血压，排除测量", unit="人")

规矩（三条）：
  1. **必须在 rla_report.py 里跑** —— 它负责设置 RLA_NOTES 并合并进账本。
     直接跑 python build.py 会报错（我们宁可吵，也不给你一个假账本）。
  2. 这类条目 `verifiable: false`：能证明"报告里的数来自这次计算"，
     但**不能复算**（没有 SQL）。审计结论会单独标注。
  3. id 一旦定下来就别改 —— 报告模板里写的是它。
  4. `expr` 是"人看的算式说明"（进 origin）；只有当你要**声明派生关系**时才传
     `derived_from=[...]`，那才会写进账本的 expr 字段（会被审计校验依赖）。
"""
from __future__ import annotations

import json
import os
from pathlib import Path

__all__ = ["note", "current_buffer"]

_ALLOWED = {"id", "label", "value", "unit", "caliber", "expr", "role",
            "confidence", "origin", "derived_from"}


class NoteError(RuntimeError):
    pass


def current_buffer() -> Path:
    """当前 note 缓冲区（由 rla_report/rla_track 通过环境变量指定）。"""
    p = os.environ.get("RLA_NOTES")
    if not p:
        raise NoteError(
            "没有在审计流程里运行：RLA_NOTES 未设置。\n"
            "  正确用法：python3 scripts/rla_report.py --out report.md -- python3 你的脚本.py\n"
            "  （直接用 python 跑脚本不会产生账本，我们宁可报错也不给你一个假账本）"
        )
    return Path(p)


def note(mid: str, value, *, label: str = "", unit: str = "",
         caliber: str = "", expr: str = "", role: str = "indicator",
         confidence: str = "", derived_from: list[str] | None = None) -> float:
    """登记一个非 SQL 算出来的数字，并原样返回它（方便 `x = note(...)` 链式使用）。"""
    if not mid or not isinstance(mid, str):
        raise NoteError("note() 的第一个参数必须是指标 id（字符串）")
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise NoteError(f"note({mid!r}) 的 value 不是数字：{value!r}") from None

    # label 必填兜底：账本契约要求每条都有 label，否则审计判"账本不合格"
    rec = {"id": mid, "value": v, "role": role or "indicator",
           "label": label or mid,
           "verifiable": False, "source": "note-api",
           # origin 必填（validate 的规矩：verifiable=false 必须说来历）
           "origin": f"rla_note 登记：{expr or caliber or '脚本内计算，无 SQL'}"}
    if unit:
        rec["unit"] = unit
    if caliber:
        rec["caliber"] = caliber
    if confidence:
        rec["confidence"] = confidence
    # expr 在账本契约里是"派生算式"（必须配 derived_from）。
    # 只有显式给了 derived_from 才写 expr，否则把算式留在 origin 里 ——
    # 免得 `len(df[...])` 这种自由文本被当成派生依赖校验。
    if derived_from:
        rec["derived_from"] = list(derived_from)
        if expr:
            rec["expr"] = expr
    extra = set(rec) - _ALLOWED - {"verifiable", "source"}
    if extra:
        raise NoteError(f"note({mid!r}) 有未知字段：{sorted(extra)}")

    buf = current_buffer()
    buf.parent.mkdir(parents=True, exist_ok=True)
    with open(buf, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return v


def load_buffer(path: str | Path) -> list[dict]:
    """读缓冲区（rla_collect 合并用）。同一 id 重复登记取最后一次。"""
    p = Path(path)
    if not p.exists():
        return []
    by_id: dict[str, dict] = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("id"):
            by_id[str(rec["id"])] = rec
    return list(by_id.values())
