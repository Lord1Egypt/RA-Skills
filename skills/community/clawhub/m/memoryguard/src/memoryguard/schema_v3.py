"""v3 数据模型（spec §3.2-§3.7）。

v3 相对 v2.1 的核心变化：
- 新增 SourceRoot/CoverageLedger/Memory IR/BuildManifest/ReleaseChange
- 保留 v2.1 的 AGR/Finding/Plan/Change（规则引擎兼容）
- 神经图降级为纯投影（不在此处定义，见 projection.py）

设计原则：
- 稳定 ID：hash(source_root_id + normalized_relative_path) 等，禁止用扫描顺序整数 ID
- Provenance 必须保留：每条 MemoryRecord 至少一个可定位来源
- 去重只生成候选组，不自动删除
- 完整性可证明：BuildManifest 必须满足五个完整性条件
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
import hashlib
import json


# ---------------------------------------------------------------------------
# 枚举
# ---------------------------------------------------------------------------


class SourceRootType(str, Enum):
    """SourceRoot 类型（spec §3.2）。"""
    PROJECT_DIRECTORY = "project_directory"
    SELECTED_DIRECTORY = "selected_directory"
    SELECTED_FILE = "selected_file"
    OBSIDIAN_VAULT = "obsidian_vault"


class CandidateStatus(str, Enum):
    """CoverageLedger 候选状态（spec §3.3）。每个候选必须且只能进入一种。"""
    READ = "read"
    UNSUPPORTED = "unsupported"
    UNREADABLE = "unreadable"
    SKIPPED_BY_POLICY = "skipped_by_policy"
    OUT_OF_SCOPE = "out_of_scope"
    CHANGED_DURING_SCAN = "changed_during_scan"
    QUARANTINED = "quarantined"


class CoverageStatus(str, Enum):
    """覆盖率状态。"""
    COMPLETE = "complete"
    PARTIAL = "partial"
    FAILED = "failed"


class MemoryKind(str, Enum):
    """MemoryRecord 类型（spec §3.4）。v3.2 扩展 CORRECTION。"""
    PREFERENCE = "preference"
    FACT = "fact"
    PROJECT = "project"
    EPISODE = "episode"
    PROCEDURE = "procedure"
    CORRECTION = "correction"  # v3.2 新增：纠错


class MemoryStatus(str, Enum):
    """MemoryRecord 状态。"""
    CANDIDATE = "candidate"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    QUARANTINED = "quarantined"
    SUPERSEDED = "superseded"


class Completeness(str, Enum):
    """MemoryRecord 完整性标记。"""
    VERIFIABLE = "verifiable"
    UNVERIFIABLE = "unverifiable"


class DuplicateDecision(str, Enum):
    """DuplicateGroup 决策。"""
    UNRESOLVED = "unresolved"
    LINK = "link"
    MERGE = "merge"
    KEEP_ALL = "keep_all"


class RecordMappingKind(str, Enum):
    """BuildManifest 中每条输入记录的归宿（spec §9.1）。"""
    PUBLISHED = "published"
    LINKED_TO_PUBLISHED = "linked_to_published"
    EXCLUDED_WITH_REASON = "excluded_with_reason"
    QUARANTINED = "quarantined"
    SUPERSEDED_WITH_EVIDENCE = "superseded_with_evidence"


class ReleaseStatus(str, Enum):
    """ReleaseChange 状态（spec §3.7）。"""
    APPLIED = "applied"
    VERIFIED = "verified"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"


# ---------------------------------------------------------------------------
# v3.1 §3-§4：自动数据源发现架构
# ---------------------------------------------------------------------------


class SourceCategory(str, Enum):
    """v3.1 §4.1 数据源分类。"""
    NATIVE_MEMORY = "native_memory"
    PROJECT_MEMORY = "project_memory"
    CONVERSATION_HISTORY = "conversation_history"
    CONTROL_SURFACE = "control_surface"
    SKILL_SURFACE = "skill_surface"
    KNOWLEDGE_SOURCE = "knowledge_source"
    RUNTIME_EVIDENCE = "runtime_evidence"
    IGNORED_RUNTIME_DATA = "ignored_runtime_data"
    UNKNOWN = "unknown"


class IngestionPolicy(str, Enum):
    """v3.1 §4.2 摄取策略。"""
    IMPORT_VERBATIM = "import_verbatim"        # 原生记忆原样导入后治理
    EXTRACT_CANDIDATES = "extract_candidates"  # 普通文档萃取候选
    GOVERN_ONLY = "govern_only"                # Instruction/Skill 只治理
    EVIDENCE_ONLY = "evidence_only"            # 运行时证据仅用于评估
    IGNORE = "ignore"                          # 忽略并说明


class Ownership(str, Enum):
    """v3.1 §4.2 所有权。"""
    EXTERNAL_READ_ONLY = "external_read_only"
    AGENT_MANAGED = "agent_managed"
    MEMORYGUARD_MANAGED = "memoryguard_managed"


class TargetRole(str, Enum):
    """v3.1 §4.2 目标角色。"""
    NONE = "none"
    TAKEOVER_INPUT = "takeover_input"
    TAKEOVER_TARGET = "takeover_target"


class SurfaceStatus(str, Enum):
    """v3.1 §3.4 表面探测状态。"""
    FOUND = "found"
    MISSING = "missing"
    UNSUPPORTED = "unsupported"
    PERMISSION_DENIED = "permission_denied"
    EXCLUDED_BY_USER = "excluded_by_user"
    NOT_APPLICABLE = "not_applicable"


class TargetCapability(str, Enum):
    """v3.1 §2.2 三种能力模式。"""
    EXPORT_ONLY = "export_only"
    SKILL_GATEWAY = "skill_gateway"
    NATIVE_TAKEOVER = "native_takeover"


class TakeoverState(str, Enum):
    """v3.1 §2.3 接管状态机。"""
    NOT_DETECTED = "not_detected"
    DISCOVERED = "discovered"
    SELECTED = "selected"
    CANONICALIZED = "canonicalized"
    RELEASE_PLANNED = "release_planned"
    PUBLISHED = "published"
    RUNTIME_VERIFIED = "runtime_verified"
    OPERATIONAL = "operational"
    DRIFTED = "drifted"
    PARTIAL = "partial"


# ---------------------------------------------------------------------------
# v3.2 §3：MCP 记忆后端 + 治理层
# ---------------------------------------------------------------------------


class DataPageMode(str, Enum):
    """v3.2 §3 数据页模式。"""
    SINGLE_AGENT = "single_agent"
    MULTI_AGENT_SHARED_MCP = "multi_agent_shared_mcp"


class MemoryWritePolicy(str, Enum):
    """v3.2 §4 写入策略。"""
    AUTO_ACCEPT = "auto_accept"                          # 默认：自动接收并整理
    AUTO_QUARANTINE_ON_RISK = "auto_quarantine_on_risk"  # 风险时隔离
    PROPOSE_ONLY = "propose_only"                        # 仅建议，不自动写入


class NativeMemoryMode(str, Enum):
    """v3.2 §6 原生记忆接管能力分级。

    不要假装所有 Agent 都能停用原生记忆：
    - DISABLED 只用于真实可关闭的 Agent
    - REDIRECTED/OBSERVED 用于无法关闭但可引导/监测的 Agent
    - UNSUPPORTED 用于只能手动导入/导出的 Agent
    """
    DISABLED = "disabled"           # 可关闭原生记忆，完全由 MCP 承接
    REDIRECTED = "redirected"       # 不能关闭，但规则/hook 引导读写 MCP
    OBSERVED = "observed"           # 无法控制，只监测漂移
    UNSUPPORTED = "unsupported"     # 只能手动导入/导出


class SharedMemoryStatus(str, Enum):
    """v3.2 §4.4 共享记忆状态。

    覆盖不是删除：SHADOWED 保留为影子，可恢复。
    """
    ACTIVE = "active"               # 当前有效
    LOW_CONFIDENCE = "low_confidence"  # 低置信度，待验证
    SHADOWED = "shadowed"           # 被新记忆覆盖，保留为影子
    CONFLICTED = "conflicted"       # 在冲突组中，待仲裁
    QUARANTINED = "quarantined"     # 被隔离（敏感/可疑）
    DELETED = "deleted"             # 软删除


class ExternalMCPLevel(str, Enum):
    """v3.2 §7 外部 MCP 检测分级。

    未知 tool 不默认调用，因为 tool 不保证只读。
    """
    L0_UNRECOGNIZABLE = "L0_unrecognizable"           # 无法识别
    L1_UNKNOWN_TOOLS = "L1_unknown_tools"             # 检测到 tools 但不确定是否只读
    L2_GENERIC_RESOURCES = "L2_generic_resources"      # 通用 MCP server
    L3_KNOWN_MEMORY_MCP = "L3_known_memory_mcp"        # 已知厂商 memory 后端
    L4_MEMORYGUARD_MCP = "L4_memoryguard_mcp"          # 自己


class ConflictResolution(str, Enum):
    """v3.2 §3.5 冲突组解决状态。"""
    UNRESOLVED = "unresolved"
    RESOLVED = "resolved"
    ESCALATED = "escalated"


class BindingStatus(str, Enum):
    """v3.2 §3.2 AgentBinding 状态。"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRIFTED = "drifted"


