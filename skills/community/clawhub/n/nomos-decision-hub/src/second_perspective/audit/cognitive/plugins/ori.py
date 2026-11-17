"""
⊙ ORI — 第一原点锚定 / Origin Anchor
===========================================

Porting provenance
------------------
Copied verbatim（只搬不改）from ``second-perspective/Second Perspective Engine.py``
（``second-perspective`` 分支的「十算子 + 元因果账本 + 自主进化层」状态）。
进入本仓库时只动了两件事：

  1. 补了一段 import 前导（源文件是单文件，其模块级 import 在 6000 行文件的顶部）；
  2. 其余一字未改 —— 没有改逻辑、没有改常数、没有改阈值。

Nomos 的插件契约比源引擎薄：一个插件就是「带 PLUGIN_NAME / PLUGIN_VERSION /
PLUGIN_DESCRIPTION 与 analyze(ctx) -> dict 的类」。以下代码天然满足该契约。

Copyright (c) 2026 Shanghai Linming Junhua Technology Co., Ltd.
              and NOHN AI TECHNOLOGY PTE. LTD.
All rights reserved.  Dual-track license — see ../LICENSE.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple

# ============================================================================
# 分区③ 算子 ⊙ORI — 第一原点锚定 / Origin Anchor
# ============================================================================
# ORI — ⊙ 第一原点锚定 / Origin Anchor Plugin
# ==========================================
#
# 锚定整条因果链的起点与终点：原点事件、目标稳态、能量资源约束。
#
# 为什么需要它
# ------------
# 规范第六条「元因果基底」给出了「溯源缺口 = 原初宇宙的起点，万事万物的能量本根」
# 与「因果承接 = 能量动态守恒，每个果即刻成为下一个因」。落到可审计的层面就是三件事：
#
#     原点事件     链不能凭空开始。没有起点，后面所有节点都失去序的依据。
#     目标稳态 S*  螺旋重构必须有收敛方向；没有终点，「迭代」退化为「转圈」。
#     能量/资源约束 无限因果思维的前提是拓扑无边界，但**能量守恒有硬顶**。
#                  资源不设上限的推演不是无限，是失控。
#
# 判定（全部为结构判断，不做估算）
# --------------------------------
#     ORIGIN_VACUUM       原点真空                      → BLOCKED    （致命）
#     GOAL_UNANCHORED     目标未锚定                    → HIGH_RISK  （信号）
#     RESOURCE_DEFICIT    资源缺口为负（能量守恒被违反）  → HIGH_RISK  （信号）
#     UNSPECIFIED_RESOURCE 资源块缺必需字段              → WARNING
#     其余                                              → PASS
#
# 「原点真空」是致命项，理由与 CCS 的信息黑洞一致：链的起点缺失时，
# 后续任何「看起来收敛了」的信号都不可信——风险集清零可能只是因为
# 没有原点可对齐。故本算子取 T1_STRUCTURAL，允许阻断。
#
# 资源缺口只做减法
# ----------------
#     gap = 可用 / 预算 − 已承诺
# 只做减法，不预测消耗、不推断剩余里程。无法做减法（字段缺位）时
# 报 UNSPECIFIED_RESOURCE，而不是猜一个数。
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

class OriginAnchorPlugin:
    """⊙ 算子：第一原点锚定。"""

    PLUGIN_NAME = "ORI"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Origin Anchor — 锚定原点事件/目标稳态/能量资源约束"

    ORIGIN_KEYS = ("origin", "origin_event", "第一原点", "□0")
    GOAL_KEYS = ("goal", "target_state", "objective", "S*", "稳态")
    RESOURCE_KEYS = ("resources", "resource", "energy", "能量", "约束")

    # 单个资源块内，代表「可用额度」与「已承诺额度」的字段名
    CAPACITY_FIELDS = ("budget", "available", "cap", "total", "额度", "预算", "上限")
    COMMITTED_FIELDS = ("committed", "used", "consumed", "spent", "已承诺", "已耗", "已用")

    def __init__(self) -> None:
        self.name = self.PLUGIN_NAME

    # ── main entry ──

    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        ctx = decision_context if isinstance(decision_context, dict) else {}
        origin = self._pick(ctx, self.ORIGIN_KEYS)
        goal = self._pick(ctx, self.GOAL_KEYS)
        resources = self._extract_resources(ctx)

        ledger = self._build_ledger(resources)
        gaps = [r for r in ledger if r["gap"] is not None and r["gap"] < 0]
        unspecified = [r for r in ledger if r["gap"] is None]

        origin_hash = self._fingerprint(origin, goal)
        warnings: List[str] = []
        reasons: List[str] = []

        # 判定优先级链：真空 > 目标 > 资源缺口 > 资源未声明 > 通过
        if not origin:
            status = "BLOCKED"
            reason = "ORIGIN_VACUUM"
            reasons.append("原点事件缺失 — 链无起点，后续节点的序无法成立")
        elif not goal:
            status = "HIGH_RISK"
            reason = "GOAL_UNANCHORED"
            reasons.append("目标稳态未锚定 — 无收敛方向，螺旋迭代退化为转圈")
        elif gaps:
            status = "HIGH_RISK"
            reason = "RESOURCE_DEFICIT"
            reasons.append("资源缺口为负 — 能量守恒被违反：" + "; ".join(
                f"{g['name']} gap={g['gap']}" for g in gaps
            ))
        elif unspecified:
            status = "WARNING"
            reason = "UNSPECIFIED_RESOURCE"
            reasons.append("资源块缺少可用/已承诺字段 — 无法做减法，拒绝估算：" + ", ".join(
                u["name"] for u in unspecified
            ))
        else:
            status = "PASS"
            reason = "ANCHORED"
            reasons.append(
                "原点、目标、资源三项锚定完成"
                + ("（未声明资源约束）" if not ledger else "")
            )

        if not ledger:
            warnings.append("未声明任何能量/资源约束 — 拓扑可扩展，但推演失去预算硬顶")
        for lost in self._pick_unknown(ctx):
            warnings.append(f"未知的资源字段 '{lost}'，已忽略（不猜测其含义）")

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "status": status,
            "reason": reason,
            "reasons": reasons,
            "warnings": warnings,
            "origin": origin or None,
            "goal": goal or None,
            "origin_hash": origin_hash,
            "resource_ledger": ledger,
            "resource_gap_total": sum(g["gap"] for g in gaps) if gaps else 0.0,
            "pass": status == "PASS",
        }

    # ── internals ──

    @staticmethod
    def _pick(ctx: Dict[str, Any], keys) -> str:
        for k in keys:
            v = ctx.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
            if isinstance(v, dict):
                for sub in ("text", "name", "id", "value"):
                    if isinstance(v.get(sub), str) and v[sub].strip():
                        return v[sub].strip()
        return ""

    def _extract_resources(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        for k in self.RESOURCE_KEYS:
            v = ctx.get(k)
            if isinstance(v, dict) and v:
                return v
        return {}

    @staticmethod
    def _pick_unknown(ctx: Dict[str, Any]) -> List[str]:
        """已知之外的资源字段一律不猜测其含义。"""
        known = set()
        for keys in (OriginAnchorPlugin.ORIGIN_KEYS, OriginAnchorPlugin.GOAL_KEYS,
                     OriginAnchorPlugin.RESOURCE_KEYS):
            known.update(keys)
        return sorted(k for k in ctx if str(k).endswith(("_energy", "_budget")) and k not in known)

    def _build_ledger(self, resources: Dict[str, Any]) -> List[Dict[str, Any]]:
        ledger: List[Dict[str, Any]] = []
        for name in sorted(resources):
            block = resources[name]
            if isinstance(block, (int, float)):
                # 只给一个裸数字：它是什么？可用额度还是已耗？无从判定 → 不做减法。
                ledger.append({
                    "name": str(name), "capacity": float(block), "committed": None,
                    "gap": None, "note": "裸数值，无法区分容量与已耗，拒绝估算",
                })
                continue
            if not isinstance(block, dict):
                ledger.append({
                    "name": str(name), "capacity": None, "committed": None,
                    "gap": None, "note": f"不支持的资源块类型 {type(block).__name__}",
                })
                continue
            cap = self._first_number(block, self.CAPACITY_FIELDS)
            com = self._first_number(block, self.COMMITTED_FIELDS)
            gap = (cap - com) if (cap is not None and com is not None) else None
            ledger.append({
                "name": str(name), "capacity": cap, "committed": com, "gap": gap,
                "note": "" if gap is not None else "缺少可用/已承诺字段",
            })
        return ledger

    @staticmethod
    def _first_number(block: Dict[str, Any], fields) -> Optional[float]:
        for f in fields:
            v = block.get(f)
            if isinstance(v, bool):
                continue
            if isinstance(v, (int, float)):
                return float(v)
        return None

    @staticmethod
    def _fingerprint(origin: str, goal: str) -> str:
        """原点指纹：螺旋层用它检测「原点漂移」。

        只由 origin + goal 的规范化文本推导，与资源、与时间均无关——
        漂移检测要问的是「还在追同一个目标吗」，不是「跑了多久」。
        """
        blob = json.dumps({"origin": origin, "goal": goal},
                          sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]
