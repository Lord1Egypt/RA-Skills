"""v3.2 §5 SharedMemoryStore 共享记忆后端版本化存储（SQLite 底层）。

存储结构：
.memoryguard/shared-memory/<group-id>/
  memory.db                # SQLite 数据库（事实源）
    表：records / events / decisions / conflicts / quarantine / versions / active_version

关键约束：
- 覆盖不是删除：supersede 保留旧 memory_id，旧记录 status=SHADOWED
- locked=True 防止自动覆盖
- 所有写入可回滚到历史版本
- 版本快照保存全部 5 类数据（records + events + decisions + conflicts + quarantine）

并发与事务：
- WAL 模式 + busy_timeout=5000，多 Agent 并发写入由 SQLite 事务/锁保证
- 每个写操作用事务上下文（成功提交、异常回滚）

向后兼容：
- __init__ 检测旧 JSONL 文件时自动迁移到 SQLite，迁移后旧文件重命名为 .bak
"""
from __future__ import annotations

import contextlib
import json
import sqlite3
from pathlib import Path
from typing import Any

from .schema_v3 import (
    ConflictGroup, ConflictResolution,
    DecisionEvent,
    MemoryEvent,
    QuarantineEntry,
    SharedMemoryRecord, SharedMemoryStatus,
    MemoryKind, MemoryStatus,
    Provenance,
    stable_hash, _now_iso,
)


_SCHEMA = """
CREATE TABLE IF NOT EXISTS records (
    memory_id TEXT PRIMARY KEY,
    body TEXT NOT NULL,
    kind TEXT NOT NULL,
    status TEXT NOT NULL,
    confidence REAL NOT NULL DEFAULT 0.5,
    conflict_group_id TEXT DEFAULT '',
    locked INTEGER NOT NULL DEFAULT 0,
    supersedes TEXT DEFAULT '[]',
    provenance TEXT DEFAULT '[]',
    agent_instance_id TEXT DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    agent_instance_id TEXT NOT NULL,
    share_group_id TEXT NOT NULL,
    raw_content TEXT NOT NULL,
    metadata TEXT DEFAULT '{}',
    auto_actions TEXT DEFAULT '[]',
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS decisions (
    event_id TEXT PRIMARY KEY,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    target_ids TEXT DEFAULT '[]',
    before_hash TEXT DEFAULT '',
    after_hash TEXT DEFAULT '',
    reason TEXT DEFAULT '',
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS conflicts (
    group_id TEXT PRIMARY KEY,
    member_ids TEXT NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL,
    resolution TEXT DEFAULT '',
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS quarantine (
    quarantine_id TEXT PRIMARY KEY,
    memory_id TEXT NOT NULL,
    reason TEXT NOT NULL,
    detected_pattern TEXT DEFAULT '',
    original_content TEXT DEFAULT '',
    released INTEGER NOT NULL DEFAULT 0,
    quarantined_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS versions (
    version_id TEXT PRIMARY KEY,
    reason TEXT NOT NULL,
    created_at TEXT NOT NULL,
    snapshot TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS active_version (
    id INTEGER PRIMARY KEY DEFAULT 1,
    version_id TEXT
);
"""

# 允许通过 _update_record_field 更新的列（白名单，防 SQL 注入）
_RECORD_COLUMNS = {
    "body", "status", "kind", "confidence", "conflict_group_id",
    "locked", "supersedes", "provenance", "agent_instance_id",
    "created_at", "updated_at",
}


