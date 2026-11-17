"""变更历史兼容层（v3.1 §8）。

问题背景：
- 旧规则修复 Change 字段：change_id / plan_id / verify_report / undo_plan
- 新记忆发布 ReleaseChange 字段：release_id / build_id / verify_result
- 旧实现把两类记录都写在 .memoryguard/changes/，list_releases 用 data["release_id"] 直接索引
- 旧 Change 文件存在时触发 KeyError: 'release_id'，整个页面崩溃

v3.1 修复策略：
- 新 Release 只写 .memoryguard/releases/
- 旧 changes/ 中误写的 Release 兼容读取
- 旧规则 Change 原地保留，标记为 rule_change
- 损坏 JSON 返回结构化 warning，不静默跳过
- rollback_release 先查 releases/，再兼容查 changes/
- undo_change 只接受 rule_change

HistoryEvent 统一两类记录为时间线。
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class HistoryRecordType(str, Enum):
    RULE_CHANGE = "rule_change"
    MEMORY_RELEASE = "memory_release"
    INVALID = "invalid_history_entry"


@dataclass
class HistoryWarning:
    """单条损坏或未知记录的结构化警告。"""
    file_name: str
    reason: str
    missing_keys: list[str] = field(default_factory=list)


@dataclass
class HistoryEvent:
    """统一时间线事件（spec §8.2）。"""
    file_name: str
    record_type: str  # rule_change | memory_release | invalid_history_entry
    schema_version: str = ""
    # 通用字段
    event_id: str = ""  # change_id 或 release_id
    plan_id: str = ""
    build_id: str = ""
    target_profile: str = ""
    applied_at: str = ""
    status: str = ""
    changed_count: int = 0
    # 原始数据（用于 rollback 路由）
    raw_data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "file_name": self.file_name,
            "record_type": self.record_type,
            "schema_version": self.schema_version,
            "event_id": self.event_id,
            "plan_id": self.plan_id,
            "build_id": self.build_id,
            "target_profile": self.target_profile,
            "applied_at": self.applied_at,
            "status": self.status,
            "changed_count": self.changed_count,
        }


def detect_record_type(data: dict[str, Any]) -> HistoryRecordType:
    """按字段形状识别记录类型（v3.1 §8.2）。

    - change_id + plan_id → rule_change
    - release_id + build_id → memory_release
    - 其他 → invalid_history_entry
    """
    has_change_keys = "change_id" in data and "plan_id" in data
    has_release_keys = "release_id" in data and "build_id" in data
    # 显式 schema_version / record_type 优先
    rt = data.get("record_type")
    if rt == "rule_change" or has_change_keys:
        return HistoryRecordType.RULE_CHANGE
    if rt == "memory_release" or has_release_keys:
        return HistoryRecordType.MEMORY_RELEASE
    return HistoryRecordType.INVALID


def load_history_record(path: Path) -> tuple[HistoryEvent | None, HistoryWarning | None]:
    """加载单条历史记录。

    返回 (event, warning)：
    - 解析成功：event 非空，warning 为 None
    - 损坏 JSON：event 为 None，warning 非空
    - 未知 schema：event 为 invalid，warning 描述缺失字段
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return None, HistoryWarning(
            file_name=path.name,
            reason=f"json parse failed: {e}",
        )
    if not isinstance(data, dict):
        return None, HistoryWarning(
            file_name=path.name,
            reason="top-level is not an object",
        )

    rt = detect_record_type(data)
    if rt == HistoryRecordType.INVALID:
        missing = []
        if "change_id" not in data and "release_id" not in data:
            missing.append("change_id or release_id")
        if "plan_id" not in data and "build_id" not in data:
            missing.append("plan_id or build_id")
        return (
            HistoryEvent(
                file_name=path.name,
                record_type=HistoryRecordType.INVALID.value,
                raw_data=data,
            ),
            HistoryWarning(
                file_name=path.name,
                reason="unknown record shape",
                missing_keys=missing,
            ),
        )

    if rt == HistoryRecordType.RULE_CHANGE:
        return HistoryEvent(
            file_name=path.name,
            record_type=rt.value,
            schema_version=data.get("schema_version", "2.1"),
            event_id=data.get("change_id", ""),
            plan_id=data.get("plan_id", ""),
            applied_at=data.get("applied_at", data.get("verified_at", "")),
            status=data.get("status", data.get("change", {}).get("status", "")),
            raw_data=data,
        ), None

    # memory_release
    return HistoryEvent(
        file_name=path.name,
        record_type=rt.value,
        schema_version=data.get("schema_version", "3.0"),
        event_id=data.get("release_id", ""),
        build_id=data.get("build_id", ""),
        target_profile=data.get("target_profile", ""),
        applied_at=data.get("applied_at", ""),
        status=data.get("status", ""),
        changed_count=len(data.get("changed_paths", [])),
        raw_data=data,
    ), None