@dataclass
class MemorySurface:
    """v3.1 §3.5 AgentProfile 声明的单个本地表面。"""

    surface_id: str
    path_template: str  # 含 %HOME% / %WORKSPACE% / %APPDATA% 占位符
    surface_role: str   # native_memory / control_surface / skill_surface / runtime_evidence 等
    scope: str = "user"  # user / project / agent / session
    load_order: int = 0
    read_policy: str = "read_only"
    write_policy: str = "do_not_write"
    loader_evidence: str = ""  # 官方文档 URL 或 fixture 标识
    classification_confidence: float = 0.5
    category: SourceCategory = SourceCategory.UNKNOWN
    ingestion_policy: IngestionPolicy = IngestionPolicy.EXTRACT_CANDIDATES
    ownership: Ownership = Ownership.EXTERNAL_READ_ONLY
    target_role: TargetRole = TargetRole.NONE

    def to_dict(self) -> dict[str, Any]:
        return {
            "surface_id": self.surface_id, "path_template": self.path_template,
            "surface_role": self.surface_role, "scope": self.scope,
            "load_order": self.load_order, "read_policy": self.read_policy,
            "write_policy": self.write_policy, "loader_evidence": self.loader_evidence,
            "classification_confidence": self.classification_confidence,
            "category": self.category.value,
            "ingestion_policy": self.ingestion_policy.value,
            "ownership": self.ownership.value, "target_role": self.target_role.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MemorySurface":
        return cls(
            surface_id=data["surface_id"], path_template=data["path_template"],
            surface_role=data.get("surface_role", ""),
            scope=data.get("scope", "user"),
            load_order=data.get("load_order", 0),
            read_policy=data.get("read_policy", "read_only"),
            write_policy=data.get("write_policy", "do_not_write"),
            loader_evidence=data.get("loader_evidence", ""),
            classification_confidence=data.get("classification_confidence", 0.5),
            category=SourceCategory(data.get("category", "unknown")),
            ingestion_policy=IngestionPolicy(data.get("ingestion_policy", "extract_candidates")),
            ownership=Ownership(data.get("ownership", "external_read_only")),
            target_role=TargetRole(data.get("target_role", "none")),
        )


@dataclass
class AgentProfile:
    """v3.1 §3.5 声明式 Agent Profile（数据文件，不执行脚本）。"""

    profile_id: str
    product: str
    profile_version: str = "1"
    supported_platforms: list[str] = field(default_factory=lambda: ["windows", "macos", "linux"])
    verified_product_versions: list[str] = field(default_factory=list)
    detection_rules: list[dict[str, Any]] = field(default_factory=list)
    surfaces: list[MemorySurface] = field(default_factory=list)
    target_capability: TargetCapability = TargetCapability.EXPORT_ONLY
    evidence_urls: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id, "product": self.product,
            "profile_version": self.profile_version,
            "supported_platforms": list(self.supported_platforms),
            "verified_product_versions": list(self.verified_product_versions),
            "detection_rules": list(self.detection_rules),
            "surfaces": [s.to_dict() for s in self.surfaces],
            "target_capability": self.target_capability.value,
            "evidence_urls": list(self.evidence_urls),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentProfile":
        return cls(
            profile_id=data["profile_id"], product=data["product"],
            profile_version=data.get("profile_version", "1"),
            supported_platforms=list(data.get("supported_platforms", ["windows", "macos", "linux"])),
            verified_product_versions=list(data.get("verified_product_versions", [])),
            detection_rules=list(data.get("detection_rules", [])),
            surfaces=[MemorySurface.from_dict(s) for s in data.get("surfaces", [])],
            target_capability=TargetCapability(data.get("target_capability", "export_only")),
            evidence_urls=list(data.get("evidence_urls", [])),
        )


@dataclass
class AgentInstance:
    """v3.1 §3.2 AgentLocator 探测到的 Agent 实例。"""

    instance_id: str
    profile_id: str
    product: str
    profile_version: str = "1"
    platform: str = ""
    host_id: str = ""
    workspace: str = ""
    config_root: str = ""
    surfaces: list[dict[str, Any]] = field(default_factory=list)  # 探测结果，含 status/path
    target_capability: TargetCapability = TargetCapability.EXPORT_ONLY

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id, "profile_id": self.profile_id,
            "product": self.product, "profile_version": self.profile_version,
            "platform": self.platform, "host_id": self.host_id,
            "workspace": self.workspace, "config_root": self.config_root,
            "surfaces": list(self.surfaces),
            "target_capability": self.target_capability.value,
        }