class SharedMemoryStore:
    """共享记忆后端版本化存储（SQLite 底层）。

    一个 share_group_id 对应一个独立的版本化存储。
    Agent 通过 MCP 写入 -> 自动整理 -> 写入 records 表。
    治理动作（编辑/合并/锁定/恢复/删除/回滚）记录为 DecisionEvent。
    """

    def __init__(self, workspace: str | Path, share_group_id: str):
        self.workspace = Path(workspace).resolve()
        self.group_id = share_group_id
        self.root = self.workspace / ".memoryguard" / "shared-memory" / share_group_id
        self.versions_dir = self.root / "versions"  # 仅用于旧数据迁移探测
        self.db_path = self.root / "memory.db"
        self._ensure_dirs()
        self._init_db()
        self._migrate_from_jsonl()

    def _ensure_dirs(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 连接与建表
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=5.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=5000")
        return conn

    @contextlib.contextmanager
    def _db(self):
        """只读连接：用完即关。"""
        conn = self._connect()
        try:
            yield conn
        finally:
            conn.close()

    @contextlib.contextmanager
    def _tx(self):
        """写事务连接：成功提交、异常回滚，用完即关。"""
        conn = self._connect()
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._db() as conn:
            conn.executescript(_SCHEMA)

    # ------------------------------------------------------------------
    # 行 <-> 对象 转换
    # ------------------------------------------------------------------

    def _insert_record(self, conn: sqlite3.Connection, record: SharedMemoryRecord) -> None:
        d = record.to_dict()
        conn.execute(
            """INSERT OR REPLACE INTO records
               (memory_id, body, kind, status, confidence, conflict_group_id, locked,
                supersedes, provenance, agent_instance_id, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (d["memory_id"], d["body"], d["kind"], d["status"], d["confidence"],
             d.get("conflict_group_id", ""), 1 if d.get("locked") else 0,
             json.dumps(d.get("supersedes", []), ensure_ascii=False),
             json.dumps(d.get("provenance", []), ensure_ascii=False),
             d.get("agent_instance_id", ""), d.get("created_at", ""), d.get("updated_at", "")),
        )

    def _row_to_record(self, row: sqlite3.Row) -> SharedMemoryRecord:
        d = {
            "memory_id": row["memory_id"],
            "body": row["body"],
            "kind": row["kind"],
            "status": row["status"],
            "confidence": row["confidence"],
            "conflict_group_id": row["conflict_group_id"] or "",
            "locked": bool(row["locked"]),
            "supersedes": json.loads(row["supersedes"] or "[]"),
            "provenance": json.loads(row["provenance"] or "[]"),
            "agent_instance_id": row["agent_instance_id"] or "",
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
        return SharedMemoryRecord.from_dict(d)

    def _insert_event(self, conn: sqlite3.Connection, event: MemoryEvent) -> None:
        d = event.to_dict()
        conn.execute(
            """INSERT OR REPLACE INTO events
               (event_id, agent_instance_id, share_group_id, raw_content, metadata, auto_actions, created_at)
               VALUES (?,?,?,?,?,?,?)""",
            (d["event_id"], d["agent_instance_id"], d["share_group_id"], d["raw_content"],
             json.dumps(d.get("metadata", {}), ensure_ascii=False),
             json.dumps(d.get("auto_actions", []), ensure_ascii=False),
             d.get("created_at", "")),
        )

    def _row_to_event(self, row: sqlite3.Row) -> MemoryEvent:
        d = {
            "event_id": row["event_id"],
            "agent_instance_id": row["agent_instance_id"],
            "share_group_id": row["share_group_id"],
            "raw_content": row["raw_content"],
            "metadata": json.loads(row["metadata"] or "{}"),
            "auto_actions": json.loads(row["auto_actions"] or "[]"),
            "created_at": row["created_at"],
        }
        return MemoryEvent.from_dict(d)

    def _insert_decision(self, conn: sqlite3.Connection, decision: DecisionEvent) -> None:
        d = decision.to_dict()
        conn.execute(
            """INSERT OR REPLACE INTO decisions
               (event_id, actor, action, target_ids, before_hash, after_hash, reason, created_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (d["event_id"], d["actor"], d["action"],
             json.dumps(d.get("target_ids", []), ensure_ascii=False),
             d.get("before_hash", ""), d.get("after_hash", ""),
             d.get("reason", ""), d.get("created_at", "")),
        )

    def _row_to_decision(self, row: sqlite3.Row) -> DecisionEvent:
        return DecisionEvent(
            event_id=row["event_id"], actor=row["actor"], action=row["action"],
            target_ids=json.loads(row["target_ids"] or "[]"),
            before_hash=row["before_hash"] or "",
            after_hash=row["after_hash"] or "",
            reason=row["reason"] or "",
            created_at=row["created_at"],
        )

    def _insert_conflict(self, conn: sqlite3.Connection, group: ConflictGroup) -> None:
        d = group.to_dict()
        conn.execute(
            """INSERT OR REPLACE INTO conflicts
               (group_id, member_ids, reason, status, resolution, created_at)
               VALUES (?,?,?,?,?,?)""",
            (d["group_id"], json.dumps(d.get("member_ids", []), ensure_ascii=False),
             d["reason"], d["status"], d.get("resolution", ""), d.get("created_at", "")),
        )

    def _row_to_conflict(self, row: sqlite3.Row) -> ConflictGroup:
        d = {
            "group_id": row["group_id"],
            "member_ids": json.loads(row["member_ids"] or "[]"),
            "reason": row["reason"],
            "status": row["status"],
            "resolution": row["resolution"] or "",
            "created_at": row["created_at"],
        }
        return ConflictGroup.from_dict(d)

    def _insert_quarantine(self, conn: sqlite3.Connection, entry: QuarantineEntry) -> None:
        d = entry.to_dict()
        conn.execute(
            """INSERT OR REPLACE INTO quarantine
               (quarantine_id, memory_id, reason, detected_pattern, original_content, released, quarantined_at)
               VALUES (?,?,?,?,?,?,?)""",
            (d["quarantine_id"], d["memory_id"], d["reason"],
             d.get("detected_pattern", ""), d.get("original_content", ""),
             1 if d.get("released") else 0, d.get("quarantined_at", "")),
        )

    def _row_to_quarantine(self, row: sqlite3.Row) -> QuarantineEntry:
        d = {
            "quarantine_id": row["quarantine_id"],
            "memory_id": row["memory_id"],
            "reason": row["reason"],
            "detected_pattern": row["detected_pattern"] or "",
            "original_content": row["original_content"] or "",
            "quarantined_at": row["quarantined_at"],
            "released": bool(row["released"]),
        }
        return QuarantineEntry.from_dict(d)

    # ------------------------------------------------------------------
    # 写入
    # ------------------------------------------------------------------

    def append_event(self, event: MemoryEvent) -> None:
        """追加原始写入事件。"""
        with self._tx() as conn:
            self._insert_event(conn, event)

    def update_event(self, event: MemoryEvent) -> None:
        """更新事件（回填 auto_actions）。仅在已存在时更新。"""
        d = event.to_dict()
        with self._tx() as conn:
            conn.execute(
                """UPDATE events SET agent_instance_id=?, share_group_id=?, raw_content=?,
                   metadata=?, auto_actions=?, created_at=? WHERE event_id=?""",
                (d["agent_instance_id"], d["share_group_id"], d["raw_content"],
                 json.dumps(d.get("metadata", {}), ensure_ascii=False),
                 json.dumps(d.get("auto_actions", []), ensure_ascii=False),
                 d.get("created_at", ""), d["event_id"]),
            )

    def append_record(self, record: SharedMemoryRecord) -> None:
        """追加记忆记录到 records 表。"""
        with self._tx() as conn:
            self._insert_record(conn, record)

    def append_decision(self, decision: DecisionEvent) -> None:
        """追加决策事件。"""
        with self._tx() as conn:
            self._insert_decision(conn, decision)

    def append_conflict(self, group: ConflictGroup) -> None:
        """追加冲突组。"""
        with self._tx() as conn:
            self._insert_conflict(conn, group)

    def append_quarantine(self, entry: QuarantineEntry) -> None:
        """追加隔离条目。"""
        with self._tx() as conn:
            self._insert_quarantine(conn, entry)

    # ------------------------------------------------------------------
    # 读取
    # ------------------------------------------------------------------

    def list_records(self, status: str | None = None,
                     kind: str | None = None) -> list[SharedMemoryRecord]:
        """列出记忆记录，可按 status/kind 过滤。"""
        sql = "SELECT * FROM records"
        clauses: list[str] = []
        params: list[Any] = []
        if status:
            clauses.append("status=?")
            params.append(status)
        if kind:
            clauses.append("kind=?")
            params.append(kind)
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY rowid"
        with self._db() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [self._row_to_record(r) for r in rows]

    def list_events(self) -> list[MemoryEvent]:
        """列出所有写入事件。"""
        with self._db() as conn:
            rows = conn.execute("SELECT * FROM events ORDER BY rowid").fetchall()
        return [self._row_to_event(r) for r in rows]

    def list_decisions(self) -> list[DecisionEvent]:
        """列出所有决策事件。"""
        with self._db() as conn:
            rows = conn.execute("SELECT * FROM decisions ORDER BY rowid").fetchall()
        return [self._row_to_decision(r) for r in rows]

    def list_conflicts(self) -> list[ConflictGroup]:
        """列出所有冲突组。"""
        with self._db() as conn:
            rows = conn.execute("SELECT * FROM conflicts ORDER BY rowid").fetchall()
        return [self._row_to_conflict(r) for r in rows]

    def list_quarantine(self) -> list[QuarantineEntry]:
        """列出所有隔离条目。"""
        with self._db() as conn:
            rows = conn.execute("SELECT * FROM quarantine ORDER BY rowid").fetchall()
        return [self._row_to_quarantine(r) for r in rows]

    def get_record(self, memory_id: str) -> SharedMemoryRecord | None:
        """获取单条记忆记录。"""
        with self._db() as conn:
            row = conn.execute(
                "SELECT * FROM records WHERE memory_id=?", (memory_id,)).fetchone()
        return self._row_to_record(row) if row else None

    def update_record(self, record: SharedMemoryRecord) -> None:
        """按 memory_id 覆盖写回单条记录。"""
        with self._tx() as conn:
            self._insert_record(conn, record)

    # ------------------------------------------------------------------
    # 治理动作
    # ------------------------------------------------------------------

    def supersede(self, old_id: str, new_id: str, reason: str,
                  actor: str = "auto") -> None:
        """覆盖旧记忆：old.status=SHADOWED, new.supersedes 追加 old_id。

        覆盖不是删除：旧记录保留为影子，可恢复。
        """
        now = _now_iso()
        with self._tx() as conn:
            conn.execute(
                "UPDATE records SET status=?, updated_at=? WHERE memory_id=?",
                (SharedMemoryStatus.SHADOWED.value, now, old_id),
            )
            row = conn.execute(
                "SELECT supersedes FROM records WHERE memory_id=?", (new_id,)).fetchone()
            if row is not None:
                try:
                    sup = json.loads(row["supersedes"] or "[]")
                except (ValueError, TypeError):
                    sup = []
                if old_id not in sup:
                    sup.append(old_id)
                conn.execute(
                    "UPDATE records SET supersedes=?, updated_at=? WHERE memory_id=?",
                    (json.dumps(sup, ensure_ascii=False), now, new_id),
                )
        # 记录 DecisionEvent
        decision = DecisionEvent(
            event_id=stable_hash("supersede", old_id, new_id, _now_iso()),
            actor=actor, action="auto_supersede",
            target_ids=[old_id, new_id],
            reason=reason, created_at=_now_iso(),
        )
        self.append_decision(decision)

    def quarantine_memory(self, memory_id: str, reason: str,
                          pattern: str, original_content: str = "") -> None:
        """隔离记忆：status=QUARANTINED + 写入 quarantine 表。

        original_content 默认空串，兼容 3 参数调用。
        """
        now = _now_iso()
        with self._tx() as conn:
            conn.execute(
                "UPDATE records SET status=?, updated_at=? WHERE memory_id=?",
                (SharedMemoryStatus.QUARANTINED.value, now, memory_id),
            )
        # 写入隔离条目
        entry = QuarantineEntry(
            quarantine_id=stable_hash("quar", memory_id, _now_iso()),
            memory_id=memory_id, reason=reason,
            detected_pattern=pattern, original_content=original_content,
            quarantined_at=_now_iso(),
        )
        self.append_quarantine(entry)
        # 记录 DecisionEvent
        decision = DecisionEvent(
            event_id=stable_hash("quarantine", memory_id, _now_iso()),
            actor="auto", action="auto_quarantine",
            target_ids=[memory_id],
            reason=reason, created_at=_now_iso(),
        )
        self.append_decision(decision)

    def conflict(self, member_ids: list[str], reason: str) -> str:
        """创建冲突组，返回 group_id。"""
        group_id = stable_hash("conflict", *member_ids, _now_iso())
        group = ConflictGroup(
            group_id=group_id, member_ids=member_ids,
            reason=reason, created_at=_now_iso(),
        )
        self.append_conflict(group)
        # 更新涉及记录的 status
        now = _now_iso()
        if member_ids:
            placeholders = ",".join("?" * len(member_ids))
            with self._tx() as conn:
                conn.execute(
                    f"UPDATE records SET status=?, conflict_group_id=?, updated_at=? "
                    f"WHERE memory_id IN ({placeholders})",
                    (SharedMemoryStatus.CONFLICTED.value, group_id, now, *member_ids),
                )
        # 记录 DecisionEvent
        decision = DecisionEvent(
            event_id=stable_hash("conflict_dec", group_id, _now_iso()),
            actor="auto", action="auto_conflict",
            target_ids=member_ids, reason=reason,
            created_at=_now_iso(),
        )
        self.append_decision(decision)
        return group_id

    def lock(self, memory_id: str) -> None:
        """锁定记忆（防止自动覆盖）。"""
        self._update_record_field(memory_id, "locked", True)

    def unlock(self, memory_id: str) -> None:
        """解锁记忆。"""
        self._update_record_field(memory_id, "locked", False)

    def restore(self, memory_id: str) -> None:
        """恢复 shadowed 记忆为 active。"""
        self._update_record_field(memory_id, "status", SharedMemoryStatus.ACTIVE.value)
        decision = DecisionEvent(
            event_id=stable_hash("restore", memory_id, _now_iso()),
            actor="user", action="restore",
            target_ids=[memory_id], reason="manual restore",
            created_at=_now_iso(),
        )
        self.append_decision(decision)

    def delete(self, memory_id: str) -> None:
        """软删除记忆。"""
        self._update_record_field(memory_id, "status", SharedMemoryStatus.DELETED.value)
        decision = DecisionEvent(
            event_id=stable_hash("delete", memory_id, _now_iso()),
            actor="user", action="delete",
            target_ids=[memory_id], reason="manual delete",
            created_at=_now_iso(),
        )
        self.append_decision(decision)

    def edit(self, memory_id: str, body: str) -> None:
        """编辑记忆正文。"""
        self._update_record_field(memory_id, "body", body)
        self._update_record_field(memory_id, "updated_at", _now_iso())
        decision = DecisionEvent(
            event_id=stable_hash("edit", memory_id, _now_iso()),
            actor="user", action="edit",
            target_ids=[memory_id], reason="manual edit",
            created_at=_now_iso(),
        )
        self.append_decision(decision)

    def _update_record_field(self, memory_id: str, field: str, value: Any) -> None:
        """更新记录的某个字段（白名单列，防 SQL 注入）。"""
        if field not in _RECORD_COLUMNS:
            return
        if field == "locked":
            col_val: Any = 1 if value else 0
        elif field == "supersedes":
            col_val = json.dumps(list(value), ensure_ascii=False)
        elif field == "provenance":
            col_val = json.dumps(
                [p.to_dict() if hasattr(p, "to_dict") else p for p in value],
                ensure_ascii=False)
        else:
            col_val = value
        with self._tx() as conn:
            conn.execute(
                f"UPDATE records SET {field}=? WHERE memory_id=?",
                (col_val, memory_id),
            )

    # ------------------------------------------------------------------
    # 版本管理
    # ------------------------------------------------------------------

    def create_version_snapshot(self, reason: str = "") -> str:
        """创建版本快照（保存全部 5 类数据），返回 version_id。"""
        version_id = stable_hash("v", self.group_id, _now_iso())
        created_at = _now_iso()
        records = self.list_records()
        snapshot = {
            "records": [r.to_dict() for r in records],
            "events": [e.to_dict() for e in self.list_events()],
            "decisions": [d.to_dict() for d in self.list_decisions()],
            "conflicts": [c.to_dict() for c in self.list_conflicts()],
            "quarantine": [q.to_dict() for q in self.list_quarantine()],
        }
        with self._tx() as conn:
            conn.execute(
                "INSERT INTO versions(version_id, reason, created_at, snapshot) VALUES (?,?,?,?)",
                (version_id, reason, created_at,
                 json.dumps(snapshot, ensure_ascii=False)),
            )
            conn.execute(
                "INSERT OR REPLACE INTO active_version(id, version_id) VALUES(1,?)",
                (version_id,),
            )
        return version_id

    def _set_active_version(self, version_id: str) -> None:
        with self._tx() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO active_version(id, version_id) VALUES(1,?)",
                (version_id,),
            )

    def get_active_version_id(self) -> str | None:
        with self._db() as conn:
            row = conn.execute(
                "SELECT version_id FROM active_version WHERE id=1").fetchone()
        if row is None or not row["version_id"]:
            return None
        return row["version_id"]

    def rollback_to_version(self, version_id: str) -> None:
        """回滚到指定版本（恢复全部 5 类数据）。"""
        with self._db() as conn:
            row = conn.execute(
                "SELECT snapshot FROM versions WHERE version_id=?",
                (version_id,),
            ).fetchone()
        if row is None:
            raise FileNotFoundError(f"version not found: {version_id}")
        # 先备份当前状态
        self.create_version_snapshot(f"pre-rollback to {version_id}")
        # 恢复全部 5 类数据
        try:
            snapshot = json.loads(row["snapshot"])
        except (ValueError, TypeError):
            snapshot = {}
        self._restore_snapshot(snapshot)
        # 更新 active 指针
        self._set_active_version(version_id)
        # 记录 DecisionEvent
        decision = DecisionEvent(
            event_id=stable_hash("rollback", version_id, _now_iso()),
            actor="user", action="rollback",
            target_ids=[version_id], reason=f"rollback to {version_id}",
            created_at=_now_iso(),
        )
        self.append_decision(decision)

    def _restore_snapshot(self, snapshot: dict[str, Any]) -> None:
        """用快照原子覆盖全部 5 类数据表。"""
        with self._tx() as conn:
            for table in ("records", "events", "decisions", "conflicts", "quarantine"):
                conn.execute(f"DELETE FROM {table}")
            for d in snapshot.get("records", []):
                try:
                    self._insert_record(conn, SharedMemoryRecord.from_dict(d))
                except (ValueError, KeyError):
                    continue
            for d in snapshot.get("events", []):
                try:
                    self._insert_event(conn, MemoryEvent.from_dict(d))
                except (ValueError, KeyError):
                    continue
            for d in snapshot.get("decisions", []):
                try:
                    self._insert_decision(conn, DecisionEvent(
                        event_id=d["event_id"], actor=d.get("actor", "user"),
                        action=d.get("action", ""),
                        target_ids=list(d.get("target_ids", [])),
                        before_hash=d.get("before_hash", ""),
                        after_hash=d.get("after_hash", ""),
                        reason=d.get("reason", ""),
                        created_at=d.get("created_at", ""),
                    ))
                except (ValueError, KeyError):
                    continue
            for d in snapshot.get("conflicts", []):
                try:
                    self._insert_conflict(conn, ConflictGroup.from_dict(d))
                except (ValueError, KeyError):
                    continue
            for d in snapshot.get("quarantine", []):
                try:
                    self._insert_quarantine(conn, QuarantineEntry.from_dict(d))
                except (ValueError, KeyError):
                    continue

    def list_versions(self) -> list[dict]:
        """列出所有版本。"""
        with self._db() as conn:
            rows = conn.execute(
                "SELECT version_id, reason, created_at, snapshot FROM versions "
                "ORDER BY created_at").fetchall()
        versions: list[dict] = []
        for row in rows:
            try:
                snap = json.loads(row["snapshot"])
            except (ValueError, TypeError):
                snap = {}
            recs = snap.get("records", [])
            versions.append({
                "version_id": row["version_id"],
                "share_group_id": self.group_id,
                "created_at": row["created_at"],
                "reason": row["reason"],
                "record_count": len(recs),
                "active_count": sum(1 for r in recs if r.get("status") == "active"),
                "shadowed_count": sum(1 for r in recs if r.get("status") == "shadowed"),
                "quarantined_count": sum(1 for r in recs if r.get("status") == "quarantined"),
                "conflicted_count": sum(1 for r in recs if r.get("status") == "conflicted"),
            })
        return versions

    # ------------------------------------------------------------------
    # 统计
    # ------------------------------------------------------------------

    def status(self) -> dict[str, Any]:
        """返回共享组状态统计。"""
        records = self.list_records()
        events = self.list_events()
        decisions = self.list_decisions()
        conflicts = self.list_conflicts()
        quarantine = self.list_quarantine()
        return {
            "share_group_id": self.group_id,
            "total_records": len(records),
            "active": sum(1 for r in records if r.status == SharedMemoryStatus.ACTIVE),
            "shadowed": sum(1 for r in records if r.status == SharedMemoryStatus.SHADOWED),
            "conflicted": sum(1 for r in records if r.status == SharedMemoryStatus.CONFLICTED),
            "quarantined": sum(1 for r in records if r.status == SharedMemoryStatus.QUARANTINED),
            "deleted": sum(1 for r in records if r.status == SharedMemoryStatus.DELETED),
            "total_events": len(events),
            "total_decisions": len(decisions),
            "total_conflicts": len(conflicts),
            "total_quarantine": len(quarantine),
            "active_version": self.get_active_version_id(),
        }

    # ------------------------------------------------------------------
    # 向后兼容：从旧 JSONL 迁移
    # ------------------------------------------------------------------

    def _migrate_from_jsonl(self) -> None:
        """检测旧 JSONL 文件并迁移到 SQLite，迁移后重命名为 .bak。"""
        jsonl_map = [
            ("records.jsonl", self._migrate_records_jsonl),
            ("events.jsonl", self._migrate_events_jsonl),
            ("decisions.jsonl", self._migrate_decisions_jsonl),
            ("conflicts.jsonl", self._migrate_conflicts_jsonl),
            ("quarantine.jsonl", self._migrate_quarantine_jsonl),
        ]
        for name, migrator in jsonl_map:
            path = self.root / name
            if path.exists():
                try:
                    migrator(path)
                except Exception:
                    # 迁移失败不阻塞初始化；旧文件保留以便重试
                    continue
                try:
                    path.rename(path.with_suffix(".bak"))
                except OSError:
                    pass
        # 迁移 active 指针
        active = self.root / "active.json"
        if active.exists():
            try:
                data = json.loads(active.read_text(encoding="utf-8"))
                vid = data.get("version_id")
                if vid:
                    self._set_active_version(vid)
            except (ValueError, OSError):
                pass
            try:
                active.rename(active.with_suffix(".bak"))
            except OSError:
                pass
        # 迁移旧 versions 目录
        self._migrate_versions_dir()

    @staticmethod
    def _read_jsonl(path: Path) -> list[dict]:
        if not path.exists():
            return []
        out: list[dict] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
        return out

    def _migrate_records_jsonl(self, path: Path) -> None:
        with self._tx() as conn:
            for d in self._read_jsonl(path):
                try:
                    self._insert_record(conn, SharedMemoryRecord.from_dict(d))
                except (ValueError, KeyError):
                    continue

    def _migrate_events_jsonl(self, path: Path) -> None:
        with self._tx() as conn:
            for d in self._read_jsonl(path):
                try:
                    self._insert_event(conn, MemoryEvent.from_dict(d))
                except (ValueError, KeyError):
                    continue

    def _migrate_decisions_jsonl(self, path: Path) -> None:
        with self._tx() as conn:
            for d in self._read_jsonl(path):
                try:
                    self._insert_decision(conn, DecisionEvent(
                        event_id=d["event_id"], actor=d.get("actor", "user"),
                        action=d.get("action", ""),
                        target_ids=list(d.get("target_ids", [])),
                        before_hash=d.get("before_hash", ""),
                        after_hash=d.get("after_hash", ""),
                        reason=d.get("reason", ""),
                        created_at=d.get("created_at", ""),
                    ))
                except (ValueError, KeyError):
                    continue

    def _migrate_conflicts_jsonl(self, path: Path) -> None:
        with self._tx() as conn:
            for d in self._read_jsonl(path):
                try:
                    self._insert_conflict(conn, ConflictGroup.from_dict(d))
                except (ValueError, KeyError):
                    continue

    def _migrate_quarantine_jsonl(self, path: Path) -> None:
        with self._tx() as conn:
            for d in self._read_jsonl(path):
                try:
                    self._insert_quarantine(conn, QuarantineEntry.from_dict(d))
                except (ValueError, KeyError):
                    continue

    def _migrate_versions_dir(self) -> None:
        if not self.versions_dir.exists():
            return
        for vdir in self.versions_dir.iterdir():
            if not vdir.is_dir():
                continue
            manifest: dict[str, Any] = {}
            mpath = vdir / "manifest.json"
            if mpath.exists():
                try:
                    manifest = json.loads(mpath.read_text(encoding="utf-8"))
                except (ValueError, OSError):
                    manifest = {}
            version_id = manifest.get("version_id") or vdir.name
            reason = manifest.get("reason", "")
            created_at = manifest.get("created_at", "")
            snapshot = {
                "records": self._read_jsonl(vdir / "records.jsonl"),
                "events": [],
                "decisions": self._read_jsonl(vdir / "decisions.jsonl"),
                "conflicts": [],
                "quarantine": [],
            }
            with self._tx() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO versions(version_id, reason, created_at, snapshot) "
                    "VALUES (?,?,?,?)",
                    (version_id, reason, created_at,
                     json.dumps(snapshot, ensure_ascii=False)),
                )
        try:
            self.versions_dir.rename(self.root / "versions.bak")
        except OSError:
            pass
