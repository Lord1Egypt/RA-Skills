"""
CCS — Causal Chain Sync Plugin
==============================

反事实校验与逆反验证。

当推演 P → Q 时，强制执行：
  1. 逆反校验: 若 非P 成立，系统稳态是回退收敛还是系统性崩溃？
  2. 反事实校验: 非P 场景下 Q 会怎样？
  3. 因果链完整性: P → Q 之间是否有断点？

确定性 · 零随机 · 零 LLM 调用
"""

from typing import Dict, Any, List


class CausalChainSyncPlugin:
    """CCS 算子：因果同步与反事实校验。"""

    PLUGIN_NAME = "CCS"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Causal Chain Sync — 逆反校验 + 反事实校验 + 因果链完整性"

    def __init__(self):
        self.name = self.PLUGIN_NAME

    # ── main entry ──
    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        decision = self._extract_decision(decision_context)
        assumptions = self._extract_assumptions(decision_context)
        branches = self._extract_branches(decision_context)
        outcome = self._extract_outcome(decision_context)

        checks: List[Dict[str, Any]] = []

        # 1. 逆反校验: 非P → 系统稳态？
        inverse_check = self._inverse_check(decision, assumptions, branches)
        checks.append(inverse_check)

        # 2. 反事实校验: 非P 下 Q 会怎样？
        counterfactual = self._counterfactual_check(decision, assumptions, outcome, branches)
        checks.append(counterfactual)

        # 3. 因果链完整性: P → Q 有断点？
        chain_integrity = self._chain_integrity_check(decision, assumptions, outcome, branches)
        checks.append(chain_integrity)

        # 4. 信息黑洞检测
        blackhole = self._blackhole_check(decision, assumptions, outcome)
        checks.append(blackhole)

        halt_count = sum(1 for c in checks if c.get("severity") == "HALT")
        warn_count = sum(1 for c in checks if c.get("severity") == "WARN")

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "checks": checks,
            "halt_count": halt_count,
            "warn_count": warn_count,
            "pass": halt_count == 0,
        }

    # ── internals ──

    @staticmethod
    def _extract_decision(ctx: Dict[str, Any]) -> str:
        if isinstance(ctx, str):
            return ctx
        for key in ("decision", "p", "premise", "action"):
            val = ctx.get(key)
            if isinstance(val, str) and val.strip():
                return val
        return ""

    @staticmethod
    def _extract_assumptions(ctx: Dict[str, Any]) -> List[str]:
        if isinstance(ctx, dict):
            for key in ("assumptions", "premises", "hypotheses"):
                val = ctx.get(key)
                if isinstance(val, list):
                    return [str(a) for a in val if a]
        return []

    @staticmethod
    def _extract_branches(ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
        if isinstance(ctx, dict):
            for key in ("branches", "branch_responses", "failure_paths"):
                val = ctx.get(key)
                if isinstance(val, list):
                    return val if all(isinstance(v, dict) for v in val) else []
        return []

    @staticmethod
    def _extract_outcome(ctx: Dict[str, Any]) -> str:
        if isinstance(ctx, dict):
            for key in ("outcome", "q", "result", "consequence"):
                val = ctx.get(key)
                if isinstance(val, str) and val.strip():
                    return val
        return ""

    @staticmethod
    def _inverse_check(decision: str, assumptions: List[str],
                       branches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """逆反校验：若非P成立，系统是回退收敛还是系统性崩溃？"""
        if not decision:
            return {
                "check": "inverse",
                "severity": "WARN",
                "description": "未提供决策(P)，无法执行逆反校验",
                "result": "SKIP",
            }

        if not branches:
            return {
                "check": "inverse",
                "severity": "HALT",
                "description": f"决策 '{decision[:50]}' 无分支响应(ΔD) — 非P 场景下系统将无回退路径，系统性崩塌",
                "result": "SYSTEM_COLLAPSE",
            }

        # 检查分支响应是否覆盖了核心前提
        covered = len(branches)
        total_assumptions = len(assumptions) if assumptions else 1
        coverage = covered / total_assumptions if total_assumptions > 0 else 0

        if coverage >= 1.0:
            return {
                "check": "inverse",
                "severity": "PASS",
                "description": f"非P 场景有 {covered}/{total_assumptions} 个分支响应 — 回退收敛",
                "result": "CONVERGE",
            }
        elif coverage >= 0.5:
            return {
                "check": "inverse",
                "severity": "WARN",
                "description": f"非P 场景仅 {covered}/{total_assumptions} 个分支响应 — 部分回退",
                "result": "PARTIAL_RECOVERY",
            }
        else:
            return {
                "check": "inverse",
                "severity": "HALT",
                "description": f"非P 场景仅 {covered}/{total_assumptions} 个分支响应 — 系统性崩塌风险",
                "result": "COLLAPSE_RISK",
            }

    @staticmethod
    def _counterfactual_check(decision: str, assumptions: List[str],
                              outcome: str, branches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """反事实校验：非P 下 Q 会怎样？"""
        if not decision or not outcome:
            return {
                "check": "counterfactual",
                "severity": "WARN",
                "description": "缺少决策(P)或结果(Q)，无法执行反事实校验",
                "result": "SKIP",
            }

        # 检查是否存在与 P 相反的场景描述
        has_counterfactual = any(
            "非" in str(b.get("assumption", b.get("premise", "")))
            or "not" in str(b.get("assumption", b.get("premise", ""))).lower()
            or "若" in str(b.get("assumption", b.get("premise", "")))
            or "if" in str(b.get("assumption", b.get("premise", ""))).lower()
            for b in branches
        )

        if has_counterfactual:
            return {
                "check": "counterfactual",
                "severity": "PASS",
                "description": "存在反事实场景描述 — 非P 下的 Q' 已被考虑",
                "result": "COVERED",
            }
        else:
            return {
                "check": "counterfactual",
                "severity": "WARN",
                "description": "无反事实场景 — 非P 下 Q 会怎样未被显式考虑",
                "result": "UNCOVERED",
            }

    @staticmethod
    def _chain_integrity_check(decision: str, assumptions: List[str],
                               outcome: str, branches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """因果链完整性：P → (A1...An) → Q 是否有断点？"""
        if not decision:
            return {
                "check": "chain_integrity",
                "severity": "WARN",
                "description": "缺少决策(P)，因果链起点缺失",
                "result": "BROKEN_AT_ROOT",
            }

        if not outcome and not assumptions:
            return {
                "check": "chain_integrity",
                "severity": "HALT",
                "description": "因果链断裂：有 P 但无前提(A)也无结果(Q)",
                "result": "BROKEN",
            }

        # 检查链路完整性: P → A → Q
        has_p = bool(decision)
        has_a = len(assumptions) > 0
        has_q = bool(outcome)

        chain = []
        if has_p: chain.append("P")
        if has_a: chain.append("A")
        if has_q: chain.append("Q")

        if has_p and has_a and has_q:
            return {
                "check": "chain_integrity",
                "severity": "PASS",
                "description": f"因果链完整: {' → '.join(chain)}",
                "result": "COMPLETE",
            }
        elif has_p and has_a and not has_q:
            return {
                "check": "chain_integrity",
                "severity": "WARN",
                "description": "因果链不完整: P → A → ? (Q 缺失)",
                "result": "MISSING_Q",
            }
        elif has_p and not has_a and has_q:
            return {
                "check": "chain_integrity",
                "severity": "WARN",
                "description": "因果链跳跃: P → Q (无显式前提 A)",
                "result": "MISSING_A",
            }
        else:
            return {
                "check": "chain_integrity",
                "severity": "HALT",
                "description": f"因果链严重不完整: {' → '.join(chain) if chain else '空链'}",
                "result": "BROKEN",
            }

    @staticmethod
    def _blackhole_check(decision: str, assumptions: List[str],
                         outcome: str) -> Dict[str, Any]:
        """信息黑洞检测：关键变量缺失导致因果链无法建立。"""
        missing: List[str] = []
        if not decision:
            missing.append("P (决策)")
        if not assumptions:
            missing.append("A (前提)")
        if not outcome:
            missing.append("Q (结果)")

        if missing:
            return {
                "check": "blackhole",
                "severity": "HALT",
                "description": f"[中断：由于关键变量 {' / '.join(missing)} 真空，因果链断裂]",
                "result": "BLACKHOLE",
                "missing_variables": missing,
            }
        return {
            "check": "blackhole",
            "severity": "PASS",
            "description": "无信息黑洞 — 所有关键变量(P/A/Q)均在位",
            "result": "CLEAR",
        }
