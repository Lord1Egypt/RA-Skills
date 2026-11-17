"""Skill 治理表面规则（spec §2 治理表面2）。

检查 SKILL.md 的: 规范、触发描述、依赖、权限、危险命令、引用缺失、重名遮蔽。
"""

from __future__ import annotations

import re
from pathlib import Path

from ..schema import AGR, AGRType, Dimension, Severity, Surface
from . import Rule, RuleContext, register_rule


# ---------------------------------------------------------------------------
# 规则5: SKILL.md 缺少 frontmatter 或 name 字段
# ---------------------------------------------------------------------------


@register_rule
class SkillMissingFrontmatter(Rule):
    rule_id = "skill.missing_frontmatter"
    dimension = Dimension.MAINTAINABILITY
    surface = Surface.SKILL
    severity = Severity.MEDIUM
    description = "SKILL.md 缺少 YAML frontmatter 或 name 字段"
    why = "frontmatter 是 Agent Skills 规范要求，缺失会导致宿主无法发现或加载 Skill"
    positive_example = "SKILL.md 无 --- frontmatter ---"
    negative_example = "SKILL.md 以 --- name: xxx --- 开头"
    verification = "manual"

    def check(self, ctx: RuleContext) -> list:
        findings = []
        for agr in ctx.skills():
            if not agr.path.endswith("SKILL.md"):
                continue
            content = ctx.read_content(agr)
            if not content.startswith("---"):
                findings.append(self._finding(ctx, agr, "缺少 YAML frontmatter"))
                continue
            # 提取 frontmatter
            parts = content.split("---", 2)
            if len(parts) < 3:
                findings.append(self._finding(ctx, agr, "frontmatter 格式不完整"))
                continue
            fm = parts[1]
            if not re.search(r"^name\s*:", fm, re.MULTILINE):
                findings.append(self._finding(ctx, agr, "frontmatter 缺少 name 字段"))
            if not re.search(r"^description\s*:", fm, re.MULTILINE):
                findings.append(self._finding(ctx, agr, "frontmatter 缺少 description 字段"))
        return findings

    def _finding(self, ctx, agr, msg):
        return self.make_finding(
            ctx, agr,
            evidence=msg,
            impact="宿主可能无法发现或正确加载该 Skill",
            suggestion="补全 frontmatter，至少含 name 和 description",
            confidence=0.9,
            fixable=True,
            span=(1, 5),
        )


# ---------------------------------------------------------------------------
# 规则6: Skill 脚本含危险命令
# ---------------------------------------------------------------------------


@register_rule
class SkillDangerousCommand(Rule):
    rule_id = "skill.dangerous_command"
    dimension = Dimension.SECURITY
    surface = Surface.SKILL
    severity = Severity.HIGH
    description = "Skill 脚本含写文件、联网或执行任意命令的危险操作"
    why = "Skill 脚本在 Agent 上下文执行，危险命令可能损坏用户文件或泄露数据"
    positive_example = "脚本含 rm -rf / curl | sh subprocess.call(shell=True)"
    negative_example = "脚本只做只读分析，无写操作、无网络"
    verification = "manual"
    DANGEROUS_PATTERNS = [
        (re.compile(r"\brm\s+-rf\b"), "rm -rf 危险删除"),
        (re.compile(r"\bcurl\b.*\|\s*(sh|bash)"), "curl 管道执行远程脚本"),
        (re.compile(r"\bwget\b.*\|\s*(sh|bash)"), "wget 管道执行远程脚本"),
        (re.compile(r"subprocess\.(call|run|Popen)\(.*shell\s*=\s*True"), "shell=True 命令注入风险"),
        (re.compile(r"\bopen\([^)]*['\"]w['\"]"), "文件写操作"),
        (re.compile(r"\bos\.system\b"), "os.system 命令执行"),
        (re.compile(r"\beval\b\("), "eval 动态执行"),
    ]

    def check(self, ctx: RuleContext) -> list:
        findings = []
        for agr in ctx.skills():
            if not agr.path.endswith((".py", ".sh", ".ps1")):
                continue
            content = ctx.read_content(agr)
            lines = content.splitlines()
            for i, line in enumerate(lines, 1):
                for pattern, label in self.DANGEROUS_PATTERNS:
                    if pattern.search(line):
                        findings.append(
                            self.make_finding(
                                ctx, agr,
                                evidence=f"line {i}: {label} -- {line.strip()[:100]}",
                                impact="Skill 脚本在 Agent 上下文执行，危险命令可能损坏文件或泄露数据",
                                suggestion="改为只读操作，或明确声明权限并要求用户批准",
                                confidence=0.9,
                                fixable=False,
                                span=(i, i),
                            )
                        )
                        break
        return findings


