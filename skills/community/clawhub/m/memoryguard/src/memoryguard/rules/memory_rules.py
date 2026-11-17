"""Memory 治理表面规则（spec §2 治理表面3）。

检查记忆文件的: 来源、重复、矛盾、陈旧、PII、作用域、不可解释总结。
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from ..schema import AGR, AGRType, Dimension, Severity, Surface
from . import Rule, RuleContext, register_rule


# ---------------------------------------------------------------------------
# 规则9: 记忆文件陈旧（mtime 超过阈值）
# ---------------------------------------------------------------------------


@register_rule
class MemoryStale(Rule):
    rule_id = "memory.stale"
    dimension = Dimension.FRESHNESS
    surface = Surface.MEMORY
    severity = Severity.LOW
    description = "记忆文件长期未更新，可能已过时"
    why = "陈旧记忆可能引用已变更的代码或规则，误导 Agent 做出过时决策"
    positive_example = "记忆文件 mtime 超过 180 天"
    negative_example = "记忆文件在 30 天内有更新"
    verification = "manual"
    STALE_DAYS = 180

    def check(self, ctx: RuleContext) -> list:
        findings = []
        now = datetime.now(timezone.utc)
        for agr in ctx.memories():
            if not agr.mtime:
                continue
            try:
                mtime = datetime.fromisoformat(agr.mtime)
                age_days = (now - mtime).days
                if age_days > self.STALE_DAYS:
                    findings.append(
                        self.make_finding(
                            ctx, agr,
                            evidence=f"{agr.metadata.get('rel_path',agr.path)} 已 {age_days} 天未更新 (> {self.STALE_DAYS})",
                            impact="陈旧记忆可能引用已变更的内容，误导 Agent",
                            suggestion="复核该记忆是否仍有效，更新或删除",
                            confidence=0.7,
                            fixable=False,
                        )
                    )
            except (ValueError, TypeError):
                continue
        return findings


# ---------------------------------------------------------------------------
# 规则10: 记忆含 PII（简单模式匹配）
# ---------------------------------------------------------------------------


@register_rule
class MemoryPII(Rule):
    rule_id = "memory.pii_pattern"
    dimension = Dimension.SECURITY
    surface = Surface.MEMORY
    severity = Severity.HIGH
    description = "记忆文件可能含 PII（邮箱/手机号/API key 模式）"
    why = "记忆会被 Agent 加载进 Context，PII 可能通过日志或对话泄露"
    positive_example = "记忆含 API key 模式 AKIA... 或手机号 1xxxxxxxxxx"
    negative_example = "记忆只有技术内容，无个人或凭证信息"
    verification = "manual"
    PII_PATTERNS = [
        (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS Access Key"),
        (re.compile(r"ghp_[A-Za-z0-9]{36}"), "GitHub Token"),
        (re.compile(r"sk-[A-Za-z0-9]{20,}"), "OpenAI API Key"),
        (re.compile(r"\b1[3-9]\d{9}\b"), "中国手机号"),
        (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"), "邮箱"),
    ]

    def check(self, ctx: RuleContext) -> list:
        findings = []
        for agr in ctx.memories():
            content = ctx.read_content(agr)
            lines = content.splitlines()
            for i, line in enumerate(lines, 1):
                for pattern, label in self.PII_PATTERNS:
                    if pattern.search(line):
                        # 邮箱降级为 medium（可能是正常的作者联系方式）
                        sev = self.severity if label != "邮箱" else Severity.MEDIUM
                        findings.append(
                            self.make_finding(
                                ctx, agr,
                                evidence=f"line {i}: 可能含 {label}",
                                impact="记忆进入 Agent Context，PII 可能通过日志或对话泄露",
                                suggestion=f"移除 {label}，或替换为脱敏占位符",
                                confidence=0.8,
                                fixable=False,
                                span=(i, i),
                            )
                        )
                        break
        return findings


# ---------------------------------------------------------------------------
# 规则11: 记忆文件无来源标记
# ---------------------------------------------------------------------------


@register_rule
class MemoryNoSource(Rule):
    rule_id = "memory.no_source"
    dimension = Dimension.VISIBILITY
    surface = Surface.MEMORY
    severity = Severity.LOW
    description = "记忆文件无来源标记，无法追溯出处"
    why = "无来源的记忆无法验证可信度，Agent 可能基于不可追溯信息做决策"
    positive_example = "记忆文件无 frontmatter 或 source 字段"
    negative_example = "记忆文件有 source: conversation 或 source: docs/xxx.md"
    verification = "manual"

    def check(self, ctx: RuleContext) -> list:
        findings = []
        for agr in ctx.memories():
            content = ctx.read_content(agr)
            # 检查 frontmatter 或首行是否有 source
            has_source = bool(re.search(r"^source\s*:", content, re.MULTILINE))
            has_attribution = bool(re.search(r"(来源|source|attribution|author)\s*[:：]", content[:1024], re.IGNORECASE))
            if not has_source and not has_attribution:
                findings.append(
                    self.make_finding(
                        ctx, agr,
                        evidence=f"{agr.metadata.get('rel_path',agr.path)} 无来源标记",
                        impact="无来源的记忆无法验证可信度，Agent 可能基于不可追溯信息决策",
                        suggestion="添加 source 字段标明出处（如 conversation/docs/xxx.md）",
                        confidence=0.6,
                        fixable=True,
                    )
                )
        return findings


# ---------------------------------------------------------------------------
# 规则12: 记忆重复（多个记忆文件含高度相似段落）
# ---------------------------------------------------------------------------


@register_rule
class MemoryDuplicate(Rule):
    rule_id = "memory.duplicate"
    dimension = Dimension.CONSISTENCY
    surface = Surface.MEMORY
    severity = Severity.LOW
    description = "多个记忆文件含重复段落"
    why = "重复记忆浪费 Context 且可能在不同文件中逐渐分叉"
    positive_example = "两个记忆文件都记录了相同的项目结构说明"
    negative_example = "每个记忆只记录独特信息"
    verification = "manual"
    MIN_BLOCK_LINES = 3
    SIMILARITY_THRESHOLD = 0.85

    def check(self, ctx: RuleContext) -> list:
        findings = []
        mems = ctx.memories()
        if len(mems) < 2:
            return findings
        blocks: list[tuple[AGR, str]] = []
        for agr in mems:
            content = ctx.read_content(agr)
            for block in self._split_blocks(content):
                if len(block.splitlines()) >= self.MIN_BLOCK_LINES:
                    blocks.append((agr, block))
        for i in range(len(blocks)):
            for j in range(i + 1, len(blocks)):
                if blocks[i][0].id == blocks[j][0].id:
                    continue
                sim = self._similarity(blocks[i][1], blocks[j][1])
                if sim >= self.SIMILARITY_THRESHOLD:
                    findings.append(
                        self.make_finding(
                            ctx, blocks[i][0],
                            evidence=f"段落与 {blocks[j][0].metadata.get('rel_path',blocks[j][0].path)} 重复 (相似度 {sim:.0%})",
                            impact="重复记忆浪费 Context 且可能逐渐分叉",
                            suggestion="合并为单一来源，其余改为引用",
                            confidence=0.75,
                            fixable=False,
                        )
                    )
        return findings

    def _split_blocks(self, content: str) -> list[str]:
        blocks, current = [], []
        for line in content.splitlines():
            if line.strip():
                current.append(line)
            elif current:
                blocks.append("\n".join(current))
                current = []
        if current:
            blocks.append("\n".join(current))
        return blocks

    def _similarity(self, a: str, b: str) -> float:
        sa, sb = set(a.split()), set(b.split())
        if not sa or not sb:
            return 0.0
        return len(sa & sb) / len(sa | sb)
