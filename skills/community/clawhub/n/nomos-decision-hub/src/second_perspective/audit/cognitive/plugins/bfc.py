"""
BFC — 二元事实校验 / Binary Fact Check
=======================================

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
# 分区③ 算子 BFC — 二元事实校验 / Binary Fact Check
# ============================================================================
# BFC — 二元事实校验 / Binary Fact Check
# =====================================
#
# 把一条断言归约为**真 / 假**两个值之一。没有第三个值。
#
# 为什么是二元的
# --------------
# 规范公理 3 原文：「无中间模糊状态：校验只有通过 / 不通过两种结果，
# 不存在"大概对""可能没问题"的灰色地带。」
#
# 所以本模块的语义边界只有两条：
#   1. 能归约  → 输出 True 或 False（真值只能由外部声明，模块永不推断）
#   2. 不能归约 → 输出一个 **status**（中断或信号），**绝不**伪造一个"未决"真值
#
# 这是本模块与其它算子最关键的区别：`binary=None` 只表示「未声明」，
# 它必然伴随 `VERDICT_UNDECLARED`，且被排除在所有统计与判定之外。
# 把 None 当成第三真值，就等于把「不知道」洗成了「一个答案」。
#
# 与 ⇄GRF 的分工
# --------------
#     ⇄ GRF  问：现实反馈回来了，**结构上有没有回退路径 ΔD**   —— 行为层
#     BFC    问：这条断言，**有没有证据、证据打不打架、核验结果是什么** —— 认知层
#
# 判定链（全部为结构判断，零 LLM、零概率词）
# ------------------------------------------
#     SKIPPED            未启用（未提供 facts / verify_facts）        不计入风险
#     NOTHING_TO_VERIFY  开闸了却一条校验对象都没有                   WARNING
#     EVIDENCE_VACUUM    某条断言证据为空                             BLOCKED（致命）
#     EVIDENCE_CONFLICT  同一断言的证据/观察互相否定                   BLOCKED（致命）
#     FALSIFIED_PREMISE  已核验为假，却仍留在 assumptions 里            BLOCKED（致命）
#     VERDICT_UNDECLARED 有证据但真值未声明                           HIGH_RISK（信号）
#     VERIFIED           全部为真                                     PASS
#
# 级别由严重度决定（HALT > HIGH_RISK > WARNING），不依赖规则书写顺序。
#
# 默认不启用
# ----------
# 不提供 `facts` 时本模块原样放行（status = SKIPPED），存量审计的判定与链根不变。
# 事实校验是**拿证据换来的**，不是默认塞给用户的。
#
# 输入契约
# --------
#     facts         list    [{"id": "F1", "claim": "需求稳定", "evidence": ["doc#123"]}]
#                           也接受 list[str]（只给断言文本，证据回落到 ctx['evidence']）
#     observations  dict    {"F1": True} 或 {"需求稳定": False}
#                           别名 verdicts / fact_verdicts；真值只能来自这里
#     verify_facts  bool    显式开闸（等价于提供了 facts）
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

SEVERITY_RANK = {"HALT": 0, "HIGH_RISK": 1, "WARNING": 2}


class BinaryFactCheckPlugin:
    """BFC 算子：二元事实校验。"""

    PLUGIN_NAME = "BFC"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Binary Fact Check — 断言归约为真/假；不能归约即中断，不给第三值"

    FACTS_KEYS = ("facts", "claims", "facts_to_check", "断言")
    OBSERVATION_KEYS = ("observations", "verdicts", "fact_verdicts", "真值")

    TRUE_TOKENS = {"true", "1", "yes", "confirmed", "confirm", "pass", "held",
                   "真", "成立", "已验证", "已证实", "属实"}
    FALSE_TOKENS = {"false", "0", "no", "falsified", "falsify", "fail", "failed",
                    "假", "不成立", "未成立", "已证伪", "属伪"}

    def __init__(self) -> None:
        self.name = self.PLUGIN_NAME

    # ── main entry ──

    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        ctx = decision_context if isinstance(decision_context, dict) else {}

        raw_facts = self._extract_facts(ctx)
        active = bool(raw_facts) or bool(ctx.get("verify_facts"))

        if not active:
            # 未启用：原样放行。不产出 status，故对收敛判定与链根零影响。
            return {
                "plugin": self.PLUGIN_NAME,
                "version": self.PLUGIN_VERSION,
                "status": "SKIPPED",
                "mode": "SKIPPED",
                "reason": "NOT_ENABLED",
                "message": "未提供 facts / verify_facts —— 二元事实校验未启用，原样放行。",
                "facts_checked": 0,
                "true_count": 0,
                "false_count": 0,
                "undeclared_count": 0,
                "verdicts": [],
                "violations": [],
                "remediation": [],
                "pass": True,
            }

        facts = self._normalize_facts(raw_facts, ctx)
        observations = self._extract_observations(ctx)
        assumptions = self._extract_assumptions(ctx)

        violations: List[Dict[str, Any]] = []
        remediation: List[str] = []
        verdicts: List[Dict[str, Any]] = []

        if not facts:
            violations.append({
                "code": "NOTHING_TO_VERIFY",
                "severity": "WARNING",
                "message": "已开闸但未提供任何校验对象 —— 空集不是「真」，也不构成校验通过。",
            })
            remediation.append("在 facts 中至少给出一条 {claim, evidence}。")

        for fact in facts:
            fid, claim = fact["id"], fact["claim"]
            evidence = fact["evidence"]
            polarity = self._evidence_polarity(evidence)
            declared = observations.get(fid, observations.get(claim, None))

            if not evidence:
                violations.append({
                    "code": "EVIDENCE_VACUUM",
                    "severity": "HALT",
                    "message": f"[中断：由于关键变量 {fid} 的证据真空，归约无法成立] "
                               f"断言「{claim}」未附任何证据。",
                })
                remediation.append(f"{fid}「{claim}」：补证据来源清单（evidence）。")
            elif polarity == "conflict":
                violations.append({
                    "code": "EVIDENCE_CONFLICT",
                    "severity": "HALT",
                    "message": f"断言「{claim}」的证据互相否定（同时存在支持与反对极性）—— "
                               f"本模块不做取舍，交由证据源裁定。",
                })
                remediation.append(f"{fid}「{claim}」：消解互斥证据，或拆成两条独立断言。")

            if declared is None and evidence and polarity != "conflict":
                violations.append({
                    "code": "VERDICT_UNDECLARED",
                    "severity": "HIGH_RISK",
                    "message": f"断言「{claim}」有证据但真值未声明 —— "
                               f"「有证据」不等于「已核验」；不给第三值，只给此信号。",
                })
                remediation.append(
                    f"{fid}「{claim}」：在 observations 中声明 true 或 false。")

            if declared is False and self._in_assumptions(claim, fid, assumptions):
                violations.append({
                    "code": "FALSIFIED_PREMISE",
                    "severity": "HALT",
                    "message": f"断言「{claim}」已核验为假，却仍留在 assumptions 中 —— "
                               f"决策支柱已断，结构上必须移除或触发对应 ΔD。",
                })
                remediation.append(f"{fid}「{claim}」：从假设集中撤下，或补齐对应分支响应。")

            verdicts.append({
                "id": fid,
                "claim": claim,
                "binary": declared,                      # None = 未声明，不是第三真值
                "evidence": [self._evidence_label(e) for e in evidence],
                "evidence_polarity": polarity,
                "source": "declared" if declared is not None else "undeclared",
            })

        has_halt = any(v["severity"] == "HALT" for v in violations)
        top = sorted(violations, key=lambda v: (SEVERITY_RANK.get(v["severity"], 9), v["code"]))

        if has_halt:
            status, reason = "BLOCKED", top[0]["code"]
        elif any(v["severity"] == "HIGH_RISK" for v in violations):
            status = "HIGH_RISK"
            reason = next(v["code"] for v in top if v["severity"] == "HIGH_RISK")
        elif violations:
            status, reason = "WARNING", top[0]["code"]
        else:
            status, reason = "PASS", "VERIFIED"

        declared_values = [v["binary"] for v in verdicts if v["binary"] is not None]
        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "status": status,
            "mode": "ACTIVE",
            "reason": reason,
            "facts_checked": len(facts),
            "true_count": sum(1 for v in declared_values if v is True),
            "false_count": sum(1 for v in declared_values if v is False),
            "undeclared_count": sum(1 for v in verdicts if v["binary"] is None),
            "verdicts": verdicts,
            "violations": violations,
            "remediation": remediation,
            "pass": status == "PASS",
        }

    # ── internals ──

    @staticmethod
    def _extract_facts(ctx: Dict[str, Any]) -> List[Any]:
        for key in BinaryFactCheckPlugin.FACTS_KEYS:
            val = ctx.get(key)
            if isinstance(val, list) and val:
                return val
        return []

    @staticmethod
    def _extract_observations(ctx: Dict[str, Any]) -> Dict[str, Any]:
        for key in BinaryFactCheckPlugin.OBSERVATION_KEYS:
            val = ctx.get(key)
            if isinstance(val, dict):
                return val
        return {}

    @staticmethod
    def _extract_assumptions(ctx: Dict[str, Any]) -> List[str]:
        for key in ("assumptions", "premises", "hypotheses", "core_assumptions"):
            val = ctx.get(key)
            if isinstance(val, list):
                return [str(a) for a in val if a]
            if isinstance(val, str) and val.strip():
                return [val]
        return []

    def _normalize_facts(self, raw: List[Any], ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
        """规范化断言列表。id 缺省时按 F1..Fn 编号；证据缺省时回落到 ctx['evidence']。"""
        fallback_evidence = ctx.get("evidence")
        if not isinstance(fallback_evidence, list):
            fallback_evidence = []

        out: List[Dict[str, Any]] = []
        for i, item in enumerate(raw):
            fid = f"F{i + 1}"
            if isinstance(item, str):
                claim = item.strip()
                evidence = list(fallback_evidence)
            elif isinstance(item, dict):
                claim = str(item.get("claim", item.get("text", item.get("statement", "")))).strip()
                fid = str(item.get("id", fid))
                ev = item.get("evidence", item.get("sources"))
                evidence = list(ev) if isinstance(ev, list) else []
            else:
                continue
            if not claim:
                continue
            out.append({"id": fid, "claim": claim, "evidence": evidence})
        return out

    def _normalize_bool(self, value: Any) -> Optional[bool]:
        """把外部声明的真值归一到 True / False；归不了就返回 None（不猜）。"""
        if isinstance(value, bool):
            return value
        if isinstance(value, dict):
            for key in ("binary", "value", "verdict", "true", "is_true"):
                if key in value:
                    return self._normalize_bool(value[key])
            return None
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if value == 1:
                return True
            if value == 0:
                return False
            return None
        if isinstance(value, str):
            token = value.strip().lower()
            if token in self.TRUE_TOKENS:
                return True
            if token in self.FALSE_TOKENS:
                return False
        return None

    def _evidence_polarity(self, evidence: List[Any]) -> str:
        """证据极性：none / support / oppose / conflict。

        只认显式声明的极性（dict 里的 polarity / supports / verdict）。
        纯字符串证据视为**并行收敛性**的中性来源——不猜测它的倾向。
        """
        polarities = set()
        for item in evidence:
            if not isinstance(item, dict):
                continue
            raw = None
            for key in ("polarity", "supports", "verdict", "holds"):
                if key in item:
                    raw = item[key]
                    break
            norm = self._normalize_bool(raw)
            if norm is not None:
                polarities.add(norm)

        if not polarities:
            return "none"
        if polarities == {True}:
            return "support"
        if polarities == {False}:
            return "oppose"
        return "conflict"

    @staticmethod
    def _evidence_label(item: Any) -> str:
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            return str(item.get("source", item.get("id", item)))
        return str(item)

    @staticmethod
    def _in_assumptions(claim: str, fid: str, assumptions: List[str]) -> bool:
        """已证伪的断言是否仍挂在假设集上。编号与全称两种写法都认。"""
        if claim in assumptions:
            return True
        return any(a in (fid, f"A{fid[1:]}", f"□{fid}") for a in assumptions)
