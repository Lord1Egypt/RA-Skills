"""v3.1 §5 Canonical Memory Store 规范记忆核心。

事实源划分（§5.1）：
- 原始 Agent 记忆文件：不可变证据源；接管前保留基线
- Canonical Memory Store：MemoryGuard 受治理的期望状态事实源  ← 本模块
- DecisionLog：用户治理决定的追加式事实源
- Neuron View：可删除、可重建的控制面投影
- Agent Release：Agent 当前实际加载的运行事实

文件结构（§5.2）：
.memoryguard/managed-memory/<agent-instance-id>/
  versions/<version-id>/
    records.jsonl       # MemoryRecord 列表
    relations.jsonl     # 关系
    provenance.jsonl    # 来源追溯
    decisions.jsonl     # 决策事件
    manifest.json       # 版本元信息
  active.json           # 当前活跃版本指针

关键约束：
- 每条记录至少一个可定位 Provenance
- 重复检测只生成候选关系，不删除来源
- 图上治理操作只追加 DecisionEvent，然后生成新版本，不直接改投影
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .schema_v3 import (
    DecisionEvent, MemoryRecord, Provenance, stable_hash, _now_iso,
)


@dataclass
class MemoryVersion:
    """单个版本元信息。"""

    version_id: str
    agent_instance_id: str
    created_at: str = ""
    parent_version_id: str = ""
    decision_count: int = 0
    record_count: int = 0
    relation_count: int = 0
    provenance_count: int = 0
    content_hash: str = ""  # 该版本所有 records 的稳定 hash
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "version_id": self.version_id,
            "agent_instance_id": self.agent_instance_id,
            "created_at": self.created_at,
            "parent_version_id": self.parent_version_id,
            "decision_count": self.decision_count,
            "record_count": self.record_count,
            "relation_count": self.relation_count,
            "provenance_count": self.provenance_count,
            "content_hash": self.content_hash,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MemoryVersion":
        return cls(
            version_id=data["version_id"],
            agent_instance_id=data.get("agent_instance_id", ""),
            created_at=data.get("created_at", ""),
            parent_version_id=data.get("parent_version_id", ""),
            decision_count=data.get("decision_count", 0),
            record_count=data.get("record_count", 0),
            relation_count=data.get("relation_count", 0),
            provenance_count=data.get("provenance_count", 0),
            content_hash=data.get("content_hash", ""),
            notes=data.get("notes", ""),
        )


class ManagedStore:
    """v3.1 §5 Canonical Memory Store。

    一个 agent_instance_id 对应一个独立的版本化存储。
    每次决策追加 → 复制上一版本 → 应用决策 → 生成新版本。
    """

    def __init__(self, workspace: str | Path, agent_instance_id: str):
        self.workspace = Path(workspace).resolve()
        self.agent_instance_id = agent_instance_id
        self.root = self.workspace / ".memoryguard" / "managed-memory" / agent_instance_id
        self.versions_dir = self.root / "versions"
        self.active_path = self.root / "active.json"

    # ------------------------------------------------------------------
    # 活跃版本指针
    # ------------------------------------------------------------------

    def get_active_version_id(self) -> str | None:
        """读取 active.json 中的当前活跃版本 ID。"""
        if not self.active_path.exists():
            return None
        try:
            data = json.loads(self.active_path.read_text(encoding="utf-8"))
            return data.get("version_id")
        except (OSError, ValueError):
            return None

    def _set_active_version_id(self, version_id: str) -> None:
        self.active_path.parent.mkdir(parents=True, exist_ok=True)
        self.active_path.write_text(
            json.dumps({
                "version_id": version_id,
                "agent_instance_id": self.agent_instance_id,
                "updated_at": _now_iso(),
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def get_active_version(self) -> MemoryVersion | None:
        vid = self.get_active_version_id()
        if vid is None:
            return None
        return self.load_version(vid)

    def load_version(self, version_id: str) -> MemoryVersion | None:
        vdir = self.versions_dir / version_id
        mpath = vdir / "manifest.json"
        if not mpath.exists():
            return None
        try:
            data = json.loads(mpath.read_text(encoding="utf-8"))
            return MemoryVersion.from_dict(data)
        except (OSError, ValueError):
            return None

    # ------------------------------------------------------------------
    # 读写 records / decisions
    # ------------------------------------------------------------------

    def list_records(self, version_id: str | None = None) -> list[MemoryRecord]:
        vid = version_id or self.get_active_version_id()
        if vid is None:
            return []
        rfile = self.versions_dir / vid / "records.jsonl"
        if not rfile.exists():
            return []
        records: list[MemoryRecord] = []
        for line in rfile.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                provs = [Provenance(**p) for p in d.get("provenance", [])]
                from .schema_v3 import MemoryKind, MemoryStatus, Completeness
                records.append(MemoryRecord(
                    memory_id=d["memory_id"],
                    kind=MemoryKind(d.get("kind", "fact")),
                    title=d.get("title", ""),
                    body=d.get("body", ""),
                    scope=d.get("scope", "project"),
                    confidence=d.get("confidence", 0.5),
                    provenance=provs,
                    status=MemoryStatus(d.get("status", "candidate")),
                    completeness=Completeness(d.get("completeness", "verifiable")),
                    created_at=d.get("created_at", ""),
                ))
            except (ValueError, KeyError):
                continue
        return records

    def list_decisions(self, version_id: str | None = None) -> list[DecisionEvent]:
        vid = version_id or self.get_active_version_id()
        if vid is None:
            return []
        dfile = self.versions_dir / vid / "decisions.jsonl"
        if not dfile.exists():
            return []
        from .schema_v3 import DecisionEvent
        events: list[DecisionEvent] = []
        for line in dfile.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                events.append(DecisionEvent(
                    event_id=d["event_id"],
                    actor=d.get("actor", "user"),
                    action=d.get("action", ""),
                    target_ids=list(d.get("target_ids", [])),
                    before_hash=d.get("before_hash", ""),
                    after_hash=d.get("after_hash", ""),
                    reason=d.get("reason", ""),
                    created_at=d.get("created_at", ""),
                ))
            except (ValueError, KeyError):
                continue
        return events

    # ------------------------------------------------------------------
    # 版本管理
    # ------------------------------------------------------------------

    def create_initial_version(self, records: list[MemoryRecord]) -> MemoryVersion:
        """v3.1 §5 创建首个规范版本（从 Memory IR 导入）。"""
        version_id = stable_hash("v1", self.agent_instance_id, _now_iso())
        self._write_version(version_id, records, [], parent_version_id="")
        self._set_active_version_id(version_id)
        return self.load_version(version_id)  # type: ignore[return-value]

    def apply_decision(self, action: str, target_ids: list[str],
                       reason: str = "", actor: str = "user") -> MemoryVersion:
        """v3.1 §6.2 图上治理操作 → 追加 DecisionEvent → 生成新规范版本。

        不直接改记录，而是：
        1. 复制当前版本的 records
        2. 根据 action 修改对应记录的 status
        3. 写入 DecisionEvent
        4. 生成新版本，更新 active 指针
        """
        cur_vid = self.get_active_version_id()
        if cur_vid is None:
            raise RuntimeError("no active version; create initial version first")
        cur_records = self.list_records(cur_vid)
        cur_decisions = self.list_decisions(cur_vid)
        # 应用 action 到记录
        from .schema_v3 import MemoryStatus
        new_records: list[MemoryRecord] = []
        for r in cur_records:
            if r.memory_id in target_ids:
                r = self._apply_action_to_record(r, action)
            new_records.append(r)
        # 新 DecisionEvent
        event_id = stable_hash("decision", action, _now_iso(), *target_ids)
        before_hash = self._records_hash(cur_records)
        after_hash = self._records_hash(new_records)
        new_decision = DecisionEvent(
            event_id=event_id, actor=actor, action=action,
            target_ids=list(target_ids),
            before_hash=before_hash, after_hash=after_hash,
            reason=reason, created_at=_now_iso(),
        )
        all_decisions = cur_decisions + [new_decision]
        # 新版本
        new_vid = stable_hash(cur_vid, event_id, _now_iso())
        self._write_version(new_vid, new_records, all_decisions, parent_version_id=cur_vid)
        self._set_active_version_id(new_vid)
        return self.load_version(new_vid)  # type: ignore[return-value]

    def _apply_action_to_record(self, record: MemoryRecord, action: str) -> MemoryRecord:
        """根据图上操作修改记录状态。"""
        from .schema_v3 import MemoryStatus
        action_to_status = {
            "accept": MemoryStatus.ACCEPTED,
            "exclude": MemoryStatus.REJECTED,
            "quarantine": MemoryStatus.QUARANTINED,
            "supersede": MemoryStatus.SUPERSEDED,
            "merge": MemoryStatus.ACCEPTED,    # 合并候选 → accepted
            "rescope": MemoryStatus.ACCEPTED,  # 改作用域仍是 accepted
        }
        new_status = action_to_status.get(action)
        if new_status is not None:
            record.status = new_status
        return record

    def _records_hash(self, records: list[MemoryRecord]) -> str:
        content = json.dumps(
            [r.to_dict() for r in records],
            sort_keys=True, ensure_ascii=False,
        )
        return stable_hash(content)

    def _write_version(self, version_id: str, records: list[MemoryRecord],
                       decisions: list[DecisionEvent], parent_version_id: str = "") -> None:
        vdir = self.versions_dir / version_id
        vdir.mkdir(parents=True, exist_ok=True)
        # records.jsonl
        (vdir / "records.jsonl").write_text(
            "\n".join(json.dumps(r.to_dict(), ensure_ascii=False) for r in records) + "\n",
            encoding="utf-8",
        )
        # decisions.jsonl
        (vdir / "decisions.jsonl").write_text(
            "\n".join(json.dumps(d.to_dict(), ensure_ascii=False) for d in decisions) + "\n",
            encoding="utf-8",
        )
        # provenance.jsonl（聚合所有记录的 provenance）
        all_provs: list[dict[str, Any]] = []
        for r in records:
            for p in r.provenance:
                all_provs.append({
                    "memory_id": r.memory_id,
                    "source_object_id": p.source_object_id,
                    "locator": p.locator,
                    "excerpt_hash": p.excerpt_hash,
                    "source_revision": p.source_revision,
                })
        (vdir / "provenance.jsonl").write_text(
            "\n".join(json.dumps(p, ensure_ascii=False) for p in all_provs) + ("\n" if all_provs else ""),
            encoding="utf-8",
        )
        # relations.jsonl（首版为空，留作后续扩展）
        (vdir / "relations.jsonl").write_text("", encoding="utf-8")
        # manifest.json
        content_hash = self._records_hash(records)
        manifest = MemoryVersion(
            version_id=version_id,
            agent_instance_id=self.agent_instance_id,
            created_at=_now_iso(),
            parent_version_id=parent_version_id,
            decision_count=len(decisions),
            record_count=len(records),
            relation_count=0,
            provenance_count=len(all_provs),
            content_hash=content_hash,
            notes="" if not parent_version_id else f"fork from {parent_version_id}",
        )
        (vdir / "manifest.json").write_text(
            json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # ------------------------------------------------------------------
    # 列出所有版本
    # ------------------------------------------------------------------

    def list_versions(self) -> list[MemoryVersion]:
        if not self.versions_dir.exists():
            return []
        versions: list[MemoryVersion] = []
        for vdir in self.versions_dir.iterdir():
            if not vdir.is_dir():
                continue
            mpath = vdir / "manifest.json"
            if not mpath.exists():
                continue
            try:
                versions.append(MemoryVersion.from_dict(
                    json.loads(mpath.read_text(encoding="utf-8"))
                ))
            except (OSError, ValueError):
                continue
        versions.sort(key=lambda v: v.created_at)
        return versions


def find_record_by_node_id(workspace: str | Path, node_id: str) -> tuple[str | None, MemoryRecord | None]:
    """根据神经图节点 ID 找到对应版本和记录。

    支持的 node_id 格式：
    1. 完整 memory_id（16 位 hash）
    2. 投影节点 ID "claim-<memory_id[:12]>"
    3. stable_hash(memory_id)

    本函数遍历所有 agent_instance 的活跃版本，匹配 memory_id 或节点 id。
    """
    ws = Path(workspace).resolve()
    mm_root = ws / ".memoryguard" / "managed-memory"
    if not mm_root.exists():
        return None, None
    # 投影节点 ID → memory_id 前缀
    memory_id_prefix = ""
    if node_id.startswith("claim-"):
        memory_id_prefix = node_id[6:]  # 去掉 "claim-" 前缀
    for inst_dir in mm_root.iterdir():
        if not inst_dir.is_dir():
            continue
        store = ManagedStore(ws, inst_dir.name)
        records = store.list_records()
        for r in records:
            if r.memory_id == node_id or stable_hash(r.memory_id) == node_id:
                vid = store.get_active_version_id()
                return vid, r
            # 投影节点 ID 匹配：claim-<memory_id[:12]>
            if memory_id_prefix and r.memory_id.startswith(memory_id_prefix):
                vid = store.get_active_version_id()
                return vid, r
    return None, None
