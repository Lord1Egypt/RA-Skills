"""v3.1 §3.2 AgentLocator 有限候选发现。

四层职责：
- AgentLocator：发现本机已知 Agent 候选，只做有限元数据探测
- AgentProfile：声明该 Agent 的已知本地表面、分类、加载关系和版本证据
- SourceRegistry：保存用户已经授权读取的 SourceRoot
- SourceAdapter：对授权根执行 inventory/read，不负责猜 Agent

安全边界（v3.1 §3.3）：
允许：
1. 当前工作区及其 Profile 明确声明的祖先规则文件；
2. Skill/CLI 宿主显式传入的配置根；
3. Profile 声明的少量固定路径模板；
4. 用户点击"检测本机 Agent"后，对固定路径执行 exists/lstat 和有限数量统计；
5. 用户手工选择的其他目录。

禁止：
- 从用户主目录递归搜索所有名为 memory/context/data 的文件夹；
- 候选阶段读取正文；
- 探测 Cookie、凭据和浏览器数据；
- 通过未公开路径猜测厂商私有数据库；
- 把云端或 GUI 内存声称为已追溯。
"""
from __future__ import annotations

import json
import os
import platform
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .agent_profiles import AgentProfileRegistry, detect_surface
from .agent_mapping import (
    AGENT_PRODUCT_MAP, IGNORED_DIRS,
    product_for_dot_dir, is_known_product, detect_stale_status,
)
from .schema_v3 import (
    AgentInstance, AgentProfile, DiscoveryEntry, DiscoveryLedger,
    SurfaceStatus, TakeoverState, TargetCapability, stable_hash,
)


@dataclass
class AgentCandidate:
    """discover_candidates() 返回的候选条目。"""
    dir_path: str
    dir_name: str
    product: str            # "unknown" 表示未映射
    has_profile: bool       # 是否有完整 AgentProfile
    stale_status: str       # "active" / "stale" / "likely_uninstalled"
    marked_uninstalled: bool = False
    mtime_iso: str = ""
    size_bytes: int = 0
    file_count: int = 0
    days_since_modified: float = -1

    def to_dict(self) -> dict[str, Any]:
        return {
            "dir_path": self.dir_path,
            "dir_name": self.dir_name,
            "product": self.product,
            "has_profile": self.has_profile,
            "stale_status": self.stale_status,
            "marked_uninstalled": self.marked_uninstalled,
            "mtime_iso": self.mtime_iso,
            "size_bytes": self.size_bytes,
            "file_count": self.file_count,
            "days_since_modified": self.days_since_modified,
        }



@dataclass
class DetectionContext:
    """宿主显式传入的检测上下文（v3.1 §3.2）。"""

    workspace: str = ""
    host_id: str = ""
    config_root: str = ""
    platform: str = field(default_factory=lambda: platform.system().lower())

    @classmethod
    def from_workspace(cls, workspace: str | Path) -> "DetectionContext":
        return cls(
            workspace=str(workspace),
            host_id=os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME") or "localhost",
            platform=platform.system().lower(),
        )