@dataclass
class DiscoveryEntry:
    """v3.1 §3.4 DiscoveryLedger 单条记录。"""

    profile_id: str
    surface_id: str
    status: SurfaceStatus
    resolved_path: str = ""
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id, "surface_id": self.surface_id,
            "status": self.status.value, "resolved_path": self.resolved_path,
            "reason": self.reason,
        }


@dataclass
class DiscoveryLedger:
    """v3.1 §3.4 + §5.4 第一本账：Profile 声明的所有表面是否都有结果。"""

    instance_id: str = ""
    entries: list[DiscoveryEntry] = field(default_factory=list)

    def counts(self) -> dict[str, int]:
        c = {s.value: 0 for s in SurfaceStatus}
        valid = {s.value for s in SurfaceStatus}
        unaccounted = 0
        for e in self.entries:
            sv = e.status.value if hasattr(e.status, 'value') else str(e.status)
            if sv in valid:
                c[sv] += 1
            else:
                unaccounted += 1
        c["surface_count"] = len(self.entries)
        c["unaccounted_count"] = unaccounted
        return c

    def status(self) -> str:
        cnt = self.counts()
        if not self.entries:
            return "failed"
        if cnt["unaccounted_count"] > 0:
            return "partial"
        if cnt["missing"] > 0 or cnt["permission_denied"] > 0 or cnt["unsupported"] > 0:
            return "partial"
        return "complete"

    def to_dict(self) -> dict[str, Any]:
        cnt = self.counts()
        cnt["status"] = self.status()
        cnt["instance_id"] = self.instance_id
        cnt["entries"] = [e.to_dict() for e in self.entries]
        return cnt


