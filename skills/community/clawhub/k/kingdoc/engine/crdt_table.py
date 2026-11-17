"""KingDoc CRDT 表格扩展引擎

把序列 CRDT 协同从智能文档扩展到电子表格与多维表格：
- 单元格级操作日志 + 向量时钟
- 冲突时保留双方修改并标记
- 支持电子表格（sheet）与多维表格（smartsheet）两种品类
- 全品类无冲突协作

本地实现，零第三方依赖。
"""
from __future__ import annotations

import json
import hashlib
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class VectorClock:
    """向量时钟：用于因果关系排序与冲突检测"""

    def __init__(self, clocks: Optional[Dict[str, int]] = None):
        self.clocks: Dict[str, int] = clocks or {}

    def increment(self, client_id: str) -> "VectorClock":
        """递增指定客户端的时钟"""
        new_clocks = dict(self.clocks)
        new_clocks[client_id] = new_clocks.get(client_id, 0) + 1
        return VectorClock(new_clocks)

    def merge(self, other: "VectorClock") -> "VectorClock":
        """合并两个向量时钟"""
        merged = {}
        all_keys = set(self.clocks.keys()) | set(other.clocks.keys())
        for k in all_keys:
            merged[k] = max(self.clocks.get(k, 0), other.clocks.get(k, 0))
        return VectorClock(merged)

    def happens_before(self, other: "VectorClock") -> bool:
        """self 是否发生在 other 之前"""
        if not self.clocks:
            return bool(other.clocks)
        for k, v in self.clocks.items():
            if v > other.clocks.get(k, 0):
                return False
        return self.clocks != other.clocks

    def is_concurrent(self, other: "VectorClock") -> bool:
        """是否并发（无因果关系）"""
        return not self.happens_before(other) and not other.happens_before(self) and self.clocks != other.clocks

    def to_dict(self) -> Dict[str, int]:
        return dict(self.clocks)

    def copy(self) -> "VectorClock":
        return VectorClock(dict(self.clocks))


class CellOperation:
    """单元格操作"""

    def __init__(self, cell_id: str, client_id: str, value: Any,
                 vector_clock: VectorClock, op_type: str = "set",
                 timestamp: Optional[float] = None):
        self.cell_id = cell_id
        self.client_id = client_id
        self.value = value
        self.vector_clock = vector_clock
        self.op_type = op_type  # set / delete
        self.timestamp = timestamp or time.time()
        self.op_id = hashlib.md5(
            f"{cell_id}:{client_id}:{self.timestamp}:{value}".encode()
        ).hexdigest()[:12]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "op_id": self.op_id,
            "cell_id": self.cell_id,
            "client_id": self.client_id,
            "value": self.value,
            "op_type": self.op_type,
            "vector_clock": self.vector_clock.to_dict(),
            "timestamp": self.timestamp,
        }


class CellState:
    """单元格状态（含冲突标记）"""

    def __init__(self, cell_id: str, row: int = 0, col: int = 0):
        self.cell_id = cell_id
        self.row = row
        self.col = col
        self.value: Any = None
        self.version: int = 0
        self.last_clock: Optional[VectorClock] = None
        self.conflict: bool = False
        self.conflict_values: List[Dict[str, Any]] = []
        self.history: List[CellOperation] = []

    def apply_operation(self, op: CellOperation) -> bool:
        """应用操作，返回是否产生冲突"""
        if self.last_clock is None:
            # 首次写入
            self.value = op.value
            self.version += 1
            self.last_clock = op.vector_clock.copy()
            self.history.append(op)
            return False

        if op.vector_clock.happens_before(self.last_clock):
            # 旧操作，忽略
            return False

        if self.last_clock.happens_before(op.vector_clock):
            # 新操作，直接覆盖
            self.value = op.value
            self.version += 1
            self.last_clock = op.vector_clock.copy()
            self.history.append(op)
            self.conflict = False
            self.conflict_values = []
            return False

        # 并发操作 → 冲突
        self.conflict = True
        self.conflict_values.append({
            "value": op.value,
            "client_id": op.client_id,
            "vector_clock": op.vector_clock.to_dict(),
            "timestamp": op.timestamp,
        })
        # 同时保留当前值作为冲突一方
        if self.value is not None:
            self.conflict_values.append({
                "value": self.value,
                "client_id": self.last_clock.clocks,
                "vector_clock": self.last_clock.to_dict(),
                "timestamp": self.history[-1].timestamp if self.history else 0,
            })
        self.history.append(op)
        return True

    def resolve_conflict(self, chosen_value: Any, chosen_client: str = "") -> None:
        """解决冲突"""
        self.value = chosen_value
        self.conflict = False
        self.conflict_values = []
        self.version += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cell_id": self.cell_id,
            "row": self.row,
            "col": self.col,
            "value": self.value,
            "version": self.version,
            "conflict": self.conflict,
            "conflict_values": self.conflict_values,
            "history_count": len(self.history),
        }