class AgentLocator:
    """v3.1 §3.2 有限候选发现器。

    只做：
    1. 加载所有 Profile
    2. 对每个 Profile 的每个 surface 执行 exists/lstat
    3. 生成 DiscoveryLedger
    4. 返回 AgentInstance 列表

    不做：
    - 不读正文
    - 不递归扫描
    - 不猜测未公开路径
    """

    def __init__(self, workspace: str | Path, context: DetectionContext | None = None):
        self.workspace = Path(workspace).resolve()
        self.context = context or DetectionContext.from_workspace(self.workspace)
        self.registry = AgentProfileRegistry(self.workspace)

    def discover_candidates(self, *, include_uninstalled: bool = False,
                            include_stale: bool = True,
                            include_unknown: bool = True) -> list[AgentCandidate]:
        """扫描当前系统 HOME 下所有 .<dir>，返回 Agent 候选列表。

        只扫当前系统 HOME（Path.home()），不做跨系统探测。
        每个候选取 stale_status，并查 uninstalled.json 判断是否已标记卸载。

        参数:
            include_uninstalled: 是否包含已标记为 uninstalled 的候选
            include_stale: 是否包含 stale 候选
            include_unknown: 是否包含未映射的 unknown 目录
        """
        home = Path.home()
        uninstalled = self._load_uninstalled_set()
        candidates: list[AgentCandidate] = []

        try:
            entries = list(home.iterdir())
        except (OSError, PermissionError):
            return []

        for entry in entries:
            if not entry.is_dir():
                continue
            if not entry.name.startswith("."):
                continue
            if entry.name in IGNORED_DIRS:
                continue

            product = product_for_dot_dir(entry.name) or "unknown"
            if product == "unknown" and not include_unknown:
                continue

            marked = product in uninstalled
            if marked and not include_uninstalled:
                continue

            stale_info = detect_stale_status(entry)
            if stale_info["stale_status"] == "stale" and not include_stale:
                continue

            has_profile = product != "unknown" and is_known_product(product)

            candidate = AgentCandidate(
                dir_path=str(entry),
                dir_name=entry.name,
                product=product,
                has_profile=has_profile,
                stale_status=stale_info["stale_status"],
                marked_uninstalled=marked,
                mtime_iso=stale_info["mtime_iso"],
                size_bytes=stale_info["size_bytes"],
                file_count=stale_info["file_count"],
                days_since_modified=stale_info["days_since_modified"],
            )
            candidates.append(candidate)

        return candidates

    def _load_uninstalled_set(self) -> set[str]:
        """读取 .memoryguard/cleanup/uninstalled.json，返回已标记卸载的产品名集合。"""
        path = self.workspace / ".memoryguard" / "cleanup" / "uninstalled.json"
        if not path.exists():
            return set()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return set(data.get("products", []))
        except (ValueError, OSError):
            return set()

    def detect_instances(self) -> tuple[list[AgentInstance], dict[str, DiscoveryLedger]]:
        """检测所有 Profile 的实例。

        返回 (instances, ledgers_by_instance_id)。
        一个 Profile 只要有一个 surface FOUND 就算作 discovered。
        """
        instances: list[AgentInstance] = []
        ledgers: dict[str, DiscoveryLedger] = {}
        for profile in self.registry.list_profiles():
            instance, ledger = self._detect_one(profile)
            # v3.1 §3.4：只有至少一个 FOUND 才算 discovered
            found_count = sum(1 for e in ledger.entries if e.status == SurfaceStatus.FOUND)
            if found_count > 0:
                instances.append(instance)
                ledgers[instance.instance_id] = ledger
        return instances, ledgers

    def _detect_one(self, profile: AgentProfile) -> tuple[AgentInstance, DiscoveryLedger]:
        """探测单个 Profile 的所有 surface。"""
        instance_id = stable_hash(
            profile.profile_id,
            self.context.host_id,
            str(self.workspace),
        )
        surfaces_results: list[dict[str, Any]] = []
        entries: list[DiscoveryEntry] = []
        for surface in profile.surfaces:
            status, resolved = detect_surface(
                surface,
                home=Path.home(),
                workspace=self.workspace,
                appdata=os.environ.get("APPDATA", str(Path.home())),
            )
            entries.append(DiscoveryEntry(
                profile_id=profile.profile_id,
                surface_id=surface.surface_id,
                status=status,
                resolved_path=resolved,
                reason="" if status == SurfaceStatus.FOUND else f"surface {surface.surface_id} {status.value}",
            ))
            surfaces_results.append({
                "surface_id": surface.surface_id,
                "path_template": surface.path_template,
                "resolved_path": resolved,
                "status": status.value,
                "surface_role": surface.surface_role,
                "scope": surface.scope,
                "category": surface.category.value,
                "ingestion_policy": surface.ingestion_policy.value,
                "ownership": surface.ownership.value,
                "target_role": surface.target_role.value,
                "classification_confidence": surface.classification_confidence,
            })
        instance = AgentInstance(
            instance_id=instance_id,
            profile_id=profile.profile_id,
            product=profile.product,
            profile_version=profile.profile_version,
            platform=self.context.platform,
            host_id=self.context.host_id,
            workspace=str(self.workspace),
            config_root=self.context.config_root,
            surfaces=surfaces_results,
            target_capability=profile.target_capability,
        )
        ledger = DiscoveryLedger(instance_id=instance_id, entries=entries)
        return instance, ledger

    def get_selection_tree(self, instance_id: str) -> dict[str, Any]:
        """v3.1 §4.3 返回分类勾选树。

        结构：
        {
          "instance_id": ...,
          "profile_id": ...,
          "categories": [
            {
              "category": "native_memory",
              "files": [
                {
                  "path": "/abs/path",
                  "surface_id": "...",
                  "ingestion_policy": "import_verbatim",
                  "ownership": "agent_managed",
                  "target_role": "takeover_input",
                  "default_selected": True,
                  "status": "found"
                }
              ]
            }
          ]
        }
        """
        instances, ledgers = self.detect_instances()
        instance = next((i for i in instances if i.instance_id == instance_id), None)
        if instance is None:
            return {"error": f"instance not found: {instance_id}"}
        # 按 category 分组
        cat_map: dict[str, list[dict[str, Any]]] = {}
        for s in instance.surfaces:
            if s.get("status") != "found":
                continue  # 只展示找到的表面
            cat = s.get("category", "unknown")
            cat_map.setdefault(cat, []).append({
                "path": s["resolved_path"],
                "surface_id": s["surface_id"],
                "ingestion_policy": s.get("ingestion_policy", "extract_candidates"),
                "ownership": s.get("ownership", "external_read_only"),
                "target_role": s.get("target_role", "none"),
                "default_selected": s.get("ingestion_policy") == "import_verbatim",
                "status": s["status"],
            })
        categories = [
            {"category": cat, "files": files}
            for cat, files in cat_map.items()
        ]
        return {
            "instance_id": instance_id,
            "profile_id": instance.profile_id,
            "product": instance.product,
            "categories": categories,
        }

    def save_discovery(self, instances: list[AgentInstance],
                       ledgers: dict[str, DiscoveryLedger]) -> Path:
        """持久化 DiscoveryLedger 到 .memoryguard/discovery/。"""
        out_dir = self.workspace / ".memoryguard" / "discovery"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "latest.json"
        data = {
            "detected_at": ledgers and list(ledgers.values())[0].entries[0].reason or "",
            "context": {
                "workspace": str(self.workspace),
                "host_id": self.context.host_id,
                "platform": self.context.platform,
            },
            "instances": [i.to_dict() for i in instances],
            "ledgers": {k: v.to_dict() for k, v in ledgers.items()},
        }
        out_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return out_path


