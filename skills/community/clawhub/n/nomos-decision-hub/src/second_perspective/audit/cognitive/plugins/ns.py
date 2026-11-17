"""
NS — Narrative Strip Plugin
============================

剥离叙事包装，提取逻辑骨架。

将输入文本中的修辞、情感、道德判断、立场粉饰分离，
只保留可形式化验证的逻辑核心 (logical core)。

确定性 · 零随机 · 零 LLM 调用
"""

import re
from typing import Dict, Any, List

# ── 修辞/情感/道德标记词库（可随年度标准更新） ──

RHETORICAL_MARKERS: List[str] = [
    # 情感强化
    "毫无疑问", "显而易见", "众所周知", "不言而喻", "毋庸置疑",
    "令人震惊", "令人担忧", "令人振奋", "令人失望", "令人兴奋",
    "遗憾的是", "幸运的是", "不幸的是", "可悲的是", "可怕的是",
    "当然", "显然", "确实", "当然啦", "毕竟",
    "amazing", "incredible", "obviously", "clearly", "undoubtedly",
    "unfortunately", "fortunately", "tragically", "sadly",
    "shockingly", "surprisingly", "inevitably", "certainly",
    # 道德/立场粉饰
    "必须承认", "应该看到", "值得注意", "需要强调",
    "不可否认", "不容忽视", "不可忽视", "不容置疑",
    "it is important to note", "it should be noted",
    "it is worth noting", "needless to say", "it goes without saying",
    # 模糊量化
    "大量", "许多", "相当多", "不少", "大部分", "绝大多数",
    "可能", "也许", "大概", "或许", "似乎", "看起来",
    "many", "several", "a lot of", "numerous", "considerable",
    "perhaps", "possibly", "likely", "arguably", "presumably",
    # 权威暗示
    "专家认为", "研究表明", "数据显示", "据报道",
    "experts say", "studies show", "research indicates", "reports suggest",
]

# 模糊量化的正则模式
VAGUE_QUANTIFIER_PATTERNS = [
    r"\b[一二两三四五六七八九十百千万亿]+\s*[百分比成]",
    r"\b\d+\s*[%％]\s*(?:左右|大概|大约|差不多|近|差不多)?",
    r"\b(?:超过|接近|将近|大约|大概|差不多)\s*\d+",
    r"\b(?:成百上千|数以万计|数以千计|数以百计|成千上万)\b",
]


class NarrativeStripPlugin:
    """NS 算子：叙事剥离。"""

    PLUGIN_NAME = "NS"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Narrative Strip — 剥离修辞/情感/道德粉饰，提取逻辑骨架"

    def __init__(self):
        self.name = self.PLUGIN_NAME
        # 预编译正则：标记词匹配
        self._marker_patterns = [
            re.compile(re.escape(m), re.IGNORECASE) for m in RHETORICAL_MARKERS
        ]
        self._vague_patterns = [re.compile(p, re.IGNORECASE) for p in VAGUE_QUANTIFIER_PATTERNS]

    # ── main entry ──
    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        text = self._extract_text(decision_context)
        if not text:
            return self._empty_result()

        segments = self._strip_narrative(text)
        logical_core = self._extract_logical_core(text, segments)
        violations = self._detect_violations(text, segments)

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "narrative_stripped": len(violations) == 0,
            "narrative_segments": segments,
            "logical_core": logical_core,
            "violations": violations,
            "violation_count": len(violations),
            "pass": len(violations) == 0,
        }

    # ── internals ──

    @staticmethod
    def _extract_text(ctx: Dict[str, Any]) -> str:
        """从 decision_context 中提取待审计文本。"""
        if isinstance(ctx, str):
            return ctx
        # 尝试常见字段
        for key in ("text", "narrative", "output", "content", "decision_text", "llm_output"):
            val = ctx.get(key)
            if isinstance(val, str) and val.strip():
                return val
        # 如果整个 context 就是纯文本
        if isinstance(ctx.get("decision"), str):
            return ctx["decision"]
        return ""

    def _strip_narrative(self, text: str) -> List[Dict[str, Any]]:
        """识别并标记所有叙事片段。"""
        segments: List[Dict[str, Any]] = []

        # 标记词
        for pat in self._marker_patterns:
            for match in pat.finditer(text):
                segments.append({
                    "type": "rhetorical_marker",
                    "marker": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                })

        # 模糊量化
        for pat in self._vague_patterns:
            for match in pat.finditer(text):
                segments.append({
                    "type": "vague_quantifier",
                    "marker": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                })

        # 去重（同一位置可能被多个模式命中）
        seen = set()
        unique: List[Dict[str, Any]] = []
        for seg in segments:
            key = (seg["start"], seg["end"])
            if key not in seen:
                seen.add(key)
                unique.append(seg)
        unique.sort(key=lambda s: s["start"])
        return unique

    @staticmethod
    def _extract_logical_core(text: str, segments: List[Dict[str, Any]]) -> str:
        """移除叙事片段后的逻辑骨架。"""
        if not segments:
            return text.strip()
        # 按位置倒序删除，避免偏移
        result = text
        for seg in sorted(segments, key=lambda s: s["start"], reverse=True):
            result = result[:seg["start"]] + result[seg["end"]:]
        # 清理多余空白
        result = re.sub(r"\s{2,}", " ", result).strip()
        return result

    @staticmethod
    def _detect_violations(text: str, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """生成违规列表。"""
        violations: List[Dict[str, Any]] = []
        for seg in segments:
            violations.append({
                "rule_id": f"NS-{seg['type']}",
                "description": f"叙事标记 '{seg['marker']}' 检出，建议剥离",
                "severity": "WARN",
                "position": [seg["start"], seg["end"]],
            })
        return violations

    @staticmethod
    def _empty_result() -> Dict[str, Any]:
        return {
            "plugin": "NS",
            "version": "1.0.0",
            "narrative_stripped": True,
            "narrative_segments": [],
            "logical_core": "",
            "violations": [],
            "violation_count": 0,
            "pass": True,
            "note": "No text found in decision_context to audit.",
        }