def list_change_history(workspace: Path) -> dict[str, Any]:
    """列出所有变更历史（v3.1 §8.4）。

    返回：
        {
            "items": [HistoryEvent.to_dict(), ...],
            "warnings": [HistoryWarning.to_dict(), ...],
            "releases_dir_count": int,
            "changes_dir_count": int,
        }

    读取顺序：
        1. .memoryguard/releases/*.json  新记忆发布
        2. .memoryguard/changes/*.json   旧规则修复 + 旧误写的 Release
    """
    mg_dir = workspace / ".memoryguard"
    releases_dir = mg_dir / "releases"
    changes_dir = mg_dir / "changes"

    items: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    releases_count = 0
    changes_count = 0
    # v3.1 §8.3：用 event_id 去重，避免同一 Release 同时在 releases/ 和 changes/ 出现两次
    seen_event_ids: set[str] = set()

    # 1. 新 releases/（优先级高）
    if releases_dir.exists():
        for p in sorted(releases_dir.glob("*.json"), reverse=True):
            releases_count += 1
            event, warn = load_history_record(p)
            if event:
                # 优先取 releases/ 中的版本，标记后续同名 changes/ 跳过
                if event.event_id:
                    seen_event_ids.add(event.event_id)
                items.append(event.to_dict())
            if warn:
                warnings.append({
                    "file_name": warn.file_name,
                    "reason": warn.reason,
                    "missing_keys": warn.missing_keys,
                })

    # 2. 旧 changes/（兼容读取，不修改；与 releases/ 重复的跳过）
    if changes_dir.exists():
        for p in sorted(changes_dir.glob("*.json"), reverse=True):
            changes_count += 1
            event, warn = load_history_record(p)
            if event:
                # 如果是 memory_release 且 event_id 已在 releases/ 出现过，跳过避免重复
                if (event.record_type == "memory_release"
                        and event.event_id
                        and event.event_id in seen_event_ids):
                    continue
                items.append(event.to_dict())
            if warn:
                warnings.append({
                    "file_name": warn.file_name,
                    "reason": warn.reason,
                    "missing_keys": warn.missing_keys,
                })

    # 按时间倒序（applied_at 为空时排到末尾）
    items.sort(key=lambda x: x.get("applied_at", ""), reverse=True)

    return {
        "items": items,
        "warnings": warnings,
        "releases_dir_count": releases_count,
        "changes_dir_count": changes_count,
    }


def get_release(workspace: Path, release_id: str) -> dict[str, Any] | None:
    """获取单个 ReleaseChange 原始数据。

    查找顺序：
        1. .memoryguard/releases/<release_id>.json
        2. .memoryguard/changes/<release_id>.json  （旧误写位置兼容）
    """
    mg_dir = workspace / ".memoryguard"
    for d in (mg_dir / "releases", mg_dir / "changes"):
        p = d / f"{release_id}.json"
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                if detect_record_type(data) == HistoryRecordType.MEMORY_RELEASE:
                    return data
            except (OSError, json.JSONDecodeError):
                continue
    return None
