"""
radial_memory/storage.py
─────────────────────────────────────────────────────────
JSON 文件持久化层。
所有数据存储在单个 origin.json 中，结构完整可移植。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .models import (
    Origin, Line, Node, StateSnapshot, FileChange, LEVELS
)


class Storage:
    """
    将 Origin（含所有 Line / Node / StateSnapshot）序列化为 JSON 文件。
    文件路径: <base_path>/origin.json
    """

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._origin_file = self.base_path / "origin.json"

    # ─────────────────────────────────────────────
    # 公开接口
    # ─────────────────────────────────────────────

    def save(self, origin: Origin) -> None:
        data = self._serialize_origin(origin)
        with open(self._origin_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self) -> Optional[Origin]:
        if not self._origin_file.exists():
            return None
        with open(self._origin_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self._deserialize_origin(data)

    def exists(self) -> bool:
        return self._origin_file.exists()

    # ─────────────────────────────────────────────
    # 序列化
    # ─────────────────────────────────────────────

    def _serialize_origin(self, origin: Origin) -> dict:
        return {
            "project_name": origin.project_name,
            "created_at": origin.created_at,
            "lines": {
                lid: self._serialize_line(line)
                for lid, line in origin.lines.items()
            },
        }

    def _serialize_line(self, line: Line) -> dict:
        return {
            "id": line.id,
            "name": line.name,
            "description": line.description,
            "created_at": line.created_at,
            "nodes": [self._serialize_node(n) for n in line.nodes],
        }

    def _serialize_node(self, node: Node) -> dict:
        return {
            "id": node.id,
            "line_id": node.line_id,
            "position": node.position,
            "created_at": node.created_at,
            "task_label": node.task_label,
            # summaries: key 存为 str（JSON 限制），反序列化时转回 int
            "summaries": {str(k): v for k, v in node.summaries.items()},
            "state": self._serialize_state(node.state) if node.state else None,
            "accumulated_history_summary": node.accumulated_history_summary,
        }

    @staticmethod
    def _serialize_state(state: StateSnapshot) -> dict:
        return {
            "conversation_summary": state.conversation_summary,
            "modified_files": [
                {
                    "path": f.path,
                    "change_type": f.change_type,
                    "diff_summary": f.diff_summary,
                }
                for f in state.modified_files
            ],
            "env_info": state.env_info,
            "todos": state.todos,
            "full_context": state.full_context,
        }

    # ─────────────────────────────────────────────
    # 反序列化
    # ─────────────────────────────────────────────

    def _deserialize_origin(self, data: dict) -> Origin:
        lines = {
            lid: self._deserialize_line(ldata)
            for lid, ldata in data.get("lines", {}).items()
        }
        return Origin(
            project_name=data["project_name"],
            created_at=data["created_at"],
            lines=lines,
        )

    def _deserialize_line(self, data: dict) -> Line:
        return Line(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            created_at=data["created_at"],
            nodes=[self._deserialize_node(n) for n in data.get("nodes", [])],
        )

    def _deserialize_node(self, data: dict) -> Node:
        summaries = {int(k): v for k, v in data.get("summaries", {}).items()}
        state = (
            self._deserialize_state(data["state"])
            if data.get("state")
            else None
        )
        return Node(
            id=data["id"],
            line_id=data["line_id"],
            position=data["position"],
            created_at=data["created_at"],
            task_label=data["task_label"],
            summaries=summaries,
            state=state,
            accumulated_history_summary=data.get("accumulated_history_summary", ""),
        )

    @staticmethod
    def _deserialize_state(data: dict) -> StateSnapshot:
        files = [
            FileChange(
                path=f["path"],
                change_type=f.get("change_type", "modified"),
                diff_summary=f.get("diff_summary", ""),
            )
            for f in data.get("modified_files", [])
        ]
        return StateSnapshot(
            conversation_summary=data["conversation_summary"],
            modified_files=files,
            env_info=data.get("env_info", {}),
            todos=data.get("todos", []),
            full_context=data.get("full_context", ""),
        )