# ---------------------------------------------------------------------------
# 规则7: Skill 未固定依赖（脚本 import 第三方但无 requirements）
# ---------------------------------------------------------------------------


@register_rule
class SkillUnpinnedDeps(Rule):
    rule_id = "skill.unpinned_deps"
    dimension = Dimension.SECURITY
    surface = Surface.SKILL
    severity = Severity.LOW
    description = "Skill 脚本 import 第三方包但目录无 requirements.txt"
    why = "未固定依赖会导致不同环境行为不一致，且增加供应链风险"
    positive_example = "脚本 import requests 但同目录无 requirements.txt"
    negative_example = "脚本只 import 标准库，或有 requirements.txt 固定版本"
    verification = "manual"

    def check(self, ctx: RuleContext) -> list:
        findings = []
        skill_agrs = [a for a in ctx.skills() if a.path.endswith(".py")]
        if not skill_agrs:
            return findings
        # 检查同目录有无 requirements.txt
        skill_dirs = {Path(a.path).parent for a in skill_agrs}
        for agr in skill_agrs:
            content = ctx.read_content(agr)
            imports = re.findall(r"^\s*(?:import|from)\s+([a-zA-Z0-9_]+)", content, re.MULTILINE)
            third_party = [imp for imp in imports if imp not in self._STDLIB]
            if not third_party:
                continue
            skill_dir = Path(agr.path).parent
            has_reqs = (skill_dir / "requirements.txt").exists() or (skill_dir / "pyproject.toml").exists()
            if not has_reqs:
                findings.append(
                    self.make_finding(
                        ctx, agr,
                        evidence=f"import 第三方包 {third_party[:3]} 但无 requirements.txt",
                        impact="不同环境行为不一致，增加供应链风险",
                        suggestion="添加 requirements.txt 并固定版本",
                        confidence=0.8,
                        fixable=False,
                    )
                )
        return findings

    # 常见标准库模块（保守子集）
    _STDLIB = {
        "os", "sys", "re", "json", "pathlib", "datetime", "hashlib", "argparse",
        "subprocess", "typing", "dataclasses", "enum", "abc", "io", "base64",
        "collections", "functools", "itertools", "logging", "tempfile", "shutil",
        "glob", "html", "http", "socket", "threading", "multiprocessing",
        "urllib", "email", "csv", "math", "random", "time", "copy", "pprint",
        "textwrap", "string", "unicodedata", "uuid", "secrets", "warnings",
    }


# ---------------------------------------------------------------------------
# 规则8: Skill 重名遮蔽（多个 Skill 同名）
# ---------------------------------------------------------------------------


@register_rule
class SkillNameShadow(Rule):
    rule_id = "skill.name_shadow"
    dimension = Dimension.CONSISTENCY
    surface = Surface.SKILL
    severity = Severity.MEDIUM
    description = "多个 Skill 同名，可能互相遮蔽"
    why = "同名 Skill 会让宿主加载不确定的那个，导致行为不一致"
    positive_example = "两个目录都有 name: graphify 的 SKILL.md"
    negative_example = "每个 Skill name 唯一"
    verification = "manual"

    def check(self, ctx: RuleContext) -> list:
        findings = []
        names: dict[str, list[AGR]] = {}
        for agr in ctx.skills():
            if not agr.path.endswith("SKILL.md"):
                continue
            content = ctx.read_content(agr)
            name = self._extract_name(content)
            if name:
                names.setdefault(name, []).append(agr)
        for name, agrs in names.items():
            if len(agrs) > 1:
                for agr in agrs:
                    findings.append(
                        self.make_finding(
                            ctx, agr,
                            evidence=f"Skill name '{name}' 出现在 {len(agrs)} 个 SKILL.md，可能互相遮蔽",
                            impact="宿主加载不确定的 Skill，行为不一致",
                            suggestion="重命名其中一个 Skill",
                            confidence=0.9,
                            fixable=False,
                        )
                    )
        return findings

    def _extract_name(self, content: str) -> str:
        if not content.startswith("---"):
            return ""
        parts = content.split("---", 2)
        if len(parts) < 3:
            return ""
        m = re.search(r"^name\s*:\s*(.+)$", parts[1], re.MULTILINE)
        return m.group(1).strip().strip("\"'") if m else ""
