"""
IAP — Implicit Assumption Plugin
================================

透视内隐假设：检测未声明的预设前提。

当推演 P → Q 时，强制挖掘并显式标记所有未声明的预设。
检测模式：
  - 自指假设 (P 引用自身作为前提)
  - 权力绕过 (P 含特权暗示，绕过正常校验)
  - 单边前提 (P 仅声明部分条件，遗漏关键前提)
  - 循环论证 (P == Q 且非空)

确定性 · 零随机 · 零 LLM 调用
"""

import re
from typing import Dict, Any, List, Tuple


class ImplicitAssumptionPlugin:
    """IAP 算子：内隐假设透视。"""

    PLUGIN_NAME = "IAP"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Implicit Assumption Perspective — 透视未声明的预设前提"

    # ── 特征码（可随年度标准更新） ──

    # 自指假设特征码
    SELF_REFERENTIAL_PATTERNS = [
        r"\b本(?:机构|组织|公司|部门|人)\s*(?:认为|确信|保证|承诺)\b",
        r"\b(?:我们|我方)\s*(?:一直以来|始终|一贯)\b",
        r"\b(?:上述|前述)\s*(?:结论|判断|决定)\s*(?:即|就是|意味着)\b",
        r"\bthis\s+(?:organization|company|department)\s+(?:believes|confirms|guarantees)\b",
        r"\bwe\s+have\s+always\b",
        r"\bthe\s+above\s+(?:conclusion|judgment|decision)\s+(?:is|means)\b",
    ]

    # 权力绕过特征码
    PRIVILEGE_BYPASS_PATTERNS = [
        r"\b(?:无需|不必|不需要)\s*(?:审批|审核|批准|备案|许可)\b",
        r"\b(?:直接|自行)\s*(?:执行|实施|处理|决定)\b",
        r"\b(?:特批|特事特办|绿色通道)\b",
        r"\b(?:豁免|免除)\s*(?:审查|审核|检查)\b",
        r"\bno\s+(?:review|approval|permission)\s+required\b",
        r"\bbypass\s+(?:review|approval|oversight)\b",
        r"\bexempt\s+from\s+(?:review|audit|inspection)\b",
    ]

    # 模糊前提标志（可能是"单边前提"的信号）
    UNILATERAL_PATTERNS = [
        r"\b(?:假设|假定|前提)\s*[:：]?\s*(?:.{0,20})\s*(?:成立|为真|有效)\b",
        r"\b(?:在其他条件不变的情况下|其他条件相同)\b",
        r"\b(?:如果|若)\s+(?:.{0,30})\s*(?:则|那么|就)\b",
        r"\bassuming\s+(?:that\s+)?\b",
        r"\bceteris\s+paribus\b",
        r"\bif\s+.{1,40}\s+then\b",
    ]

    def __init__(self):
        self.name = self.PLUGIN_NAME
        self._self_ref = [re.compile(p, re.IGNORECASE) for p in self.SELF_REFERENTIAL_PATTERNS]
        self._priv_bypass = [re.compile(p, re.IGNORECASE) for p in self.PRIVILEGE_BYPASS_PATTERNS]
        self._unilateral = [re.compile(p, re.IGNORECASE) for p in self.UNILATERAL_PATTERNS]

    # ── main entry ──
    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        text = self._extract_text(decision_context)
        assumptions = self._extract_assumptions(decision_context)

        if not text and not assumptions:
            return self._empty_result()

        flags: List[Dict[str, Any]] = []

        # Flag 0: 自指假设
        self_ref_hits = self._scan_patterns(text, self._self_ref, "self_referential")
        flags.extend(self_ref_hits)

        # Flag 1: 权力绕过
        priv_hits = self._scan_patterns(text, self._priv_bypass, "privilege_bypass")
        flags.extend(priv_hits)

        # Flag 2: 单边前提
        unilateral_hits = self._scan_patterns(text, self._unilateral, "unilateral_premise")
        flags.extend(unilateral_hits)

        # Flag 3: 循环论证 (P == Q)
        circular = self._detect_circular(decision_context)
        if circular:
            flags.append(circular)

        # Flag 4: 缺失前提检测
        missing = self._detect_missing_assumptions(decision_context, text)
        flags.extend(missing)

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "implicit_assumptions_found": len(flags) > 0,
            "flags": flags,
            "flag_count": len(flags),
            "pass": len(flags) == 0,
        }

    # ── internals ──

    @staticmethod
    def _extract_text(ctx: Dict[str, Any]) -> str:
        if isinstance(ctx, str):
            return ctx
        for key in ("text", "narrative", "output", "content", "decision_text", "llm_output", "decision"):
            val = ctx.get(key)
            if isinstance(val, str) and val.strip():
                return val
        return ""

    @staticmethod
    def _extract_assumptions(ctx: Dict[str, Any]) -> List[str]:
        """从 decision_context 提取显式声明的前提列表。"""
        if isinstance(ctx, dict):
            for key in ("assumptions", "premises", "hypotheses", "core_assumptions"):
                val = ctx.get(key)
                if isinstance(val, list):
                    return [str(a) for a in val]
                if isinstance(val, str):
                    return [val]
        return []

    @staticmethod
    def _scan_patterns(text: str, patterns: List[re.Pattern], flag_type: str) -> List[Dict[str, Any]]:
        hits: List[Dict[str, Any]] = []
        if not text:
            return hits
        for pat in patterns:
            for m in pat.finditer(text):
                hits.append({
                    "flag_type": flag_type,
                    "flag_id": f"IAP-{flag_type}",
                    "match": m.group(),
                    "position": [m.start(), m.end()],
                    "severity": "WARN" if flag_type != "privilege_bypass" else "HALT",
                    "description": f"内隐假设: {flag_type} — '{m.group()}'",
                })
        return hits

    @staticmethod
    def _detect_circular(ctx: Dict[str, Any]) -> Dict[str, Any] | None:
        """检测循环论证: P == Q 且非空。"""
        if not isinstance(ctx, dict):
            return None
        p = str(ctx.get("decision", ctx.get("p", "")))
        q = str(ctx.get("outcome", ctx.get("q", ctx.get("result", ""))))
        if p and q and p.strip() == q.strip():
            return {
                "flag_type": "circular_justification",
                "flag_id": "IAP-circular",
                "match": f"P == Q: '{p[:60]}'",
                "severity": "HALT",
                "description": "循环论证: 决策(P)与结果(Q)相同且非空",
            }
        return None

    @staticmethod
    def _detect_missing_assumptions(ctx: Dict[str, Any], text: str) -> List[Dict[str, Any]]:
        """检测决策是否缺少显式前提声明。"""
        violations: List[Dict[str, Any]] = []
        if not isinstance(ctx, dict):
            return violations

        decision = ctx.get("decision", "")
        assumptions = ctx.get("assumptions", ctx.get("premises", []))

        has_decision = isinstance(decision, str) and decision.strip()
        has_assumptions = isinstance(assumptions, list) and len(assumptions) > 0

        if has_decision and not has_assumptions:
            violations.append({
                "flag_type": "missing_assumptions",
                "flag_id": "IAP-missing",
                "match": "decision present, assumptions absent",
                "severity": "WARN",
                "description": "决策已声明但未列出任何前提假设 — 单边前提风险",
            })

        return violations

    @staticmethod
    def _empty_result() -> Dict[str, Any]:
        return {
            "plugin": "IAP",
            "version": "1.0.0",
            "implicit_assumptions_found": False,
            "flags": [],
            "flag_count": 0,
            "pass": True,
            "note": "No text or assumptions found to audit.",
        }
