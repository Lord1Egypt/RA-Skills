"""Instruction 治理表面规则（spec §2 治理表面1）。

检查 AGENTS.md/CLAUDE.md 等指令文件的: 冲突、重复、层级覆盖、过长、模糊规则、失效引用。
"""

from __future__ import annotations

import re
from pathlib import Path

from ..schema import AGR, AGRType, Dimension, RefRelation, Severity, Surface
from . import Rule, RuleContext, register_rule


# ---------------------------------------------------------------------------
# 规则1: 指令文件过长
# ---------------------------------------------------------------------------


@register_rule
class InstructionTooLong(Rule):
    rule_id = "instruction.too_long"
    dimension = Dimension.EFFECTIVENESS
    surface = Surface.INSTRUCTION
    severity = Severity.MEDIUM
    description = "指令文件过长，可能浪费 Agent Context 预算"
    why = "过长的指令会占用有限的 Context 窗口，降低 Agent 对实际任务内容的注意力"
    positive_example = "AGENTS.md 超过 500 行"
    negative_example = "AGENTS.md 100 行以内，聚焦核心规则"
    verification = "manual"
    THRESHOLD_LINES = 500

    def check(self, ctx: RuleContext) -> list:
        findings = []
        for agr in ctx.instructions():
            content = ctx.read_content(agr)
            lines = content.count("\n") + 1
            if lines > self.THRESHOLD_LINES:
                findings.append(
                    self.make_finding(
                        ctx, agr,
                        evidence=f"{agr.metadata.get('rel_path', agr.path)} has {lines} lines (> {self.THRESHOLD_LINES})",
                        impact="过长的指令文件占用 Context 预算，降低 Agent 对任务内容的注意力",
                        suggestion=f"拆分为多个聚焦的规则文件，或精简到 {self.THRESHOLD_LINES} 行以内",
                        confidence=0.95,
                        fixable=False,
                        span=(1, lines),
                    )
                )
        return findings


# ---------------------------------------------------------------------------
# 规则2: 模糊规则（含"尽量""可能""适当"等不确定词）
# ---------------------------------------------------------------------------


@register_rule
class InstructionVague(Rule):
    rule_id = "instruction.vague_terms"
    dimension = Dimension.MAINTAINABILITY
    surface = Surface.INSTRUCTION
    severity = Severity.LOW
    description = "指令含模糊术语，Agent 难以确定性执行"
    why = "模糊指令让 Agent 在不同上下文产生不一致行为，且无法验证是否遵守"
    positive_example = "代码应尽量保持简洁"
    negative_example = "函数体不超过 50 行，嵌套不超过 3 层"
    verification = "manual"
    VAGUE_TERMS = ("尽量", "尽可能", "适当", "合理", "必要时", "酌情", "差不多", "大概")

    def check(self, ctx: RuleContext) -> list:
        findings = []
        for agr in ctx.instructions():
            content = ctx.read_content(agr)
            lines = content.splitlines()
            for i, line in enumerate(lines, 1):
                for term in self.VAGUE_TERMS:
                    if term in line:
                        findings.append(
                            self.make_finding(
                                ctx, agr,
                                evidence=f"line {i}: {line.strip()[:120]} (含模糊词 '{term}')",
                                impact="模糊指令让 Agent 行为不确定，无法验证是否遵守",
                                suggestion=f"用可量化的标准替换 '{term}'，如具体数值或明确条件",
                                confidence=0.7,
                                fixable=False,
                                span=(i, i),
                            )
                        )
                        break  # 每行只报一次
        return findings


# ---------------------------------------------------------------------------
# 规则3: 失效引用（引用的文件路径不存在）
# ---------------------------------------------------------------------------


