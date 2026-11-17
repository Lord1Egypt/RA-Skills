#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
state_accessor.py v2 — 统一的 _state 访问门面（DDD/Legacy 双维护）

第四轮审查修复: 引擎层和 DDD 层之间的唯一桥梁。
同时维护 _state dict 和 StateRoot，确保两条路径的一致性。
"""

import copy, logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

_log = logging.getLogger("state_accessor")


@dataclass
class ProgressSnapshot:
    written_count: int = 0
    total_planned: int = 0
    last_chapter: int = 0
    written_list: List[int] = field(default_factory=list)

    @classmethod
    def from_state(cls, progress: dict) -> "ProgressSnapshot":
        w = progress.get("written", 0)
        if isinstance(w, list):
            w = max(w) if w else 0
        return cls(
            written_count=int(w),
            total_planned=progress.get("total_planned", 0),
            last_chapter=progress.get("last_chapter", 0),
            written_list=list(progress.get("written_list", [])),
        )


@dataclass
class CharacterSnapshot:
    name: str
    state: str = "?"
    location: str = "?"
    identity: str = ""
    personality: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, name: str, data: dict) -> "CharacterSnapshot":
        return cls(
            name=name,
            state=data.get("state", "?"),
            location=data.get("location", "?"),
            identity=data.get("identity", ""),
            personality=data.get("personality", {}),
        )


class StateAccessor:
    """统一的 _state 访问门面 — 引擎层和 DDD 层的唯一桥梁

    规则:
      - 所有引擎通过此类读写状态，禁止直接操作 ns._state
      - 同时维护 _state dict（引擎层）和 StateRoot（DDD 层）的一致性
      - 写操作自动记录审计日志
      - save() 先通过 StateRoot 校验再持久化
    """

    def __init__(self, novel_state):
        self._ns = novel_state
        self._state_root = None  # DDD 聚合根缓存
        self._audit_log: List[str] = []

    # ── DDD 桥接 ──

    def _build_state_root(self):
        """从 _state dict 构建 DDD StateRoot，失败时返回 None"""
        try:
            from domain.state import StateRoot
            self._state_root = StateRoot.from_dict(self._ns._state)
        except Exception as e:
            _log.warning(f"StateAccessor: StateRoot.from_dict() 失败: {e}")
            self._state_root = None

    def _invalidate_root(self):
        self._state_root = None

    def validate_ddd(self) -> bool:
        """验证当前 _state 是否可以通过 DDD 校验"""
        try:
            self._build_state_root()
            return self._state_root is not None
        except Exception:
            return False

    def save(self):
        """统一持久化: 先 DDD 校验，再写磁盘，失败时 fallback 到原始 save"""
        # 先尝试 DDD 路径
        try:
            self._build_state_root()
            if self._state_root is not None:
                from infrastructure.state_repository import StateRepository
                repo = StateRepository(str(self._ns._state.get("_book_dir", ".")))
                repo.save(self._state_root)
                return
        except Exception as e:
            _log.debug(f"StateAccessor: DDD save failed ({e}), falling back to legacy")

        # Fallback: Legacy 路径
        try:
            self._ns.save()
        except Exception as e:
            _log.error(f"StateAccessor: 所有持久化路径失败: {e}")

    # ── Progress ──

    def get_progress(self) -> ProgressSnapshot:
        p = self._ns._state.get("progress", {})
        return ProgressSnapshot.from_state(p)

    def get_written_count(self) -> int:
        p = self._ns._state.get("progress", {})
        w = p.get("written", 0)
        return int(w) if not isinstance(w, list) else (max(w) if w else 0)

    def get_last_chapter(self) -> int:
        return self._ns._state.get("progress", {}).get("last_chapter", 0)

    def set_progress(self, snapshot: ProgressSnapshot):
        p = self._ns._state.setdefault("progress", {})
        p["written"] = snapshot.written_count
        p["total_planned"] = snapshot.total_planned
        p["last_chapter"] = snapshot.last_chapter
        p["written_list"] = list(snapshot.written_list)
        self._invalidate_root()
        self._audit("progress", f"written={snapshot.written_count}")

    # ── Meta ──

    def get_meta(self, key: str, default: Any = "") -> Any:
        return (self._ns._state.get("meta", {}) or {}).get(key, default)

    def set_meta(self, key: str, value: Any):
        m = self._ns._state.setdefault("meta", {})
        m[key] = value
        self._invalidate_root()
        self._audit("meta", f"{key}={value}")

    def get_platform(self) -> str:
        return self.get_meta("platform", "番茄")

    def get_genre(self) -> str:
        return self.get_meta("genre", "都市")

    def get_title(self) -> str:
        return self.get_meta("title", "")

    # ── Characters ──

    def get_characters(self) -> Dict[str, dict]:
        return self._ns._state.get("characters", {}) or {}

    def get_character(self, name: str) -> Optional[dict]:
        return self.get_characters().get(name)

    def get_all_character_snapshots(self) -> List[CharacterSnapshot]:
        return [
            CharacterSnapshot.from_dict(name, data)
            for name, data in self.get_characters().items()
        ]

    def set_character(self, name: str, data: dict):
        chars = self._ns._state.setdefault("characters", {})
        chars[name] = data
        self._invalidate_root()
        self._audit("characters", f"updated {name}")

    # ── Plot / Hooks ──

    def get_hooks(self) -> List[dict]:
        return self._ns._state.get("plot", {}).get("hooks", [])

    def get_active_hooks(self) -> List[dict]:
        return [h for h in self.get_hooks() if h.get("status", "active") != "resolved"]

    def get_resolved_hooks(self) -> List[str]:
        return self._ns._state.get("plot", {}).get("resolved_hooks", [])

    # ── Foreshadows ──

    def get_foreshadows(self) -> List[dict]:
        return self._ns._state.get("foreshadows", [])

    # ── Character States ──

    def get_character_states(self) -> dict:
        cs = self._ns._state.get("character_states", {})
        if isinstance(cs, list):
            return {}
        return cs

    # ── Global Memory ──

    def get_global_memory(self) -> dict:
        return self._ns._state.get("global_memory", {})

    # ── Settings ──

    def get_settings(self) -> list:
        return self._ns._state.get("settings", [])

    # ── Timeline ──

    def get_timeline(self) -> list:
        return self._ns._state.get("timeline", [])

    # ── Payoff Ledger ──

    def get_payoff_ledger(self) -> list:
        return self._ns._state.get("payoff_ledger", [])

    # ── Readers ──

    def get_readers(self) -> dict:
        return self._ns._state.get("readers", {})

    # ── 直接访问 _state（仅内部事务层使用）──

    def get_raw_state(self) -> dict:
        """获取原始 _state dict 引用（仅供 ChapterTransaction 等事务层使用）"""
        return self._ns._state

    def set_raw_field(self, key: str, value: Any):
        """直接设置 _state 字段（仅供事务层的 Promise 回调使用）"""
        self._ns._state[key] = value
        self._invalidate_root()

    # ── Audit ──

    def _audit(self, field: str, detail: str):
        entry = f"[{field}] {detail}"
        self._audit_log.append(entry)
        _log.debug(f"StateAccessor: {entry}")

    def get_audit_log(self) -> List[str]:
        return list(self._audit_log)

    def clear_audit_log(self):
        self._audit_log.clear()