def compute_takeover_state(instance: AgentInstance,
                           ledger: DiscoveryLedger | None,
                           selection_committed: bool,
                           canonicalized: bool,
                           release_planned: bool,
                           published: bool,
                           runtime_verified: bool,
                           drifted: bool = False) -> TakeoverState:
    """v3.1 §2.3 接管状态机。

    优先级（从高到低）：
    DRIFTED > OPERATIONAL > PUBLISHED > RELEASE_PLANNED > CANONICALIZED >
    SELECTED > PARTIAL（覆盖缺口） > DISCOVERED > NOT_DETECTED
    """
    if drifted:
        return TakeoverState.DRIFTED
    if runtime_verified:
        return TakeoverState.OPERATIONAL
    if published:
        return TakeoverState.PUBLISHED
    if release_planned:
        return TakeoverState.RELEASE_PLANNED
    if canonicalized:
        return TakeoverState.CANONICALIZED
    if selection_committed:
        return TakeoverState.SELECTED
    # 覆盖缺口优先于 DISCOVERED（v3.1 §2.3：PARTIAL 表示部分覆盖）
    if ledger is not None:
        cnt = ledger.counts()
        if cnt.get("unaccounted_count", 0) > 0 or cnt.get("missing", 0) > 0:
            return TakeoverState.PARTIAL
    if instance is not None:
        return TakeoverState.DISCOVERED
    return TakeoverState.NOT_DETECTED
