"""
STATE — State Anchor Plugin
===========================

责任闭环锚定：穿透集体平庸与组织模糊。

强制追溯每一个权重分配、参数设定或行为选择背后，
具体的、不可推卸的最小决策单元或自然人节点。

同时汇总前四级（NS/IAP/LCH/CCS）的审计结果，
生成最终审计结论与 AUDIT_PASS / AUDIT_WARN / AUDIT_HALT 信号。

确定性 · 零随机 · 零 LLM 调用
"""

import hashlib
import time
from typing import Dict, Any, List


class StateAnchorPlugin:
    """STATE 算子：责任锚定 + 最终裁定。"""

    PLUGIN_NAME = "STATE"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "State Anchor — 责任闭环锚定 + 最终审计裁定"

    def __init__(self):
        self.name = self.PLUGIN_NAME

    # ── main entry ──
    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        account = decision_context.get("_responsibility_account", {})
        prior_reports = decision_context.get("_prior_audit_results", {})

        # 1. 责任锚定
        responsibility = self._anchor_responsibility(account, decision_context)

        # 2. 汇总前四级结果
        verdict = self._aggregate_verdict(prior_reports)

        # 3. 生成审计证书
        certificate = self._generate_certificate(
            responsibility, verdict, decision_context
        )

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "responsibility": responsibility,
            "verdict": verdict,
            "certificate": certificate,
            "pass": verdict["level"] != "AUDIT_HALT",
        }

    # ── internals ──

    @staticmethod
    def _anchor_responsibility(account: Dict[str, Any],
                               ctx: Dict[str, Any]) -> Dict[str, Any]:
        """穿透组织模糊，锚定到最小决策单元。"""
        org = account.get("organization", ctx.get("organization", "UNKNOWN"))
        role = account.get("role", ctx.get("role", "UNKNOWN"))
        stage = account.get("stage", ctx.get("stage", "UNKNOWN"))
        nonce = account.get("nonce", ctx.get("nonce", "UNANCHORED"))

        # 检测组织模糊
        is_vague = org in ("UNKNOWN", "", "集体", "团队", "公司", "各部门",
                           "group", "team", "company", "everyone", "all")

        anchor = {
            "organization": org,
            "role": role,
            "stage": stage,
            "nonce": nonce,
            "is_vague": is_vague,
            "anchor_status": "UNANCHORED" if is_vague else "ANCHORED",
            "warning": None,
        }

        if is_vague:
            anchor["warning"] = (
                f"责任主体 '{org}' 为组织模糊表述 — "
                f"必须追溯至具体的、不可推卸的最小决策单元或自然人节点"
            )

        return anchor

    @staticmethod
    def _aggregate_verdict(prior: Dict[str, Any]) -> Dict[str, Any]:
        """汇总 NS/IAP/LCH/CCS 四级结果，生成最终裁定。"""
        ns_result   = prior.get("NS", {})
        iap_result  = prior.get("IAP", {})
        lch_result  = prior.get("LCH", {})
        ccs_result  = prior.get("CCS", {})

        # 收集所有 HALT
        halts: List[str] = []
        warns: List[str] = []

        # NS
        if not ns_result.get("pass", True):
            warns.append(f"NS: {ns_result.get('violation_count', 0)} 叙事违规")

        # IAP
        for flag in iap_result.get("flags", []):
            if flag.get("severity") == "HALT":
                halts.append(f"IAP: {flag.get('flag_type', 'unknown')}")
            elif flag.get("severity") == "WARN":
                warns.append(f"IAP: {flag.get('flag_type', 'unknown')}")

        # LCH
        if not lch_result.get("pass", True):
            sys_dd = lch_result.get("system_delta_d", 0)
            warns.append(f"LCH: system Delta D = {sys_dd}")
            if sys_dd >= 0.7:
                halts.append(f"LCH: system Delta D = {sys_dd} ≥ 0.7 — 系统崩塌风险")

        # CCS
        for check in ccs_result.get("checks", []):
            if check.get("severity") == "HALT":
                halts.append(f"CCS: {check.get('check', 'unknown')} — {check.get('result', '')}")
            elif check.get("severity") == "WARN":
                warns.append(f"CCS: {check.get('check', 'unknown')} — {check.get('result', '')}")

        # ── 通用扫描：所有带 status 的算子统一映射 ──
        # 少了这一步，新增算子的 BLOCKED 会被静默吞掉：⊙ORI / ⊞TPG / BFC /
        # ⇄GRF 都不在上面四条专用摘录里，而「新算子没被计入」恰恰是最危险的
        # 那种失效 —— 报告看起来一切正常，阻断其实已经发生了。
        BLOCKING = {"BLOCKED", "CRITICAL"}
        RISKY = {"HIGH_RISK", "WARNING"}
        operator_statuses: Dict[str, str] = {}
        extra_halts: List[str] = []
        extra_warns: List[str] = []
        for name in sorted(prior):
            result = prior.get(name)
            if not isinstance(result, dict):
                continue
            status = result.get("status")
            if status is None:
                continue
            operator_statuses[name] = str(status)
            label = f"{name}: {result.get('reason', status)}"
            if status in BLOCKING:
                extra_halts.append(label)
            elif status in RISKY:
                extra_warns.append(label)

        # 只有通用扫描真的有内容时才合并（专用摘录在前，通用扫描在后）。
        # 于是「只跑原五算子子集」的调用方拿到的 verdict 与扩展前逐字节一致 ——
        # 兼容不是靠解释，是靠不写入空字段。
        if extra_halts or extra_warns:
            halts = list(dict.fromkeys(halts + extra_halts))
            warns = list(dict.fromkeys(warns + extra_warns))

        # 最终裁定
        if halts:
            level = "AUDIT_HALT"
            summary = f"审计阻断: {len(halts)} 项致命违规"
        elif warns:
            level = "AUDIT_WARN"
            summary = f"审计警告: {len(warns)} 项需关注"
        else:
            level = "AUDIT_PASS"
            summary = "审计通过: 无致命违规，无警告"

        return {
            "level": level,
            "summary": summary,
            "halt_items": halts,
            "warn_items": warns,
            "halt_count": len(halts),
            "warn_count": len(warns),
            "ns_pass": ns_result.get("pass", True),
            "iap_pass": iap_result.get("pass", True),
            "lch_pass": lch_result.get("pass", True),
            "ccs_pass": ccs_result.get("pass", True),
        }

    @staticmethod
    def _generate_certificate(resp: Dict[str, Any], verdict: Dict[str, Any],
                              ctx: Dict[str, Any]) -> Dict[str, Any]:
        """生成不可篡改的审计证书（哈希签名）。"""
        timestamp = int(time.time())
        # 构造待签名字符串
        sig_input = (
            f"{resp.get('organization','')}"
            f"|{resp.get('role','')}"
            f"|{resp.get('stage','')}"
            f"|{resp.get('nonce','')}"
            f"|{verdict.get('level','')}"
            f"|{verdict.get('halt_count',0)}"
            f"|{verdict.get('warn_count',0)}"
            f"|{timestamp}"
        )
        sig_hash = hashlib.sha256(sig_input.encode("utf-8")).hexdigest()

        return {
            "audit_id": f"SPL-{resp.get('nonce', '00000000')}-{timestamp}",
            "timestamp": timestamp,
            "signature": sig_hash,
            "algorithm": "SHA-256",
            "verifiable": True,
            "note": "本证书由 Cognitive Audit Engine 生成，"
                    "可通过签名哈希验证完整性。任何篡改将导致哈希不匹配。",
        }
