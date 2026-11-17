"""
REPORT — Bilingual Report Renderer (可选)
==========================================

把 CognitiveAuditEngine.audit() 产出的结构化报告，渲染为一个**可选语言**
的中文/英文外壳视图。

设计原则（与引擎定位保持一致）：
  - 零依赖、确定性、无 LLM 调用，纯词条映射。
  - 「外壳」双语：报告标题、算子名、裁定级别、证书字段、责任账户标签。
  - 「证据正文」保原文：logical_core / checks / violations 等分析内容是
    动态拼接的证据级文本，不做翻译，避免失真与破坏可签名验证语义。
  - 渲染器不修改原始报告，也不参与五算子管线；作为可选工具供上层调用。

用法：
    from plugins import ReportRenderer

    renderer = ReportRenderer()
    zh_view = renderer.render(report, lang="zh")   # 中文外壳
    en_view = renderer.render(report, lang="en")   # 英文外壳
"""

import time
from typing import Dict, Any, List


class ReportRenderer:
    """可选双语外壳渲染器：把审计报告本地化外壳、保留证据正文。"""

    # ── 词条表：{key: (zh, en)} ──
    TITLE = "认知审计报告", "Cognitive Audit Report"

    OPERATORS = {
        "NS":        ("叙事剥离",       "Narrative Strip"),
        "IAP":       ("隐假设透视",     "Implicit Assumption Analysis"),
        "LCH":       ("脆弱性对冲",     "Fragility Latch"),
        "CCS":       ("因果链同步",     "Causal Chain Sync"),
        "STATE":     ("责任锚定",       "State Anchor"),
        "llm_enhanced": ("LLM 增强分析", "LLM-Enhanced Analysis"),
    }

    VERDICT_LEVELS = {
        "AUDIT_HALT": ("审计阻断", "AUDIT HALT"),
        "AUDIT_WARN": ("审计警告", "AUDIT WARN"),
        "AUDIT_PASS": ("审计通过", "AUDIT PASS"),
    }

    FIELDS = {
        "title":                ("报告", "Report"),
        "disclaimer":           ("免责声明", "Disclaimer"),
        "responsibility_account": ("责任账户", "Responsibility Account"),
        "organization":         ("组织", "Organization"),
        "role":                 ("角色", "Role"),
        "stage":                ("阶段", "Stage"),
        "nonce":                ("防重放随机串", "Nonce"),
        "is_vague":             ("组织模糊", "Vague Org"),
        "anchor_status":        ("锚定状态", "Anchor Status"),
        "warning":              ("警告", "Warning"),
        "custom_fields":        ("自定义字段", "Custom Fields"),
        "operators":            ("审计算子", "Audit Operators"),
        "verdict":              ("最终裁定", "Final Verdict"),
        "level":                ("级别", "Level"),
        "summary":              ("摘要", "Summary"),
        "halt_count":           ("致命违规数", "Halt Count"),
        "warn_count":           ("警告数", "Warn Count"),
        "halt_items":           ("致命违规明细", "Halt Items"),
        "warn_items":           ("警告明细", "Warn Items"),
        "certificate":          ("审计证书", "Audit Certificate"),
        "audit_id":             ("审计 ID", "Audit ID"),
        "timestamp":            ("时间戳", "Timestamp"),
        "signature":            ("签名哈希", "Signature"),
        "algorithm":            ("签名算法", "Algorithm"),
        "verifiable":           ("可验证", "Verifiable"),
        "note":                 ("说明", "Note"),
        "responsibility":       ("责任锚定", "Responsibility"),
    }

    @staticmethod
    def _t(table: Dict[str, Any], key: str, lang: str) -> str:
        """按语言取词条：未收录的 key 原样返回。"""
        entry = table.get(key)
        if not entry:
            return key
        return entry[0] if lang == "zh" else entry[1]

    def _localize_status(self, level: str, lang: str) -> str:
        """裁定级别：中文外壳给中文名，英文外壳保留枚举（机器可读）。"""
        return self._t(self.VERDICT_LEVELS, level, lang) or level

    def render(self, report: Dict[str, Any], lang: str = "zh") -> Dict[str, Any]:
        """
        把审计报告渲染为指定语言的外壳视图。

        Args:
            report: engine.audit() 的返回（含 responsibility_account / analysis / ...）。
            lang:   "zh" 或 "en"，默认中文。
        Returns:
            本地化外壳的字典：顶层标题/免责声明/责任账户/裁定/证书/各算子
            （证据正文字段按原样保留）。
        """
        if lang not in ("zh", "en"):
            lang = "zh"

        analysis = report.get("analysis", {})
        state = analysis.get("STATE", {}) if isinstance(analysis, dict) else {}

        # 责任账户：仅本地化已收录的显示标签，未收录字段保留原样
        ra = report.get("responsibility_account", {})
        responsibility_view = {
            self._t(self.FIELDS, k, lang): v for k, v in ra.items()
        }

        # 各算子：核心标题本地化，分析正文透传
        operators_view = {}
        for name, result in analysis.items():
            label = self._t(self.OPERATORS, name, lang)
            if isinstance(result, dict):
                operators_view[name] = {
                    "label": label,
                    "result": result,
                }
            else:
                operators_view[name] = {"label": label, "result": result}

        # 裁定与证书：从 STATE 抽出做外壳本地化（值保持机器可读）
        verdict_view = None
        certificate_view = None
        if isinstance(state, dict):
            verdict = state.get("verdict") or {}
            if isinstance(verdict, dict):
                verdict_view = {
                    self._t(self.FIELDS, "level", lang): self._localize_status(
                        verdict.get("level", ""), lang),
                    self._t(self.FIELDS, "summary", lang): verdict.get("summary", ""),
                    self._t(self.FIELDS, "halt_count", lang): verdict.get("halt_count", 0),
                    self._t(self.FIELDS, "warn_count", lang): verdict.get("warn_count", 0),
                    self._t(self.FIELDS, "halt_items", lang): verdict.get("halt_items", []),
                    self._t(self.FIELDS, "warn_items", lang): verdict.get("warn_items", []),
                }
            cert = state.get("certificate") or {}
            if isinstance(cert, dict):
                certificate_view = {
                    self._t(self.FIELDS, "audit_id", lang): cert.get("audit_id", ""),
                    self._t(self.FIELDS, "timestamp", lang): cert.get("timestamp", ""),
                    self._t(self.FIELDS, "signature", lang): cert.get("signature", ""),
                    self._t(self.FIELDS, "algorithm", lang): cert.get("algorithm", ""),
                    self._t(self.FIELDS, "verifiable", lang): cert.get("verifiable", ""),
                    self._t(self.FIELDS, "note", lang): cert.get("note", ""),
                }

        return {
            "title": self.TITLE[0 if lang == "zh" else 1],
            self._t(self.FIELDS, "disclaimer", lang): report.get("disclaimer", ""),
            self._t(self.FIELDS, "responsibility_account", lang): responsibility_view,
            self._t(self.FIELDS, "verdict", lang): verdict_view,
            self._t(self.FIELDS, "certificate", lang): certificate_view,
            self._t(self.FIELDS, "operators", lang): operators_view,
            self._t(self.FIELDS, "custom_fields", lang): report.get("custom_fields", {}),
            "_meta": {
                "lang": lang,
                "generated_at": int(time.time()),
            },
        }

    def render_text(self, report: Dict[str, Any], lang: str = "zh") -> str:
        """渲染为便于人工阅读的纯文本（保留原文正文）。"""
        view = self.render(report, lang)
        lines: List[str] = []
        lines.append(view["title"])
        lines.append("=" * 40)

        dis = view.get(self._t(self.FIELDS, "disclaimer", lang))
        if dis:
            lines.append(f"{self._t(self.FIELDS, 'disclaimer', lang)}: {dis}")

        ra = view.get(self._t(self.FIELDS, "responsibility_account", lang))
        if isinstance(ra, dict):
            header = self._t(self.FIELDS, "responsibility_account", lang)
            lines.append(f"\n{header}")
            for k, v in ra.items():
                lines.append(f"  {k}: {v}")

        vd = view.get(self._t(self.FIELDS, "verdict", lang))
        if isinstance(vd, dict):
            lines.append(f"\n{self._t(self.FIELDS, 'verdict', lang)}")
            for k, v in vd.items():
                lines.append(f"  {k}: {v}")

        cert = view.get(self._t(self.FIELDS, "certificate", lang))
        if isinstance(cert, dict):
            lines.append(f"\n{self._t(self.FIELDS, 'certificate', lang)}")
            for k, v in cert.items():
                lines.append(f"  {k}: {v}")

        ops = view.get(self._t(self.FIELDS, "operators", lang))
        if isinstance(ops, dict):
            lines.append(f"\n{self._t(self.FIELDS, 'operators', lang)}")
            for name, item in ops.items():
                lines.append(f"  {item['label']} ({name})")
                result = item.get("result")
                if isinstance(result, dict):
                    # 证据正文原样透传：logical_core / checks / violations 等
                    for k, v in result.items():
                        if isinstance(v, (dict, list)):
                            lines.append(f"    {k}: {v}")
                        else:
                            lines.append(f"    {k}: {v}")

        return "\n".join(lines)