@dataclass
class SelectionEntry:
    """v3.1 §4.3 SelectionManifest 单条用户勾选。"""

    surface_id: str
    resolved_path: str
    category: SourceCategory
    ingestion_policy: IngestionPolicy
    ownership: Ownership
    target_role: TargetRole
    selected: bool = True
    file_level: list[dict[str, Any]] = field(default_factory=list)  # 细化到文件级

    def to_dict(self) -> dict[str, Any]:
        return {
            "surface_id": self.surface_id, "resolved_path": self.resolved_path,
            "category": self.category.value,
            "ingestion_policy": self.ingestion_policy.value,
            "ownership": self.ownership.value, "target_role": self.target_role.value,
            "selected": self.selected, "file_level": list(self.file_level),
        }


@dataclass
class SelectionManifest:
    """v3.1 §4.3 用户分类勾选的快照。"""

    selection_id: str
    instance_id: str
    profile_id: str
    created_at: str = ""
    entries: list[SelectionEntry] = field(default_factory=list)
    authorization_summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "selection_id": self.selection_id, "instance_id": self.instance_id,
            "profile_id": self.profile_id, "created_at": self.created_at,
            "entries": [e.to_dict() for e in self.entries],
            "authorization_summary": dict(self.authorization_summary),
        }


# ---------------------------------------------------------------------------
# 稳定 ID 工具
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_hash(*parts: str) -> str:
    """稳定 ID 生成：对拼接字符串取 sha256 前 16 位。"""
    raw = "\x1f".join(parts).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def normalize_rel_path(path: str) -> str:
    """路径归一化：替换反斜杠为正斜杠，去前导 ./。"""
    p = path.replace("\\", "/").lstrip("./")
    return p


# ---------------------------------------------------------------------------
# SourceRoot（spec §3.2）
# ---------------------------------------------------------------------------


