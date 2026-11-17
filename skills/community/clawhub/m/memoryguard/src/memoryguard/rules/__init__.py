"""规则引擎框架（spec §8）。

每条规则必须包含: rule_id, dimension, surface, severity, description, why,
positive_example, negative_example, verification, 以及一个 check(context) -> list[Finding] 方法。

设计:
- Rule 是抽象基类，子类实现 check。
- RuleRegistry 全局注册表，支持按 surface/dimension 查询。
- RuleContext 把 AGR 列表组织成便于跨表面分析的结构。
- 确定性优先：纯文本/结构分析，不调 LLM。语义矛盾留待后续可选模块。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

from ..schema import (
    AGR,
    AGRType,
    Dimension,
    Finding,
    Location,
    RefRelation,
    Severity,
    Surface,
    stable_id,
)


# ---------------------------------------------------------------------------
# 规则上下文
# ---------------------------------------------------------------------------


@dataclass
class RuleContext:
    """规则执行上下文：把 AGR 列表组织成便于查询的结构。"""

    agrs: list[AGR]
    _by_type: dict[AGRType, list[AGR]] = field(default_factory=dict, init=False)
    _by_id: dict[str, AGR] = field(default_factory=dict, init=False)
    _content_cache: dict[str, str] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        for agr in self.agrs:
            self._by_type.setdefault(agr.type, []).append(agr)
            self._by_id[agr.id] = agr

    def by_type(self, t: AGRType) -> list[AGR]:
        return self._by_type.get(t, [])

    def get(self, agr_id: str) -> AGR | None:
        return self._by_id.get(agr_id)

    def instructions(self) -> list[AGR]:
        return self.by_type(AGRType.INSTRUCTION)

    def skills(self) -> list[AGR]:
        return self.by_type(AGRType.SKILL)

    def memories(self) -> list[AGR]:
        return self.by_type(AGRType.MEMORY)

    def rags(self) -> list[AGR]:
        return self.by_type(AGRType.RAG_SOURCE)

    def read_content(self, agr: AGR) -> str:
        """读取 AGR 对应文件内容（带缓存）。失败返回空串。"""
        if agr.id in self._content_cache:
            return self._content_cache[agr.id]
        try:
            content = Path(agr.path).read_text(encoding="utf-8", errors="replace")
        except OSError:
            content = ""
        self._content_cache[agr.id] = content
        return content


# ---------------------------------------------------------------------------
# 规则基类
# ---------------------------------------------------------------------------


class Rule(ABC):
    """规则抽象基类（spec §8.1）。

    每条规则必须声明: 维度、表面、严重度、为什么重要、正反例、验证方式。
    """

    rule_id: str = ""
    dimension: Dimension = Dimension.VISIBILITY
    surface: Surface = Surface.INSTRUCTION
    severity: Severity = Severity.INFO
    description: str = ""
    why: str = ""
    positive_example: str = ""  # 触发规则的样例
    negative_example: str = ""  # 不触发规则的样例
    verification: str = "manual"

    @abstractmethod
    def check(self, ctx: RuleContext) -> list[Finding]:
        """执行规则，返回 Finding 列表。纯只读，无副作用。"""
        ...

    def make_finding(
        self,
        ctx: RuleContext,
        agr: AGR,
        evidence: str,
        impact: str,
        suggestion: str,
        *,
        confidence: float = 0.9,
        fixable: bool = False,
        span: tuple[int, int] = (0, 0),
    ) -> Finding:
        """构造 Finding 的便捷方法，自动填入 rule_id/dimension/surface 等。"""
        return Finding(
            id=stable_id("find", self.rule_id, agr.id, evidence[:64]),
            rule_id=self.rule_id,
            severity=self.severity,
            dimension=self.dimension,
            surface=self.surface,
            location=Location(agr_id=agr.id, path=agr.path, span=span),
            evidence=evidence[:500],  # 截断，避免报告膨胀
            impact=impact,
            suggestion=suggestion,
            confidence=confidence,
            verification=self.verification,
            fixable=fixable,
        )


# ---------------------------------------------------------------------------
# 注册表
# ---------------------------------------------------------------------------


class RuleRegistry:
    """规则注册表。支持按 surface/dimension 查询、注册、列出。"""

    def __init__(self) -> None:
        self._rules: dict[str, Rule] = {}

    def register(self, rule: Rule) -> Rule:
        if not rule.rule_id:
            raise ValueError(f"rule {rule.__class__.__name__} has no rule_id")
        if rule.rule_id in self._rules:
            raise ValueError(f"duplicate rule_id: {rule.rule_id}")
        self._rules[rule.rule_id] = rule
        return rule

    def get(self, rule_id: str) -> Rule | None:
        return self._rules.get(rule_id)

    def all(self) -> list[Rule]:
        return list(self._rules.values())

    def by_surface(self, surface: Surface) -> list[Rule]:
        return [r for r in self._rules.values() if r.surface == surface]

    def by_dimension(self, dim: Dimension) -> list[Rule]:
        return [r for r in self._rules.values() if r.dimension == dim]

    def __len__(self) -> int:
        return len(self._rules)


# 全局默认注册表
default_registry = RuleRegistry()


def register_rule(rule_cls: type[Rule]) -> type[Rule]:
    """装饰器：实例化并注册规则到 default_registry。"""
    default_registry.register(rule_cls())
    return rule_cls


def run_rules(ctx: RuleContext, registry: RuleRegistry | None = None) -> list[Finding]:
    """执行所有规则，返回合并后的 Finding 列表。"""
    reg = registry or default_registry
    findings: list[Finding] = []
    for rule in reg.all():
        try:
            findings.extend(rule.check(ctx))
        except Exception as e:
            # 规则失败不应中断整体扫描；记入 invisible 待后续处理
            import sys

            print(f"warning: rule {rule.rule_id} failed: {e}", file=sys.stderr)
    return findings
