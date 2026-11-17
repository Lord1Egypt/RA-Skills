"""Local RAG 治理表面规则（spec §2 治理表面4）。

检查本地 RAG 源的: 文档质量、冲突、重复、过期、敏感、坏链接、缺元数据、Chunk 检查。
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from ..schema import AGR, AGRType, Dimension, Severity, Surface
from . import Rule, RuleContext, register_rule


# ---------------------------------------------------------------------------
# 规则13: RAG 文档缺元数据（无标题、无日期、无所有者）
# ---------------------------------------------------------------------------


@register_rule
class RAGMissingMetadata(Rule):
    rule_id = "rag.missing_metadata"
    dimension = Dimension.MAINTAINABILITY
    surface = Surface.RAG
    severity = Severity.LOW
    description = "RAG 文档缺少标题或元数据"
    why = "无标题的文档在检索时难以区分，Agent 无法判断文档用途和时效性"
    positive_example = "文档以普通段落开头，无 # 标题"
    negative_example = "文档以 # 标题 开头，含日期和所有者"
    verification = "manual"

    def check(self, ctx: RuleContext) -> list:
        findings = []
        for agr in ctx.rags():
            content = ctx.read_content(agr)
            if not content.strip():
                continue
            # 首个非空行应为标题
            first_line = next((l for l in content.splitlines() if l.strip()), "")
            if not first_line.startswith("#"):
                findings.append(
                    self.make_finding(
                        ctx, agr,
                        evidence=f"首行非标题: {first_line[:60]}",
                        impact="无标题的文档在检索时难以区分，Agent 无法判断用途",
                        suggestion="在文档开头添加 # 标题",
                        confidence=0.7,
                        fixable=True,
                        span=(1, 1),
                    )
                )
        return findings


# ---------------------------------------------------------------------------
# 规则14: RAG 文档含坏链接
# ---------------------------------------------------------------------------


@register_rule
class RAGBrokenLink(Rule):
    rule_id = "rag.broken_link"
    dimension = Dimension.MAINTAINABILITY
    surface = Surface.RAG
    severity = Severity.MEDIUM
    description = "RAG 文档含指向不存在文件的相对链接"
    why = "坏链接让 Agent 无法获取引用的上下文，可能基于不完整信息做决策"
    positive_example = "文档链接 [xxx](./missing.md) 但 missing.md 不存在"
    negative_example = "所有相对链接都指向存在的文件"
    verification = "manual"
    LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

    def check(self, ctx: RuleContext) -> list:
        findings = []
        for agr in ctx.rags():
            content = ctx.read_content(agr)
            lines = content.splitlines()
            agr_dir = agr.path.rsplit("\\", 1)[0] if "\\" in agr.path else agr.path.rsplit("/", 1)[0]
            from pathlib import Path
            base = Path(agr.path).parent
            for i, line in enumerate(lines, 1):
                for match in self.LINK_PATTERN.finditer(line):
                    link = match.group(1)
                    if link.startswith(("http://", "https://", "mailto:", "#")):
                        continue
                    target = (base / link).resolve()
                    if not target.exists():
                        findings.append(
                            self.make_finding(
                                ctx, agr,
                                evidence=f"line {i}: 坏链接 {link}",
                                impact="Agent 无法获取引用的上下文，基于不完整信息决策",
                                suggestion=f"修复或删除链接 {link}",
                                confidence=0.85,
                                fixable=False,
                                span=(i, i),
                            )
                        )
        return findings


# ---------------------------------------------------------------------------
# 规则15: RAG 文档过大（可能需要分 Chunk）
# ---------------------------------------------------------------------------


@register_rule
class RAGTooLarge(Rule):
    rule_id = "rag.too_large"
    dimension = Dimension.EFFECTIVENESS
    surface = Surface.RAG
    severity = Severity.MEDIUM
    description = "RAG 文档过大，单次检索可能超出 Context 预算"
    why = "过大的文档被整体检索时会挤占 Context，降低 Agent 对其他信息的注意力"
    positive_example = "单个 RAG 文档超过 2000 行"
    negative_example = "文档控制在 500 行以内，或已分 Chunk"
    verification = "manual"
    THRESHOLD_LINES = 2000

    def check(self, ctx: RuleContext) -> list:
        findings = []
        for agr in ctx.rags():
            content = ctx.read_content(agr)
            lines = content.count("\n") + 1
            if lines > self.THRESHOLD_LINES:
                findings.append(
                    self.make_finding(
                        ctx, agr,
                        evidence=f"{agr.metadata.get('rel_path',agr.path)} 有 {lines} 行 (> {self.THRESHOLD_LINES})",
                        impact="整体检索时挤占 Context，降低 Agent 注意力",
                        suggestion="拆分为多个聚焦的小文档，或建立 Chunk 索引",
                        confidence=0.9,
                        fixable=False,
                        span=(1, lines),
                    )
                )
        return findings


# ---------------------------------------------------------------------------
# 规则16: RAG 文档含敏感信息模式
# ---------------------------------------------------------------------------


@register_rule
class RAGSensitiveContent(Rule):
    rule_id = "rag.sensitive_content"
    dimension = Dimension.SECURITY
    surface = Surface.RAG
    severity = Severity.HIGH
    description = "RAG 文档可能含凭证或密钥"
    why = "RAG 内容会被检索进 Context，密钥可能通过日志或对话泄露"
    positive_example = "文档含 BEGIN PRIVATE KEY 或 AKIA 模式"
    negative_example = "文档只有技术内容，无凭证"
    verification = "manual"
    SENSITIVE_PATTERNS = [
        (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "私钥"),
        (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS Access Key"),
        (re.compile(r"ghp_[A-Za-z0-9]{36}"), "GitHub Token"),
        (re.compile(r"sk-[A-Za-z0-9]{20,}"), "OpenAI API Key"),
    ]

    def check(self, ctx: RuleContext) -> list:
        findings = []
        for agr in ctx.rags():
            content = ctx.read_content(agr)
            lines = content.splitlines()
            for i, line in enumerate(lines, 1):
                for pattern, label in self.SENSITIVE_PATTERNS:
                    if pattern.search(line):
                        findings.append(
                            self.make_finding(
                                ctx, agr,
                                evidence=f"line {i}: 可能含 {label}",
                                impact="RAG 内容进入 Context，凭证可能通过日志或对话泄露",
                                suggestion=f"移除 {label}，或移到 .env 并在文档中引用变量名",
                                confidence=0.9,
                                fixable=False,
                                span=(i, i),
                            )
                        )
                        break
        return findings


# ---------------------------------------------------------------------------
# 规则17: RAG 文档空内容
# ---------------------------------------------------------------------------


@register_rule
class RAGEmpty(Rule):
    rule_id = "rag.empty"
    dimension = Dimension.EFFECTIVENESS
    surface = Surface.RAG
    severity = Severity.MEDIUM
    description = "RAG 文档为空或只有空白"
    why = "空文档浪费检索预算，且让 Agent 误以为该主题无可用信息"
    positive_example = "文档只有空行或标题无内容"
    negative_example = "文档有实质内容"
    verification = "manual"

    def check(self, ctx: RuleContext) -> list:
        findings = []
        for agr in ctx.rags():
            content = ctx.read_content(agr)
            if not content.strip():
                findings.append(
                    self.make_finding(
                        ctx, agr,
                        evidence="文档内容为空",
                        impact="浪费检索预算，让 Agent 误以为该主题无可用信息",
                        suggestion="填充内容或删除该空文档",
                        confidence=0.95,
                        fixable=True,
                    )
                )
            elif len(content.strip()) < 20:
                findings.append(
                    self.make_finding(
                        ctx, agr,
                        evidence=f"文档内容过少: {content.strip()[:30]}",
                        impact="内容过少难以提供有效上下文",
                        suggestion="补充内容或合并到其他文档",
                        confidence=0.7,
                        fixable=True,
                    )
                )
        return findings


# ---------------------------------------------------------------------------
# 规则18: 跨表面冲突（指令与 RAG 描述矛盾）
# ---------------------------------------------------------------------------


@register_rule
class CrossSurfaceConflict(Rule):
    rule_id = "cross.conflict_instruction_rag"
    dimension = Dimension.CONSISTENCY
    surface = Surface.RAG
    severity = Severity.HIGH
    description = "指令文件与 RAG 文档含矛盾的技术声明"
    why = "跨表面矛盾让 Agent 行为不可判定：遵守指令则违背 RAG，反之亦然"
    positive_example = "AGENTS.md 要求 Python 3.10+，RAG 文档说支持 3.8"
    negative_example = "指令与 RAG 对技术要求的描述一致"
    verification = "manual"
    # 简化版：检测版本号矛盾模式
    VERSION_PATTERN = re.compile(r"(Python|Node|Go| Rust)\s*(\d+\.\d+)")

    def check(self, ctx: RuleContext) -> list:
        findings = []
        instrs = ctx.instructions()
        rags = ctx.rags()
        if not instrs or not rags:
            return findings
        # 收集指令中的版本声明
        instr_versions: dict[str, str] = {}
        for agr in instrs:
            content = ctx.read_content(agr)
            for m in self.VERSION_PATTERN.finditer(content):
                instr_versions[m.group(1).lower()] = m.group(2)
        if not instr_versions:
            return findings
        # 在 RAG 中找矛盾
        for agr in rags:
            content = ctx.read_content(agr)
            for m in self.VERSION_PATTERN.finditer(content):
                lang = m.group(1).lower()
                rag_ver = m.group(2)
                if lang in instr_versions and instr_versions[lang] != rag_ver:
                    findings.append(
                        self.make_finding(
                            ctx, agr,
                            evidence=f"{lang} 版本矛盾: 指令要求 {instr_versions[lang]}，RAG 文档说 {rag_ver}",
                            impact="跨表面矛盾让 Agent 行为不可判定",
                            suggestion="统一版本声明，以指令为准更新 RAG 文档",
                            confidence=0.85,
                            fixable=True,
                        )
                    )
        return findings