@dataclass
class SourceRoot:
    """用户授权的本地数据源（v3.1 §4.2 扩展字段）。"""

    root_id: str
    type: SourceRootType
    display_name: str
    path: str
    scope: str = "project"  # project | user
    authorized_at: str = ""
    recursive: bool = True
    follow_symlinks: bool = False
    include: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=list)
    enabled: bool = True
    # v3.1 §4.2 新字段
    agent_instance_id: str = ""           # 关联 AgentInstance
    surface_id: str = ""                  # 关联 MemorySurface
    source_category: str = "unknown"      # SourceCategory.value
    ingestion_policy: str = "extract_candidates"  # IngestionPolicy.value
    ownership: str = "external_read_only"  # Ownership.value
    target_role: str = "none"             # TargetRole.value

    def to_dict(self) -> dict[str, Any]:
        return {
            "root_id": self.root_id, "type": self.type.value,
            "display_name": self.display_name, "path": self.path,
            "scope": self.scope, "authorized_at": self.authorized_at,
            "recursive": self.recursive, "follow_symlinks": self.follow_symlinks,
            "include": list(self.include), "exclude": list(self.exclude),
            "enabled": self.enabled,
            "agent_instance_id": self.agent_instance_id,
            "surface_id": self.surface_id,
            "source_category": self.source_category,
            "ingestion_policy": self.ingestion_policy,
            "ownership": self.ownership, "target_role": self.target_role,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SourceRoot":
        return cls(
            root_id=data["root_id"], type=SourceRootType(data["type"]),
            display_name=data["display_name"], path=data["path"],
            scope=data.get("scope", "project"),
            authorized_at=data.get("authorized_at", ""),
            recursive=data.get("recursive", True),
            follow_symlinks=data.get("follow_symlinks", False),
            include=list(data.get("include", [])),
            exclude=list(data.get("exclude", [])),
            enabled=data.get("enabled", True),
            agent_instance_id=data.get("agent_instance_id", ""),
            surface_id=data.get("surface_id", ""),
            source_category=data.get("source_category", "unknown"),
            ingestion_policy=data.get("ingestion_policy", "extract_candidates"),
            ownership=data.get("ownership", "external_read_only"),
            target_role=data.get("target_role", "none"),
        )


# ---------------------------------------------------------------------------
# CoverageLedger（spec §3.3）
# ---------------------------------------------------------------------------


@dataclass
class CoverageEntry:
    """单个候选的覆盖率记录。"""

    source_root_id: str
    relative_path: str
    status: CandidateStatus
    reason: str = ""  # 非 read 状态的原因
    size: int = 0
    media_type: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_root_id": self.source_root_id,
            "relative_path": self.relative_path,
            "status": self.status.value, "reason": self.reason,
            "size": self.size, "media_type": self.media_type,
        }


@dataclass
class CoverageLedger:
    """覆盖率账本：证明扫描完整性。"""

    source_snapshot_id: str = ""
    entries: list[CoverageEntry] = field(default_factory=list)

    def counts(self) -> dict[str, int]:
        """按状态统计计数。

        v3.1 §1.4 P0：unaccounted_count 不再硬编码 0，
        而是统计 entries 中所有状态不在 CandidateStatus 枚举内的条目。
        任一预算截断/权限失败/扫描中变化都必须产生 ledger entry，
        不能用默认 0 冒充完整性。
        """
        c = {s.value: 0 for s in CandidateStatus}
        valid_status_set = {s.value for s in CandidateStatus}
        unaccounted = 0
        for e in self.entries:
            status_val = e.status.value if hasattr(e.status, 'value') else str(e.status)
            if status_val in valid_status_set:
                c[status_val] += 1
            else:
                unaccounted += 1
        c["candidate_count"] = len(self.entries)
        c["unaccounted_count"] = unaccounted
        return c

    def status(self) -> CoverageStatus:
        """判定覆盖率状态。

        v3.1 §1.4 P0：unaccounted > 0 时强制 PARTIAL，
        不能用默认 complete 掩盖静默漏项。
        """
        cnt = self.counts()
        if not self.entries:
            return CoverageStatus.FAILED
        if cnt["unaccounted_count"] > 0:
            return CoverageStatus.PARTIAL
        if cnt["unreadable"] > 0 or cnt["changed_during_scan"] > 0:
            return CoverageStatus.PARTIAL
        if cnt["unsupported"] > 0 or cnt["skipped_by_policy"] > 0:
            return CoverageStatus.PARTIAL
        return CoverageStatus.COMPLETE

    def to_dict(self) -> dict[str, Any]:
        cnt = self.counts()
        cnt["coverage_status"] = self.status().value
        cnt["source_snapshot_id"] = self.source_snapshot_id
        cnt["entries"] = [e.to_dict() for e in self.entries]
        return cnt

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CoverageLedger":
        entries = [CoverageEntry(
            source_root_id=e["source_root_id"],
            relative_path=e["relative_path"],
            status=CandidateStatus(e["status"]),
            reason=e.get("reason", ""), size=e.get("size", 0),
            media_type=e.get("media_type", ""),
        ) for e in data.get("entries", [])]
        return cls(source_snapshot_id=data.get("source_snapshot_id", ""), entries=entries)