@register_rule
class InstructionBrokenRef(Rule):
    rule_id = "instruction.broken_ref"
    dimension = Dimension.MAINTAINABILITY
    surface = Surface.INSTRUCTION
    severity = Severity.MEDIUM
    description = "指令引用的文件路径不存在"
    why = "失效引用让 Agent 无法加载依赖规则或配置，可能导致部分治理规则被静默跳过"
    positive_example = "遵循 `.agent/PREFERENCES.md` 但该文件已删除"
    negative_example = "所有引用路径都存在且可读"
    verification = "manual"
    # 匹配 markdown 链接和反引号路径
    REF_PATTERN = re.compile(r"`?(\.[a-zA-Z0-9_\-/]+\.[a-zA-Z]+)`?")

    def check(self, ctx: RuleContext) -> list:
        findings = []
        workspace = ctx.agrs[0].path if ctx.agrs else ""
        # 推断工作区根：取第一个 AGR 路径的父目录上溯找
        ws_root = self._guess_workspace_root(ctx)
        for agr in ctx.instructions():
            content = ctx.read_content(agr)
            lines = content.splitlines()
            for i, line in enumerate(lines, 1):
                for match in self.REF_PATTERN.finditer(line):
                    ref_path = match.group(1)
                    if ws_root:
                        target = ws_root / ref_path
                        if not target.exists():
                            findings.append(
                                self.make_finding(
                                    ctx, agr,
                                    evidence=f"line {i}: 引用 '{ref_path}' 不存在",
                                    impact="Agent 无法加载该依赖，相关规则可能被静默跳过",
                                    suggestion=f"删除该引用或恢复文件 {ref_path}",
                                    confidence=0.85,
                                    fixable=False,
                                    span=(i, i),
                                )
                            )
        return findings

    def _guess_workspace_root(self, ctx: RuleContext) -> Path | None:
        for agr in ctx.agrs:
            p = Path(agr.path).parent
            while p != p.parent:
                if (p / "AGENTS.md").exists() or (p / ".agents").exists():
                    return p
                p = p.parent
        return None


# ---------------------------------------------------------------------------
# 规则4: 重复规则（多个指令文件含高度相似段落）
# ---------------------------------------------------------------------------


@register_rule
class InstructionDuplicate(Rule):
    rule_id = "instruction.duplicate_section"
    dimension = Dimension.CONSISTENCY
    surface = Surface.INSTRUCTION
    severity = Severity.LOW
    description = "多个指令文件含重复段落"
    why = "重复规则浪费 Context 且在更新时容易不同步，导致 Agent 行为不一致"
    positive_example = "AGENTS.md 和 CLAUDE.md 都写了相同的代码风格规则"
    negative_example = "每个规则只在一处定义，其余文件引用"
    verification = "manual"
    MIN_BLOCK_LINES = 3
    SIMILARITY_THRESHOLD = 0.8

    def check(self, ctx: RuleContext) -> list:
        findings = []
        instrs = ctx.instructions()
        if len(instrs) < 2:
            return findings
        # 提取每个文件的段落（连续非空行）
        blocks: list[tuple[AGR, str]] = []
        for agr in instrs:
            content = ctx.read_content(agr)
            for block in self._split_blocks(content):
                if len(block.splitlines()) >= self.MIN_BLOCK_LINES:
                    blocks.append((agr, block))
        # 两两比较
        for i in range(len(blocks)):
            for j in range(i + 1, len(blocks)):
                agr_i, block_i = blocks[i]
                agr_j, block_j = blocks[j]
                if agr_i.id == agr_j.id:
                    continue
                sim = self._similarity(block_i, block_j)
                if sim >= self.SIMILARITY_THRESHOLD:
                    findings.append(
                        self.make_finding(
                            ctx, agr_i,
                            evidence=f"段落与 {agr_j.metadata.get('rel_path', agr_j.path)} 重复 (相似度 {sim:.0%})",
                            impact="重复规则浪费 Context 且更新时易不同步",
                            suggestion="只在一处定义，另一处改为引用",
                            confidence=0.8,
                            fixable=False,
                        )
                    )
        return findings

    def _split_blocks(self, content: str) -> list[str]:
        blocks = []
        current = []
        for line in content.splitlines():
            if line.strip():
                current.append(line)
            else:
                if current:
                    blocks.append("\n".join(current))
                    current = []
        if current:
            blocks.append("\n".join(current))
        return blocks

    def _similarity(self, a: str, b: str) -> float:
        """简单 Jaccard 相似度：按行分词。"""
        set_a = set(a.split())
        set_b = set(b.split())
        if not set_a or not set_b:
            return 0.0
        return len(set_a & set_b) / len(set_a | set_b)
