"""
⇄ GRF — 灰度执行与现实反馈 / Gray Feedback
=================================================

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
# 分区③ 算子 ⇄GRF — 灰度执行与现实反馈 / Gray Feedback
# ============================================================================
# GRF — ⇄ 灰度执行与现实反馈 / Gray Feedback Plugin
# ================================================
#
# 把「预测的崩塌」与「现实返回的观测」对齐。这是整条流水线里唯一引入
# 现实输入的算子，对应规范里「叙事遮蔽 — 现实的反面，与现实一体两面」。
#
# 三层判定
# --------
#   REALITY_CONTRADICTION  假设已被现实证伪，决策却未触发对应的 ΔD   → BLOCKED
#   NO_GRAY_LADDER         无灰度档位且一次性全量放行                  → HIGH_RISK
#   UNOBSERVED_ASSUMPTION  放量已越过档位，该假设仍未观测到            → WARNING
#   UNKNOWN_FEEDBACK_SUBJECT 反馈指向了未声明的假设                    → WARNING
#   其余                                                             → PASS
#
# 为什么 REALITY_CONTRADICTION 必须阻断
# -------------------------------------
# 这是本算子唯一不可让渡的判定：现实已经给出了否定证据，而结构上却没有任何
# 回退路径被触发。此时「审计通过」是纯粹的谎言——不是证据不足，是证据与结构
# 直接矛盾。故取 T1_STRUCTURAL 并允许阻断。
#
# 灰度档位的语义
# --------------
# gray_levels 是放量梯度（如 [0.01, 0.05, 0.25, 1.0]）。它的作用不是「建议分批」，
# 而是给「未观测」设一个可判定的期限：越过某档位后仍未观测到，就不再是「还没轮到」，
# 而是「没有观测手段」。因此缺档位 = 崩塌不可逆 = 结构性缺失。
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

class GrayFeedbackPlugin:
    """⇄ 算子：灰度执行与现实反馈。"""

    PLUGIN_NAME = "GRF"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Gray Feedback — 灰度档位 + 现实反馈对齐 + 证伪冲突检测"

    FEEDBACK_KEYS = ("feedback", "reality", "observation", "observations", "现实反馈")
    LEVEL_KEYS = ("gray_levels", "gray_ladder", "rollout_levels", "灰度档位")
    RATIO_KEYS = ("commit_ratio", "rollout_ratio", "exposure", "放量比例")

    CONFIRMED = {"confirmed", "confirm", "true", "pass", "held", "证实", "成立", "已验证", "已证实"}
    FALSIFIED = {"falsified", "falsify", "false", "fail", "failed", "broken",
                 "证伪", "失效", "不成立", "未成立", "已证伪"}
    UNOBSERVED = {"unobserved", "unknown", "pending", "none", "n/a",
                  "未观测", "未观测到", "待观测", "未知", "暂无"}

    def __init__(self) -> None:
        self.name = self.PLUGIN_NAME

    # ── main entry ──

    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        ctx = decision_context if isinstance(decision_context, dict) else {}
        assumptions = self._extract_assumptions(ctx)
        branches = self._extract_branches(ctx)
        feedback = self._extract_feedback(ctx)
        levels = self._extract_levels(ctx)
        ratio = self._extract_ratio(ctx)

        violations: List[Dict[str, Any]] = []
        warnings: List[str] = []

        # ── 规则一：现实证伪 vs 结构回退（唯一致命项）──
        contradictions: List[str] = []
        unobserved: List[str] = []
        unknown_subjects: List[str] = []
        alignment: List[Dict[str, Any]] = []

        for subject in sorted(feedback):
            verdict = feedback[subject]
            matched_assumption = self._match_assumption(subject, assumptions)
            branch = self._find_branch(matched_assumption, branches) if matched_assumption else None

            if not matched_assumption and assumptions:
                unknown_subjects.append(subject)

            if verdict == "falsified":
                if branch is None:
                    contradictions.append(subject)
                alignment.append({
                    "assumption": subject, "observed": "falsified",
                    "predicted_delta_d": None,
                    "branch_fired": branch is not None,
                    "aligned": branch is not None,
                })
            elif verdict == "unobserved":
                unobserved.append(subject)
                alignment.append({
                    "assumption": subject, "observed": "unobserved",
                    "predicted_delta_d": None, "branch_fired": False, "aligned": None,
                })
            else:
                alignment.append({
                    "assumption": subject, "observed": verdict,
                    "predicted_delta_d": None, "branch_fired": False, "aligned": True,
                })

        if contradictions:
            violations.append({
                "code": "REALITY_CONTRADICTION",
                "severity": "HALT",
                "message": ("现实已证伪下列假设，但结构上无对应 ΔD 分支被触发："
                            + ", ".join(contradictions)
                            + "。证据与结构直接矛盾，审计不得判通过。"),
            })

        # ── 规则二：灰度梯度缺位 ──
        if not levels and (ratio is None or float(ratio) >= 1.0):
            violations.append({
                "code": "NO_GRAY_LADDER",
                "severity": "HIGH_RISK",
                "message": ("未声明灰度档位且放量比例为全量 — 一旦崩塌不可逆，"
                            "现实反馈来不及产生就被吞掉。"),
            })

        # ── 规则三：越档仍未观测 ──
        if unobserved and levels:
            violations.append({
                "code": "UNOBSERVED_ASSUMPTION",
                "severity": "WARNING",
                "message": (f"灰度已推进至档位 {levels}，下列假设仍未观测到："
                            + ", ".join(unobserved) + " — 属观测手段缺失，非时间未到。"),
            })
        elif unobserved:
            violations.append({
                "code": "UNOBSERVED_ASSUMPTION",
                "severity": "WARNING",
                "message": "下列假设未观测到且无档位可界定期限：" + ", ".join(unobserved),
            })

        # ── 规则四：反馈对象悬空 ──
        if unknown_subjects:
            violations.append({
                "code": "UNKNOWN_FEEDBACK_SUBJECT",
                "severity": "WARNING",
                "message": "反馈指向未声明的假设：" + ", ".join(unknown_subjects),
            })

        if not feedback:
            warnings.append("未提供现实反馈 — 本次判定仅覆盖结构与灰度，不含现实对齐")

        has_halt = any(v["severity"] == "HALT" for v in violations)
        has_signal = any(v["severity"] in ("HIGH_RISK", "WARNING") for v in violations)

        if has_halt:
            status, reason = "BLOCKED", "REALITY_CONTRADICTION"
        elif any(v["severity"] == "HIGH_RISK" for v in violations):
            status, reason = "HIGH_RISK", next(
                v["code"] for v in violations if v["severity"] == "HIGH_RISK")
        elif has_signal:
            status, reason = "WARNING", next(
                v["code"] for v in violations if v["severity"] == "WARNING")
        else:
            status, reason = "PASS", "ALIGNED"

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "status": status,
            "reason": reason,
            "gray_levels": levels,
            "commit_ratio": ratio,
            "observed_count": len(feedback),
            "falsified_without_branch": contradictions,
            "unobserved": unobserved,
            "violations": violations,
            "reality_alignment": alignment,
            "warnings": warnings,
            "pass": status == "PASS",
        }

    # ── internals ──

    @staticmethod
    def _extract_assumptions(ctx: Dict[str, Any]) -> List[str]:
        for key in ("assumptions", "premises", "hypotheses", "core_assumptions"):
            val = ctx.get(key)
            if isinstance(val, list):
                return [str(a) for a in val if a]
            if isinstance(val, str) and val.strip():
                return [val]
        return []

    @staticmethod
    def _extract_branches(ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
        for key in ("branches", "branch_responses", "failure_paths"):
            val = ctx.get(key)
            if isinstance(val, list) and all(isinstance(v, dict) for v in val):
                return val
        return []

    def _extract_feedback(self, ctx: Dict[str, Any]) -> Dict[str, str]:
        for key in self.FEEDBACK_KEYS:
            val = ctx.get(key)
            if isinstance(val, dict):
                out: Dict[str, str] = {}
                for k in sorted(val):
                    out[str(k)] = self._normalize(val[k])
                return out
        return {}

    def _normalize(self, value: Any) -> str:
        """归一观测值。无法归一的一律记 unobserved——不猜。"""
        if isinstance(value, bool):
            return "confirmed" if value else "falsified"
        text = str(value).strip().lower()
        if text in self.FALSIFIED:
            return "falsified"
        if text in self.CONFIRMED:
            return "confirmed"
        if text in self.UNOBSERVED:
            return "unobserved"
        return "unobserved"

    @staticmethod
    def _extract_levels(ctx: Dict[str, Any]) -> List[float]:
        for key in GrayFeedbackPlugin.LEVEL_KEYS:
            val = ctx.get(key)
            if isinstance(val, list):
                out = []
                for v in val:
                    if isinstance(v, bool):
                        continue
                    if isinstance(v, (int, float)):
                        out.append(float(v))
                    elif isinstance(v, dict) and isinstance(v.get("ratio"), (int, float)):
                        out.append(float(v["ratio"]))
                if out:
                    return out
        return []

    @staticmethod
    def _extract_ratio(ctx: Dict[str, Any]) -> Optional[float]:
        for key in GrayFeedbackPlugin.RATIO_KEYS:
            val = ctx.get(key)
            if isinstance(val, bool):
                continue
            if isinstance(val, (int, float)):
                return float(val)
        return None

    @staticmethod
    def _match_assumption(subject: str, assumptions: List[str]) -> Optional[str]:
        """匹配口径与 LCH._check_branch_coverage 保持一致：全称文本或 A{i} 编号。"""
        if subject in assumptions:
            return subject
        for i, a in enumerate(assumptions):
            if subject in (f"A{i + 1}", f"□A{i + 1}"):
                return a
        return None

    @staticmethod
    def _find_branch(assumption: Optional[str], branches: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not assumption:
            return None
        for b in branches:
            for key in ("assumption", "premise", "target"):
                if str(b.get(key, "")) == assumption:
                    return b
        return None

# ============================================================================
# 分区③ 算子 ⊚STATE — 责任锚定 / State Anchor
# ============================================================================
# STATE — State Anchor Plugin