# ---------------------------------------------------------------------------
# Memory IR（spec §3.4）
# ---------------------------------------------------------------------------


@dataclass
class SourceObject:
    """来源对象：一次扫描中读取到的稳定记录。"""

    source_object_id: str  # = hash(source_root_id + normalized_relative_path)
    source_root_id: str
    relative_path: str
    content_hash: str
    media_type: str = "text/plain"
    read_status: str = "read"
    captured_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_object_id": self.source_object_id,
            "source_root_id": self.source_root_id,
            "relative_path": self.relative_path,
            "content_hash": self.content_hash,
            "media_type": self.media_type, "read_status": self.read_status,
            "captured_at": self.captured_at,
        }


@dataclass
class Provenance:
    """记忆的来源追溯链。"""

    source_object_id: str
    locator: str  # line/span/message-id/json-pointer/canvas-node-id
    excerpt_hash: str
    source_revision: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_object_id": self.source_object_id, "locator": self.locator,
            "excerpt_hash": self.excerpt_hash, "source_revision": self.source_revision,
        }


@dataclass
class MemoryRecord:
    """规范化记忆记录。"""

    memory_id: str  # = hash(source_object_id + stable_locator + normalized_content_fingerprint)
    kind: MemoryKind
    title: str
    body: str
    scope: str = "project"
    confidence: float = 0.5
    provenance: list[Provenance] = field(default_factory=list)
    status: MemoryStatus = MemoryStatus.CANDIDATE
    completeness: Completeness = Completeness.VERIFIABLE
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "memory_id": self.memory_id, "kind": self.kind.value,
            "title": self.title, "body": self.body, "scope": self.scope,
            "confidence": self.confidence,
            "provenance": [p.to_dict() for p in self.provenance],
            "status": self.status.value, "completeness": self.completeness.value,
            "created_at": self.created_at,
        }


@dataclass
class DuplicateGroup:
    """重复候选组：TF-IDF 只生成候选，不自动删除。"""

    group_id: str
    member_ids: list[str]
    similarity_method: str = "tfidf_cosine"
    scores: list[float] = field(default_factory=list)
    decision: DuplicateDecision = DuplicateDecision.UNRESOLVED

    def to_dict(self) -> dict[str, Any]:
        return {
            "group_id": self.group_id, "member_ids": list(self.member_ids),
            "similarity_method": self.similarity_method,
            "scores": list(self.scores), "decision": self.decision.value,
        }


@dataclass
class DecisionEvent:
    """人工决策事件（追加到 decisions.jsonl）。"""

    event_id: str
    actor: str
    action: str
    target_ids: list[str]
    before_hash: str = ""
    after_hash: str = ""
    reason: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id, "actor": self.actor, "action": self.action,
            "target_ids": list(self.target_ids),
            "before_hash": self.before_hash, "after_hash": self.after_hash,
            "reason": self.reason, "created_at": self.created_at,
        }


# ---------------------------------------------------------------------------
# BuildManifest（spec §3.5）
# ---------------------------------------------------------------------------


@dataclass
class RecordMappingEntry:
    """单条输入记录在 BuildManifest 中的归宿。"""

    memory_id: str
    mapping: RecordMappingKind
    reason: str = ""
    target_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "memory_id": self.memory_id, "mapping": self.mapping.value,
            "reason": self.reason, "target_path": self.target_path,
        }