class CRDTTableEngine:
    """CRDT 表格扩展引擎"""

    SUPPORTED_CATEGORIES: Dict[str, str] = {
        "sheet": "电子表格",
        "smartsheet": "多维表格",
        "smart_note": "智能文档",
    }

    def __init__(self, backend: Any = None, db_path: Optional[str] = None):
        self.backend = backend
        self.db_path = db_path or self._default_db_path()
        self._sessions: Dict[str, "CRDTTableSession"] = {}
        self._init_db()

    def _default_db_path(self) -> str:
        skill_root = Path(__file__).resolve().parent.parent
        return str(skill_root / ".crdt_table.db")

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS crdt_sessions (
                    session_id TEXT PRIMARY KEY,
                    category TEXT,
                    client_id TEXT,
                    created_at TEXT,
                    cell_count INTEGER DEFAULT 0,
                    conflict_count INTEGER DEFAULT 0
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def create_session(self, session_id: str, category: str,
                       client_id: str) -> Dict[str, Any]:
        """创建 CRDT 表格协同会话"""
        if category not in self.SUPPORTED_CATEGORIES:
            return {
                "success": False,
                "error": f"不支持的品类: {category}。支持: {list(self.SUPPORTED_CATEGORIES.keys())}",
            }

        session = CRDTTableSession(session_id, category, client_id)
        self._sessions[session_id] = session

        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """INSERT OR REPLACE INTO crdt_sessions
                   (session_id, category, client_id, created_at, cell_count, conflict_count)
                   VALUES (?, ?, ?, ?, 0, 0)""",
                (session_id, category, client_id, datetime.now().isoformat()),
            )
            conn.commit()
        finally:
            conn.close()

        return {
            "success": True,
            "session_id": session_id,
            "category": category,
            "category_name": self.SUPPORTED_CATEGORIES[category],
            "client_id": client_id,
        }

    def get_session(self, session_id: str) -> Optional["CRDTTableSession"]:
        """获取会话"""
        return self._sessions.get(session_id)

    def list_sessions(self) -> Dict[str, Any]:
        """列出所有会话"""
        return {
            "total": len(self._sessions),
            "sessions": [
                {
                    "session_id": sid,
                    "category": s.category,
                    "client_id": s.client_id,
                    "cell_count": len(s.cells),
                    "conflict_count": sum(1 for c in s.cells.values() if c.conflict),
                }
                for sid, s in self._sessions.items()
            ],
        }

    def set_cell(self, session_id: str, cell_id: str, value: Any,
                 client_id: str, row: int = 0, col: int = 0) -> Dict[str, Any]:
        """设置单元格值"""
        session = self._sessions.get(session_id)
        if not session:
            return {"success": False, "error": f"会话不存在: {session_id}"}

        conflict = session.set_cell(cell_id, value, client_id, row, col)
        cell = session.cells[cell_id]

        return {
            "success": True,
            "cell_id": cell_id,
            "value": cell.value,
            "conflict": conflict,
            "version": cell.version,
            "conflict_values": cell.conflict_values if conflict else [],
        }

    def get_cell(self, session_id: str, cell_id: str) -> Dict[str, Any]:
        """获取单元格状态"""
        session = self._sessions.get(session_id)
        if not session:
            return {"success": False, "error": f"会话不存在: session_id"}

        cell = session.cells.get(cell_id)
        if not cell:
            return {"success": False, "error": f"单元格不存在: {cell_id}"}

        return {"success": True, **cell.to_dict()}

    def resolve_cell_conflict(self, session_id: str, cell_id: str,
                              chosen_value: Any, chosen_client: str = "") -> Dict[str, Any]:
        """解决单元格冲突"""
        session = self._sessions.get(session_id)
        if not session:
            return {"success": False, "error": f"会话不存在: {session_id}"}

        cell = session.cells.get(cell_id)
        if not cell:
            return {"success": False, "error": f"单元格不存在: {cell_id}"}

        if not cell.conflict:
            return {"success": False, "error": "该单元格无冲突"}

        cell.resolve_conflict(chosen_value, chosen_client)
        return {
            "success": True,
            "cell_id": cell_id,
            "value": cell.value,
            "conflict": False,
        }

    def get_conflicts(self, session_id: str) -> Dict[str, Any]:
        """获取所有冲突单元格"""
        session = self._sessions.get(session_id)
        if not session:
            return {"success": False, "error": f"会话不存在: {session_id}"}

        conflicts = [
            cell.to_dict()
            for cell in session.cells.values()
            if cell.conflict
        ]
        return {
            "success": True,
            "total_conflicts": len(conflicts),
            "conflicts": conflicts,
        }

    def get_table_state(self, session_id: str) -> Dict[str, Any]:
        """获取完整表格状态"""
        session = self._sessions.get(session_id)
        if not session:
            return {"success": False, "error": f"会话不存在: {session_id}"}

        cells = {cid: c.to_dict() for cid, c in session.cells.items()}
        conflicts = [c for c in session.cells.values() if c.conflict]

        return {
            "success": True,
            "session_id": session_id,
            "category": session.category,
            "total_cells": len(cells),
            "conflict_count": len(conflicts),
            "cells": cells,
        }


