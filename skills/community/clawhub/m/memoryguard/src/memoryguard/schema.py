"""Schema 契约模块（spec §3）。

所有字段为契约级，实现时不得无声偏离。
- AGR (Agent Governance Record): 每个被治理对象的统一记录
- Finding: 一条带位置/证据/影响/建议/置信度/验证方式的问题记录
- Report: 一次扫描的完整结果
- Plan / Change: 安全修复闭环的变更契约（spec §3.4）

设计选择:
- dataclass 而非 pydantic：首期零第三方依赖，纯标准库。
- 枚举用 str 子类，便于 JSON 序列化且保持可读。
- to_dict / from_dict 提供确定性序列化，不依赖 dataclasses.asdict
  以便后续对敏感字段做脱敏控制。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Iterable
import hashlib
import json


# ---------------------------------------------------------------------------
# 枚举（str 子类，JSON 友好）
# ---------------------------------------------------------------------------


class AGRType(str, Enum):
    INSTRUCTION = "instruction"
    SKILL = "skill"
    MEMORY = "memory"
    RAG_SOURCE = "rag_source"
    TOOL_CONFIG = "tool_config"
    RUN_EVIDENCE = "run_evidence"


class Scope(str, Enum):
    PROJECT = "project"
    USER = "user"
    GLOBAL = "global"


class Sensitivity(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RefRelation(str, Enum):
    DEFINES = "defines"
    CALLS = "calls"
    OVERRIDES = "overrides"
    CITES = "cites"
    DUPLICATES = "duplicates"
    CONFLICTS = "conflicts"


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Dimension(str, Enum):
    VISIBILITY = "visibility"
    CONSISTENCY = "consistency"
    EFFECTIVENESS = "effectiveness"
    SECURITY = "security"
    FRESHNESS = "freshness"
    MAINTAINABILITY = "maintainability"
    RECOVERABILITY = "recoverability"


class Surface(str, Enum):
    INSTRUCTION = "instruction"
    SKILL = "skill"
    MEMORY = "memory"
    RAG = "rag"
    TOOL = "tool"
    EVIDENCE = "evidence"


class ChangeStatus(str, Enum):
    APPLIED = "applied"
    VERIFIED = "verified"
    UNDONE = "undone"
    FAILED = "failed"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# ---------------------------------------------------------------------------
# Schema: AGR (spec §3.1)
# ---------------------------------------------------------------------------


@dataclass
class Ref:
    """AGR 之间的引用关系。"""

    to: str
    relation: RefRelation

    def to_dict(self) -> dict[str, Any]:
        return {"to": self.to, "relation": self.relation.value}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Ref":
        return cls(to=data["to"], relation=RefRelation(data["relation"]))


@dataclass
class AGR:
    """Agent Governance Record: 每个被治理对象的统一记录（spec §3.1）。"""

    id: str
    type: AGRType
    path: str
    scope: Scope = Scope.PROJECT
    source: str = ""
    hash: str = ""
    mtime: str = ""
    sensitivity: Sensitivity = Sensitivity.NONE
    refs: list[Ref] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "path": self.path,
            "scope": self.scope.value,
            "source": self.source,
            "hash": self.hash,
            "mtime": self.mtime,
            "sensitivity": self.sensitivity.value,
            "refs": [r.to_dict() for r in self.refs],
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AGR":
        return cls(
            id=data["id"],
            type=AGRType(data["type"]),
            path=data["path"],
            scope=Scope(data.get("scope", "project")),
            source=data.get("source", ""),
            hash=data.get("hash", ""),
            mtime=data.get("mtime", ""),
            sensitivity=Sensitivity(data.get("sensitivity", "none")),
            refs=[Ref.from_dict(r) for r in data.get("refs", [])],
            metadata=dict(data.get("metadata", {})),
        )

    @property
    def invisible_reason(self) -> str:
        """非空表示该对象无法读取或导出，必须显式显示为'不可见'。"""
        return str(self.metadata.get("invisible_reason", ""))


# ---------------------------------------------------------------------------
# Schema: Finding (spec §3.2)
# ---------------------------------------------------------------------------


@dataclass
class Location:
    """Finding 在源文件中的位置。"""

    agr_id: str
    path: str
    span: tuple[int, int] = (0, 0)

    def to_dict(self) -> dict[str, Any]:
        return {
            "agr_id": self.agr_id,
            "path": self.path,
            "span": [self.span[0], self.span[1]],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Location":
        span = data.get("span", [0, 0])
        return cls(
            agr_id=data["agr_id"],
            path=data["path"],
            span=(int(span[0]), int(span[1])),
        )


@dataclass
class Finding:
    """一条带证据的问题记录（spec §3.2）。

    必须包含: 位置、证据、为什么重要、建议、置信度、验证方式。
    """

    id: str
    rule_id: str
    severity: Severity
    dimension: Dimension
    surface: Surface
    location: Location
    evidence: str
    impact: str
    suggestion: str
    confidence: float = 0.0
    verification: str = "manual"
    fixable: bool = False
    related_findings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "rule_id": self.rule_id,
            "severity": self.severity.value,
            "dimension": self.dimension.value,
            "surface": self.surface.value,
            "location": self.location.to_dict(),
            "evidence": self.evidence,
            "impact": self.impact,
            "suggestion": self.suggestion,
            "confidence": self.confidence,
            "verification": self.verification,
            "fixable": self.fixable,
            "related_findings": list(self.related_findings),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Finding":
        return cls(
            id=data["id"],
            rule_id=data["rule_id"],
            severity=Severity(data["severity"]),
            dimension=Dimension(data["dimension"]),
            surface=Surface(data["surface"]),
            location=Location.from_dict(data["location"]),
            evidence=data.get("evidence", ""),
            impact=data.get("impact", ""),
            suggestion=data.get("suggestion", ""),
            confidence=float(data.get("confidence", 0.0)),
            verification=data.get("verification", "manual"),
            fixable=bool(data.get("fixable", False)),
            related_findings=list(data.get("related_findings", [])),
        )


# ---------------------------------------------------------------------------
# Schema: Report (spec §3.3)
# ---------------------------------------------------------------------------


@dataclass
class ConflictGroup:
    id: str
    members: list[str]
    evidence: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "members": list(self.members),
            "evidence": self.evidence,
        }


@dataclass
class ContextBudget:
    redundant_bytes: int = 0
    top_contributors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "redundant_bytes": self.redundant_bytes,
            "top_contributors": list(self.top_contributors),
        }


@dataclass
class Report:
    """一次扫描的完整结果（spec §3.3）。"""

    schema_version: str = "1.0"
    workspace: str = ""
    generated_at: str = ""
    duration_ms: int = 0
    health_score: float = 0.0
    objects: list[AGR] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    conflict_groups: list[ConflictGroup] = field(default_factory=list)
    context_budget: ContextBudget = field(default_factory=ContextBudget)
    # 不可见范围：必须显式记录，不能静默当作不存在（spec §2.2, §13 盲点5）
    invisible: list[dict[str, Any]] = field(default_factory=list)

    def summary(self) -> dict[str, Any]:
        """摘要：按严重度统计 Finding 数量 + 不可见对象数量。"""
        by_severity: dict[str, int] = {}
        for f in self.findings:
            by_severity[f.severity.value] = by_severity.get(f.severity.value, 0) + 1
        return {
            "object_count": len(self.objects),
            "finding_count_by_severity": by_severity,
            "invisible_count": len(self.invisible),
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "workspace": self.workspace,
            "generated_at": self.generated_at,
            "duration_ms": self.duration_ms,
            "health_score": self.health_score,
            "summary": self.summary(),
            "objects": [o.to_dict() for o in self.objects],
            "findings": [f.to_dict() for f in self.findings],
            "conflict_groups": [g.to_dict() for g in self.conflict_groups],
            "context_budget": self.context_budget.to_dict(),
            "invisible": list(self.invisible),
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Report":
        return cls(
            schema_version=data.get("schema_version", "1.0"),
            workspace=data.get("workspace", ""),
            generated_at=data.get("generated_at", ""),
            duration_ms=int(data.get("duration_ms", 0)),
            health_score=float(data.get("health_score", 0.0)),
            objects=[AGR.from_dict(o) for o in data.get("objects", [])],
            findings=[Finding.from_dict(f) for f in data.get("findings", [])],
            conflict_groups=[
                ConflictGroup(
                    id=g["id"],
                    members=list(g.get("members", [])),
                    evidence=g.get("evidence", ""),
                )
                for g in data.get("conflict_groups", [])
            ],
            context_budget=ContextBudget(
                redundant_bytes=int(data.get("context_budget", {}).get("redundant_bytes", 0)),
                top_contributors=list(data.get("context_budget", {}).get("top_contributors", [])),
            ),
            invisible=list(data.get("invisible", [])),
        )


# ---------------------------------------------------------------------------
# Schema: Plan / Change (spec §3.4)
# ---------------------------------------------------------------------------


@dataclass
class Patch:
    """单个文件的最小补丁。"""

    path: str
    operation: str  # replace | insert | delete | move
    before_hash: str
    diff: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "operation": self.operation,
            "before_hash": self.before_hash,
            "diff": self.diff,
        }


@dataclass
class Plan:
    """修复计划：生成 Diff，不写文件（spec §3.4, §9）。"""

    plan_id: str
    finding_ids: list[str]
    intent: str
    risk_level: RiskLevel
    patches: list[Patch]
    created_at: str = ""
    preconditions: list[str] = field(default_factory=list)
    verification: list[str] = field(default_factory=list)
    requires_approval: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "finding_ids": list(self.finding_ids),
            "created_at": self.created_at,
            "intent": self.intent,
            "risk_level": self.risk_level.value,
            "preconditions": list(self.preconditions),
            "patches": [p.to_dict() for p in self.patches],
            "verification": list(self.verification),
            "requires_approval": self.requires_approval,
        }


@dataclass
class Change:
    """一次 apply 的结果记录，支撑 verify/undo（spec §3.4, §9）。"""

    change_id: str
    plan_id: str
    applied_at: str
    backup_paths: list[str]
    changed_paths: list[str]
    status: ChangeStatus
    verify_report: str = ""
    undo_plan: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "change_id": self.change_id,
            "plan_id": self.plan_id,
            "applied_at": self.applied_at,
            "backup_paths": list(self.backup_paths),
            "changed_paths": list(self.changed_paths),
            "verify_report": self.verify_report,
            "undo_plan": self.undo_plan,
            "status": self.status.value,
        }


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------


def now_iso() -> str:
    """UTC ISO8601 时间戳。"""
    return datetime.now(timezone.utc).isoformat()


def sha256_text(text: str) -> str:
    """对文本内容计算 SHA256，用于 AGR.hash 和 Patch.before_hash。"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    """对文件原始字节计算 SHA256，避免文本模式 CRLF 归一化导致 hash 不稳定。"""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(prefix: str, *parts: Any) -> str:
    """基于内容生成稳定 ID，避免随机串导致重扫时 ID 漂移。"""
    raw = "|".join(str(p) for p in parts)
    return f"{prefix}-{sha256_text(raw)[:12]}"