@dataclass
class BuildManifest:
    """结构性完整替换的证明。"""

    build_id: str
    source_snapshot_id: str
    policy_version: str = "memory-policy-v1"
    decision_log_hash: str = ""
    target_profile: str = "generic-markdown-v1"
    coverage_status: str = "unknown"  # v3.1 §1.4：不再硬编码 complete，由真实账本计算
    input_record_count: int = 0
    published_record_count: int = 0
    linked_record_count: int = 0
    excluded_record_count: int = 0
    quarantined_record_count: int = 0
    unaccounted_record_count: int = 0
    record_mappings: list[RecordMappingEntry] = field(default_factory=list)
    release_hash: str = ""

    def integrity_ok(self) -> bool:
        """五个完整性条件（spec §9.1）。"""
        return (
            self.unaccounted_record_count == 0
            and self.input_record_count
            == self.published_record_count + self.linked_record_count
            + self.excluded_record_count + self.quarantined_record_count
            and bool(self.release_hash)
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "build_id": self.build_id,
            "source_snapshot_id": self.source_snapshot_id,
            "policy_version": self.policy_version,
            "decision_log_hash": self.decision_log_hash,
            "target_profile": self.target_profile,
            "coverage_status": self.coverage_status,
            "input_record_count": self.input_record_count,
            "published_record_count": self.published_record_count,
            "linked_record_count": self.linked_record_count,
            "excluded_record_count": self.excluded_record_count,
            "quarantined_record_count": self.quarantined_record_count,
            "unaccounted_record_count": self.unaccounted_record_count,
            "record_mappings": [m.to_dict() for m in self.record_mappings],
            "release_hash": self.release_hash,
        }


# ---------------------------------------------------------------------------
# ReleaseChange（spec §3.7）
# ---------------------------------------------------------------------------


@dataclass
class ReleaseChange:
    """发布事务的原子切换记录。"""

    release_id: str
    build_id: str
    target_profile: str
    applied_at: str = ""
    backup_paths: list[str] = field(default_factory=list)
    changed_paths: list[str] = field(default_factory=list)
    verify_result: dict[str, Any] = field(default_factory=dict)
    status: ReleaseStatus = ReleaseStatus.APPLIED

    def to_dict(self) -> dict[str, Any]:
        return {
            "release_id": self.release_id, "build_id": self.build_id,
            "target_profile": self.target_profile, "applied_at": self.applied_at,
            "backup_paths": list(self.backup_paths),
            "changed_paths": list(self.changed_paths),
            "verify_result": dict(self.verify_result),
            "status": self.status.value,
        }


# ---------------------------------------------------------------------------
# Snapshot（spec §3.3 配套）
# ---------------------------------------------------------------------------


@dataclass
class SourceSnapshot:
    """一次扫描的稳定证据。"""

    snapshot_id: str
    created_at: str
    source_objects: list[SourceObject]
    coverage: CoverageLedger

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id, "created_at": self.created_at,
            "source_objects": [o.to_dict() for o in self.source_objects],
            "coverage": self.coverage.to_dict(),
        }


# ---------------------------------------------------------------------------
# v3.2 §3：MCP 记忆后端数据模型
# ---------------------------------------------------------------------------


@dataclass
class AgentBinding:
    """v3.2 §3.2 Agent 与 share_group 的绑定关系。

    native_memory_mode 必须基于真实能力声明，不能假装 disabled。
    """
    binding_id: str
    agent_instance_id: str
    share_group_id: str
    mcp_server_name: str
    native_memory_mode: NativeMemoryMode
    status: BindingStatus = BindingStatus.ACTIVE
    redirect_paths: list[str] = field(default_factory=list)
    bound_at: str = ""
    last_drift_check: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "agent_instance_id": self.agent_instance_id,
            "share_group_id": self.share_group_id,
            "mcp_server_name": self.mcp_server_name,
            "native_memory_mode": self.native_memory_mode.value,
            "status": self.status.value if hasattr(self.status, 'value') else str(self.status),
            "redirect_paths": list(self.redirect_paths),
            "bound_at": self.bound_at,
            "last_drift_check": self.last_drift_check,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentBinding":
        return cls(
            binding_id=data["binding_id"],
            agent_instance_id=data["agent_instance_id"],
            share_group_id=data["share_group_id"],
            mcp_server_name=data["mcp_server_name"],
            native_memory_mode=NativeMemoryMode(data.get("native_memory_mode", "unsupported")),
            status=BindingStatus(data.get("status", "active")),
            redirect_paths=list(data.get("redirect_paths", [])),
            bound_at=data.get("bound_at", ""),
            last_drift_check=data.get("last_drift_check", ""),
        )


