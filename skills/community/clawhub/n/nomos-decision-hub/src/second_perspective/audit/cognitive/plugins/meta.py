"""
META — 元因果账本 / Meta-Causal Ledger
=========================================

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

from .topology import (
    SYM_NODE, SYM_EDGE, SYM_CONSTRAINT, SYM_UPSTREAM, SYM_DOWNSTREAM,
    REL_INPUT, REL_OUTPUT,
    SEVERITY_HALT, SEVERITY_WARN,
    CHECK_CONSISTENCY, CHECK_CONSTRAINT, CHECK_CLOSURE, CHECK_TIME_ORDER,
    TOPOLOGY_VERSION, TOPOLOGY_GRAMMAR_VERSION,
    TopoNode, TopoEdge, Constraint, ValidationIssue,
    default_constraints, TopologyGraph, TopologyValidator,
    build_from_decision_context,
)

# ===========================
#
# 责任闭环锚定：穿透集体平庸与组织模糊。
#
# 强制追溯每一个权重分配、参数设定或行为选择背后，
# 具体的、不可推卸的最小决策单元或自然人节点。
#
# 同时汇总前四级（NS/IAP/LCH/CCS）的审计结果，
# 生成最终审计结论与 AUDIT_PASS / AUDIT_WARN / AUDIT_HALT 信号。
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

# META — 元因果账本 / Meta-Causal Ledger
# ========================================
#
# 规范第六条元因果基底的**判据化**。五基在此改用因果论术语：
# 溯源缺口 / 并行收敛 / 叙事遮蔽 / 审计有界 / 因果承接。
# 它不引入任何新的因果律，只把规范里已经写死、却在引擎里只停留在注释里的
# 五条元基，落成五个可计算的账本。五条元基的原文与落地口径一一对应：
#
#   溯源缺口  原文：原初宇宙的起点，万事万物的能量本根。它看似无规则地涌动，
#               但随机不在世界，在观测者的知识缺口之中：
#               全部前置因未被解析，故显为溯源缺口。
#         落地：chaos_gaps     未解析的前置因逐条点名（既无分支补偿 ΔD，
#                              也无现实反馈 —— 两条结构化信号都没有）
#               misattributed 把「未解析」说成「随机/运气/说不准」的地方。
#                              这是规范点名要拦截的归因错误：随机不在世界，在缺口。
#
#   并行收敛  原文：最初之始，亦是最终之终。它容纳未来的一切因果链：多线并行，
#               而非分支分叉；极限处唯一收敛（S∞ = S*）。
#         落地：parallel_chains 多起点 —— 合法，这就是「平行」
#               forks           同一对节点的多条边 —— 违规，这就是「分叉」
#               limit_reached   由 ∞ 极限收敛器的状态回传，本算子只读不判
#
#   叙事遮蔽  原文：现实的反面，与现实一体两面，为一切谎言与梦境提供基底。
#               它是叙事事件 N_t 的所在：⊖ 从中析出干逻辑，A6 叙事熵度量其遮蔽程度。
#         落地：a6_narrative_entropy = 遮蔽字符数 / 原文总字符数（有理数，非概率）
#               reality_face         同一时刻的现实面：⇄GRF 的现实对齐状态
#               —— 「一体两面」的两半必须同时出现在账本里，缺任何一半都不算记完。
#
#   审计有界  原文：公平本身：相对的公平，对万物一视同仁，维系世间的动态平衡。
#               这是审计中立的本体表述：审计不参与决策，只审计决策如何形成；
#               A10 审计熵增有界，使演化收敛于 S*。
#         落地：audit_neutrality 审计只审计「决策如何形成」（恒 True，作为断言留痕）
#               a10_audit_entropy 每层新增留痕条数 = 「version 递增速率」的离散版
#               bounded           A10 是否有界 —— 这是自主进化能收敛于 S* 的算术前提，
#                                 也是 evolve() 的停机定理来源。
#
#   因果承接  原文：在万事万物中无处不在；它不是链的自环，而是链的普遍承接：
#               能量动态守恒，每一个果即刻成为下一个因，序不可倒置。
#         落地：succession_intact 承接完整性：序排得出来、且无自环
#               energy_ledger     ⇄ 能量账本（取 ⊙ORI 的只做减法结果，不重复估算）
#               —— 「不是链的自环」归 T303；「序不可倒置」归 T305/T307/T308。
#
# 级别：T2_SIGNAL —— 永不阻断
# -------------------------------
# 本算子是**度量与账本**，不是结构性缺失。把度量升格为阻断，等于用
# 「指标不好看」替换「输入不完整」，那正是本引擎一直拒绝的事
# （I-1 非猜测：中断只留给缺失，不留给观感）。因此它取 T2，
# 结构上就不可能翻转任何一次审计的通过与否。
#
# 确定性 · 零随机 · 零概率词 · 零 LLM 调用
# ----------------------------------------------------------------------------

TRACE_ATTRIBUTION_PATTERNS = (
    "随机", "运气", "说不准", "看情况", "玄学", "碰运气", "天意", "听天由命",
    "不可预测", "random", "luck", "lucky", "by chance", "unpredictable",
)


class MetaCausalLedgerPlugin:
    """META 算子：元因果账本（溯源缺口 · 并行收敛 · 叙事遮蔽 · 审计有界 · 因果承接）。"""

    PLUGIN_NAME = "META"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Meta-Causal Ledger — 元因果基底五条元基的判据化账本"

    # 阈值默认值 = 「规范未给数时的显式声明值」。要换口径就换 config，
    # 不允许在别处悄悄改常数（否则同一份输入在不同地方算出不同的 A6 / A10）。
    DEFAULT_NARRATIVE_ENTROPY_CEILING = 0.15
    DEFAULT_AUDIT_ENTROPY_CEILING = 12.0

    BG_TRACE_GAP = "trace_gap"
    BG_PARALLEL_CONVERGENCE = "parallel_convergence"
    BG_NARRATIVE_OCCLUSION = "narrative_occlusion"
    BG_BOUNDED_AUDIT = "bounded_audit"
    BG_CAUSAL_SUCCESSION = "causal_succession"

    def __init__(self) -> None:
        self.name = self.PLUGIN_NAME

    # ── main entry ──

    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        ctx = decision_context if isinstance(decision_context, dict) else {}
        prior = ctx.get("_prior_audit_results", {}) or {}

        def _r(name: str) -> Dict[str, Any]:
            val = prior.get(name)
            return val if isinstance(val, dict) else {}

        ns, tpg, grf, ori = _r("NS"), _r("TPG"), _r("GRF"), _r("ORI")

        ledger = {
            self.BG_TRACE_GAP: self._chaos(ctx, tpg, ns),
            self.BG_PARALLEL_CONVERGENCE: self._wuji(ctx, tpg),
            self.BG_NARRATIVE_OCCLUSION: self._illusion(ctx, ns, grf),
            self.BG_BOUNDED_AUDIT: self._tiandao(ctx, tpg),
            self.BG_CAUSAL_SUCCESSION: self._lunhui(ctx, tpg, ori),
        }

        highs = [k for k in sorted(ledger) if ledger[k]["status"] == "HIGH_RISK"]
        warns = [k for k in sorted(ledger) if ledger[k]["status"] == "WARNING"]
        if highs:
            status, reason = "HIGH_RISK", f"META_{highs[0]}"
        elif warns:
            status, reason = "WARNING", f"META_{warns[0]}"
        else:
            status, reason = "PASS", "META_BALANCED"

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "status": status,
            "reason": reason,
            "meta_bases": ledger,
            "high_risk_bases": highs,
            "warning_bases": warns,
            "pass": status == "PASS",
        }

    # ── 五条元基 ──

    def _chaos(self, ctx: Dict[str, Any], tpg: Dict[str, Any],
               ns: Dict[str, Any]) -> Dict[str, Any]:
        """溯源缺口：随机不在溯源缺口之中，只在观测者的知识缺口之中。"""
        topo = tpg.get("topology", {}) or {}
        edges = topo.get("edges", []) or []

        compensated = {str(e.get("src")) for e in edges
                       if str(e.get("dst", "")).startswith(SYM_NODE + "ΔD")}
        observed = {str(k) for k in (ctx.get("feedback") or {})}

        gaps: List[Dict[str, Any]] = []
        for node in topo.get("nodes", []) or []:
            nid = str(node.get("id", ""))
            if not nid.startswith(SYM_NODE + "A"):
                continue
            if nid in compensated:
                continue          # 前置因已被 ΔD 补偿路径解析
            if str(node.get("note", "")) in observed:
                continue          # 前置因已被现实反馈解析
            gaps.append({
                "node": nid,
                "gap": "前置因未被解析：既无分支补偿 ΔD，也无现实反馈",
            })

        text = self._text(ctx).lower()
        misattributed = [p for p in TRACE_ATTRIBUTION_PATTERNS if p.lower() in text]

        if misattributed and gaps:
            status, reason = "HIGH_RISK", "TRACE_MISATTRIBUTED_WITH_GAPS"
        elif misattributed:
            status, reason = "WARNING", "TRACE_MISATTRIBUTED"
        elif gaps:
            status, reason = "WARNING", "TRACE_GAPS_UNRESOLVED"
        else:
            status, reason = "PASS", "TRACE_RESOLVED"

        return {
            "status": status,
            "reason": reason,
            "gaps": gaps,
            "gap_count": len(gaps),
            "misattributed": misattributed,
            "doctrine": "随机不在世界，在观测者的知识缺口之中",
        }

    def _wuji(self, ctx: Dict[str, Any], tpg: Dict[str, Any]) -> Dict[str, Any]:
        """并行收敛：多线并行，而非分支分叉；极限处唯一收敛。"""
        order = (tpg.get("topology", {}) or {}).get("time_order", {}) or {}
        forks = order.get("forks", []) or []
        parallel = int(order.get("parallel_chains", 0) or 0)

        lim = ctx.get("_limit_state")
        limit_reached = bool(isinstance(lim, dict) and lim.get("limit_reached"))

        status = "WARNING" if forks else "PASS"
        reason = "CONVERGENCE_FORK_VIOLATION" if forks else "CONVERGENCE_PARALLEL_OK"
        return {
            "status": status,
            "reason": reason,
            "parallel_chains": parallel,
            "forks": forks,
            "fork_count": len(forks),
            "limit_reached": limit_reached,
            "doctrine": "平行是同一世界线上多条各自有序的链；分支是未来真的分叉。"
                        "SPL 是强决定论，只承认前者。",
        }

    def _illusion(self, ctx: Dict[str, Any], ns: Dict[str, Any],
                  grf: Dict[str, Any]) -> Dict[str, Any]:
        """叙事遮蔽：叙事事件 N_t 的所在；A6 叙事熵度量其遮蔽程度。"""
        text = self._text(ctx)
        segments = ns.get("narrative_segments", []) or []
        masked = sum(len(str(s.get("marker", ""))) for s in segments
                     if isinstance(s, dict))
        total = len(text)
        a6 = round(masked / total, 6) if total else 0.0
        ceiling = self._ceiling(ctx, "narrative_entropy_ceiling",
                                self.DEFAULT_NARRATIVE_ENTROPY_CEILING)

        status = "WARNING" if a6 > ceiling else "PASS"
        return {
            "status": status,
            "reason": "NARRATIVE_OCCLUDED" if status == "WARNING" else "NARRATIVE_TRANSPARENT",
            "a6_narrative_entropy": a6,
            "masked_chars": masked,
            "total_chars": total,
            "ceiling": ceiling,
            # 一体两面的另一半：现实面。此处只记录，不继承它的严重度，
            # 否则同一个现实问题会在 GRF 与 META 里被计两次。
            "reality_face": {
                "status": grf.get("status"),
                "reason": grf.get("reason"),
            },
            "doctrine": "叙事遮蔽与现实一体两面；A6 只度量遮蔽，不判断对错",
        }

    def _tiandao(self, ctx: Dict[str, Any], tpg: Dict[str, Any]) -> Dict[str, Any]:
        """审计有界：审计中立；A10 审计熵增有界，使演化收敛于 S*。"""
        topo = tpg.get("topology", {}) or {}
        provenance = topo.get("provenance", []) or []

        spiral = ctx.get("_spiral_state")
        layers = 1
        if isinstance(spiral, dict):
            layer_list = spiral.get("layers") or []
            if isinstance(layer_list, list) and layer_list:
                layers = len(layer_list)

        a10 = round(len(provenance) / layers, 6) if layers else 0.0
        ceiling = self._ceiling(ctx, "audit_entropy_ceiling",
                                self.DEFAULT_AUDIT_ENTROPY_CEILING)
        bounded = a10 <= ceiling

        return {
            "status": "PASS" if bounded else "WARNING",
            "reason": "AUDIT_BOUNDED" if bounded else "AUDIT_ENTROPY_UNBOUNDED",
            # 审计中立的本体断言：引擎只审计「决策如何形成」，
            # 不参与决策、不出建议、不给排名 —— 这三条在结构上由
            # FORBIDDEN_LLM_KEYS 与决策无关性共同保证。
            "audit_neutrality": True,
            "a10_audit_entropy": a10,
            "ceiling": ceiling,
            "bounded": bounded,
            "provenance_entries": len(provenance),
            "layers": layers,
            "doctrine": "审计不参与决策，只审计决策如何形成；熵增有界则演化收敛于 S*",
        }

    def _lunhui(self, ctx: Dict[str, Any], tpg: Dict[str, Any],
                ori: Dict[str, Any]) -> Dict[str, Any]:
        """因果承接：不是链的自环，而是链的普遍承接；果即刻成因，序不可倒置。"""
        order = (tpg.get("topology", {}) or {}).get("time_order", {}) or {}
        assignable = bool(order.get("assignable"))
        inverted = order.get("inverted", []) or []

        succession = assignable and not inverted
        return {
            "status": "PASS" if succession else "WARNING",
            "reason": "SUCCESSION_INTACT" if succession
                      else "SUCCESSION_BROKEN",
            "succession_intact": succession,
            "assignable": assignable,
            "inverted": inverted,
            "observer_anchor": order.get("observer_anchor", ""),
            "observer_chain_size": order.get("observer_chain_size", 0),
            # 能量账本直接取 ⊙ORI 的只做减法结果，不在本算子重算一遍 ——
            # 同一件事算两次，迟早会算出两个数。
            "energy_ledger": ori.get("resource_ledger", []),
            "doctrine": "它不是链的自环，而是链的普遍承接；序不可倒置",
        }

    # ── internals ──

    @staticmethod
    def _text(ctx: Dict[str, Any]) -> str:
        """与 ⊗NS 同源取文：保证 A6 度量的是 NS 实际看过的那段文本。"""
        if isinstance(ctx, str):
            return ctx
        for key in ("text", "narrative", "output", "content",
                    "decision_text", "llm_output", "background", "summary", "description"):
            val = ctx.get(key)
            if isinstance(val, str) and val.strip():
                return val
        if isinstance(ctx.get("decision"), str):
            return ctx["decision"]
        return ""

    @staticmethod
    def _ceiling(ctx: Dict[str, Any], key: str, default: float) -> float:
        cfg = ctx.get("_config")
        if isinstance(cfg, dict) and key in cfg:
            try:
                return float(cfg[key])
            except (TypeError, ValueError):
                return default
        return default
