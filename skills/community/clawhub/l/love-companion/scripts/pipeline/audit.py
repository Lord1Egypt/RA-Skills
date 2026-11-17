#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token 审计（M8）——方案第七部分验收标准的执行者

要回答两个问题：
1. 真实一轮跑下来，各段各占多少 Token？合计有没有超红线（默认 500）？
2. 最坏情况（所有模块同时拉满）会不会超？超了是怎么被压下去的？

`stress_test` 会构造一个「每个模块都给超额内容」的极端场景，
验证注入器确实把它压回预算内——这是方案红线的回归测试。
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# 允许 `python scripts/pipeline/audit.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core import schema  # noqa: E402
from scripts.pipeline.injector import Injector  # noqa: E402

DEFAULT_TOTAL = schema.DEFAULT_INJECTION_BUDGET["合计上限"]


def audit_prepared(prepared: Dict[str, Any]) -> Dict[str, Any]:
    """审计一次 prepare() 的实际产出"""
    tokens: Dict[str, int] = dict(prepared.get("tokens") or {})
    total = int(prepared.get("total_tokens", sum(tokens.values())))
    budget = int(prepared.get("budget", DEFAULT_TOTAL))
    return {
        "tokens": tokens,
        "total": total,
        "budget": budget,
        "headroom": budget - total,
        "within_budget": total <= budget,
        "truncated": list(prepared.get("truncated") or []),
        "dropped": list(prepared.get("dropped") or []),
        "by_priority": [(k, tokens.get(k, 0)) for k in schema.INJECTION_PRIORITY],
    }


def breakdown(prepared: Dict[str, Any]) -> str:
    """人话版审计结果"""
    a = audit_prepared(prepared)
    lines = [f"单轮注入 {a['total']}/{a['budget']} Token（余量 {a['headroom']}）"
             f"{'✅' if a['within_budget'] else '❌'}"]
    for key, used in a["by_priority"]:
        quota = schema.DEFAULT_INJECTION_BUDGET.get(key, 0)
        if used or key in (prepared.get("sections") or {}):
            lines.append(f"- {key}：{used} / 上限 {quota}")
    if a["truncated"]:
        lines.append(f"被截断：{'、'.join(a['truncated'])}")
    if a["dropped"]:
        lines.append(f"被丢弃：{'、'.join(a['dropped'])}")
    return "\n".join(lines)


def stress_test(total: Optional[int] = None, oversize: int = 5) -> Dict[str, Any]:
    """最坏情况压测：每个模块都给 5 倍超额内容

    Returns:
        审计结果；within_budget 必须为 True，否则说明预算约束失效
    """
    total = int(total if total is not None else DEFAULT_TOTAL)
    unit = "这是一段刻意超额的测试内容，用来验证预算硬约束。"
    inj = Injector(total_budget=total)
    for key in schema.INJECTION_PRIORITY:
        quota = schema.DEFAULT_INJECTION_BUDGET.get(key, 100)
        need = max(1, quota * oversize)
        inj.add(key, (unit * (need // len(unit) + 1))[:need])
    built = inj.build()
    prepared = {
        "tokens": built["tokens"],
        "total_tokens": built["total_tokens"],
        "budget": built["budget"],
        "truncated": built["truncated"],
        "dropped": built["dropped"],
        "sections": built["sections"],
    }
    result = audit_prepared(prepared)
    result["scenario"] = f"五模块同时给 {oversize} 倍超额内容"
    return result


def worst_case_table() -> List[Dict[str, Any]]:
    """各模块「单模块上限」与「优先级分配后实际能拿到的额度」对照表"""
    allocated = schema.allocate_budget(DEFAULT_TOTAL)
    rows = []
    for key in schema.INJECTION_PRIORITY:
        rows.append({
            "模块": key,
            "单模块上限": schema.DEFAULT_INJECTION_BUDGET[key],
            "总额度内能拿到": allocated[key],
            "是否被压缩": allocated[key] < schema.DEFAULT_INJECTION_BUDGET[key],
        })
    rows.append({"模块": "合计", "单模块上限": sum(
        schema.DEFAULT_INJECTION_BUDGET[k] for k in schema.INJECTION_PRIORITY),
        "总额度内能拿到": sum(allocated[k] for k in schema.INJECTION_PRIORITY),
        "是否被压缩": False})
    return rows


if __name__ == "__main__":
    import json
    print(json.dumps(worst_case_table(), ensure_ascii=False, indent=2))
    print()
    print(json.dumps(stress_test(), ensure_ascii=False, indent=2))