@dataclass
class MemoryEvent:
    """v3.2 §3.3 Agent 写入 MCP 的原始事件。

    Agent 调用 memoryguard_memory_write 时产生，含自动整理执行的动作。
    """
    event_id: str
    agent_instance_id: str
    share_group_id: str
    raw_content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    auto_actions: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "agent_instance_id": self.agent_instance_id,
            "share_group_id": self.share_group_id,
            "raw_content": self.raw_content,
            "metadata": dict(self.metadata),
            "auto_actions": list(self.auto_actions),
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MemoryEvent":
        return cls(
            event_id=data["event_id"],
            agent_instance_id=data["agent_instance_id"],
            share_group_id=data["share_group_id"],
            raw_content=data["raw_content"],
            metadata=dict(data.get("metadata", {})),
            auto_actions=list(data.get("auto_actions", [])),
            created_at=data.get("created_at", ""),
        )


@dataclass
class SharedMemoryRecord:
    """v3.2 §3.4 MCP 中的记忆记录。

    覆盖不是删除：supersedes 保留旧 memory_id 列表，旧记录 status=SHADOWED。
    locked=True 防止自动覆盖。
    """
    memory_id: str
    body: str
    kind: MemoryKind
    status: SharedMemoryStatus
    confidence: float = 0.5
    provenance: list[Provenance] = field(default_factory=list)
    supersedes: list[str] = field(default_factory=list)
    conflict_group_id: str = ""
    locked: bool = False
    created_at: str = ""
    updated_at: str = ""
    agent_instance_id: str = ""  # 写入来源 Agent

    def to_dict(self) -> dict[str, Any]:
        return {
            "memory_id": self.memory_id,
            "body": self.body,
            "kind": self.kind.value,
            "status": self.status.value if hasattr(self.status, 'value') else str(self.status),
            "confidence": self.confidence,
            "provenance": [p.to_dict() for p in self.provenance],
            "supersedes": list(self.supersedes),
            "conflict_group_id": self.conflict_group_id,
            "locked": self.locked,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "agent_instance_id": self.agent_instance_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SharedMemoryRecord":
        provs = [Provenance(**p) for p in data.get("provenance", [])]
        return cls(
            memory_id=data["memory_id"],
            body=data["body"],
            kind=MemoryKind(data.get("kind", "fact")),
            status=SharedMemoryStatus(data.get("status", "active")),
            confidence=data.get("confidence", 0.5),
            provenance=provs,
            supersedes=list(data.get("supersedes", [])),
            conflict_group_id=data.get("conflict_group_id", ""),
            locked=data.get("locked", False),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            agent_instance_id=data.get("agent_instance_id", ""),
        )


@dataclass
class ConflictGroup:
    """v3.2 §3.5 冲突组：互斥记忆的集合。"""
    group_id: str
    member_ids: list[str]
    reason: str
    status: ConflictResolution = ConflictResolution.UNRESOLVED
    resolution: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "group_id": self.group_id,
            "member_ids": list(self.member_ids),
            "reason": self.reason,
            "status": self.status.value if hasattr(self.status, 'value') else str(self.status),
            "resolution": self.resolution,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConflictGroup":
        return cls(
            group_id=data["group_id"],
            member_ids=list(data["member_ids"]),
            reason=data["reason"],
            status=ConflictResolution(data.get("status", "unresolved")),
            resolution=data.get("resolution", ""),
            created_at=data.get("created_at", ""),
        )


@dataclass
class QuarantineEntry:
    """v3.2 §3.6 隔离条目：敏感/可疑记忆。

    secret/token/credential 自动进入隔离，不进入 active。
    """
    quarantine_id: str
    memory_id: str
    reason: str
    detected_pattern: str
    original_content: str
    quarantined_at: str = ""
    released: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "quarantine_id": self.quarantine_id,
            "memory_id": self.memory_id,
            "reason": self.reason,
            "detected_pattern": self.detected_pattern,
            "original_content": self.original_content,
            "quarantined_at": self.quarantined_at,
            "released": self.released,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QuarantineEntry":
        return cls(
            quarantine_id=data["quarantine_id"],
            memory_id=data["memory_id"],
            reason=data["reason"],
            detected_pattern=data["detected_pattern"],
            original_content=data["original_content"],
            quarantined_at=data.get("quarantined_at", ""),
            released=data.get("released", False),
        )
