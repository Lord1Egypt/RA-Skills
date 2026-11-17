"""
LCH — Fragility Latch Plugin
============================

脆弱性对冲：定位逻辑链中最脆弱的隐性变量 A。
计算当 非A（变量缺失或失效）发生时，整体决策的崩塌概率 Delta D。

输出：
  - 脆弱变量列表（按 Delta D 降序）
  - 每个变量的依赖链路径
  - 崩塌场景描述

确定性 · 零随机 · 零 LLM 调用
"""

from typing import Dict, Any, List


class FragilityLatchPlugin:
    """LCH 算子：脆弱性对冲。"""

    PLUGIN_NAME = "LCH"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Fragility Latch — 定位最脆弱变量，计算崩塌概率 Delta D"

    def __init__(self):
        self.name = self.PLUGIN_NAME

    # ── main entry ──
    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        assumptions = self._extract_assumptions(decision_context)
        dependencies = self._extract_dependencies(decision_context)
        branches = self._extract_branches(decision_context)

        if not assumptions:
            return self._empty_result()

        # 为每个前提计算脆弱性
        fragility_report: List[Dict[str, Any]] = []
        for i, assumption in enumerate(assumptions):
            frag = self._assess_fragility(
                assumption=assumption,
                index=i,
                assumptions=assumptions,
                dependencies=dependencies,
                branches=branches,
            )
            fragility_report.append(frag)

        # 按 Delta D 降序
        fragility_report.sort(key=lambda x: x["delta_d"], reverse=True)

        # 最脆弱变量
        weakest = fragility_report[0] if fragility_report else None
        system_delta_d = max((f["delta_d"] for f in fragility_report), default=0.0)

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "assumptions_audited": len(assumptions),
            "fragility_report": fragility_report,
            "weakest_variable": weakest,
            "system_delta_d": round(system_delta_d, 4),
            "has_branch_coverage": self._check_branch_coverage(assumptions, branches),
            "pass": system_delta_d < 0.7 and self._check_branch_coverage(assumptions, branches),
        }

    # ── internals ──

    @staticmethod
    def _extract_assumptions(ctx: Dict[str, Any]) -> List[str]:
        if isinstance(ctx, dict):
            for key in ("assumptions", "premises", "hypotheses", "core_assumptions"):
                val = ctx.get(key)
                if isinstance(val, list):
                    return [str(a) for a in val if a]
                if isinstance(val, str):
                    return [val] if val.strip() else []
        return []

    @staticmethod
    def _extract_dependencies(ctx: Dict[str, Any]) -> Dict[str, List[str]]:
        """提取依赖关系图。格式: {"A": ["B", "C"]} 表示 A 依赖 B 和 C。"""
        if isinstance(ctx, dict):
            for key in ("dependencies", "dependency_graph", "deps"):
                val = ctx.get(key)
                if isinstance(val, dict):
                    return {str(k): [str(v) for v in vs] for k, vs in val.items()}
        return {}

    @staticmethod
    def _extract_branches(ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
        """提取分支响应。格式: [{"assumption": "A1", "delta_d": "ΔD1"}]"""
        if isinstance(ctx, dict):
            for key in ("branches", "branch_responses", "failure_paths", "delta_d"):
                val = ctx.get(key)
                if isinstance(val, list):
                    return val if all(isinstance(v, dict) for v in val) else []
        return []

    @staticmethod
    def _assess_fragility(
        assumption: str,
        index: int,
        assumptions: List[str],
        dependencies: Dict[str, List[str]],
        branches: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """评估单个前提的脆弱性。"""
        # 基础 Delta D
        delta_d = 0.3  # 基础值

        # 因素 1: 无分支响应 → 脆弱性增加
        has_branch = any(
            b.get("assumption", b.get("premise", "")) == assumption
            or b.get("assumption", b.get("premise", "")) == f"A{index+1}"
            for b in branches
        )
        if not has_branch:
            delta_d += 0.3
        else:
            delta_d -= 0.1

        # 因素 2: 被其他前提依赖 → 脆弱性增加（关键节点）
        dependents = [
            a for a, deps in dependencies.items()
            if assumption in deps or f"A{index+1}" in deps
        ]
        if dependents:
            delta_d += 0.15 * len(dependents)

        # 因素 3: 模糊表述 → 脆弱性增加
        vague_markers = ["可能", "大概", "也许", "或许", "通常", "一般", "应该",
                         "maybe", "probably", "usually", "generally", "should"]
        lower_assumption = assumption.lower() if isinstance(assumption, str) else ""
        vague_count = sum(1 for m in vague_markers if m in lower_assumption)
        delta_d += 0.1 * vague_count

        # 因素 4: 不可证伪 → 脆弱性极高
        if not FragilityLatchPlugin._is_falsifiable(assumption):
            delta_d += 0.25

        # Clamp
        delta_d = max(0.0, min(1.0, delta_d))

        return {
            "assumption": assumption,
            "index": index,
            "delta_d": round(delta_d, 4),
            "has_branch_response": has_branch,
            "dependents": dependents,
            "is_falsifiable": FragilityLatchPlugin._is_falsifiable(assumption),
            "vague_markers_found": vague_count,
            "failure_scenario": f"若 非A{index+1} 成立（'{assumption[:40]}' 失效），"
                                f"决策崩塌概率 Delta D = {delta_d:.2f}",
        }

    @staticmethod
    def _is_falsifiable(assumption: str) -> bool:
        """检查前提是否可证伪。"""
        if not isinstance(assumption, str) or not assumption.strip():
            return False
        # 不可证伪的标志
        non_falsifiable = ["总是", "永远", "从不", "必然", "绝对",
                            "always", "never", "inevitably", "absolutely"]
        lower = assumption.lower()
        return not any(m in lower for m in non_falsifiable)

    @staticmethod
    def _check_branch_coverage(assumptions: List[str], branches: List[Dict[str, Any]]) -> bool:
        """检查是否所有前提都有对应的分支响应。"""
        if not assumptions:
            return True
        branch_targets = set()
        for b in branches:
            for key in ("assumption", "premise", "target"):
                val = b.get(key)
                if val:
                    branch_targets.add(str(val))
        covered = sum(1 for i, a in enumerate(assumptions)
                      if a in branch_targets or f"A{i+1}" in branch_targets)
        return covered == len(assumptions)

    @staticmethod
    def _empty_result() -> Dict[str, Any]:
        return {
            "plugin": "LCH",
            "version": "1.0.0",
            "assumptions_audited": 0,
            "fragility_report": [],
            "weakest_variable": None,
            "system_delta_d": 0.0,
            "has_branch_coverage": True,
            "pass": True,
            "note": "No assumptions found to assess fragility.",
        }