class CRDTTableSession:
    """CRDT 表格协同会话"""

    def __init__(self, session_id: str, category: str, client_id: str):
        self.session_id = session_id
        self.category = category
        self.client_id = client_id
        self.cells: Dict[str, CellState] = {}
        self.vector_clock = VectorClock()
        self.created_at = datetime.now().isoformat()

    def set_cell(self, cell_id: str, value: Any, client_id: str,
                 row: int = 0, col: int = 0) -> bool:
        """设置单元格值，返回是否产生冲突"""
        if cell_id not in self.cells:
            self.cells[cell_id] = CellState(cell_id, row, col)

        cell = self.cells[cell_id]
        self.vector_clock = self.vector_clock.increment(client_id)

        op = CellOperation(
            cell_id=cell_id,
            client_id=client_id,
            value=value,
            vector_clock=self.vector_clock.copy(),
            op_type="set",
        )

        return cell.apply_operation(op)


def get_crdt_table_engine(backend: Any = None) -> CRDTTableEngine:
    """工厂函数"""
    return CRDTTableEngine(backend=backend)


# ===========================================================================
# 模块级便捷函数
# ===========================================================================

def create_session(session_id: str, category: str, client_id: str) -> Dict[str, Any]:
    engine = get_crdt_table_engine()
    return engine.create_session(session_id, category, client_id)

def set_cell(session_id: str, cell_id: str, value: Any,
             client_id: str, row: int = 0, col: int = 0) -> Dict[str, Any]:
    engine = get_crdt_table_engine()
    return engine.set_cell(session_id, cell_id, value, client_id, row, col)

def get_cell(session_id: str, cell_id: str) -> Dict[str, Any]:
    engine = get_crdt_table_engine()
    return engine.get_cell(session_id, cell_id)

def resolve_conflict(session_id: str, cell_id: str, chosen_value: Any,
                     chosen_client: str = "") -> Dict[str, Any]:
    engine = get_crdt_table_engine()
    return engine.resolve_cell_conflict(session_id, cell_id, chosen_value, chosen_client)

def get_conflicts(session_id: str) -> Dict[str, Any]:
    engine = get_crdt_table_engine()
    return engine.get_conflicts(session_id)

def get_table_state(session_id: str) -> Dict[str, Any]:
    engine = get_crdt_table_engine()
    return engine.get_table_state(session_id)

def list_crdt_sessions() -> Dict[str, Any]:
    engine = get_crdt_table_engine()
    return engine.list_sessions()
